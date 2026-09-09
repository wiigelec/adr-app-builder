# FS-004 — Repo-Spec-Aware Application Repositories

### FS-004-NR-001 — Functional Set Scope

**Classification: S**

FS-004 shall extend the accepted `split-git` realization with repo-spec-aware Ruleset repository lifecycle management while preserving inherited ADR application-instance, Ruleset, Dataset, binding, compatibility, transition, and initialization semantics without adding a new ADR semantic role.

### FS-004-NR-002 — Lifecycle Profile Boundary

**Classification: B**


FS-004 repo-spec lifecycle behavior shall apply only to `split-git`. `single-file`, `split-files`, and `single-git` shall retain their accepted lifecycle behavior and shall not receive FS-004 repo-spec lifecycle installation.

### FS-004-NR-003 — Mandatory Split-Git Ruleset Lifecycle

**Classification: M**


Every newly generated `split-git` Ruleset repository shall be constructed by invoking the selected accepted repo-spec revision's `repo-spec init --repo DESTINATION` initializer against an empty candidate, shall preserve the initializer-produced lifecycle scaffold, and shall support the installed Design → Planning → Build → Validation → Semantic Review → Acceptance repository-development lifecycle. After initialization and before adding App Builder application material, App Builder shall adapt only the installed canonical `repo/validation/structure-policy.json` to authorize maintained root files `application.json`, `binding.json`, and `provenance.json`, maintained root directory `init-config`, and exactly the selected FS-003 Ruleset runtime root role (`ruleset.json` as a root file or `ruleset` as a root directory), while preserving initializer-supplied authorization and default-deny semantics. Accepted repo-spec revision `f241d287e0ca9476c3ea96e3c5ad0cc49767ed04` is the reviewed baseline for this initializer contract.

### FS-004-NR-004 — Dataset Lifecycle Exclusion

**Classification: M**


The paired `split-git` Dataset repository shall not contain repo-spec product-development lifecycle installation or repository-development ownership surfaces.

### FS-004-NR-005 — No Independent Lifecycle Selector

**Classification: M**


`split-git` shall have no independent configuration option that disables, selects, or substitutes the FS-004 repo-spec lifecycle contract.

### FS-004-NR-006 — Provider Lifecycle Independence

**Classification: M**


Changing only provider selection shall not enable, disable, reinterpret, or alter FS-004 lifecycle eligibility or installed repo-spec framework content.

### FS-004-NR-007 — Ruleset Product Repository Role

**Classification: S**

The `split-git` Ruleset repository is the repository-development home for the application-rule product; repo-spec lifecycle management shall not make repo-spec an authority over application-owned Ruleset meaning.

### FS-004-NR-008 — Runtime Ruleset Location Preservation

**Classification: M**


Installing repo-spec lifecycle material shall preserve the accepted FS-003 runtime Ruleset realization at its runtime location and shall not require runtime Ruleset material to move beneath `product/`.

### FS-004-NR-009 — Framework and Product-State Separation

**Classification: M**


Generated Ruleset repositories shall keep reusable repo-spec framework state mechanically distinguishable from repository-specific product-development state, accepted runtime Ruleset material, construction provenance, and `init-config/`.

### FS-004-NR-010 — Bootstrap Non-Acceptance

**Classification: S**

Generic App Builder-generated lifecycle or guidance material shall not become accepted repository-specific Product Design, normative requirements, or application semantics merely because it was generated during construction.

### FS-004-NR-011 — Exact Accepted Repo-Spec Source

**Classification: M**


Each `split-git` build shall resolve one supplying repo-spec repository `refs/heads/main` to one exact accepted commit, fetch that exact commit, and invoke the repo-spec initializer from that fetched supplying checkout. App Builder shall not manually substitute a selectively copied framework surface for the initializer-produced repository.

### FS-004-NR-012 — Repo-Spec Source Truthfulness

**Classification: M**


Generated repo-spec source lineage shall identify the actual supplying repository and resolved commit used for installation and shall not silently substitute another repository or revision.

### FS-004-NR-013 — Ruleset/Dataset Binding Determinacy

**Classification: S**

The generated `split-git` repository pair shall preserve enough stable realization identity or traceability to determine which exact Ruleset realization is bound as the applicable Ruleset authority for the application instance while Ruleset and Dataset repositories evolve independently, without making the binding metadata itself semantic authority.

### FS-004-NR-014 — Binding Representation Non-Prescription

**Classification: S**

The FS-004 `binding.json` mechanism is an App Builder realization-binding choice and shall not be represented as a universal ADR binding encoding, versioning model, repository technology, application-owned binding rule, or application-specific semantic identifier.

### FS-004-NR-015 — Binding Authority Separation

**Classification: S**

FS-004 realization binding information shall determinately identify which Ruleset realization is bound to the application instance while remaining non-authoritative metadata: it shall not create Ruleset meaning, transfer committed-state authority away from the Dataset, or override, reinterpret, normalize, or replace application-owned Ruleset semantics or binding-related source fields.

### FS-004-NR-016 — Initialization Determinacy

**Classification: M**


A fresh generated `split-git` realization shall expose enough repository-local material to establish application identity, selected application-instance identity, the exact Ruleset realization bound as applicable authority, the application-owned semantics governing that Ruleset's meaning and compatibility behavior, authoritative Dataset state location, and required binding information without prior conversational context, the App Builder checkout, or the supplying repo-spec checkout.

### FS-004-NR-017 — Dataset Repository Operational Role

**Classification: S**

The `split-git` Dataset repository shall remain independently evolving application-instance persistence rather than a repo-spec product-development repository.

### FS-004-NR-018 — Dataset-Side Governance Ownership

**Classification: S**

Ruleset-owned validation, compatibility, migration, refusal, recovery, or related mechanisms remain Ruleset-owned when installed into or invoked from the Dataset repository; physical location shall not redefine semantic ownership.

### FS-004-NR-019 — Dataset Lifecycle Non-Transfer

**Classification: M**


Dataset-side Ruleset-governance tooling, when present, shall not install, imply, or require repo-spec product-development lifecycle ownership in the Dataset repository.

### FS-004-NR-020 — Generic Product Readiness

**Classification: M**


The generated Ruleset repository shall preserve the reusable framework, generic product-development scaffold, root Validation composition, CI Validation delegation, and framework source identity produced by the selected repo-spec initializer, while adding App Builder lifecycle guidance required to begin later repository-specific Ruleset product development without inventing repository-specific Product Design at construction time.

### FS-004-NR-021 — No Invented Application Semantics

**Classification: S**

FS-004 construction shall not invent application-specific normative requirements, Dataset schemas, invariants, state vocabularies, validation semantics, compatibility semantics, migration semantics, or implementation merely to populate lifecycle surfaces.

### FS-004-NR-022 — Ruleset Repository Independence

**Classification: M**


After construction, the Ruleset repository shall execute its installed canonical repo-spec Validation and support ordinary repository-development lifecycle work without requiring the App Builder checkout or supplying repo-spec working tree.

### FS-004-NR-023 — Dataset Repository Independence

**Classification: M**


After construction, the Dataset repository shall remain usable as application-instance persistence according to the generated realization and applicable Ruleset binding without requiring App Builder to act as runtime, save, commit, or lookup service.

### FS-004-NR-024 — Repo-Spec Source Provenance

**Classification: M**


The generated Ruleset repository shall retain deterministic source lineage containing the normalized supplying repo-spec repository identity and exact resolved repo-spec commit installed during construction.

### FS-004-NR-025 — Provenance and Binding Distinction

**Classification: M**


Repo-spec source lineage and FS-004 realization binding shall be mechanically distinguishable from ADR provenance, App Builder provenance, ordinary Git history, Dataset committed-state values, and application-owned binding-related fields or semantics, while the binding remains sufficient to identify the bound runtime Ruleset realization.

### FS-004-NR-026 — Governance Artifact Traceability

**Classification: M**


When FS-004 installs Ruleset-owned governance artifacts into the Dataset repository, the generated realization shall preserve enough Ruleset identity or traceability to determine their governing Ruleset source where consequential.

### FS-004-NR-027 — Canonical Generated-Repository Validation

**Classification: M**


Every generated `split-git` Ruleset repository shall preserve executable root `scripts/validate` composition and repo-spec Validation surfaces installed by the selected initializer; after App Builder adapts the installed structural policy and adds application material, that canonical repository-wide Validation shall succeed.

### FS-004-NR-028 — Generated Candidate Validation

**Classification: M**


App Builder FS-004 Validation shall construct and evaluate generated candidate repository pairs and shall not treat successful file generation alone as evidence of conformance.

### FS-004-NR-029 — Deterministic Generated Trees

**Classification: M**


Equivalent resolved FS-004 build inputs, including the exact repo-spec source commit, shall produce byte-identical package-owned generated content and identical Git tree identity subject to the accepted FS-003 construction-time commit semantics.

### FS-004-NR-030 — Repo-Spec Upgrade Boundary

**Classification: S**

A later repo-spec framework upgrade is a Ruleset-repository lifecycle operation; FS-004 shall not make App Builder a universal post-construction repo-spec upgrade, migration, or runtime service.

### FS-004-NR-031 — Prior Functional Set Compatibility

**Classification: B**


FS-001, FS-002, and FS-003 remain applicable except where FS-004 deliberately strengthens the `split-git` Ruleset lifecycle contract. Existing runtime application, Ruleset, Dataset, application-owned binding-related fields, `init-config/`, provenance, save, provider, and Git construction semantics remain unchanged unless this specification explicitly states otherwise. FS-004 shall not infer new semantic meaning from arbitrary binding-looking source fields.
