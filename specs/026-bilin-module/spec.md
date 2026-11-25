# Feature Specification: Formed Modules category implementation (`cat.bilin_module`)

**Feature Branch**: `026-bilin-module` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.bilin_module` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.bilin_module`.
- **Object**: an $R$-module $M$ with a bilinear form $b : M \times M \to W$ (the family `fam.bilin_module` at $R$ and $W$).
- **Morphism**: a linear map that preserves the forms.
- **Built from**: `cat.commutative_rings`, `cat.modules_r` (structural functors and classifier forgets of the catalogue).
- **Engine**: Sage free modules with an inner product matrix (`FreeModule(R, n, inner_product_matrix=G)`, `submodule`, `gram_matrix()`, module homomorphisms) (engine survey, "Bilinear and quadratic modules").

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 15 | 0 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 1 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.bilin_module` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher builds the named formed modules of the catalogue (the degenerate plane, its target and its dotted variant, the rational diagonal form $\langle 2, 3 \rangle$), restricts a form to the kernel of a map with its inclusion, evaluates the pairing, changes the value module along a linear map, forms the selected cones and comparison maps of the pulled-back forms, and forgets a formed module to its module.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category bilin_module` starts `backends/bilin_module.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.bilin_module` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T243 ("Implement Formed modules Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.bilin_module`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher builds a formed module from a module and a bilinear map.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category bilin_module` starts `backends/bilin_module.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.bilin_module` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T262 ("Implement Formed modules Spec V2"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.bilin_module`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A named formed module arrives with its name and no unfolded definition | `status:"unsupported"`; the missing Gram data are a finding against the contract (CONTRIBUTING MTH001) | LV1, LV14 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.bilin_module`** (category structure, V1). The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout.
- **FR-002 — `obj.bilin_module.degenerate_plane`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `obj.bilin_module.degenerate_plane_target`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `obj.bilin_module.degenerate_plane_with_dot`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-005 — `obj.bilin_module.rational_diagonal_2_3`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-006 — `mor.sets.bilin_module_pairing`** (operation, V1). Catalogue: The selected form as a map of sets, retaining the chosen ring, value module and object. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-007 — `fun.bilin_module.forget`** (functor, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-008 — `obj.bilin_module.ordinary_kernel_restriction`** (object constructor, V1). Catalogue: Given a selected commutative ring `R`, value module `W`, formed module `X : BilinModuleCat R W`, target module `Y`, and ordinary module map `f : X.carrierObj ⟶ Y`, form the `W`-valued module on the actual submodule … The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-009 — `mor.bilin_module.ordinary_kernel_inclusion`** (operation, V1). Catalogue: At the selected parameters `R`, `W`, `X`, `Y`, `f`, the formed map from `ordinaryKernelRestriction R W X Y f` to `X` sending each kernel element `⟨x, hx⟩` to its original vector `x`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-010 — `fun.bilin_module.change_value`** (functor, V1). The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018). Inputs before it: lean-categories T029 (#192).
- **FR-011 — `mor.bilin_module.degenerate_plane_map`** (operation, V1). The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-012 — `mor.bilin_module.degenerate_plane_cone`** (operation, V1). The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-013 — `mor.bilin_module.degenerate_plane_paired_cone`** (operation, V1). The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-014 — `mor.bilin_module.pulled_back_forward`** (operation, V1). Catalogue: The forward arrow of `pulledBackIso R W W' a X i`, from `(changeValue R W a).obj (pulledBack R W W' a X i)` to the actual formed object `K`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T029 (#192).
- **FR-015 — `mor.bilin_module.pulled_back_backward`** (operation, V1). Catalogue: The inverse arrow of the same `pulledBackIso`, with exact source `K` and target `(changeValue R W a).obj (pulledBack R W W' a X i)`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T029 (#192).

### Functional Requirements — V2

- **FR-016 — `obj.bilin_module.bilinear_form`** (object constructor, V2). Catalogue: A chosen bilinear map, with its actual scalar, carrier and value modules. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.

### Key Entities

- **Category implementation of `cat.bilin_module`**: the module `backends/bilin_module.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 15 requirements FR-001 to FR-015 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): tier 1 of `bilin_module` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T243 ("Implement Formed modules Spec V1") consumes the version with no kernel-side evaluation of a row of this version.
- **SC-004** (V2): each of the 1 requirements FR-016 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-005** (V2): tier 1 of `bilin_module` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-006** (V2): kernel T262 ("Implement Formed modules Spec V2") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
