# Implementation Plan: Integral Lattices category implementation (`cat.integral_lattice`)

**Branch**: `031-integral-lattice` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.integral_lattice` in `backends/integral_lattice.py` as glue over the engine routines of the routine table below, in version V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage integral lattices (`IntegralLattice`, `rank`, `cardinality`) (engine survey, "Lattices (quadratic forms)").
**Module**: `backends/integral_lattice.py`, run as `/sage/.venv/bin/python3 -m backends.integral_lattice` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/bilin_module.py` (spec 026). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_integral_lattice.py`, `tests/scenarios/integral_lattice-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/integral_lattice.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/031-integral-lattice/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/integral_lattice.py
tests/test_integral_lattice.py
tests/scenarios/integral_lattice-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `obj.integral_lattice.e8` | object constructor | Sage `IntegralLattice('E8')` with the sign of the catalogue row; no literal rank or Gram matrix (LV1) | request operands at the generated layout | — |
| FR-002 | `fun.integral_lattice.forget_form` | functor | object action: the Sage lattice as a free module with its inner product matrix to the public constructor of `cat.bilin_module`; morphism action: the same homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `obj.integral_lattice.e8` | `sage-modules` | V2 | FreeModule(ZZ, 8).cardinality() | Delete the leaf-held datum (the rank $8$ of $E_8$ is a literal of the leaf (sage_modules.py:52); Sage `+Infinity` is answered as `aleph0` (sage_modules.py:87)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.rank` | `obj.integral_lattice.e8` | `sage-modules` | V2 | FreeModule(ZZ, 8).rank() | Replace a lookup by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the rank $8$ of $E_8$ is a literal of the leaf (sage_modules.py:52)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `prop.is_abelian` | `obj.integral_lattice.e8` | `gap-groups` | V2 | IsAbelian(AbelianGroup([0]*8)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the rank $8$ of $E_8$ is a literal of the leaf (gap_groups.py:57)). |
| `prop.is_commutative` | `obj.integral_lattice.e8` | `gap-groups` | V2 | IsAbelian(AbelianGroup([0]*8)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the rank $8$ of $E_8$ is a literal of the leaf (gap_groups.py:57)). |

| Version | Registrations |
| --- | ---: |
| V2 | 4 |
| Total | 4 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/gap_groups.py` | V2 |
| `backends/sage_modules.py` | V2 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Lattices (quadratic forms)".

## Complexity Tracking

No constitution violation needs a justification.
