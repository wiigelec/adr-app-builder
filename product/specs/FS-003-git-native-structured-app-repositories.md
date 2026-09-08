# FS-003 — Git-Native Structured Application Repositories

### FS-003-NR-001 — Functional Set Scope

**Classification: S**

FS-003 shall extend the accepted Git-backed `single-git` and `split-git` packaging profiles with self-contained runtime repositories, deterministic file-or-tree realization, preserved construction inputs, repository-local operational guidance, and explicit separation between active working state and persisted Dataset state without extending ADR semantic roles.

### FS-003-NR-002 — Git-Backed Profile Boundary

**Classification: B**

FS-003 runtime realization behavior shall apply only to `single-git` and `split-git`. `single-file` and `split-files` shall not accept FS-003 runtime realization configuration.

### FS-003-NR-003 — Construction Input Preservation

**Classification: M**

Every FS-003 generated Git repository shall contain `init-config/application.json`, `init-config/ruleset.json`, `init-config/dataset.json`, and `init-config/build.json` as byte-for-byte copies of the four CLI input files used to construct that repository.

### FS-003-NR-004 — Init-Config Non-Authority

**Classification: S**

`init-config/` is immutable construction lineage and shall not become runtime application, Ruleset, or Dataset authority. Ordinary runtime operation and Dataset persistence shall not modify it.

### FS-003-NR-005 — Runtime Application Definition

**Classification: M**

Every FS-003 generated Git repository shall contain deterministic root `application.json` semantically equal to the application-definition source supplied to the build.

### FS-003-NR-006 — Runtime Application Initialization Authority

**Classification: S**

Generated operational guidance shall direct the operating Agent or environment to consume the runtime application definition for application-owned initialization semantics without duplicating or reinterpreting application-specific initialization instructions in generated guidance.

### FS-003-NR-007 — Explicit Construction Provenance

**Classification: M**

Every FS-003 generated Git repository shall contain deterministic root `provenance.json` recording the ADR repository and exact resolved ADR commit plus the actual App Builder checkout repository identity and exact clean App Builder commit used for construction.

### FS-003-NR-008 — App Builder Repository Identity

**Classification: M**

For GitHub repositories, equivalent supported SSH and HTTPS origin forms for the same App Builder checkout shall normalize to one deterministic repository identity, while a forked checkout shall preserve the fork repository identity rather than substituting an assumed upstream.

### FS-003-NR-009 — Provenance Non-Authority

**Classification: S**

Construction provenance is immutable lineage and upgrade-anchor material only. It shall not become application, Ruleset, Dataset, provider, or active-working-state authority.

### FS-003-NR-010 — Runtime Component Representation

**Classification: B**

For each FS-003 Ruleset and Dataset runtime component, the build definition may independently select `file` or `tree` representation. Omitted runtime realization configuration shall default that component to `file`.

### FS-003-NR-011 — Build-Owned Physical Realization

**Classification: S**

The build definition owns runtime physical realization choices and deterministic file/tree mappings. Ruleset and Dataset semantic inputs shall not acquire App Builder-owned physical-layout meaning merely because they are realized as files or trees.

### FS-003-NR-012 — Ruleset/Dataset Semantic Ownership

**Classification: S**

FS-003 shall preserve the ADR ownership boundary in which Ruleset owns rules governing application interpretation, Dataset structure and validity, transitions, compatibility, and migration semantics, while Dataset owns committed application-instance data. Physical realization location shall not transfer semantic ownership.

### FS-003-NR-013 — File Representation

**Classification: M**

A file-backed runtime Ruleset shall be realized as deterministic root `ruleset.json`, and a file-backed runtime Dataset shall be realized as deterministic root `dataset.json`, each semantically equal to its parsed source input.

### FS-003-NR-014 — Tree Mapping Syntax and Path Safety

**Classification: M**

Tree realization shall require a non-empty deterministic mapping of normalized relative POSIX output paths to RFC 6901 JSON Pointers and shall reject absolute paths, traversal, empty or dot path segments, `.git` segments, duplicate normalized paths, invalid pointers, nonexistent selectors, and package-owned path collisions.

### FS-003-NR-015 — Tree Mapping Non-Overlap

**Classification: M**

Within one runtime component mapping, duplicate source selectors and overlapping ancestor/descendant source selectors shall be rejected.

### FS-003-NR-016 — Lossless Tree Realization

**Classification: M**

Selected values in each tree mapping shall collectively preserve the complete source document without omission or duplication, and deterministic reconstruction using the configured mapping shall produce a JSON value semantically equal to the complete source document.

### FS-003-NR-017 — Deterministic Tree Serialization

**Classification: M**

Tree output paths shall be generated in deterministic order and each selected value shall be serialized deterministically as JSON.

### FS-003-NR-018 — Runtime Package References

**Classification: M**

Git package references shall identify each runtime Ruleset and Dataset component with explicit `kind` and `path` information corresponding to its realized file or tree shape; split-Git references shall additionally retain repository location information.

### FS-003-NR-019 — Generated Repository Guidance

**Classification: M**

Every FS-003 generated repository shall contain deterministic topology-appropriate `README.md` and `AGENTS.md` describing repository role, runtime component locations, `init-config/` purpose, application initialization source, provenance role, active-versus-persisted state, and save preservation behavior without creating application-specific semantics.

### FS-003-NR-020 — Active Working State

**Classification: S**

An active application session may maintain governed working state newer than the persisted Dataset. Governed edits to active working state shall not implicitly require Dataset persistence.

### FS-003-NR-021 — Explicit Dataset Persistence

**Classification: S**

Persisting governed working state to the Dataset is a distinct application operation and shall occur only when application semantics and a user request or user-accepted save authorize persistence.

### FS-003-NR-022 — Dataset Save Preservation

**Classification: M**

Ordinary Dataset save behavior shall preserve runtime application definition, runtime Ruleset material, `provenance.json`, `init-config/`, `README.md`, `AGENTS.md`, and all other non-Dataset generated realization material unchanged.

### FS-003-NR-023 — Split-Git Isolation

**Classification: M**

For `split-git`, ordinary Dataset persistence shall change only Dataset runtime material and Dataset-repository history; the Ruleset repository shall remain unchanged.

### FS-003-NR-024 — Post-Construction Independence

**Classification: S**

After repository construction completes, ordinary generated-application initialization, active-state management, Dataset persistence, and runtime Git history evolution shall not require App Builder to remain available or participate as a runtime, save, or commit service.

### FS-003-NR-025 — Initial Git Repository State

**Classification: M**

Each FS-003 generated Git repository shall use canonical branch `main` and contain exactly one initial commit with the complete generated tree, fixed message `ADR App Builder initial package`, App Builder-controlled author/committer identity, and actual construction-time author/committer timestamps.

### FS-003-NR-026 — Generated Tree Determinism

**Classification: M**

Equivalent resolved FS-003 build inputs shall produce byte-identical generated package-owned content and identical Git tree identity. Initial commit SHA need not be identical because construction time participates in commit identity.

### FS-003-NR-027 — No Bootstrap Marker Artifacts

**Classification: M**

FS-003 generated repositories shall not create a separate bootstrap/creation commit or `.adr-app-builder-created.json` marker.

### FS-003-NR-028 — Provider Independence

**Classification: M**

Changing only provider selection shall not alter generated FS-003 runtime application semantics, Ruleset/Dataset realization shape or content, construction provenance, or repository guidance.

### FS-003-NR-029 — Backward-Compatible Git Defaults

**Classification: M**

When no FS-003 runtime realization section is supplied, existing Git-backed packaging shall retain file-backed runtime names `ruleset.json` and `dataset.json` while gaining the accepted FS-003 repository material required by this specification.

### FS-003-NR-030 — FS-004 Exclusion

**Classification: S**

FS-003 does not define repo-spec-aware repository lifecycle installation, Ruleset-repository product-development scaffolding, Dataset-repository lifecycle eligibility, or other DP-102 / FS-004 behavior. Such behavior requires a later accepted Functional Set.
