#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES = ROOT / "product" / "src" / "profiles"

def load(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def profile_path(profile_id: str) -> Path:
    mapping = {
        "generic-self-contained": PROFILES / "generic-self-contained.json",
        "microsoft-copilot": PROFILES / "microsoft-copilot.json",
    }
    if profile_id not in mapping:
        raise SystemExit(f"unknown provider profile: {profile_id}")
    return mapping[profile_id]

def build_one(application, ruleset, dataset, profile):
    if profile.get("packaging") != "self-contained-json":
        raise SystemExit(f"unsupported packaging: {profile.get('packaging')}")
    return {
        "adr_realization": {
            "format": "adr-app-builder/self-contained-json",
            "format_version": 1,
            "authority": {
                "generated_realization_is_normative": False,
                "dataset_is_authoritative_for_committed_application_state": True,
            },
            "provider": {"profile": profile["id"], "name": profile["provider"]},
            "application": application,
            "initialization": profile["initialization"],
            "ruleset": ruleset,
            "dataset": dataset,
        }
    }

def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--application", required=True, type=Path)
    p.add_argument("--ruleset", required=True, type=Path)
    p.add_argument("--dataset", required=True, type=Path)
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()
    application = load(args.application)
    ruleset = load(args.ruleset)
    dataset = load(args.dataset)
    build = load(args.build)
    if build.get("packaging_profile") != "self-contained-json":
        raise SystemExit("FS-001 supports only packaging_profile=self-contained-json")
    providers = build.get("providers")
    if not isinstance(providers, list) or not providers:
        raise SystemExit("build.providers must be a non-empty list")
    for provider_id in providers:
        profile = load(profile_path(provider_id))
        artifact = build_one(application, ruleset, dataset, profile)
        write_json(args.output_dir / f"{provider_id}.json", artifact)

if __name__ == "__main__":
    main()
