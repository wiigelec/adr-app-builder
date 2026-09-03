# FS-002 — Ruleset/Dataset Packaging

### FS-002-NR-001 — Packaging Scope

**Classification: S**

A Ruleset/Dataset packaging profile shall control the physical persistence relationship, addressing, preservation, and writeback behavior of Ruleset and Dataset material without redefining their application-owned meaning.

### FS-002-NR-002 — Independent Component Identity

**Classification: S**

Every FS-002 package shall preserve Ruleset and Dataset as independently identifiable and addressable semantic components.

### FS-002-NR-003 — Provider Independence

**Classification: S**

Provider bootstrap or presentation adaptation shall not alter the selected Ruleset/Dataset package topology, merge Ruleset and Dataset semantics, or inject provider-owned meaning into either component.

### FS-002-NR-004 — Packaging Profile Set

**Classification: B**

Build shall provide the packaging profiles `single-file`, `split-files`, `single-git`, and `split-git`.

### FS-002-NR-005 — File Encoding

**Classification: B**

The `single-file` and `split-files` profiles shall use deterministic JSON serialization for FS-002.

### FS-002-NR-006 — Single-File Structure

**Classification: B**

The `single-file` profile shall generate one physical JSON package containing separately addressable top-level `ruleset` and `dataset` components.

### FS-002-NR-007 — Single-File Source Fidelity

**Classification: M**

Mechanical validation shall verify that the `single-file` package's `ruleset` value equals the source Ruleset object and its `dataset` value equals the source Dataset object.

### FS-002-NR-008 — Single-File Dataset Mutation Preservation

**Classification: S**

An accepted Dataset-only mutation of a `single-file` package may rewrite the containing file but shall preserve the Ruleset component unchanged.

### FS-002-NR-009 — Split-Files Structure

**Classification: B**

The `split-files` profile shall generate exactly two package files named `ruleset.json` and `dataset.json`, with no additional packaging manifest, wrapper, sidecar, application file, provenance file, or provider metadata file.

### FS-002-NR-010 — Split-Files Source Fidelity

**Classification: M**

Mechanical validation shall verify that `ruleset.json` preserves the source Ruleset and `dataset.json` preserves the source Dataset apart from deterministic JSON serialization.

### FS-002-NR-011 — Split-Files Dataset Mutation Isolation

**Classification: S**

An accepted Dataset-only mutation of a `split-files` package shall update `dataset.json` without rewriting or modifying `ruleset.json`.

### FS-002-NR-012 — Single-Git Structure

**Classification: B**

The `single-git` profile shall generate one Git repository whose package worktree contains distinct `ruleset.json` and `dataset.json` paths.

### FS-002-NR-013 — Single-Git Initial State

**Classification: B**

The `single-git` profile shall create one deterministic initial commit representing the generated Ruleset and Dataset package and shall not require or configure a Git remote.

### FS-002-NR-014 — Single-Git Dataset Mutation Isolation

**Classification: S**

An accepted Dataset-only mutation in a `single-git` package shall change Dataset content without changing Ruleset content and shall record the resulting shared-repository state as a Dataset mutation commit.

### FS-002-NR-015 — Split-Git Structure

**Classification: B**

The `split-git` profile shall generate two independent Git repositories: a Ruleset repository whose package worktree contains exactly `ruleset.json` and a Dataset repository whose package worktree contains exactly `dataset.json`.

### FS-002-NR-016 — Split-Git Initial State

**Classification: B**

Each `split-git` repository shall receive one deterministic initial commit and shall not require or configure a Git remote.

### FS-002-NR-017 — Split-Git Dataset Mutation Isolation

**Classification: S**

An accepted Dataset-only mutation in a `split-git` package shall change and commit only the Dataset repository; the Ruleset repository worktree and HEAD shall remain unchanged.

### FS-002-NR-018 — Deterministic Git Metadata

**Classification: M**

Mechanical validation shall verify that Git-backed package generation canonicalizes initial branch naming, commit metadata, timestamps, commit messages, and package content sufficiently for equivalent repeated builds to produce identical initial repository HEADs.

### FS-002-NR-019 — Ruleset Fidelity Across Topologies

**Classification: M**

Mechanical validation shall verify that all four packaging profiles preserve the same source Ruleset meaning and that Dataset-only mutation does not alter Ruleset material.

### FS-002-NR-020 — Dataset Fidelity Across Topologies

**Classification: M**

Mechanical validation shall verify that all four packaging profiles preserve the same source Dataset meaning before governed mutation.

### FS-002-NR-021 — Source Immutability

**Classification: M**

Generation and packaging validation shall not mutate source Ruleset or Dataset documents.

### FS-002-NR-022 — Provider-Topology Independence

**Classification: M**

Mechanical validation shall verify that selecting an existing provider profile does not change the Ruleset/Dataset topology or component content established by the selected packaging profile.

### FS-002-NR-023 — Repeat-Build Determinism

**Classification: M**

Equivalent repeated builds using the same Ruleset and Dataset sources, selected packaging profile, resolved ADR inputs, and App Builder implementation shall produce byte-identical file-backed packages and identical initial Git-backed package HEADs.

### FS-002-NR-024 — Runtime Evolution Boundary

**Classification: S**

Governed runtime Dataset mutations and their resulting Git commits are application-state evolution and shall not be classified as failure of initial build determinism.

### FS-002-NR-025 — Migration and Upgrade Exclusion

**Classification: S**

FS-002 shall preserve independent Ruleset/Dataset upgradeability but shall not define application-specific migration semantics, a migration engine, an upgrade engine, or a universal Ruleset or Dataset versioning scheme.
