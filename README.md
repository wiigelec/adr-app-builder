# ADR App Builder

ADR App Builder constructs deployable realizations of ADR-derived applications.

ADR remains the Agent · Dataset · Ruleset semantic framework. App Builder owns concrete authoring, packaging, provider adaptation, deterministic generation, and realization validation.

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
