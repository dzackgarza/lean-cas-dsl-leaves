# Feature Specification: Arrows of Formed Modules category implementation (`cat.arrows_bilin_module`)

**Feature Branch**: `027-arrows-bilin-module` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.arrows_bilin_module` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.arrows_bilin_module`.
- **Object**: a morphism of formed modules (an object of the arrow category of $\mathrm{Bil}(R, W)$).
- **Morphism**: a commutative square of morphisms of formed modules.
- **Built from**: `cat.bilin_module` (structural functors and classifier forgets of the catalogue).
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 2 | 4 |

**V3.** The rows whose home is `cat.arrows_bilin_module` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher restricts a formed module along an inclusion of modules, with the restricted form, the inclusion and the two comparison maps, and restricts after a change of values.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category arrows_bilin_module` starts `backends/arrows_bilin_module.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.arrows_bilin_module` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T244 ("Implement Arrows of formed modules Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.arrows_bilin_module`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a computation that asks the kernel for an operation of another category, **When** the peer resumes with the `noImplementation` slot, **Then** the backend receives a `NoImplementation` value and continues under its own control logic (LV8).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/arrows_bilin_module.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A lift field request whose preceding outputs differ from the request's prefix | `status:"error"` naming the field; the reply never substitutes another prefix | LV4, LV11 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `lift.bilin_module.restrict`** (lift, V1). Catalogue: Restriction of forms: the cartesian lift of a monomorphism `K ↪ U(X)` along the forgetful functor `U` of formed modules is `X` restricted to the image of `K`, with its isometric inclusion. The implementation MUST compute each field of the lift from the request and the outputs of the preceding fields that the request supplies, and retain them in each reply. Inputs before it: lean-categories T029 (#192).
- **FR-002 — `lift.bilin_module.change_value_restriction`** (lift, V1). Catalogue: Cartesian monomorphism lifts for the functor `changeValue R W a : BilinModuleCat R W ⥤ BilinModuleCat R W'`, which postcomposes each pairing by the selected linear map `a : W →ₗ[R] W'`. The implementation MUST compute each field of the lift from the request and the outputs of the preceding fields that the request supplies, and retain them in each reply. Inputs before it: lean-categories T029 (#192).
- **FR-003 — Existing registrations of V1** (4). The implementation MUST move the 4 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V1 into `backends/arrows_bilin_module.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Key Entities

- **Category implementation of `cat.arrows_bilin_module`**: the module `backends/arrows_bilin_module.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 2 requirements FR-001 and FR-002 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 4 registrations of FR-003 are served by `backends/arrows_bilin_module.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `arrows_bilin_module` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel T244 ("Implement Arrows of formed modules Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
