# FS-002 — Ruleset/Dataset Packaging Plan

## Objective

Add the four DP-100 Ruleset/Dataset packaging classes without collapsing the semantic boundary between Ruleset and Dataset or expanding into migration, deployment, or remote Git lifecycle management.

## Package Contract

Packaging operates on the Ruleset and Dataset source documents. The selected packaging profile determines their physical persistence relationship and writeback behavior.

Application definition, provider bootstrap or presentation adaptation, and ADR/App Builder build provenance remain realization context rather than Ruleset/Dataset package content.

The four profile identifiers are:

- `single-file`
- `split-files`
- `single-git`
- `split-git`

## Single-File Package

Generate one JSON package with separately addressable top-level `ruleset` and `dataset` components.

The embedded Ruleset value shall equal the source Ruleset object exactly. The embedded Dataset value shall equal the source Dataset object exactly.

A Dataset-only mutation rewrites the containing file as needed while preserving the Ruleset component exactly.

## Split-Files Package

Generate exactly two package files:

- `ruleset.json`
- `dataset.json`

Each file shall preserve its corresponding source document exactly apart from deterministic JSON serialization.

No manifest, wrapper, provenance sidecar, application file, or provider metadata file is part of the split-files package.

A Dataset-only mutation rewrites `dataset.json` only.

## Single-Git Package

Generate one Git repository whose package worktree contains:

- `ruleset.json`
- `dataset.json`

Ruleset and Dataset remain distinct repository paths.

The builder creates a deterministic initial repository state with one initial commit. Commit metadata and message shall be canonicalized so equivalent resolved build inputs produce the same initial Git package identity.

No remote is required or configured by FS-002.

A Dataset-only mutation changes `dataset.json` and records a Dataset mutation commit without changing `ruleset.json`.

## Split-Git Package

Generate two independent Git repositories.

The Ruleset repository worktree contains exactly `ruleset.json`. The Dataset repository worktree contains exactly `dataset.json`.

Each repository receives a deterministic initial commit with canonical commit metadata and message. No remote is required or configured by FS-002.

A Dataset-only mutation changes and commits only the Dataset repository. The Ruleset repository HEAD and worktree remain unchanged.

## Deterministic Git Initialization

Git-backed packages shall use canonical initial branch naming, author/committer identity, timestamps, commit messages, and repository content sufficient to make equivalent repeated builds produce identical initial repository HEADs.

Exact canonical values are Build choices, but Validation shall establish repeat-build identity.

Runtime mutation commits are state evolution and are not required to reproduce the initial build commit.

## Provider Compatibility

Provider profiles remain presentation/bootstrap adapters. Provider-specific material shall not be inserted into Ruleset or Dataset components and shall not change the selected package topology.

FS-002 validation shall exercise at least the existing generic and Microsoft Copilot provider selections against the new packaging model to ensure package semantics remain provider-independent.

## Reference Fixture

Extend or add packaging fixtures based on the task-tracker sources. The fixture shall build all four packaging profiles from the same Ruleset and Dataset source documents.

Mutation fixtures shall perform one Dataset-only state change for each topology and verify Ruleset preservation plus topology-specific writeback behavior.

## Validation

Validation shall check profile existence and shape, exact Ruleset/Dataset fidelity, deterministic package structure, single-file component addressability, split-files exact two-file shape, single-Git path separation, split-Git repository separation, deterministic initial Git HEADs, Dataset-only mutation preservation, source immutability, provider-topology independence, and repeat-build determinism.

Repository-wide Validation remains the mechanical acceptance entry point.
