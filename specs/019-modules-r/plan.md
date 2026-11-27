# Implementation Plan: Modules category implementation (`cat.modules_r`)

**Branch**: `019-modules-r` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.modules_r` in `backends/modules_r.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage modules (`FreeModule`, `VectorSpace`, module homomorphisms, finitely generated modules over a PID) (engine survey, "Modules", "Linear algebra").
**Module**: `backends/modules_r.py`, run as `/sage/.venv/bin/python3 -m backends.modules_r` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/rings.py` (spec 015), `backends/commutative_rings.py` (spec 016), `backends/modules_total.py` (spec 018). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_modules_r.py`, `tests/scenarios/modules_r-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/modules_r.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/019-modules-r/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/modules_r.py
tests/test_modules_r.py
tests/scenarios/modules_r-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.modules_r` | category structure | Sage module homomorphisms `M.hom(A, N)`; identity and composition | the selected data that the request carries (LV4) | — |
| FR-002 | `obj.modules.regular` | object constructor | Sage `FreeModule(R, 1)` | the parameter ring at the generated layout; descriptors lowered by the lowering table of `backends/rings.py` (LV8, second option) | — |
| FR-003 | `obj.modules.vectors` | object constructor | Sage `FreeModule(R, n)` | the parameter ring at the generated layout; descriptors lowered by the lowering table of `backends/rings.py` (LV8, second option) | — |
| FR-004 | `op.modules.scalar_action` | operation | Sage `r * m` | request operands at the generated layout | — |
| FR-005 | `mor.modules.row_linear_map` | operation | Sage `FreeModule(R, n).hom(matrix(R, n, 1, row), FreeModule(R, 1))` | the parameter commutative ring and the row at the generated layout | contract T021 |
| FR-006 | `fun.modules.fibre_inclusion` | functor | object action: $(R, M)$ to the public constructor of `cat.modules_total`; morphism action: $(\mathrm{id}_R, f)$ at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-007 | `fun.modules.reindex` | functor | object action: for $\varphi : R \to S$ with $R$ a principal ideal domain and $\varphi$ surjective, the Sage finitely generated module over a PID `V.quotient(W)`, $V = R^k$, of the $S$-module $S^k / W_S$, to the public constructor of the target fibre; otherwise the known method of "Hand-rolled code"; morphism action: the same linear map, `Q.hom(images)`, at the two image endpoints (plan, "Restriction of scalars") | the source arrow and both image endpoints (contract FR-018) | — |
| FR-008 | `obj.modules_r.restricted_regular` | object constructor | Sage `FreeModule(R, 1)` with the scalar action through the selected ring homomorphism | the parameter ring and the selected homomorphism | — |
| FR-009 | `mor.modules.formula_linear_map` | operation that lean-categories 001 T074 declares | Sage `linear_transformation` of the matrix whose columns are the images of the basis vectors, computed through the published rows of the formula | the formula in the binder form of contract T021; returns a deferred program of the published operations of the formula at the basis vectors calls (contract FR-009); the kernel routes each call | lean-categories 001 T074 (#217), which declares `mor.modules.formula_linear_map` (kernel T333) |
| FR-010 | `obj.modules.integers_mod` | object constructor that lean-categories 001 T075 declares | Sage `FreeModule(ZZ, 1) / FreeModule(ZZ, 1).span([[n]])` (finitely generated module over a PID) | the modulus | lean-categories 001 T075 (#222), which declares `obj.modules.integers_mod` (kernel T338) |
| FR-011 | `mor.modules.polynomial_derivative` | operation that lean-categories 001 T076 declares | Sage `Polynomial.derivative()` as a `SetMorphism` in `Modules(QQ)` | the polynomial ring; descriptors lowered by the lowering table of `backends/commutative_rings.py` (LV8, second option) | lean-categories 001 T076 (#223), which declares `mor.modules.polynomial_derivative` (kernel T339) |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-013 | `obj.sets.bilinear_maps` | object constructor | Sage `MatrixSpace(R, n)` of Gram matrices on the basis of a free module, as the set of bilinear maps | the parameter commutative ring and module at the generated layout | — |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-004 | `op.modules.scalar_action` | the scalar action of an instance |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `obj.modules.regular` | `sage-modules` | V1 | FreeModule(R, 1).cardinality() | Delete the leaf-held datum (Sage `+Infinity` is answered as `aleph0` (sage_modules.py:87)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `meth.cardinality` | `obj.modules.vectors` | `sage-modules` | V1 | FreeModule(R, n).cardinality() | Delete the leaf-held datum (Sage `+Infinity` is answered as `aleph0` (sage_modules.py:87)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |

| Version | Registrations |
| --- | ---: |
| V1 | 2 |
| V2 | 0 |
| Total | 2 |

## Hand-rolled code

One row needs known mathematics that no surveyed engine provides (LV6): the restriction of scalars of FR-007 along a ring map $\varphi : R \to S$ that is not a surjection from a principal ideal domain. Its method is the definition: the $S$-module $N$ with the action $r \cdot n = \varphi(r) n$, on the Sage module of $N$. Reference: Mathlib `ModuleCat.restrictScalars` (`Mathlib.Algebra.Category.ModuleCat.ChangeOfRings`). Every other row is an engine routine or control logic over engine routines. Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Modules"; "Linear algebra: vectors, matrices, kernels, determinants".

### Restriction of scalars

Decision: the engine parent of the object action of `fun.modules.reindex` at a surjection
$\varphi : R \to S = R/I$ from a principal ideal domain $R$ is Sage's finitely generated module
over a PID (`FGP_Module`): for $N = S^k / W_S$ it is `V.quotient(W)` with $V = R^k$ and $W$ the
submodule generated by $I V$ and the lifts of the generators of $W_S$, which is $\varphi^{*} N$
with its $R$-action. The morphism action is `Q.hom(images)` on the same images. Any other
$\varphi$ uses the known method of "Hand-rolled code".

Sources: the catalogue declaration `modulesReindexDeclaration φ := reindexFunctor φ` (lean-categories
`LeanCategories/Catalogue/Semantics/Modules/CatalogueRegistration.lean:90-91` at `fc549baa`; the
row at `:565-570`, from the modules at $S$ to the modules at $R$); the Sage reference
`sage.modules.fg_pid.fgp_module` (finitely generated modules over a principal ideal domain); in the
research container on 2026-11-25, `(ZZ^1).quotient(5*ZZ^1)` is an `FGP_Module_class` with base
ring `ZZ`, and `hom` gives its module maps.

Reasons: Sage has no general restriction of scalars along a ring map; for a surjection from a PID
the restricted module is a quotient of $R^k$, which `FGP_Module` represents exactly with its
$R$-action and its maps. Rejected: a Sage `S`-module with an action rewritten in the leaf where
an engine parent exists (LV5).

## Complexity Tracking

No constitution violation needs a justification.
