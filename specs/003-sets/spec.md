# Feature Specification: Sets category implementation (`cat.sets`)

**Feature Branch**: `003-sets` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.sets` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.sets`.
- **Object**: a set (a type `X : Type u`, Mathlib `Type u`).
- **Morphism**: a function $f : X \to Y$.
- **Engine**: the engines of the [plan](plan.md#technical-context), with the routine of each row in its routine table.

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 74 | 31 |

**V3.** The rows whose home is `cat.sets` join V3 by the membership rule of [001](../001-category-implementations/spec.md#the-category-specs) when kernel tasks T140 to T147 produce the classified statements of lean-cas-dsl #20, #21 and #23.

**V2 statements.** No row of `cat.sets` is in V2, so this spec has no V2. The full-B0 statements of lean-cas-dsl #19 whose rows have their latest home in `cat.sets` need only V1 rows; kernel T202 ("Implement Sets Spec V1") accepts them with the V1 statements.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher builds the number sets $\mathbb{N}$, $\mathbb{N}_{>0}$, the primes, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$, $\mathbb{Z}/n$, $(\mathbb{Z}/n)^k$, $\mathrm{Fin}\,n$, finite subsets and power sets; tests equality of elements; applies and composes maps and reads their graphs; forms products, coproducts and pullbacks of sets; takes the direct image of a subset; computes gcd, primality, prime factors and multiplicities of natural numbers, the real and imaginary parts, conjugate and modulus of complex numbers and square roots of reals; sums and multiplies over finite sets; and takes limits, integrals and Taylor expansions of real functions built from $\sin$, $\exp$, $\sqrt{\cdot}$ and $\pi$.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category sets` starts `backends/sets.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.sets` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T202 ("Implement Sets Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.sets`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a request whose computation is a composition of published operations, **When** the backend replies, **Then** the reply is a deferred program of those calls (contract FR-009).
4. **Given** an existing registration of V1, **When** the kernel sends its request in protocol 2, **Then** `backends/sets.py` answers it with the routine of its decision, and no v1 program serves it.
5. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A product has an infinite factor | The apex and the legs are the registered limit with shape-object legs of contract T021; no connection-local projection token | LV14; contract FR-025 |
| SymPy returns an unevaluated integral or limit | The implementation sends the same bound map to Sage `integrate` or `limit` (Maxima) and names both routines (control logic) | LV8, LV11 |
| The symbolic ring cannot decide an equality of two real or complex values | The decision packet `none` | LV11; contract FR-012 |
| The graph of a map with an infinite domain is requested | `status:"unsupported"` with the exact `op` | LV11 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `cat.sets`** (category structure, V1). Catalogue: Sets as types: the bundled category `Type u` (Mathlib `Cat.of (Type u)`), written as the bundle itself and reducible, so that its objects are reducibly types. The implementation MUST realize the identities, the composition and the application of the morphisms of the category at the generated layout. It takes over from the kernel: application and composition of maps.
- **FR-002 — `mor.sets.equality`** (operation, V1). Catalogue: Equality `X × X → Ω`, the characteristic map of the diagonal. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: equality of elements.
- **FR-003 — `obj.sets.truth_values`** (object constructor, V1). Catalogue: `Ω`, the truth values. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-004 — `obj.sets.naturals`** (object constructor, V1). Catalogue: `ℕ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-005 — `obj.sets.positive_naturals`** (object constructor, V1). Catalogue: `ℕ⁺`, the positive naturals. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-006 — `obj.sets.primes`** (object constructor, V1). Catalogue: `ℙ`, the primes. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-007 — `obj.sets.integers`** (object constructor, V1). Catalogue: `ℤ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-008 — `obj.sets.rationals`** (object constructor, V1). Catalogue: `ℚ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-009 — `obj.sets.reals`** (object constructor, V1). Catalogue: `ℝ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-010 — `obj.sets.complexes`** (object constructor, V1). Catalogue: `ℂ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: contract T021.
- **FR-011 — `obj.sets.fin`** (object constructor, V1). Catalogue: `Fin n`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-012 — `obj.sets.integers_mod`** (object constructor, V1). Catalogue: `ℤ/n`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-013 — `obj.sets.integers_mod_power`** (object constructor, V1). Catalogue: `(ℤ/n)^k`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-014 — `obj.sets.cyclic_quotient`** (object constructor, V1). Catalogue: For a natural modulus `n`, the set of integer classes in `ℤ / nℤ`, represented by `Multiplicative (ℤ ⧸ AddSubgroup.zmultiples (n : ℤ))`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-015 — `obj.sets.f9_x`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-016 — `obj.sets.f9_y`** (object constructor, V1). The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-017 — `obj.sets.integer_square_bound`** (object constructor, V1). Catalogue: For `r : ℕ`, the set object with carrier `{n : ℤ // n ^ 2 ≤ (r : ℤ) ^ 2}`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-018 — `obj.sets.vectors`** (object constructor, V1). Catalogue: `Xⁿ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-019 — `obj.sets.finite_subsets`** (object constructor, V1). Catalogue: `𝒫_fin(X)`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares.
- **FR-020 — `obj.sets.power_set`** (object constructor, V1). Catalogue: `𝒫(X)`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories 001 T013 (#191), contract T021.
- **FR-021 — `pow.sets`** (operation, V1). Catalogue: `⊤ : 1 → Ω`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: membership in a subset. Inputs before it: lean-categories 001 T013 (#191), contract T021.
- **FR-022 — `lit.sets.finite_subsets`** (operation, V1). Catalogue: `Finset α` is the type of finite sets of elements of `α`. The implementation MUST return the value of the literal or numeral descriptor at the generated layout.
- **FR-023 — `mor.sets.direct_image`** (operation, V1). Catalogue: Direct image of every subset under the whole supplied function. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories 001 T013 (#191), contract T021.
- **FR-024 — `mor.sets.integer_square_bound_subset`** (operation, V1). Catalogue: For `r : ℕ`, the constant point `Fin 1 → Set ℤ` with value `{n : ℤ | n ^ 2 ≤ (r : ℤ) ^ 2}`, equivalently the closed integer interval `[-r, r]` by `squareBound_eq_Icc`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-025 — `mor.sets.integer_square_bound_admitted`** (operation, V1). Catalogue: For `r : ℕ`, the constant point `Fin 1 → Finset ℤ` representing exactly the finite subset `{n : ℤ | n ^ 2 ≤ (r : ℤ) ^ 2}`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-026 — `obj.sets.continuous_maps`** (object constructor, V1). Catalogue: `C(ℝ)`, the continuous maps `ℝ → ℝ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-027 — `obj.sets.smooth_maps`** (object constructor, V1). Catalogue: `C^∞(ℝ)`, the smooth maps `ℝ → ℝ`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-028 — `obj.sets.convergent_maps_at_infinity`** (object constructor, V1). Catalogue: The maps convergent at `a = ±∞`. The implementation MUST construct the object from the request at the generated layout, with the complete interface that its category declares. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-029 — `num.sets.fin`** (operation, V1). Catalogue: The point `k` of `Fin n`, for `k < n`. The implementation MUST return the value of the literal or numeral descriptor at the generated layout.
- **FR-030 — `mor.sets.tuple_empty`** (operation, V1). Catalogue: The empty tuple `() ∈ X⁰`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-031 — `mor.sets.tuple_cons`** (operation, V1). Catalogue: `(x, v) ↦ (x, v₀, …)`, `X × Xⁿ → Xⁿ⁺¹`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-032 — `incl.sets.naturals_integers`** (operation, V1). Catalogue: `ℕ ⊆ ℤ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-033 — `incl.sets.integers_rationals`** (operation, V1). Catalogue: `ℤ ⊆ ℚ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-034 — `incl.sets.rationals_reals`** (operation, V1). Catalogue: `ℚ ⊆ ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-035 — `incl.sets.reals_complexes`** (operation, V1). Catalogue: `ℝ ⊆ ℂ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-036 — `incl.sets.naturals_degrees`** (operation, V1). Catalogue: `k ∈ ℕ ∪ {-∞}`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-037 — `incl.sets.naturals_krull_dimensions`** (operation, V1). Catalogue: `ℕ ⊆ ℕ∞ ∪ {-∞}`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-038 — `mor.sets.cyclic_quotient_map`** (operation, V1). Catalogue: For `n : ℕ`, the set map `ℤ → quotientCarrier n` sending every integer `k` to its class `[k]` modulo the subgroup `nℤ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-039 — `lim.sets.product`** (operation, V1). Catalogue: Binary products in `Sets`. The implementation MUST return the selected cone or cocone with its apex and all its legs, computed from the selected diagram of the request (K:C23). It takes over from the kernel: the projections of a product. Inputs before it: lean-categories 001 T031 (#187), contract T021.
- **FR-040 — `colim.sets.coproduct`** (operation, V1). Catalogue: Binary coproducts in `Sets`. The implementation MUST return the selected cone or cocone with its apex and all its legs, computed from the selected diagram of the request (K:C23). Inputs before it: lean-categories 001 T031 (#187).
- **FR-041 — `lim.sets.pullback`** (operation, V1). Catalogue: Pullbacks in `Sets`. The implementation MUST return the selected cone or cocone with its apex and all its legs, computed from the selected diagram of the request (K:C23). Inputs before it: lean-categories 001 T031 (#187).
- **FR-042 — `graph.sets`** (operation, V1). Catalogue: The function `X → Y` with graph `l`, which lists each element of `X` exactly once. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: the graph of a map.
- **FR-043 — `cmp.sets.singleton_terminal`** (comparison, V1). Catalogue: The public singleton and this terminal set have their actual point comparison. The implementation MUST return the components of the selected comparison in both directions, at the endpoints that the request selects.
- **FR-044 — `cmp.sets.fin_reversal`** (comparison, V1). Catalogue: The complete reversal isomorphism of the original `Fin n`. The implementation MUST return the components of the selected comparison in both directions, at the endpoints that the request selects.
- **FR-045 — `mor.sets.fin_rev`** (operation, V1). Catalogue: `Fin.rev : Fin n → Fin n`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-046 — `clf.sets.finite`** (classifier, V1). Catalogue: Finite classifier: FintypeCat → Type. The implementation MUST answer the classifier's decision at the supplied object with the decision packet of contract FR-012, and retain the selected structure of the request.
- **FR-047 — `clf.sets.enumerated`** (classifier, V1). Catalogue: A chosen partial-inverse enumeration as a structure classifier on sets. The implementation MUST answer the classifier's decision at the supplied object with the decision packet of contract FR-012, and retain the selected structure of the request.
- **FR-048 — `clf.sets.binary_operation`** (classifier, V1). Catalogue: BinaryOperation classifier: MagmaCat → Type. The implementation MUST answer the classifier's decision at the supplied object with the decision packet of contract FR-012, and retain the selected structure of the request.
- **FR-049 — `prop.is_finite`** (property, V1). The implementation MUST answer the property with the decision packet of contract FR-012 (`none` when the engine cannot establish it).
- **FR-050 — `mor.sets.gcd`** (operation, V1). Catalogue: `gcd : ℤ × ℤ → ℤ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: gcd.
- **FR-051 — `mor.sets.nat_is_prime`** (operation, V1). Catalogue: `n ↦ n is prime`, `ℕ → Ω`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. It takes over from the kernel: primality.
- **FR-052 — `mor.sets.nat_multiplicity`** (operation, V1). Catalogue: `(n, p) ↦ eₚ`, the exponent of the prime `p` in `n ∈ ℕ⁺` (`0` when `p ∤ n`). The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-053 — `mor.sets.nat_prime_factors`** (operation, V1). Catalogue: The prime factors of `n ∈ ℕ⁺` (none for `n = 1`), `ℕ⁺ → 𝒫_fin(ℙ)`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-054 — `mor.sets.complex_re`** (operation, V1). Catalogue: The real part `ℂ → ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-055 — `mor.sets.complex_im`** (operation, V1). Catalogue: The imaginary part `ℂ → ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-056 — `mor.sets.complex_bar`** (operation, V1). Catalogue: Conjugation `ℂ → ℂ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-057 — `mor.sets.complex_abs`** (operation, V1). Catalogue: The absolute value `ℂ → ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-058 — `mor.sets.complex_i`** (operation, V1). Catalogue: The element `i ∈ ℂ`, `1 → ℂ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-059 — `mor.sets.real_pi`** (operation, V1). Catalogue: `π ∈ ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-060 — `mor.sets.real_sqrt`** (operation, V1). Catalogue: The square root `ℝ → ℝ` (`0` below `0`, Mathlib `Real.sqrt`). The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: contract T021.
- **FR-061 — `mor.sets.f9_x_constants`** (operation, V1). Catalogue: The defining coefficient map of the named source presentation. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-062 — `mor.sets.f9_y_constants`** (operation, V1). Catalogue: The defining coefficient map of the named target presentation. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-063 — `bind.sets.finite_sum`** (operation, V1). Catalogue: `f ↦ ∑_{a ∈ A} f(a)`, `Y^X → Y`, at the finite subset `A ∈ 𝒫_fin(X)` (Mathlib `Finset.sum`). The implementation MUST compute the binder from the bound map and the bounds that the request carries. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-064 — `bind.sets.finite_product`** (operation, V1). Catalogue: `f ↦ ∏_{a ∈ A} f(a)`, `Y^X → Y`, at the finite subset `A ∈ 𝒫_fin(X)` (Mathlib `Finset.prod`). The implementation MUST compute the binder from the bound map and the bounds that the request carries. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-065 — `mor.sets.real_sin`** (operation, V1). Catalogue: `sin : ℝ → ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-066 — `mor.sets.real_exp`** (operation, V1). Catalogue: `exp : ℝ → ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-067 — `mor.sets.infinity`** (operation, V1). Catalogue: `∞ = +∞ ∈ ℝ̄ ∖ ℝ`. The implementation MUST compute the operation at its actual domain and reply at the generated result layout.
- **FR-068 — `bind.sets.limit`** (operation, V1). Catalogue: `f ↦ lim_{t → a} f(t)`, the limit at `a ∈ ℝ` of a map convergent there: the value its convergence carries, which is the unique limit (`limit_eq`). The implementation MUST compute the binder from the bound map and the bounds that the request carries. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-069 — `bind.sets.limit_at_infinity`** (operation, V1). Catalogue: `f ↦ lim_{t → a} f(t)` at `a = ±∞`, the unique limit (`limitAtInfinity_eq`). The implementation MUST compute the binder from the bound map and the bounds that the request carries. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-070 — `bind.sets.integral`** (operation, V1). Catalogue: `f ↦ ∫_a^b f(t) dt`, `C(ℝ) → ℝ`, at the bounds `a b ∈ ℝ`: the binder `∫_{a}^{b} e dt`, its arguments the two bounds. The implementation MUST compute the binder from the bound map and the bounds that the request carries. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-071 — `mor.sets.taylor_expansion`** (operation, V1). Catalogue: `(f, a) ↦ Σ f⁽ᵏ⁾(a)/k! tᵏ`, the division by `k! ∈ ℝˣ` being division by a unit. The implementation MUST compute the operation at its actual domain and reply at the generated result layout. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-072 — `bind.sets.power_series_sum`** (operation, V1). Catalogue: The sum of series in `R[[t]]`: `f ↦ ∑_{n ∈ N} f(n)`, the series sum `seriesSum` at the object `powerSeriesTAdic R` (`powerSeriesSum_eq`). The implementation MUST compute the binder from the bound map and the bounds that the request carries. Inputs before it: lean-categories 001 T027 (#190), contract T021.
- **FR-073 — `mor.sets.real_approximation`** (operation that lean-categories 001 T066 declares, V1): a rational approximation $a \in \mathbb{Q}$ of $x \in \mathbb{R}$ within a positive rational tolerance, with the exact source and both tolerances retained. The implementation MUST compute it (LV1, LV14). Inputs before it: lean-categories 001 T066 (#212), which declares `mor.sets.real_approximation` (kernel T328); the workstream of this spec finishes that task first, as a formalization author, and then implements the row.
- **FR-074 — `mor.sets.complex_sqrt`** (operation that lean-categories 001 T067 declares, V1): the principal square root in $\mathbb{C}$ of a negative rational, $z^{1/2}$ with $\arg z \in (-\pi, \pi]$ (lean-categories research D21). The implementation MUST compute it (LV1, LV14). Inputs before it: lean-categories 001 T067 (#215), which declares `mor.sets.complex_sqrt` (kernel T331); the workstream of this spec finishes that task first, as a formalization author, and then implements the row.
- **FR-075 — Existing registrations of V1** (31). The implementation MUST move the 31 registrations of `leaves.json` at `8b181d7` that the plan's table "Registrations that move" lists for V1 into `backends/sets.py` on protocol 2 and the generated interface (LV12; 001 FR-026), with the decision of each row in that table: a hand-rolled, partial or lookup answer is replaced by an engine routine, a leaf-held datum is deleted, and a kept routine moves with its registration.

### Key Entities

- **Category implementation of `cat.sets`**: the module `backends/sets.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 74 requirements FR-001 to FR-074 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches.
- **SC-002** (V1): the 31 registrations of FR-075 are served by `backends/sets.py` on protocol 2, and no v1 program serves any of them.
- **SC-003** (V1): tier 1 of `sets` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-004** (V1): kernel T202 ("Implement Sets Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- The assumptions of the shared feature [001](../001-category-implementations/spec.md#assumptions) apply.
