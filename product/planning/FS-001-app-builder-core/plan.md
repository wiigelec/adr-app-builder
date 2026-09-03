# FS-001 — ADR App Builder Core Plan

## Objective

Build the smallest executable realization tool that turns semantically separate ADR application sources into traceable deterministic self-contained provider realizations.

## Source Contract

A build consumes application definition, Ruleset, Dataset, and build definition JSON documents. Application-owned initialization lives in the application definition. The build definition selects one packaging profile and one or more provider profiles.

## Upstream Contract

Before generation, the builder resolves `wiigelec/adr` `main` to an exact commit. Output records that ADR commit and the exact App Builder implementation commit used.

## Packaging and Providers

FS-001 provides `self-contained-json`, `generic-self-contained`, and `microsoft-copilot`. Packaging defines physical assembly and complete-realization preservation; providers adapt bootstrap/presentation only.

## Reference Fixture

The task-tracker selects both providers and exercises identity, application-owned initialization, Ruleset authority, Dataset instance state, provider bootstrap, provenance, and preservation/writeback guidance.

## Validation

Validation checks ADR seed-spec consumption, source/profile structure, dual provenance, both provider outputs, exact Ruleset/Dataset preservation, separated initialization, preservation contract presence, source immutability, and repeat-build determinism. A checked-in byte-exact expected artifact is not required because ADR `main` is a moving build input.
