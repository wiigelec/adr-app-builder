#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
PROFILES = ROOT / "product" / "src" / "profiles"
DEFAULT_ADR_REPOSITORY = "https://github.com/wiigelec/adr.git"
APP_BUILDER_REPOSITORY = "https://github.com/wiigelec/adr-app-builder.git"
FS002_PROFILES = {"single-file", "split-files", "single-git", "split-git"}

GIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "ADR App Builder",
    "GIT_AUTHOR_EMAIL": "app-builder@adr.invalid",
    "GIT_COMMITTER_NAME": "ADR App Builder",
    "GIT_COMMITTER_EMAIL": "app-builder@adr.invalid",
}
GIT_INITIAL_MESSAGE = "ADR App Builder initial package"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")



_MISSING = object()


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2) + "\n").encode("utf-8")


def decode_json_pointer(pointer: str) -> tuple[str, ...]:
    if not isinstance(pointer, str):
        raise SystemExit("runtime tree selector must be a string")
    if pointer == "":
        return ()
    if not pointer.startswith("/"):
        raise SystemExit(f"invalid RFC 6901 source selector: {pointer}")
    tokens = []
    for raw in pointer[1:].split("/"):
        decoded = []
        i = 0
        while i < len(raw):
            if raw[i] != "~":
                decoded.append(raw[i])
                i += 1
                continue
            if i + 1 >= len(raw) or raw[i + 1] not in {"0", "1"}:
                raise SystemExit(f"invalid RFC 6901 source selector: {pointer}")
            decoded.append("~" if raw[i + 1] == "0" else "/")
            i += 2
        tokens.append("".join(decoded))
    return tuple(tokens)


def resolve_pointer(source, pointer: str):
    value = source
    for token in decode_json_pointer(pointer):
        if isinstance(value, dict):
            if token not in value:
                raise SystemExit(f"nonexistent source selector: {pointer}")
            value = value[token]
        elif isinstance(value, list):
            if not token.isdigit() or (len(token) > 1 and token.startswith("0")):
                raise SystemExit(f"nonexistent source selector: {pointer}")
            index = int(token)
            if index >= len(value):
                raise SystemExit(f"nonexistent source selector: {pointer}")
            value = value[index]
        else:
            raise SystemExit(f"nonexistent source selector: {pointer}")
    return value


def terminal_paths(value, prefix=()):
    if isinstance(value, dict):
        if not value:
            yield prefix
        else:
            for key, child in value.items():
                yield from terminal_paths(child, prefix + (key,))
    elif isinstance(value, list):
        if not value:
            yield prefix
        else:
            for index, child in enumerate(value):
                yield from terminal_paths(child, prefix + (str(index),))
    else:
        yield prefix


def new_container(value):
    if isinstance(value, dict):
        return {}
    if isinstance(value, list):
        return [_MISSING for _ in value]
    return _MISSING


def assign_reconstructed(root, source, tokens, selected):
    if not tokens:
        return copy.deepcopy(selected)
    out = root
    src = source
    for position, token in enumerate(tokens):
        last = position == len(tokens) - 1
        if isinstance(src, dict):
            child = src[token]
            if last:
                out[token] = copy.deepcopy(selected)
            else:
                if token not in out:
                    out[token] = new_container(child)
                out = out[token]
            src = child
        elif isinstance(src, list):
            index = int(token)
            child = src[index]
            if last:
                out[index] = copy.deepcopy(selected)
            else:
                if out[index] is _MISSING:
                    out[index] = new_container(child)
                out = out[index]
            src = child
        else:
            raise SystemExit("internal reconstruction failure")
    return root


def normalize_runtime_path(path: str) -> str:
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path:
        raise SystemExit(f"invalid relative output path: {path!r}")
    segments = path.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise SystemExit(f"invalid relative output path: {path}")
    if ".git" in segments:
        raise SystemExit(f"invalid relative output path: {path}")
    normalized = PurePosixPath(path).as_posix()
    if normalized != path:
        raise SystemExit(f"invalid relative output path: {path}")
    return normalized


def validate_tree_mapping(component: str, source, mapping):
    if not isinstance(mapping, dict) or not mapping:
        raise SystemExit(f"{component} tree mapping must be a non-empty object")

    entries = []
    normalized_paths = set()
    selectors = []
    for output_path, selector in mapping.items():
        normalized = normalize_runtime_path(output_path)
        if normalized in normalized_paths:
            raise SystemExit(f"duplicate normalized output path: {normalized}")
        normalized_paths.add(normalized)
        tokens = decode_json_pointer(selector)
        selected = resolve_pointer(source, selector)
        entries.append((normalized, selector, tokens, selected))
        selectors.append((selector, tokens))

    seen = set()
    for selector, _ in selectors:
        if selector in seen:
            raise SystemExit(f"duplicate source selector within {component} mapping: {selector}")
        seen.add(selector)

    for i, (selector_a, tokens_a) in enumerate(selectors):
        for selector_b, tokens_b in selectors[i + 1:]:
            shorter, longer = (
                (tokens_a, tokens_b)
                if len(tokens_a) <= len(tokens_b)
                else (tokens_b, tokens_a)
            )
            if longer[:len(shorter)] == shorter:
                raise SystemExit(
                    f"overlapping ancestor/descendant source selectors: {selector_a} / {selector_b}"
                )

    selector_tokens = [tokens for _, tokens in selectors]
    for terminal in terminal_paths(source):
        if not any(terminal[:len(tokens)] == tokens for tokens in selector_tokens):
            raise SystemExit(f"incomplete {component} tree mapping omits source material")

    reconstructed = new_container(source)
    for _, _, tokens, selected in entries:
        reconstructed = assign_reconstructed(reconstructed, source, tokens, selected)
    if reconstructed != source:
        raise SystemExit(
            f"{component} tree mapping cannot reconstruct a value semantically equal to the source"
        )
    return sorted(entries, key=lambda item: item[0])


def runtime_component_spec(build, component: str, source):
    runtime = build.get("runtime")
    if runtime is None:
        return {"representation": "file"}
    require_object("build.runtime", runtime)
    raw = runtime.get(component, {"representation": "file"})
    require_object(f"build.runtime.{component}", raw)
    representation = raw.get("representation", "file")
    if representation == "file":
        if "files" in raw:
            raise SystemExit(f"{component} file representation shall not define files mapping")
        return {"representation": "file"}
    if representation != "tree":
        raise SystemExit(f"unsupported runtime representation: {component}/{representation}")
    return {
        "representation": "tree",
        "entries": validate_tree_mapping(component, source, raw.get("files")),
    }


def realize_component(component: str, source, spec):
    if spec["representation"] == "file":
        path = f"{component}.json"
        return {path: json_bytes(source)}, {"kind": "file", "path": path}

    files = {}
    for output_path, _, _, selected in spec["entries"]:
        files[f"{component}/{output_path}"] = json_bytes(selected)
    return files, {"kind": "tree", "path": component}


def init_config_files(input_paths):
    return {
        "init-config/application.json": input_paths["application"].read_bytes(),
        "init-config/ruleset.json": input_paths["ruleset"].read_bytes(),
        "init-config/dataset.json": input_paths["dataset"].read_bytes(),
        "init-config/build.json": input_paths["build"].read_bytes(),
    }


def runtime_metadata_files(application, adr_repository: str, adr_commit: str, builder_commit: str):
    return {
        "application.json": json_bytes(application),
        "provenance.json": json_bytes(
            {
                "adr": {
                    "repository": str(adr_repository),
                    "commit": adr_commit,
                },
                "app_builder": {
                    "repository": APP_BUILDER_REPOSITORY,
                    "commit": builder_commit,
                },
            }
        ),
    }


def guidance_files(profile_id: str, role: str, component_refs):
    locations = "\n".join(
        f"- {name}: `{ref['path']}` ({ref['kind']})"
        for name, ref in sorted(component_refs.items())
    )
    if role == "single":
        role_text = (
            "This repository contains the runtime application definition, runtime Ruleset, "
            "and persisted runtime Dataset."
        )
        agents_role = (
            "Read the runtime application definition and apply its application-owned initialization "
            "instructions. Read the runtime Ruleset, initialize active working state from the runtime "
            "Dataset according to those semantics, maintain governed working state during the session, "
            "and persist it only when the user requests or accepts a save."
        )
    elif role == "ruleset":
        role_text = (
            "This repository contains the runtime application definition and runtime Ruleset. "
            "Persisted Dataset state is external."
        )
        agents_role = (
            "Read the local runtime application definition and apply its application-owned initialization "
            "instructions. The local runtime Ruleset defines behavior. Persisted Dataset state is external; "
            "ordinary application-state saves do not belong in this repository."
        )
    else:
        role_text = (
            "This repository contains the runtime application definition and persisted runtime Dataset. "
            "The applicable Ruleset is external."
        )
        agents_role = (
            "Read the local runtime application definition and apply its application-owned initialization "
            "instructions. The local runtime Dataset is persisted application state. The applicable runtime "
            "Ruleset is external. Initialize active working state from the Dataset according to governed "
            "semantics and persist current governed state only when the user requests or accepts a save."
        )

    readme = (
        "# ADR App Builder Generated Repository\n\n"
        f"Packaging profile: `{profile_id}`\n\n"
        f"{role_text}\n\n"
        "## Runtime components\n\n"
        f"{locations}\n\n"
        "## Initialization inputs\n\n"
        "`init-config/` contains byte-for-byte copies of the four App Builder CLI input files that "
        "created this repository. Those files reproduce the original build invocation; they are not "
        "runtime application, Ruleset, or Dataset authority.\n\n"
        "## Provenance\n\n"
        "`provenance.json` records the exact ADR and App Builder construction commits as immutable lineage "
        "and upgrade anchors. It is not application, Ruleset, Dataset, or active-session authority.\n\n"
        "## Working state and save\n\n"
        "Active application working state may be newer than the persisted Dataset. Governed edits do "
        "not automatically persist. A user-requested or user-accepted save writes current governed "
        "working state to the runtime Dataset while preserving non-Dataset realization material.\n"
    )

    tree_note = ""
    if any(ref["kind"] == "tree" for ref in component_refs.values()):
        tree_note = (
            "\nFor tree-backed runtime components, `init-config/build.json` records the build-owned "
            "RFC 6901 physical realization mapping. Use that mapping only to locate or reconstruct "
            "physical runtime material; it does not become Ruleset or Dataset semantic authority.\n"
        )

    agents = (
        "# Generated Application Agent Guidance\n\n"
        f"{agents_role}\n\n"
        "Active governed application working state is the current state for the active session and may "
        "differ from the last persisted Dataset. Ordinary conversation content is not automatically "
        "application state.\n\n"
        "Do not automatically save governed edits. Save only when the user requests or accepts save.\n\n"
        "During ordinary save, preserve the runtime application definition, runtime Ruleset material, "
        "`provenance.json`, `init-config/`, `README.md`, `AGENTS.md`, and all other non-Dataset realization "
        "material. Never use `init-config/dataset.json` as mutable runtime storage.\n"
        + tree_note
    )
    return {"README.md": readme.encode(), "AGENTS.md": agents.encode()}


def merge_files(*groups):
    merged = {}
    for group in groups:
        for path, content in group.items():
            if path in merged:
                raise SystemExit(f"package-owned path collision: {path}")
            merged[path] = content
    return merged

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


def consume_adr_seed_specs(repository: str, commit: str):
    """Consume accepted ADR seed specs from the exact resolved Git revision."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "adr"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, text=True, capture_output=True, check=True)
        fetch = subprocess.run(
            ["git", "fetch", "-q", "--depth=1", repository, commit],
            cwd=repo,
            text=True,
            capture_output=True,
        )
        if fetch.returncode != 0:
            raise SystemExit("unable to consume ADR seed specs: " + fetch.stderr.strip())
        fetched = subprocess.run(
            ["git", "rev-parse", "FETCH_HEAD"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        if fetched != commit:
            raise SystemExit(f"ADR seed fetch mismatch: expected {commit}, observed {fetched}")
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD", "--", "product/src"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.splitlines()
        paths = sorted(path for path in listing if path.endswith(".seed.json"))
        if not paths:
            raise SystemExit("resolved ADR revision contains no accepted seed specs")
        seeds = []
        for path in paths:
            raw = subprocess.run(
                ["git", "show", f"FETCH_HEAD:{path}"],
                cwd=repo,
                capture_output=True,
                check=True,
            ).stdout
            try:
                parsed = json.loads(raw.decode("utf-8"))
            except Exception as exc:
                raise SystemExit(f"ADR seed {path} is invalid JSON: {exc}")
            require_object(f"ADR seed {path}", parsed)
            seeds.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest()})
        return seeds

def app_builder_commit() -> str:
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    if dirty:
        raise SystemExit("App Builder worktree must be clean before building")
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def profile(profile_id: str):
    path = PROFILES / f"{profile_id}.json"
    if not path.is_file():
        raise SystemExit(f"unknown profile: {profile_id}")
    return load(path)


def validate_sources(application, ruleset, dataset, build):
    for name, value in [("application", application), ("ruleset", ruleset), ("dataset", dataset), ("build", build)]:
        require_object(name, value)
    require_string("application.id", application.get("id"))
    require_object("application.initialization", application.get("initialization"))
    instructions = application["initialization"].get("instructions")
    if not isinstance(instructions, list) or not instructions or not all(isinstance(item, str) and item for item in instructions):
        raise SystemExit("application.initialization.instructions must be a non-empty string list")
    require_object("dataset.instance", dataset.get("instance"))
    require_string("dataset.instance.id", dataset["instance"].get("id"))
    require_string("build.packaging_profile", build.get("packaging_profile"))
    providers = build.get("providers")
    if (
        not isinstance(providers, list)
        or not providers
        or not all(isinstance(item, str) and item for item in providers)
        or len(set(providers)) != len(providers)
    ):
        raise SystemExit("build.providers must be a non-empty unique string list")


def validate_fs002_profile(packaging, profile_id: str):
    if packaging.get("id") != profile_id:
        raise SystemExit(f"invalid FS-002 packaging profile id: {profile_id}")
    if packaging.get("package_type") != "ruleset-dataset":
        raise SystemExit(f"invalid FS-002 package type: {profile_id}")
    storage = packaging.get("storage")
    topology = packaging.get("topology")
    expected = {
        "single-file": ("file", "single"),
        "split-files": ("file", "split"),
        "single-git": ("git", "single"),
        "split-git": ("git", "split"),
    }[profile_id]
    if (storage, topology) != expected:
        raise SystemExit(f"invalid FS-002 storage/topology: {profile_id}")


def run_git(repo: Path, args: list[str], *, env_extra=None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        env=env,
    )
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed in {repo}: {p.stderr.strip()}")
    return p



def init_git_repo(repo: Path, files: dict[str, bytes]) -> None:
    repo.mkdir(parents=True, exist_ok=False)
    run_git(repo, ["init", "-q", "-b", "main"])
    for name in sorted(files):
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(files[name])
    run_git(repo, ["add", "--", *sorted(files)])

    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    commit_env = {
        **GIT_IDENTITY,
        "GIT_AUTHOR_DATE": created_at,
        "GIT_COMMITTER_DATE": created_at,
    }
    run_git(repo, ["commit", "-q", "-m", GIT_INITIAL_MESSAGE], env_extra=commit_env)


def build_fs002_package(
    output_dir: Path,
    profile_id: str,
    application,
    ruleset,
    dataset,
    build,
    input_paths,
    adr_repository: str,
    adr_commit: str,
    builder_commit: str,
) -> dict:
    package_dir = output_dir / "package"
    if package_dir.exists():
        raise SystemExit(f"package output already exists: {package_dir}")
    package_dir.mkdir(parents=True)

    if profile_id == "single-file":
        if build.get("runtime") is not None:
            raise SystemExit("FS-003 runtime realization is supported only for Git-backed profiles")
        write_json(package_dir / "package.json", {"ruleset": ruleset, "dataset": dataset})
        return {
            "profile": profile_id,
            "storage": "file",
            "topology": "single",
            "location": "../package/package.json",
            "components": {"ruleset": "ruleset", "dataset": "dataset"},
        }

    if profile_id == "split-files":
        if build.get("runtime") is not None:
            raise SystemExit("FS-003 runtime realization is supported only for Git-backed profiles")
        write_json(package_dir / "ruleset.json", ruleset)
        write_json(package_dir / "dataset.json", dataset)
        return {
            "profile": profile_id,
            "storage": "file",
            "topology": "split",
            "location": "../package",
            "components": {"ruleset": "ruleset.json", "dataset": "dataset.json"},
        }

    rules_spec = runtime_component_spec(build, "ruleset", ruleset)
    dataset_spec = runtime_component_spec(build, "dataset", dataset)
    rules_files, rules_ref = realize_component("ruleset", ruleset, rules_spec)
    dataset_files, dataset_ref = realize_component("dataset", dataset, dataset_spec)
    init_files = init_config_files(input_paths)
    runtime_metadata = runtime_metadata_files(
        application, adr_repository, adr_commit, builder_commit
    )
    application_ref = {"kind": "file", "path": "application.json"}
    provenance_ref = {"kind": "file", "path": "provenance.json"}

    if profile_id == "single-git":
        guidance = guidance_files(
            profile_id,
            "single",
            {
                "application": application_ref,
                "ruleset": rules_ref,
                "dataset": dataset_ref,
                "provenance": provenance_ref,
            },
        )
        init_git_repo(
            package_dir / "repository",
            merge_files(init_files, runtime_metadata, rules_files, dataset_files, guidance),
        )
        return {
            "profile": profile_id,
            "storage": "git",
            "topology": "single",
            "location": "../package/repository",
            "components": {"ruleset": rules_ref, "dataset": dataset_ref},
        }

    if profile_id == "split-git":
        init_git_repo(
            package_dir / "ruleset",
            merge_files(
                init_files,
                runtime_metadata,
                rules_files,
                guidance_files(
                    profile_id,
                    "ruleset",
                    {
                        "application": application_ref,
                        "ruleset": rules_ref,
                        "provenance": provenance_ref,
                    },
                ),
            ),
        )
        init_git_repo(
            package_dir / "dataset",
            merge_files(
                init_files,
                runtime_metadata,
                dataset_files,
                guidance_files(
                    profile_id,
                    "dataset",
                    {
                        "application": application_ref,
                        "dataset": dataset_ref,
                        "provenance": provenance_ref,
                    },
                ),
            ),
        )
        return {
            "profile": profile_id,
            "storage": "git",
            "topology": "split",
            "components": {
                "ruleset": {"location": "../package/ruleset", **rules_ref},
                "dataset": {"location": "../package/dataset", **dataset_ref},
            },
        }

    raise SystemExit(f"unsupported FS-002 profile: {profile_id}")

def validate_provider(provider_id: str):
    provider = profile(provider_id)
    if provider.get("id") != provider_id:
        raise SystemExit(f"invalid provider profile: {provider_id}")
    require_object("provider.bootstrap", provider.get("bootstrap"))
    if provider["bootstrap"].get("mode") != "initialize" or not provider["bootstrap"].get("instructions"):
        raise SystemExit(f"invalid provider profile: {provider_id}")
    return provider


def build_legacy(application, ruleset, dataset, build, packaging, adr_commit, builder_commit, output_dir: Path):
    require_object("packaging.preservation", packaging.get("preservation"))
    if (
        packaging.get("id") != build["packaging_profile"]
        or packaging["preservation"].get("writeback") != "complete-realization"
        or packaging["preservation"].get("preserve_non_dataset_realization_material") is not True
    ):
        raise SystemExit("invalid FS-001 packaging profile")

    for provider_id in build["providers"]:
        provider = validate_provider(provider_id)
        artifact = {
            "adr_realization": {
                "format": packaging["format"],
                "format_version": packaging["format_version"],
                "provenance": {"adr_commit": adr_commit, "app_builder_commit": builder_commit},
                "authority": {
                    "generated_realization_is_normative": False,
                    "dataset_is_authoritative_for_committed_application_state": True,
                },
                "provider": {"profile": provider_id, "name": provider["provider"]},
                "application": application,
                "initialization": {"provider": provider["bootstrap"]},
                "ruleset": ruleset,
                "dataset": dataset,
                "preservation": packaging["preservation"],
            }
        }
        write_json(output_dir / f"{provider_id}.json", artifact)


def build_fs002(
    application,
    ruleset,
    dataset,
    build,
    packaging,
    adr_repository,
    adr_commit,
    builder_commit,
    output_dir: Path,
    input_paths,
):
    validate_fs002_profile(packaging, build["packaging_profile"])
    package_reference = build_fs002_package(
        output_dir,
        build["packaging_profile"],
        application,
        ruleset,
        dataset,
        build,
        input_paths,
        adr_repository,
        adr_commit,
        builder_commit,
    )

    providers_dir = output_dir / "providers"
    providers_dir.mkdir(parents=True)
    for provider_id in build["providers"]:
        provider = validate_provider(provider_id)
        require_object("provider.package_bootstrap", provider.get("package_bootstrap"))
        if provider["package_bootstrap"].get("mode") != "initialize" or not provider["package_bootstrap"].get("instructions"):
            raise SystemExit(f"provider lacks FS-002 package bootstrap: {provider_id}")
        artifact = {
            "adr_realization": {
                "provenance": {"adr_commit": adr_commit, "app_builder_commit": builder_commit},
                "authority": {
                    "generated_realization_is_normative": False,
                    "dataset_is_authoritative_for_committed_application_state": True,
                },
                "provider": {"profile": provider_id, "name": provider["provider"]},
                "application": application,
                "initialization": {"provider": provider["package_bootstrap"]},
                "package": package_reference,
            }
        }
        write_json(providers_dir / f"{provider_id}.json", artifact)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--application", required=True, type=Path)
    parser.add_argument("--ruleset", required=True, type=Path)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--adr-repository", default=DEFAULT_ADR_REPOSITORY)
    args = parser.parse_args()

    application = load(args.application)
    ruleset = load(args.ruleset)
    dataset = load(args.dataset)
    build = load(args.build)
    validate_sources(application, ruleset, dataset, build)

    packaging = profile(build["packaging_profile"])
    adr_commit = resolve_adr_main(args.adr_repository)
    consume_adr_seed_specs(args.adr_repository, adr_commit)
    builder_commit = app_builder_commit()

    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit("output directory must be absent or empty")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if build["packaging_profile"] in FS002_PROFILES:
        build_fs002(
            application,
            ruleset,
            dataset,
            build,
            packaging,
            args.adr_repository,
            adr_commit,
            builder_commit,
            args.output_dir,
            {
                "application": args.application,
                "ruleset": args.ruleset,
                "dataset": args.dataset,
                "build": args.build,
            },
        )
    else:
        build_legacy(application, ruleset, dataset, build, packaging, adr_commit, builder_commit, args.output_dir)


if __name__ == "__main__":
    main()
