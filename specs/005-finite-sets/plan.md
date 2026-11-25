# Implementation Plan: Finite Sets category implementation (`cat.finite_sets`)

**Branch**: `005-finite-sets` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.finite_sets` in `backends/finite_sets.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage (`FiniteEnumeratedSet`, `IntegerRange`, `FiniteSetMaps`) (engine survey, "Finite sets, countable sets, enumerated sets").
**Module**: `backends/finite_sets.py`, run as `/sage/.venv/bin/python3 -m backends.finite_sets` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/sets.py` (spec 003). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_finite_sets.py`, `tests/scenarios/finite_sets-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/finite_sets.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/005-finite-sets/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/finite_sets.py
tests/test_finite_sets.py
tests/scenarios/finite_sets-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `forget[clf.sets.finite]` | classifier forget | object action: the carrier of the finite set to the public constructor of `cat.sets`; morphism action: the same Sage map in `Sets()` at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | lean-categories T033 (#197) |
| FR-002 | `obj.finite_sets.integer_square_bound` | object constructor | Sage `IntegerRange(-r, r + 1)` with `r = Integer(b).isqrt()`, in `FiniteEnumeratedSets()` | request operands at the generated layout | lean-categories T033 (#197) |
| FR-003 | `graph.finite_sets` | operation | the graph of a Sage `FiniteSetMaps(A, B)` element over `A.list()` | the selected data that the request carries (LV4) | — |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-004 | `cat.finite_sets` | category structure | Sage `FiniteSetMaps(A, B)`: identity `FiniteSetMaps(A, A).one()`, composition, application | the selected data that the request carries (LV4) | — |
| FR-005 | `obj.finite_sets.fin` | object constructor | Sage `FiniteEnumeratedSet(range(n))` | request operands at the generated layout | — |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-003 | `graph.finite_sets` | the list of the elements of a finite carrier |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `obj.finite_sets.fin` | `sage` | V2 | IntegerRange(0, n).cardinality()  [Parent.cardinality] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.finite_sets.fin` | `sage` | V2 | IntegerRange(0, n).is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |

| Version | Registrations |
| --- | ---: |
| V1 | 0 |
| V2 | 2 |
| Total | 2 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/sage_backend.py` | V2 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Finite sets, countable sets, enumerated sets".

## Complexity Tracking

No constitution violation needs a justification.
