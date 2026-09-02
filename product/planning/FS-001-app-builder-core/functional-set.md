# FS-001 — ADR App Builder Core

functional_set: FS-001
design_revision: 3f0540213f1a8816854b9d264285bcb66932fb8c
upstream_adr_fs003_commit: ef8d8bcdcf152364dd719038d82e90bb4c321b49

## Purpose

FS-001 establishes the first executable ADR App Builder slice: canonical source separation, self-contained packaging, provider profiles, provider-set generation, deterministic build behavior, and reference-fixture validation.

## Functional Boundary

FS-001 includes separate application, Ruleset, Dataset, and build-definition source inputs; self-contained JSON packaging; one or more provider profiles; deterministic generation; a generic provider profile; a Microsoft Copilot profile; and a task-tracker reference fixture.

## Exclusions

FS-001 does not establish a universal ADR file format, managed shared-Ruleset packaging, provider APIs, automated upload, live model conformance testing, arbitrary schema migration, or application-specific workflow semantics beyond the fixture.

## Planning Result

FS-001 is realized through this Functional Set, `plan.md`, the canonical normative specification, the reference builder, built-in profiles, and deterministic fixture validation.
