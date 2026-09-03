---
doc_id: DP-100
title: ADR App Builder Architecture
depends_on: []
---

# ADR App Builder Architecture

## Purpose

ADR App Builder is realization tooling for constructing deployable ADR-derived application artifacts and provider sets from application-owned source material. It is not the ADR framework itself and does not create or replace ADR normative meaning.

## Upstream ADR Boundary

App Builder tracks the current `main` branch of `wiigelec/adr` when building a new application realization. Each build resolves ADR `main` to one exact commit, consumes and validates the accepted ADR seed-spec artifacts present under `product/src` at that exact commit, and records the resolved ADR commit in the generated realization.

A generated realization also records the exact current App Builder repository commit used for the build. These commits are provenance and future-upgrade anchors, not runtime authorities. The consumed ADR seed specs are build inputs and need not be copied into the generated realization.

## Canonical Application Source Model

App Builder consumes semantically distinct application definition, Ruleset, Dataset, and build-definition inputs. The application definition includes application identity and any application-owned initialization semantics. The build definition selects packaging and provider profiles.

Ruleset and Dataset remain distinct semantic components regardless of physical packaging. Packaging shall not collapse their semantic boundary. Each component shall remain independently identifiable and addressable so that governed Dataset mutation, Ruleset replacement, Dataset migration, and later upgrade operations can act on the intended component without implicitly redefining the other.

## Initialization

Application-owned initialization semantics and provider bootstrap adaptation are distinct. Application-owned initialization remains represented once under the application definition; provider bootstrap remains separate realization metadata. Provider adaptation may add environment-specific guidance but shall not replace, weaken, duplicate, or reinterpret application-owned initialization, Ruleset, Dataset, instance, authority, or transition meaning.

Initialization shall not implicitly mutate Dataset state. Explicit initialization-associated transitions remain application-owned and Ruleset-governed.

## Packaging Model

A packaging profile defines the persistence relationship, physical arrangement, addressing, preservation, and writeback behavior of the Ruleset and Dataset. Packaging does not define application-owned Ruleset or Dataset meaning and does not make one component authoritative over the other.

Packaging varies along two independent characteristics:

- **Storage authority** — file or Git repository.
- **Component topology** — co-located under one storage authority or separated across independent storage authorities.

The resulting packaging classes are:

- **single-file** — Ruleset and Dataset are independently addressable components within one physical file.
- **split-files** — Ruleset and Dataset are carried as separate files and no additional packaging file is required by this topology.
- **single-git** — Ruleset and Dataset occupy distinct paths or components within one Git repository and share one repository history.
- **split-git** — Ruleset and Dataset are governed by separate Git repositories with independent histories.

“Single” denotes one storage authority, not semantic fusion. A single-file or single-Git package shall preserve enough structural separation that Ruleset and Dataset can be located, compared, replaced, migrated, and upgraded independently.

## Packaging Preservation and Mutation

Dataset mutation is governed by the Ruleset and shall not implicitly modify Ruleset material. A packaging profile defines the minimum physical writeback required to persist an accepted Dataset mutation while preserving non-mutated Ruleset material.

For a single-file package, an accepted Dataset mutation may require rewriting the containing file, but the Ruleset component shall remain independently identifiable and unchanged unless a separate governed operation authorizes its modification.

For split-files packaging, an accepted Dataset mutation updates the Dataset file without requiring Ruleset-file rewrite.

For single-Git packaging, an accepted Dataset mutation updates Dataset paths or components in the shared repository while preserving Ruleset paths or components, then records the resulting repository state according to the packaging profile's Git persistence behavior.

For split-Git packaging, an accepted Dataset mutation updates the Dataset repository without requiring a Ruleset-repository change.

A deliberate upgrade or migration may change Ruleset, Dataset, or both, but packaging shall preserve the distinction between those operations and ordinary Dataset mutation.

## Upgradeability

Packaging shall not prevent independent lifecycle evolution of Ruleset and Dataset. Ruleset identity and revision, Dataset identity and state or schema revision, and storage-level provenance may evolve at different rates.

Git commit identity is storage provenance and shall not replace application-semantic identity. A shared Git repository may provide one repository commit for a complete package state while still preserving independently addressable Ruleset and Dataset components. Split Git repositories may carry independent Ruleset and Dataset revisions.

This Design establishes upgradeability constraints on packaging but does not define a migration engine, upgrade engine, or universal versioning scheme.

## Provider Profiles

A provider profile adapts initialization and presentation for a target Agent environment. Provider profiles do not define Ruleset/Dataset packaging and shall not change the selected packaging topology.

## Provider Sets

A build may select one or more provider profiles. One realization is generated per selected provider from the same application sources, selected packaging profile, resolved ADR commit, and App Builder implementation.

## Provenance

Each generated realization records the exact resolved ADR commit and the exact current App Builder repository commit. The build also consumes the accepted ADR seed-spec artifacts from that resolved ADR revision. This supports later upgrade analysis without requiring either repository at runtime.

Packaging may add storage-level provenance for Ruleset and Dataset material. Such provenance remains lineage information and does not become independent ADR, App Builder, Ruleset, or Dataset authority.

## Deterministic Build

Identical sources, profiles, resolved ADR commit and seed-spec contents, and App Builder repository commit shall produce deterministic output. ADR `main` is intentionally moving, so a later build after ADR advances has a different build input.

For Git-backed packaging, deterministic realization concerns the generated package content and declared initial repository state from the same resolved inputs; subsequent governed runtime commits represent state evolution rather than repeated-build output.

## Validation

Validation checks required source identity, profile existence and shape, source preservation, dual provenance, initialization separation, Ruleset/Dataset separation, packaging preservation contracts, provider-set generation, and repeat-build determinism for the same resolved inputs.

Packaging-specific validation shall verify that Ruleset and Dataset remain independently addressable and that Dataset-only mutation does not implicitly alter Ruleset material.

## Reference Application

The initial reference fixture is a tiny task tracker used to exercise realization assembly and preservation behavior, not to define App Builder business semantics.

## Design Boundary

This Design does not define a universal ADR application format, migration engine, upgrade engine, provider API, plugin system, semantic-diff framework, universal Ruleset versioning scheme, or universal Dataset migration scheme.
