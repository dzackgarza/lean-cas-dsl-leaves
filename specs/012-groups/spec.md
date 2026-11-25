# Feature Specification: Groups category implementation (`cat.groups`)

**Feature Branch**: `012-groups` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.groups` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.groups`.
- **Object**: a group.
- **Morphism**: a group homomorphism.
- **Engine**: GAP through Sage `libgap` (`CyclicGroup`, `SymmetricGroup`, `Units`, `AutomorphismGroup`, `GroupHomomorphismByImages`, `Size`, `IsAbelian`, `Inverse`) (engine survey, "Groups", "Group-valued constructions").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 10 | 6 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 8 | 6 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.groups` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher builds the cyclic group $\mathbb{Z}/n$ and the quotient $\mathbb{Z}/n\mathbb{Z}$ as groups, the unit group of a monoid, the automorphisms of a cyclic quotient given by units and their inverses, and composes and inverts these automorphisms; a researcher asks the size and the finiteness of these groups and forgets a group to its monoid.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category groups` starts `backends/groups.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.groups` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Groups Spec V1" (`cat.groups`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.groups`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/groups.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher builds the symmetric group, the identity, sign and trivial homomorphisms, the unit group of a monoid by its functor, inverts an element of a group, and tests whether a group is abelian.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category groups` starts `backends/groups.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.groups` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Groups Spec V2" (`cat.groups`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.groups`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
5. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/groups.py` answers it with the routine of its decision, and no v1 program serves it.
6. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A composite of two group maps given only by their graphs | The `compose` envelope carries the selected intermediate group (contract T021); without it the request is `unsupported` | LV4, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.groups`** (category structure, V1). The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout. Inputs before it: contract T021.
- **FR-002 — `obj.groups.cyclic`** (object constructor, V1). Catalogue: The additive cyclic group, expressed multiplicatively as an object of groups. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `obj.groups.cyclic_quotient`** (object constructor, V1). Catalogue: For `n : ℕ`, the group with carrier `ℤ / nℤ` in multiplicative notation: `[a] * [b] = [a + b]`, identity `[0]`, and inverse `[a]⁻¹ = [-a]`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `obj.groups.units`** (object constructor, V1). Catalogue: The chosen group of units, with all its group structure. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-005 — `fun.groups.monoid`** (functor, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-006 — `con.automorphisms`** (construction, V1). Catalogue: Automorphisms in the selected category, applied directly rather than through an inherited method on the underlying set. The implementation MUST construct the result with its defining data at the generated result layout.
- **FR-007 — `cmp.groups.cyclic_quotient_residue`** (comparison, V1). Catalogue: For `n : ℕ`, the group isomorphism from `cyclicQuotient n` to `FiniteGroups.cyclic n`, whose latter carrier is `Multiplicative (ZMod n)`. The implementation MUST return the components of the selected comparison in both directions, at the endpoints that the request selects.
- **FR-008 — `mor.groups.cyclic_quotient_aut_by_unit`** (operation, V1). Catalogue: For `n : ℕ`, the group morphism from the unit group `(ZMod n)ˣ` to the categorical automorphism group of the integer quotient `ℤ / nℤ` with its additive group law, represented as `cyclicQuotient n`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-009 — `mor.groups.automorphism_forward`** (operation, V1). Catalogue: The forward group homomorphism of an element of `Aut(G)` in `Groups`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-010 — `mor.groups.automorphism_backward`** (operation, V1). Catalogue: The inverse group homomorphism of the same `Aut(G)` element. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-011 — Existing registrations of V1** (6). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/groups.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `meth.cardinality` | `obj.groups.cyclic` | `gap-groups` |
  | `meth.cardinality` | `obj.groups.units` | `gap-groups` |
  | `prop.is_commutative` | `obj.groups.cyclic` | `gap-groups` |
  | `prop.is_commutative` | `obj.groups.units` | `gap-groups` |
  | `prop.is_finite` | `obj.groups.cyclic` | `gap-groups` |
  | `prop.is_finite` | `obj.groups.units` | `gap-groups` |

### Functional Requirements — V2

- **FR-012 — `obj.groups.symmetric`** (object constructor, V2). Catalogue: The chosen symmetric group of an ordinal. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-013 — `mor.groups.identity`** (operation, V2). Catalogue: The identity map in any chosen group. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-014 — `mor.groups.sign`** (operation, V2). Catalogue: The parity map `Sₙ → ℤ/2`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-015 — `mor.groups.trivial`** (operation, V2). Catalogue: The trivial homomorphism between chosen groups. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-016 — `op.groups.inverse`** (operation, V2). Catalogue: Inversion belongs to every group, independent of how that group was constructed. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: the inverse of an instance. Inputs before it: contract T021.
- **FR-017 — `prop.is_abelian`** (property, V2). The implementation MUST answer the property with the decision packet of contract FR-012 (`none` when the engine cannot establish it).
- **FR-018 — `meth.units`** (operation, V2). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-019 — `fun.monoids.units`** (functor, V2). Catalogue: The canonical units functor, right adjoint to forgetting a group's inverses. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). The object reply carries the group with its operations and the defining inclusion of the units at the request's monoid, for the later group and map operations that consume them; this row also serves kernel T155.
- **FR-020 — Existing registrations of V2** (6). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/groups.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `meth.cardinality` | `obj.groups.symmetric` | `gap-groups` |
  | `prop.is_abelian` | `obj.groups.cyclic` | `gap-groups` |
  | `prop.is_abelian` | `obj.groups.symmetric` | `gap-groups` |
  | `prop.is_abelian` | `obj.groups.units` | `gap-groups` |
  | `prop.is_commutative` | `obj.groups.symmetric` | `gap-groups` |
  | `prop.is_finite` | `obj.groups.symmetric` | `gap-groups` |

### Key Entities

- **Category implementation of `cat.groups`**: the module `backends/groups.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 10 requirements FR-001 to FR-010 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 6 registrations of FR-011 are served by `backends/groups.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `groups` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel task "Implement Groups Spec V1" (`cat.groups`) consumes the version with no kernel-side evaluation of a row of this version.
- **SC-005** (V2): each of the 8 requirements FR-012 to FR-019 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-006** (V2): the 6 registrations of FR-020 are served by `backends/groups.py` on protocol 2, and no v1 program serves any of them.
- **SC-007** (V2): tier 1 of `groups` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-008** (V2): kernel task "Implement Groups Spec V2" (`cat.groups`) consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
