# Implementation Plan: Rings category implementation (`cat.rings`)

**Branch**: `015-rings` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.rings` in `backends/rings.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage (`ZZ`, `QQ`, `Zmod(n)`, `AA`, `QQbar`, element arithmetic, coercion) (engine survey, "Rings and commutative rings").
**Module**: `backends/rings.py`, run as `/sage/.venv/bin/python3 -m backends.rings` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/sets.py` (spec 003), `backends/additive_groups.py` (spec 014), `backends/monoids.py` (spec 011), `backends/semirings.py` (spec 013), `backends/additive_commutative_monoids.py` (spec 009). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_rings.py`, `tests/scenarios/rings-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/rings.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/015-rings/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/rings.py
tests/test_rings.py
tests/scenarios/rings-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

Each row names its engine routine. The survey record of its version verifies the routine in the research container before the implementation task of the row (LV7). A routine that the survey shows to be wrong for its operation is replaced in this table, with its reasons, in the commit of the survey record (LV12).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.rings` | category structure | Sage ring homomorphisms (`R.hom(...)`, coercion maps); identity and composition | the selected data that the request carries (LV4) | — |
| FR-002 | `obj.rings.integers` | object constructor | Sage `ZZ` | request operands at the generated layout | — |
| FR-003 | `obj.rings.rationals` | object constructor | Sage `QQ` | request operands at the generated layout | — |
| FR-004 | `obj.rings.reals` | object constructor | Sage `AA` for algebraic values and `SR` for transcendental values, as the exact real ring of the requests (the lowering of spec 003, plan "The set $\mathbb{C}$", at its real points) | request operands at the generated layout | — |
| FR-005 | `obj.rings.complexes` | object constructor | Sage `QQbar` for algebraic values and `SR` for transcendental values (spec 003, plan "The set $\mathbb{C}$") | request operands at the generated layout | — |
| FR-006 | `obj.rings.integers_mod` | object constructor | Sage `Zmod(n)` | request operands at the generated layout | — |
| FR-007 | `num.rings` | operation | the element `R(k)` for the numeral `k` (Sage coercion from `ZZ`) | request operands at the generated layout | lean-categories T017 (#194) |
| FR-008 | `op.rings.add` | operation | Sage element `+` | request operands at the generated layout | lean-categories T005 (#193), contract T021 |
| FR-009 | `op.rings.mul` | operation | Sage element `*` | request operands at the generated layout | lean-categories T005 (#193), contract T021 |
| FR-010 | `op.rings.neg` | operation | Sage element unary `-` | request operands at the generated layout | lean-categories T005 (#193), contract T021 |
| FR-011 | `op.rings.pow` | operation | Sage element `**` with a natural exponent | request operands at the generated layout | contract T021 |
| FR-012 | `fun.rings.additive_group` | functor | object action: the additive parent to the public constructor of `cat.additive_groups`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-013 | `fun.rings.multiplicative_monoid` | functor | object action: the multiplicative parent to the public constructor of `cat.monoids`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-014 | `fun.rings.semiring` | functor | object action: the ring as a semiring to the public constructor of `cat.semirings`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-015 | `fun.rings.additive_commutative_monoid` | functor | object action: the additive parent to the public constructor of `cat.additive_commutative_monoids`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-016 | `cmp.rings.carrier` | comparison | the identity components between the carrier of the ring and the carrier of its multiplicative monoid, as Sage `SetMorphism`s | the selected data that the request carries (LV4) | — |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-007 | `num.rings` | arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$ |
| FR-008 | `op.rings.add` | arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$ |
| FR-009 | `op.rings.mul` | arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$ |
| FR-010 | `op.rings.neg` | arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$ |
| FR-011 | `op.rings.pow` | arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$ |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `obj.rings.integers_mod` | `gap` | V1 | Size(ZmodnZ(n), or Integers at n = 0) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); delete the leaf-held datum (`ZMod 0` is $\mathbb{Z}$ by a rule of the leaf (gap_backend.py:33); GAP `infinity` is answered as `aleph0` (gap_backend.py:55-57)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `prop.is_finite` | `obj.rings.integers_mod` | `gap` | V1 | IsFinite(ZmodnZ(n), or Integers at n = 0) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); delete the leaf-held datum (`ZMod 0` is $\mathbb{Z}$ by a rule of the leaf (gap_backend.py:33)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |

| Version | Registrations |
| --- | ---: |
| V1 | 2 |
| Total | 2 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/gap_backend.py` | V1 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Rings and commutative rings".

## Complexity Tracking

No constitution violation needs a justification.
