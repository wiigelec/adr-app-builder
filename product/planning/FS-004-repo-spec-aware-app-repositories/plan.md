# FS-004 — Repo-Spec-Aware Application Repositories Plan

design_revision: ac7cca859e6027461f9a23694fb7d8cf38ae026a

## Objective

Implement DP-102 by extending the accepted FS-003 `split-git` realization with a repo-spec-managed Ruleset repository paired with a non-repo-spec Dataset repository.

The Build shall preserve all accepted FS-001 through FS-003 behavior except where FS-004 deliberately strengthens the `split-git` lifecycle contract.

This Planning result owns the consequential technical intent and the canonical normative requirements consumed by Build. Build may make ordinary code-level decisions only within these boundaries.

## Planned Functional Scope

FS-004 work is bounded to:

- resolving one exact accepted repo-spec framework source for each `split-git` build;
- installing reusable repo-spec framework material into the generated Ruleset repository;
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
4. install framework material only from that fetched commit;
5. normalize supported equivalent GitHub SSH/HTTPS forms to one deterministic repository identity for generated source lineage.

Acceptance for the supplying framework is represented by integration into the supplying repository's `main`, matching repo-spec's lifecycle rule that accepted state is intentionally integrated into `main`.

No supplying working tree is used as an authority. Uncommitted local changes are not consumed merely because a local Git repository path is supplied.

### Installed repo-spec framework surface

From the exact resolved repo-spec commit, FS-004 shall install into the generated Ruleset repository:

```text
repo/**
scripts/validate
.github/workflows/validation.yml
```

These are the reusable framework ownership/validation surfaces.

The supplier repository's `product/**`, root `README.md`, and initializer-product-specific product state shall not be copied.

The supplier root `AGENTS.md` shall not be copied verbatim because FS-003 already owns generated root agent guidance. App Builder shall instead generate one combined `AGENTS.md` that preserves accepted runtime Ruleset guidance and adds repo-spec lifecycle guidance sufficient to direct later Design/Planning/Build/Validation/Semantic Review/Acceptance work to the installed framework.

The existing App Builder-generated root `README.md` shall likewise be extended with a development-lifecycle section rather than replaced by the supplying repo-spec README.

FS-004 shall not create a repository-specific `product/` domain during construction. The installed framework and generated guidance make the repository structurally ready for later Ruleset product development; repository-specific `product/` state begins only when later Product Design intentionally creates it.

This avoids creating a vacuous product validator or generated placeholder Product Design.

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

The digest is a deterministic App Builder realization identity for the exact Ruleset content paired into the generated realization. It is not an ADR semantic version, not an independent Ruleset authority, not a Git commit identity, and not an application-owned binding rule.

`binding.json` is realization traceability only. It records which application instance and exact Ruleset content App Builder paired at construction time. It shall not override, reinterpret, normalize, replace, or assign meaning to application-owned binding semantics that may already exist in `application.json`, runtime Ruleset material, or runtime Dataset material.

App Builder shall preserve application-owned source fields according to the accepted FS-001 through FS-003 preservation contracts, including fields whose names appear binding-related. FS-004 defines no universal schema for such fields and shall not infer that an arbitrary field such as `dataset.instance.ruleset_binding` is semantically equivalent to `binding.json.ruleset_authority`.

If a current or future accepted source contract defines a mechanically recognizable application-owned binding assertion and that assertion is mechanically incompatible with the Ruleset content selected for the generated realization, construction shall fail rather than silently rewrite either the application-owned assertion or `binding.json`. When no such accepted mechanical contract exists, App Builder shall preserve the application-owned field unchanged and shall not claim to have validated its semantic compatibility.

A later Ruleset-repository lifecycle operation that intentionally changes applicable Ruleset semantics is responsible for application-owned compatibility handling and for updating realization traceability through that later lifecycle; App Builder does not perform that post-construction operation.

Ordinary Dataset saves shall preserve `binding.json` unchanged under the accepted FS-003 non-Dataset preservation contract.

### Initialization material

Fresh split-git initialization shall use existing accepted runtime material plus `binding.json`:

- `application.json` provides application identity and application-owned initialization semantics;
- Dataset `instance.id` represented in `binding.json` provides selected application-instance identity;
- application-owned Ruleset/binding semantics remain authoritative for interpreting which Ruleset is applicable;
- `binding.json.ruleset_authority` provides realization traceability to the exact Ruleset content App Builder paired at construction time;
- existing runtime component references/guidance identify runtime Ruleset and Dataset locations;
- runtime Dataset material remains authoritative persisted state.

Generated guidance shall never instruct the operating environment to treat `binding.json` as overriding contradictory application-owned semantics. If those semantics cannot establish a determinate applicable Ruleset, that is an application-owned compatibility/initialization issue rather than authority granted to App Builder metadata.

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

The copied root `scripts/validate` remains the canonical repository-wide entry point.

Because FS-004 construction does not create repository-specific `product/`, the root composition shall execute installed `repo/scripts/validate` and shall succeed without requiring a product Validation entry point.

The installed `.github/workflows/validation.yml` shall delegate to root `scripts/validate` as supplied by the exact repo-spec framework revision.

Generated candidate Validation shall execute root `scripts/validate` inside the generated Ruleset repository.

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
- external applicable Ruleset semantics plus App Builder realization traceability recorded by `binding.json`;
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

1. `repo-spec-source` — exact `main` resolution, fetch identity, source truthfulness, and installed framework correspondence.
2. `lifecycle-installation` — split-git-only eligibility, Ruleset framework installation, Dataset/non-split exclusion, and no selector/provider drift.
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
2. Add exact framework extraction/installation from the selected repo-spec commit.
3. Add deterministic `binding.json` generation and preservation.
4. Extend Ruleset-only provenance with repo-spec source lineage.
5. Extend generated Ruleset/Dataset README and AGENTS guidance.
6. Integrate framework installation only into `split-git` Ruleset repository construction.
7. Add the seven planned functional Validation tasks.
8. Bind all mechanically evaluated FS-004 requirements in `product/validation/requirement-evaluation.json`.
9. Validate positive and negative generated candidates, canonical repository Validation, and determinism.
10. Perform Build Review and Semantic Review against DP-102, this Plan, and the canonical FS-004 specification before Acceptance.

## Exclusions

This plan does not authorize:

- lifecycle installation for `single-file`, `split-files`, or `single-git`;
- repo-spec lifecycle installation in Dataset repositories;
- application-specific schema or migration invention;
- a universal ADR Ruleset/Dataset binding format;
- use of Git commit identity as the Ruleset semantic binding identity;
- generated placeholder Product Design or a vacuous product validator;
- automatic repo-spec framework upgrades;
- runtime App Builder participation after construction;
- provider-specific changes to lifecycle eligibility;
- changes to upstream ADR semantics.
