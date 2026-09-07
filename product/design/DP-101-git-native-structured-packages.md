---
doc_id: DP-101
title: Git-Native Structured Package Architecture
depends_on:
  - DP-100
---

# Git-Native Structured Package Architecture

## Purpose

ADR App Builder shall support Git-backed application repositories whose runtime Ruleset and Dataset representations may be larger or more structured than one JSON file, while preserving the four-file App Builder invocation model, repository-local guidance, and the Ruleset/Dataset semantic boundary established by DP-100.

This Design extends DP-100. It does not replace provider separation, deterministic-build requirements, Git provenance, or the distinction between Ruleset behavior and Dataset state.

## App Builder Invocation Model

App Builder continues to consume four semantically distinct JSON input files:

- application definition;
- Ruleset configuration;
- Dataset configuration;
- build definition.

These four JSON files are the inputs supplied to the App Builder CLI invocation. Runtime Ruleset and Dataset realization shape is independent of the physical shape of these input files.

A Ruleset configuration input remains one JSON file even when the generated runtime Ruleset is a directory tree.

A Dataset configuration input remains one JSON file even when the generated runtime Dataset is a directory tree.

FS-003 does not redefine the App Builder CLI around directory-valued Ruleset or Dataset inputs.

## Initialization Configuration Snapshot

Every generated Git repository shall contain an `init-config/` directory with exact copies of the files supplied to the App Builder CLI invocation that created the repository.

For the current four-file invocation model:

```text
init-config/
├── application.json
├── ruleset.json
├── dataset.json
└── build.json
```

Each copied file shall be byte-for-byte identical to the corresponding CLI input file.

Its purpose is to preserve the exact App Builder invocation inputs in the generated repository so those same files can be used to rerun App Builder.

`init-config/` is not runtime Ruleset authority and is not runtime Dataset state.

Ordinary application execution, working-state changes, saves, Ruleset use, and Dataset persistence shall not mutate `init-config/`.

For split-Git packaging, each generated repository receives the complete four-file `init-config/` snapshot. Duplication is intentional and does not create additional runtime authority.

## Runtime Component Model

The runtime Ruleset and runtime Dataset are generated realization components at repository root.

Each runtime component may be represented by either:

- one JSON file; or
- a structured directory tree containing multiple files and directories.

A structured runtime Ruleset remains one Ruleset semantic component.

A structured runtime Dataset remains one Dataset semantic component.

The runtime representation shall remain independently identifiable and addressable regardless of whether it is one file or a tree.

The build definition owns the physical runtime realization choice and any deterministic mapping needed to realize a Ruleset or Dataset as a file or tree.

Ruleset and Dataset input documents remain the semantic sources for their runtime components. File/tree realization directives shall not become Ruleset or Dataset meaning.

The exact build-definition schema used to select and map file-or-tree realization is a Planning and Build concern. This Design does not impose a universal internal tree schema.

## Runtime and Configuration Separation

The four files under `init-config/` describe the App Builder invocation that produced the repository.

The runtime Ruleset and Dataset at repository root are the realized application components used during application operation.

These roles shall not be conflated.

A runtime Dataset may evolve after generation while `init-config/dataset.json` remains unchanged.

A runtime Ruleset may later be deliberately upgraded while `init-config/ruleset.json` remains the original build-input snapshot unless a separately governed rebuild produces a new realization.

Re-running App Builder from `init-config/` means rebuilding from the original invocation inputs, not reconstructing the latest runtime Dataset state.

Once generated, the Git-backed application repositories operate independently of App Builder. Runtime initialization, active working-state changes, Dataset saves, and subsequent Git-history evolution described by this Design are performed by the generated application and its operating Agent/environment. App Builder does not provide a runtime service, save service, or commit service to an already generated application.

## Single-Git Topology

A `single-git` package uses one Git repository as the shared persistence boundary for runtime Ruleset and Dataset components.

A representative file-backed runtime layout is:

```text
repository/
├── README.md
├── AGENTS.md
├── init-config/
│   ├── application.json
│   ├── ruleset.json
│   ├── dataset.json
│   └── build.json
├── ruleset.json
└── dataset.json
```

A representative structured runtime layout is:

```text
repository/
├── README.md
├── AGENTS.md
├── init-config/
│   ├── application.json
│   ├── ruleset.json
│   ├── dataset.json
│   └── build.json
├── ruleset/
│   └── ...
└── dataset/
    └── ...
```

Mixed file/tree runtime representations are permitted when independently identifiable.

Ruleset and Dataset share repository history but not semantic authority.

## Split-Git Topology

A `split-git` package uses separate Git repositories for runtime Ruleset and runtime Dataset persistence.

The Ruleset repository contains its runtime Ruleset representation at repository root, generated guidance, and the complete duplicated `init-config/` snapshot.

The Dataset repository contains its runtime Dataset representation at repository root, generated guidance, and the complete duplicated `init-config/` snapshot.

Representative layouts are:

```text
ruleset-repository/
├── README.md
├── AGENTS.md
├── init-config/
│   ├── application.json
│   ├── ruleset.json
│   ├── dataset.json
│   └── build.json
└── ruleset.json or ruleset/
```

```text
dataset-repository/
├── README.md
├── AGENTS.md
├── init-config/
│   ├── application.json
│   ├── ruleset.json
│   ├── dataset.json
│   └── build.json
└── dataset.json or dataset/
```

The duplicated configuration snapshot does not change component ownership. The Ruleset repository is the persistence authority for the runtime Ruleset component. The Dataset repository is the persistence authority for the runtime Dataset component.

## Active Application State

An active application session may maintain current application state in agent/session working memory.

That active working state is analogous to an application's in-memory state.

Governed user interactions may change active working state without immediately writing the runtime Dataset.

While the session remains active, the current governed working state may be authoritative for subsequent application interactions even when it differs from the last persisted Dataset state.

Ordinary conversation text is not automatically application state. The agent shall maintain a distinguishable application working state governed by the Ruleset.

## Persisted Dataset State

The runtime Dataset represents persisted application state analogous to saved state on disk.

At application initialization or reopen, active working state is initialized from the persisted runtime Dataset unless another explicitly governed recovery mechanism applies.

A user may make governed changes to active working state and continue interacting with those changes before saving.

Persisting current application state to the Dataset is a distinct operation from changing active working state.

A user-requested or user-accepted save operation writes the current governed working state to the runtime Dataset according to the Ruleset and Dataset representation.

Closing or losing an active session before save may discard volatile working-state changes. The persisted Dataset remains the restore point for a later session.

## Save Semantics

A save operation persists current governed working state to the runtime Dataset.

A save may update one runtime Dataset file or multiple files within a structured runtime Dataset.

A save shall preserve runtime Ruleset material, `init-config/`, generated `README.md`, generated `AGENTS.md`, and other non-Dataset realization material unless a separate governed operation explicitly authorizes their modification.

For `single-git`, a persisted save changes Dataset paths within the shared repository and may advance the shared repository history.

For `split-git`, a persisted save changes only the Dataset repository and shall not require a Ruleset-repository commit.

The physical number of Dataset files written does not alter the semantic classification of the operation.

## Repository Guidance

Every Git repository generated as part of a Git-backed package shall contain deterministic repository-local guidance for human and agent consumers.

### README.md

`README.md` is human-facing realization guidance.

It shall identify the repository role, runtime Ruleset/Dataset layout relevant to that repository, the presence and purpose of `init-config/`, and the distinction between active working state and persisted Dataset state where applicable.

`README.md` is not Ruleset authority and is not Dataset state.

### AGENTS.md

`AGENTS.md` is agent-facing operational guidance.

For `single-git`, it shall direct an agent to:

- identify and read the runtime Ruleset;
- initialize working state from the runtime Dataset;
- apply governed interactions to active working state;
- treat active working state as current session state;
- persist working state to the runtime Dataset when the user requests or accepts a save;
- preserve runtime Ruleset material, `init-config/`, and generated guidance during ordinary saves.

For a split Ruleset repository, it shall identify the local runtime Ruleset as behavior material, identify authoritative persisted Dataset state as external to that repository, and state that ordinary application-state saves do not belong in the Ruleset repository.

For a split Dataset repository, it shall identify the local runtime Dataset as persisted application state, identify the applicable runtime Ruleset as external to that repository, initialize active working state from the Dataset when opening, and persist user-requested or user-accepted saves to the Dataset repository.

`AGENTS.md` shall explain that `init-config/` contains the exact App Builder CLI input files and shall not be used as mutable runtime state.

## Guidance Independence

Generated `README.md` and `AGENTS.md` shall be provider-independent.

Provider adaptation shall not change runtime Ruleset/Dataset component structure or generated repository guidance.

Guidance shall not introduce provider-owned application semantics or reinterpret application-owned initialization, Ruleset, Dataset, or save meaning.

## Deterministic Repository Identity

The four-file `init-config/` snapshot, generated repository guidance, runtime component realization, and any package-owned discovery material participate in deterministic generated package content.

Equivalent resolved build inputs shall produce byte-identical `init-config/` files, deterministic guidance, deterministic runtime layout, and the same generated repository tree.

A generated Git repository shall contain one initial commit. That commit shall:

- contain the complete generated repository tree;
- use App Builder-controlled author and committer identity;
- use the actual repository-construction time for author and committer timestamps;
- use a fixed App Builder-controlled initial commit message;
- be repository `HEAD` on the canonical branch.

The initial commit SHA is storage provenance for that generated repository instance and is intentionally not a repeat-build deterministic identity. The generated tree and package-owned content are the repeat-build deterministic realization.

No App Builder-owned repository-creation marker file or second bootstrap commit shall be added solely to express creation time.

Subsequent governed working-state changes do not affect repository state until persisted.

Subsequent saved Dataset evolution is runtime state evolution and is not required to reproduce the original initial commit SHA.

## Compatibility

Existing single-document runtime Ruleset and Dataset realizations remain valid.

Structured runtime Ruleset and Dataset trees extend Git-backed packaging without requiring directory-valued CLI inputs.

File-backed `single-file` and `split-files` profiles are not required by this Design to adopt structured runtime trees or Git repository guidance.

## Provider and Application Boundaries

Git-native runtime structure remains separate from provider adaptation.

Application definition and application-owned initialization semantics remain distinct from runtime Ruleset/Dataset realization.

The `init-config/` snapshot preserves the four App Builder invocation documents without making those copies additional runtime authorities.

Generated guidance may explain operation and persistence but shall not create new application transitions, invariants, or state.

## Design Boundary

This Design defines:

- four-file App Builder invocation preservation under `init-config/`;
- root runtime Ruleset/Dataset file-or-tree realization;
- active working-state versus persisted Dataset-state semantics;
- explicit save behavior;
- deterministic repository guidance for Git-backed applications.

It does not define:

- a universal runtime Ruleset tree schema;
- a universal runtime Dataset tree schema;
- a universal manifest filename or schema;
- application-specific migration semantics;
- a migration or upgrade engine;
- Git remote creation, push, synchronization, or hosting behavior;
- provider-specific repository instructions;
- automatic save policy independent of user request or acceptance;
- concurrent-session save, conflict-detection, merge, or reconciliation semantics.

Those mechanics may be specified by Planning where required to realize this Design.
