# Feature Specification: Monoids category implementation (`cat.monoids`)

**Feature Branch**: `011-monoids` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.monoids` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.monoids`.
- **Object**: a monoid (written multiplicatively).
- **Morphism**: a monoid homomorphism.
- **Engine**: Sage multiplicative parents (`ZZ`, `QQ`, `Zmod(n)`, matrix spaces) and GAP through `libgap` (`Units`) (engine survey, "Magmas, semigroups, monoids", "Groups").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 7 | 2 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.monoids` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher multiplies in a monoid, reads its unit, takes powers, divides by a unit, forms the set of units of a monoid such as $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{Z}/n$ or a matrix monoid, asks the size and the finiteness of that set, and forgets a monoid to its semigroup.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category monoids` starts `backends/monoids.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.monoids` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T214 ("Implement Monoids Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.monoids`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/monoids.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| The units of a monoid that no lowering here supplies | `status:"unsupported"` with the exact `op`; the v1 limit of GAP `Units` on other monoids stays explicit | LV11 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.monoids`** (category structure, V1). The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout. Inputs before it: lean-categories T005 (#193).
- **FR-002 — `op.monoids.mul`** (operation, V1). Catalogue: The multiplication of the selected monoid, with its entire binary domain. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: multiplication of an instance. Inputs before it: lean-categories T005 (#193), contract T021.
- **FR-003 — `op.monoids.one`** (operation, V1). Catalogue: The selected monoid's identity, as a point with terminal source. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: the unit of an instance. Inputs before it: lean-categories T005 (#193).
- **FR-004 — `mor.sets.monoid_power`** (operation, V1). Catalogue: `(x, n) ↦ xⁿ` in a monoid `M`, an object of monoids: `x⁰ = 1` is `M`'s unit and `xⁿ⁺¹ = xⁿ x` its multiplication (Mathlib `Monoid.npow`). The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-005 — `fun.monoids.semigroup`** (functor, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-006 — `obj.sets.units`** (object constructor, V1). Catalogue: `Mˣ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-007 — `mor.sets.divide`** (operation, V1). Catalogue: `(a, u) ↦ a u⁻¹`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-008 — Existing registrations of V1** (2). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/monoids.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `prop.is_finite` | `obj.sets.units` | `gap-groups` |
  | `meth.cardinality` | `obj.sets.units` | `gap-groups` |

### Key Entities

- **Category implementation of `cat.monoids`**: the module `backends/monoids.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 7 requirements FR-001 to FR-007 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 2 registrations of FR-008 are served by `backends/monoids.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `monoids` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel T214 ("Implement Monoids Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
