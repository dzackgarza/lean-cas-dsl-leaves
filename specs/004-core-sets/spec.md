# Feature Specification: Core Sets category implementation (`cat.core_sets`)

**Feature Branch**: `004-core-sets` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.core_sets` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.core_sets`.
- **Object**: a set.
- **Morphism**: a bijection: the catalogue builds the category as the core $\mathrm{Core}(\mathbf{Set})$ (`ctor.core` of `cat.sets`).
- **Built from**: `cat.sets` (structural functors and classifier forgets of the catalogue).
- **Engine**: Sage (`cardinality()`, `Subsets(X, 2)`, `Permutations`), with the cardinal arithmetic of spec 002 (engine survey, "Sets", "Cardinals").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 6 | 13 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.core_sets` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher asks the size of a set: of a finite set, of a number set, of $\mathbb{Z}/n$ and its powers, of the permutations of $\mathrm{Fin}\,n$, of a power set, of a product or a set built from these. A researcher forms the set of two-element subsets of a set and transports it along a bijection, and uses the reversal of $\mathrm{Fin}\,n$ as a bijection.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category core_sets` starts `backends/core_sets.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.core_sets` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Core Sets Spec V1" (`cat.core_sets`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.core_sets`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
5. **Given** a computation that asks the kernel for an operation of another category, **When** the peer resumes with the `noImplementation` slot, **Then** the backend receives a `NoImplementation` value and continues under its own control logic (LV8).
6. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/core_sets.py` answers it with the routine of its decision, and no v1 program serves it.
7. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A set that the engine presents as infinite and not as an enumerated set | `status:"unsupported"`: the implementation computes finite cardinals and $\aleph_0$ and their arithmetic, and this presentation determines neither | LV6, LV11 |
| A cardinality is asked of a set whose rows are not lowered here | The request receiver and its residual actions arrive at the generated layout; the implementation asks the kernel for the residual actions | LV8; contract FR-017 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `meth.cardinality`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-002 — `fun.sets.cardinality`** (functor, V1). Catalogue: `card : Core(Sets) ⥤ Disc(Card)`. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-003 — `obj.sets.two_subsets`** (object constructor, V1). Catalogue: For any set carrier `X : Type u`, the set of unordered finite subsets `s : Finset X` satisfying `s.card = 2`, as Mathlib `Set.powersetCard X 2`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `meth.two_subsets`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-005 — `fun.core_sets.two_subsets`** (functor, V1). Catalogue: The functor `Core (Type u) ⥤ Type u` sending a selected set `X` to its unordered two-element subsets. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-006 — `mor.core_sets.fin_rev`** (operation, V1). Catalogue: The specified reversal of `Fin n`, now as an arrow of `Core(Sets)`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-007 — Existing registrations of V1** (13). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/core_sets.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `meth.cardinality` | `cat.sets` | `sage-set-limits` |
  | `meth.cardinality` | `obj.sets.f9_x` | `sage-presentations` |
  | `meth.cardinality` | `obj.sets.f9_y` | `sage-presentations` |
  | `meth.cardinality` | `obj.sets.fin` | `sage` |
  | `meth.cardinality` | `obj.sets.integers` | `sage` |
  | `meth.cardinality` | `obj.sets.integers_mod` | `gap` |
  | `meth.cardinality` | `obj.sets.integers_mod_power` | `gap` |
  | `meth.cardinality` | `obj.sets.naturals` | `sage` |
  | `meth.cardinality` | `obj.sets.permutations` | `gap-groups` |
  | `meth.cardinality` | `obj.sets.positive_naturals` | `sage` |
  | `meth.cardinality` | `obj.sets.power_set` | `sage-power-set` |
  | `meth.cardinality` | `obj.sets.primes` | `sage` |
  | `meth.cardinality` | `obj.sets.rationals` | `sage` |

### Key Entities

- **Category implementation of `cat.core_sets`**: the module `backends/core_sets.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 6 requirements FR-001 to FR-006 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 13 registrations of FR-007 are served by `backends/core_sets.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `core_sets` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel task "Implement Core Sets Spec V1" (`cat.core_sets`) consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
