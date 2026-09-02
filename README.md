# ADR App Builder

ADR App Builder constructs deployable realizations of ADR-derived applications.

ADR remains the Agent · Dataset · Ruleset semantic framework. App Builder owns concrete authoring, packaging, provider adaptation, deterministic generation, and realization validation.

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

The initial Functional Set supports deterministic self-contained JSON output and provider profiles, including a Microsoft Copilot realization profile.

`main` represents accepted repository state. Product work follows Design → Planning → Build → Validation → Semantic Review → Acceptance.
