# Feature Specification: Boolean Algebras category implementation (`cat.boolean_algebras`)

**Feature Branch**: `030-boolean-algebras` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.boolean_algebras` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.boolean_algebras`.
- **Object**: a Boolean algebra (catalogue: "Boolean algebras").
- **Morphism**: a homomorphism of Boolean algebras.
- **Engine**: Sage finite sets and power sets (`Set`, `Subsets`), with the power-object values of the sets implementation for infinite subsets (engine survey, "Boolean algebras and power sets").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 7 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.boolean_algebras` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher takes the union, intersection, difference and symmetric difference of subsets, tests inclusion of subsets, including subsets of $\mathbb{C}$ such as $\mathbb{C} \setminus \mathbb{Q}$, and forgets a power set to its underlying set.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category boolean_algebras` starts `backends/boolean_algebras.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.boolean_algebras` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T249 ("Implement Boolean algebras Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.boolean_algebras`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| Inclusion of two presented infinite subsets that the engine cannot decide | The decision packet `none` | LV11; contract FR-012 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `obj.boolean_algebras.power_set`** (object constructor, V1). Catalogue: `𝒫(X)` as a Boolean algebra. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-002 — `op.boolean_algebras.union`** (operation, V1). Catalogue: `∪`, the join. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-003 — `op.boolean_algebras.inter`** (operation, V1). Catalogue: `∩`, the meet. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-004 — `op.boolean_algebras.diff`** (operation, V1). Catalogue: `\`, the difference. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-005 — `op.boolean_algebras.symm_diff`** (operation, V1). Catalogue: `△`, the symmetric difference. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-006 — `op.boolean_algebras.subset`** (operation, V1). Catalogue: `⊆`, the order, into `Ω`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-007 — `fun.boolean_algebras.forget`** (functor, V1). Catalogue: The underlying set of a Boolean algebra. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).

### Key Entities

- **Category implementation of `cat.boolean_algebras`**: the module `backends/boolean_algebras.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 7 requirements FR-001 to FR-007 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `boolean_algebras` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T249 ("Implement Boolean algebras Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
