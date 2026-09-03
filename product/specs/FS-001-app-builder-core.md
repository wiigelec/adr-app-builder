# FS-001 — ADR App Builder Core

### FS-001-NR-001 — Source Separation

**Classification: S**

The builder shall accept application definition, Ruleset source, Dataset source, and build definition as semantically distinct inputs.

### FS-001-NR-002 — ADR Main Resolution

**Classification: S**

A new build shall resolve the configured ADR framework `main` branch to one exact commit before generation and shall consume and validate the accepted `product/src/*.seed.json` artifacts present at that exact revision.

### FS-001-NR-003 — Dual Provenance

**Classification: M**

Each generated realization shall record the exact ADR commit resolved for the build and the exact current App Builder repository commit used to generate it.

### FS-001-NR-004 — Application Initialization Semantics

**Classification: S**

Application-owned initialization semantics shall remain represented once under the application definition and shall remain distinguishable from provider-specific bootstrap adaptation.

### FS-001-NR-005 — Packaging Profile Selection

**Classification: S**

A build definition shall select a packaging profile that controls physical realization and preservation behavior without redefining application-owned Ruleset or Dataset meaning.

### FS-001-NR-006 — Provider Profile Selection

**Classification: S**

A build definition may select one or more provider profiles that adapt initialization or presentation without defining packaging.

### FS-001-NR-007 — Provider Set Generation

**Classification: M**

When multiple provider profiles are selected, the builder shall generate one realization per selected provider from the same sources and resolved build inputs.

### FS-001-NR-008 — Self-Contained Packaging

**Classification: B**

Build shall provide a `self-contained-json` packaging profile that co-locates realization material in one JSON artifact while preserving semantic distinction.

### FS-001-NR-009 — Complete Realization Preservation

**Classification: S**

For mutable self-contained realizations, governed Dataset mutation shall preserve non-Dataset realization material and write back the complete realization rather than a Dataset-only fragment.

### FS-001-NR-010 — Ruleset Fidelity

**Classification: M**

Generation shall preserve the source Ruleset content exactly within each generated realization.

### FS-001-NR-011 — Dataset Fidelity

**Classification: M**

Generation shall preserve the source Dataset content exactly within each generated realization.

### FS-001-NR-012 — Provider Metadata Non-Authority

**Classification: S**

Provider-specific bootstrap and presentation metadata shall not become authoritative committed Dataset state merely by inclusion in a realization.

### FS-001-NR-013 — Generated Artifact Non-Authority

**Classification: S**

Generated realizations and provenance metadata shall not be treated as independent ADR or App Builder normative authority.

### FS-001-NR-014 — Generic Provider Profile

**Classification: B**

Build shall provide a generic self-contained provider profile.

### FS-001-NR-015 — Microsoft Copilot Profile

**Classification: B**

Build shall provide a Microsoft Copilot profile with explicit fresh-session and complete-realization preservation guidance.

### FS-001-NR-016 — Structural Validation

**Classification: M**

Mechanical validation shall verify required application identity, application-instance identity, profile existence and shape, separated initialization material, and preservation-contract presence.

### FS-001-NR-017 — Source Immutability During Build

**Classification: M**

Mechanical validation shall verify that generation does not mutate source application, Ruleset, Dataset, or build-definition documents.

### FS-001-NR-018 — Repeat-Build Determinism

**Classification: M**

Equivalent repeated builds using the same source documents, profiles, resolved ADR commit and seed-spec contents, and App Builder repository commit shall produce byte-identical provider outputs.
