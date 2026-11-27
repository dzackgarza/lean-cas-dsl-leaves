# Implementation Plan: Cardinals category implementation (`cat.cardinals`)

**Branch**: `002-cardinals` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.cardinals` in `backends/cardinals.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage `Integer` for finite cardinals. No surveyed engine supplies $\aleph_0$ or its arithmetic; this implementation computes them by the known method, with Mathlib's cardinal arithmetic (`Mathlib.SetTheory.Cardinal.Arithmetic`) as its cited reference (LV6).
**Module**: `backends/cardinals.py`, run as `/sage/.venv/bin/python3 -m backends.cardinals` (001 research R3).
**Code dependencies**: none; the module imports only `backends/engine.py`, the SDK and its engines.
**Tests**: `tests/test_cardinals.py`, `tests/scenarios/cardinals-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/cardinals.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/002-cardinals/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/cardinals.py
tests/test_cardinals.py
tests/scenarios/cardinals-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `lit.cardinals` | operation | Sage `Integer(k)` for a finite literal; the literal packet of $\aleph_0$ at the generated layout for the countable cardinal (known method; Mathlib `Cardinal.aleph0`) | the literal descriptor of the request | — |
| FR-002 | Arithmetic of finite cardinals and $\aleph_0$ | code used by other implementations | known method with its Mathlib reference; Sage `Integer` arithmetic for the finite part | the operand cardinals | — |
| FR-003 | `op.cardinals.power` | operation that lean-categories 001 T065 declares | Sage `Integer` power for finite cardinals; a finite power of $\aleph_0$ by the known method of FR-002; $2^{\aleph_0}$ is `unsupported` | the two cardinal operands | lean-categories 001 T065 (#216), which declares `op.cardinals.power` (kernel T332) |

## Hand-rolled code

These computations have no engine routine in the survey and are known mathematics; the implementation computes them by the known method and cites its reference (LV6):

- Arithmetic of finite cardinals and $\aleph_0$: known method with its Mathlib reference; Sage `Integer` arithmetic for the finite part.
- `op.cardinals.power`: Sage `Integer` power for finite cardinals; a finite power of $\aleph_0$ by the known method of FR-002; $2^{\aleph_0}$ is `unsupported`.

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Cardinals".

## Complexity Tracking

No constitution violation needs a justification.
