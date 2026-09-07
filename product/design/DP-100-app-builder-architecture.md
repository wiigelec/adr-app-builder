---
doc_id: DP-100
title: ADR App Builder Architecture
depends_on: []
---

# ADR App Builder Architecture

## Purpose

ADR App Builder is realization tooling for constructing deployable ADR-derived application artifacts and provider sets from application-owned source material. It is not the ADR framework itself and does not create or replace ADR normative meaning.

## Post-Construction Independence

App Builder is construction tooling. Its responsibility for a generated application realization ends when construction of that realization is complete.

The generated application is self-contained for ordinary operation and has no runtime dependency on App Builder. Application initialization, active working-state management, Dataset persistence, runtime Git commits, and subsequent Ruleset or Dataset evolution are responsibilities of the generated application and its operating Agent/environment according to the generated Ruleset, Dataset, packaging, and repository guidance.

App Builder may later be invoked as a separate build or rebuild operation, including from preserved invocation inputs where available. Such a later invocation is not participation in the ordinary runtime operation of an already generated application.

## Upstream ADR Boundary

App Builder tracks the current `main` branch of `wiigelec/adr` when building a new application realization. Each build resolves ADR `main` to one exact commit, consumes and validates the accepted ADR seed-spec artifacts present under `product/src` at that exact commit, and records the resolved ADR commit in the generated realization.

A generated realization also records the exact current App Builder repository commit used for the build. These commits are provenance and future-upgrade anchors, not runtime authorities. The consumed ADR seed specs are build inputs and need not be copied into the generated realization.

## Canonical Application Source Model

App Builder consumes semantically distinct application definition, Ruleset, Dataset, and build-definition inputs. The application definition includes application identity and any application-owned initialization semantics. The build definition selects packaging and provider profiles and owns App Builder realization choices that determine generated physical form without redefining Ruleset or Dataset semantics.

Ruleset and Dataset remain distinct semantic components regardless of physical packaging. Packaging shall not collapse their semantic boundary. Each component shall remain independently identifiable and addressable so that governed working-state evolution, Dataset persistence, Ruleset replacement, Dataset migration, and later upgrade operations can act on the intended component without implicitly redefining the other.

## Initialization

Application-owned initialization semantics and provider bootstrap adaptation are distinct. Application-owned initialization remains represented once under the application definition; provider bootstrap remains separate realization metadata. Provider adaptation may add environment-specific guidance but shall not replace, weaken, duplicate, or reinterpret application-owned initialization, Ruleset, Dataset, instance, authority, transition meaning, working-state meaning, or persistence meaning.

Initialization establishes active application working state from persisted Dataset state unless application-owned semantics define another governed initialization or recovery behavior.

Initialization shall not implicitly persist a Dataset write. Explicit initialization-associated state transitions remain application-owned and Ruleset-governed.

## Runtime Application State

An active application session may maintain current application state in Agent/session working memory.

That active working state is analogous to application state held in RAM.

Governed interactions may change active working state without immediately modifying the persisted Dataset.

While the application session remains active, the current governed working state may be authoritative for subsequent application interactions, even when it is newer than the persisted Dataset.

Conversation history, Agent working memory, or another active-session memory surface may carry authoritative working state when the application realization and Ruleset establish that state. Their authority is limited to the active application context and does not make arbitrary conversational content application state.

Application working state shall remain distinguishable from unrelated conversational context, inferred transient reasoning, and provider-owned state.

## Persisted Dataset State

The Dataset represents persisted application state analogous to saved state on disk.

Persisted Dataset state is the durable restore point from which a later application session can initialize or reopen.

A governed change to active working state does not by itself require a Dataset write.

Persisting working state to the Dataset is a distinct application operation.

A user-requested or user-accepted save operation may write current governed working state to the Dataset according to Ruleset and application semantics.

Closing or losing an active session before persistence may discard newer volatile working-state changes. Persisted Dataset state remains available for subsequent initialization or reopen.

The Dataset is therefore authoritative for persisted state, while current governed working state may be authoritative for the active session.

## Realization Configuration

Physical realization choices belong to the build definition rather than Ruleset or Dataset semantic meaning.

The build definition may select whether a runtime Ruleset or Dataset is realized as a single file or a structured tree and may carry the deterministic mapping information required for that physical representation.

Ruleset and Dataset inputs remain the semantic sources for their runtime components. App Builder realization configuration shall not create, remove, or reinterpret application behavior or state.

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

“Single” denotes one storage authority, not semantic fusion. A single-file or single-Git package shall preserve enough structural separation that Ruleset and Dataset can be located, compared, replaced, migrated, persisted, and upgraded independently.

## Packaging Preservation and Persistence

Working-state mutation is governed by the Ruleset and does not by itself imply physical package writeback.

A persistence operation writes accepted application state to the Dataset while preserving non-mutated Ruleset material.

A packaging profile defines the minimum physical writeback required to persist Dataset state.

For a single-file package, a Dataset save may require rewriting the containing file, but the Ruleset component shall remain independently identifiable and unchanged unless a separate governed operation authorizes its modification.

For split-files packaging, a Dataset save updates the Dataset file without requiring Ruleset-file rewrite.

For single-Git packaging, a Dataset save updates Dataset paths or components in the shared repository while preserving Ruleset paths or components, then records the resulting repository state according to the packaging profile's Git persistence behavior.

For split-Git packaging, a Dataset save updates the Dataset repository without requiring a Ruleset-repository change.

A deliberate upgrade or migration may change Ruleset, Dataset, or both, but packaging shall preserve the distinction among active working-state mutation, Dataset persistence, Ruleset change, migration, and upgrade.

## Upgradeability

Packaging shall not prevent independent lifecycle evolution of Ruleset and Dataset. Ruleset identity and revision, Dataset identity and persisted state or schema revision, active working state, and storage-level provenance may evolve at different rates.

Git commit identity is storage provenance and shall not replace application-semantic identity. A shared Git repository may provide one repository commit for a complete persisted package state while still preserving independently addressable Ruleset and Dataset components. Split Git repositories may carry independent Ruleset and Dataset revisions.

This Design establishes upgradeability constraints on packaging but does not define a migration engine, upgrade engine, or universal versioning scheme.

## Provider Profiles

A provider profile adapts initialization and presentation for a target Agent environment. Provider profiles do not define Ruleset/Dataset packaging and shall not change the selected packaging topology.

A provider profile may expose or carry active application working state during a session, but it shall not redefine whether that working state or the persisted Dataset is authoritative for a given application operation.

## Provider Sets

A build may select one or more provider profiles. One realization is generated per selected provider from the same application sources, selected packaging profile, resolved ADR commit, and App Builder implementation.

## Provenance

Each generated realization records the exact resolved ADR commit and the exact current App Builder repository commit. The build also consumes the accepted ADR seed-spec artifacts from that resolved ADR revision. This supports later upgrade analysis without requiring either repository at runtime.

Packaging may add storage-level provenance for Ruleset and Dataset material. Such provenance remains lineage information and does not become independent ADR, App Builder, Ruleset, Dataset, or active-session authority.

## Deterministic Build

Identical sources, profiles, resolved ADR commit and seed-spec contents, and App Builder repository commit shall produce deterministic generated package content. ADR `main` is intentionally moving, so a later build after ADR advances has a different build input.

For Git-backed packaging, deterministic build requirements apply to the generated repository tree and package-owned file content, not to the Git commit SHA or commit timestamp.

Each newly generated Git repository shall contain one initial commit whose author and committer timestamps represent the actual repository-construction time. The initial commit shall contain the complete generated repository tree so ordinary Git hosting surfaces attribute the generated files to the repository's actual creation time.

Git author/committer identity, branch name, and initial commit message remain App Builder-controlled. Because construction time participates in Git commit identity, equivalent builds performed at different times are not required to produce the same initial commit SHA.

No additional creation/bootstrap commit or repository-creation marker file is required.

Subsequent governed working-state changes are runtime activity, and subsequent persisted Dataset commits represent saved state evolution rather than repeated-build output.

## Validation

Validation checks required source identity, profile existence and shape, source preservation, dual provenance, initialization separation, Ruleset/Dataset separation, working-state versus persisted-state separation, packaging preservation contracts, provider-set generation, and repeat-build determinism for the same resolved inputs.

Packaging-specific validation shall verify that Ruleset and Dataset remain independently addressable, that working-state mutation need not cause Dataset writeback, and that a Dataset save does not implicitly alter Ruleset material.

## Reference Application

The initial reference fixture is a tiny task tracker used to exercise realization assembly and preservation behavior, not to define App Builder business semantics.

## Design Boundary

This Design does not define a universal ADR application format, automatic save policy, concurrent-session save/conflict/merge semantics, migration engine, upgrade engine, provider API, plugin system, semantic-diff framework, universal Ruleset versioning scheme, or universal Dataset migration scheme.
