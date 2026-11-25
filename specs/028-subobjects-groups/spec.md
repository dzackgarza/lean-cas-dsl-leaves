# Feature Specification: Subobjects of Groups category implementation (`cat.subobjects_groups`)

**Feature Branch**: `028-subobjects-groups` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.subobjects_groups` against the released contract `cas-computation/2`, in version V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.subobjects_groups`.
- **Object**: a subgroup $H \le G$ (an object of $\mathrm{Subobjects}(\mathbf{Grp})$).
- **Morphism**: a homomorphism of the ambient groups that carries one subgroup into the other.
- **Built from**: `cat.groups` (structural functors and classifier forgets of the catalogue).
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 2 | 11 |

**V3.** The rows whose home is `cat.subobjects_groups` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V2: the full-B0 computations (Priority: P1)

A researcher builds the alternating group as a subgroup of the symmetric group, reads a subgroup as a group, and asks the size, the finiteness and the commutativity of a subgroup, including a subgroup that a kernel returns.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category subobjects_groups` starts `backends/subobjects_groups.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.subobjects_groups` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T263 ("Implement Subgroups Spec V2"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.subobjects_groups`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/subobjects_groups.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A property of a subgroup that a kernel returned | The engine subgroup is built from the supplied inclusion images, not from the named kernel | CONTRIBUTING DAT001 |

## Requirements *(mandatory)*

### Functional Requirements — V2

- **FR-001 — `obj.subgroups.alternating`** (object constructor, V2). Catalogue: The alternating subgroup, including its defining inclusion into `Sₙ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-002 — `fun.subobjects_groups.domain`** (functor, V2). Catalogue: A subgroup is the group it is: the domain of its inclusion. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-003 — Existing registrations of V2** (11). The implementation MUST move the 11 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V2 into `backends/subobjects_groups.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Key Entities

- **Category implementation of `cat.subobjects_groups`**: the module `backends/subobjects_groups.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V2): each of the 2 requirements FR-001 and FR-002 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V2): the 11 registrations of FR-003 are served by `backends/subobjects_groups.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V2): tier 1 of `subobjects_groups` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V2): kernel T263 ("Implement Subgroups Spec V2") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
