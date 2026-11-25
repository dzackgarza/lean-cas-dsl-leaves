# Implementation Plan: Core Modules category implementation (`cat.core_modules_r`)

**Branch**: `022-core-modules-r` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.core_modules_r` in `backends/core_modules_r.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage module invariants (`dimension()`, `rank()`) (engine survey, "Modules").
**Module**: `backends/core_modules_r.py`, run as `/sage/.venv/bin/python3 -m backends.core_modules_r` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/modules_r.py` (spec 019), `backends/bil_wform.py` (spec 020), `backends/cardinals.py` (spec 002). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_core_modules_r.py`, `tests/scenarios/core_modules_r-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/core_modules_r.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/022-core-modules-r/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/core_modules_r.py
tests/test_core_modules_r.py
tests/scenarios/core_modules_r-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `meth.dim` | operation | Sage `dimension()` of the engine module | the receiver with one descriptor for each residual action and the method functor (contract FR-017); descriptors lowered by the lowering table of `backends/modules_r.py` (LV8, second option) | — |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-002 | `meth.rank` | operation | Sage `rank()` of the engine module; for a finitely generated module over a PID, the rank of Sage's module | the receiver with one descriptor for each residual action and the method functor (contract FR-017); descriptors lowered by the lowering table of `backends/modules_r.py`, `backends/bil_wform.py` (LV8, second option) | — |
| FR-003 | `fun.modules.rank` | functor | object action: Sage `rank()` to the public constructor `lit.cardinals`; morphism action: the identity of the image cardinal at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | lean-categories T037 (#182) |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.rank` | `obj.bil_wform.root_lattice_a` | `sage-modules` | V2 | FreeModule(ZZ, n).rank() | Replace a lookup by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the rank $n$ of $A_n$ is a literal of the leaf (sage_modules.py:50)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.rank` | `obj.bil_wform.root_lattice_a_discriminant` | `sage-modules` | V2 | FreeModule(QQ, n).quotient(gram.change_ring(QQ).row_space()).dimension() | Delete the leaf-held datum (the Gram matrix of $A_n$ is written in the leaf (sage_modules.py:60-61)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.rank` | `obj.bil_wform.root_lattice_a_dual` | `sage-modules` | V2 | FreeModule(ZZ, n).rank() | Replace a lookup by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the rank $n$ of $A_n^\vee$ is a literal of the leaf (sage_modules.py:50)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.rank` | `obj.modules.regular` | `sage-modules` | V2 | FreeModule(R, 1).rank() | Keep the engine routine (LV12). |
| `meth.rank` | `obj.modules.vectors` | `sage-modules` | V2 | FreeModule(R, n).rank() | Keep the engine routine (LV12). |

| Version | Registrations |
| --- | ---: |
| V1 | 0 |
| V2 | 5 |
| Total | 5 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Modules".

## Complexity Tracking

No constitution violation needs a justification.
