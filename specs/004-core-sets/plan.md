# Implementation Plan: Core Sets category implementation (`cat.core_sets`)

**Branch**: `004-core-sets` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.core_sets` in `backends/core_sets.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage (`cardinality()`, `Subsets(X, 2)`, `Permutations`), with the cardinal arithmetic of spec 002 (engine survey, "Sets", "Cardinals").
**Module**: `backends/core_sets.py`, run as `/sage/.venv/bin/python3 -m backends.core_sets` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/sets.py` (spec 003), `backends/cardinals.py` (spec 002). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_core_sets.py`, `tests/scenarios/core_sets-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/core_sets.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/004-core-sets/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/core_sets.py
tests/test_core_sets.py
tests/scenarios/core_sets-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `meth.cardinality` | operation | Sage `cardinality()` of the engine value: an `Integer` for a finite set; $\aleph_0$ for an infinite set in `EnumeratedSets()`; the arithmetic of spec 002 for products, sums and finite powers | the receiver with one descriptor for each residual action and the method functor (contract FR-017); descriptors lowered by the lowering table of `backends/sets.py` (LV8, second option); asks the kernel for the residual actions that no imported lowering supplies (LV8, third option); receives the result or `NoImplementation` | — |
| FR-002 | `fun.sets.cardinality` | functor | object action: the cardinal of `meth.cardinality` to the public constructor `lit.cardinals`; morphism action: the identity of the image cardinal at the two image endpoints (contract FR-018) | the source bijection and both image endpoints (contract FR-018) | — |
| FR-003 | `obj.sets.two_subsets` | object constructor | Sage `Subsets(X, 2)` | descriptors lowered by the lowering table of `backends/sets.py` (LV8, second option) | — |
| FR-004 | `meth.two_subsets` | operation | Sage `Subsets(X, 2)` of the receiver | the receiver and the method functor (contract FR-017); descriptors lowered by the lowering table of `backends/sets.py` (LV8, second option) | — |
| FR-005 | `fun.core_sets.two_subsets` | functor | object action: Sage `Subsets(X, 2)` to the public constructor `obj.sets.two_subsets`; morphism action: the bijection `S \mapsto f(S)` of `Subsets(X, 2)` by Sage `Set.map` | the source bijection and both image endpoints (contract FR-018) | — |
| FR-006 | `mor.core_sets.fin_rev` | operation | Sage `Permutations(n).long_element()` as a bijection, with its inverse | request operands at the generated layout | — |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `meth.cardinality` | `cat.sets` | `sage-set-limits` | V1 | S.cardinality() of the enumerated carrier (FiniteEnumeratedSet, IntegerRange, Zmod(n), cartesian_product) | Replace a partly hand-rolled algorithm by the routine of the routine table (LV6, LV12); Delete the leaf-held datum (the tables `COUNTABLE` and `UNCOUNTABLE` decide which named sets are countable (sage_set_limits.py:75-83, :192-199)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.f9_x` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).cardinality() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.f9_y` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).cardinality() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.fin` | `sage` | V1 | IntegerRange(0, n).cardinality()  [Parent.cardinality] | Keep the engine routine (LV12). |
| `meth.cardinality` | `obj.sets.integers` | `sage` | V1 | ZZ.cardinality()  [Parent.cardinality] | Delete the leaf-held datum (Sage answers `+Infinity`; the leaf answers `aleph0` from its own table `COUNTABLE` (sage_backend.py:51-52, :73)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.integers_mod` | `gap` | V1 | Size(ZmodnZ(n), or Integers at n = 0) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); Delete the leaf-held datum (`ZMod 0` is $\mathbb{Z}$ by a rule of the leaf (gap_backend.py:33); GAP `infinity` is answered as `aleph0` (gap_backend.py:55-57)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.integers_mod_power` | `gap` | V1 | Size(FullRowModule(ZmodnZ(n), k)) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); Delete the leaf-held datum (`ZMod 0` is $\mathbb{Z}$ by a rule of the leaf (gap_backend.py:33); GAP `infinity` is answered as `aleph0` (gap_backend.py:55-57)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.naturals` | `sage` | V1 | NonNegativeIntegers().cardinality()  [Parent.cardinality] | Delete the leaf-held datum (Sage answers `+Infinity`; the leaf answers `aleph0` from its own table `COUNTABLE` (sage_backend.py:51-52, :73)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.permutations` | `gap-groups` | V1 | Size(SymmetricGroup(n)) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1). |
| `meth.cardinality` | `obj.sets.positive_naturals` | `sage` | V1 | PositiveIntegers().cardinality()  [Parent.cardinality] | Delete the leaf-held datum (Sage answers `+Infinity`; the leaf answers `aleph0` from its own table `COUNTABLE` (sage_backend.py:51-52, :73)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.power_set` | `sage-power-set` | V1 | Subsets(S).cardinality()  [sage.combinat.subset] | Delete the leaf-held datum (the leaf refuses an infinite `S` with the statement that its power set is uncountable (sage_power_set.py:53-55); `S` comes from a second table of parents (sage_power_set.py:38-48)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.primes` | `sage` | V1 | Primes().cardinality()  [Parent.cardinality] | Delete the leaf-held datum (Sage answers `+Infinity`; the leaf answers `aleph0` from its own table `COUNTABLE` (sage_backend.py:51-52, :73)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.sets.rationals` | `sage` | V1 | QQ.cardinality()  [Parent.cardinality] | Delete the leaf-held datum (Sage answers `+Infinity`; the leaf answers `aleph0` from its own table `COUNTABLE` (sage_backend.py:51-52, :73)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |

| Version | Registrations |
| --- | ---: |
| V1 | 13 |
| Total | 13 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/sage_power_set.py` | V1 |
| `backends/sage_set_limits.py` | V1 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Sets"; "Cardinals"; "Finite sets, countable sets, enumerated sets".

## Complexity Tracking

No constitution violation needs a justification.
