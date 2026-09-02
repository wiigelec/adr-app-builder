# FS-001 — ADR App Builder Core

functional_set: FS-001
design_revision: 6fc55280cb45624af50367481f1d429698424fc6

## Purpose

FS-001 establishes source separation, build-time ADR `main` resolution, dual provenance, self-contained packaging, provider adaptation, complete-realization preservation, deterministic generation, and reference-fixture validation.

## Functional Boundary

FS-001 includes application, Ruleset, Dataset, and build-definition inputs; application-owned initialization semantics; one explicit self-contained JSON packaging profile; generic and Microsoft Copilot provider profiles; one-or-more-provider generation; dual ADR/App Builder provenance; complete-realization writeback guidance; and deterministic validation.

## Exclusions

FS-001 does not establish a universal ADR file format, migration or upgrade automation, provider APIs, automated upload, live model conformance testing, plugin architecture, or application-specific workflow semantics beyond the fixture.

## Upstream ADR Model

A new build resolves `wiigelec/adr` `main` at build time and records the exact resolved ADR commit. App Builder Design is not permanently pinned to one ADR candidate revision.
