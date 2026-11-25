# Feature Specification: Finite Sets category implementation (`cat.finite_sets`)

**Feature Branch**: `005-finite-sets` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.finite_sets` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.finite_sets`.
- **Object**: a finite type (catalogue: "Finite types").
- **Morphism**: a function between finite types.
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 3 | 0 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 2 | 2 |

**V3.** The rows whose home is `cat.finite_sets` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher refines a finite set of integers, such as $\{n \in \mathbb{Z} \mid n^2 \le b\}$, to a finite set, reads it back as a set, and reads the graph of a map between finite sets.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category finite_sets` starts `backends/finite_sets.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.finite_sets` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T204 ("Implement Finite sets Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.finite_sets`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher builds $\mathrm{Fin}\,n$ as a finite set, composes maps of finite sets and asks the size and the finiteness of a finite set.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category finite_sets` starts `backends/finite_sets.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.finite_sets` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T255 ("Implement Finite sets Spec V2"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.finite_sets`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/finite_sets.py` answers it with the routine of its decision, and no v1 program serves it.
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `forget[clf.sets.finite]`** (classifier forget, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). Inputs before it: lean-categories T033 (#197).
- **FR-002 — `obj.finite_sets.integer_square_bound`** (object constructor, V1). Catalogue: For `r : ℕ`, the finite-set object with the same carrier `{n : ℤ // n ^ 2 ≤ (r : ℤ) ^ 2}` as `extent r`, equipped with finiteness from `squareBound_finite`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T033 (#197).
- **FR-003 — `graph.finite_sets`** (operation, V1). Catalogue: The map of finite sets `X → Y` with graph `l`, which lists each element of `X` exactly once. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: the list of the elements of a finite carrier.

### Functional Requirements — V2

- **FR-004 — `cat.finite_sets`** (category structure, V2). Catalogue: Finite types. The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout.
- **FR-005 — `obj.finite_sets.fin`** (object constructor, V2). Catalogue: `Fin n` as a finite set. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-006 — Existing registrations of V2** (2). The implementation MUST move the 2 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V2 into `backends/finite_sets.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Key Entities

- **Category implementation of `cat.finite_sets`**: the module `backends/finite_sets.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 3 requirements FR-001 to FR-003 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `finite_sets` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T204 ("Implement Finite sets Spec V1") consumes the version with no kernel-side evaluation of a row of this version.
- **SC-004** (V2): each of the 2 requirements FR-004 and FR-005 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-005** (V2): the 2 registrations of FR-006 are served by `backends/finite_sets.py` on protocol 2, and no v1 program serves any of them.
- **SC-006** (V2): tier 1 of `finite_sets` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-007** (V2): kernel T255 ("Implement Finite sets Spec V2") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
