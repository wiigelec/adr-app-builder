# FS-002 — Ruleset/Dataset Packaging Plan

## Objective

Add the four DP-100 Ruleset/Dataset packaging classes without collapsing the semantic boundary between Ruleset and Dataset or expanding into migration, deployment, or remote Git lifecycle management.

## Package Contract

Packaging operates on the Ruleset and Dataset source documents. The selected packaging profile determines their physical persistence relationship and writeback behavior.

Application definition, provider bootstrap or presentation adaptation, and ADR/App Builder build provenance remain realization context rather than Ruleset/Dataset package content.

A build creates one Ruleset/Dataset package for the selected packaging profile. All provider realizations selected by that build consume or reference that same package. The builder shall not duplicate the package into separate mutable provider-owned copies.

The four profile identifiers are:

- `single-file`
- `split-files`
- `single-git`
- `split-git`

Across all four topologies, parsing generated JSON content shall produce Ruleset and Dataset values equal to the corresponding source JSON values before governed mutation.

## Single-File Package

Generate one JSON package with separately addressable top-level `ruleset` and `dataset` components.

The parsed embedded Ruleset value shall equal the parsed source Ruleset value exactly. The parsed embedded Dataset value shall equal the parsed source Dataset value exactly.

A Dataset-only mutation rewrites the containing file as needed while preserving the Ruleset component exactly.

## Split-Files Package

Generate exactly two package files:

- `ruleset.json`
- `dataset.json`

Parsing each generated file shall produce a value equal to its corresponding parsed source document.

No manifest, wrapper, provenance sidecar, application file, or provider metadata file is part of the split-files package.

A Dataset-only mutation rewrites `dataset.json` only.

## Single-Git Package

Generate one Git repository whose package worktree contains:

- `ruleset.json`
- `dataset.json`

Ruleset and Dataset remain distinct repository paths.

Parsing `ruleset.json` and `dataset.json` shall produce values equal to the corresponding parsed source documents.

The builder creates a deterministic initial repository state with one initial commit. Commit metadata and message shall be canonicalized so equivalent resolved build inputs produce the same initial Git package identity.

The initial and subsequent package commit identities are storage-level provenance for the shared Git package. They do not replace application-semantic Ruleset or Dataset identity.

No remote is required or configured by FS-002.

A Dataset-only mutation changes `dataset.json` and records a Dataset mutation commit without changing `ruleset.json`.

## Split-Git Package

Generate two independent Git repositories.

The Ruleset repository worktree contains exactly `ruleset.json`. The Dataset repository worktree contains exactly `dataset.json`.

Parsing each repository's JSON file shall produce a value equal to its corresponding parsed source document.

Each repository receives a deterministic initial commit with canonical commit metadata and message. Each repository HEAD is storage-level provenance for that package component and does not replace application-semantic identity. No remote is required or configured by FS-002.

A Dataset-only mutation changes and commits only the Dataset repository. The Ruleset repository HEAD and worktree remain unchanged.

## Deterministic Git Initialization

Git-backed packages shall use canonical initial branch naming, author/committer identity, timestamps, commit messages, and repository content sufficient to make equivalent repeated builds produce identical initial repository HEADs.

Exact canonical values are Build choices, but Validation shall establish repeat-build identity.

Runtime mutation commits are state evolution and are not required to reproduce the initial build commit.

## Provider Compatibility

Provider profiles remain presentation/bootstrap adapters. Provider-specific material shall not be inserted into Ruleset or Dataset components and shall not change the selected package topology.

A provider realization may carry a reference or delivery adaptation for the package, but provider selection shall not cause the builder to generate an independent mutable Ruleset/Dataset package copy per provider.

FS-002 validation shall exercise at least the existing generic and Microsoft Copilot provider selections against the same generated package to ensure package semantics and Dataset authority remain provider-independent.

## Reference Fixture

Extend or add packaging fixtures based on the task-tracker sources. The fixture shall build all four packaging profiles from the same Ruleset and Dataset source documents.

For a multi-provider build, the fixture shall verify that all selected provider adaptations resolve to or consume the same package instance rather than separate mutable package copies.

Mutation fixtures shall perform one Dataset-only state change for each topology and verify Ruleset preservation plus topology-specific writeback behavior.

## Validation

Validation shall check profile existence and shape, exact parsed Ruleset/Dataset value fidelity, deterministic package structure, single-file component addressability, split-files exact two-file shape, single-Git path separation, split-Git repository separation, deterministic initial Git HEADs, Dataset-only mutation preservation, source immutability, provider-topology independence, shared-package provider composition, Git storage-provenance behavior, and repeat-build determinism.

Repository-wide Validation remains the mechanical acceptance entry point.
