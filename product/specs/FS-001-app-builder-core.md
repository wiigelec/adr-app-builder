# FS-001 — ADR App Builder Core

### FS-001-NR-001 — Source Separation

**Classification: S**

The builder shall accept application definition, Ruleset source, Dataset source, and build definition as semantically distinct inputs.

### FS-001-NR-002 — ADR Semantic Preservation

**Classification: S**

The builder shall preserve applicable ADR Agent, Dataset, Ruleset, instance, authority, initialization, and transition meaning represented by its application sources.

### FS-001-NR-003 — Packaging Profile Selection

**Classification: S**

A build definition shall select a packaging profile that controls physical realization without redefining application-owned Ruleset or Dataset meaning.

### FS-001-NR-004 — Provider Profile Selection

**Classification: S**

A build definition may select one or more provider profiles that adapt initialization or presentation for target Agent environments.

### FS-001-NR-005 — Provider Set Generation

**Classification: S**

When multiple provider profiles are selected, the builder shall generate one realization per selected provider from the same application, Ruleset, Dataset, and packaging source.

### FS-001-NR-006 — Self-Contained Packaging

**Classification: S**

The initial self-contained packaging profile shall physically co-locate application definition, provider initialization material, Ruleset, and Dataset in one JSON realization while preserving semantic distinction.

### FS-001-NR-007 — Initialization Material

**Classification: S**

A generated provider realization shall carry sufficient profile-defined initialization material to guide fresh-session binding without requiring initialization itself to mutate Dataset state.

### FS-001-NR-008 — Ruleset Fidelity

**Classification: M**

Provider adaptation shall preserve the source Ruleset content exactly within the generated realization.

### FS-001-NR-009 — Dataset Fidelity

**Classification: M**

Provider adaptation shall preserve the source Dataset content exactly within the generated realization.

### FS-001-NR-010 — Provider Metadata Non-Authority

**Classification: S**

Provider-specific initialization and presentation metadata shall not be treated as authoritative committed Dataset state merely by being included in a generated realization.

### FS-001-NR-011 — Generated Artifact Non-Authority

**Classification: S**

Generated realizations shall not be treated as independent ADR or App Builder normative authority.

### FS-001-NR-012 — Deterministic Generation

**Classification: M**

Identical source documents, profile documents, and builder implementation shall produce byte-identical generated output.

### FS-001-NR-013 — Generic Provider Profile

**Classification: B**

Build shall provide a generic self-contained provider profile suitable for provider-neutral reference generation.

### FS-001-NR-014 — Microsoft Copilot Profile

**Classification: B**

Build shall provide a Microsoft Copilot provider profile that supplies explicit fresh-session initialization guidance without changing Ruleset or Dataset source semantics.

### FS-001-NR-015 — Task Tracker Fixture

**Classification: B**

Build shall provide a task-tracker reference source set that exercises application identity, Ruleset governance, Dataset state, initialization, read-only interaction guidance, and state transitions.

### FS-001-NR-016 — Exact Fixture Correspondence

**Classification: M**

Mechanical validation shall generate the task-tracker Microsoft Copilot realization and compare it byte-for-byte with the checked-in expected realization.

### FS-001-NR-017 — Source Immutability During Build

**Classification: M**

Mechanical validation shall verify that building a realization does not mutate the source Ruleset or Dataset documents.

### FS-001-NR-018 — Repeat-Build Determinism

**Classification: M**

Mechanical validation shall run equivalent repeated builds and verify byte-identical output.
