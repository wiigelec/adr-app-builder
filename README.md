# ADR App Builder

ADR App Builder constructs deployable realizations of ADR-derived applications.

ADR remains the Agent · Dataset · Ruleset semantic framework. App Builder owns concrete authoring, packaging, provider adaptation, deterministic generation, and realization validation.


## Agent-operated product interface

Ordinary ADR App Builder use is agent-operated:

```text
human intent
    │
    ▼
AI Agent
    │
    ▼
canonical sources
    │
    ▼
deterministic App Builder
    │
    ▼
generated realization
```

The Agent translates application intent into the canonical application definition, Ruleset, Dataset, and build definition, then invokes the deterministic builder. JSON and the CLI remain available canonical/lower-level interfaces, but ordinary product use does not require the human to author canonical JSON or operate the CLI directly.

Product use is distinct from maintaining the ADR App Builder implementation repository. Repository maintenance occurs only when explicitly requested; operating a generated application's own Git repository remains application/product operation.

The machine-readable Agent Operation Protocol is `product/src/agent-authoring-contract.json`. It defines canonical source requirements, supported realization choices, complete builder invocation, output discovery, and source-authority rules for reopening or modifying applications.

## Repository surfaces

- `repo/design/` - installed framework Design.
- `repo/specs/` - installed framework normative specifications.
- `repo/scripts/validate` - framework-owned mechanical Validation entry point.
- `scripts/validate` - repository-wide mechanical Validation entry point.
- `product/` - App Builder product-owned domain.
- `product/design/` - canonical App Builder Product Design.
- `product/planning/` - Functional Sets and Plans.
- `product/specs/` - canonical normative product specifications.
- `product/src/` - executable builder, profiles, and reference sources.
- `product/validation/` - product-owned mechanical validation fixtures.
- `user/` - user-owned operational material outside the framework.

## Initial model

```text
application source
├── application definition
├── Ruleset
├── Dataset
└── build definition
       │
       ▼
   App Builder
       │
       ├── packaging profile
       └── provider profile(s)
               │
               ▼
         generated provider set
```

The initial Functional Set supports deterministic self-contained JSON output, explicit packaging and provider profiles, dual ADR/App Builder provenance, and complete-realization preservation for governed Dataset updates.

`main` represents accepted repository state. Product work follows Design → Planning → Build → Validation → Semantic Review → Acceptance.
