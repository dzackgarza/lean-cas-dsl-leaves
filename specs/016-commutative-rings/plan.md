# Implementation Plan: Commutative Rings category implementation (`cat.commutative_rings`)

**Branch**: `016-commutative-rings` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.commutative_rings` in `backends/commutative_rings.py` as glue over the engine routines of the routine table below, in versions V1 and V2, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage polynomial, power-series, quotient and matrix rings (`PolynomialRing`, `LazyPowerSeriesRing`, `quotient`, `MatrixSpace`), with Singular inside Sage for several variables and PARI through Sage for factorization (engine survey, "Rings and commutative rings", "Polynomial rings", "Linear algebra").
**Module**: `backends/commutative_rings.py`, run as `/sage/.venv/bin/python3 -m backends.commutative_rings` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/rings.py` (spec 015), `backends/sets.py` (spec 003). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_commutative_rings.py`, `tests/scenarios/commutative_rings-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/commutative_rings.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
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
specs/016-commutative-rings/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/commutative_rings.py
tests/test_commutative_rings.py
tests/scenarios/commutative_rings-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `cat.commutative_rings` | category structure | Sage ring homomorphisms between commutative rings; identity and composition | the selected data that the request carries (LV4) | — |
| FR-002 | `obj.commutative_rings.integers` | object constructor | Sage `ZZ` | request operands at the generated layout | — |
| FR-003 | `obj.commutative_rings.rationals` | object constructor | Sage `QQ` | request operands at the generated layout | — |
| FR-004 | `obj.commutative_rings.integers_mod` | object constructor | Sage `Zmod(n)` | request operands at the generated layout | — |
| FR-005 | `fun.commutative_rings.ring` | functor | object action: the same Sage ring to the public constructor of `cat.rings`; morphism action: the homomorphism at the two image endpoints | the source arrow and both image endpoints (contract FR-018) | — |
| FR-006 | `clf.commutative_rings.field` | classifier | Sage `R.is_field()`; the decision packet `none` where the engine raises `NotImplementedError` | request operands at the generated layout | lean-categories T033 (#197) |
| FR-007 | `mor.commutative_rings.integer_coefficients` | operation | Sage `R.coerce_map_from(ZZ)` | the parameter commutative ring at the generated layout | — |
| FR-008 | `obj.commutative_rings.f9_x` | object constructor | Sage `PolynomialRing(GF(3), 't').quotient(f)`, with `f` from the unfolded definition that the request carries (K:C22) | request operands at the generated layout | — |
| FR-009 | `obj.commutative_rings.f9_y` | object constructor | Sage `PolynomialRing(GF(3), 't').quotient(f)`, with `f` from the unfolded definition that the request carries (K:C22) | request operands at the generated layout | — |
| FR-010 | `cmp.f9.translation` | comparison | Sage quotient-ring homomorphisms `F.hom([g], E)` in both directions, with the generator image `g` from the unfolded definition that the request carries; native composition of the selected comparisons | the selected data that the request carries (LV4) | — |
| FR-011 | `obj.rings.polynomials` | object constructor | Sage `PolynomialRing(K, 'x')` | the parameter commutative ring at the generated layout; descriptors lowered by the lowering table of `backends/rings.py` (LV8, second option) | — |
| FR-012 | `obj.sets.polynomials` | object constructor | Sage `PolynomialRing(K, 'x')` as a set | the parameter commutative ring at the generated layout | — |
| FR-013 | `obj.sets.nonzero_polynomials` | object constructor | the nonzero elements of `PolynomialRing(K, 'x')`, admitted by `p != 0` | the parameter commutative ring at the generated layout | lean-categories T023 (#198) |
| FR-014 | `obj.sets.monics` | object constructor | the monic elements of `PolynomialRing(K, 'x')`, admitted by `p.is_monic()` | the parameter commutative ring at the generated layout | — |
| FR-015 | `mor.sets.polynomial_own_evaluation` | operation | Sage evaluation `p(a)` at an element of the coefficient ring | request operands at the generated layout | — |
| FR-016 | `mor.sets.polynomial_map` | operation | Sage `Polynomial.change_ring(S)` along the selected ring homomorphism | the selected data that the request carries (LV4) | — |
| FR-017 | `mor.sets.polynomial_degree` | operation | Sage `Polynomial.degree()`; the value in $\mathbb{N} \cup \{-\infty\}$ as the native constructor packet of contract T021 | request operands at the generated layout | contract T021 |
| FR-018 | `mor.sets.polynomial_derivative` | operation | Sage `Polynomial.derivative()` | request operands at the generated layout | — |
| FR-019 | `mor.sets.krull_dimension` | operation | Sage `R.krull_dimension()` | request operands at the generated layout | lean-categories T021 (#189) |
| FR-020 | `obj.sets.polynomial_factorization_data` | object constructor | Sage `Factorization` values: the unit and the irreducible factors with their multiplicities | request operands at the generated layout | — |
| FR-021 | `mor.sets.polynomial_factorization` | operation | Sage `Polynomial.factor()` | request operands at the generated layout | — |
| FR-022 | `mor.sets.polynomial_factorization_unit` | operation | Sage `Factorization.unit()` | request operands at the generated layout | — |
| FR-023 | `mor.sets.polynomial_factors` | operation | Sage `Polynomial.factor()` over the coefficient ring (`QQbar` for $\mathbb{C}$), as the finite set of its irreducible factors; algebraic coefficients in the forms of contract T021 | request operands at the generated layout | contract T021 |
| FR-024 | `mor.sets.polynomial_roots` | operation | Sage `Polynomial.roots(multiplicities=False)` in the coefficient ring (`QQbar` for $\mathbb{C}$); each root in the forms of contract T021 through `radical_expression()` | request operands at the generated layout | contract T021 |
| FR-025 | `obj.sets.kaehler_polynomials` | object constructor | the coefficient polynomial of `dx` in `PolynomialRing(K, 'x')`, in the Kähler form of contract T021 | request operands at the generated layout | contract T021 |
| FR-026 | `mor.sets.polynomial_differential` | operation | Sage `Polynomial.derivative()`, as the differential in the Kähler form of contract T021 | request operands at the generated layout | contract T021 |
| FR-027 | `mor.sets.kaehler_scale` | operation | Sage polynomial `*` on the coefficient of `dx` | request operands at the generated layout | contract T021 |
| FR-028 | `mor.sets.kaehler_primitives` | operation | Sage `Polynomial.integral()` for one primitive; the set of primitives as that primitive with the constants of the coefficient ring, at the layout of the catalogue row | request operands at the generated layout | contract T021 |
| FR-029 | `obj.rings.matrices` | object constructor | Sage `MatrixSpace(K, n)` | the parameter commutative ring at the generated layout | contract T021 |
| FR-030 | `obj.sets.matrices` | object constructor | Sage `MatrixSpace(K, n)` as a set | the parameter commutative ring at the generated layout | contract T021 |
| FR-031 | `obj.sets.rectangular_matrices` | object constructor | Sage `MatrixSpace(K, m, n)` as a set | the parameter commutative ring at the generated layout | contract T021 |
| FR-032 | `mor.sets.matrix_rows` | operation | Sage `matrix(K, rows)` from the rows that `mor.sets.tuple_cons` and `mor.sets.tuple_empty` build | request operands at the generated layout | contract T021 |
| FR-033 | `mor.sets.matrix_det` | operation | Sage `Matrix.det()` | request operands at the generated layout | — |
| FR-034 | `mor.sets.matrix_trace` | operation | Sage `Matrix.trace()` | request operands at the generated layout | — |
| FR-035 | `mor.sets.matrix_rank` | operation | Sage `Matrix.rank()` | request operands at the generated layout | — |
| FR-036 | `mor.sets.matrix_ker` | operation | Sage `Matrix.right_kernel()`, as a subset in the power-object form of contract T021 | request operands at the generated layout | lean-categories T013 (#191), contract T021 |
| FR-037 | `mor.sets.matrix_charpoly` | operation | Sage `Matrix.charpoly()` | request operands at the generated layout | — |
| FR-038 | `mor.sets.companion_matrix` | operation | Sage `companion_matrix(p, format=...)` with the format of the catalogue row's declaration, fixed by the survey record of T001 | request operands at the generated layout | contract T021 |
| FR-039 | `obj.rings.power_series` | object constructor | Sage `LazyPowerSeriesRing(K, 't')` | the parameter commutative ring at the generated layout | — |
| FR-040 | `obj.sets.power_series` | object constructor | Sage `LazyPowerSeriesRing(K, 't')` as a set | the parameter commutative ring at the generated layout | — |
| FR-041 | `mor.sets.power_series_coefficient` | operation | the coefficient `f[k]` of a Sage lazy power series, computed when a request demands it (LV25) | request operands at the generated layout | — |
| FR-042 | `mor.sets.power_series_of_coefficients` | operation | Sage `LazyPowerSeriesRing(K, 't')(c)` from the coefficient function `c` of the request | request operands at the generated layout | — |
| FR-043 | `mor.sets.successor_power_series_terms` | operation | the terms `f[k] * t**k` of a Sage lazy power series, as a lazy family; the survey record of T001 checks the layout of the catalogue row | request operands at the generated layout | — |
| FR-044 | `obj.sets.mv_polynomials` | object constructor | Sage `PolynomialRing(K, names)` as a set (Singular inside Sage) | the parameter commutative ring at the generated layout | lean-categories T021 (#189) |
| FR-045 | `missing.ufd_factorization` | row that the catalogue lacks | Sage `Integer.factor()` with `Factorization.unit()` | the integer operand | the lean-categories task that declares `missing.ufd_factorization` (none at lean-categories `fc549baa`) |
| FR-046 | `missing.ufd_prime` | row that the catalogue lacks | Sage `ZZ.ideal(x).is_prime()` with the nonzero condition of the catalogue row | the integer operand | the lean-categories task that declares `missing.ufd_prime` (none at lean-categories `fc549baa`) |
| FR-047 | `missing.root_multiset` | row that the catalogue lacks | Sage `Polynomial.roots(multiplicities=True)` | the polynomial operand | the lean-categories task that declares `missing.root_multiset` (none at lean-categories `fc549baa`) |
| FR-048 | `missing.series_truncation` | row that the catalogue lacks | Sage lazy power series `truncate(n)` and `add_bigoh(n)` | the series and the exponent | the lean-categories task that declares `missing.series_truncation` (none at lean-categories `fc549baa`) |
| FR-049 | `missing.power_series_inclusion` | row that the catalogue lacks | Sage coercion `LazyPowerSeriesRing(AA, 't').coerce_map_from(LazyPowerSeriesRing(QQ, 't'))` | the two coefficient rings | the lean-categories task that declares `missing.power_series_inclusion` (none at lean-categories `fc549baa`) |
| FR-050 | `missing.matrix_inverse_domain` | row that the catalogue lacks | Sage `Matrix.is_invertible()` | the matrix operand | the lean-categories task that declares `missing.matrix_inverse_domain` (none at lean-categories `fc549baa`) |

### V2

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-052 | `obj.rings.mv_polynomials` | object constructor | Sage `PolynomialRing(K, names)` (Singular inside Sage) | the parameter commutative ring at the generated layout | lean-categories T021 (#189) |
| FR-053 | `mor.sets.mv_total_degree` | operation | Sage `MPolynomial.total_degree()`; the value at $0$ is the value that the catalogue row declares, in the form of contract T021 | request operands at the generated layout | lean-categories T021 (#189), contract T021 |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `cmp.f9.translation` | `obj.commutative_rings.f9_x` | `sage-presentations` | V1 | F.hom([E.gen() + E(shift)], E)  [quotient-ring homomorphism], applied to the point | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75); the image of the generator is the literal shift $2$ or $-2$ (sage_presentations.py:147)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `cmp.f9.translation` | `obj.commutative_rings.f9_y` | `sage-presentations` | V1 | F.hom([E.gen() + E(shift)], E)  [quotient-ring homomorphism], applied to the point | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75); the image of the generator is the literal shift $2$ or $-2$ (sage_presentations.py:147)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.commutative_rings.f9_x` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).cardinality() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `meth.cardinality` | `obj.commutative_rings.f9_y` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).cardinality() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.companion_matrix` | `obj.sets.monics` | `sage-symbolic` | V1 | companion_matrix(p, format="right")  [sage.matrix.special] | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.polynomial_degree` | `obj.sets.polynomials` | `sage-symbolic` | V1 | Polynomial.degree() | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92); the degree of $0$ is answered `none` (sage_symbolic.py:466)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.polynomial_derivative` | `obj.sets.polynomials` | `sage-symbolic` | V1 | Polynomial.derivative() | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.polynomial_differential` | `obj.sets.polynomials` | `sage-symbolic` | V1 | Polynomial.derivative(), answered as the composite with `mor.sets.kaehler_from_coordinate` | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.polynomial_factors` | `obj.sets.nonzero_polynomials` | `sage-symbolic` | V1 | Polynomial.factor() | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.polynomial_map` | `obj.sets.polynomials` | `sage-symbolic` | V1 | Polynomial.change_ring(S) | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.polynomial_roots` | `obj.sets.nonzero_polynomials` | `sage-symbolic` | V1 | Polynomial.roots(multiplicities=False); radical_expression() for AA/QQbar | Delete the leaf-held datum (coefficients in $\mathbb{R}$ and $\mathbb{C}$ are read in `AA` and `QQbar` (sage_symbolic.py:89-92)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.commutative_rings.f9_x` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).is_finite() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `prop.is_finite` | `obj.commutative_rings.f9_y` | `sage-presentations` | V1 | PolynomialRing(GF(3), 't').quotient(modulus).is_finite() | Delete the leaf-held datum (the two defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ are literals of the leaf (sage_presentations.py:75)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |
| `mor.sets.mv_total_degree` | `obj.sets.mv_polynomials` | `sage-symbolic` | V2 | MPolynomial.total_degree() | Delete the leaf-held datum (the total degree of $0$ is answered $0$ (sage_symbolic.py:535 `return max(int(d), 0)`)); the routine runs on the engine value of this module's lowering table or of the request's data (LV1). |

| Version | Registrations |
| --- | ---: |
| V1 | 13 |
| V2 | 1 |
| Total | 14 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/sage_presentations.py` | V1 |
| `backends/sage_symbolic.py` | V2 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Rings and commutative rings"; "Polynomial rings"; "Linear algebra: vectors, matrices, kernels, determinants"; "Fields".

## Complexity Tracking

No constitution violation needs a justification.
