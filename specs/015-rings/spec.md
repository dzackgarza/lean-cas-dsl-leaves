# Feature Specification: Rings category implementation (`cat.rings`)

**Feature Branch**: `015-rings` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.rings` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.rings`.
- **Object**: a ring.
- **Morphism**: a ring homomorphism.
- **Engine**: Sage (`ZZ`, `QQ`, `Zmod(n)`, `AA`, `QQbar`, element arithmetic, coercion) (engine survey, "Rings and commutative rings").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 16 | 2 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.rings` join V3 of this spec. This spec plans nothing more for V3.

**V2 of the kernel.** Kernel T257 ("Implement Rings Spec V2") assesses the V2 statements whose last route category is `cat.rings`. No row of `cat.rings` is in V2, so this spec has no V2: the earlier versions of this spec serve that kernel task.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher computes in $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$ and $\mathbb{Z}/n$: numerals, sums, products, negatives and powers, exact values such as $1 + 1/2$ and $(1 + \sqrt{2})(1 - \sqrt{2})$; a researcher asks the size and the finiteness of $\mathbb{Z}/n$ as a ring and forgets a ring to its additive group, its multiplicative monoid, its semiring and its underlying set.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category rings` starts `backends/rings.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.rings` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T218 ("Implement Rings Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.rings`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/rings.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.rings`** (category structure, V1). The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout.
- **FR-002 — `obj.rings.integers`** (object constructor, V1). Catalogue: `ℤ` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `obj.rings.rationals`** (object constructor, V1). Catalogue: `ℚ` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `obj.rings.reals`** (object constructor, V1). Catalogue: `ℝ` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-005 — `obj.rings.complexes`** (object constructor, V1). Catalogue: `ℂ` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-006 — `obj.rings.integers_mod`** (object constructor, V1). Catalogue: `ℤ/n` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-007 — `num.rings`** (operation, V1). Catalogue: The numeral `k` of a ring `R`: the image of `k ∈ ℕ ⊆ ℤ` under the unique ring map `ℤ → R` out of the initial ring (Mathlib `Int.castRingHom`), LC-15. The implementation MUST return the value of the literal or numeral descriptor at the generated layout. It takes over from the kernel: arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$. Inputs before it: lean-categories T017 (#194).
- **FR-008 — `op.rings.add`** (operation, V1). Catalogue: Addition, `R × R → R`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$. Inputs before it: lean-categories T005 (#193), lean-categories T064 (#211), contract T021.
- **FR-009 — `op.rings.mul`** (operation, V1). Catalogue: Multiplication, `R × R → R`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$. Inputs before it: lean-categories T005 (#193), lean-categories T064 (#211), contract T021.
- **FR-010 — `op.rings.neg`** (operation, V1). Catalogue: Negation, `R → R`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$. Inputs before it: lean-categories T005 (#193), lean-categories T064 (#211), contract T021.
- **FR-011 — `op.rings.pow`** (operation, V1). Catalogue: The power `x ↦ x^k`, `R → R`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: arithmetic of $\mathbb{Z}$ and $\mathbb{Z}/n$. Inputs before it: lean-categories T064 (#211), contract T021.
- **FR-012 — `fun.rings.additive_group`** (functor, V1). Catalogue: The additive group of a ring. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-013 — `fun.rings.multiplicative_monoid`** (functor, V1). Catalogue: The multiplicative monoid of a ring. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-014 — `fun.rings.semiring`** (functor, V1). Catalogue: The first factor already used by `Ports.ringsMultiplicative`. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-015 — `fun.rings.additive_commutative_monoid`** (functor, V1). Catalogue: The additive commutative monoid of a ring. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-016 — `cmp.rings.carrier`** (comparison, V1). Catalogue: The two underlying sets of a ring are identified by the identity natural isomorphism. The implementation MUST return the components of the selected comparison in both directions, at the endpoints that the request selects.
- **FR-017 — Existing registrations of V1** (2). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/rings.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `meth.cardinality` | `obj.rings.integers_mod` | `gap` |
  | `prop.is_finite` | `obj.rings.integers_mod` | `gap` |

### Key Entities

- **Category implementation of `cat.rings`**: the module `backends/rings.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 16 requirements FR-001 to FR-016 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 2 registrations of FR-017 are served by `backends/rings.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `rings` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel T218 ("Implement Rings Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
