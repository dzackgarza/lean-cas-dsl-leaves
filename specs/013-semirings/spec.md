# Feature Specification: Semirings category implementation (`cat.semirings`)

**Feature Branch**: `013-semirings` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.semirings` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.semirings`.
- **Object**: a semiring (catalogue: "Semirings").
- **Morphism**: a semiring homomorphism.
- **Engine**: Sage (`NonNegativeIntegerSemiring`, element arithmetic) (engine survey, "Semirings"; homomorphisms are glue).

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 7 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.semirings` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher computes with natural numbers as a semiring: numerals, sums, products and powers, and forgets a semiring to its underlying set and to its multiplicative monoid.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category semirings` starts `backends/semirings.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.semirings` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Semirings Spec V1" (`cat.semirings`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.semirings`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `obj.semirings.naturals`** (object constructor, V1). Catalogue: `ℕ` as a semiring; its underlying set is `ℕ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-002 — `num.semirings`** (operation, V1). Catalogue: The numeral `k` of a semiring `S`: the image of `k` under the unique semiring map `ℕ → S` out of the initial semiring (Mathlib `Nat.castRingHom`), LC-15; for `S = ℕ`, `k` itself. The implementation MUST return the value of the literal or numeral descriptor at the generated layout. Inputs before it: lean-categories T017 (#194).
- **FR-003 — `op.semirings.add`** (operation, V1). Catalogue: Addition. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{N}$. Inputs before it: lean-categories T005 (#193), contract T021.
- **FR-004 — `op.semirings.mul`** (operation, V1). Catalogue: Multiplication. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{N}$. Inputs before it: lean-categories T005 (#193), contract T021.
- **FR-005 — `op.semirings.pow`** (operation, V1). Catalogue: The power `x ↦ x^k`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{N}$. Inputs before it: contract T021.
- **FR-006 — `fun.semirings.forget`** (functor, V1). Catalogue: The underlying set of a semiring. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-007 — `fun.semirings.monoid`** (functor, V1). Catalogue: The second factor already used by `Ports.ringsMultiplicative`. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).

### Key Entities

- **Category implementation of `cat.semirings`**: the module `backends/semirings.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 7 requirements FR-001 to FR-007 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `semirings` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel task "Implement Semirings Spec V1" (`cat.semirings`) consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
