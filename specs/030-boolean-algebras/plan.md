# Implementation Plan: Boolean Algebras category implementation (`cat.boolean_algebras`)

**Branch**: `030-boolean-algebras` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.boolean_algebras` in `backends/boolean_algebras.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage finite sets and power sets (`Set`, `Subsets`), with the power-object values of the sets implementation for infinite subsets (engine survey, "Boolean algebras and power sets").
**Module**: `backends/boolean_algebras.py`, run as `/sage/.venv/bin/python3 -m backends.boolean_algebras` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/sets.py` (spec 003). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_boolean_algebras.py`, `tests/scenarios/boolean_algebras-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/boolean_algebras.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
| LV2, LV14 | No acceptance statement or expected answer; kernel tasks are named by ID or title. |
| LV3 | Each row of each version has a port, or a gap record of mathematically new work. |
| LV4 | Each routine computes from the selected data of the request; tier 1 checks their retention. |
| LV5–LV7 | Each row names its engine routine; each version starts with its survey record. |
| LV8 | Dependent inputs arrive as operands, through declared code dependencies or by a kernel request (column "Dependent inputs"). |
| LV12 | Each moved registration has a decision (table "Registrations that move"). |
| LV13 | The survey task of each version follows the versions of the categories that its rows reach. |

Gate result: pass.

## Project Structure

```text
specs/030-boolean-algebras/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/boolean_algebras.py
tests/test_boolean_algebras.py
tests/scenarios/boolean_algebras-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `obj.boolean_algebras.power_set` | object constructor | Sage `Subsets(S)` for a finite `S`; for an infinite `S` the power-object values of contract T021 | descriptors lowered by the lowering table of `backends/sets.py` (LV8, second option) | lean-categories 001 T013 (#191), contract T021 |
| FR-002 | `op.boolean_algebras.union` | operation | Sage `Set.union` of finite extents; the power-object rows for presented infinite subsets | request operands at the generated layout | lean-categories 001 T013 (#191), contract T021 |
| FR-003 | `op.boolean_algebras.inter` | operation | Sage `Set.intersection` of finite extents; the power-object rows for presented infinite subsets | request operands at the generated layout | lean-categories 001 T013 (#191), contract T021 |
| FR-004 | `op.boolean_algebras.diff` | operation | Sage `Set.difference` of finite extents; the power-object rows for presented infinite subsets | request operands at the generated layout | lean-categories 001 T013 (#191), contract T021 |
| FR-005 | `op.boolean_algebras.symm_diff` | operation | Sage `Set.symmetric_difference` of finite extents | request operands at the generated layout | lean-categories 001 T013 (#191), contract T021 |
| FR-006 | `op.boolean_algebras.subset` | operation | Sage `Set.issubset` of finite extents; membership tests of the power-object rows for a finite subset of a presented infinite subset; otherwise the decision packet `none` | request operands at the generated layout | lean-categories 001 T013 (#191), contract T021 |
| FR-007 | `fun.boolean_algebras.forget` | functor | object action: the carrier to the public constructor of `cat.sets`; morphism action: the homomorphism as a map of sets at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Boolean algebras and power sets".

## Complexity Tracking

No constitution violation needs a justification.
