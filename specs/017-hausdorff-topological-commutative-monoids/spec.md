# Feature Specification: Hausdorff Topological Commutative Monoids category implementation (`cat.hausdorff_topological_commutative_monoids`)

**Feature Branch**: `017-hausdorff-topological-commutative-monoids` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.hausdorff_topological_commutative_monoids` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.hausdorff_topological_commutative_monoids`.
- **Object**: a Hausdorff commutative topological monoid.
- **Morphism**: a continuous monoid homomorphism.
- **Engine**: Sage lazy power series (`LazyPowerSeriesRing`) with the $t$-adic topology (engine survey, "Polynomial rings").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 4 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.hausdorff_topological_commutative_monoids` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher reads a power series ring as a Hausdorff topological monoid, sums a summable family of power series terms, and forgets the topology.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category hausdorff_topological_commutative_monoids` starts `backends/hausdorff_topological_commutative_monoids.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.hausdorff_topological_commutative_monoids` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T222 ("Implement Hausdorff topological commutative monoids Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.hausdorff_topological_commutative_monoids`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A family that is not summable in the $t$-adic topology | `status:"unsupported"` with the exact `op` | LV11 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.hausdorff_topological_commutative_monoids`** (category structure, V1). Catalogue: The Hausdorff commutative topological monoids, as an object of the categories. The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout.
- **FR-002 — `obj.hausdorff_topological_monoids.power_series`** (object constructor, V1). Catalogue: `R[[t]]` with its `(t)`-adic topology, a Hausdorff commutative topological monoid. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `obj.sets.summable_families`** (object constructor, V1). Catalogue: `Σ(N, Y)`, the summable families `N → Y`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T027 (#190).
- **FR-004 — `fun.hausdorff_topological_commutative_monoids.additive_commutative_monoid`** (functor, V1). Catalogue: The underlying additive commutative monoid of a Hausdorff commutative topological monoid. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).

### Key Entities

- **Category implementation of `cat.hausdorff_topological_commutative_monoids`**: the module `backends/hausdorff_topological_commutative_monoids.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 4 requirements FR-001 to FR-004 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `hausdorff_topological_commutative_monoids` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T222 ("Implement Hausdorff topological commutative monoids Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
