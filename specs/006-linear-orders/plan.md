# Implementation Plan: Linear Orders category implementation (`cat.linear_orders`)

**Branch**: `006-linear-orders` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.linear_orders` in `backends/linear_orders.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage posets (`Poset`, `is_lequal`, `is_less_than`) for finite orders; Sage element comparison on `ZZ`, `NonNegativeIntegers()`, `QQ` and the exact reals for the infinite orders (engine survey, "Order structures"; gap "Infinite posets": glue over a comparison function).
**Module**: `backends/linear_orders.py`, run as `/sage/.venv/bin/python3 -m backends.linear_orders` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/sets.py` (spec 003). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_linear_orders.py`, `tests/scenarios/linear_orders-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/linear_orders.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/006-linear-orders/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/linear_orders.py
tests/test_linear_orders.py
tests/scenarios/linear_orders-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.linear_orders` | category structure | monotone maps as Sage `SetMorphism`s of the carriers; identity and composition of `Hom` in `Sets()` | the selected data that the request carries (LV4) | lean-categories T041 (#195) |
| FR-002 | `obj.linear_orders.fin_ordinary` | object constructor | Sage `posets.ChainPoset(n)` | request operands at the generated layout | lean-categories T041 (#195) |
| FR-003 | `obj.linear_orders.fin_reverse` | object constructor | Sage `posets.ChainPoset(n).dual()` | request operands at the generated layout | lean-categories T041 (#195) |
| FR-004 | `obj.linear_orders.integers` | object constructor | Sage `ZZ` with its comparison | request operands at the generated layout | lean-categories T041 (#195) |
| FR-005 | `obj.linear_orders.naturals` | object constructor | Sage `NonNegativeIntegers()` with its comparison | request operands at the generated layout | lean-categories T041 (#195) |
| FR-006 | `obj.linear_orders.reals` | object constructor | Sage `RealSet.real_line()` with the comparison of `AA` and `SR` values | request operands at the generated layout | lean-categories T041 (#195) |
| FR-007 | `op.linear_orders.le` | operation | Sage `Poset.is_lequal` for a finite order; `<=` of `ZZ`, `QQ`, `AA` elements; `bool(x <= y)` in `SR` with the decision packet `none` when neither `x <= y` nor `x > y` is proved | request operands at the generated layout | lean-categories T041 (#195) |
| FR-008 | `op.linear_orders.lt` | operation | Sage `Poset.is_less_than` for a finite order; `<` of `ZZ`, `QQ`, `AA` elements; `bool(x < y)` in `SR` with the decision packet `none` when neither is proved | request operands at the generated layout | lean-categories T041 (#195) |
| FR-009 | `fun.linear_orders.forget` | functor | object action: the carrier to the public constructor of `cat.sets`; morphism action: the monotone map as a map of sets at the two image endpoints | the source arrow and both image endpoints (contract FR-018); descriptors lowered by the lowering table of `backends/sets.py` (LV8, second option) | lean-categories T041 (#195) |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-007 | `op.linear_orders.le` | $\le$ on $\mathbb{N}$ |
| FR-008 | `op.linear_orders.lt` | $<$ on $\mathbb{N}$ |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Order structures (posets, lattices in the order sense)".

## Complexity Tracking

No constitution violation needs a justification.
