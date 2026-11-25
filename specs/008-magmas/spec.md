# Feature Specification: Magmas category implementation (`cat.magmas`)

**Feature Branch**: `008-magmas` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.magmas` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.magmas`.
- **Object**: a set with a binary operation (the total category of the classifier `clf.sets.binary_operation`).
- **Morphism**: a map that preserves the operation.
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 3 | 0 |

**V3.** The rows whose home is `cat.magmas` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher reads a set with a binary operation as a magma, tests associativity, and forgets a magma to its underlying set.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category magmas` starts `backends/magmas.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.magmas` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T211 ("Implement Magmas Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.magmas`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
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

- **FR-001 — `cat.magmas`** (category structure, V1). The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout. Inputs before it: lean-categories T005 (#193).
- **FR-002 — `clf.magmas.associative`** (classifier, V1). Catalogue: Associative classifier. The implementation MUST answer the classifier's decision at the supplied object with the decision packet of contract FR-012, and retain the selected structure of the request. Inputs before it: lean-categories T033 (#197).
- **FR-003 — `forget[clf.sets.binary_operation]`** (classifier forget, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). Inputs before it: lean-categories T033 (#197).

### Key Entities

- **Category implementation of `cat.magmas`**: the module `backends/magmas.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 3 requirements FR-001 to FR-003 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `magmas` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T211 ("Implement Magmas Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
