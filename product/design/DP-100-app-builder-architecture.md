---
doc_id: DP-100
title: ADR App Builder Architecture
depends_on: []
---

# ADR App Builder Architecture

## Purpose

ADR App Builder is realization tooling for constructing deployable ADR-derived application artifacts and provider sets from application-owned source material.

It is not the ADR framework itself and does not create or replace ADR normative meaning.

## Upstream Semantic Boundary

App Builder consumes ADR semantics as an upstream contract.

The initial Product Design is aligned to the published ADR FS-003 candidate at commit `ef8d8bcdcf152364dd719038d82e90bb4c321b49`, which defines application realization and initialization while keeping provider, encoding, packaging, and builder choices outside ADR core.

App Builder must preserve applicable ADR Agent, Dataset, Ruleset, application-instance, binding, initialization, authority, and transition semantics.

## Canonical Application Source Model

App Builder treats an application build source as semantically distinct inputs:

- **application definition** — application identity and application-owned realization metadata;
- **Ruleset source** — governed application semantics;
- **Dataset source** — an application instance's authoritative or initial committed state;
- **build definition** — selected packaging and provider targets.

These inputs may be stored separately for maintainability even when a generated target co-locates them physically.

The builder source model is not itself an ADR-mandated schema. It is this product's authoring model.

## Packaging Profiles

A packaging profile defines how application source material is physically assembled.

The initial product supports a **self-contained single-file** packaging profile in which application identity, initialization material, Ruleset, and Dataset are emitted in one artifact.

Future profiles may emit shared-Ruleset plus independent-Dataset packages, multi-file bundles, repository-backed realizations, or other arrangements.

Packaging must not collapse Ruleset and Dataset semantic distinction merely because material is physically co-located.

## Provider Profiles

A provider profile adapts a packaged realization for a target Agent environment.

A provider profile may define bootstrap wording, interaction hints, provider metadata, ordering, or other environment-facing material.

Provider adaptation must not silently change application-owned Ruleset or Dataset semantics.

Provider-specific material is realization metadata, not committed Dataset authority.

## Provider Sets

One build definition may select multiple provider profiles.

The resulting **provider set** is a group of generated realizations derived from the same application, Ruleset, Dataset source, and packaging intent.

Provider-set members may differ in provider-facing bootstrap or presentation while preserving the application semantics required by their supported operations.

## Initialization

Generated realizations shall provide sufficient initialization material for their target profile to bind a fresh Agent operation to the application identity, selected application instance, applicable Ruleset authority where consequential, and relevant Dataset state.

Initialization material must not itself mutate Dataset state.

## Generated Artifact Authority

Generated artifacts are deployable realizations.

They are not independent ADR normative authority and are not independent App Builder design authority.

For mutable self-contained applications, a generated artifact may subsequently carry newer authoritative Dataset state than the original builder source. That runtime state evolution does not retroactively redefine the source Ruleset or builder semantics.

## Deterministic Build

For identical source material, profile definitions, and builder version, a build should be deterministic.

## Validation

App Builder validation shall distinguish source-shape validity, profile existence, Ruleset/Dataset preservation, initialization metadata, and deterministic reference-fixture correspondence.

Semantic equivalence across arbitrary language models cannot be established by mechanical validation alone.

## Initial Reference Application

The initial reference fixture is a tiny task tracker derived from the one-file ADR proof-of-concept.

Its purpose is to prove deterministic assembly. The task tracker is a fixture, not App Builder product semantics.

## Design Boundary

App Builder does not define ADR core semantics, a universal ADR application file format, a universal provider command language, or application-specific business workflows.

Its product meaning is controlled construction of realizations from semantically distinct application source material.
