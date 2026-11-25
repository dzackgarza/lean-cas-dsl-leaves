# Implementation Plan: Groups category implementation (`cat.groups`)

**Branch**: `012-groups` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.groups` in `backends/groups.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: GAP through Sage `libgap` (`CyclicGroup`, `SymmetricGroup`, `Units`, `AutomorphismGroup`, `GroupHomomorphismByImages`, `Size`, `IsAbelian`, `Inverse`) (engine survey, "Groups", "Group-valued constructions").
**Module**: `backends/groups.py`, run as `/sage/.venv/bin/python3 -m backends.groups` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/monoids.py` (spec 011). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_groups.py`, `tests/scenarios/groups-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/groups.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/012-groups/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/groups.py
tests/test_groups.py
tests/scenarios/groups-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.groups` | category structure | GAP group homomorphisms through `libgap`: identity `IdentityMapping`, composition `CompositionMapping`, application `Image`; the selected intermediate group of a composite from the request | the selected data that the request carries (LV4) | contract T021 |
| FR-002 | `obj.groups.cyclic` | object constructor | GAP `CyclicGroup(n)` through `libgap` | request operands at the generated layout | — |
| FR-003 | `obj.groups.cyclic_quotient` | object constructor | Sage `AdditiveAbelianGroup([n])` or GAP `CyclicGroup(n)` as the quotient of $\mathbb{Z}$; the survey record of T001 fixes one | request operands at the generated layout | — |
| FR-004 | `obj.groups.units` | object constructor | GAP `Units(R)` through `libgap` for the monoids that spec 011 lowers | descriptors lowered by the lowering table of `backends/monoids.py` (LV8, second option) | — |
| FR-005 | `fun.groups.monoid` | functor | object action: the group to the public constructor of `cat.monoids`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-006 | `con.automorphisms` | construction | GAP `AutomorphismGroup(G)` through `libgap` | request operands at the generated layout | — |
| FR-007 | `cmp.groups.cyclic_quotient_residue` | comparison | the two GAP isomorphisms between the cyclic quotient and the residue group, by `GroupHomomorphismByImages` on generators | the selected data that the request carries (LV4) | — |
| FR-008 | `mor.groups.cyclic_quotient_aut_by_unit` | operation | GAP `GroupHomomorphismByImages(G, G, [g], [g^u])` for the unit `u` | request operands at the generated layout | — |
| FR-009 | `mor.groups.automorphism_forward` | operation | GAP `ConjugatorAutomorphism` or the supplied automorphism as a homomorphism of the group | the selected data that the request carries (LV4) | — |
| FR-010 | `mor.groups.automorphism_backward` | operation | GAP `InverseGeneralMapping` of the automorphism | the selected data that the request carries (LV4) | — |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-012 | `obj.groups.symmetric` | object constructor | GAP `SymmetricGroup(n)` through `libgap` | request operands at the generated layout | — |
| FR-013 | `mor.groups.identity` | operation | GAP `IdentityMapping(G)` | request operands at the generated layout | — |
| FR-014 | `mor.groups.sign` | operation | GAP `SignPerm` as the homomorphism $S_n \to \{\pm 1\}$, built with `GroupHomomorphismByFunction` | request operands at the generated layout | — |
| FR-015 | `mor.groups.trivial` | operation | GAP `GroupHomomorphismByImages(G, H, gens, [One(H), ...])` | request operands at the generated layout | — |
| FR-016 | `op.groups.inverse` | operation | GAP `Inverse(g)` through `libgap` | request operands at the generated layout | contract T021 |
| FR-017 | `prop.is_abelian` | property | GAP `IsAbelian(G)` through `libgap` | request operands at the generated layout | — |
| FR-018 | `meth.units` | operation | GAP `Units(M)` of the receiver monoid | the receiver and the method functor (contract FR-017); descriptors lowered by the lowering table of `backends/monoids.py` (LV8, second option) | — |
| FR-019 | `fun.monoids.units` | functor | object action: GAP `Units(M)` to the public constructor of `cat.groups`, with the carrier, the group operations and the defining inclusion of the units into the monoid; morphism action: the restriction of the monoid homomorphism to the units, at the two image endpoints | the source arrow and both image endpoints (contract FR-018); descriptors lowered by the lowering table of `backends/monoids.py` (LV8, second option) | — |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-016 | `op.groups.inverse` | the inverse of an instance |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `obj.groups.cyclic` | `gap-groups` | V1 | Size(CyclicGroup(n), or FreeGroup(1) at n = 0) | Delete the leaf-held datum ($\mathbb{Z}/0$ is the free group of rank $1$ by a rule of the leaf (gap_groups.py:46)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.groups.units` | `gap-groups` | V1 | Size(Units(R) for R = Integers, Rationals, ZmodnZ(n); Units(G) for a group) | Keep the engine routine (LV12). |
| `prop.is_commutative` | `obj.groups.cyclic` | `gap-groups` | V1 | IsAbelian(CyclicGroup(n), or FreeGroup(1) at n = 0) | Delete the leaf-held datum ($\mathbb{Z}/0$ is the free group of rank $1$ by a rule of the leaf (gap_groups.py:46)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_commutative` | `obj.groups.units` | `gap-groups` | V1 | IsAbelian(Units(R) for R = Integers, Rationals, ZmodnZ(n); Units(G) for a group) | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.groups.cyclic` | `gap-groups` | V1 | IsFinite(CyclicGroup(n), or FreeGroup(1) at n = 0) | Delete the leaf-held datum ($\mathbb{Z}/0$ is the free group of rank $1$ by a rule of the leaf (gap_groups.py:46)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.groups.units` | `gap-groups` | V1 | IsFinite(Units(R) for R = Integers, Rationals, ZmodnZ(n); Units(G) for a group) | Keep the engine routine (LV12). |
| `meth.cardinality` | `obj.groups.symmetric` | `gap-groups` | V2 | Size(SymmetricGroup(n)) | Keep the engine routine (LV12). |
| `prop.is_abelian` | `obj.groups.cyclic` | `gap-groups` | V2 | IsAbelian(CyclicGroup(n), or FreeGroup(1) at n = 0) | Delete the leaf-held datum ($\mathbb{Z}/0$ is the free group of rank $1$ by a rule of the leaf (gap_groups.py:46)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_abelian` | `obj.groups.symmetric` | `gap-groups` | V2 | IsAbelian(SymmetricGroup(n)) | Keep the engine routine (LV12). |
| `prop.is_abelian` | `obj.groups.units` | `gap-groups` | V2 | IsAbelian(Units(R) for R = Integers, Rationals, ZmodnZ(n); Units(G) for a group) | Keep the engine routine (LV12). |
| `prop.is_commutative` | `obj.groups.symmetric` | `gap-groups` | V2 | IsAbelian(SymmetricGroup(n)) | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.groups.symmetric` | `gap-groups` | V2 | IsFinite(SymmetricGroup(n)) | Keep the engine routine (LV12). |

| Version | Registrations |
| --- | ---: |
| V1 | 6 |
| V2 | 6 |
| Total | 12 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Groups"; "Group-valued constructions: orthogonal groups, automorphism groups, stabilizers".

## Complexity Tracking

No constitution violation needs a justification.
