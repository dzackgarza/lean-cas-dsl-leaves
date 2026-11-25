# Feature Specification: Bilinear Forms category implementation (`cat.bil_wform`)

**Feature Branch**: `020-bil-wform` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.bil_wform` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.bil_wform`.
- **Object**: an $R$-module with a bilinear form valued in an $R$-module (the family `fam.bil_wform` at a commutative ring $R$).
- **Morphism**: a morphism of the family `fam.bil_wform`: a linear map compatible with the two forms.
- **Built from**: `cat.commutative_rings` (structural functors and classifier forgets of the catalogue).
- **Engine**: Sage integral lattices and torsion quadratic modules (`IntegralLattice`, `dual_lattice`, `discriminant_group`, `FreeModule(..., inner_product_matrix=G)`), PARI `matsnf` through `cypari2` for Smith invariants (engine survey, "Bilinear and quadratic modules", "Lattices (quadratic forms)").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 3 | 5 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 3 | 5 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.bil_wform` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher forms the discriminant of the root lattice $A_n$ as the cokernel of its inclusion into the dual lattice, with the projection, and forgets a form to its module.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category bil_wform` starts `backends/bil_wform.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.bil_wform` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T235 ("Implement Valued bilinear forms Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.bil_wform`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/bil_wform.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher builds the root lattice $A_n$ and a form from a module and a bilinear map, evaluates the pairing, and asks the size of these forms and whether they are abelian as groups.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category bil_wform` starts `backends/bil_wform.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.bil_wform` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T260 ("Implement Valued bilinear forms Spec V2"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.bil_wform`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/bil_wform.py` answers it with the routine of its decision, and no v1 program serves it.
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A cokernel diagram other than the selected parallel pair of the request | The implementation computes the cokernel of the selected pair that the request carries; it does not match the diagram against a named one | LV4 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `mor.bil_wform.root_lattice_a_to_dual`** (operation, V1). Catalogue: `A_n ⊆ A_n^♯`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-002 — `colim.bil_w_form.cokernel`** (operation, V1). Catalogue: Cokernels of formed modules with varying values. The implementation MUST return the selected cone or cocone with its apex and all its legs, computed from the selected diagram of the request (K:C23). Inputs before it: lean-categories T031 (#187).
- **FR-003 — `fun.bil_wform.carrier`** (functor, V1). Catalogue: The carrier functor of formed modules with varying values (`LeanCategories.Modules.Bilinear.Valued.carrierFunctor`). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-004 — Existing registrations of V1** (5). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/bil_wform.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `colim.bil_w_form.cokernel` | `cat.bil_wform` | `sage-discriminant` |
  | `meth.cardinality` | `obj.bil_wform.root_lattice_a_discriminant` | `sage-discriminant` |
  | `meth.cardinality` | `obj.bil_wform.root_lattice_a_dual` | `sage-modules` |
  | `prop.is_commutative` | `obj.bil_wform.root_lattice_a_discriminant` | `gap-groups` |
  | `prop.is_commutative` | `obj.bil_wform.root_lattice_a_dual` | `gap-groups` |

### Functional Requirements — V2

- **FR-005 — `obj.bil_wform.root_lattice_a`** (object constructor, V2). Catalogue: The root lattice `A_n`, on its simple roots. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-006 — `obj.bil_wform.formed`** (object constructor, V2). Catalogue: The same chosen bilinear map in the variable-value category. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-007 — `mor.sets.formed_pairing`** (operation, V2). Catalogue: Evaluate a variable-value form without forgetting its selected value module. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-008 — Existing registrations of V2** (5). The implementation MUST move these registrations of `leaves.json` at `8b181d7` into `backends/bil_wform.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in the plan: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

  | Operation | Input | v1 backend |
  | --- | --- | --- |
  | `meth.cardinality` | `obj.bil_wform.root_lattice_a` | `sage-modules` |
  | `prop.is_abelian` | `obj.bil_wform.root_lattice_a` | `gap-groups` |
  | `prop.is_abelian` | `obj.bil_wform.root_lattice_a_discriminant` | `gap-groups` |
  | `prop.is_abelian` | `obj.bil_wform.root_lattice_a_dual` | `gap-groups` |
  | `prop.is_commutative` | `obj.bil_wform.root_lattice_a` | `gap-groups` |

### Key Entities

- **Category implementation of `cat.bil_wform`**: the module `backends/bil_wform.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 3 requirements FR-001 to FR-003 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 5 registrations of FR-004 are served by `backends/bil_wform.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `bil_wform` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel T235 ("Implement Valued bilinear forms Spec V1") consumes the version with no kernel-side evaluation of a row of this version.
- **SC-005** (V2): each of the 3 requirements FR-005 to FR-007 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-006** (V2): the 5 registrations of FR-008 are served by `backends/bil_wform.py` on protocol 2, and no v1 program serves any of them.
- **SC-007** (V2): tier 1 of `bil_wform` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-008** (V2): kernel T260 ("Implement Valued bilinear forms Spec V2") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
