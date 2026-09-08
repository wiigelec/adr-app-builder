---
doc_id: DP-102
title: Repo-Spec-Aware Application Repositories
depends_on:
  - DP-100
  - DP-101
---

# Repo-Spec-Aware Application Repositories

## Purpose

ADR App Builder shall support optional repo-spec-aware realization of generated Git repositories so sufficiently complex ADR-derived applications can carry an independently usable repository-development lifecycle for their Ruleset and other application-rule development concerns.

Repo-spec integration is a repository-development concern. It does not extend ADR semantics, does not add another ADR semantic component, and does not make repo-spec authority over application-owned Ruleset or Dataset meaning.

This Design extends DP-100 and DP-101. It preserves App Builder's role as construction tooling, the semantic separation among application definition, Ruleset, Dataset, packaging, and provider adaptation, and the post-construction independence of generated repositories.

## ADR Ownership Boundary

The governing ownership distinction remains semantic and intentionally simple:

- **Ruleset owns rules.**
- **Dataset owns data.**
- **Agent reasoning is transient and does not own committed application state merely by reasoning about it.**

The Ruleset therefore owns application meaning and governance, including rules that define interpretation of Dataset state, permitted and prohibited state, structural or schema requirements for Dataset data, invariants, transition validity and acceptance, mechanical validation obligations, compatibility semantics, and migration or transformation semantics required when Ruleset evolution changes the requirements placed on persisted Dataset data.

The Dataset owns the actual committed instance data governed by those rules.

A rule does not become Dataset-owned merely because it validates, transforms, or otherwise operates on Dataset data. Dataset data does not become Ruleset-owned merely because a Ruleset change requires that data to be validated, migrated, or transformed.

Ruleset evolution may therefore require a governed Dataset compatibility transition without transferring committed-state authority from the Dataset to the Ruleset.

This boundary follows semantic role rather than physical location, file type, execution location, or update frequency.

## Application Interaction Model

For architectural reasoning, an ADR-derived application may be understood approximately as:

- Agent — transient client and reasoning interface;
- Ruleset — application contract, governance, and business rules;
- Dataset — persistent application-instance state.

This comparison is explanatory rather than a required runtime architecture.

## Repository Development Lifecycle as a Ruleset Realization Choice

Repo-spec-aware realization provides a development lifecycle for application-rule development.

For a Ruleset-bearing generated Git repository, repo-spec may manage development of the Ruleset product itself through Design → Planning → Build → Validation → Semantic Review → Acceptance.

The accepted runtime Ruleset realization may remain at the runtime location established by the selected App Builder packaging and runtime-representation choices. Repo-spec lifecycle ownership does not require runtime Ruleset files to be relocated beneath `product/`.

The repo-spec `product/` domain owns development artifacts and implementation work for the Ruleset/application-rule product. Runtime Ruleset material remains the accepted operational realization governed by that lifecycle.

Repository-development lifecycle selection remains independent from packaging topology, runtime component representation, and provider adaptation. Selecting repo-spec-aware lifecycle behavior shall not require a new packaging topology, and provider profiles shall not modify the lifecycle choice.

## Dataset Repository Governance

A Dataset-only repository is not, merely by containing application data, a repo-spec product-development repository.

Its ordinary lifecycle is application operation over committed data rather than Design → Planning → Build development of application rules.

A Dataset repository may contain or consume Ruleset-defined mechanical validation, compatibility, or migration mechanisms needed to operate safely on its data. Such mechanisms remain Ruleset-owned application rules or implementations of those rules even when installed into, invoked from, or physically stored within a Dataset repository.

Installing a Ruleset-defined validator or migration mechanism into a Dataset repository does not create independent Dataset-side semantic authority and does not by itself install a repo-spec development lifecycle.

Dataset persistence remains governed by the applicable Ruleset semantics. An application may require validation before persistence or may require compatibility, migration, refusal, recovery, or author-governed resolution when the applicable Ruleset changes.

FS-004 does not define a separate repo-spec product-development lifecycle for Dataset-only repositories.

## Split-Git Roles

For split-Git packaging, the Ruleset and Dataset repositories have different lifecycle roles.

The Ruleset repository may be repo-spec-aware because it contains the application rules being developed and accepted. The Dataset repository remains an independently evolving application-instance data repository.

Ruleset-owned validation, compatibility, or migration mechanisms may be installed or made available to the Dataset repository when required by application-owned semantics, but those mechanisms shall not cause the Dataset repository to be represented as though its instance data were a repo-spec-developed product.

The lifecycle material selected for the Ruleset repository shall not silently impose repo-spec Design, Planning, or product-development authority on the Dataset repository.

## Single-Git Roles

A single-Git repository may contain both runtime Ruleset and runtime Dataset material while preserving their semantic roles.

When repo-spec-aware lifecycle is selected for a single-Git repository, the lifecycle governs development of the Ruleset/application-rule product. The Dataset material in that same repository remains committed application-instance data governed by the accepted Ruleset rather than becoming product-development state merely because both roles share one Git worktree.

Repository layout and shared Git persistence do not collapse Ruleset and Dataset ownership.

## Repo-Spec Source

A repo-spec-aware build shall consume one exact accepted repo-spec framework revision for each repo-spec framework state it installs.

The supplying repo-spec state shall be identified truthfully and exactly enough to determine the framework revision used for construction.

App Builder shall not silently substitute an unrelated repo-spec revision while representing the generated repository as having been constructed from the selected source.

The exact source-selection and resolution mechanism is a Planning and Build concern. Design does not require a particular remote, local checkout, archive format, or transport when equivalent source identity can be established correctly.

## Installed Framework Meaning

Repo-spec-aware realization installs the reusable repository-development framework, not the repo-spec initializer product's own product semantics.

Framework-owned repository state shall remain distinguishable from repository-specific Ruleset/application-rule development state, accepted runtime Ruleset realization, committed Dataset data, App Builder construction provenance, and `init-config/` construction inputs.

A repo-spec-aware generated repository shall preserve repo-spec's ownership distinction between reusable framework material and repository-specific product material. For an ADR application repository governed by this Design, repository-specific product material concerns development of application rules and their realizations.

App Builder-generated bootstrap material shall not masquerade as accepted future Product Design merely because App Builder constructed the initial repository.

## Runtime Material and Development Material

Runtime Ruleset and Dataset components retain the semantic ownership established by ADR, DP-100, and DP-101.

Installed repo-spec framework material is development-lifecycle material.

Generated repository guidance shall distinguish runtime Ruleset material as accepted operational application-rule realization, runtime Dataset material as committed application-instance data, repo-spec framework material as lifecycle infrastructure, repository-specific product material as development of the Ruleset/application-rule product, and App Builder provenance plus `init-config/` as construction lineage rather than runtime or development semantic authority.

Ruleset-defined Dataset validation or migration mechanisms remain rules or implementations of rules even when executed against Dataset data.

Ordinary application operation shall not require a repo-spec development action merely because repo-spec is installed. Ordinary Dataset state transition and persistence shall not be reclassified as Ruleset product development merely because the Dataset is governed by a repo-spec-developed Ruleset.

## Ruleset Evolution and Dataset Compatibility

Ruleset semantics may evolve independently from committed Dataset state.

A Ruleset change may be compatible with existing Dataset data without transformation, or it may introduce new structural requirements, state vocabulary, invariants, transition semantics, or other rules that make existing Dataset data incompatible with the newer Ruleset.

When that occurs, the application Ruleset owns the compatibility, migration, refusal, recovery, or other transition rules necessary to determine whether and how the existing Dataset may become valid under the newer Ruleset.

Applying those rules may produce modified Dataset data. The accepted result remains Dataset-owned committed application state.

Ruleset evolution shall not silently reinterpret incompatible committed Dataset data merely because a newer Ruleset exists. App Builder does not invent application-specific compatibility or migration meaning.

## Ruleset-Defined Dataset Validation and Migration

A complex Ruleset product may define or realize mechanical mechanisms that operate on Dataset data, including structural or schema validation, cross-record invariant validation, dependency or stale-state validation, compatibility evaluation, deterministic migrations, and migration preconditions or postconditions.

These mechanisms are developed and accepted through the Ruleset repository's lifecycle when they carry application-rule meaning or mechanically enforce accepted application rules.

A validator is not an independent semantic authority. A migration implementation is not an independent semantic authority. If validator or migration behavior conflicts with accepted Ruleset meaning or normative requirements, that is a Ruleset product defect.

A Dataset repository may receive installed copies, wrappers, or entry points for such mechanisms when a self-contained realization requires them. Installation location does not alter their semantic ownership.

## Post-Construction Independence

After successful construction, a repo-spec-aware repository shall be independently usable for its installed Design → Planning → Build → Validation → Semantic Review → Acceptance lifecycle without requiring the App Builder checkout or the supplying repo-spec working tree to remain available.

App Builder does not become the repository's runtime service, save service, commit service, Planning service, Validation service, migration service, or upgrade service after construction.

A later App Builder invocation is a separate realization operation.

A later repo-spec framework upgrade is a repository-development operation governed by the installed repository lifecycle and applicable repo-spec upgrade semantics, not an implicit App Builder runtime action.

## Product Readiness

A repo-spec-aware Ruleset-bearing generated repository shall be structurally ready for repository-specific Product Design and later lifecycle work on the Ruleset/application-rule product.

The installed lifecycle may establish generic product-development surfaces required by repo-spec, including Design, normative specification, implementation, and product Validation ownership surfaces.

Generic lifecycle scaffolding does not create application-specific Design meaning.

App Builder shall not invent application-specific normative requirements, Dataset schemas, validation rules, compatibility semantics, migration rules, validators, or implementation merely to populate the installed lifecycle.

Application-specific engineering begins when repository-specific Design establishes that meaning and Planning derives a bounded Functional Set from it.

Dataset-only repositories do not receive those product-development surfaces merely for symmetry.

## Application-Specific Schemas and Mechanical Enforcement

Repo-spec-aware Ruleset development is intended to provide a correct ownership location and lifecycle for application-specific engineering concerns that exceed ordinary unvalidated prose.

Examples include application-defined Dataset schemas, artifact relationship rules, lifecycle state definitions, provenance rules, deterministic invariants, stale-state semantics, compatibility rules, migration semantics, validation tooling, and other mechanical enforcement.

These concerns are Ruleset-side rules or realizations of Ruleset-side rules when they define or enforce what Dataset data means, may contain, or may become. Actual application-instance records and values remain Dataset data.

Mechanically decidable application requirements may be bound to Ruleset product Validation according to the installed repo-spec lifecycle. The same accepted validator logic may also be executed against a concrete Dataset instance as an application-state persistence or compatibility check.

Development Validation and Dataset-instance validation have different subjects even when they reuse the same implementation.

Semantic correctness remains subject to Semantic Review and Acceptance; passing mechanical Validation does not establish semantic completeness.

## Deterministic Construction

Repo-spec-aware lifecycle selection, Ruleset-owned Dataset-governance artifact selection, and the exact resolved repo-spec framework source are build inputs when applicable.

For equivalent resolved inputs, App Builder shall deterministically construct the same generated repository tree and package-owned file content, subject to the existing DP-100 and DP-101 treatment of Git construction timestamps and commit identity.

Repo-spec installation and Ruleset-owned Dataset-governance installation shall not introduce unexplained dependency on incidental local repository state.

Generated Git commit identity remains storage provenance rather than application-semantic or repo-spec-semantic identity.

## Provenance and Source Relationship

A repo-spec-aware generated repository shall retain sufficient exact source information to identify the repo-spec framework revision installed during construction.

That information is lineage and an upgrade anchor.

It does not make the supplying repo-spec repository a runtime authority, import supplier Git ancestry into the generated repository, or create a parallel Acceptance record.

Existing ADR and App Builder provenance requirements remain unchanged.

When a generated Dataset repository receives Ruleset-owned validation, compatibility, or migration artifacts, the realization shall preserve enough Ruleset identity or traceability to determine the governing source of those artifacts when that distinction matters.

The installed repo-spec source relationship shall remain distinguishable from ADR provenance, App Builder provenance, runtime Ruleset identity, Dataset state, Ruleset-to-Dataset binding, and later repository history.

## Validation

App Builder Validation shall mechanically verify realization obligations that are mechanically decidable.

At minimum, Validation shall be capable of establishing that:

- repo-spec lifecycle selection applies to the intended Ruleset-bearing repository role without being conflated with packaging or provider selection;
- the installed framework corresponds to the exact resolved accepted repo-spec source selected for construction;
- framework-owned, product-owned, runtime Ruleset, runtime Dataset, `init-config/`, and provenance roles remain distinguishable;
- the generated repo-spec-aware Ruleset-bearing repository provides the canonical repo-spec Validation composition required by the installed framework;
- the generated Ruleset-bearing repository has no ordinary post-construction dependency on App Builder or the supplying repo-spec checkout;
- baseline Git-backed output remains available when repo-spec-aware lifecycle is not selected;
- split-Git repo-spec lifecycle material does not leak into the Dataset peer repository;
- Ruleset-owned Dataset validation or migration artifacts, when selected for Dataset installation, remain traceable to their applicable Ruleset source and do not introduce Dataset-owned semantic authority;
- equivalent resolved build inputs preserve required deterministic generated-tree correspondence.

Validation shall evaluate generated candidate repositories rather than treating successful file generation as sufficient evidence.

Mechanical Validation may establish concrete independence properties such as required local entry points, absence of construction-checkout dependencies, and successful generated-repository validation. It does not claim to prove every semantic aspect of future independent operability.

Mechanical Validation does not establish that future repository-specific Product Design, Planning, Build, Dataset content, or application semantics are correct.

## Upgrade Boundary

This Design establishes source identity and structural readiness for later repo-spec framework upgrade work.

It also establishes the architectural boundary under which Ruleset evolution may require application-owned compatibility evaluation or migration of Dataset data.

It does not define a universal App Builder-driven upgrade engine for already generated repositories, universal Dataset schema migration semantics, universal Ruleset/Dataset compatibility rules, or universal reconciliation behavior.

Application-specific compatibility and migration semantics belong to the Ruleset product and may later be designed, planned, implemented, validated, reviewed, and accepted through its installed repo-spec lifecycle.

A generated Dataset may consume those accepted mechanisms without itself becoming a repo-spec-developed product.

## Compatibility

Existing App Builder builds that do not select repo-spec-aware lifecycle behavior remain valid.

FS-001, FS-002, and FS-003 realization semantics remain applicable.

Repo-spec awareness extends Git-backed Ruleset/application-rule development without redefining file-backed packaging, provider semantics, runtime Ruleset meaning, Dataset committed-state authority, active working-state behavior, or ordinary save semantics.

This Design refines the earlier FS-004 concept that split-Git repositories could symmetrically receive the same repository-development lifecycle. Ruleset and Dataset repositories instead retain distinct lifecycle roles consistent with their ADR ownership: Ruleset owns rules; Dataset owns data.

## Design Boundary

This Design defines:

- the ADR ownership rule that Ruleset owns rules and Dataset owns committed application-instance data;
- optional repo-spec-aware development lifecycle for Ruleset-bearing generated Git repositories;
- Ruleset product development as including application rules governing Dataset structure, validation, compatibility, and migration;
- preservation of runtime Ruleset paths as accepted operational realization without requiring relocation beneath `product/`;
- Dataset repositories as application-state repositories rather than symmetric repo-spec product-development repositories;
- Ruleset-defined validation, compatibility, or migration mechanisms as remaining Ruleset-owned when installed or executed against Dataset data;
- governed Dataset compatibility transition as a valid consequence of Ruleset evolution without transfer of Dataset authority;
- separation of repository-development material from runtime application material;
- post-construction independence from App Builder and the supplying repo-spec checkout;
- exact accepted repo-spec source identity;
- provenance and deterministic-construction expectations for installed framework and Ruleset-owned Dataset-governance artifacts.

This Design does not define:

- a new ADR semantic component;
- a universal Dataset schema;
- application-specific artifact schemas or lifecycle states;
- universal provenance graphs for application artifacts;
- universal stale-state or dependency algorithms;
- application-specific migration behavior;
- universal Ruleset/Dataset compatibility identifiers or versioning;
- a universal App Builder upgrade engine for generated repositories;
- automatic repo-spec upgrades after construction;
- runtime application save or commit services;
- provider-specific repo-spec semantics;
- mandatory repo-spec installation for all ADR applications;
- repo-spec Design/Planning lifecycle installation for Dataset-only repositories;
- a requirement that Ruleset-owned Dataset validation or migration tooling use one universal physical layout or execution model.
