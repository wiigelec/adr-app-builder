# FS-005 — Agent-Operated Product Interface

### FS-005-NR-001 — Functional Set Scope

**Classification: S**

FS-005 shall establish the agent-operated authoring and product-use interface defined by DP-103 without redefining upstream ADR semantics or replacing accepted FS-001 through FS-004 construction, packaging, provider, Git, repo-spec, provenance, runtime, or post-construction semantics.

### FS-005-NR-002 — Agent Default Interface

**Classification: S**

The default human-facing ADR App Builder interaction shall be mediated by an AI Agent that interprets user intent, authors or updates canonical App Builder source material, and invokes the deterministic builder boundary.

### FS-005-NR-003 — Default Product Mode

**Classification: M**

The repository-owned agent-authoring contract shall declare `product` as the default operating mode and shall define product use to include creation, inspection, modification, rebuilding, and operation of application realizations and their canonical source material.

### FS-005-NR-004 — Explicit Repository-Maintenance Intent

**Classification: M**

The repository-owned agent-authoring contract shall require explicit user intent before ADR App Builder implementation-repository maintenance is authorized. In the absence of explicit repository-maintenance intent, ambiguous requests shall remain in product mode.

### FS-005-NR-005 — Generated-Repository Operation Distinction

**Classification: B**

Creating, modifying, validating, committing, or otherwise operating a generated application's own Git repository according to that application's realization shall not be classified as ADR App Builder implementation-repository maintenance solely because Git or repository operations are involved.

### FS-005-NR-006 — Canonical Four-Source Boundary

**Classification: M**

The agent-authoring contract shall identify exactly the accepted semantic source roles supplied to the deterministic App Builder boundary: application definition, Ruleset, Dataset, and build definition. The contract shall not define conversation history or another authoring surface as an additional canonical builder input.

### FS-005-NR-007 — Agent-to-Source Ownership Routing

**Classification: S**

The operating Agent shall route user intent according to accepted ownership boundaries: application identity and application-owned initialization to the application definition; behavior, invariants, transitions, validation, compatibility, migration, and other rule meaning to the Ruleset; initial or persisted application-instance values to the Dataset; and packaging, runtime representation, provider selection, and other realization choices to the build definition.

### FS-005-NR-008 — No Hidden Conversational Build Input

**Classification: M**

The repository-owned authoring contract shall state that natural-language request text, conversation transcript history, Agent chain-of-thought, provider-owned hidden state, model-internal state, or other conversational material is not an implicit deterministic App Builder input. Once canonical sources are established, the builder shall operate from those sources and accepted resolved external inputs.

### FS-005-NR-009 — Deterministic Builder Separation

**Classification: M**

The agent-authoring contract shall keep natural-language interpretation Agent-owned and deterministic construction canonical-source-owned. FS-005 shall not add unconstrained natural-language interpretation to `product/src/app_builder.py` or make model output an implicit builder input.

### FS-005-NR-010 — Shared Create/Modify Authoring Model

**Classification: M**

The agent-authoring contract shall define creation and modification as one canonical authoring model with different starting state. Creation shall produce a complete canonical source set from user intent. Modification shall begin from existing authoritative material, apply requested changes to the implicated ownership surfaces, preserve unaffected canonical material, and use the same deterministic builder boundary when rebuilding is required.

### FS-005-NR-011 — Bounded Modification Preservation

**Classification: S**

An application-modification request shall not authorize unrelated semantic or realization changes. The operating Agent shall preserve authoritative material outside the ownership surfaces implicated by the requested change unless the user separately authorizes broader modification.

### FS-005-NR-012 — Consequential Ambiguity Escalation

**Classification: S**

The operating Agent shall seek user input when unresolved ambiguity would materially change application meaning, semantic authority, persisted Dataset state, application or instance identity, compatibility or migration meaning, destructive effect, or another consequential user-visible product outcome.

### FS-005-NR-013 — No Consequential Semantic Invention

**Classification: S**

The operating Agent shall not silently invent missing consequential application semantics merely to complete a canonical source set or build.

### FS-005-NR-014 — Non-Semantic Choice Autonomy

**Classification: S**

The operating Agent may resolve non-consequential formatting, temporary naming, deterministic ordering, mechanically equivalent serialization, and other implementation details already governed by accepted App Builder Design and Planning without requiring user decisions.

### FS-005-NR-015 — Provider-Independent Authoring Contract

**Classification: M**

The repository-owned agent-authoring contract shall be provider-independent. Changing only provider selection shall not alter the canonical source ownership model, default product mode, repository-maintenance boundary, ambiguity policy, or creation/modification authoring model.

### FS-005-NR-016 — Human-Facing Non-JSON Requirement

**Classification: B**

Ordinary product use shall not require the human user to author canonical JSON, select internal filenames, or operate the App Builder CLI directly. Raw canonical serialization and CLI details may remain available when requested or when useful for diagnostics, automation, interoperability, or explicit lower-level operation.

### FS-005-NR-017 — Root Agent Guidance Alignment

**Classification: M**

Root `AGENTS.md` shall operationally align with the FS-005 agent-authoring contract by stating the default product mode, explicit repository-maintenance opt-in, canonical ownership routing, consequential-ambiguity policy, generated-repository distinction, and deterministic builder separation while continuing to state that `AGENTS.md` does not independently define normative meaning.

### FS-005-NR-018 — Direct CLI Compatibility

**Classification: M**

The existing canonical-source App Builder CLI shall remain available and behaviorally compatible with accepted FS-001 through FS-004 semantics. FS-005 shall not require a natural-language CLI mode or remove direct canonical-source invocation.

### FS-005-NR-019 — Prior Functional Set Compatibility

**Classification: B**

FS-001 through FS-004 remain applicable except for the new human-facing authoring and product-operation layer explicitly defined by FS-005. Existing application definition, Ruleset, Dataset, build-definition, packaging, provider, provenance, Git, repo-spec, runtime, and post-construction semantics remain unchanged unless this specification explicitly states otherwise.

### FS-005-NR-020 — Agent Operation Protocol Completeness

**Classification: M**

The repository-owned agent-authoring contract shall contain enough machine-readable operational information for a capable Agent to author builder-valid canonical inputs, discover supported realization choices, invoke the builder through its complete public CLI boundary, locate generated results, and acquire authoritative material for modification without inferring the operating protocol from `app_builder.py`.

### FS-005-NR-021 — Canonical Source Contract Discovery

**Classification: M**

The Agent Operation Protocol shall expose the builder-enforced required shape of application definition, Ruleset, Dataset, and build definition, including the optional Git runtime representation grammar. For `tree` representation it shall define the non-empty output-path-to-RFC-6901-selector mapping, valid relative output-path constraints, selector uniqueness and non-overlap, complete source coverage, and semantic reconstruction requirement. It shall identify usable product-owned reference examples for each source role.

### FS-005-NR-022 — Supported Choice Discovery

**Classification: M**

The Agent Operation Protocol shall expose the supported packaging profiles, provider profiles, and Git runtime representations, or shall identify authoritative product-owned discovery surfaces that provide those choices without requiring inference from builder implementation code.

### FS-005-NR-023 — Complete Builder Invocation Protocol

**Classification: M**

The Agent Operation Protocol shall identify the builder command, all required CLI arguments, supported optional external-source arguments and defaults, the profile conditions under which optional external inputs are consumed, and operation-affecting preconditions including the clean App Builder worktree and absent-or-empty output directory requirements.

### FS-005-NR-024 — Result and Success Discovery

**Classification: M**

The Agent Operation Protocol shall define successful builder completion mechanically and shall identify generated-result locations for the accepted legacy self-contained realization and packaged realization families.

### FS-005-NR-025 — Modification Source Authority Protocol

**Classification: B**

For modification, the Agent Operation Protocol shall prefer an existing canonical source set when available; for generated Git realizations it shall distinguish current runtime application, Ruleset, and Dataset authority from construction-time `init-config/` lineage, use the build-definition runtime file mappings when structured runtime material must be reconstructed, and require user escalation rather than semantic invention when a complete authoritative source set cannot be established.

### FS-005-NR-026 — Protocol-to-Builder Alignment

**Classification: M**

Mechanical Validation shall verify that the Agent Operation Protocol agrees with the accepted builder CLI, builder-enforced canonical source and Git runtime mapping preconditions, supported product profile surfaces, operation-affecting preconditions, and referenced product-owned examples.
