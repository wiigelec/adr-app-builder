# FS-001 — ADR App Builder Core Plan

## Objective

Build the smallest executable realization tool that can turn semantically separate ADR application sources into deterministic single-file provider realizations.

## Source Contract

A build consumes four JSON documents: application definition, Ruleset, Dataset, and build definition.

The build definition selects a packaging profile and one or more provider profiles.

## Output Contract

For each selected provider, Build shall emit one deterministic JSON realization carrying builder realization metadata, application definition, provider initialization material, Ruleset, and Dataset.

The envelope is an App Builder format, not an ADR universal format.

## Profiles

FS-001 shall include `generic-self-contained` and `microsoft-copilot`.

Provider profiles may supply initialization instructions but shall not mutate Ruleset or Dataset content.

## Reference Fixture

The task-tracker fixture shall exercise application identity, embedded Ruleset authority, Dataset instance state, bootstrap initialization, read-only interaction guidance, and state-transition rules.

Validation shall compare generated Copilot output byte-for-byte with a checked-in expected artifact and prove repeat-build determinism and source immutability.

## Upstream Boundary

This plan is aligned to the published ADR FS-003 candidate commit `ef8d8bcdcf152364dd719038d82e90bb4c321b49`. App Builder does not make that candidate's concrete realization-neutral semantics into a provider-specific ADR requirement.
