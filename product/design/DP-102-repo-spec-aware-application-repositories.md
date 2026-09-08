---
doc_id: DP-102
title: Repo-Spec-Aware Application Repositories
depends_on:
  - DP-100
  - DP-101
---

# Repo-Spec-Aware Application Repositories

## Purpose

ADR App Builder shall realize `split-git` applications as two repositories with intentionally different lifecycle roles:

- the Ruleset repository is always managed by the repo-spec repository-development lifecycle; and
- the Dataset repository remains an independently evolving application-instance data repository and is not managed by the repo-spec product-development lifecycle.

Repo-spec integration is a repository-development concern. It does not extend ADR semantics, does not add another ADR semantic component, and does not make repo-spec authority over application-owned Ruleset or Dataset meaning.

This Design extends DP-100 and DP-101. It preserves App Builder's role as construction tooling, the semantic separation among application definition, Ruleset, Dataset, packaging, and provider adaptation, and the post-construction independence of generated repositories.

## Upstream ADR Authority

FS-004 inherits ADR's accepted Agent, Dataset, Ruleset, application-instance, ownership, binding, compatibility, transition, and initialization semantics from the accepted ADR product state.

ADR defines the Dataset as the sole authority for committed application-instance state, the Ruleset as the owner of semantics governing Dataset structure, interpretation, validity, transition, compatibility, and migration, and Agent reasoning as transient unless accepted into Dataset state through governed transition semantics.

This Design does not redefine those semantics. It defines only how App Builder realizes them for `split-git` repositories while adding repo-spec repository-development lifecycle management to the Ruleset repository and preserving the Dataset repository as independently evolving application-instance state.

## Packaging and Lifecycle Eligibility

Repo-spec product-development lifecycle management is defined only for the Ruleset repository produced by `split-git`.

Under this Design:

- `single-file` does not use repo-spec lifecycle management;
- `split-files` does not use repo-spec lifecycle management;
- `single-git` does not use repo-spec lifecycle management;
- `split-git` always installs repo-spec lifecycle management in the Ruleset repository; and
- the `split-git` Dataset repository does not receive repo-spec Design, Planning, Build, Semantic Review, or Acceptance lifecycle management.

There is no independent repo-spec lifecycle selector for `split-git`.

Selecting `split-git` selects the lifecycle contract defined here.

Provider profiles shall not enable, disable, reinterpret, or modify this lifecycle behavior.

## Split-Git Ruleset Repository

The Ruleset repository produced by `split-git` is the application-rule product repository.

It shall carry the reusable repo-spec framework and shall support development of the Ruleset product through:

Design → Planning → Build → Validation → Semantic Review → Acceptance.

The accepted runtime Ruleset realization may remain at the runtime location established by App Builder's runtime-representation choices. Repo-spec lifecycle ownership does not require runtime Ruleset files to be relocated beneath `product/`.

The repo-spec `product/` domain owns development artifacts and implementation work for the Ruleset/application-rule product. Runtime Ruleset material remains the accepted operational realization governed by that lifecycle.

Ruleset product development may include application rules governing Dataset structure, validation, compatibility, and migration.

## Split-Git Ruleset/Dataset Binding

The separately managed Ruleset and Dataset repositories produced by `split-git` shall preserve enough identity or traceability to determine the applicable Ruleset authority for Dataset operations whenever that distinction is consequential.

The binding must remain determinate as the Ruleset and Dataset repositories evolve independently.

The concrete binding representation is a Planning and Build concern. It may be realized through repository-local metadata, references, identifiers, or another mechanically sufficient mechanism, but FS-004 does not prescribe one universal encoding, version field, Git reference, artifact format, or lookup protocol.

Binding information is not an independent semantic authority and does not transfer committed-state authority away from the Dataset.

The Ruleset/Dataset binding shall remain distinguishable from:

- ADR provenance;
- App Builder construction provenance;
- repo-spec framework source provenance;
- ordinary repository history; and
- Dataset committed-state values.

A consequential change in applicable Ruleset authority shall not silently reinterpret incompatible committed Dataset state. Compatibility, migration, acceptance, refusal, recovery, and related behavior follow the derived application's Ruleset-owned semantics inherited from ADR.

The generated split-git realization shall preserve enough application identity, selected application-instance identity, applicable Ruleset authority, relevant authoritative Dataset state, and required binding information for a fresh reasoning operation to initialize under determinate application semantics without relying on prior conversational memory, the App Builder checkout, or the supplying repo-spec checkout.

## Split-Git Dataset Repository

The Dataset repository produced by `split-git` is an independently evolving application-instance data repository.

It is not a repo-spec product-development repository.

Its ordinary lifecycle is application operation over committed data rather than Design → Planning → Build development of application rules.

The Dataset repository may contain or consume Ruleset-defined mechanical validation, compatibility, or migration mechanisms needed to operate safely on its data. Such mechanisms remain Ruleset-owned application rules or implementations of those rules even when installed into, invoked from, or physically stored within the Dataset repository.

Installing a Ruleset-defined validator or migration mechanism into the Dataset repository does not create independent Dataset-side semantic authority and does not install a repo-spec product-development lifecycle.

Dataset persistence remains governed by the applicable Ruleset semantics. An application may require validation before persistence or may require compatibility, migration, refusal, recovery, or author-governed resolution when the applicable Ruleset changes.

Repo-spec lifecycle material from the Ruleset repository shall not leak into the Dataset repository merely because both repositories were produced by the same `split-git` build.

## Single-Git Boundary

A `single-git` repository may continue to contain both runtime Ruleset and runtime Dataset material while preserving their semantic ownership boundaries.

`single-git` is not eligible for repo-spec lifecycle management under this Design.

This restriction avoids conflating Ruleset product-development history with independently evolving Dataset runtime history inside one Git repository.

The absence of repo-spec lifecycle management does not weaken ADR semantic separation between Ruleset and Dataset in `single-git`.

## Repo-Spec Source

Every `split-git` build shall consume one exact accepted repo-spec framework revision for installation into the Ruleset repository.

The supplying repo-spec state shall be identified truthfully and exactly enough to determine the framework revision used for construction.

App Builder shall not silently substitute an unrelated repo-spec revision while representing the generated Ruleset repository as having been constructed from the selected source.

The exact source-selection, resolution, and mechanically sufficient accepted-state determination mechanism is a Planning and Build concern. Design does not require a particular remote, local checkout, archive format, or transport when equivalent source identity can be established correctly.

## Installed Framework Meaning

The `split-git` Ruleset repository installs the reusable repository-development framework, not the repo-spec initializer product's own product semantics.

Framework-owned repository state shall remain distinguishable from repository-specific Ruleset/application-rule development state, accepted runtime Ruleset realization, App Builder construction provenance, and `init-config/` construction inputs.

The generated Ruleset repository shall preserve repo-spec's ownership distinction between reusable framework material and repository-specific product material. Repository-specific product material concerns development of application rules and their realizations.

App Builder-generated bootstrap material shall not masquerade as accepted future Product Design merely because App Builder constructed the initial repository.

## Runtime Material and Development Material

Runtime Ruleset and Dataset components retain the semantic ownership established by ADR, DP-100, and DP-101.

Installed repo-spec framework material exists only in the `split-git` Ruleset repository and is development-lifecycle material.

Generated repository guidance shall distinguish:

- runtime Ruleset material as accepted operational application-rule realization;
- runtime Dataset material as committed application-instance data;
- repo-spec framework material as Ruleset repository lifecycle infrastructure;
- repository-specific product material as development of the Ruleset/application-rule product;
- Ruleset-defined Dataset validation or migration mechanisms as rules or implementations of rules even when executed against Dataset data; and
- App Builder provenance plus `init-config/` as construction lineage rather than runtime or development semantic authority.

Ordinary Dataset state transition and persistence shall not be reclassified as Ruleset product development.

## Ruleset Evolution, Validation, and Migration Realization

FS-004 inherits ADR's Ruleset/Dataset compatibility and evolution semantics rather than redefining them.

The FS-004 realization consequence is that Ruleset-owned validation, compatibility, migration, refusal, recovery, or related mechanisms may be physically installed into or invoked from the Dataset repository when the generated realization requires them.

Physical installation or execution location does not transfer semantic authority to the Dataset repository and does not install the repo-spec product-development lifecycle there.

Such mechanisms remain Ruleset-owned rules or realizations of Ruleset-owned rules, while any accepted resulting application-instance values remain Dataset-owned committed state.

App Builder does not invent application-specific compatibility, migration, or validation meaning and does not become a runtime migration or upgrade service after construction.

## Post-Construction Independence

After successful construction, the `split-git` Ruleset repository shall be independently usable for its installed Design → Planning → Build → Validation → Semantic Review → Acceptance lifecycle without requiring the App Builder checkout or the supplying repo-spec working tree to remain available.

The paired Dataset repository shall likewise remain independently usable as application-instance persistence according to the generated realization and applicable Ruleset binding.

App Builder does not become the runtime service, save service, commit service, Planning service, Validation service, migration service, or upgrade service after construction.

A later App Builder invocation is a separate realization operation.

A later repo-spec framework upgrade is a Ruleset-repository development operation governed by the installed repository lifecycle and applicable repo-spec upgrade semantics.

Ruleset-to-Dataset compatibility or migration remains application-owned behavior even when tooling realizing that behavior was initially installed by App Builder.

## Product Readiness

The `split-git` Ruleset repository shall be structurally ready for repository-specific Product Design and later lifecycle work on the Ruleset/application-rule product.

The installed lifecycle may establish generic product-development surfaces required by repo-spec, including Design, normative specification, implementation, and product Validation ownership surfaces.

Generic lifecycle scaffolding does not create application-specific Design meaning.

App Builder shall not invent application-specific normative requirements, Dataset schemas, validation rules, compatibility semantics, migration rules, validators, or implementation merely to populate the installed lifecycle.

Application-specific engineering begins when repository-specific Design establishes that meaning and Planning derives a bounded Functional Set from it.

The paired Dataset repository does not receive those product-development surfaces.

## Application-Specific Schemas and Mechanical Enforcement

Repo-spec-managed Ruleset development provides the ownership location and lifecycle for application-specific engineering concerns that exceed ordinary unvalidated prose.

Examples include application-defined Dataset schemas, artifact relationship rules, lifecycle state definitions, provenance rules, deterministic invariants, stale-state semantics, compatibility rules, migration semantics, validation tooling, and other mechanical enforcement.

These concerns are Ruleset-side rules or realizations of Ruleset-side rules when they define or enforce what Dataset data means, may contain, or may become.

Actual application-instance records and values remain Dataset data.

Mechanically decidable application requirements may be bound to Ruleset product Validation according to the installed repo-spec lifecycle.

The same accepted validator logic may also be executed against a concrete Dataset instance as an application-state persistence or compatibility check.

Development Validation and Dataset-instance validation have different subjects even when they reuse the same implementation.

Semantic correctness remains subject to Semantic Review and Acceptance; passing mechanical Validation does not establish semantic completeness.

## Deterministic Construction

For `split-git`, the exact resolved repo-spec framework source and any Ruleset-owned Dataset-governance artifacts selected for Dataset installation are build inputs.

For equivalent resolved inputs, App Builder shall deterministically construct the same generated repository trees and package-owned file content, subject to the existing DP-100 and DP-101 treatment of Git construction timestamps and commit identity.

Repo-spec installation and Ruleset-owned Dataset-governance installation shall not introduce unexplained dependency on incidental local repository state.

Generated Git commit identity remains storage provenance rather than application-semantic or repo-spec-semantic identity.

## Provenance and Source Relationship

The generated `split-git` Ruleset repository shall retain sufficient exact source information to identify the repo-spec framework revision installed during construction.

That information is lineage and an upgrade anchor.

It does not make the supplying repo-spec repository a runtime authority, import supplier Git ancestry into the generated repository, or create a parallel Acceptance record.

Existing ADR and App Builder provenance requirements remain unchanged.

When the generated Dataset repository receives Ruleset-owned validation, compatibility, or migration artifacts, the realization shall preserve enough Ruleset identity or traceability to determine the governing source of those artifacts when that distinction matters.

The installed repo-spec source relationship shall remain distinguishable from ADR provenance, App Builder provenance, runtime Ruleset identity, Dataset state, Ruleset-to-Dataset binding, and later repository history.

## Validation

App Builder Validation shall mechanically verify realization obligations that are mechanically decidable.

At minimum, Validation shall establish that:

- `split-git` always installs the repo-spec lifecycle into the Ruleset repository;
- `split-git` does not install repo-spec product-development lifecycle material into the Dataset repository;
- `single-file`, `split-files`, and `single-git` do not install repo-spec lifecycle material;
- the Ruleset repository's installed framework corresponds to the exact resolved accepted repo-spec source selected for construction;
- framework-owned, product-owned, runtime Ruleset, runtime Dataset, `init-config/`, and provenance roles remain distinguishable;
- the generated Ruleset repository provides the canonical repo-spec Validation composition required by the installed framework;
- the generated Ruleset repository has no ordinary post-construction dependency on App Builder or the supplying repo-spec checkout;
- Ruleset-owned Dataset validation or migration artifacts installed into the Dataset repository remain traceable to their applicable Ruleset source and do not introduce Dataset-owned semantic authority;
- the generated split-git realization preserves mechanically sufficient Ruleset/Dataset binding material to determine the applicable Ruleset authority where consequential;
- that binding material remains distinguishable from ADR provenance, App Builder provenance, repo-spec source provenance, repository history, and Dataset committed-state values;
- a fresh realization can establish application identity, application-instance identity, applicable Ruleset authority, authoritative Dataset state location, and required binding information without depending on prior conversational context, the App Builder checkout, or the supplying repo-spec checkout; and
- equivalent resolved build inputs preserve required deterministic generated-tree correspondence.

Validation shall evaluate generated candidate repositories rather than treating successful file generation as sufficient evidence.

Mechanical Validation may establish concrete independence properties such as required local entry points, absence of construction-checkout dependencies, and successful generated-repository validation. It does not claim to prove every semantic aspect of future independent operability.

Mechanical Validation does not establish that future repository-specific Product Design, Planning, Build, Dataset content, or application semantics are correct.

## Upgrade Boundary

This Design establishes source identity and structural readiness for later repo-spec framework upgrade work in the `split-git` Ruleset repository.

It also establishes the architectural boundary under which Ruleset evolution may require application-owned compatibility evaluation or migration of Dataset data.

It does not define a universal App Builder-driven upgrade engine for already generated repositories, universal Dataset schema migration semantics, universal Ruleset/Dataset compatibility rules, or universal reconciliation behavior.

Application-specific compatibility and migration semantics belong to the Ruleset product and may later be designed, planned, implemented, validated, reviewed, and accepted through its installed repo-spec lifecycle.

The paired Dataset repository may consume those accepted mechanisms without itself becoming a repo-spec-developed product.

## Compatibility

`single-file`, `split-files`, and `single-git` remain valid App Builder packaging profiles and retain their existing lifecycle behavior.

FS-001, FS-002, and FS-003 realization semantics remain applicable except where FS-004 deliberately strengthens the `split-git` Ruleset repository contract.

Under FS-004, every newly generated `split-git` realization contains a repo-spec-managed Ruleset repository paired with a non-repo-spec Dataset repository.

This is a deliberate `split-git` behavior change rather than an optional lifecycle extension.

The change does not redefine provider semantics, runtime Ruleset meaning, Dataset committed-state authority, active working-state behavior, or ordinary Dataset save semantics.

## Design Boundary

This Design defines:

- the `split-git` repository realization of inherited ADR application-instance, Ruleset, Dataset, binding, and initialization semantics;
- `split-git` as the only packaging profile using repo-spec lifecycle management;
- mandatory repo-spec lifecycle management for every `split-git` Ruleset repository;
- no independent lifecycle-selection option for `split-git`;
- no repo-spec lifecycle management for `single-file`, `split-files`, or `single-git`;
- the `split-git` Dataset repository as application-state persistence rather than a repo-spec product-development repository;
- Ruleset product development as including application rules governing Dataset structure, validation, compatibility, and migration;
- preservation of runtime Ruleset paths as accepted operational realization without requiring relocation beneath `product/`;
- Ruleset-defined validation, compatibility, or migration mechanisms as remaining Ruleset-owned when installed or executed against Dataset data;
- `split-git` realization support for inherited Ruleset-governed Dataset compatibility transitions without transferring Dataset authority or repo-spec lifecycle ownership;
- post-construction independence from App Builder and the supplying repo-spec checkout;
- exact accepted repo-spec source identity;
- determinate Ruleset/Dataset binding for separately evolving `split-git` repositories; and
- provenance and deterministic-construction expectations for installed framework and Ruleset-owned Dataset-governance artifacts.

This Design does not define:

- ADR ownership, application-instance, transition, compatibility, migration, binding, or initialization semantics already owned by the accepted ADR product;
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
- repo-spec lifecycle management for `single-file`, `split-files`, or `single-git`;
- repo-spec Design/Planning lifecycle installation for Dataset repositories; or
- a universal physical layout or execution model for Ruleset-owned Dataset validation or migration tooling.
