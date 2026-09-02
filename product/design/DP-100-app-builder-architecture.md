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

## Initialization

Application-owned initialization semantics and provider bootstrap adaptation are distinct. Provider adaptation may add environment-specific guidance but shall not replace, weaken, or reinterpret application-owned initialization, Ruleset, Dataset, instance, authority, or transition meaning.

Initialization shall not implicitly mutate Dataset state. Explicit initialization-associated transitions remain application-owned and Ruleset-governed.

## Packaging Profiles

A packaging profile defines physical assembly and preservation behavior. FS-001 provides `self-contained-json`, which co-locates provenance, application material, initialization material, Ruleset, and Dataset while preserving their semantic roles.

For mutable self-contained realizations, governed Dataset state may change while non-Dataset realization material is preserved. Writeback returns the complete realization rather than a Dataset-only fragment.

## Provider Profiles

A provider profile adapts initialization and presentation for a target Agent environment. FS-001 provides `generic-self-contained` and `microsoft-copilot`. Provider profiles do not define packaging.

## Provider Sets

A build may select one or more provider profiles. One realization is generated per selected provider from the same sources, packaging profile, resolved ADR commit, and App Builder implementation.

## Provenance

Each generated realization records the exact resolved ADR commit and the exact current App Builder repository commit. The build also consumes the accepted ADR seed-spec artifacts from that resolved ADR revision. This supports later upgrade analysis without requiring either repository at runtime.

## Deterministic Build

Identical sources, profiles, resolved ADR commit and seed-spec contents, and App Builder repository commit shall produce deterministic output. ADR `main` is intentionally moving, so a later build after ADR advances has a different build input.

## Validation

Validation checks required source identity, profile existence and shape, source preservation, dual provenance, initialization separation, complete-realization preservation, multi-provider generation, and repeat-build determinism for the same resolved inputs.

## Reference Application

The initial reference fixture is a tiny task tracker used to exercise realization assembly and preservation behavior, not to define App Builder business semantics.

## Design Boundary

FS-001 does not define a universal ADR application format, migration engine, upgrade engine, provider API, plugin system, or semantic-diff framework.
