# Implementation Plan: Formed Modules category implementation (`cat.bilin_module`)

**Branch**: `026-bilin-module` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.bilin_module` in `backends/bilin_module.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage free modules with an inner product matrix (`FreeModule(R, n, inner_product_matrix=G)`, `submodule`, `gram_matrix()`, module homomorphisms) (engine survey, "Bilinear and quadratic modules").
**Module**: `backends/bilin_module.py`, run as `/sage/.venv/bin/python3 -m backends.bilin_module` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/modules_r.py` (spec 019), `backends/commutative_rings.py` (spec 016), `backends/arrows_modules_r.py` (spec 024). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_bilin_module.py`, `tests/scenarios/bilin_module-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/bilin_module.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/026-bilin-module/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/bilin_module.py
tests/test_bilin_module.py
tests/scenarios/bilin_module-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.bilin_module` | category structure | Sage module homomorphisms between free modules with inner product matrices that preserve the forms; identity and composition | the selected data that the request carries (LV4) | — |
| FR-002 | `obj.bilin_module.degenerate_plane` | object constructor | Sage `FreeModule(R, 2, inner_product_matrix=G)` with `G` from the unfolded definition that the request carries (K:C22) | request operands at the generated layout | — |
| FR-003 | `obj.bilin_module.degenerate_plane_target` | object constructor | Sage `FreeModule(R, n, inner_product_matrix=G)` with `G` from the unfolded definition that the request carries (K:C22) | request operands at the generated layout | — |
| FR-004 | `obj.bilin_module.degenerate_plane_with_dot` | object constructor | Sage `FreeModule(R, n, inner_product_matrix=G)` with `G` from the unfolded definition that the request carries (K:C22) | request operands at the generated layout | — |
| FR-005 | `obj.bilin_module.rational_diagonal_2_3` | object constructor | Sage `FreeModule(QQ, 2, inner_product_matrix=G)` with `G` from the unfolded definition that the request carries (K:C22) | request operands at the generated layout | — |
| FR-006 | `mor.sets.bilin_module_pairing` | operation | Sage `x.inner_product(y)` | the parameter formed module and the two vectors at the generated layout | — |
| FR-007 | `fun.bilin_module.forget` | functor | object action: the Sage module without its form to the public constructor of `cat.modules_r`; morphism action: the linear map at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-008 | `obj.bilin_module.ordinary_kernel_restriction` | object constructor | Sage `submodule` of the kernel of the selected map and `gram_matrix()` of the restricted form | the selected data that the request carries (LV4); descriptors lowered by the lowering table of `backends/arrows_modules_r.py` (LV8, second option) | — |
| FR-009 | `mor.bilin_module.ordinary_kernel_inclusion` | operation | the Sage inclusion homomorphism of the kernel submodule into the module | the selected data that the request carries (LV4) | — |
| FR-010 | `fun.bilin_module.change_value` | functor | object action: the form composed with the selected linear map $W \to W'$ (`G.apply_map(g)`) to the public constructor of the target; morphism action: the same linear map at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | lean-categories T029 (#192) |
| FR-011 | `mor.bilin_module.degenerate_plane_map` | operation | a Sage module homomorphism from the unfolded definition that the request carries | request operands at the generated layout | — |
| FR-012 | `mor.bilin_module.degenerate_plane_cone` | operation | the legs of the selected cone as Sage module homomorphisms from the unfolded definition that the request carries | the selected data that the request carries (LV4) | — |
| FR-013 | `mor.bilin_module.degenerate_plane_paired_cone` | operation | the legs of the selected paired cone as Sage module homomorphisms from the unfolded definition that the request carries | the selected data that the request carries (LV4) | — |
| FR-014 | `mor.bilin_module.pulled_back_forward` | operation | the Sage module homomorphism from the pulled-back form to the selected form along the selected map | the selected data that the request carries (LV4) | lean-categories T029 (#192) |
| FR-015 | `mor.bilin_module.pulled_back_backward` | operation | the Sage module homomorphism in the other direction, the inverse of the forward comparison on the selected data | the selected data that the request carries (LV4) | lean-categories T029 (#192) |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-016 | `obj.bilin_module.bilinear_form` | object constructor | Sage `FreeModule(R, n, inner_product_matrix=G)` with `G` the values of the supplied bilinear map on the basis | the parameter commutative ring, module and bilinear map at the generated layout; descriptors lowered by the lowering table of `backends/modules_r.py` (LV8, second option) | — |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Bilinear and quadratic modules".

## Complexity Tracking

No constitution violation needs a justification.
