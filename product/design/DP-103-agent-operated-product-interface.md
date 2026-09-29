---
doc_id: DP-103
title: Agent-Operated Product Interface
depends_on:
  - DP-100
---

# Agent-Operated Product Interface

## Purpose

ADR App Builder is operated through an AI Agent as its default human-facing product interface.

A user expresses application intent in natural language. The operating Agent interprets that intent, authors or updates the canonical App Builder source model, and invokes the deterministic App Builder realization process.

The user is not required to author JSON, understand the App Builder CLI, select internal filenames, or perform repository-development operations in order to use the product.

This Design extends DP-100. It does not replace the canonical application source model, deterministic construction, Ruleset/Dataset separation, packaging profiles, provider profiles, provenance, or post-construction independence.

## Interaction Model

The default product interaction is:

```text
human intent
    │
    ▼
AI Agent
    │
    ├── interpret application meaning
    ├── author/update canonical sources
    └── select realization configuration
            │
            ▼
canonical App Builder source model
├── application definition
├── Ruleset
├── Dataset
└── build definition
            │
            ▼
deterministic App Builder
            │
            ▼
generated realization
```

The Agent is the human-facing authoring interface.

The canonical source model remains the deterministic builder interface.

Natural-language conversation is therefore an authoring surface, not a replacement for canonical build inputs.

## Canonical Source Boundary

Application definition, Ruleset, Dataset, and build definition remain the semantically distinct canonical inputs established by DP-100.

The Agent may construct, update, serialize, validate, and supply those inputs on the user's behalf.

The deterministic App Builder shall not become responsible for interpreting unconstrained natural-language application intent.

Once the Agent has authored a canonical source set for a build, that source set is the reproducible build input. Conversation history is not an additional hidden build input.

The Agent shall not rely on unstated conversational memory to change the meaning of an otherwise identical canonical source set.

## Agent Authoring Responsibility

The Agent is responsible for translating user intent into the correct App Builder ownership surface.

Examples include:

- application identity and application-owned initialization meaning → application definition;
- application behavior, invariants, transitions, validation, compatibility, or other rule meaning → Ruleset;
- initial or persisted application-instance values → Dataset;
- packaging topology, runtime representation, provider selection, and other realization choices → build definition.

The Agent shall preserve the semantic boundary among these inputs even when a user's natural-language request does not use App Builder terminology.

The Agent shall not place a realization choice into Ruleset or Dataset meaning merely because doing so is convenient.

The Agent shall not place application semantics into provider adaptation or packaging configuration.

## Create and Modify

Application creation and application modification use the same authoring model.

For creation, the Agent derives a canonical source set from user intent and builds a realization.

For modification, the Agent evaluates the existing canonical application sources or other authoritative application material, applies the requested semantic or realization change to the appropriate ownership surface, and rebuilds or updates the realization as applicable.

A modification request does not authorize unrelated semantic changes.

The Agent should describe consequential changes in user-facing application terms rather than requiring the user to inspect raw serialization.

## Ambiguity Handling

The Agent shall resolve non-semantic implementation and serialization details without requiring unnecessary user decisions.

The Agent shall ask for user input when an unresolved ambiguity would materially change application meaning, authority, behavior, persisted state, compatibility, or another consequential product outcome.

Examples of consequential ambiguity include:

- two materially different interpretations of an application rule;
- uncertainty about whether supplied information is intended as behavior or persisted state;
- a choice that would change application-instance identity or initialization meaning;
- a destructive or incompatible modification whose intended outcome is not established.

Examples that ordinarily do not require user clarification include:

- JSON formatting;
- internal temporary filenames;
- deterministic ordering;
- mechanically equivalent serialization choices;
- other implementation details already governed by accepted App Builder Design and Planning.

The Agent may present a proposed interpretation when that is more useful than exposing internal schema terminology.

## Product Mode

Product mode is the default operating mode.

In product mode, requests are interpreted as requests to use ADR App Builder to create, inspect, modify, rebuild, or otherwise operate on application realizations and their canonical source material.

The existence of the App Builder implementation repository does not make repository-development work the default interpretation of a user request.

A request to build or modify an application is not authorization to modify the App Builder product repository.

## Repository-Maintenance Boundary

Modification or maintenance of the ADR App Builder implementation repository occurs only when the user explicitly requests repository or product-development work on ADR App Builder itself.

Repository-maintenance operations include changes to App Builder Design, Planning, specifications, implementation, validation, repository framework integration, or other source-controlled App Builder development material.

Generating a Git-backed application realization is not App Builder repository maintenance merely because the generated product uses Git repositories.

Operating on a generated application's repository according to that application's accepted realization and Ruleset is likewise distinct from modifying the ADR App Builder implementation repository.

When the user's request is ambiguous between product use and App Builder repository maintenance, the Agent shall prefer product mode unless repository-maintenance intent is explicit.

## Agent Authority Boundary

The Agent is an authoring and operating interface, not a new ADR semantic authority.

The Agent may interpret user intent and propose canonical application material, but accepted application semantics remain represented in the application definition, Ruleset, Dataset, and other authoritative application artifacts according to their established ownership.

The Agent shall not silently invent consequential application semantics merely to complete a build.

The Agent shall not treat provider behavior, model tendencies, conversational style, or transient reasoning as application authority.

Where user intent is sufficiently established, the Agent may perform the mechanical work needed to encode that intent without separately asking the user to approve each serialization step.

## Realization Configuration

The Agent may select or recommend App Builder realization configuration from user intent and available product defaults.

A user may express realization intent in ordinary language, for example:

- keep Ruleset and Dataset in separate Git repositories;
- produce a self-contained realization;
- support Microsoft Copilot;
- keep the Dataset as a structured tree.

The Agent translates that intent into the build definition and applicable profiles.

Realization configuration remains distinct from application semantics.

## User-Facing Presentation

The Agent should present application behavior, state, changes, build choices, warnings, and results in human-meaningful terms.

Raw canonical JSON, CLI commands, internal paths, or profile identifiers may be shown when requested or when materially useful for diagnosis, review, or interoperability, but they are not the required primary user interface.

The Agent shall not require the user to manipulate canonical serialization merely because the builder consumes canonical serialization.

## Determinism and Reproducibility

Agent-operated authoring does not weaken DP-100 deterministic-build requirements.

Once a canonical source set and resolved external build inputs are established, deterministic construction is evaluated from those canonical inputs.

Two conversations that produce byte-equivalent canonical inputs and equivalent resolved build inputs shall not produce different generated package content merely because their conversational wording differed.

If different user intent produces different canonical inputs, differing realizations are expected and do not violate deterministic construction.

## Provider Boundary

The authoring Agent interface is distinct from generated-application provider profiles.

Provider profiles adapt the generated realization for a target Agent environment.

The authoring Agent translates human intent into App Builder canonical sources and realization configuration.

A provider profile shall not become the mechanism by which App Builder interprets application-authoring intent.

## Validation

Mechanical Validation may verify properties of the agent-operated authoring realization that are mechanically decidable, including:

- canonical source separation;
- deterministic translation of mechanically equivalent authoring operations where Planning requires it;
- preservation of existing canonical material during bounded modification;
- correct routing of build configuration versus application semantic material;
- absence of hidden builder dependence on conversational context; and
- product-mode safeguards against unintended App Builder repository mutation where mechanically enforceable.

Validation does not establish that an Agent correctly understood every possible natural-language request.

Semantic Review remains responsible for evaluating whether the realized authoring behavior preserves this Design.

## Design Boundary

This Design defines:

- the AI Agent as the default human-facing ADR App Builder interface;
- natural-language interaction as an authoring surface over the canonical App Builder source model;
- continued use of application definition, Ruleset, Dataset, and build definition as deterministic builder inputs;
- Agent responsibility for routing user intent to the correct ownership surface;
- consequential-ambiguity handling;
- one authoring model for creation and modification;
- product mode as the default operating mode;
- explicit opt-in for ADR App Builder repository maintenance;
- separation between App Builder repository maintenance and generated Git-backed application operation;
- human-facing presentation that does not require direct JSON or CLI manipulation; and
- preservation of deterministic construction after canonicalization.

This Design does not define:

- a universal natural-language grammar;
- one mandatory Agent implementation or model provider;
- a universal conversational memory mechanism;
- a new ADR semantic authority;
- replacement of canonical App Builder inputs with conversation history;
- automatic invention of missing consequential application semantics;
- a universal application-edit merge or conflict-resolution algorithm;
- a universal graphical user interface;
- provider-specific application semantics;
- runtime behavior of generated applications beyond the applicable accepted application realization; or
- repository-development authority without explicit user intent.
