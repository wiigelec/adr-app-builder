# FS-003 — Git-Native Structured Application Repositories

functional_set: FS-003
design_revision: faefffaa2a1591d6a7c54d9365a036cde0131218

## Purpose

FS-003 realizes DP-101 and the revised DP-100 state model for Git-backed application repositories.

It extends the existing `single-git` and `split-git` profiles so generated repositories:

- operate independently of App Builder after construction;
- preserve the exact App Builder CLI input files under `init-config/`;
- keep runtime Ruleset and Dataset material at repository root;
- support runtime Ruleset and Dataset realization as either files or directory trees;
- generate deterministic `README.md` and `AGENTS.md`;
- distinguish active in-memory application state from persisted Dataset state;
- persist Dataset state only through explicit save behavior.

## CLI Input Preservation

App Builder continues to consume the same four JSON input files:

- application definition;
- Ruleset;
- Dataset;
- build definition.

Every generated Git repository shall contain:

```text
init-config/
├── application.json
├── ruleset.json
├── dataset.json
└── build.json
```

Each file in `init-config/` shall be a byte-for-byte copy of the corresponding file supplied to the App Builder CLI invocation that created the repository.

`init-config/` is not runtime Ruleset material and is not runtime Dataset state.

Ordinary runtime operation shall not mutate `init-config/`.

## Runtime Component Realization

Runtime Ruleset and Dataset material remain at repository root.

Each runtime component may be realized as either:

- one JSON file; or
- one structured directory tree.

The build definition owns the physical realization choice and the deterministic mapping required to produce file or tree output.

Ruleset and Dataset JSON inputs remain semantic inputs and shall not contain App Builder-owned physical-layout semantics.

Runtime realization shall preserve the semantic meaning of the Ruleset and Dataset inputs.

## Single-Git Repository Contract

A `single-git` repository contains:

```text
README.md
AGENTS.md
init-config/
ruleset.json or ruleset/
dataset.json or dataset/
```

Ruleset and Dataset may independently use file or tree realization.

During operation of the generated application, a save updates only runtime Dataset material and the shared repository history. App Builder is not involved in that runtime save or history evolution.

A save shall preserve:

- runtime Ruleset material;
- `init-config/`;
- `README.md`;
- `AGENTS.md`;
- other non-Dataset generated realization material.

## Split-Git Repository Contract

`split-git` generates two repositories.

The Ruleset repository contains:

```text
README.md
AGENTS.md
init-config/
ruleset.json or ruleset/
```

The Dataset repository contains:

```text
README.md
AGENTS.md
init-config/
dataset.json or dataset/
```

Both repositories receive the complete four-file `init-config/` snapshot.

The duplicated snapshot does not create duplicate runtime authority.

During operation of the generated application, a Dataset save updates only the Dataset repository. App Builder is not involved in that runtime save or Dataset-repository history evolution.

## Active Application State

The active Agent/session may maintain current governed application state in working memory.

That working state is the current application state for the active session.

A governed interaction may change active working state without modifying the persisted Dataset.

Ordinary conversation content is not automatically application state.

## Persisted Dataset State

The runtime Dataset is persisted application state.

Opening or initializing the application loads active working state from the runtime Dataset unless application-owned semantics define another governed recovery behavior.

Persisting working state is distinct from changing working state.

A user-requested or user-accepted save writes current governed working state to the runtime Dataset.

Closing or losing a session before save may discard newer volatile changes.

## Repository Guidance

Every generated Git repository shall include deterministic `README.md` and `AGENTS.md`.

README shall describe:

- repository role;
- runtime component locations;
- `init-config/` purpose;
- active-state versus persisted-state behavior;
- save behavior.

AGENTS shall provide topology-specific operational guidance without creating application semantics.

## Determinism and Repository Creation Time

Equivalent resolved build inputs shall produce deterministic generated repository content and the same Git tree.

Each generated Git repository shall contain exactly one initial commit containing that complete generated tree. The commit shall use actual construction time for author and committer timestamps so a newly generated repository appears newly created on Git hosting surfaces.

Repeat-build determinism applies to generated content and Git tree identity, not to the initial commit SHA or timestamp.

No creation/bootstrap commit or `.adr-app-builder-created.json` marker shall be generated.

Runtime working-state changes do not affect Git state until persisted.

Persisted Dataset changes are runtime state evolution rather than repeated-build output.

## Compatibility

Existing single-document Git runtime layouts remain valid.

When no structured realization is requested, runtime outputs remain:

```text
ruleset.json
dataset.json
```

FS-003 does not extend `single-file` or `split-files`.

## Exclusions

FS-003 does not define:

- a universal Ruleset tree schema;
- a universal Dataset tree schema;
- directory-valued CLI Ruleset/Dataset inputs;
- automatic save independent of user request or acceptance;
- concurrent-session save/conflict/merge semantics;
- migration or upgrade automation;
- Git remote creation, push, synchronization, or hosting;
- provider-specific repository instructions.

## Corrective Runtime Application Preservation — Issue #5

Git-backed generated applications shall preserve the application definition as explicit runtime material independently of `init-config/`.

For `single-git`, the generated repository shall contain a deterministic root `application.json` semantically equal to the application-definition CLI input.

For `split-git`, both generated repositories shall contain the same deterministic root `application.json` so repository-local agent guidance can consume application-owned initialization without treating `init-config/application.json` as runtime authority.

Generated `AGENTS.md` shall direct the operating Agent/environment to consume the runtime application definition and apply its application-owned initialization semantics. Guidance shall not duplicate or reinterpret application-specific initialization instructions.

Ordinary Dataset saves shall preserve the runtime application definition unchanged.

## Corrective Provenance Preservation — Issue #5

Every generated Git repository shall contain deterministic immutable provenance material identifying:

- the ADR repository used for construction and the exact resolved ADR commit;
- the ADR App Builder repository and the exact clean App Builder commit used for construction.

The App Builder repository identity shall identify the actual checkout repository supplying the recorded App Builder commit, not an assumed canonical upstream. Common equivalent GitHub transport forms shall normalize to one deterministic repository identity so HTTPS and SSH checkouts of the same repository do not change generated provenance content. A forked checkout shall record the fork repository identity.

The canonical Git-backed realization uses root `provenance.json`.

Provenance is lineage and upgrade-anchor material only. It is not application, Ruleset, Dataset, active-working-state, or provider authority.

Ordinary Dataset saves shall preserve provenance unchanged. Equivalent resolved build inputs shall produce byte-identical provenance content.
