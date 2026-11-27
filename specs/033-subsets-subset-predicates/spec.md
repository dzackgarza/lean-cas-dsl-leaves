# Feature Specification: Subset Predicates category implementation (`cat.subsets.subset_predicates`)

**Feature Branch**: `033-subsets-subset-predicates` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.subsets.subset_predicates` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.subsets.subset_predicates`.
- **Object**: a subset with a predicate on the subsets of its ambient set (the category of elements of `fun.subsets.subset_predicates` on $\mathrm{Core}(\mathrm{Subobjects}(\mathbf{Set}))$).
- **Morphism**: a morphism of the category of elements: an isomorphism of subsets that carries one predicate to the other.
- **Built from**: `cat.core_subobjects_sets`, `cat.sets` (structural functors and classifier forgets of the catalogue).
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 1 | 0 |

**V3.** The rows whose home is `cat.subsets.subset_predicates` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher compares the underlying set of a structure with a set given by its elements.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category subsets_subset_predicates` starts `backends/subsets_subset_predicates.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.subsets.subset_predicates` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T251 ("Implement Subset predicates Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.subsets.subset_predicates`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** an inherited method request with the receiver, the residual action descriptors and the method functor, **When** the backend replies, **Then** it has realized that composite and no other (contract FR-017).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| Equality of two presented infinite subsets that the engine cannot decide | The decision packet `none` | LV11; contract FR-012 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `meth.set_eq`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017). Inputs before it: lean-categories 001 T007 (#200), lean-categories 001 T013 (#191), contract T021.

### Key Entities

- **Category implementation of `cat.subsets.subset_predicates`**: the module `backends/subsets_subset_predicates.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 1 requirements FR-001 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `subsets_subset_predicates` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T251 ("Implement Subset predicates Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
