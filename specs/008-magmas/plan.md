# Implementation Plan: Magmas category implementation (`cat.magmas`)

**Branch**: `008-magmas` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.magmas` in `backends/magmas.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: GAP through Sage `libgap` (`MagmaByMultiplicationTable`, `IsAssociative`) and Sage category membership (`Magmas()`, `Semigroups()`) (engine survey, "Magmas, semigroups, monoids").
**Module**: `backends/magmas.py`, run as `/sage/.venv/bin/python3 -m backends.magmas` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/sets.py` (spec 003). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_magmas.py`, `tests/scenarios/magmas-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/magmas.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/008-magmas/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/magmas.py
tests/test_magmas.py
tests/scenarios/magmas-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.magmas` | category structure | operation-preserving maps as Sage `SetMorphism`s of the carriers; identity and composition of `Hom` in `Sets()` | the selected data that the request carries (LV4) | lean-categories T005 (#193) |
| FR-002 | `clf.magmas.associative` | classifier | Sage category membership `M in Semigroups()` of the engine parent; GAP `IsAssociative` for a magma given by a finite table | the selected data that the request carries (LV4) | lean-categories T033 (#197) |
| FR-003 | `forget[clf.sets.binary_operation]` | classifier forget | object action: the carrier to the public constructor of `cat.sets`; morphism action: the map of sets at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | lean-categories T033 (#197) |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Magmas, semigroups, monoids".

## Complexity Tracking

No constitution violation needs a justification.
