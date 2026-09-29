# FS-005 — Agent-Operated Product Interface Plan

design_revision: 0a38733e284319b54a818c384841d43db95caba3

## Objective

Implement DP-103 by establishing a provider-independent agent-operating contract around the accepted canonical App Builder source model and deterministic builder.

The Build shall make natural-language product operation practical for an AI Agent without moving natural-language interpretation into `app_builder.py`.

FS-001 through FS-004 remain applicable.

## Planned Functional Scope

FS-005 work is bounded to:

- defining a machine-readable, repository-owned agent-authoring contract;
- aligning root `AGENTS.md` with product-mode default behavior and the explicit repository-maintenance boundary;
- documenting the human-facing natural-language product interaction in `README.md`;
- preserving the four canonical source roles as the only deterministic builder inputs;
- defining one creation/modification authoring flow;
- making consequential-ambiguity escalation explicit;
- preserving provider independence of the authoring layer;
- adding mechanical Validation for the contract and guidance alignment; and
- binding mechanically decidable FS-005 requirements to real Validation tasks.

## Consequential Technical Decisions

### Agent-authoring contract

Build shall add:

```text
product/src/agent-authoring-contract.json
```

as the canonical machine-readable operating contract for an Agent using ADR App Builder.

The contract shall be product-owned, provider-independent, deterministic repository content.

It shall contain at least:

- `schema_version`;
- `default_mode`;
- canonical source-role declarations for application, Ruleset, Dataset, and build definition;
- a declaration that natural-language interpretation is Agent-owned and builder execution is canonical-source-owned;
- a declaration that repository maintenance requires explicit user intent;
- a declaration that generated-application repository operations are distinct from App Builder repository maintenance;
- a creation/modification authoring-model declaration;
- a consequential-ambiguity policy; and
- the deterministic builder invocation boundary.

The exact JSON member names are Build-level details provided their meaning remains mechanically decidable and stable enough for Validation.

The contract is operational metadata. It does not become application definition, Ruleset, Dataset, build definition, provider metadata, or a new ADR semantic authority.

### Root agent guidance

`AGENTS.md` shall be updated so an Agent entering the repository can operate the product correctly without first inferring mode from repository-development context.

It shall state, in substance:

- ADR App Builder product mode is the default;
- application creation/modification requests are product operations;
- repository maintenance occurs only when explicitly requested;
- generated Git-backed application work is not App Builder repository maintenance;
- user intent is routed to application definition, Ruleset, Dataset, or build definition according to ownership;
- consequential semantic ambiguity is escalated to the user;
- non-semantic serialization/mechanical choices should not burden the user; and
- the deterministic builder consumes canonical sources rather than conversation directly.

`AGENTS.md` remains operational guidance and shall continue to state that it does not independently define normative meaning.

### Human-facing README

Root `README.md` shall describe the default interaction model as:

```text
human intent -> AI Agent -> canonical sources -> deterministic App Builder -> generated realization
```

It shall explain that JSON and CLI remain canonical/internal or lower-level interfaces, but ordinary product use does not require the human to author those artifacts directly.

The README shall distinguish product use from maintaining the App Builder implementation repository.

### Canonical-source authoring

FS-005 shall reuse the existing canonical input documents and existing builder CLI.

No natural-language request text, conversation transcript, Agent chain-of-thought, provider-specific hidden state, or other conversational material shall be added as an implicit builder input.

The authoring Agent may create or modify canonical JSON files, but the builder shall continue to receive the same semantically distinct source roles already accepted by DP-100 and subsequent Functional Sets.

### Create/modify flow

Build shall define creation and modification in the agent-authoring contract as the same authoring pipeline with different starting state:

- **create** starts from no existing application source set and produces a complete canonical source set;
- **modify** starts from existing authoritative source material, applies only requested changes to affected ownership surfaces, preserves unaffected canonical material, then invokes the same builder boundary as creation where rebuilding is required.

No separate semantic model shall be introduced for modification.

### Ambiguity policy

The contract shall distinguish consequential ambiguity from mechanical choice.

Consequential ambiguity includes unresolved choices that materially affect:

- application behavior;
- semantic authority;
- Dataset persisted state;
- application or instance identity;
- compatibility or migration meaning;
- destructive outcomes; or
- another user-visible semantic result.

Mechanical choices include formatting, temporary naming, deterministic ordering, and equivalent serialization already governed by accepted product rules.

The contract shall direct the Agent to ask the user only for unresolved consequential ambiguity.

### Product-mode / maintenance boundary

The contract and `AGENTS.md` shall define an explicit boolean-equivalent rule:

```text
repository maintenance requires explicit user intent
```

Absent that explicit intent, ambiguous requests shall remain in product mode.

This rule applies to the ADR App Builder implementation repository only.

Creating, modifying, validating, committing, or otherwise operating a generated application's own repository according to that application's realization is not classified as App Builder repository maintenance solely because Git is involved.

### Provider independence

The agent-authoring contract shall not vary by selected provider profile.

Provider selection remains a build-definition concern.

A provider profile may affect generated realization adaptation, but it shall not change the authoring ownership model, product-mode default, ambiguity rule, or repository-maintenance boundary.

### Existing CLI compatibility

The existing CLI remains supported.

FS-005 does not remove or hide direct canonical-source invocation.

The Agent may invoke the CLI after authoring canonical inputs; humans may invoke it directly when desired.

No new natural-language CLI mode is required.

## Stable Normative Requirement IDs

The canonical FS-005 normative specification shall use these IDs and classifications.

| ID | Title | Class |
| --- | --- | --- |
| FS-005-NR-001 | Functional Set Scope | S |
| FS-005-NR-002 | Agent Default Interface | S |
| FS-005-NR-003 | Default Product Mode | M |
| FS-005-NR-004 | Explicit Repository-Maintenance Intent | M |
| FS-005-NR-005 | Generated-Repository Operation Distinction | B |
| FS-005-NR-006 | Canonical Four-Source Boundary | M |
| FS-005-NR-007 | Agent-to-Source Ownership Routing | S |
| FS-005-NR-008 | No Hidden Conversational Build Input | M |
| FS-005-NR-009 | Deterministic Builder Separation | M |
| FS-005-NR-010 | Shared Create/Modify Authoring Model | M |
| FS-005-NR-011 | Bounded Modification Preservation | S |
| FS-005-NR-012 | Consequential Ambiguity Escalation | S |
| FS-005-NR-013 | No Consequential Semantic Invention | S |
| FS-005-NR-014 | Non-Semantic Choice Autonomy | S |
| FS-005-NR-015 | Provider-Independent Authoring Contract | M |
| FS-005-NR-016 | Human-Facing Non-JSON Requirement | B |
| FS-005-NR-017 | Root Agent Guidance Alignment | M |
| FS-005-NR-018 | Direct CLI Compatibility | M |
| FS-005-NR-019 | Prior Functional Set Compatibility | B |

Classification follows the accepted convention:

- **S** — semantic requirement whose correctness ultimately requires Semantic Review;
- **B** — boundary/compatibility requirement;
- **M** — mechanically decidable requirement expected to bind to product Validation.

## Planned Requirement Meaning

### FS-005-NR-001 — Functional Set Scope

FS-005 realizes the agent-operated authoring interface and does not redefine ADR semantics or replace accepted builder/packaging/runtime semantics.

### FS-005-NR-002 — Agent Default Interface

The default human-facing product interaction is mediated by an AI Agent that translates user intent into canonical App Builder inputs.

### FS-005-NR-003 — Default Product Mode

The repository-owned agent contract declares product operation as the default mode.

### FS-005-NR-004 — Explicit Repository-Maintenance Intent

The repository-owned agent contract requires explicit user intent before ADR App Builder repository-maintenance operations are authorized.

### FS-005-NR-005 — Generated-Repository Operation Distinction

Operations on generated application repositories are not App Builder repository maintenance merely because they use Git.

### FS-005-NR-006 — Canonical Four-Source Boundary

The agent-authoring contract identifies application definition, Ruleset, Dataset, and build definition as the canonical builder source roles.

### FS-005-NR-007 — Agent-to-Source Ownership Routing

User intent is routed according to the accepted ownership boundaries of the four canonical source roles.

### FS-005-NR-008 — No Hidden Conversational Build Input

Conversation text, transcript history, model reasoning, or provider-owned hidden state is not an implicit deterministic builder input.

### FS-005-NR-009 — Deterministic Builder Separation

Natural-language interpretation remains Agent-owned; the deterministic builder continues to execute from canonical sources.

### FS-005-NR-010 — Shared Create/Modify Authoring Model

Creation and modification use one canonical authoring model and the same deterministic builder boundary where construction is required.

### FS-005-NR-011 — Bounded Modification Preservation

A modification request changes only the canonical ownership surfaces implicated by the requested change and preserves unrelated authoritative material.

### FS-005-NR-012 — Consequential Ambiguity Escalation

The Agent seeks user input when unresolved ambiguity would materially alter a consequential semantic or destructive outcome.

### FS-005-NR-013 — No Consequential Semantic Invention

The Agent does not silently invent missing consequential application semantics merely to complete a build.

### FS-005-NR-014 — Non-Semantic Choice Autonomy

Mechanically equivalent serialization and implementation details governed by accepted product rules need not be escalated to the user.

### FS-005-NR-015 — Provider-Independent Authoring Contract

Provider selection does not change the agent-authoring ownership model, product-mode default, ambiguity policy, or maintenance boundary.

### FS-005-NR-016 — Human-Facing Non-JSON Requirement

Ordinary product use does not require the human to author canonical JSON or operate the CLI directly.

### FS-005-NR-017 — Root Agent Guidance Alignment

Root `AGENTS.md` operational guidance represents the FS-005 product-mode, maintenance-boundary, ownership-routing, ambiguity, and builder-separation rules without claiming independent normative authority.

### FS-005-NR-018 — Direct CLI Compatibility

The existing canonical-source CLI remains available and behaviorally compatible with the accepted prior Functional Sets.

### FS-005-NR-019 — Prior Functional Set Compatibility

FS-001 through FS-004 remain applicable except for the new human-facing authoring/operation layer explicitly defined by FS-005.

## Planned Validation Task Decomposition

Build should add real functional Validation predicates for mechanically classified requirements.

Likely responsibilities include:

- agent-authoring contract schema and required semantics;
- product-mode and repository-maintenance boundary;
- canonical source-role mapping;
- builder/conversation separation;
- shared create/modify declaration;
- provider independence;
- root guidance alignment; and
- CLI surface compatibility.

Semantic-only requirements shall not receive vacuous mechanical bindings.

`product/validation/requirement-evaluation.json` shall be updated only when corresponding Validation tasks exist.

## Build Sequence

1. Add `product/src/agent-authoring-contract.json`.
2. Update root `AGENTS.md` to implement the default product-mode operating boundary.
3. Update root `README.md` with the natural-language Agent interaction model.
4. Add FS-005 product Validation tasks for the machine-readable contract and guidance alignment.
5. Verify the existing builder remains canonical-source-only and direct CLI behavior is unchanged.
6. Add the canonical FS-005 normative specification using the reserved IDs above.
7. Bind mechanically classified requirements to real Validation tasks.
8. Run full canonical Validation.
9. Perform Semantic Review against DP-103 and accepted prior Functional Sets.
10. Integrate only after Acceptance.

## Exclusions

This plan does not authorize:

- natural-language interpretation inside `app_builder.py`;
- a new model-provider dependency;
- a fifth canonical build input;
- storage of conversation transcripts as builder authority;
- automatic invention of missing consequential application semantics;
- provider-specific authoring semantics;
- a graphical UI;
- a universal concurrent-edit merge engine;
- changes to generated-application runtime semantics not otherwise required by accepted prior Functional Sets; or
- App Builder repository maintenance without explicit user intent.
