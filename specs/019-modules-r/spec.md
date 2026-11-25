# Feature Specification: Modules category implementation (`cat.modules_r`)

**Feature Branch**: `019-modules-r` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.modules_r` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.modules_r`.
- **Object**: an $R$-module (the fibre of the module family at a ring $R$).
- **Morphism**: an $R$-linear map.
- **Built from**: `cat.rings` (structural functors and classifier forgets of the catalogue).
- **Engine**: Sage modules (`FreeModule`, `VectorSpace`, module homomorphisms, finitely generated modules over a PID) (engine survey, "Modules", "Linear algebra").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 11 | 2 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 1 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.modules_r` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher builds $R$, $R^n$ and $\mathbb{Z}/n$ as $R$-modules, acts by scalars, restricts scalars along a ring homomorphism, builds a linear map from a row or from a formula, reads the derivation $d/dx$ of $\mathbb{Q}[x]$ as a linear map, asks the size of a module, and includes a module into the total category.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category modules_r` starts `backends/modules_r.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.modules_r` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Modules Spec V1" (`cat.modules_r`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.modules_r`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/modules_r.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher forms the set of bilinear maps on a module.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category modules_r` starts `backends/modules_r.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.modules_r` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel task "Implement Modules Spec V2" (`cat.modules_r`); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.modules_r`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A request whose rows need a declaration that lean-categories does not have | No port answers it; the declaration is a lean-categories task before the consumer | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.modules_r`** (category structure, V1). Catalogue: Fibre of the parameterized family at an arbitrary ring object. The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout.
- **FR-002 — `obj.modules.regular`** (object constructor, V1). Catalogue: The left regular module of the selected scalar ring: its additive group is the ring's own additive group, and scalar action is its multiplication. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `obj.modules.vectors`** (object constructor, V1). Catalogue: The product module over the selected scalar ring, with pointwise addition and scalar action; no basis or coordinates are chosen beyond the index `Fin n`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `op.modules.scalar_action`** (operation, V1). Catalogue: The selected module's actual scalar action, uncurried as a map of sets. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: the scalar action of an instance. Inputs before it: lean-categories T064 (#211).
- **FR-005 — `mor.modules.row_linear_map`** (operation, V1). Catalogue: Given `columns : ℕ`, a selected commutative ring `R`, and a row matrix `M : Fin 1 → Fin columns → R`, the `R`-linear map from `R^columns` to the regular module with carrier `R`, sending `x` to `∑ j, M 0 j * x j`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-006 — `fun.modules.fibre_inclusion`** (functor, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-007 — `fun.modules.reindex`** (functor, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-008 — `obj.modules_r.restricted_regular`** (object constructor, V1). Catalogue: Given selected rings `R`, `S` and a selected ring morphism `q : R ⟶ S`, the `R`-module obtained by restricting the regular left `S`-module along `q`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-009 — `missing.linear_map_from_formula`** (row that the catalogue lacks, V1): a linear map $\mathbb{Q}^n \to \mathbb{Q}^m$ given by a formula linear in its binders, as a morphism of `cat.modules_r` with its kernel and image. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: the lean-categories task that declares `missing.linear_map_from_formula` (none at lean-categories `fc549baa`).
- **FR-010 — `missing.cyclic_module_object`** (row that the catalogue lacks, V1): the $\mathbb{Z}$-module $\mathbb{Z}/n$ as an object of `cat.modules_r`. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: the lean-categories task that declares `missing.cyclic_module_object` (none at lean-categories `fc549baa`).
- **FR-011 — `missing.derivative_linear`** (row that the catalogue lacks, V1): the derivation $d/dx : \mathbb{Q}[x] \to \mathbb{Q}[x]$ as a morphism of $\mathbb{Q}$-modules. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: the lean-categories task that declares `missing.derivative_linear` (none at lean-categories `fc549baa`).
- **FR-012 — Existing registrations of V1** (2). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/modules_r.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `meth.cardinality` | `obj.modules.regular` | `sage-modules` |
  | `meth.cardinality` | `obj.modules.vectors` | `sage-modules` |

### Functional Requirements — V2

- **FR-013 — `obj.sets.bilinear_maps`** (object constructor, V2). Catalogue: The set of bilinear maps between two selected modules, with the selected value module. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.

### Key Entities

- **Category implementation of `cat.modules_r`**: the module `backends/modules_r.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 11 requirements FR-001 to FR-011 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 2 registrations of FR-012 are served by `backends/modules_r.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `modules_r` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel task "Implement Modules Spec V1" (`cat.modules_r`) consumes the version with no kernel-side evaluation of a row of this version.
- **SC-005** (V2): each of the 1 requirements FR-013 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-006** (V2): tier 1 of `modules_r` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-007** (V2): kernel task "Implement Modules Spec V2" (`cat.modules_r`) consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
