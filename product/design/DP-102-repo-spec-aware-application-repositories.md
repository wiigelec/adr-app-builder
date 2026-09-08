---
doc_id: DP-102
title: Repo-Spec-Aware Application Repositories
depends_on:
  - DP-100
  - DP-101
---

# Repo-Spec-Aware Application Repositories

## Purpose

ADR App Builder shall support optional repo-spec-aware realization of generated Git repositories so sufficiently complex ADR-derived applications can carry an independently usable repository-development lifecycle in addition to their runtime Ruleset and Dataset realization.

Repo-spec integration is a repository-development concern. It does not extend ADR semantics, does not add another ADR semantic component, and does not make repo-spec authority over application-owned Ruleset or Dataset meaning.

This Design extends DP-100 and DP-101. It preserves App Builder's role as construction tooling, the semantic separation among application definition, Ruleset, Dataset, packaging, and provider adaptation, and the post-construction independence of generated repositories.

## Repository Lifecycle as an Independent Realization Choice

Repository lifecycle support is independent from packaging topology, runtime component representation, and provider adaptation.

A Git-backed build may select a repository lifecycle for each generated repository role where the selected packaging profile produces more than one repository.

The baseline lifecycle remains the existing App Builder-generated Git repository behavior defined by DP-101.

A repo-spec-aware lifecycle installs a reusable repo-spec framework state into the generated repository in addition to the application-owned runtime material required by the selected packaging profile.

Selecting repo-spec-aware lifecycle behavior shall not require creation of a new packaging topology merely to represent the lifecycle choice.

Provider profiles shall not enable, disable, reinterpret, or modify repository lifecycle selection.

## Opt-In Scope

Repo-spec-aware realization is optional.

Applications that do not require a repository-development lifecycle shall remain able to use the existing generated Git repository forms without repo-spec installation.

For split-Git packaging, lifecycle selection may differ by generated repository role. A Ruleset repository may be repo-spec-aware while its paired Dataset repository remains baseline, or vice versa, when the build definition explicitly selects that result.

The lifecycle selected for one generated repository shall not silently impose repository-development material on another generated repository produced by the same application build.

## Repo-Spec Source

A repo-spec-aware build shall consume one exact accepted repo-spec framework revision for each repo-spec framework state it installs.

The supplying repo-spec state shall be identified truthfully and exactly enough to determine the framework revision used for construction.

App Builder shall not silently substitute an unrelated repo-spec revision while representing the generated repository as having been constructed from the selected source.

The exact source-selection and resolution mechanism is a Planning and Build concern. Design does not require a particular remote, local checkout, archive format, or transport when equivalent source identity can be established correctly.

## Installed Framework Meaning

Repo-spec-aware realization installs the reusable repository-development framework, not the repo-spec initializer product's own product semantics.

Framework-owned repository state shall remain distinguishable from application-owned runtime state and repository-specific product state.

A repo-spec-aware generated repository shall preserve repo-spec's ownership distinction between reusable framework material and repository-specific product material.

The generated repository's product-owned domain may describe or implement application-specific development concerns only when those concerns are established by the generated repository's own Product Design and subsequent lifecycle work.

App Builder-generated bootstrap material shall not masquerade as accepted future Product Design merely because App Builder constructed the initial repository.

## Runtime Material and Development Material

Runtime Ruleset and Dataset components retain the semantic ownership established by DP-100 and DP-101.

Installed repo-spec framework material is development-lifecycle material. Its presence does not convert runtime Ruleset or Dataset files into framework-owned state.

Generated repository guidance shall make the distinction understandable to human and agent consumers:

- runtime application material is governed by ADR application semantics and the applicable Ruleset/Dataset authority;
- repo-spec framework material governs repository-development lifecycle responsibilities;
- App Builder provenance and `init-config/` describe construction lineage and inputs rather than runtime or development semantic authority.

Ordinary application operation shall not require a repo-spec development action merely because repo-spec is installed.

Ordinary repository-development work shall not reinterpret application working-state or Dataset persistence semantics.

## Post-Construction Independence

After successful construction, a repo-spec-aware repository shall be independently usable for its installed Design → Planning → Build → Validation → Semantic Review → Acceptance lifecycle without requiring the App Builder checkout or the supplying repo-spec working tree to remain available.

App Builder does not become the repository's runtime service, save service, commit service, Planning service, Validation service, migration service, or upgrade service after construction.

A later App Builder invocation is a separate realization operation.

A later repo-spec framework upgrade is a repository-development operation governed by the installed repository lifecycle and applicable repo-spec upgrade semantics, not an implicit App Builder runtime action.

## Product Readiness

A repo-spec-aware generated repository shall be structurally ready for repository-specific Product Design and later lifecycle work.

The installed lifecycle may establish generic product-development surfaces required by repo-spec, including Design, normative specification, and product Validation ownership surfaces.

Generic lifecycle scaffolding does not create application-specific Design meaning.

App Builder shall not invent application-specific normative requirements, migration rules, schemas, validators, or implementation merely to populate the installed lifecycle.

Application-specific engineering begins when repository-specific Design establishes that meaning and Planning derives a bounded Functional Set from it.

## Application-Specific Schemas and Mechanical Enforcement

Repo-spec-aware realization is intended to provide a correct ownership location and lifecycle for application-specific engineering concerns that exceed ordinary Ruleset prose.

Examples include application-defined artifact schemas, provenance relationships, lifecycle state representations, deterministic invariants, stale-state detection, migration tooling, and mechanical Validation.

These concerns remain application-specific.

App Builder may install the generic lifecycle substrate needed to develop and validate them, but shall not infer their meaning from the shape of Ruleset or Dataset data and shall not generate universal application semantics for them.

Mechanically decidable application requirements may later be bound to product Validation according to the installed repo-spec lifecycle.

Semantic correctness remains subject to Semantic Review and Acceptance; passing mechanical Validation does not establish semantic completeness.

## Deterministic Construction

Repo-spec-aware lifecycle selection and the exact resolved repo-spec framework source are build inputs.

For equivalent resolved inputs, App Builder shall deterministically construct the same generated repository tree and package-owned file content, subject to the existing DP-100 and DP-101 treatment of Git construction timestamps and commit identity.

Repo-spec installation shall not introduce unexplained dependency on incidental local repository state.

Generated Git commit identity remains storage provenance rather than application-semantic or repo-spec-semantic identity.

## Provenance and Source Relationship

A repo-spec-aware generated repository shall retain sufficient exact source information to identify the repo-spec framework revision installed during construction.

That information is lineage and an upgrade anchor.

It does not make the supplying repo-spec repository a runtime authority, import supplier Git ancestry into the generated repository, or create a parallel Acceptance record.

Existing ADR and App Builder provenance requirements remain unchanged.

The installed repo-spec source relationship shall remain distinguishable from ADR provenance, App Builder provenance, runtime Ruleset identity, Dataset state, and later repository history.

## Validation

App Builder Validation shall mechanically verify repo-spec-aware realization obligations that are mechanically decidable.

At minimum, Validation shall be capable of establishing that:

- lifecycle selection is honored independently from packaging and provider selection;
- the installed framework corresponds to the exact resolved repo-spec source selected for construction;
- framework-owned, product-owned, runtime Ruleset, runtime Dataset, `init-config/`, and provenance roles remain distinguishable;
- the generated repository provides the canonical repo-spec Validation composition required by the installed framework;
- repo-spec-aware output remains independently operable after construction;
- baseline Git-backed output remains available when repo-spec-aware lifecycle is not selected;
- split-Git role-specific lifecycle selection does not leak installed lifecycle material into an unselected peer repository;
- equivalent resolved build inputs preserve required deterministic generated-tree correspondence.

Validation shall evaluate the generated candidate repository rather than treating successful file generation as sufficient evidence.

Mechanical Validation does not establish that future repository-specific Product Design, Planning, Build, or application semantics are correct.

## Upgrade Boundary

This Design establishes source identity and structural readiness for later repo-spec framework upgrade work.

It does not define a universal App Builder-driven upgrade engine for already generated repositories.

It also does not define application-specific Ruleset upgrades, Dataset schema migrations, application artifact migrations, or reconciliation semantics.

Those operations may later be designed and implemented within the generated repository's installed lifecycle when application-specific need establishes them.

## Compatibility

Existing App Builder builds that do not select repo-spec-aware lifecycle behavior remain valid.

FS-001, FS-002, and FS-003 realization semantics remain applicable.

Repo-spec awareness extends Git-backed repository realization without redefining file-backed packaging, provider semantics, runtime Ruleset meaning, Dataset meaning, active working-state behavior, or save semantics.

## Design Boundary

This Design defines:

- optional repo-spec-aware lifecycle selection for generated Git repositories;
- lifecycle selection as orthogonal to packaging topology and provider adaptation;
- role-specific lifecycle selection for multi-repository packaging;
- exact repo-spec source identity as a construction input;
- installation of reusable repo-spec framework state without importing supplier product semantics;
- separation of repository-development material from runtime application material;
- post-construction independence from App Builder and the supplying repo-spec checkout;
- generic Product Design and Validation readiness for later application-specific engineering;
- provenance and deterministic-construction expectations for the installed framework.

This Design does not define:

- a new ADR semantic component;
- application-specific artifact schemas or lifecycle states;
- universal provenance graphs for application artifacts;
- universal stale-state or dependency algorithms;
- application-specific migration behavior;
- a universal App Builder upgrade engine for generated repositories;
- automatic repo-spec upgrades after construction;
- runtime application save or commit services;
- provider-specific repo-spec semantics;
- mandatory repo-spec installation for all ADR applications;
- a requirement that every repository in split-Git packaging use the same repository lifecycle.
