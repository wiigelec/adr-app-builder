# FS-002 — Ruleset/Dataset Packaging

functional_set: FS-002
design_revision: 74f322e6b77846c3e147908885df65a552c38f84

## Purpose

FS-002 realizes the Ruleset/Dataset packaging model established by DP-100 by providing four concrete packaging profiles with independent Ruleset/Dataset addressability, topology-specific persistence behavior, deterministic generation, and mutation-preservation validation.

## Functional Boundary

FS-002 provides four Ruleset/Dataset packaging profiles:

- `single-file` — one JSON package containing separately addressable Ruleset and Dataset components.
- `split-files` — exactly two package files, `ruleset.json` and `dataset.json`.
- `single-git` — one Git repository containing distinct `ruleset.json` and `dataset.json` paths.
- `split-git` — one Ruleset Git repository containing `ruleset.json` and one Dataset Git repository containing `dataset.json`.

The Ruleset and Dataset package is distinct from application definition, provider bootstrap or presentation adaptation, and ADR/App Builder build provenance. Provider behavior may consume or carry a selected package but shall not alter the package topology or merge Ruleset and Dataset semantics.

FS-002 preserves exact Ruleset and Dataset source content within their package components and defines Dataset-only mutation preservation appropriate to each topology.

## Persistence Model

`single-file` and `single-git` use one shared persistence boundary while retaining independently addressable Ruleset and Dataset components.

`split-files` and `split-git` use independent persistence boundaries for Ruleset and Dataset.

File-backed profiles use JSON for FS-002. Git-backed profiles use deterministic repository initialization and do not require a remote.

## Mutation Model

Ordinary governed Dataset mutation changes Dataset material only.

For `single-file`, the containing file may be rewritten, but the Ruleset component remains unchanged.

For `split-files`, only `dataset.json` is rewritten.

For `single-git`, only Dataset content changes in the mutation commit; Ruleset content remains unchanged.

For `split-git`, only the Dataset repository changes; the Ruleset repository remains unchanged.

## Exclusions

FS-002 does not define application-specific migration semantics, a migration engine, an upgrade engine, Git remote creation, push or synchronization behavior, branch-management workflows beyond deterministic initial repository state, provider APIs, automated deployment, universal Ruleset versioning, universal Dataset schema versioning, or additional serialization formats.

FS-002 does not revise the accepted FS-001 provider profiles except where compatibility validation is required to ensure provider adaptation does not redefine package topology.
