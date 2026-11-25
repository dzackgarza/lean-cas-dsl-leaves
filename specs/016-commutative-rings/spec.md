# Feature Specification: Commutative Rings category implementation (`cat.commutative_rings`)

**Feature Branch**: `016-commutative-rings` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.commutative_rings` against the released contract `cas-computation/2`, in versions V1 and V2, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.commutative_rings`.
- **Object**: a commutative ring.
- **Morphism**: a ring homomorphism.
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 50 | 13 |
| V2 | the remaining full-B0 statements of lean-cas-dsl #19 | 2 | 1 |

**V3.** The rows whose home is `cat.commutative_rings` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher works with polynomials over $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$ and $\mathbb{C}$: evaluates them, changes coefficients, takes degrees, derivatives and differentials $d(f) = f'\,dx$, primitives, factors with their unit, roots in the coefficient ring and their multiset, and the companion matrix of a monic polynomial; works with square and rectangular matrices: rows, determinant, trace, rank, kernel, characteristic polynomial and invertibility; works with power series given by their coefficients, reads a coefficient and truncates a series; factors an integer and tests whether an integer is prime; builds the two presentations of $\mathbb{F}_9$ and translates elements between them; reads the Krull dimension of a polynomial ring.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category commutative_rings` starts `backends/commutative_rings.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.commutative_rings` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T221 ("Implement Commutative rings Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.commutative_rings`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies, **Then** the arrow has exactly those endpoints (contract FR-018).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/commutative_rings.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### User Story 2 — V2: the full-B0 computations (Priority: P2)

A researcher builds a polynomial ring in several variables and reads the total degree of a polynomial.

**Why this priority**: the full-B0 statements of lean-cas-dsl #19 that pass through this category need these rows (LV13).

**Independent Test**: `just test-category commutative_rings` starts `backends/commutative_rings.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.commutative_rings` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T258 ("Implement Commutative rings Spec V2"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.commutative_rings`, **When** the backend receives a request at a port of V2, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** an existing registration of V2, **When** the kernel sends its request in protocol 2, **Then** `backends/commutative_rings.py` answers it with the routine of its decision, and no v1 program serves it.
4. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A named presentation arrives with its name and no unfolded definition | `status:"unsupported"`, and the missing datum is a finding against the contract (CONTRIBUTING MTH001); no defining polynomial is written in the source | LV1, LV14 |
| The roots of a polynomial over $\mathbb{C}$ have no radical expression | `status:"unsupported"` with the exact `op` | LV11 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.commutative_rings`** (category structure, V1). The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout.
- **FR-002 — `obj.commutative_rings.integers`** (object constructor, V1). Catalogue: `ℤ` with its canonical commutative ring structure. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-003 — `obj.commutative_rings.rationals`** (object constructor, V1). Catalogue: `ℚ` with its canonical commutative ring structure. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `obj.commutative_rings.integers_mod`** (object constructor, V1). Catalogue: `ZMod n` with its canonical commutative ring structure. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-005 — `fun.commutative_rings.ring`** (functor, V1). Catalogue: The underlying ring of a commutative ring. The implementation MUST realize the object action through a public constructor of the target category and the morphism action at the two image endpoints that the request supplies (K:C23; contract FR-018).
- **FR-006 — `clf.commutative_rings.field`** (classifier, V1). Catalogue: Fields retain the chosen commutative ring structure. The implementation MUST answer the classifier's decision at the supplied object with the decision packet of contract FR-012, and retain the selected structure of the request. Inputs before it: lean-categories T033 (#197).
- **FR-007 — `mor.commutative_rings.integer_coefficients`** (operation, V1). Catalogue: The canonical integer coefficient map into any chosen commutative ring. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-008 — `obj.commutative_rings.f9_x`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-009 — `obj.commutative_rings.f9_y`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-010 — `cmp.f9.translation`** (comparison, V1). The implementation MUST return the components of the selected comparison in both directions, at the endpoints that the request selects.
- **FR-011 — `obj.rings.polynomials`** (object constructor, V1). Catalogue: `R[x]` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-012 — `obj.sets.polynomials`** (object constructor, V1). Catalogue: `R[x]`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-013 — `obj.sets.nonzero_polynomials`** (object constructor, V1). Catalogue: `R[x] ∖ {0}`, the nonzero polynomials. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T023 (#198).
- **FR-014 — `obj.sets.monics`** (object constructor, V1). Catalogue: `Monicₙ(K)`, the monic polynomials of degree `n`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-015 — `mor.sets.polynomial_own_evaluation`** (operation, V1). Catalogue: Evaluation in the selected coefficient ring itself, using its identity map. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-016 — `mor.sets.polynomial_map`** (operation, V1). Catalogue: `map : R[x] → S[x]` along `R → S`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-017 — `mor.sets.polynomial_degree`** (operation, V1). Catalogue: `deg : R[x] → ℕ ∪ {-∞}`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-018 — `mor.sets.polynomial_derivative`** (operation, V1). Catalogue: `d/dx : R[x] → R[x]`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-019 — `mor.sets.krull_dimension`** (operation, V1). Catalogue: The Krull dimension of a commutative ring `A`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T021 (#189).
- **FR-020 — `obj.sets.polynomial_factorization_data`** (object constructor, V1). Catalogue: Reusable factorization data over the selected coefficient ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-021 — `mor.sets.polynomial_factorization`** (operation, V1). Catalogue: Full factorization, unlike `factors`, retains multiplicity and the unit. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-022 — `mor.sets.polynomial_factorization_unit`** (operation, V1). Catalogue: The unit as a polynomial, immediately usable by polynomial operations. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-023 — `mor.sets.polynomial_factors`** (operation, V1). Catalogue: The normalized irreducible factors `R[x] ∖ {0} → 𝒫_fin(R[x])`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-024 — `mor.sets.polynomial_roots`** (operation, V1). Catalogue: The roots `R[x] ∖ {0} → 𝒫_fin(R)`, finitely many for a nonzero polynomial over a domain `R` (Mathlib `Polynomial.roots`, `Polynomial.mem_roots`). The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-025 — `obj.sets.kaehler_polynomials`** (object constructor, V1). Catalogue: `Ω¹_{R[x]/R}`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-026 — `mor.sets.polynomial_differential`** (operation, V1). Catalogue: The universal derivation `d : R[x] → Ω¹_{R[x]/R}`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-027 — `mor.sets.kaehler_scale`** (operation, V1). Catalogue: The module structure `R[x] × Ω¹_{R[x]/R} → Ω¹_{R[x]/R}`, `(p, ω) ↦ p ω`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-028 — `mor.sets.kaehler_primitives`** (operation, V1). Catalogue: The primitives `∫ ω = {g | d g = ω}` of a differential. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-029 — `obj.rings.matrices`** (object constructor, V1). Catalogue: Square matrices with their canonical ring structure, including the selected coefficient ring's addition and multiplication. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-030 — `obj.sets.matrices`** (object constructor, V1). Catalogue: `Matₙ(K)`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-031 — `obj.sets.rectangular_matrices`** (object constructor, V1). Catalogue: The set of all matrices `Fin rows → Fin columns → R` over the selected commutative ring `R`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-032 — `mor.sets.matrix_rows`** (operation, V1). Catalogue: The matrix with the given rows. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-033 — `mor.sets.matrix_det`** (operation, V1). Catalogue: The determinant. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-034 — `mor.sets.matrix_trace`** (operation, V1). Catalogue: The trace. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-035 — `mor.sets.matrix_rank`** (operation, V1). Catalogue: The independence rank of the column module over the selected nontrivial commutative ring (Mathlib `Matrix.rank`). The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-036 — `mor.sets.matrix_ker`** (operation, V1). Catalogue: The kernel `{v | M v = 0}`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T013 (#191), contract T021.
- **FR-037 — `mor.sets.matrix_charpoly`** (operation, V1). Catalogue: The characteristic polynomial `det(x - M)`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-038 — `mor.sets.companion_matrix`** (operation, V1). Catalogue: The companion matrix of a monic `p = xⁿ + Σ_{i<n} pᵢ xⁱ`: ones below the diagonal and `-p₀, …, -pₙ₋₁` in the last column. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-039 — `obj.rings.power_series`** (object constructor, V1). Catalogue: `R[[t]]` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-040 — `obj.sets.power_series`** (object constructor, V1). Catalogue: `R[[t]]`, for an object `R` of commutative rings. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-041 — `mor.sets.power_series_coefficient`** (operation, V1). Catalogue: The coefficient of `tⁿ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-042 — `mor.sets.power_series_of_coefficients`** (operation, V1). Catalogue: `Σ c(n) tⁿ`, the series with the coefficient sequence `c : ℕ → R`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-043 — `mor.sets.successor_power_series_terms`** (operation, V1). Catalogue: For the selected commutative ring `R`, the set map `ℕ → PowerSeries R` sending every index `n` to `PowerSeries.C (n + 1 : R) * PowerSeries.X ^ n`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-044 — `obj.sets.mv_polynomials`** (object constructor, V1). Catalogue: `R[x₀, …, xₙ₋₁]`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T021 (#189).
- **FR-045 — `mor.sets.ufd_factorization`** (operation that lean-categories T068 declares, V1): the factorization of a nonzero integer into a unit and irreducible factors with multiplicities. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T068 (#213), which declares `mor.sets.ufd_factorization` (kernel T329).
- **FR-046 — `mor.sets.is_prime`** (operation that lean-categories T069 declares, V1): primality of an element of a commutative ring ($x$ prime when $(x)$ is a nonzero prime ideal), for $\mathbb{Z}$. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T069 (#214), which declares `mor.sets.is_prime` (kernel T330).
- **FR-047 — `mor.sets.polynomial_root_multiset`** (operation that lean-categories T070 declares, V1): the multiset of roots of a nonzero polynomial over a domain (Mathlib `Polynomial.roots`). The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T070 (#218), which declares `mor.sets.polynomial_root_multiset` (kernel T334).
- **FR-048 — `mor.sets.power_series_truncation`** (operation that lean-categories T071 declares, V1): the truncation $R[[t]] \to R[[t]]/(t^{n})$ with its display $\sum_{k<n} a_k t^k + O(t^{n})$. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T071 (#219), which declares `mor.sets.power_series_truncation` (kernel T335).
- **FR-049 — `incl.sets.power_series_map`** (operation that lean-categories T072 declares, V1): the inclusion $\mathbb{Q}[[t]] \subseteq \mathbb{R}[[t]]$ induced by $\mathbb{Q} \subseteq \mathbb{R}$. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T072 (#220), which declares `incl.sets.power_series_map` (kernel T336).
- **FR-050 — `mor.sets.matrix_is_unit`** (operation that lean-categories T073 declares, V1): membership in the unit group $\mathrm{Mat}_n(K)^{\times}$ as a decided predicate. The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: lean-categories T073 (#221), which declares `mor.sets.matrix_is_unit` (kernel T337).
- **FR-051 — Existing registrations of V1** (13). The implementation MUST move the 13 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V1 into `backends/commutative_rings.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Functional Requirements — V2

- **FR-052 — `obj.rings.mv_polynomials`** (object constructor, V2). Catalogue: `R[x₀, …, xₙ₋₁]` as a ring. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories T021 (#189).
- **FR-053 — `mor.sets.mv_total_degree`** (operation, V2). Catalogue: The total degree. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories T021 (#189), contract T021.
- **FR-054 — Existing registrations of V2** (1). The implementation MUST move the 1 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V2 into `backends/commutative_rings.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Key Entities

- **Category implementation of `cat.commutative_rings`**: the module `backends/commutative_rings.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 50 requirements FR-001 to FR-050 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 13 registrations of FR-051 are served by `backends/commutative_rings.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `commutative_rings` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel T221 ("Implement Commutative rings Spec V1") consumes the version with no kernel-side evaluation of a row of this version.
- **SC-005** (V2): each of the 2 requirements FR-052 and FR-053 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-006** (V2): the 1 registrations of FR-054 are served by `backends/commutative_rings.py` on protocol 2, and no v1 program serves any of them.
- **SC-007** (V2): tier 1 of `commutative_rings` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-008** (V2): kernel T258 ("Implement Commutative rings Spec V2") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
