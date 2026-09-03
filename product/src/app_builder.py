#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES = ROOT / "product" / "src" / "profiles"
DEFAULT_ADR_REPOSITORY = "https://github.com/wiigelec/adr.git"
DEFAULT_ADR_API_REPOSITORY = "https://api.github.com/repos/wiigelec/adr"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def require_object(name, value):
    if not isinstance(value, dict):
        raise SystemExit(f"{name} must be a JSON object")

def require_string(name, value):
    if not isinstance(value, str) or not value:
        raise SystemExit(f"{name} must be a non-empty string")

def resolve_adr_main(repository: str) -> str:
    p = subprocess.run(["git", "ls-remote", repository, "refs/heads/main"], text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("unable to resolve ADR main: " + p.stderr.strip())
    parts = p.stdout.strip().split()
    if not parts:
        raise SystemExit("ADR main did not resolve")
    return parts[0]

def http_json(url: str):
    req = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"adr-app-builder"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise SystemExit(f"unable to consume ADR seed specs: {exc}")

def consume_adr_seed_specs(api_repository: str, commit: str):
    ref = urllib.parse.quote(commit, safe="")
    listing = http_json(f"{api_repository}/contents/product/src?ref={ref}")
    if not isinstance(listing, list):
        raise SystemExit("ADR product/src listing is not a directory")
    seeds = []
    for item in sorted(listing, key=lambda value: value.get("name", "")):
        name = item.get("name")
        if not isinstance(name, str) or not name.endswith(".seed.json"):
            continue
        path = item.get("path")
        if not isinstance(path, str):
            raise SystemExit("ADR seed entry missing path")
        content = http_json(f"{api_repository}/contents/{path}?ref={ref}")
        if content.get("encoding") != "base64":
            raise SystemExit(f"ADR seed {path} is not base64 encoded")
        raw = base64.b64decode(content["content"])
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise SystemExit(f"ADR seed {path} is invalid JSON: {exc}")
        require_object(f"ADR seed {path}", parsed)
        seeds.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest()})
    if not seeds:
        raise SystemExit("resolved ADR revision contains no accepted seed specs")
    return seeds

def app_builder_commit() -> str:
    dirty = subprocess.run(["git","status","--porcelain","--untracked-files=all"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    if dirty:
        raise SystemExit("App Builder worktree must be clean before building")
    return subprocess.run(["git","rev-parse","HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()

def profile(profile_id: str):
    path = PROFILES / f"{profile_id}.json"
    if not path.is_file():
        raise SystemExit(f"unknown profile: {profile_id}")
    return load(path)

def validate_sources(application, ruleset, dataset, build):
    for name, value in [("application",application),("ruleset",ruleset),("dataset",dataset),("build",build)]:
        require_object(name, value)
    require_string("application.id", application.get("id"))
    require_object("application.initialization", application.get("initialization"))
    instructions = application["initialization"].get("instructions")
    if not isinstance(instructions, list) or not instructions or not all(isinstance(item,str) and item for item in instructions):
        raise SystemExit("application.initialization.instructions must be a non-empty string list")
    require_object("dataset.instance", dataset.get("instance"))
    require_string("dataset.instance.id", dataset["instance"].get("id"))
    require_string("build.packaging_profile", build.get("packaging_profile"))
    providers = build.get("providers")
    if not isinstance(providers,list) or not providers or not all(isinstance(item,str) and item for item in providers) or len(set(providers)) != len(providers):
        raise SystemExit("build.providers must be a non-empty unique string list")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--application", required=True, type=Path)
    parser.add_argument("--ruleset", required=True, type=Path)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--adr-repository", default=DEFAULT_ADR_REPOSITORY)
    parser.add_argument("--adr-api-repository", default=DEFAULT_ADR_API_REPOSITORY)
    args = parser.parse_args()

    application = load(args.application)
    ruleset = load(args.ruleset)
    dataset = load(args.dataset)
    build = load(args.build)
    validate_sources(application, ruleset, dataset, build)

    packaging = profile(build["packaging_profile"])
    require_object("packaging.preservation", packaging.get("preservation"))
    if packaging.get("id") != build["packaging_profile"] or packaging["preservation"].get("writeback") != "complete-realization" or packaging["preservation"].get("preserve_non_dataset_realization_material") is not True:
        raise SystemExit("invalid FS-001 packaging profile")

    adr_commit = resolve_adr_main(args.adr_repository)
    consume_adr_seed_specs(args.adr_api_repository, adr_commit)
    builder_commit = app_builder_commit()

    for provider_id in build["providers"]:
        provider = profile(provider_id)
        require_object("provider.bootstrap", provider.get("bootstrap"))
        if provider.get("id") != provider_id or provider["bootstrap"].get("mode") != "initialize" or not provider["bootstrap"].get("instructions"):
            raise SystemExit(f"invalid provider profile: {provider_id}")
        artifact = {
            "adr_realization": {
                "format": packaging["format"],
                "format_version": packaging["format_version"],
                "provenance": {"adr_commit": adr_commit, "app_builder_commit": builder_commit},
                "authority": {
                    "generated_realization_is_normative": False,
                    "dataset_is_authoritative_for_committed_application_state": True
                },
                "provider": {"profile": provider_id, "name": provider["provider"]},
                "application": application,
                "initialization": {"application": application["initialization"], "provider": provider["bootstrap"]},
                "ruleset": ruleset,
                "dataset": dataset,
                "preservation": packaging["preservation"]
            }
        }
        output = args.output_dir / f"{provider_id}.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
