# FS-004 — Repo-Spec-Aware Application Repositories Plan

design_revision: ac7cca859e6027461f9a23694fb7d8cf38ae026a

## Objective

Implement DP-102 by extending the accepted FS-003 `split-git` realization with a repo-spec-managed Ruleset repository paired with a non-repo-spec Dataset repository.

The Build shall preserve all accepted FS-001 through FS-003 behavior except where FS-004 deliberately strengthens the `split-git` lifecycle contract.

This Planning artifact shall not create new ADR or application-specific semantic meaning.

## Planned Functional Scope

FS-004 work is bounded to:

- selecting and resolving one exact accepted repo-spec framework source for each `split-git` build;
- installing reusable repo-spec framework material into the generated Ruleset repository;
- creating generic Ruleset product-development surfaces required by the installed framework without inventing application-specific Product Design;
- excluding repo-spec lifecycle material from the Dataset repository and non-`split-git` packaging profiles;
- preserving accepted runtime Ruleset and Dataset realizations from FS-003;
- establishing a determinate Ruleset/Dataset binding mechanism for independently evolving split repositories;
- preserving initialization determinacy under that binding;
- extending generated provenance/source-lineage material as needed to distinguish repo-spec source, Ruleset identity, and Ruleset/Dataset binding;
- preserving post-construction independence;
- validating generated candidate repositories mechanically.

## Planning Decisions to Resolve in Build

The following mechanisms must be selected during Build without changing the Functional Set's semantic requirements:

### Repo-Spec source selection

Build shall select:

- the CLI/build-definition surface by which the repo-spec source is supplied or resolved;
- the accepted-state verification procedure;
- exact revision resolution;
- supported source transports;
- failure behavior for dirty, unaccepted, missing, ambiguous, or mismatched source state.

The selected mechanism must produce one exact accepted framework revision and truthful source identity.

### Framework installation

Build shall determine the exact reusable framework-owned files and directories copied or generated into the Ruleset repository.

The installation must preserve repo-spec's distinction between reusable framework material and repository-specific product material.

Initializer-product-specific Product Design or implementation shall not be copied as though it were the generated Ruleset product's accepted semantics.

### Generic product scaffolding

Build may create generic lifecycle surfaces required for later Ruleset product engineering.

Any generated repository-specific content must be structurally generic and must not invent application-specific:

- normative requirements;
- Dataset schema;
- invariants;
- state vocabulary;
- compatibility semantics;
- migration semantics;
- validation meaning;
- implementation.

### Ruleset/Dataset binding

Build shall select one deterministic, mechanically evaluable binding representation that preserves enough identity or traceability to determine applicable Ruleset authority where consequential.

The selected mechanism must:

- survive independent Ruleset and Dataset repository evolution;
- remain distinguishable from Dataset committed-state values;
- remain distinguishable from ADR, App Builder, and repo-spec source provenance;
- not use ordinary Git commit identity as a substitute for application-semantic identity unless the realization intentionally defines a traceable reference whose semantics remain clear;
- permit fresh initialization to determine applicable Ruleset authority.

The mechanism may use generated metadata or references, but its concrete format is a Build decision rather than upstream ADR meaning.

### Initialization material

Build shall ensure generated repository-local guidance and metadata allow a fresh operation to establish:

- application identity;
- application-instance identity;
- applicable Ruleset authority;
- authoritative Dataset state location;
- required binding information.

Existing FS-003 runtime `application.json`, component references, and provenance material should be reused where sufficient rather than duplicated without need.

### Dataset-side Ruleset governance artifacts

Build may install Ruleset-owned validators, migration helpers, wrappers, or entry points in the Dataset repository only when required by the selected realization.

When installed, their governing Ruleset source must remain traceable and their physical presence must not create repo-spec lifecycle ownership in the Dataset repository.

FS-004 does not require application-specific governance artifacts to exist in the generic reference realization.

### Provenance/source relationship

Build shall determine the minimal deterministic additions necessary to preserve:

- exact repo-spec framework source identity and revision;
- distinction from ADR/App Builder construction provenance;
- distinction from runtime Ruleset identity;
- distinction from Ruleset/Dataset binding;
- traceability of Dataset-side Ruleset-owned governance artifacts when present.

Existing `provenance.json` remains construction lineage. Build should extend or complement it only where the resulting roles remain mechanically distinguishable.

### Generated repository validation

Build shall define functional Validation tasks that evaluate generated candidate repository pairs.

Validation shall avoid treating successful file generation alone as evidence of conformance.

Tests shall exercise both positive and negative lifecycle/binding/source cases where mechanically decidable.

## Stable Normative Requirement IDs

The canonical FS-004 normative specification shall use the following IDs and classifications.

These IDs are reserved by Planning and shall not be renumbered during Build. Wording may be refined only to preserve the accepted Design meaning.

| ID | Title | Class |
| --- | --- | --- |
| FS-004-NR-001 | Functional Set Scope | S |
| FS-004-NR-002 | Lifecycle Profile Boundary | B |
| FS-004-NR-003 | Mandatory Split-Git Ruleset Lifecycle | M |
| FS-004-NR-004 | Dataset Lifecycle Exclusion | M |
| FS-004-NR-005 | No Independent Lifecycle Selector | M |
| FS-004-NR-006 | Provider Lifecycle Independence | M |
| FS-004-NR-007 | Ruleset Product Repository Role | S |
| FS-004-NR-008 | Runtime Ruleset Location Preservation | M |
| FS-004-NR-009 | Framework and Product-State Separation | M |
| FS-004-NR-010 | Bootstrap Non-Acceptance | S |
| FS-004-NR-011 | Exact Accepted Repo-Spec Source | M |
| FS-004-NR-012 | Repo-Spec Source Truthfulness | M |
| FS-004-NR-013 | Ruleset/Dataset Binding Determinacy | S |
| FS-004-NR-014 | Binding Representation Non-Prescription | S |
| FS-004-NR-015 | Binding Authority Separation | S |
| FS-004-NR-016 | Initialization Determinacy | M |
| FS-004-NR-017 | Dataset Repository Operational Role | S |
| FS-004-NR-018 | Dataset-Side Governance Ownership | S |
| FS-004-NR-019 | Dataset Lifecycle Non-Transfer | M |
| FS-004-NR-020 | Generic Product Readiness | M |
| FS-004-NR-021 | No Invented Application Semantics | S |
| FS-004-NR-022 | Ruleset Repository Independence | M |
| FS-004-NR-023 | Dataset Repository Independence | M |
| FS-004-NR-024 | Repo-Spec Source Provenance | M |
| FS-004-NR-025 | Provenance and Binding Distinction | M |
| FS-004-NR-026 | Governance Artifact Traceability | M |
| FS-004-NR-027 | Canonical Generated-Repository Validation | M |
| FS-004-NR-028 | Generated Candidate Validation | M |
| FS-004-NR-029 | Deterministic Generated Trees | M |
| FS-004-NR-030 | Repo-Spec Upgrade Boundary | S |
| FS-004-NR-031 | Prior Functional Set Compatibility | B |

Classification follows the repository's accepted convention:

- **S** — semantic requirement whose correctness ultimately requires semantic review;
- **B** — boundary/compatibility requirement;
- **M** — mechanically decidable requirement expected to bind to product Validation.

## Planned Requirement Meaning

### FS-004-NR-001 — Functional Set Scope

FS-004 is limited to the repo-spec-aware realization of `split-git` application repositories and shall not extend upstream ADR semantic roles.

### FS-004-NR-002 — Lifecycle Profile Boundary

Repo-spec lifecycle behavior applies only to `split-git`; `single-file`, `split-files`, and `single-git` retain their accepted lifecycle behavior.

### FS-004-NR-003 — Mandatory Split-Git Ruleset Lifecycle

Every newly generated `split-git` Ruleset repository receives the selected accepted repo-spec framework and its repository-development lifecycle.

### FS-004-NR-004 — Dataset Lifecycle Exclusion

The paired `split-git` Dataset repository does not receive repo-spec product-development lifecycle material.

### FS-004-NR-005 — No Independent Lifecycle Selector

`split-git` has no independent option that disables or selects repo-spec lifecycle installation.

### FS-004-NR-006 — Provider Lifecycle Independence

Changing provider selection does not enable, disable, or alter FS-004 lifecycle eligibility.

### FS-004-NR-007 — Ruleset Product Repository Role

The `split-git` Ruleset repository is the repository-development home for application-rule product engineering.

### FS-004-NR-008 — Runtime Ruleset Location Preservation

Installing repo-spec lifecycle material does not require accepted runtime Ruleset material to move beneath `product/`.

### FS-004-NR-009 — Framework and Product-State Separation

Generated Ruleset repositories keep reusable repo-spec framework state distinguishable from repository-specific product-development state and accepted runtime Ruleset material.

### FS-004-NR-010 — Bootstrap Non-Acceptance

Generic App Builder-generated bootstrap material does not become accepted future Product Design merely because it was generated during construction.

### FS-004-NR-011 — Exact Accepted Repo-Spec Source

Each `split-git` build consumes one exact accepted repo-spec framework revision.

### FS-004-NR-012 — Repo-Spec Source Truthfulness

Generated source lineage identifies the actual selected repo-spec source/revision and does not silently substitute an unrelated revision.

### FS-004-NR-013 — Ruleset/Dataset Binding Determinacy

The generated repository pair preserves enough identity or traceability to determine the applicable Ruleset authority when consequential while the repositories evolve independently.

### FS-004-NR-014 — Binding Representation Non-Prescription

FS-004 does not define one universal binding encoding, version field, Git reference, artifact format, or lookup protocol.

### FS-004-NR-015 — Binding Authority Separation

Ruleset/Dataset binding information does not become independent semantic authority or transfer committed-state authority away from the Dataset.

### FS-004-NR-016 — Initialization Determinacy

A fresh generated realization can establish application identity, instance identity, applicable Ruleset authority, authoritative Dataset state, and required binding information without prior conversational context or construction checkouts.

### FS-004-NR-017 — Dataset Repository Operational Role

The Dataset repository remains application-instance persistence rather than a repo-spec product-development repository.

### FS-004-NR-018 — Dataset-Side Governance Ownership

Ruleset-owned validation, compatibility, migration, refusal, recovery, or related mechanisms remain Ruleset-owned when installed or invoked Dataset-side.

### FS-004-NR-019 — Dataset Lifecycle Non-Transfer

Dataset-side Ruleset-governance tooling does not install or imply repo-spec product-development lifecycle ownership in the Dataset repository.

### FS-004-NR-020 — Generic Product Readiness

The generated Ruleset repository contains the generic repo-spec lifecycle surfaces required for later repository-specific Ruleset product engineering.

### FS-004-NR-021 — No Invented Application Semantics

Construction scaffolding does not invent application-specific requirements, schemas, invariants, validation semantics, migration semantics, or implementation.

### FS-004-NR-022 — Ruleset Repository Independence

After construction the Ruleset repository can perform its installed lifecycle without the App Builder checkout or supplying repo-spec working tree.

### FS-004-NR-023 — Dataset Repository Independence

After construction the Dataset repository remains usable as application-instance persistence according to the generated realization and applicable Ruleset binding without App Builder acting as a runtime service.

### FS-004-NR-024 — Repo-Spec Source Provenance

The generated Ruleset repository retains sufficient exact source lineage to identify the installed repo-spec framework revision.

### FS-004-NR-025 — Provenance and Binding Distinction

Repo-spec source lineage and Ruleset/Dataset binding remain mechanically distinguishable from ADR provenance, App Builder provenance, ordinary repository history, and Dataset committed-state values.

### FS-004-NR-026 — Governance Artifact Traceability

When Ruleset-owned governance artifacts are installed Dataset-side, enough Ruleset identity or traceability is preserved to determine their governing Ruleset source where consequential.

### FS-004-NR-027 — Canonical Generated-Repository Validation

The generated Ruleset repository provides the canonical repo-spec Validation composition required by the installed framework.

### FS-004-NR-028 — Generated Candidate Validation

App Builder Validation evaluates generated candidate repositories rather than treating successful generation as conformance evidence.

### FS-004-NR-029 — Deterministic Generated Trees

Equivalent resolved FS-004 build inputs produce deterministic package-owned content and generated Git tree identity subject to accepted FS-003 construction-time commit semantics.

### FS-004-NR-030 — Repo-Spec Upgrade Boundary

Later repo-spec framework upgrade is a Ruleset-repository lifecycle operation; FS-004 does not create a universal App Builder-driven upgrade engine.

### FS-004-NR-031 — Prior Functional Set Compatibility

FS-001 through FS-003 remain applicable except where FS-004 deliberately strengthens the `split-git` Ruleset lifecycle contract.

## Planned Validation Task Decomposition

Build should introduce functional task names only after the concrete implementation surfaces are known.

Likely validation responsibilities include:

- lifecycle/profile eligibility;
- repo-spec source acceptance and identity;
- framework installation and framework/product separation;
- binding and initialization determinacy;
- generated-repository independence;
- provenance and governance-artifact traceability;
- deterministic generated repository realization.

The exact task names are intentionally not normative at this Planning step.

Mechanically classified FS-004 requirements shall be added to `product/validation/requirement-evaluation.json` only when their corresponding real Validation tasks exist. Placeholder or vacuous bindings are prohibited.

## Build Sequence

1. Select the repo-spec source contract and exact accepted-state resolution mechanism.
2. Define reusable framework installation surfaces.
3. Define generic Ruleset product scaffolding.
4. Define the deterministic split-git Ruleset/Dataset binding representation.
5. Define any required provenance/source-lineage extensions.
6. Extend generated Ruleset and Dataset repository guidance.
7. Implement generated repository construction changes.
8. Add functional Validation tasks and bind every mechanically classified FS-004 requirement.
9. Add the canonical `product/specs/FS-004-repo-spec-aware-application-repositories.md` using the reserved IDs above.
10. Run generated candidate Validation, full canonical Validation, semantic review, and acceptance workflow.

## Exclusions

This plan does not authorize:

- lifecycle installation for `single-file`, `split-files`, or `single-git`;
- repo-spec lifecycle installation in Dataset repositories;
- application-specific schema or migration invention;
- a universal Ruleset/Dataset binding format beyond the selected FS-004 realization mechanism;
- automatic repo-spec framework upgrades;
- runtime App Builder participation after construction;
- provider-specific changes to lifecycle eligibility;
- changes to upstream ADR semantics.
