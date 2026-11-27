# Feature Specification: Core Modules category implementation (`cat.core_modules_r`)

**Feature Branch**: `022-core-modules-r` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.core_modules_r` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.core_modules_r`.
- **Object**: an $R$-module.
- **Morphism**: an $R$-linear isomorphism: the catalogue builds the category as $\mathrm{Core}(\mathbf{Mod}_R)$.
- **Built from**: `cat.modules_r` (structural functors and classifier forgets of the catalogue).
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 1 | 0 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 2 | 5 |

**V3.** The rows whose home is `cat.core_modules_r` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher reads the dimension of a vector space.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category core_modules_r` starts `backends/core_modules_r.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.core_modules_r` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T237 ("Implement Core of modules Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.core_modules_r`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher reads the rank of a module, of a root lattice, of its dual and of its discriminant.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category core_modules_r` starts `backends/core_modules_r.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.core_modules_r` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T261 ("Implement Core of modules Spec V2"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.core_modules_r`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
5. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/core_modules_r.py` answers it with the routine of its decision, and no v1 program serves it.
6. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `meth.dim`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).

### Functional Requirements — V2

- **FR-002 — `meth.rank`** (operation, V2). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-003 — `fun.modules.rank`** (functor, V2). Catalogue: `rank : Core(Mod_R) ⥤ Disc(Card)`. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). Inputs before it: lean-categories 001 T037 (#182).
- **FR-004 — Existing registrations of V2** (5). The implementation MUST move the 5 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V2 into `backends/core_modules_r.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Key Entities

- **Category implementation of `cat.core_modules_r`**: the module `backends/core_modules_r.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 1 requirements FR-001 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `core_modules_r` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T237 ("Implement Core of modules Spec V1") consumes the version with no kernel-side evaluation of a row of this version.
- **SC-004** (V2): each of the 2 requirements FR-002 and FR-003 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-005** (V2): the 5 registrations of FR-004 are served by `backends/core_modules_r.py` on protocol 2, and no v1 program serves any of them.
- **SC-006** (V2): tier 1 of `core_modules_r` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-007** (V2): kernel T261 ("Implement Core of modules Spec V2") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
