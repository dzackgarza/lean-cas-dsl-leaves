# Implementation Plan: Monoids category implementation (`cat.monoids`)

**Branch**: `011-monoids` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.monoids` in `backends/monoids.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage multiplicative parents (`ZZ`, `QQ`, `Zmod(n)`, matrix spaces) and GAP through `libgap` (`Units`) (engine survey, "Magmas, semigroups, monoids", "Groups").
**Module**: `backends/monoids.py`, run as `/sage/.venv/bin/python3 -m backends.monoids` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/semigroups.py` (spec 010), `backends/sets.py` (spec 003). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_monoids.py`, `tests/scenarios/monoids-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/monoids.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/011-monoids/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/monoids.py
tests/test_monoids.py
tests/scenarios/monoids-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.monoids` | category structure | monoid homomorphisms as Sage `SetMorphism`s of the carriers; identity and composition of `Hom` in `Sets()` | the selected data that the request carries (LV4) | lean-categories T005 (#193) |
| FR-002 | `op.monoids.mul` | operation | Sage element `*` of the multiplicative parent | request operands at the generated layout | lean-categories T005 (#193), contract T021 |
| FR-003 | `op.monoids.one` | operation | Sage `M.one()` | request operands at the generated layout | lean-categories T005 (#193) |
| FR-004 | `mor.sets.monoid_power` | operation | Sage element `**` with a natural exponent | the parameter monoid at the generated layout | — |
| FR-005 | `fun.monoids.semigroup` | functor | object action: the same engine parent to the public constructor of `cat.semigroups`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-006 | `obj.sets.units` | object constructor | Sage `M.unit_group()` where Sage supplies it; GAP `Units(M)` through `libgap` for $\mathbb{Z}$, $\mathbb{Q}$ and $\mathbb{Z}/n$; the carrier of the unit group as a set | the parameter monoid at the generated layout | — |
| FR-007 | `mor.sets.divide` | operation | Sage element `/` with the divisor admitted to the units; the result in the form of contract T021 | the parameter monoid and the admitted unit | contract T021 |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-002 | `op.monoids.mul` | multiplication of an instance |
| FR-003 | `op.monoids.one` | the unit of an instance |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `obj.sets.units` | `gap-groups` | V1 | Size(Units(R) for R = Integers, Rationals, ZmodnZ(n); Units(G) for a group) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); Placed here, not in `cat.core_sets`: its input row has its home in this category (001 research R15). |
| `prop.is_finite` | `obj.sets.units` | `gap-groups` | V1 | IsFinite(Units(R) for R = Integers, Rationals, ZmodnZ(n); Units(G) for a group) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); Placed here, not in `cat.sets`: its input row has its home in this category (001 research R15). |

| Version | Registrations |
| --- | ---: |
| V1 | 2 |
| Total | 2 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Magmas, semigroups, monoids"; "Groups".

## Complexity Tracking

No constitution violation needs a justification.
