# Feature Specification: Ideals category implementation (`cat.ideals_r`)

**Feature Branch**: `034-ideals-r` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.ideals_r` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.ideals_r`.
- **Object**: an ideal of $R$ (catalogue: "The ideals of `R`, as a discrete category").
- **Morphism**: an identity: the category is discrete.
- **Engine**: Sage ideals and module annihilators (`ZZ.ideal(n)`, `annihilator()`) (engine survey, "Modules").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 2 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.ideals_r` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher reads the annihilator of a module, such as $\mathbb{Z}/4$ or $\mathbb{Z}/12$ over $\mathbb{Z}$, as an ideal.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category ideals_r` starts `backends/ideals_r.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.ideals_r` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T252 ("Implement Ideals Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.ideals_r`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
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

- **FR-001 — `meth.annihilator`** (operation, V1). The implementation MUST answer the method at its actual domain; an inherited request carries the receiver, one descriptor for each residual action and the method functor, and the implementation realizes that composite (contract FR-017).
- **FR-002 — `missing.module_annihilator_value`** (row that the catalogue lacks, V1): objects of `cat.ideals_r`, such as the principal ideal $(4) \subseteq \mathbb{Z}$. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: kernel T341, the lean-categories task that declares `missing.module_annihilator_value` (issue not yet filed).

### Key Entities

- **Category implementation of `cat.ideals_r`**: the module `backends/ideals_r.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 2 requirements FR-001 and FR-002 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `ideals_r` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T252 ("Implement Ideals Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
