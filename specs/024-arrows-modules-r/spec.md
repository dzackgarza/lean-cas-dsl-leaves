# Feature Specification: Arrows of Modules category implementation (`cat.arrows_modules_r`)

**Feature Branch**: `024-arrows-modules-r` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.arrows_modules_r` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.arrows_modules_r`.
- **Object**: an $R$-linear map $f : M \to N$ (an object of the arrow category of $\mathbf{Mod}_R$).
- **Morphism**: a commutative square of linear maps.
- **Built from**: `cat.modules_r` (structural functors and classifier forgets of the catalogue).
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 3 | 0 |

**V3.** The rows whose home is `cat.arrows_modules_r` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher takes the kernel and the image of a linear map as subobjects of its domain and codomain, with their inclusions.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category arrows_modules_r` starts `backends/arrows_modules_r.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.arrows_modules_r` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T241 ("Implement Arrows of modules Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.arrows_modules_r`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `meth.arrow_ker`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-002 — `meth.kernel`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-003 — `meth.arrow_im`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).

### Key Entities

- **Category implementation of `cat.arrows_modules_r`**: the module `backends/arrows_modules_r.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 3 requirements FR-001 to FR-003 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `arrows_modules_r` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T241 ("Implement Arrows of modules Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
