# Feature Specification: Linear Orders category implementation (`cat.linear_orders`)

**Feature Branch**: `006-linear-orders` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.linear_orders` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.linear_orders`.
- **Object**: a linear order (catalogue: "Linear orders").
- **Morphism**: a monotone map.
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 9 | 0 |

**V3.** The rows whose home is `cat.linear_orders` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher compares two integers, naturals or reals with $<$ and $\le$, reads $\mathrm{Fin}\,n$ with its ordinary and its reversed order, and forgets an order to its underlying set.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category linear_orders` starts `backends/linear_orders.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.linear_orders` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T207 ("Implement Linear orders Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.linear_orders`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| Two exact reals that the engine cannot compare | The decision packet `none` | LV11; contract FR-012 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.linear_orders`** (category structure, V1). Catalogue: Linear orders. The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout. Inputs before it: lean-categories T041 (#195).
- **FR-002 — `obj.linear_orders.fin_ordinary`** (object constructor, V1). Catalogue: For `n : ℕ`, the linear-order object with carrier `Fin n` and the usual relation `a ≤ b` exactly when `a.val ≤ b.val` in `ℕ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T041 (#195).
- **FR-003 — `obj.linear_orders.fin_reverse`** (object constructor, V1). Catalogue: For `n : ℕ`, the linear-order object on `OrderDual (Fin n)`: its elements are the same finite ordinals, and `a ≤ b` in this selected order means `b.val ≤ a.val` in the usual natural-number order. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T041 (#195).
- **FR-004 — `obj.linear_orders.integers`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T041 (#195).
- **FR-005 — `obj.linear_orders.naturals`** (object constructor, V1). Catalogue: `ℕ, ℤ, ℚ, ℝ` as linear orders, and their underlying sets. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T041 (#195).
- **FR-006 — `obj.linear_orders.reals`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T041 (#195).
- **FR-007 — `op.linear_orders.le`** (operation, V1). Catalogue: `≤`, into `Ω`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: $\le$ on $\mathbb{N}$. Inputs before it: lean-categories T041 (#195).
- **FR-008 — `op.linear_orders.lt`** (operation, V1). Catalogue: `<`, into `Ω`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: $<$ on $\mathbb{N}$. Inputs before it: lean-categories T041 (#195).
- **FR-009 — `fun.linear_orders.forget`** (functor, V1). Catalogue: The underlying set of a linear order. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). Inputs before it: lean-categories T041 (#195).

### Key Entities

- **Category implementation of `cat.linear_orders`**: the module `backends/linear_orders.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 9 requirements FR-001 to FR-009 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `linear_orders` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T207 ("Implement Linear orders Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
