# Feature Specification: Enumerated Sets category implementation (`cat.enumerated_sets`)

**Feature Branch**: `032-enumerated-sets` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.enumerated_sets` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.enumerated_sets`.
- **Object**: a set with a selected partial-inverse enumeration (catalogue: "The category of sets with a selected partial-inverse enumeration").
- **Morphism**: a map of the sets that is compatible with the selected enumerations.
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 2 | 0 |

**V3.** The rows whose home is `cat.enumerated_sets` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher reads the $k$-th element of $\mathbb{Z}$ or $\mathbb{Q}$ in the adopted enumeration order, and forgets an enumerated set to its underlying set.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category enumerated_sets` starts `backends/enumerated_sets.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.enumerated_sets` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T250 ("Implement Enumerated sets Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.enumerated_sets`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| Sage's own enumeration of `ZZ` or `QQ` differs from the adopted order | The implementation computes the adopted `Denumerable.ofNat` order, not Sage's `unrank` | LV6 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `forget[clf.sets.enumerated]`** (classifier forget, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-002 — `obj.enumerated_sets.naturals`, `obj.enumerated_sets.integers`, `obj.enumerated_sets.rationals` and `mor.sets.enumeration_at`** (object constructors and operation that lean-categories T077 declares, V1): the enumeration $\mathbb{N} \to X$ of a denumerable set in the adopted `Denumerable.ofNat` order, its evaluation $X[k]$, and the objects of `cat.enumerated_sets` for $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$ and the progressions. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T077 (#224), which declares `obj.enumerated_sets.naturals`, `obj.enumerated_sets.integers`, `obj.enumerated_sets.rationals` and `mor.sets.enumeration_at` (kernel T340), lean-categories T039 (#199).

### Key Entities

- **Category implementation of `cat.enumerated_sets`**: the module `backends/enumerated_sets.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 2 requirements FR-001 and FR-002 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `enumerated_sets` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T250 ("Implement Enumerated sets Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
