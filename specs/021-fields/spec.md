# Feature Specification: Fields category implementation (`cat.fields`)

**Feature Branch**: `021-fields` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.fields` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.fields`.
- **Object**: a field (the total category of the classifier `clf.commutative_rings.field`).
- **Morphism**: a field homomorphism.
- **Engine**: Sage (`GF`, `QQ`, `VectorSpace`, `span`, `dimension`) (engine survey, "Fields", "Linear algebra").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 5 | 1 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.fields` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher builds $\mathbb{Q}$ and $\mathbb{Z}/p$ as fields, spans a subspace of $K^n$ by vectors, compares spans, tests membership in a span and reads its dimension.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category fields` starts `backends/fields.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.fields` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Fields Spec V1" (`cat.fields`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.fields`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/fields.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `obj.fields.rationals`** (object constructor, V1). Catalogue: The named rational field refines its already selected commutative ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-002 — `obj.fields.prime_residues`** (object constructor, V1). Catalogue: For a natural number `p` and explicit evidence `hp : p.Prime`, the field whose carrier is `ZMod p = ℤ / pℤ` with its usual residue addition and multiplication. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `forget[clf.commutative_rings.field]`** (classifier forget, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). Inputs before it: lean-categories T033 (#197).
- **FR-004 — `mor.sets.span`** (operation, V1). Catalogue: The span of a set of vectors over the selected field. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-005 — `mor.sets.span_dim`** (operation, V1). Catalogue: The dimension of the span over the selected field, using its compatible field structure. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-006 — Existing registrations of V1** (1). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/fields.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `mor.sets.span` | `obj.sets.power_set` | `sage-symbolic` |

### Key Entities

- **Category implementation of `cat.fields`**: the module `backends/fields.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 5 requirements FR-001 to FR-005 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 1 registrations of FR-006 are served by `backends/fields.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `fields` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel task "Implement Fields Spec V1" (`cat.fields`) consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
