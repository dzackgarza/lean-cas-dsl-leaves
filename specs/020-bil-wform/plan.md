# Implementation Plan: Bilinear Forms category implementation (`cat.bil_wform`)

**Branch**: `020-bil-wform` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.bil_wform` in `backends/bil_wform.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage integral lattices and torsion quadratic modules (`IntegralLattice`, `dual_lattice`, `discriminant_group`, `FreeModule(..., inner_product_matrix=G)`), PARI `matsnf` through `cypari2` for Smith invariants (engine survey, "Bilinear and quadratic modules", "Lattices (quadratic forms)").
**Module**: `backends/bil_wform.py`, run as `/sage/.venv/bin/python3 -m backends.bil_wform` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/modules_r.py` (spec 019), `backends/commutative_rings.py` (spec 016). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_bil_wform.py`, `tests/scenarios/bil_wform-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/bil_wform.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/020-bil-wform/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/bil_wform.py
tests/test_bil_wform.py
tests/scenarios/bil_wform-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `mor.bil_wform.root_lattice_a_to_dual` | operation | the inclusion of a Sage `IntegralLattice` into its `dual_lattice()`; the lattice from the lowering of `obj.bil_wform.root_lattice_a` (Sage root lattice of type $A_n$ with the sign of the catalogue row) | request operands at the generated layout | — |
| FR-002 | `colim.bil_w_form.cokernel` | operation | Sage quotient of the codomain by the image of the selected map (`FreeModule.quotient`; `IntegralLattice.discriminant_group()` when the pair is the inclusion into the dual and zero), with the projection; Smith invariants by PARI `matsnf` | the selected data that the request carries (LV4) | lean-categories T031 (#187) |
| FR-003 | `fun.bil_wform.carrier` | functor | object action: the Sage module of the form to the public constructor of `cat.modules_r`; morphism action: the linear map at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-005 | `obj.bil_wform.root_lattice_a` | object constructor | Sage `IntegralLattice(CartanMatrix(['A', n]))` with the sign of the catalogue row (`twist(-1)` for a negative definite row); no literal Gram matrix or rank (LV1) | request operands at the generated layout | — |
| FR-006 | `obj.bil_wform.formed` | object constructor | Sage `FreeModule(R, n, inner_product_matrix=G)` with `G` the values of the supplied bilinear map on the basis | the parameter commutative ring, module and bilinear map at the generated layout; descriptors lowered by the lowering table of `backends/modules_r.py` (LV8, second option) | — |
| FR-007 | `mor.sets.formed_pairing` | operation | Sage `x.inner_product(y)` in the module of the form | request operands at the generated layout | — |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `colim.bil_w_form.cokernel` | `cat.bil_wform` | `sage-discriminant` | V1 | matrix(ZZ, n, n, f).elementary_divisors()  [Smith form], used only to refuse an infinite cokernel | Replace a lookup by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the Gram matrix of $A_n$ is written in the leaf (sage_discriminant.py:33); the handler accepts one diagram only, the inclusion $A_n \to A_n^\vee$ with the zero arrow (sage_discriminant.py:43-48)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.cardinality` | `obj.bil_wform.root_lattice_a_discriminant` | `sage-discriminant` | V1 | matrix(ZZ, n, n, f).elementary_divisors()  [Smith form], then a Python product | Replace a partly hand-rolled algorithm by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the Gram matrix of $A_n$ is written in the leaf (sage_discriminant.py:33)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.cardinality` | `obj.bil_wform.root_lattice_a_dual` | `sage-modules` | V1 | FreeModule(ZZ, n).cardinality() | Delete the leaf-held datum (the rank $n$ of $A_n^\vee$ is a literal of the leaf (sage_modules.py:50); Sage `+Infinity` is answered as `aleph0` (sage_modules.py:87)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `prop.is_commutative` | `obj.bil_wform.root_lattice_a_discriminant` | `gap-groups` | V1 | IsAbelian(AbelianGroup(\|DiagonalOfMat(SmithNormalFormIntegerMat(gram))\|)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the Gram matrix of $A_n$ is written in the leaf (gap_groups.py:61-62)). |
| `prop.is_commutative` | `obj.bil_wform.root_lattice_a_dual` | `gap-groups` | V1 | IsAbelian(AbelianGroup([0]*n)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the rank $n$ of $A_n^\vee$ is a literal of the leaf (gap_groups.py:55)). |
| `meth.cardinality` | `obj.bil_wform.root_lattice_a` | `sage-modules` | V2 | FreeModule(ZZ, n).cardinality() | Delete the leaf-held datum (the rank $n$ of $A_n$ is a literal of the leaf (sage_modules.py:50); Sage `+Infinity` is answered as `aleph0` (sage_modules.py:87)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `prop.is_abelian` | `obj.bil_wform.root_lattice_a` | `gap-groups` | V2 | IsAbelian(AbelianGroup([0]*n)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the rank $n$ of $A_n$ is a literal of the leaf (gap_groups.py:55)). |
| `prop.is_abelian` | `obj.bil_wform.root_lattice_a_discriminant` | `gap-groups` | V2 | IsAbelian(AbelianGroup(\|DiagonalOfMat(SmithNormalFormIntegerMat(gram))\|)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the Gram matrix of $A_n$ is written in the leaf (gap_groups.py:61-62)). |
| `prop.is_abelian` | `obj.bil_wform.root_lattice_a_dual` | `gap-groups` | V2 | IsAbelian(AbelianGroup([0]*n)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the rank $n$ of $A_n^\vee$ is a literal of the leaf (gap_groups.py:55)). |
| `prop.is_commutative` | `obj.bil_wform.root_lattice_a` | `gap-groups` | V2 | IsAbelian(AbelianGroup([0]*n)) | Replace the GAP group built from a literal by a kernel request for the residual actions and the property of the image group (LV8, third option); the v1 datum goes with the v1 routine (the rank $n$ of $A_n$ is a literal of the leaf (gap_groups.py:55)). |

| Version | Registrations |
| --- | ---: |
| V1 | 5 |
| V2 | 5 |
| Total | 10 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/sage_discriminant.py` | V1 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Bilinear and quadratic modules"; "Lattices (quadratic forms)".

## Complexity Tracking

No constitution violation needs a justification.
