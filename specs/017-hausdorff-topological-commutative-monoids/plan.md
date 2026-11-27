# Implementation Plan: Hausdorff Topological Commutative Monoids category implementation (`cat.hausdorff_topological_commutative_monoids`)

**Branch**: `017-hausdorff-topological-commutative-monoids` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.hausdorff_topological_commutative_monoids` in `backends/hausdorff_topological_commutative_monoids.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage lazy power series (`LazyPowerSeriesRing`) with the $t$-adic topology (engine survey, "Polynomial rings").
**Module**: `backends/hausdorff_topological_commutative_monoids.py`, run as `/sage/.venv/bin/python3 -m backends.hausdorff_topological_commutative_monoids` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/commutative_rings.py` (spec 016), `backends/additive_commutative_monoids.py` (spec 009). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_hausdorff_topological_commutative_monoids.py`, `tests/scenarios/hausdorff_topological_commutative_monoids-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/hausdorff_topological_commutative_monoids.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/017-hausdorff-topological-commutative-monoids/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/hausdorff_topological_commutative_monoids.py
tests/test_hausdorff_topological_commutative_monoids.py
tests/scenarios/hausdorff_topological_commutative_monoids-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.hausdorff_topological_commutative_monoids` | category structure | continuous homomorphisms of Sage lazy power series rings; identity and composition | the selected data that the request carries (LV4) | — |
| FR-002 | `obj.hausdorff_topological_monoids.power_series` | object constructor | Sage `LazyPowerSeriesRing(K, 't')` with the $t$-adic topology | the parameter commutative ring at the generated layout; descriptors lowered by the lowering table of `backends/commutative_rings.py` (LV8, second option) | — |
| FR-003 | `obj.sets.summable_families` | object constructor | families of Sage lazy power series whose valuations tend to infinity; the sum by Sage lazy `sum` | the parameter topological monoid at the generated layout | lean-categories 001 T027 (#190) |
| FR-004 | `fun.hausdorff_topological_commutative_monoids.additive_commutative_monoid` | functor | object action: the same Sage ring to the public constructor of `cat.additive_commutative_monoids`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Polynomial rings".

## Complexity Tracking

No constitution violation needs a justification.
