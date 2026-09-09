# FS-004 — Repo-Spec-Aware Application Repositories Plan

design_revision: ac7cca859e6027461f9a23694fb7d8cf38ae026a

## Objective

Implement DP-102 by extending the accepted FS-003 `split-git` realization with a repo-spec-managed Ruleset repository paired with a non-repo-spec Dataset repository.

The Build shall preserve all accepted FS-001 through FS-003 behavior except where FS-004 deliberately strengthens the `split-git` lifecycle contract.

This Planning result owns the consequential technical intent and the canonical normative requirements consumed by Build. Build may make ordinary code-level decisions only within these boundaries.

## Planned Functional Scope

FS-004 work is bounded to:

- resolving one exact accepted repo-spec framework source for each `split-git` build;
- constructing the generated Ruleset repository through the selected repo-spec initializer and adapting its installed structural policy for the exact App Builder-owned runtime/realization surface;
- generating combined runtime/development guidance without inventing application-specific Product Design;
- excluding repo-spec lifecycle material from the Dataset repository and non-`split-git` packaging profiles;
- preserving accepted runtime Ruleset and Dataset realizations from FS-003;
- establishing a deterministic Ruleset/Dataset binding mechanism for independently evolving split repositories;
- preserving initialization determinacy under that binding;
- extending generated source-lineage material to identify the installed repo-spec framework revision;
- preserving post-construction independence;
- validating generated candidate repositories mechanically.

## Consequential Technical Decisions

### Repo-Spec source contract

App Builder shall add CLI option:

```text
--repo-spec-repository <git-repository>
```

with default:

```text
https://github.com/wiigelec/repo-spec.git
```

The option is accepted by the CLI for compatibility of one command surface, but it is resolved and consumed only when `build.packaging_profile` is `split-git`. Changing it for a non-`split-git` build shall not alter generated output.

For `split-git`, App Builder shall:

1. resolve `<repository>` `refs/heads/main` with Git;
2. require that the reference resolves to one commit;
3. fetch that exact commit into an isolated temporary Git repository;
4. require the fetched supplying checkout to expose the accepted `repo-spec init --repo DESTINATION` initializer contract reviewed at accepted repo-spec revision `f241d287e0ca9476c3ea96e3c5ad0cc49767ed04` or a later accepted compatible revision;
5. invoke the initializer from that exact fetched supplying checkout against an empty temporary Ruleset candidate repository;
6. treat the initializer-produced repository as the only authoritative repo-spec lifecycle scaffold for that generated Ruleset repository rather than selectively copying framework paths;
7. normalize supported equivalent GitHub SSH/HTTPS forms to one deterministic repository identity for generated source lineage.

Acceptance for the supplying framework is represented by integration into the supplying repository's `main`, matching repo-spec's lifecycle rule that accepted state is intentionally integrated into `main`.

No supplying working tree is used as an authority. Uncommitted local changes are not consumed merely because a local Git repository path is supplied.

### Repo-Spec initialization and structural-policy adaptation

Accepted repo-spec revision `f241d287e0ca9476c3ea96e3c5ad0cc49767ed04` establishes the initializer and repository-owned structural-policy contract consumed by this Planning result.

App Builder shall not manually assemble a partial repo-spec repository by copying `repo/**`, `scripts/validate`, `.github/workflows/validation.yml`, or other selected framework paths.

Instead, from the exact resolved accepted supplying commit, App Builder shall invoke:

```text
repo-spec init --repo <temporary-ruleset-candidate>
```

using that supplying checkout's accepted initializer implementation.

The initialized candidate is the authoritative generic repo-spec repository scaffold. App Builder shall preserve initializer-produced reusable framework state, root Validation composition, CI delegation, framework source identity, generic product-development scaffold, and canonical:

```text
repo/validation/structure-policy.json
```

The generic `product/` scaffold produced by repo-spec initialization is lifecycle infrastructure and readiness state. App Builder shall not populate it with application-specific Product Design, normative requirements, validators, migration semantics, or other invented application meaning during FS-004 construction.

After successful initialization and before adding App Builder runtime/realization material, App Builder shall adapt only the installed structural-policy authorization required by the exact generated Ruleset repository shape.

For every FS-004 `split-git` Ruleset repository, Planning authorizes these additional maintained root files:

```text
application.json
binding.json
provenance.json
```

and this additional maintained root directory:

```text
init-config
```

The selected Ruleset runtime representation additionally authorizes exactly one of:

```text
root.files += ["ruleset.json"]
```

or:

```text
root.directories += ["ruleset"]
```

according to the already accepted FS-003 file/tree realization.

App Builder shall preserve every initializer-supplied authorization and shall not remove or reinterpret repo-spec-required roles. Policy adaptation shall remain explicit and finite; it shall not add wildcard, glob, recursive, negative, plugin, or generalized bypass behavior.

After policy adaptation, App Builder shall add the accepted FS-003/FS-004 application material, generated combined guidance, binding material, and Ruleset-only construction provenance.

The Dataset repository shall continue to use the accepted App Builder construction path and shall not invoke repo-spec initialization or receive repo-spec lifecycle state.

### Ruleset/Dataset binding representation

Every generated `split-git` Ruleset and Dataset repository shall contain deterministic root:

```text
binding.json
```

Both repositories shall receive byte-identical binding content for one generated pair.

The binding object shall have this realization-owned shape:

```json
{
  "schema_version": 1,
  "application_id": "<application.id>",
  "instance_id": "<dataset.instance.id>",
  "ruleset_authority": {
    "kind": "content-sha256",
    "sha256": "<canonical Ruleset semantic digest>"
  }
}
```

`application_id` and `instance_id` reuse identities already required by the accepted App Builder source contract.

The Ruleset digest shall be SHA-256 over canonical UTF-8 JSON encoding of the parsed Ruleset value using:

- keys sorted recursively;
- compact separators;
- UTF-8 with non-ASCII characters preserved;
- no trailing whitespace.

The digest is a deterministic App Builder realization identity for the exact Ruleset content bound into the generated realization. It is not an ADR semantic version, not an independent Ruleset authority, not a Git commit identity, and not an application-owned rule.

`binding.json` is non-authoritative realization binding metadata. Its Ruleset identity does not create or own Ruleset semantics; it determinately identifies which exact Ruleset realization is bound to the generated application instance. It shall not override, reinterpret, normalize, replace, or assign semantic meaning to application-owned binding semantics that may already exist in `application.json`, runtime Ruleset material, or runtime Dataset material.

App Builder shall preserve application-owned source fields according to the accepted FS-001 through FS-003 preservation contracts, including fields whose names appear binding-related. FS-004 defines no universal schema for such fields and shall not infer that an arbitrary field such as `dataset.instance.ruleset_binding` is semantically equivalent to `binding.json.ruleset_authority`.

If a current or future accepted source contract defines a mechanically recognizable application-owned binding assertion and that assertion is mechanically incompatible with the Ruleset realization identified by `binding.json`, construction shall fail rather than silently rewrite either the application-owned assertion or `binding.json`. When no such accepted mechanical contract exists, App Builder shall preserve the application-owned field unchanged and uninterpreted; the mere presence of an unknown binding-looking field does not displace the determinate FS-004 realization binding.

A later Ruleset-repository lifecycle operation that intentionally changes applicable Ruleset semantics is responsible for application-owned compatibility handling and for updating realization traceability through that later lifecycle; App Builder does not perform that post-construction operation.

Ordinary Dataset saves shall preserve `binding.json` unchanged under the accepted FS-003 non-Dataset preservation contract.

### Initialization material

Fresh split-git initialization shall use existing accepted runtime material plus `binding.json`:

- `application.json` provides application identity and application-owned initialization semantics;
- Dataset `instance.id` represented in `binding.json` provides selected application-instance identity;
- application-owned Ruleset semantics remain authoritative for what the applicable Ruleset means and how compatibility or transition is governed;
- `binding.json.ruleset_authority` determinately identifies which exact Ruleset realization is bound to this generated application instance;
- existing runtime component references/guidance identify runtime Ruleset and Dataset locations;
- runtime Dataset material remains authoritative persisted state.

Generated guidance shall never instruct the operating environment to treat `binding.json` as owning or redefining Ruleset semantics. The binding identifies which Ruleset realization applies; the identified Ruleset and application-owned semantics determine what that authority means and how compatibility, migration, refusal, recovery, or transition is governed.

Generated Ruleset and Dataset `README.md` / `AGENTS.md` shall direct the operating environment to use these surfaces without duplicating application-specific semantics.

### Repo-Spec source provenance

For FS-004 `split-git`, the Ruleset repository's root `provenance.json` shall extend the accepted FS-003 construction lineage with:

```json
"repo_spec": {
  "repository": "<normalized supplying repository identity>",
  "commit": "<exact resolved main commit>"
}
```

The Dataset repository shall retain the accepted FS-003 ADR/App Builder construction provenance and shall not gain repo-spec source provenance merely because its paired Ruleset repository uses repo-spec.

`binding.json` is a separate realization record and shall not be embedded into `provenance.json`.

This keeps:

- construction source lineage;
- applicable Ruleset binding;
- runtime Ruleset identity;
- Dataset committed values; and
- Git history

mechanically distinct.

### Dataset-side Ruleset governance artifacts

The generic FS-004 construction shall not install application-specific validators, migration helpers, or other Ruleset-governance artifacts into the Dataset repository.

FS-004 nevertheless preserves the Design boundary for future Ruleset products: if later application-specific lifecycle work installs such artifacts Dataset-side, their Ruleset ownership and traceability must remain explicit and must not install repo-spec lifecycle ownership in the Dataset repository.

Build Validation for FS-004 shall verify that the generic generated Dataset repository contains no repo-spec framework surface.

### Generated Ruleset repository Validation

The root `scripts/validate` installed by the selected repo-spec initializer remains the canonical repository-wide entry point.

The initializer-produced generic product scaffold and Validation composition shall remain intact. App Builder shall not replace that composition with a generated substitute.

The installed `.github/workflows/validation.yml` shall continue to delegate to root `scripts/validate` as supplied by the exact repo-spec framework revision.

After structural-policy adaptation and application-material insertion, generated candidate Validation shall execute root `scripts/validate` inside the completed Ruleset repository and construction shall fail before promotion if canonical Validation fails.

### Generated guidance

The generated Ruleset repository guidance shall distinguish:

- runtime `application.json`;
- runtime Ruleset material;
- `binding.json`;
- construction `provenance.json`;
- immutable `init-config/`;
- installed `repo/` framework material;
- canonical root `scripts/validate`;
- future repository-specific `product/` ownership when later Design creates it.

The generated Dataset repository guidance shall distinguish:

- runtime `application.json`;
- persisted Dataset material;
- external applicable Ruleset semantics plus the determinate Ruleset realization binding recorded by `binding.json`;
- construction provenance;
- `init-config/`;
- absence of repo-spec product-development lifecycle ownership.

Provider profiles shall not modify these lifecycle distinctions.

## Stable Normative Requirement IDs

The canonical specification `product/specs/FS-004-repo-spec-aware-application-repositories.md` is part of this Planning result and uses stable IDs `FS-004-NR-001` through `FS-004-NR-031`.

The IDs and classifications are fixed by Planning and shall not be renumbered during Build.

Mechanically evaluated requirements (`M` and `B`) are published by Planning with `**State: Inactive**` until Build constructs their real enforcement.

Build shall activate each mechanically evaluated FS-004 requirement only in the same candidate that:
- removes that requirement's `State: Inactive` marker;
- implements the real Validation task predicate; and
- adds the corresponding manifest binding.

Placeholder, vacuous, or pre-implementation bindings are prohibited.

## Evaluation Classification

The canonical specification classifies requirements using the accepted repository convention:

- **S** — semantic correctness requires Semantic Review;
- **B** — boundary/compatibility obligation;
- **M** — mechanically decidable obligation requiring product Validation once Build supplies the corresponding enforcement task.

Planning owns these classifications. Build owns construction of the corresponding mechanical enforcement.

## Planned Validation Responsibilities

Build shall introduce functional Validation tasks covering these responsibilities:

1. `repo-spec-source` — exact `main` resolution, fetch identity, accepted initializer availability, source truthfulness, and initialized framework correspondence.
2. `lifecycle-installation` — split-git-only initializer invocation, exact installed structural-policy adaptation, Dataset/non-split exclusion, and no selector/provider drift.
3. `ruleset-binding` — deterministic `binding.json`, semantic digest construction, preservation/non-override of application-owned binding fields, binding/provenance separation, recognized-contract conflict rejection, and initialization determinacy.
4. `generated-ruleset-lifecycle` — installed framework structure, combined guidance, canonical root Validation, CI delegation, and no generated repository-specific `product/`.
5. `split-repository-independence` — post-construction Ruleset/Dataset independence and Dataset save preservation.
6. `fs004-provenance` — Ruleset-only repo-spec provenance and distinction from binding/ADR/App Builder lineage.
7. `fs004-determinism` — equivalent resolved inputs including repo-spec commit produce byte-identical generated content and Git tree identity.

These task names are part of Planning's consequential Validation intent and shall be used for FS-004 requirement bindings unless Build discovers a concrete mechanical reason that requires returning to Planning.

## Planned Requirement Binding

Build shall bind every M-classified FS-004 requirement to one or more of the functional tasks above according to the requirement's actual predicate.

S-classified requirements remain Semantic Review obligations.

B-classified requirements shall receive mechanical bindings where their boundary is mechanically enforceable and Semantic Review shall also confirm that the boundary meaning is preserved.

The requirement-evaluation manifest shall not be changed during Planning. Build shall update it only when the corresponding task implementations exist and the bound requirements are activated in the same candidate.

## Build Sequence

Build shall consume this reviewed Planning result and its canonical normative specification.

1. Add repo-spec source resolution/fetch helpers and the `--repo-spec-repository` CLI surface.
2. Invoke the exact selected supplying commit's accepted `repo-spec init --repo DESTINATION` initializer against an empty temporary Ruleset candidate.
3. Adapt the initializer-installed `repo/validation/structure-policy.json` with exactly the App Builder-owned root files/directories authorized by this Plan and the selected FS-003 Ruleset runtime representation.
4. Add accepted FS-003 runtime material plus deterministic `binding.json` generation and preservation into the initialized Ruleset candidate.
5. Extend Ruleset-only provenance with repo-spec source lineage.
6. Extend generated Ruleset/Dataset README and AGENTS guidance without replacing initializer-owned lifecycle composition.
7. Keep the Dataset repository on the non-repo-spec construction path.
8. Add the seven planned functional Validation tasks.
9. Bind all mechanically evaluated FS-004 requirements in `product/validation/requirement-evaluation.json`.
10. Validate positive and negative generated candidates, canonical generated Ruleset repository Validation, and determinism.
11. Perform Build Review and Semantic Review against DP-102, this Plan, and the canonical FS-004 specification before Acceptance.

## Exclusions

This plan does not authorize:

- lifecycle installation for `single-file`, `split-files`, or `single-git`;
- repo-spec lifecycle installation in Dataset repositories;
- application-specific schema or migration invention;
- a universal ADR Ruleset/Dataset binding format;
- use of Git commit identity as the Ruleset semantic binding identity;
- manual selective copying of repo-spec framework/lifecycle files instead of using the accepted initializer;
- treating initializer-produced generic product scaffold as accepted application-specific Product Design;
- automatic repo-spec framework upgrades;
- runtime App Builder participation after construction;
- provider-specific changes to lifecycle eligibility;
- changes to upstream ADR semantics.
