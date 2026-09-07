#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "product" / "src" / "examples" / "task-tracker"
STRUCTURED_BASE = ROOT / "product" / "src" / "examples" / "task-tracker-structured"
BUILDER = ROOT / "product" / "src" / "app_builder.py"
PROFILES_ROOT = ROOT / "product" / "src" / "profiles"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
PROVIDERS = ["generic-self-contained", "microsoft-copilot"]
FS002_PROFILES = ["single-file", "split-files", "single-git", "split-git"]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "product" / "src"))
from session_state import ApplicationSession

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def app_builder_head():
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def run_build(
    out: Path,
    build_path: Path,
    adr_repository: Path,
    *,
    application_path: Path | None = None,
    ruleset_path: Path | None = None,
    dataset_path: Path | None = None,
    check: bool = True,
):
    cmd = [
        "python3",
        str(BUILDER),
        "--application",
        str(application_path or BASE / "application.json"),
        "--ruleset",
        str(ruleset_path or BASE / "ruleset.json"),
        "--dataset",
        str(dataset_path or BASE / "dataset.json"),
        "--build",
        str(build_path),
        "--output-dir",
        str(out),
        "--adr-repository",
        str(adr_repository),
    ]
    cp = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and cp.returncode != 0:
        raise SystemExit(
            "FAIL: App Builder invocation failed: "
            + (cp.stderr.strip() or cp.stdout.strip())
        )
    return cp


def write_build(path: Path, packaging_profile: str):
    path.write_text(
        json.dumps(
            {"packaging_profile": packaging_profile, "providers": PROVIDERS},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(repo: Path, *args: str, env_extra=None):
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
        env=env,
    ).stdout.rstrip("\r\n")


def repo_files(repo: Path):
    return sorted(
        p.relative_to(repo).as_posix()
        for p in repo.rglob("*")
        if p.is_file() and ".git" not in p.parts
    )


def verify_git_initial_history(repo: Path, label: str):
    if git(repo, "rev-list", "--count", "HEAD") != "1":
        raise SystemExit(f"FAIL: {label} must contain exactly one initial commit")
    if git(repo, "show", "-s", "--format=%s", "HEAD") != "ADR App Builder initial package":
        raise SystemExit(f"FAIL: {label} initial commit message")

    identity = git(
        repo,
        "show",
        "-s",
        "--format=%an%n%ae%n%cn%n%ce",
        "HEAD",
    ).splitlines()
    if identity != [
        "ADR App Builder",
        "app-builder@adr.invalid",
        "ADR App Builder",
        "app-builder@adr.invalid",
    ]:
        raise SystemExit(f"FAIL: {label} initial author/committer identity")

    dates = git(repo, "show", "-s", "--format=%at%n%ct", "HEAD").splitlines()
    if len(dates) != 2:
        raise SystemExit(f"FAIL: {label} initial timestamp shape")
    now = int(time.time())
    if any(abs(now - int(value)) > 300 for value in dates):
        raise SystemExit(f"FAIL: {label} initial timestamp is not current")

    committed_files = git(repo, "ls-tree", "-r", "--name-only", "HEAD").splitlines()
    if committed_files != repo_files(repo):
        raise SystemExit(f"FAIL: {label} initial commit does not contain complete generated tree")

    if git(repo, "status", "--porcelain=v1", "--untracked-files=all").splitlines():
        raise SystemExit(f"FAIL: {label} generated repository is dirty after initial commit")


def verify_provider_set(out: Path, expected_package_ref: dict):
    providers = out / "providers"
    if sorted(p.name for p in providers.glob("*.json")) != sorted(f"{p}.json" for p in PROVIDERS):
        raise SystemExit("FAIL: FS-002 provider set")
    for pid in PROVIDERS:
        r = read_json(providers / f"{pid}.json")["adr_realization"]
        if "ruleset" in r or "dataset" in r:
            raise SystemExit(f"FAIL: provider duplicates package content {pid}")
        if r.get("package") != expected_package_ref:
            raise SystemExit(f"FAIL: provider does not share package reference {pid}")


def mutate_dataset(dataset):
    updated = json.loads(json.dumps(dataset))
    updated.setdefault("state", {})["fs002_validation_mutation"] = True
    return updated


def validate_single_file(out: Path, rules, dataset):
    package_dir = out / "package"
    if sorted(p.name for p in package_dir.iterdir()) != ["package.json"]:
        raise SystemExit("FAIL: single-file package shape")
    package = package_dir / "package.json"
    value = read_json(package)
    if value != {"ruleset": rules, "dataset": dataset}:
        raise SystemExit("FAIL: single-file source fidelity")
    expected_ref = {
        "profile": "single-file",
        "storage": "file",
        "topology": "single",
        "location": "../package/package.json",
        "components": {"ruleset": "ruleset", "dataset": "dataset"},
    }
    verify_provider_set(out, expected_ref)

    original_rules = json.loads(json.dumps(value["ruleset"]))
    value["dataset"] = mutate_dataset(value["dataset"])
    package.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    if read_json(package)["ruleset"] != original_rules:
        raise SystemExit("FAIL: single-file mutation changed Ruleset")


def validate_split_files(out: Path, rules, dataset):
    package = out / "package"
    if sorted(p.name for p in package.iterdir()) != ["dataset.json", "ruleset.json"]:
        raise SystemExit("FAIL: split-files package shape")
    if read_json(package / "ruleset.json") != rules or read_json(package / "dataset.json") != dataset:
        raise SystemExit("FAIL: split-files source fidelity")
    expected_ref = {
        "profile": "split-files",
        "storage": "file",
        "topology": "split",
        "location": "../package",
        "components": {"ruleset": "ruleset.json", "dataset": "dataset.json"},
    }
    verify_provider_set(out, expected_ref)

    rules_hash = sha(package / "ruleset.json")
    (package / "dataset.json").write_text(
        json.dumps(mutate_dataset(dataset), indent=2) + "\n",
        encoding="utf-8",
    )
    if sha(package / "ruleset.json") != rules_hash:
        raise SystemExit("FAIL: split-files mutation rewrote Ruleset")


def validate_single_git(out: Path, rules, dataset):
    repo = out / "package" / "repository"
    expected_files = [
        "AGENTS.md",
        "README.md",
        "dataset.json",
        "init-config/application.json",
        "init-config/build.json",
        "init-config/dataset.json",
        "init-config/ruleset.json",
        "ruleset.json",
    ]
    if repo_files(repo) != expected_files:
        raise SystemExit("FAIL: single-git worktree shape")
    if read_json(repo / "ruleset.json") != rules or read_json(repo / "dataset.json") != dataset:
        raise SystemExit("FAIL: single-git source fidelity")
    if git(repo, "remote"):
        raise SystemExit("FAIL: single-git remote configured")
    if git(repo, "symbolic-ref", "--short", "HEAD") != "main":
        raise SystemExit("FAIL: single-git canonical branch")
    verify_git_initial_history(repo, "single-git")
    expected_ref = {
        "profile": "single-git",
        "storage": "git",
        "topology": "single",
        "location": "../package/repository",
        "components": {
            "ruleset": {"kind": "file", "path": "ruleset.json"},
            "dataset": {"kind": "file", "path": "dataset.json"},
        },
    }
    verify_provider_set(out, expected_ref)

    rules_hash = sha(repo / "ruleset.json")
    (repo / "dataset.json").write_text(
        json.dumps(mutate_dataset(dataset), indent=2) + "\n",
        encoding="utf-8",
    )
    if sha(repo / "ruleset.json") != rules_hash:
        raise SystemExit("FAIL: single-git Dataset mutation changed Ruleset")


def validate_split_git(out: Path, rules, dataset):
    rules_repo = out / "package" / "ruleset"
    dataset_repo = out / "package" / "dataset"
    expected_rules = [
        "AGENTS.md",
        "README.md",
        "init-config/application.json",
        "init-config/build.json",
        "init-config/dataset.json",
        "init-config/ruleset.json",
        "ruleset.json",
    ]
    expected_dataset = [
        "AGENTS.md",
        "README.md",
        "dataset.json",
        "init-config/application.json",
        "init-config/build.json",
        "init-config/dataset.json",
        "init-config/ruleset.json",
    ]
    if repo_files(rules_repo) != expected_rules or repo_files(dataset_repo) != expected_dataset:
        raise SystemExit("FAIL: split-git worktree shape")
    if read_json(rules_repo / "ruleset.json") != rules or read_json(dataset_repo / "dataset.json") != dataset:
        raise SystemExit("FAIL: split-git source fidelity")
    if git(rules_repo, "remote") or git(dataset_repo, "remote"):
        raise SystemExit("FAIL: split-git remote configured")
    if git(rules_repo, "symbolic-ref", "--short", "HEAD") != "main":
        raise SystemExit("FAIL: split-git Ruleset canonical branch")
    if git(dataset_repo, "symbolic-ref", "--short", "HEAD") != "main":
        raise SystemExit("FAIL: split-git Dataset canonical branch")
    verify_git_initial_history(rules_repo, "split-git Ruleset repository")
    verify_git_initial_history(dataset_repo, "split-git Dataset repository")
    expected_ref = {
        "profile": "split-git",
        "storage": "git",
        "topology": "split",
        "components": {
            "ruleset": {
                "location": "../package/ruleset",
                "kind": "file",
                "path": "ruleset.json",
            },
            "dataset": {
                "location": "../package/dataset",
                "kind": "file",
                "path": "dataset.json",
            },
        },
    }
    verify_provider_set(out, expected_ref)

    rules_head = git(rules_repo, "rev-parse", "HEAD")
    rules_hash = sha(rules_repo / "ruleset.json")
    (dataset_repo / "dataset.json").write_text(
        json.dumps(mutate_dataset(dataset), indent=2) + "\n",
        encoding="utf-8",
    )
    if (
        git(rules_repo, "rev-parse", "HEAD") != rules_head
        or sha(rules_repo / "ruleset.json") != rules_hash
    ):
        raise SystemExit("FAIL: split-git Dataset mutation changed Ruleset repository")


def compare_initial(profile: str, a: Path, b: Path):
    if profile == "single-file":
        if (a / "package" / "package.json").read_bytes() != (b / "package" / "package.json").read_bytes():
            raise SystemExit("FAIL: single-file repeat determinism")
    elif profile == "split-files":
        for name in ["ruleset.json", "dataset.json"]:
            if (a / "package" / name).read_bytes() != (b / "package" / name).read_bytes():
                raise SystemExit(f"FAIL: split-files repeat determinism {name}")
    elif profile == "single-git":
        at = git(a / "package" / "repository", "rev-parse", "HEAD^{tree}")
        bt = git(b / "package" / "repository", "rev-parse", "HEAD^{tree}")
        if at != bt:
            raise SystemExit("FAIL: single-git generated tree determinism")
    elif profile == "split-git":
        for name in ["ruleset", "dataset"]:
            at = git(a / "package" / name, "rev-parse", "HEAD^{tree}")
            bt = git(b / "package" / name, "rev-parse", "HEAD^{tree}")
            if at != bt:
                raise SystemExit(f"FAIL: split-git generated tree determinism {name}")


def validate_fs001(app, rules, dataset, adr, builder, adr_repository: Path):
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        pa, pb = Path(a), Path(b)
        run_build(pa, BASE / "build.json", adr_repository)
        run_build(pb, BASE / "build.json", adr_repository)
        expected_names = sorted(f"{pid}.json" for pid in PROVIDERS)
        if sorted(p.name for p in pa.iterdir()) != expected_names:
            raise SystemExit("FAIL: FS-001 provider output set")
        for pid in PROVIDERS:
            aa, bb = pa / f"{pid}.json", pb / f"{pid}.json"
            if not aa.is_file() or aa.read_bytes() != bb.read_bytes():
                raise SystemExit(f"FAIL: FS-001 deterministic provider output {pid}")
            r = read_json(aa)["adr_realization"]
            if r["provenance"] != {"adr_commit": adr, "app_builder_commit": builder}:
                raise SystemExit(f"FAIL: FS-001 provenance {pid}")
            application = r.get("application")
            if not isinstance(application, dict) or application.get("id") != app.get("id"):
                raise SystemExit(f"FAIL: FS-001 application identity {pid}")
            if r["ruleset"] != rules or r["dataset"] != dataset:
                raise SystemExit(f"FAIL: FS-001 Ruleset/Dataset fidelity {pid}")
            if application.get("initialization") != app["initialization"]:
                raise SystemExit(f"FAIL: FS-001 application initialization fidelity {pid}")
            if "application" in r.get("initialization", {}):
                raise SystemExit(f"FAIL: FS-001 duplicated application initialization {pid}")
            if r["initialization"]["provider"].get("mode") != "initialize":
                raise SystemExit(f"FAIL: FS-001 provider bootstrap {pid}")
            preservation = r.get("preservation")
            if not isinstance(preservation, dict):
                raise SystemExit(f"FAIL: FS-001 preservation contract {pid}")
            required_preservation_fields = {
                "writeback",
                "preserve_non_dataset_realization_material",
            }
            if not required_preservation_fields <= set(preservation):
                raise SystemExit(f"FAIL: FS-001 preservation contract fields {pid}")


def package_identity(profile: str, out: Path):
    if profile == "single-file":
        return (out / "package" / "package.json").read_bytes()
    if profile == "split-files":
        return (
            (out / "package" / "ruleset.json").read_bytes(),
            (out / "package" / "dataset.json").read_bytes(),
        )
    def runtime_guidance_identity(repo: Path):
        return tuple(
            (relative, (repo / relative).read_bytes())
            for relative in repo_files(repo)
            if not relative.startswith("init-config/")
        )
    if profile == "single-git":
        return runtime_guidance_identity(out / "package" / "repository")
    if profile == "split-git":
        return (
            runtime_guidance_identity(out / "package" / "ruleset"),
            runtime_guidance_identity(out / "package" / "dataset"),
        )
    raise SystemExit(f"FAIL: unknown profile identity {profile}")


def validate_provider_selection_independence(profile: str, adr_repository: Path, configs: Path):
    identities = []
    for provider in PROVIDERS:
        build_path = configs / f"{profile}-{provider}.json"
        build_path.write_text(
            json.dumps({"packaging_profile": profile, "providers": [provider]}, indent=2) + "\n",
            encoding="utf-8",
        )
        with tempfile.TemporaryDirectory() as out:
            out_path = Path(out)
            run_build(out_path, build_path, adr_repository)
            identities.append(package_identity(profile, out_path))
    if identities[0] != identities[1]:
        raise SystemExit(f"FAIL: provider selection changed package {profile}")

def require_clean_tree():
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    if dirty.splitlines():
        raise SystemExit("FAIL: validation requires a clean committed App Builder tree")


def source_snapshot(names):
    return {BASE / name: sha(BASE / name) for name in names}


def assert_source_snapshot(before):
    for path, digest in before.items():
        if sha(path) != digest:
            raise SystemExit(f"FAIL: source mutated {path.relative_to(ROOT)}")


def create_adr_fixture(parent: Path):
    repo = parent / "adr"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    seed = repo / "product" / "src" / "validation.seed.json"
    seed.parent.mkdir(parents=True)
    seed.write_text('{"fixture":"adr-app-builder-validation"}\n', encoding="utf-8")
    git(repo, "add", "--", "product/src/validation.seed.json")
    git(
        repo,
        "commit",
        "-q",
        "-m",
        "ADR validation fixture",
        env_extra={
            "GIT_AUTHOR_NAME": "ADR Validation Fixture",
            "GIT_AUTHOR_EMAIL": "validation-fixture@adr.invalid",
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+00:00",
            "GIT_COMMITTER_NAME": "ADR Validation Fixture",
            "GIT_COMMITTER_EMAIL": "validation-fixture@adr.invalid",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+00:00",
        },
    )
    return repo, git(repo, "rev-parse", "HEAD")


def task_profile_contracts():
    require_clean_tree()

    expected_fs002 = {
        "single-file": ("file", "single"),
        "split-files": ("file", "split"),
        "single-git": ("git", "single"),
        "split-git": ("git", "split"),
    }
    for profile_id, (storage, topology) in expected_fs002.items():
        value = read_json(PROFILES_ROOT / f"{profile_id}.json")
        if value.get("id") != profile_id:
            raise SystemExit(f"FAIL: packaging profile id {profile_id}")
        if value.get("package_type") != "ruleset-dataset":
            raise SystemExit(f"FAIL: packaging profile package_type {profile_id}")
        if (value.get("storage"), value.get("topology")) != (storage, topology):
            raise SystemExit(f"FAIL: packaging profile topology {profile_id}")

    legacy = read_json(PROFILES_ROOT / "self-contained-json.json")
    preservation = legacy.get("preservation")
    if legacy.get("id") != "self-contained-json" or not isinstance(preservation, dict):
        raise SystemExit("FAIL: self-contained-json preservation contract")
    required_preservation_fields = {
        "writeback",
        "preserve_non_dataset_realization_material",
    }
    if not required_preservation_fields <= set(preservation):
        raise SystemExit("FAIL: self-contained-json preservation contract fields")

    for provider_id in PROVIDERS:
        provider = read_json(PROFILES_ROOT / f"{provider_id}.json")
        if provider.get("id") != provider_id:
            raise SystemExit(f"FAIL: provider profile id {provider_id}")
        for label in ("bootstrap", "package_bootstrap"):
            value = provider.get(label)
            if (
                not isinstance(value, dict)
                or value.get("mode") != "initialize"
                or not isinstance(value.get("instructions"), list)
                or not value["instructions"]
                or not all(isinstance(item, str) and item for item in value["instructions"])
            ):
                raise SystemExit(f"FAIL: provider {provider_id} {label} shape")

    copilot = read_json(PROFILES_ROOT / "microsoft-copilot.json")
    copilot_text = "\n".join(copilot["bootstrap"]["instructions"]).lower()
    if "fresh copilot chat" not in copilot_text:
        raise SystemExit("FAIL: Microsoft Copilot profile lacks explicit fresh-session guidance")
    if "complete updated realization" not in copilot_text:
        raise SystemExit(
            "FAIL: Microsoft Copilot profile lacks complete-realization preservation guidance"
        )


def task_fs001_build():
    require_clean_tree()
    before = source_snapshot(["application.json", "ruleset.json", "dataset.json", "build.json"])
    builder = app_builder_head()
    app = read_json(BASE / "application.json")
    rules = read_json(BASE / "ruleset.json")
    dataset = read_json(BASE / "dataset.json")

    with tempfile.TemporaryDirectory() as tmp:
        adr_repository, adr = create_adr_fixture(Path(tmp))
        validate_fs001(app, rules, dataset, adr, builder, adr_repository)

    assert_source_snapshot(before)


def expect_build_failure(
    label: str,
    adr_repository: Path,
    *,
    application=None,
    ruleset=None,
    dataset=None,
    build=None,
):
    application = application if application is not None else read_json(BASE / "application.json")
    ruleset = ruleset if ruleset is not None else read_json(BASE / "ruleset.json")
    dataset = dataset if dataset is not None else read_json(BASE / "dataset.json")
    build = build if build is not None else read_json(BASE / "build.json")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        application_path = root / "application.json"
        ruleset_path = root / "ruleset.json"
        dataset_path = root / "dataset.json"
        build_path = root / "build.json"
        for path, value in (
            (application_path, application),
            (ruleset_path, ruleset),
            (dataset_path, dataset),
            (build_path, build),
        ):
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

        cp = run_build(
            root / "out",
            build_path,
            adr_repository,
            application_path=application_path,
            ruleset_path=ruleset_path,
            dataset_path=dataset_path,
            check=False,
        )
        if cp.returncode == 0:
            raise SystemExit(f"FAIL: invalid input accepted: {label}")


def task_fs001_input_validation():
    require_clean_tree()
    with tempfile.TemporaryDirectory() as tmp:
        adr_repository, _ = create_adr_fixture(Path(tmp))

        app = read_json(BASE / "application.json")
        bad = json.loads(json.dumps(app))
        bad.pop("id", None)
        expect_build_failure("missing application.id", adr_repository, application=bad)

        bad = json.loads(json.dumps(app))
        bad.pop("initialization", None)
        expect_build_failure("missing application.initialization", adr_repository, application=bad)

        dataset = read_json(BASE / "dataset.json")
        bad_dataset = json.loads(json.dumps(dataset))
        bad_dataset.setdefault("instance", {}).pop("id", None)
        expect_build_failure("missing dataset.instance.id", adr_repository, dataset=bad_dataset)

        build = read_json(BASE / "build.json")
        bad_build = json.loads(json.dumps(build))
        bad_build["providers"] = [PROVIDERS[0], PROVIDERS[0]]
        expect_build_failure("duplicate providers", adr_repository, build=bad_build)

        bad_build = json.loads(json.dumps(build))
        bad_build["packaging_profile"] = "__missing_packaging_profile__"
        expect_build_failure("unknown packaging profile", adr_repository, build=bad_build)

        bad_build = json.loads(json.dumps(build))
        bad_build["providers"] = ["__missing_provider_profile__"]
        expect_build_failure("unknown provider profile", adr_repository, build=bad_build)


def validate_fs002_group(profiles):
    before = source_snapshot(["ruleset.json", "dataset.json"])
    rules = read_json(BASE / "ruleset.json")
    dataset = read_json(BASE / "dataset.json")
    validators = {
        "single-file": validate_single_file,
        "split-files": validate_split_files,
        "single-git": validate_single_git,
        "split-git": validate_split_git,
    }

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        adr_repository, _ = create_adr_fixture(root)
        configs = root / "configs"
        configs.mkdir()

        for profile in profiles:
            build_path = configs / f"{profile}.json"
            write_build(build_path, profile)
            with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
                pa, pb = Path(a), Path(b)
                run_build(pa, build_path, adr_repository)
                run_build(pb, build_path, adr_repository)
                compare_initial(profile, pa, pb)
                validators[profile](pa, rules, dataset)

    assert_source_snapshot(before)


def task_fs002_file_packaging():
    require_clean_tree()
    validate_fs002_group(["single-file", "split-files"])


def task_fs002_git_packaging():
    require_clean_tree()
    validate_fs002_group(["single-git", "split-git"])


def task_fs002_provider_independence():
    require_clean_tree()
    before = source_snapshot(["ruleset.json", "dataset.json"])
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        adr_repository, _ = create_adr_fixture(root)
        configs = root / "configs"
        configs.mkdir()
        for profile in FS002_PROFILES:
            validate_provider_selection_independence(profile, adr_repository, configs)
    assert_source_snapshot(before)


def pointer_tokens(pointer: str):
    if pointer == "":
        return ()
    return tuple(raw.replace("~1", "/").replace("~0", "~") for raw in pointer[1:].split("/"))


def pointer_value(value, pointer: str):
    current = value
    for token in pointer_tokens(pointer):
        current = current[token] if isinstance(current, dict) else current[int(token)]
    return current


def set_pointer_value(root, source, pointer: str, selected):
    tokens = pointer_tokens(pointer)
    if not tokens:
        return json.loads(json.dumps(selected))
    if root is None:
        root = [] if isinstance(source, list) else {}
    out, src = root, source
    for position, token in enumerate(tokens):
        last = position == len(tokens) - 1
        if isinstance(src, dict):
            child = src[token]
            if last:
                out[token] = json.loads(json.dumps(selected))
            else:
                if token not in out:
                    out[token] = [] if isinstance(child, list) else {}
                out = out[token]
            src = child
        else:
            index = int(token)
            child = src[index]
            while len(out) < len(src):
                out.append(None)
            if last:
                out[index] = json.loads(json.dumps(selected))
            else:
                if out[index] is None:
                    out[index] = [] if isinstance(child, list) else {}
                out = out[index]
            src = child
    return root


def reconstruct_component(repo: Path, component: str, source, mapping):
    root = None
    for relative, selector in mapping.items():
        root = set_pointer_value(root, source, selector, read_json(repo / component / relative))
    return root


def assert_init_config(repo: Path, application_path: Path, ruleset_path: Path, dataset_path: Path, build_path: Path):
    expected = {
        "application.json": application_path.read_bytes(),
        "ruleset.json": ruleset_path.read_bytes(),
        "dataset.json": dataset_path.read_bytes(),
        "build.json": build_path.read_bytes(),
    }
    for name, content in expected.items():
        if (repo / "init-config" / name).read_bytes() != content:
            raise SystemExit(f"FAIL: FS-003 init-config byte fidelity {name}")


def snapshot_without_dataset(repo: Path):
    return {
        relative: sha(repo / relative)
        for relative in repo_files(repo)
        if relative != "dataset.json" and not relative.startswith("dataset/")
    }


def assert_snapshot(repo: Path, snapshot):
    for relative, digest in snapshot.items():
        if sha(repo / relative) != digest:
            raise SystemExit(f"FAIL: FS-003 save changed non-Dataset material {relative}")


def write_tree_dataset(repo: Path, dataset, mapping):
    for relative, selector in mapping.items():
        (repo / "dataset" / relative).write_text(
            json.dumps(pointer_value(dataset, selector), indent=2) + "\n",
            encoding="utf-8",
        )


def structured_build_value(profile: str, providers=None, *, mixed=False):
    value = read_json(STRUCTURED_BASE / "build.json")
    value["packaging_profile"] = profile
    if providers is not None:
        value["providers"] = providers
    if mixed:
        value["runtime"]["ruleset"] = {"representation": "file"}
    return value


def task_fs003_git_structured():
    require_clean_tree()
    source_paths = [
        STRUCTURED_BASE / "application.json",
        STRUCTURED_BASE / "ruleset.json",
        STRUCTURED_BASE / "dataset.json",
        STRUCTURED_BASE / "build.json",
    ]
    before = {path: sha(path) for path in source_paths}
    rules = read_json(STRUCTURED_BASE / "ruleset.json")
    dataset = read_json(STRUCTURED_BASE / "dataset.json")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        adr_repository, _ = create_adr_fixture(root)
        configs = root / "configs"
        configs.mkdir()

        for profile in ["single-git", "split-git"]:
            build_path = configs / f"{profile}.json"
            value = structured_build_value(profile)
            build_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
                pa, pb = Path(a), Path(b)
                for out in [pa, pb]:
                    run_build(
                        out,
                        build_path,
                        adr_repository,
                        application_path=STRUCTURED_BASE / "application.json",
                        ruleset_path=STRUCTURED_BASE / "ruleset.json",
                        dataset_path=STRUCTURED_BASE / "dataset.json",
                    )

                if profile == "single-git":
                    repo = pa / "package" / "repository"
                    repo_b = pb / "package" / "repository"
                    verify_git_initial_history(repo, "FS-003 single-git")
                    verify_git_initial_history(repo_b, "FS-003 single-git repeat")
                    if git(repo, "rev-parse", "HEAD^{tree}") != git(repo_b, "rev-parse", "HEAD^{tree}"):
                        raise SystemExit("FAIL: FS-003 single-git generated tree repeat determinism")
                    assert_init_config(
                        repo,
                        STRUCTURED_BASE / "application.json",
                        STRUCTURED_BASE / "ruleset.json",
                        STRUCTURED_BASE / "dataset.json",
                        build_path,
                    )
                    if reconstruct_component(
                        repo, "ruleset", rules, value["runtime"]["ruleset"]["files"]
                    ) != rules:
                        raise SystemExit("FAIL: FS-003 Ruleset lossless reconstruction")
                    mapping = value["runtime"]["dataset"]["files"]
                    if reconstruct_component(repo, "dataset", dataset, mapping) != dataset:
                        raise SystemExit("FAIL: FS-003 Dataset lossless reconstruction")

                    preserved = snapshot_without_dataset(repo)
                    session = ApplicationSession(
                        lambda: reconstruct_component(repo, "dataset", dataset, mapping),
                        lambda current: write_tree_dataset(repo, current, mapping),
                    )
                    session.edit(
                        lambda current: current.setdefault("state", {}).__setitem__(
                            "fs003_validation_mutation", True
                        )
                    )
                    if reconstruct_component(repo, "dataset", dataset, mapping) != dataset:
                        raise SystemExit("FAIL: FS-003 edit persisted before save")
                    session.save()
                    saved = reconstruct_component(repo, "dataset", session.read(), mapping)
                    if saved != session.read():
                        raise SystemExit("FAIL: FS-003 explicit save did not persist active state")
                    assert_snapshot(repo, preserved)
                    if session.reopen() != saved:
                        raise SystemExit("FAIL: FS-003 reopen did not restore persisted Dataset")
                else:
                    rules_repo = pa / "package" / "ruleset"
                    dataset_repo = pa / "package" / "dataset"
                    rules_repo_b = pb / "package" / "ruleset"
                    dataset_repo_b = pb / "package" / "dataset"
                    for candidate, label in [
                        (rules_repo, "FS-003 split Ruleset"),
                        (dataset_repo, "FS-003 split Dataset"),
                        (rules_repo_b, "FS-003 split Ruleset repeat"),
                        (dataset_repo_b, "FS-003 split Dataset repeat"),
                    ]:
                        verify_git_initial_history(candidate, label)
                    if (
                        git(rules_repo, "rev-parse", "HEAD^{tree}")
                        != git(rules_repo_b, "rev-parse", "HEAD^{tree}")
                        or git(dataset_repo, "rev-parse", "HEAD^{tree}")
                        != git(dataset_repo_b, "rev-parse", "HEAD^{tree}")
                    ):
                        raise SystemExit("FAIL: FS-003 split-git generated tree repeat determinism")
                    for repo in [rules_repo, dataset_repo]:
                        assert_init_config(
                            repo,
                            STRUCTURED_BASE / "application.json",
                            STRUCTURED_BASE / "ruleset.json",
                            STRUCTURED_BASE / "dataset.json",
                            build_path,
                        )
                    rules_head = git(rules_repo, "rev-parse", "HEAD")
                    rules_snapshot = {
                        relative: sha(rules_repo / relative)
                        for relative in repo_files(rules_repo)
                    }
                    mapping = value["runtime"]["dataset"]["files"]
                    session = ApplicationSession(
                        lambda: reconstruct_component(dataset_repo, "dataset", dataset, mapping),
                        lambda current: write_tree_dataset(dataset_repo, current, mapping),
                    )
                    session.edit(
                        lambda current: current.setdefault("state", {}).__setitem__(
                            "fs003_validation_mutation", True
                        )
                    )
                    session.save()
                    if git(rules_repo, "rev-parse", "HEAD") != rules_head:
                        raise SystemExit("FAIL: FS-003 split save advanced Ruleset repository")
                    assert_snapshot(rules_repo, rules_snapshot)

        mixed_path = configs / "mixed.json"
        mixed = structured_build_value("single-git", mixed=True)
        mixed_path.write_text(json.dumps(mixed, indent=2) + "\n", encoding="utf-8")
        with tempfile.TemporaryDirectory() as out:
            out_path = Path(out)
            run_build(
                out_path,
                mixed_path,
                adr_repository,
                application_path=STRUCTURED_BASE / "application.json",
                ruleset_path=STRUCTURED_BASE / "ruleset.json",
                dataset_path=STRUCTURED_BASE / "dataset.json",
            )
            repo = out_path / "package" / "repository"
            if not (repo / "ruleset.json").is_file() or not (repo / "dataset").is_dir():
                raise SystemExit("FAIL: FS-003 mixed file/tree realization")
            verify_provider_set(
                out_path,
                {
                    "profile": "single-git",
                    "storage": "git",
                    "topology": "single",
                    "location": "../package/repository",
                    "components": {
                        "ruleset": {"kind": "file", "path": "ruleset.json"},
                        "dataset": {"kind": "tree", "path": "dataset"},
                    },
                },
            )

        provider_identities = []
        for provider in PROVIDERS:
            provider_path = configs / f"provider-{provider}.json"
            provider_build = structured_build_value("single-git", [provider])
            provider_path.write_text(
                json.dumps(provider_build, indent=2) + "\n", encoding="utf-8"
            )
            with tempfile.TemporaryDirectory() as out:
                out_path = Path(out)
                run_build(
                    out_path,
                    provider_path,
                    adr_repository,
                    application_path=STRUCTURED_BASE / "application.json",
                    ruleset_path=STRUCTURED_BASE / "ruleset.json",
                    dataset_path=STRUCTURED_BASE / "dataset.json",
                )
                provider_identities.append(package_identity("single-git", out_path))
        if provider_identities[0] != provider_identities[1]:
            raise SystemExit("FAIL: FS-003 provider selection changed runtime/guidance")

        bad_cases = []
        bad = structured_build_value("single-git")
        bad["runtime"]["dataset"]["representation"] = "unsupported"
        bad_cases.append(("unsupported representation", bad))

        bad = structured_build_value("single-git")
        bad["runtime"]["dataset"]["files"] = {}
        bad_cases.append(("empty mapping", bad))

        bad = structured_build_value("single-git")
        bad["runtime"]["dataset"]["files"] = {"bad.json": "/does-not-exist"}
        bad_cases.append(("nonexistent selector", bad))

        bad = structured_build_value("single-git")
        bad["runtime"]["dataset"]["files"] = {
            "state.json": "/state",
            "tasks.json": "/state/tasks",
            "instance.json": "/instance",
            "history.json": "/history",
        }
        bad_cases.append(("overlapping selectors", bad))

        bad = structured_build_value("single-git")
        bad["runtime"]["dataset"]["files"] = {
            "state.json": "/state",
            "instance.json": "/instance",
        }
        bad_cases.append(("incomplete mapping", bad))

        bad = structured_build_value("single-git")
        bad["runtime"]["dataset"]["files"] = {
            "../state.json": "/state",
            "instance.json": "/instance",
            "history.json": "/history",
        }
        bad_cases.append(("path traversal", bad))

        for label, build_value in bad_cases:
            expect_build_failure(
                "FS-003 " + label,
                adr_repository,
                application=read_json(STRUCTURED_BASE / "application.json"),
                ruleset=rules,
                dataset=dataset,
                build=build_value,
            )

    for path, digest in before.items():
        if sha(path) != digest:
            raise SystemExit(f"FAIL: FS-003 source mutated {path.relative_to(ROOT)}")

TASKS = {
    "profile-contracts": task_profile_contracts,
    "fs001-build": task_fs001_build,
    "fs001-input-validation": task_fs001_input_validation,
    "fs002-file-packaging": task_fs002_file_packaging,
    "fs002-git-packaging": task_fs002_git_packaging,
    "fs002-provider-independence": task_fs002_provider_independence,
    "fs003-git-structured": task_fs003_git_structured,
}


def fail(message: str) -> int:
    print(f"FAIL product-validation: {message}", file=sys.stderr)
    return 1


def required_tasks():
    data = read_json(MANIFEST)
    required = []
    seen = set()
    for binding in data.get("bindings", []):
        for task in binding.get("tasks", []):
            if task not in seen:
                seen.add(task)
                required.append(task)
    for task in data.get("build_tasks", []):
        if task not in seen:
            seen.add(task)
            required.append(task)
    return required


def run_task(name: str):
    fn = TASKS.get(name)
    if fn is None:
        raise SystemExit(f"FAIL product-validation: unknown product Validation task: {name}")
    fn()
    print(f"PASS {name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-tasks", action="store_true")
    parser.add_argument("--task")
    args = parser.parse_args(argv)

    if args.list_tasks and args.task:
        return fail("--list-tasks and --task are mutually exclusive")

    if args.list_tasks:
        for task in sorted(TASKS):
            print(task)
        return 0

    if args.task:
        if args.task not in TASKS:
            return fail(f"unknown product Validation task: {args.task}")
        run_task(args.task)
        return 0

    for task in required_tasks():
        run_task(task)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
