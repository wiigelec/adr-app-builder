# Repository Agent Guidance

This file provides operational guidance and does not independently define normative meaning.

## Lifecycle ownership

A missing consequential semantic decision → **Design**.

A Functional Set, Plan, normative requirement, scope, or evaluation-classification defect → **Planning**.

An implementation or mechanical-enforcement-construction defect → **Build**.

Validation does not create Design meaning or normative requirements.


## Default product operation

Product mode is the default operating mode.

Interpret requests to create, inspect, modify, rebuild, or operate an application realization or its canonical source material as ADR App Builder product use unless the user explicitly requests maintenance of the ADR App Builder implementation repository.

ADR App Builder repository maintenance requires explicit user intent. Creating, modifying, validating, committing, or otherwise operating a generated application's repository is product operation and is not App Builder repository maintenance merely because Git is involved.

When authoring from user intent, preserve the canonical ownership boundary: application identity and application-owned initialization belong to the application definition; behavior and rules belong to the Ruleset; initial or persisted application-instance values belong to the Dataset; packaging, runtime representation, provider selection, and other realization choices belong to the build definition.

Ask the user when unresolved consequential semantic ambiguity would materially change application meaning, authority, persisted state, identity, compatibility, migration meaning, or destructive effect. Resolve routine serialization and mechanically equivalent implementation choices without burdening the user.

The Agent interprets user intent, but the deterministic builder consumes canonical sources rather than conversation directly. Conversation history is not a hidden fifth build input.

## Repository ownership

`repo/` is the reusable repository-development framework.

`product/` is the generic product-owned domain. Do not assume Product meaning before Product Design establishes it.

`scripts/` is the narrow repository-wide operational composition role.

`user/` is user-owned operational material outside the framework.

Closed architectural boundaries are default-deny. Do not add new direct children or files where the accepted architecture does not allow them.


## App Builder product boundaries

ADR App Builder is realization tooling, not ADR normative authority.

Preserve semantic separation between application definition, Ruleset source, Dataset source, packaging, and provider adaptation even when generated artifacts physically combine them.

Do not silently rewrite application-owned Ruleset or Dataset meaning in a provider adapter.

Treat single-file output, JSON encoding, bootstrap wording, provider metadata, and provider-set layout as App Builder realization choices rather than ADR core requirements.

Generated realizations are derived outputs. For mutable application artifacts, later Dataset state carried by an operated artifact may be newer than builder input; do not mistake that state evolution for a change to builder or ADR semantics.

Preserve application-owned initialization separately from provider bootstrap adaptation. For mutable self-contained realizations, preserve non-Dataset realization material and require complete-realization writeback after governed Dataset mutation.

Generated applications record exact ADR and App Builder provenance commits. Treat those commits as lineage and upgrade anchors, not runtime authorities.

## Build discipline

Consume reviewed Design and Planning. Prefer the simplest implementation that preserves their meaning and satisfies applicable normative requirements.

Do not infer normative intent from implementation behavior.

## Validation

Use `scripts/validate` as the repository-wide mechanical Validation entry point. `repo/scripts/validate` remains authoritative for framework mechanical checks.

Mechanical Validation passing does not establish semantic acceptance.

## Semantic Review and Acceptance

Semantic Review evaluates the realized candidate against the complete applicable Design and Planning result.

`main` represents accepted state. Acceptance occurs only through intentional integration of a satisfactory candidate into `main`.
