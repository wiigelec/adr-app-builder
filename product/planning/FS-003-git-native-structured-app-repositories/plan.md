# FS-003 — Git-Native Structured Application Repositories Plan

## Objective

Implement the finalized DP-100/DP-101 architecture for Git-backed application repositories.

The Build shall:

- copy the four CLI input files byte-for-byte into `init-config/`;
- keep runtime Ruleset and Dataset material separate at repository root;
- allow build-defined runtime file or tree realization;
- generate deterministic README/AGENTS guidance;
- model active working state separately from persisted Dataset state;
- persist Dataset state only on explicit save;
- preserve Git packaging semantics while using current repository-construction time for the one initial Git commit.

## CLI Contract

The App Builder CLI remains unchanged:

```text
--application <application.json>
--ruleset <ruleset.json>
--dataset <dataset.json>
--build <build.json>
```

All four arguments identify JSON files.

FS-003 shall not accept Ruleset or Dataset directories as CLI inputs.

## init-config

For every generated Git repository:

```text
init-config/
├── application.json
├── ruleset.json
├── dataset.json
└── build.json
```

The files shall be copied from the exact CLI inputs.

Validation shall compare raw bytes, not parsed JSON equivalence.

The destination names are canonical regardless of caller source filenames.

Runtime writes shall never modify `init-config/`.

## Build-Owned Runtime Realization

The build definition shall own file/tree realization.

A planned build-definition section is:

```json
{
  "runtime": {
    "ruleset": {
      "representation": "file"
    },
    "dataset": {
      "representation": "file"
    }
  }
}
```

or:

```json
{
  "runtime": {
    "ruleset": {
      "representation": "tree",
      "files": {
        "purpose.json": "/purpose",
        "authority.json": "/authority",
        "standard-interactions.json": "/standard_interactions",
        "task-states.json": "/task_states",
        "transitions.json": "/transitions",
        "invariants.json": "/invariants"
      }
    },
    "dataset": {
      "representation": "tree",
      "files": {
        "instance.json": "/instance",
        "state.json": "/state",
        "history.json": "/history"
      }
    }
  }
}
```

Tree selectors shall use RFC 6901 JSON Pointer syntax.

Each Ruleset selector is evaluated from the root of the Ruleset JSON input document.

Each Dataset selector is evaluated from the root of the Dataset JSON input document.

The mapping belongs to `build.json` and shall not be reinterpreted as Ruleset or Dataset semantics.

### File representation

Default for backward compatibility.

Ruleset runtime path:

```text
ruleset.json
```

Dataset runtime path:

```text
dataset.json
```

The runtime JSON shall represent the semantic Ruleset or Dataset input without injecting App Builder realization metadata.

### Tree representation

For each tree component, `build.json` supplies deterministic relative output paths and selectors identifying source values from the semantic input document.

Requirements:

- output paths are normalized relative POSIX paths;
- absolute paths are rejected;
- `..` traversal is rejected;
- empty path segments are rejected;
- `.git` path segments are rejected;
- duplicate normalized output paths are rejected;
- package-owned paths are rejected;
- selectors use RFC 6901 JSON Pointer syntax;
- selectors are resolved against the root of the corresponding Ruleset or Dataset input document;
- nonexistent selectors are rejected;
- duplicate source selectors within one component mapping are rejected;
- overlapping ancestor/descendant selectors within one component mapping are rejected;
- the selected source values shall collectively preserve the complete source document without omission or duplication;
- deterministic reconstruction from the realized tree using the configured mapping shall produce a JSON value semantically equal to the original source document;
- output path order is deterministic;
- each selected source value is serialized deterministically as JSON;
- at least one output file is required.

The tree mechanism is an App Builder realization mapping, not a universal Ruleset/Dataset schema.

Tree realization is physical restructuring only. It shall not create, remove, duplicate, or reinterpret Ruleset behavior or Dataset state.

## Repository Layout

### single-git

File/file:

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

Tree/tree:

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

Mixed file/tree combinations are valid.

### split-git Ruleset repo

```text
README.md
AGENTS.md
init-config/
  application.json
  ruleset.json
  dataset.json
  build.json
ruleset.json or ruleset/
```

### split-git Dataset repo

```text
README.md
AGENTS.md
init-config/
  application.json
  ruleset.json
  dataset.json
  build.json
dataset.json or dataset/
```

## Package References

Git package references shall identify runtime shape explicitly.

File example:

```json
{
  "kind": "file",
  "path": "ruleset.json"
}
```

Tree example:

```json
{
  "kind": "tree",
  "path": "ruleset"
}
```

The same applies to Dataset.

Split-Git references additionally retain repository identity/location information already defined by FS-002.

## README Generation

README content shall be deterministic and topology-specific.

It shall identify:

- package profile;
- repository role;
- runtime Ruleset/Dataset locations;
- `init-config/` as exact copies of CLI inputs;
- that runtime Dataset state may evolve independently of `init-config/dataset.json`;
- that active application state may differ from persisted Dataset state until save.

## AGENTS Generation

### single-git

AGENTS shall instruct the Agent to:

1. read the runtime Ruleset;
2. initialize active working state from the runtime Dataset;
3. maintain governed working state during the session;
4. apply governed edits to active working state without automatic Dataset persistence;
5. treat active working state as current session state;
6. save to runtime Dataset only when the user requests or accepts save;
7. preserve runtime Ruleset, `init-config/`, README, AGENTS, and non-Dataset realization material during ordinary save;
8. never use `init-config/dataset.json` as mutable runtime storage.

### split Ruleset repository

AGENTS shall state:

- local runtime Ruleset defines behavior;
- persisted Dataset state is external;
- ordinary state saves do not belong in this repository;
- `init-config/` contains exact original CLI inputs and is not mutable runtime state.

### split Dataset repository

AGENTS shall state:

- local runtime Dataset is persisted application state;
- applicable runtime Ruleset is external and required for governed operation;
- active working state initializes from Dataset;
- governed edits may remain volatile;
- save persists current working state here;
- `init-config/` is not mutable runtime state.

## Post-Construction Operational Boundary

App Builder constructs the generated repository or repositories and then exits the ordinary application lifecycle.

After construction, the generated application is self-contained for ordinary operation. Initialization, active working-state management, Dataset persistence, and runtime Git-history evolution are responsibilities of the generated application and its operating Agent/environment. They shall not require App Builder to remain available or participate as a runtime, save, or commit service.

Any later App Builder invocation is a separate build or rebuild operation, not continuation of the runtime lifecycle of the already generated application.

## Active-State Test Model

Mechanical tests cannot inspect LLM private memory directly.

Build shall therefore include a deterministic session-state harness that models the generated application's operational contract without making App Builder a runtime dependency. The harness shall implement:

```text
open:
    persisted Dataset -> active working state

edit:
    active working state -> changed active working state
    persisted Dataset unchanged

read:
    observe active working state

save:
    active working state -> persisted Dataset

reopen:
    persisted Dataset -> new active working state
```

Tests shall establish that edit and save are distinct operations.

## Dataset Save Behavior

The following save behavior describes operation of the generated application after App Builder construction is complete.

### single-git

On save:

- only runtime Dataset paths may change;
- runtime Ruleset paths remain unchanged;
- `init-config/` remains byte-identical;
- README/AGENTS remain unchanged;
- the repository may receive a Dataset-save commit.

### split-git

On save:

- Ruleset repository remains unchanged;
- Dataset runtime paths may change;
- Dataset `init-config/` remains byte-identical;
- Dataset README/AGENTS remain unchanged;
- only Dataset repository history advances;
- App Builder does not participate in the save or runtime commit.

## Git Initialization

Generalize Git initialization to stage deterministically:

- raw `init-config/` copies;
- runtime file outputs;
- runtime tree outputs;
- generated README;
- generated AGENTS;
- existing package metadata/provenance.

All paths shall be sorted before staging.

Each generated Git repository shall receive exactly one initial commit with:

- the complete generated repository tree;
- App Builder author and committer identity;
- author and committer timestamps taken from the actual repository-construction time, with second precision;
- canonical branch `main`;
- fixed commit message `ADR App Builder initial package`.

Equivalent resolved builds shall reproduce the same generated file content and Git tree. They are not required to reproduce the same initial commit SHA because commit time is repository-instance metadata.

No creation/bootstrap commit and no `.adr-app-builder-created.json` file shall be generated.

Generated application repositories shall continue to have no configured remote.

## Fixtures

Retain the existing task-tracker fixture for backward compatibility.

Add one FS-003 structured fixture with:

- four ordinary JSON CLI inputs;
- `build.json` requesting tree runtime realization;
- nested Ruleset tree paths;
- nested Dataset tree paths;
- at least two Dataset files involved in save;
- exact `init-config/` byte-fidelity checks;
- single-git and split-git coverage;
- active edit without persistence;
- explicit save persistence.

## Failure Cases

Build shall fail for:

- unsupported runtime representation;
- missing tree mapping;
- empty tree mapping;
- invalid relative output path;
- absolute output path;
- path traversal;
- `.git` path segment;
- duplicate normalized path;
- collision with `README.md`, `AGENTS.md`, `init-config/`, Ruleset root, or Dataset root as applicable;
- invalid RFC 6901 source selector;
- nonexistent source selector;
- duplicate source selector within one component mapping;
- overlapping ancestor/descendant source selectors;
- incomplete mapping that omits any source material;
- mapping that cannot deterministically reconstruct a JSON value semantically equal to the original source document;
- ambiguous package reference.

## Compatibility

If `build.json` contains no FS-003 runtime realization section:

- Ruleset defaults to file representation;
- Dataset defaults to file representation;
- root names remain `ruleset.json` and `dataset.json`.

Existing Git repositories intentionally gain README, AGENTS, and `init-config/` under FS-003. Equivalent FS-003 inputs preserve deterministic generated content and Git tree identity, while initial Git commit SHA varies with repository construction time.

`single-file` and `split-files` remain unchanged.

## Validation

Canonical validation shall verify:

- raw byte equality between each CLI input and `init-config/` copy;
- default file realization;
- build-owned tree realization;
- mixed file/tree realization;
- deterministic tree paths and serialization;
- lossless tree realization with deterministic reconstruction semantically equal to the complete source document;
- rejection of incomplete or overlapping tree mappings;
- runtime Ruleset/Dataset separation;
- package-reference `kind` and `path`;
- deterministic README/AGENTS;
- provider independence: changing only provider selection does not change generated repository guidance or runtime Ruleset/Dataset structure/content;
- active edit without Dataset write;
- explicit save causing Dataset write;
- non-Dataset preservation;
- split-Git Ruleset isolation;
- repeat-build deterministic generated repository content and Git tree identity;
- exactly one initial Git commit per generated repository;
- initial commit contains the complete generated tree, uses the fixed initial message, and has current construction-time author/committer timestamps;
- no creation/bootstrap commit or `.adr-app-builder-created.json` marker;
- clean source-input preservation.

Concurrent-session conflict behavior is not part of FS-003 validation.

Mechanical validation passing does not establish semantic acceptance.
