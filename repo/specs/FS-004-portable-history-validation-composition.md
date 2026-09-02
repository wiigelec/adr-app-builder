# FS-004 — Portable History and Validation Composition Normative Requirements

### FS-004-NR-001 — Root operational scripts role

**Classification: B**

The maintained repository-root boundary shall authorize `scripts/` only as a repository-wide operational composition role, and FS-004 shall authorize `scripts/validate` as its only maintained entry.

### FS-004-NR-002 — Repository-wide Validation entry point

**Classification: M**

The repository shall provide executable `scripts/validate` as the repository-wide mechanical Validation entry point.

### FS-004-NR-003 — Framework Validation ownership

**Classification: B**

Repository-wide Validation shall delegate framework mechanical Validation to `repo/scripts/validate` without moving or duplicating framework normative predicates into the root composition layer.

### FS-004-NR-004 — Product Validation composition

**Classification: B**

When `product/scripts/validate` exists, repository-wide Validation shall require it to be executable, execute it after successful framework Validation, and fail when product Validation fails; absence of that product entry point shall not itself fail repository-wide Validation.

### FS-004-NR-005 — CI delegation

**Classification: B**

Active CI mechanical gating shall delegate to `./scripts/validate` and shall not independently select framework or product Validation implementations.

### FS-004-NR-006 — Portable Design revision representation

**Classification: B**

Each Functional Set shall retain exactly one well-formed 40-character lowercase `design_revision` identifier, and generic framework Validation shall not require that identifier's originating Git commit object to exist in the current repository merely to validate the retained Planning artifact.

### FS-004-NR-007 — Existing exact Design binding preservation

**Classification: B**

Where an existing normative requirement fixes a Functional Set to one exact Design revision value, framework Validation shall continue to enforce that exact value even though generic local-object resolution is not required.

### FS-004-NR-008 — Independent-history framework operation

**Classification: B**

Canonical framework mechanical Validation shall remain operable when a well-formed retained framework Planning `design_revision` refers to an originating commit object absent from the current repository.

### FS-004-NR-009 — Active documentation alignment

**Classification: B**

`README.md` and `AGENTS.md` shall describe repository-root Validation composition, domain Validation ownership, and the portable meaning of retained Design revision identifiers.

### FS-004-NR-012 — Minimal installed framework snapshot

**Classification: B**

When `repo/validation/framework-source.json` exists, `repo/planning/` may be absent. Canonical framework Validation shall not fail merely because framework-development Planning history is absent, shall skip Planning-history checks that require that directory, and shall continue mechanically evaluating the installed normative requirement state from `repo/specs/` and `repo/validation/requirement-evaluation.json`.

### FS-004-NR-010 — Composition does not own normative meaning

**Classification: S**

Repository-root operational composition shall not become a source of framework or product Design meaning, normative requirements, or domain implementation semantics.

### FS-004-NR-011 — No supplier-history machinery

**Classification: S**

FS-004 shall not require imported supplier ancestry, Git grafts, replace refs, bundles, hidden remotes, provenance databases, lineage systems, or generalized plugin machinery merely to preserve framework portability.
