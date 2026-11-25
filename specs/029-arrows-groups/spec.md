# Feature Specification: Arrows of Groups category implementation (`cat.arrows_groups`)

**Feature Branch**: `029-arrows-groups` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.arrows_groups` against the released contract `cas-computation/2`, in version V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.arrows_groups`.
- **Object**: a group homomorphism $f : G \to H$ (an object of the arrow category of $\mathbf{Grp}$).
- **Morphism**: a commutative square of group homomorphisms.
- **Built from**: `cat.groups` (structural functors and classifier forgets of the catalogue).
- **Engine**: GAP through Sage `libgap` (`GroupHomomorphismByImages`, `Kernel`, `Elements`) (engine survey, "Groups").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 2 | 2 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.arrows_groups` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V2: the full-B0 computations (Priority: P1)

A researcher takes the kernel of a group homomorphism, such as the sign, identity or trivial map of a symmetric group, as a subgroup with its inclusion.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category arrows_groups` starts `backends/arrows_groups.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.arrows_groups` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Arrows of Groups Spec V2" (`cat.arrows_groups`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.arrows_groups`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
5. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/arrows_groups.py` answers it with the routine of its decision, and no v1 program serves it.
6. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V2

- **FR-001 — `meth.group_arrow_kernel`** (operation, V2). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-002 — `fun.arrows_groups.kernel`** (functor, V2). Catalogue: Group kernels act functorially on squares, preserving their defining inclusions. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-003 — Existing registrations of V2** (2). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/arrows_groups.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `fun.arrows_groups.kernel` | `cat.arrows_groups` | `gap-groups` |
  | `meth.group_arrow_kernel` | `cat.arrows_groups` | `gap-groups` |

### Key Entities

- **Category implementation of `cat.arrows_groups`**: the module `backends/arrows_groups.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V2): each of the 2 requirements FR-001 and FR-002 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V2): the 2 registrations of FR-003 are served by `backends/arrows_groups.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V2): tier 1 of `arrows_groups` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V2): kernel task "Implement Arrows of Groups Spec V2" (`cat.arrows_groups`) consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
