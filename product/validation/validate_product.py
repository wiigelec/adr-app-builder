#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "product" / "src" / "examples" / "task-tracker"
BUILDER = ROOT / "product" / "src" / "app_builder.py"
PROFILES_ROOT = ROOT / "product" / "src" / "profiles"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
PROVIDERS = ["generic-self-contained", "microsoft-copilot"]
FS002_PROFILES = ["single-file", "split-files", "single-git", "split-git"]

MUTATION_ENV = {
    "GIT_AUTHOR_NAME": "ADR Runtime Fixture",
    "GIT_AUTHOR_EMAIL": "runtime-fixture@adr.invalid",
    "GIT_AUTHOR_DATE": "2000-01-02T00:00:00+00:00",
    "GIT_COMMITTER_NAME": "ADR Runtime Fixture",
    "GIT_COMMITTER_EMAIL": "runtime-fixture@adr.invalid",
    "GIT_COMMITTER_DATE": "2000-01-02T00:00:00+00:00",
}


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
    if repo_files(repo) != ["dataset.json", "ruleset.json"]:
        raise SystemExit("FAIL: single-git worktree shape")
    if read_json(repo / "ruleset.json") != rules or read_json(repo / "dataset.json") != dataset:
        raise SystemExit("FAIL: single-git source fidelity")
    if git(repo, "remote"):
        raise SystemExit("FAIL: single-git remote configured")
    if git(repo, "symbolic-ref", "--short", "HEAD") != "main":
        raise SystemExit("FAIL: single-git canonical branch")
    if git(repo, "rev-list", "--count", "HEAD") != "1":
        raise SystemExit("FAIL: single-git must contain exactly one initial commit")
    expected_ref = {
        "profile": "single-git",
        "storage": "git",
        "topology": "single",
        "location": "../package/repository",
        "components": {"ruleset": "ruleset.json", "dataset": "dataset.json"},
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
    if repo_files(rules_repo) != ["ruleset.json"] or repo_files(dataset_repo) != ["dataset.json"]:
        raise SystemExit("FAIL: split-git worktree shape")
    if read_json(rules_repo / "ruleset.json") != rules or read_json(dataset_repo / "dataset.json") != dataset:
        raise SystemExit("FAIL: split-git source fidelity")
    if git(rules_repo, "remote") or git(dataset_repo, "remote"):
        raise SystemExit("FAIL: split-git remote configured")
    if git(rules_repo, "symbolic-ref", "--short", "HEAD") != "main":
        raise SystemExit("FAIL: split-git Ruleset canonical branch")
    if git(dataset_repo, "symbolic-ref", "--short", "HEAD") != "main":
        raise SystemExit("FAIL: split-git Dataset canonical branch")
    if git(rules_repo, "rev-list", "--count", "HEAD") != "1":
        raise SystemExit("FAIL: split-git Ruleset repository must contain exactly one initial commit")
    if git(dataset_repo, "rev-list", "--count", "HEAD") != "1":
        raise SystemExit("FAIL: split-git Dataset repository must contain exactly one initial commit")
    expected_ref = {
        "profile": "split-git",
        "storage": "git",
        "topology": "split",
        "components": {
            "ruleset": {"location": "../package/ruleset", "path": "ruleset.json"},
            "dataset": {"location": "../package/dataset", "path": "dataset.json"},
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
        ah = git(a / "package" / "repository", "rev-parse", "HEAD")
        bh = git(b / "package" / "repository", "rev-parse", "HEAD")
        if ah != bh:
            raise SystemExit("FAIL: single-git initial HEAD determinism")
    elif profile == "split-git":
        for name in ["ruleset", "dataset"]:
            ah = git(a / "package" / name, "rev-parse", "HEAD")
            bh = git(b / "package" / name, "rev-parse", "HEAD")
            if ah != bh:
                raise SystemExit(f"FAIL: split-git initial HEAD determinism {name}")


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
            if r["application"] != app or r["ruleset"] != rules or r["dataset"] != dataset:
                raise SystemExit(f"FAIL: FS-001 source fidelity {pid}")
            if r["application"].get("initialization") != app["initialization"]:
                raise SystemExit(f"FAIL: FS-001 application initialization fidelity {pid}")
            if "application" in r.get("initialization", {}):
                raise SystemExit(f"FAIL: FS-001 duplicated application initialization {pid}")
            if r["initialization"]["provider"].get("mode") != "initialize":
                raise SystemExit(f"FAIL: FS-001 provider bootstrap {pid}")
            if (
                r["preservation"].get("writeback") != "complete-realization"
                or r["preservation"].get("preserve_non_dataset_realization_material") is not True
            ):
                raise SystemExit(f"FAIL: FS-001 preservation {pid}")


def package_identity(profile: str, out: Path):
    if profile == "single-file":
        return (out / "package" / "package.json").read_bytes()
    if profile == "split-files":
        return (
            (out / "package" / "ruleset.json").read_bytes(),
            (out / "package" / "dataset.json").read_bytes(),
        )
    if profile == "single-git":
        return git(out / "package" / "repository", "rev-parse", "HEAD")
    if profile == "split-git":
        return (
            git(out / "package" / "ruleset", "rev-parse", "HEAD"),
            git(out / "package" / "dataset", "rev-parse", "HEAD"),
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
    if (
        legacy.get("id") != "self-contained-json"
        or not isinstance(preservation, dict)
        or preservation.get("writeback") != "complete-realization"
        or preservation.get("preserve_non_dataset_realization_material") is not True
    ):
        raise SystemExit("FAIL: self-contained-json preservation contract")

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


TASKS = {
    "profile-contracts": task_profile_contracts,
    "fs001-build": task_fs001_build,
    "fs001-input-validation": task_fs001_input_validation,
    "fs002-file-packaging": task_fs002_file_packaging,
    "fs002-git-packaging": task_fs002_git_packaging,
    "fs002-provider-independence": task_fs002_provider_independence,
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
if __name__ == "__main__":
    raise SystemExit(main())
