# Implementation Plan: Sets category implementation (`cat.sets`)

**Branch**: `003-sets` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.sets` in `backends/sets.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage (`sage.sets`, maps and homsets in `Sets()`), Catlab.jl through `juliacall` for the pullback of finite sets, SymPy for the calculus rows with the Sage symbolic ring (Maxima) where SymPy returns an unevaluated form (engine survey, "Sets", "Cross-cutting layer", "Calculus").
**Module**: `backends/sets.py`, run as `/sage/.venv/bin/python3 -m backends.sets` (001 research R3).
**Code dependencies**: none; the module imports only `backends/engine.py`, the SDK and its engines.
**Tests**: `tests/test_sets.py`, `tests/scenarios/sets-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/sets.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
| LV2, LV14 | No acceptance statement or expected answer; kernel tasks are named by ID or title. |
| LV3 | Each row of each version has a port, or a gap record of mathematically new work. |
| LV4 | Each routine computes from the selected data of the request; tier 1 checks their retention. |
| LV5–LV7 | Each row names its engine routine; each version starts with its survey record. |
| LV8 | Dependent inputs arrive as operands, through declared code dependencies or by a kernel request (column "Dependent inputs"). |
| LV12 | Each moved registration has a decision (table "Registrations that move"). |
| LV13 | The survey task of each version follows the versions of the categories that its rows reach. |

Gate result: pass.

## Project Structure

```text
specs/003-sets/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/sets.py
tests/test_sets.py
tests/scenarios/sets-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.sets` | category structure | Sage `Hom(A, B)` in `Sets()` with `SetMorphism`; identity `Hom(A, A).identity()`; composition `g * f`; application `f(x)`; `FiniteSetMaps(A, B)` for maps of finite sets | the selected data that the request carries (LV4) | — |
| FR-002 | `mor.sets.equality` | operation | Sage `==` in the parent of the two operands: exact in `ZZ`, `QQ`, `Zmod(n)`, `AA`, `QQbar`; in `SR`, `bool(x == y)` gives `true`, `bool(x != y)` gives `false`, and otherwise the decision packet is `none` (contract FR-012) | request operands at the generated layout | — |
| FR-003 | `obj.sets.truth_values` | object constructor | the decision packets of contract FR-012 as its points; no engine parent | request operands at the generated layout | — |
| FR-004 | `obj.sets.naturals` | object constructor | Sage `NonNegativeIntegers()` | request operands at the generated layout | — |
| FR-005 | `obj.sets.positive_naturals` | object constructor | Sage `PositiveIntegers()` | request operands at the generated layout | — |
| FR-006 | `obj.sets.primes` | object constructor | Sage `Primes()` | request operands at the generated layout | — |
| FR-007 | `obj.sets.integers` | object constructor | Sage `ZZ` | request operands at the generated layout | — |
| FR-008 | `obj.sets.rationals` | object constructor | Sage `QQ`; a non-integral point in the form of contract T021 (`mor.sets.divide`) | request operands at the generated layout | contract T021 |
| FR-009 | `obj.sets.reals` | object constructor | Sage `RealSet.real_line()` as the set; points are exact values in `AA` or `SR` in the forms of contract T021 | request operands at the generated layout | contract T021 |
| FR-010 | `obj.sets.complexes` | object constructor | points are exact values in `QQbar` or `SR` in the forms of contract T021; the set parent is settled by the survey record of T001 | request operands at the generated layout | contract T021 |
| FR-011 | `obj.sets.fin` | object constructor | Sage `IntegerRange(0, n)` | request operands at the generated layout | — |
| FR-012 | `obj.sets.integers_mod` | object constructor | Sage `Zmod(n)` (Sage gives `ZZ` at $n = 0$) | request operands at the generated layout | — |
| FR-013 | `obj.sets.integers_mod_power` | object constructor | Sage `cartesian_product([Zmod(n)] * k)` | request operands at the generated layout | — |
| FR-014 | `obj.sets.cyclic_quotient` | object constructor | Sage `Zmod(n)` as the quotient set of `ZZ` | request operands at the generated layout | — |
| FR-015 | `obj.sets.f9_x` | object constructor | Sage `PolynomialRing(GF(3), 't').quotient(f)`, with `f` built from the unfolded definition that the request carries (K:C22); no defining polynomial in the source (LV1) | request operands at the generated layout | — |
| FR-016 | `obj.sets.f9_y` | object constructor | Sage `PolynomialRing(GF(3), 't').quotient(f)`, with `f` built from the unfolded definition that the request carries (K:C22); no defining polynomial in the source (LV1) | request operands at the generated layout | — |
| FR-017 | `obj.sets.integer_square_bound` | object constructor | Sage `IntegerRange(-r, r + 1)` with `r = Integer(b).isqrt()` for the bound `b` of the request | request operands at the generated layout | — |
| FR-018 | `obj.sets.vectors` | object constructor | Sage `cartesian_product([X] * n)` | request operands at the generated layout | — |
| FR-019 | `obj.sets.finite_subsets` | object constructor | Sage `Set` values (`sage.sets.set`) as the points; the object is a descriptor of $\mathcal{P}_{\mathrm{fin}}(X)$ | request operands at the generated layout | — |
| FR-020 | `obj.sets.power_set` | object constructor | Sage `Subsets(S)` for a finite `S`; for an infinite `S` a descriptor whose points are the power-object values of contract T021 | request operands at the generated layout | lean-categories T013 (#191), contract T021 |
| FR-021 | `pow.sets` | operation | the power-object maps of lean-categories #191 (`mor.sets.member`, `mor.sets.extent`, `mor.sets.image`, `mor.sets.inverse_image`); Sage `Set` for finite extents | request operands at the generated layout | lean-categories T013 (#191), contract T021 |
| FR-022 | `lit.sets.finite_subsets` | operation | Sage `Set([...])` of the lowered elements | request operands at the generated layout | — |
| FR-023 | `mor.sets.direct_image` | operation | Sage `Sets.MorphismMethods.image` of the map on a finite subset; for an infinite subset the image row of lean-categories #191 in the form of contract T021 | request operands at the generated layout | lean-categories T013 (#191), contract T021 |
| FR-024 | `mor.sets.integer_square_bound_subset` | operation | the inclusion of `IntegerRange(-r, r + 1)` into `ZZ` as a Sage `SetMorphism` | request operands at the generated layout | — |
| FR-025 | `mor.sets.integer_square_bound_admitted` | operation | the admitted element of `IntegerRange(-r, r + 1)` from a supplied integer, by Sage membership `x in IntegerRange(-r, r + 1)` | request operands at the generated layout | — |
| FR-026 | `obj.sets.continuous_maps` | object constructor | a descriptor; its points are bound maps in the binder form of contract T021, lowered to SymPy `Lambda` expressions | request operands at the generated layout | lean-categories T027 (#190), contract T021 |
| FR-027 | `obj.sets.smooth_maps` | object constructor | a descriptor; its points are bound maps in the binder form of contract T021, lowered to SymPy `Lambda` expressions | request operands at the generated layout | lean-categories T027 (#190), contract T021 |
| FR-028 | `obj.sets.convergent_maps_at_infinity` | object constructor | a descriptor; its points are bound maps in the binder form of contract T021, lowered to SymPy `Lambda` expressions | request operands at the generated layout | lean-categories T027 (#190), contract T021 |
| FR-029 | `num.sets.fin` | operation | the element `IntegerRange(0, n)(k)` | request operands at the generated layout | — |
| FR-030 | `mor.sets.tuple_empty` | operation | the empty element of `cartesian_product([])` | request operands at the generated layout | contract T021 |
| FR-031 | `mor.sets.tuple_cons` | operation | the element of `cartesian_product([X, X^n])` from the head and the tail | request operands at the generated layout | contract T021 |
| FR-032 | `incl.sets.naturals_integers` | operation | Sage `ZZ.coerce_map_from(NonNegativeIntegers())` | request operands at the generated layout | — |
| FR-033 | `incl.sets.integers_rationals` | operation | Sage `QQ.coerce_map_from(ZZ)` | request operands at the generated layout | — |
| FR-034 | `incl.sets.rationals_reals` | operation | Sage `AA.coerce_map_from(QQ)` | request operands at the generated layout | contract T021 |
| FR-035 | `incl.sets.reals_complexes` | operation | Sage `QQbar.coerce_map_from(AA)`; the identity of `SR` on real expressions; the result in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-036 | `incl.sets.naturals_degrees` | operation | the native constructor packet `some k` of $\mathbb{N} \cup \{-\infty\}$ (contract T021, `obj.sets.degrees`) | request operands at the generated layout | contract T021 |
| FR-037 | `incl.sets.naturals_krull_dimensions` | operation | the native constructor packet of the target layout of Krull dimensions (contract T021) | request operands at the generated layout | contract T021 |
| FR-038 | `mor.sets.cyclic_quotient_map` | operation | Sage `Zmod(n).coerce_map_from(ZZ)` | request operands at the generated layout | — |
| FR-039 | `lim.sets.product` | operation | Sage `cartesian_product([S, T])` with `cartesian_projection(i)` for the legs; with an infinite factor, the registered limit with shape-object legs of contract T021 | the selected data that the request carries (LV4) | lean-categories T031 (#187), contract T021 |
| FR-040 | `colim.sets.coproduct` | operation | Sage `DisjointUnionEnumeratedSets(Family([S, T]), keepkey=True)` with its injections | the selected data that the request carries (LV4) | lean-categories T031 (#187) |
| FR-041 | `lim.sets.pullback` | operation | Catlab.jl `pullback` of two `FinFunction`s through `juliacall`, with its two legs | the selected data that the request carries (LV4) | lean-categories T031 (#187) |
| FR-042 | `graph.sets` | operation | the graph of a Sage `FiniteSetMaps(A, B)` element, listed over the enumeration of `A`; an infinite domain is `unsupported` | the selected data that the request carries (LV4) | — |
| FR-043 | `cmp.sets.singleton_terminal` | comparison | Sage `FiniteEnumeratedSet([()])` with the unique `SetMorphism` components in both directions | the selected data that the request carries (LV4) | — |
| FR-044 | `cmp.sets.fin_reversal` | comparison | Sage `Permutations(n).long_element()` and its inverse as the two components | the selected data that the request carries (LV4) | — |
| FR-045 | `mor.sets.fin_rev` | operation | Sage `Permutations(n).long_element()`; application by `Permutation.__call__`, composition by `right_action_product` | request operands at the generated layout | — |
| FR-046 | `clf.sets.finite` | classifier | Sage `Parent.is_finite()`; the decision packet `none` where the engine raises `NotImplementedError` | request operands at the generated layout | — |
| FR-047 | `clf.sets.enumerated` | classifier | Sage category membership `X in EnumeratedSets()` | request operands at the generated layout | — |
| FR-048 | `clf.sets.binary_operation` | classifier | the selected binary operation that the request carries; Sage category membership `X in Magmas()` or `X in AdditiveMagmas()` of the engine parent | the selected data that the request carries (LV4) | — |
| FR-049 | `prop.is_finite` | property | Sage `Parent.is_finite()`; the decision packet `none` where the engine raises `NotImplementedError` | request operands at the generated layout | — |
| FR-050 | `mor.sets.gcd` | operation | Sage `gcd(a, b)` on `ZZ` | request operands at the generated layout | — |
| FR-051 | `mor.sets.nat_is_prime` | operation | Sage `Integer.is_prime()` | request operands at the generated layout | — |
| FR-052 | `mor.sets.nat_multiplicity` | operation | Sage `Integer.valuation(p)` | request operands at the generated layout | — |
| FR-053 | `mor.sets.nat_prime_factors` | operation | Sage `Integer.prime_divisors()` | request operands at the generated layout | — |
| FR-054 | `mor.sets.complex_re` | operation | Sage `QQbar` `real()`; `SR` `real_part()` for a transcendental value; the result in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-055 | `mor.sets.complex_im` | operation | Sage `QQbar` `imag()`; `SR` `imag_part()` for a transcendental value; the result in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-056 | `mor.sets.complex_bar` | operation | Sage `QQbar` `conjugate()`; `SR` `conjugate()` for a transcendental value; the result in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-057 | `mor.sets.complex_abs` | operation | Sage `QQbar` `abs()`; `SR` `abs()` for a transcendental value; the result in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-058 | `mor.sets.complex_i` | operation | Sage `QQbar(I)`; the point in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-059 | `mor.sets.real_pi` | operation | Sage `pi` in `SR`; the point in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-060 | `mor.sets.real_sqrt` | operation | Sage `AA(x).sqrt()` for an algebraic `x`; `sqrt(SR(x))` otherwise; the result in the form of contract T021 | request operands at the generated layout | contract T021 |
| FR-061 | `mor.sets.f9_x_constants` | operation | Sage `F.coerce_map_from(F.base_ring())` for the quotient `F` of `obj.sets.f9_x` | request operands at the generated layout | — |
| FR-062 | `mor.sets.f9_y_constants` | operation | Sage `F.coerce_map_from(F.base_ring())` for the quotient `F` of `obj.sets.f9_y` | request operands at the generated layout | — |
| FR-063 | `bind.sets.finite_sum` | operation | no engine arithmetic in this module: a deferred program (contract FR-009) of the addition of the selected structure over the elements of the finite set | the bound map, the finite set and the selected additive structure; returns a deferred program of addition calls (contract FR-009); the kernel routes each call | lean-categories T027 (#190), contract T021 |
| FR-064 | `bind.sets.finite_product` | operation | no engine arithmetic in this module: a deferred program (contract FR-009) of the multiplication of the selected structure over the elements of the finite set | the bound map, the finite set and the selected multiplicative structure; returns a deferred program of multiplication calls (contract FR-009); the kernel routes each call | lean-categories T027 (#190), contract T021 |
| FR-065 | `mor.sets.real_sin` | operation | SymPy `sin`; exact values through Sage `SR` `sin` at a point | request operands at the generated layout | — |
| FR-066 | `mor.sets.real_exp` | operation | SymPy `exp`; exact values through Sage `SR` `exp` at a point | request operands at the generated layout | — |
| FR-067 | `mor.sets.infinity` | operation | SymPy `oo` as the point at infinity of the limit binder | request operands at the generated layout | — |
| FR-068 | `bind.sets.limit` | operation | SymPy `limit(f, t, a)`; Sage `limit(f, t=a)` (Maxima) where SymPy returns an unevaluated `Limit` | the bound map in the binder form of contract T021, lowered to SymPy | lean-categories T027 (#190), contract T021 |
| FR-069 | `bind.sets.limit_at_infinity` | operation | SymPy `limit(f, t, oo)`; Sage `limit(f, t=oo)` (Maxima) where SymPy returns an unevaluated `Limit` | the bound map in the binder form of contract T021, lowered to SymPy | lean-categories T027 (#190), contract T021 |
| FR-070 | `bind.sets.integral` | operation | SymPy `integrate(f, (t, a, b))`; Sage `integrate(f, t, a, b)` (Maxima) where SymPy returns an unevaluated `Integral` | the bound map in the binder form of contract T021, lowered to SymPy | lean-categories T027 (#190), contract T021 |
| FR-071 | `mor.sets.taylor_expansion` | operation | a lazy Sage `LazyPowerSeriesRing(SR, 't')` element whose coefficient $k$ is SymPy `series(f, t, x0, k + 1).coeff(t, k)`, computed when a request demands it (LV25) | the bound map in the binder form of contract T021, lowered to SymPy | lean-categories T027 (#190), contract T021 |
| FR-072 | `bind.sets.power_series_sum` | operation | Sage `LazyPowerSeriesRing(R, 't')` element from the coefficient function of the bound map | the bound map in the binder form of contract T021 | lean-categories T027 (#190), contract T021 |
| FR-073 | `missing.real_approximation` | row that the catalogue lacks | Sage `RealBallField(prec)` evaluation of the exact real at the precision that the tolerance requires; the midpoint by `exact_rational()` | the exact real and the tolerance | the lean-categories task that declares `missing.real_approximation` (none at lean-categories `fc549baa`) |
| FR-074 | `missing.complex_sqrt` | row that the catalogue lacks | Sage `QQbar(x).sqrt()` | the rational operand | the lean-categories task that declares `missing.complex_sqrt` (none at lean-categories `fc549baa`) |

## Computations that move in from the kernel

The kernel removes these evaluations and leaves the no-implementation outcome that names the operation (kernel C22). This implementation supplies them.

| FR | Row | Computation |
| --- | --- | --- |
| FR-001 | `cat.sets` | application and composition of maps |
| FR-002 | `mor.sets.equality` | equality of elements |
| FR-021 | `pow.sets` | membership in a subset |
| FR-039 | `lim.sets.product` | the projections of a product |
| FR-042 | `graph.sets` | the graph of a map |
| FR-050 | `mor.sets.gcd` | gcd |
| FR-051 | `mor.sets.nat_is_prime` | primality |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `bind.sets.integral` | `cat.sets` | `sage-symbolic` | V1 | integrate(f, t, a, b)  [symbolic integration] | Delete the leaf-held datum (the bound map is evaluated by the leaf's own interpreter of composites, mediators and pointwise operations (`function_of`, `apply_map`, sage_symbolic.py:235-293)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `bind.sets.limit` | `cat.sets` | `sage-symbolic` | V1 | limit(f, t=a) | Delete the leaf-held datum (the bound map is evaluated by the leaf's own interpreter of composites, mediators and pointwise operations (`function_of`, `apply_map`, sage_symbolic.py:235-293)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `bind.sets.limit_at_infinity` | `cat.sets` | `sage-symbolic` | V1 | limit(f, t=oo) or limit(f, t=-oo) | Delete the leaf-held datum (the bound map is evaluated by the leaf's own interpreter of composites, mediators and pointwise operations (`function_of`, `apply_map`, sage_symbolic.py:235-293)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `colim.sets.coproduct` | `cat.sets` | `sage-set-limits` | V1 | DisjointUnionEnumeratedSets(Family([S, T]), keepkey=True)  [sage.sets.disjoint_union_enumerated_sets] | Keep the engine routine (LV12). |
| `lim.sets.product` | `cat.sets` | `sage-set-limits` | V1 | cartesian_product([S, T])  [sage.sets.cartesian_product], enumerated; no engine object for an infinite factor | Replace a partly hand-rolled algorithm by the routine of the routine table (LV6, LV12); Delete the leaf-held datum (the tables `COUNTABLE` and `UNCOUNTABLE` decide which named sets are countable (sage_set_limits.py:75-83, :192-199)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `lim.sets.pullback` | `cat.sets` | `sage-set-limits` | V1 | cartesian_product([FiniteEnumeratedSet(dom f), FiniteEnumeratedSet(dom g)]), then a Python filter | Replace a hand-rolled algorithm by the routine of the routine table (LV6, LV12). |
| `mor.sets.complex_abs` | `obj.sets.complexes` | `sage-symbolic` | V1 | SR(x).abs() | Delete the leaf-held datum (points of $\mathbb{R}$ and $\mathbb{C}$ are values of Sage's symbolic ring `SR` (sage_symbolic.py:56)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.complex_bar` | `obj.sets.complexes` | `sage-symbolic` | V1 | SR(x).conjugate() | Delete the leaf-held datum (points of $\mathbb{R}$ and $\mathbb{C}$ are values of Sage's symbolic ring `SR` (sage_symbolic.py:56)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.complex_im` | `obj.sets.complexes` | `sage-symbolic` | V1 | SR(x).imag_part() | Delete the leaf-held datum (points of $\mathbb{R}$ and $\mathbb{C}$ are values of Sage's symbolic ring `SR` (sage_symbolic.py:56)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.complex_re` | `obj.sets.complexes` | `sage-symbolic` | V1 | SR(x).real_part() | Delete the leaf-held datum (points of $\mathbb{R}$ and $\mathbb{C}$ are values of Sage's symbolic ring `SR` (sage_symbolic.py:56)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.equality` | `mor.sets.equality` | `sage-symbolic` | V1 | bool(x == y) in the decoded Sage parent | Delete the leaf-held datum (on `SR` the value `False` also means that Sage did not prove the equality (sage_symbolic.py:561)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.f9_x_constants` | `mor.sets.f9_x_constants` | `sage-presentations` | V1 | F.coerce_map_from(F.base_ring())  [coercion map GF(3) -> F] | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.f9_x_constants` | `obj.sets.integers_mod` | `sage-presentations` | V1 | F.coerce_map_from(F.base_ring())  [coercion map GF(3) -> F] | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.f9_y_constants` | `mor.sets.f9_y_constants` | `sage-presentations` | V1 | F.coerce_map_from(F.base_ring())  [coercion map GF(3) -> F] | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.f9_y_constants` | `obj.sets.integers_mod` | `sage-presentations` | V1 | F.coerce_map_from(F.base_ring())  [coercion map GF(3) -> F] | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.fin_rev` | `mor.sets.fin_rev` | `sage-fin-rev` | V1 | Permutation([n, ..., 1])  [sage.combinat.permutation]; composition by right_action_product; application by Permutation.__call__ | Delete the leaf-held datum (the definition of the reversal is the image list written in the leaf (sage_fin_rev.py:22 `Permutation(list(range(n, 0, -1)))`)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.nat_prime_factors` | `obj.sets.positive_naturals` | `sage-symbolic` | V1 | Integer.prime_divisors() | Keep the engine routine (LV12). |
| `mor.sets.real_sqrt` | `obj.sets.reals` | `sage-symbolic` | V1 | sqrt(SR(x)) | Delete the leaf-held datum (points of $\mathbb{R}$ and $\mathbb{C}$ are values of Sage's symbolic ring `SR` (sage_symbolic.py:56)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.sets.complexes` | `sage` | V1 | CC.is_finite()  [Parent.is_finite] | Delete the leaf-held datum (the leaf models the set by the 53-bit floating-point field `CC` (sage_backend.py:44-45)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.sets.f9_x` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).is_finite() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.sets.f9_y` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).is_finite() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.sets.fin` | `sage` | V1 | IntegerRange(0, n).is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.sets.integers` | `sage` | V1 | ZZ.is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.sets.integers_mod` | `gap` | V1 | IsFinite(ZmodnZ(n), or Integers at n = 0) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); Delete the leaf-held datum (`ZMod 0` is $\mathbb{Z}$ by a rule of the leaf (gap_backend.py:33)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.sets.integers_mod_power` | `gap` | V1 | IsFinite(FullRowModule(ZmodnZ(n), k)) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1); Delete the leaf-held datum (`ZMod 0` is $\mathbb{Z}$ by a rule of the leaf (gap_backend.py:33)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.sets.naturals` | `sage` | V1 | NonNegativeIntegers().is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.sets.permutations` | `gap-groups` | V1 | IsFinite(SymmetricGroup(n)) | Replace the GAP routine by the Sage routine on the value of this module's lowering table (one lowering table, LV1). |
| `prop.is_finite` | `obj.sets.positive_naturals` | `sage` | V1 | PositiveIntegers().is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.sets.primes` | `sage` | V1 | Primes().is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.sets.rationals` | `sage` | V1 | QQ.is_finite()  [Parent.is_finite] | Keep the engine routine (LV12). |
| `prop.is_finite` | `obj.sets.reals` | `sage` | V1 | RR.is_finite()  [Parent.is_finite] | Delete the leaf-held datum (the leaf models the set by the 53-bit floating-point field `RR` (sage_backend.py:44-45)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |

| Version | Registrations |
| --- | ---: |
| V1 | 31 |
| Total | 31 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/sage_fin_rev.py` | V1 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Sets"; "Cross-cutting layer: parents, morphisms, functors"; "Calculus: limits, series, derivatives, integrals"; "Finite sets, countable sets, enumerated sets"; "Boolean algebras and power sets".

The survey names no exact engine parent for the set $\mathbb{C}$; the survey record of T001 settles the lowering of `obj.sets.complexes`.

## Complexity Tracking

No constitution violation needs a justification.
