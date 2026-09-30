# FS-005 — Agent-Operated Product Interface

functional_set: FS-005
design_revision: 0a38733e284319b54a818c384841d43db95caba3

## Purpose

FS-005 realizes DP-103 by making an AI Agent the default human-facing interface for ADR App Builder while preserving the accepted deterministic builder boundary.

A user may describe application intent in natural language. The operating Agent shall translate that intent into the existing canonical App Builder source model:

- application definition;
- Ruleset;
- Dataset; and
- build definition.

The deterministic App Builder continues to consume canonical sources rather than unconstrained conversation.

FS-005 shall not replace the accepted FS-001 through FS-004 construction, packaging, provider, Git, repo-spec, provenance, or post-construction semantics.

## Default Product Mode

Product mode is the default interaction mode.

When a request can reasonably be interpreted as using ADR App Builder to create, inspect, modify, rebuild, or operate on an application realization or its canonical source material, the Agent shall treat it as product use.

The presence of the App Builder implementation repository does not by itself authorize repository-development work.

App Builder repository maintenance requires explicit user intent to modify or maintain ADR App Builder itself.

Generating or operating a Git-backed application realization is product operation, not App Builder repository maintenance.

## Canonical Authoring Boundary

The Agent shall author through the four accepted canonical ownership surfaces.

Application identity and application-owned initialization belong to the application definition.

Application behavior, invariants, transitions, validation, compatibility, migration, and other rule meaning belong to the Ruleset.

Initial or persisted application-instance values belong to the Dataset.

Packaging topology, runtime representation, provider selection, and other realization choices belong to the build definition.

The Agent shall not route realization choices into Ruleset or Dataset semantics and shall not route application semantics into provider or packaging configuration.

Conversation history shall not become a hidden fifth build input.

## Agent Authoring Contract

FS-005 shall provide a repository-owned, provider-independent agent-authoring contract that mechanically states:

- product mode is the default;
- repository maintenance requires explicit user intent;
- the canonical source roles and their ownership boundaries;
- the distinction between Agent interpretation and deterministic builder execution;
- the consequential-ambiguity rule;
- the shared creation/modification authoring model; and
- the accepted builder invocation boundary.

The contract shall be readable by an operating Agent without requiring inference from implementation source.

Human-facing repository documentation shall explain the same product interaction model without requiring users to manipulate JSON or CLI details for ordinary use.

## Creation and Modification

Creation and modification use the same canonical authoring pipeline.

For creation, the Agent authors a complete canonical source set sufficient for the requested realization and invokes the builder.

For modification, the Agent begins from the existing authoritative canonical sources or authoritative generated application material, applies only the requested semantic or realization changes to the appropriate ownership surfaces, and rebuilds or updates as applicable.

A modification request shall not authorize unrelated canonical-source changes.

FS-005 does not define a universal merge engine for conflicting concurrent edits.

## Ambiguity Handling

The Agent shall resolve non-consequential serialization and implementation details without requiring user decisions.

The Agent shall request user input when unresolved ambiguity would materially change application meaning, authority, behavior, persisted state, compatibility, identity, destructive effect, or another consequential product outcome.

The Agent shall not silently invent consequential application semantics to complete canonical source material.

Mechanical defaults may be used only where accepted Design and Planning establish them as non-semantic realization choices.

## Builder Boundary

The deterministic App Builder remains a canonical-source realization engine.

FS-005 shall not add unconstrained natural-language interpretation to `app_builder.py` or make model output an implicit builder input.

After canonical sources are established, equivalent canonical sources and equivalent resolved external inputs remain subject to the accepted deterministic-build requirements.

Provider profiles remain generated-realization adaptation and shall not become the authoring-intent interpretation layer.

## Repository Guidance

Root repository agent guidance shall make the operating-mode boundary explicit:

- default to product operation;
- perform App Builder repository maintenance only on explicit request;
- preserve the canonical source ownership boundaries when authoring;
- ask only for consequential semantic ambiguity rather than routine serialization choices; and
- distinguish generated-application Git operations from App Builder repository maintenance.

This guidance is an implementation of DP-103 and does not independently create product semantics.

## Validation

FS-005 mechanical Validation shall verify at least:

- existence and shape of the agent-authoring contract;
- default product-mode declaration;
- explicit repository-maintenance opt-in;
- canonical four-source ownership mapping;
- separation of Agent interpretation from builder execution;
- creation/modification use of the same authoring model;
- consequential-ambiguity policy representation;
- provider independence of the authoring contract;
- root agent guidance alignment with the contract; and
- preservation of the existing deterministic builder input surface.

Mechanical Validation cannot establish that an Agent understood every natural-language request correctly.

Semantic Review remains responsible for evaluating whether the resulting operating contract faithfully realizes DP-103.

## Compatibility

FS-001 through FS-004 remain applicable.

FS-005 changes the human-facing operating model, not the semantic meaning of previously accepted canonical source documents or generated realizations.

Existing direct CLI use remains a supported lower-level interface for diagnostics, automation, interoperability, and users who explicitly choose it.

FS-005 does not require generated applications to depend on App Builder or the authoring Agent after construction.

## Exclusions

FS-005 does not define:

- a universal natural-language grammar;
- one mandatory model provider or Agent implementation;
- natural-language parsing inside the deterministic builder;
- a universal conversational-memory subsystem;
- a fifth canonical build input derived from conversation history;
- automatic invention of missing consequential application semantics;
- a graphical user interface;
- a universal concurrent-edit merge engine;
- provider-specific application semantics;
- repository-maintenance authority without explicit user intent; or
- changes to upstream ADR semantics.
