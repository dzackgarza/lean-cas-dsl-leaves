# Research: Category implementations for the computational milestones

Each decision names its source. The facts about engines and the container come from the engine
survey of 2026-11-25 (lean-cas-dsl `specs/001-categorical-research-language/research/engine-survey.md`,
marks [C] verified in the container, [W] read in a web source). The facts about this
repository's registrations come from `leaves.json` at `8b181d7`, equal to `efecce8`.

## Decisions

**R1. Interpreter and SDK.** Decision: every backend runs as
`/sage/.venv/bin/python3 -m backends.<program>`, in the repository root. `just setup` installs
the locked dependencies of `pyproject.toml` (the contract package at tag `v2.0.0`, with the
SDK and its `pydantic`) for that interpreter into `.deps/`:
`uv export --frozen --no-dev --format requirements-txt | uv pip install --python /sage/.venv/bin/python3 --target .deps -r -`.
The test harness puts `.deps` on `PYTHONPATH`; in production the kernel puts the `python`
directory of the contract revision that it pins on `PYTHONPATH` (`README.md`), and kernel T105
checks that it is the same release. Sources: LV16, LV21; survey "Container result" (SageMath
importable from `/sage/.venv/bin/python3` [C], Python 3.14.10 [C], no passagemath [C]);
contract plan "Technical Context" (`pydantic` is the SDK's frame-model dependency, `uv sync
--frozen`). Rejected: a second virtual environment that must import Sage, because the survey
shows Sage only in `/sage/.venv` and a derived environment's access to its site packages is
not established by any record.

**R2. Julia packages.** Decision: `Project.toml` and `Manifest.toml` at the repository root
declare Catlab.jl 0.17.7 and Oscar.jl 1.8.2; `just setup` runs
`julia --project=. -e 'using Pkg; Pkg.instantiate()'`. `backends/engine.py` sets
`PYTHON_JULIACALL_EXE=/usr/local/bin/julia` and `PYTHON_JULIACALL_PROJECT` to the repository
root in its own process before it imports `juliacall`. Sources: kernel plan row T200 (Catlab.jl
"declared in the Julia project of the leaf repository"); survey: `juliacall` 0.9.36 and Julia
1.12.7 [C], Catlab source in the depot but not in the default project [C], `juliacall` can use an
existing Julia through those two variables [W S44].

**R3. One program per milestone.** Decision: each requirement FR-001 to FR-025 has one backend
program (two where a second engine must not share the Sage process, R6). Reasons: the kernel
consumes a milestone as a unit; one process keeps one engine session; a tier 1 test of one
milestone starts one program (LV16). C23 requires no process per category.

**R4. The v1 programs leave the manifest at setup.** Decision: the setup task rewrites
`leaves.json` to the protocol-2 form with only protocol-2 programs. The v1 programs stay in
`backends/` as the source of their moves and are trashed by the task that moves their last
registration (plan, milestone map). Reasons: the contract admits a manifest all or none and
requires `preferredRoutes` on every registration (contract FR-004, T005); a v1 `ready` frame
fails negotiation (contract FR-002).

**R5. `lim.sets.product` moves with sets.** Decision: FR-001 moves it, not FR-008. Reason: the
kernel moves the projections of a product into its sets milestone (kernel plan row T200), and
the projections are the legs of the product cone of `lim.sets.product`; `cat.sets` owns the
operation (LV3).

**R6. Engines by milestone.** The engine of each requirement is the kernel plan row and the
survey recommendation for its family ("Recommendation summary"). Three choices are made here:

- Preorders (FR-003): GAP Digraphs (`IsPreorderDigraph`, loadable [C]); Sage has no preorder
  category in the survey's index.
- Modules over polynomial rings (FR-023): Macaulay2 1.24.11 through `sage.interfaces.macaulay2`,
  a separate process. Rejected: Oscar inside the Sage process, because Oscar loads its own GAP,
  Singular and FLINT, untested beside Sage's copies (survey, constraint 5).
- Hecke (FR-024, FR-025): `forms_over_rings_hecke.py` and `lattices_hecke.py` load Oscar through
  `juliacall` and import no Sage module, for the same reason. Catlab.jl loads none of those
  libraries, so it stays in the Sage process of FR-001 and FR-018.

**R7. Operations of another category.** Decision: a program computes the operations of its own
categories; for an operation of another category it asks the kernel by an adaptive suspension
(LV8, third option; contract FR-010). Rejected: importing another program's code, because each
program would then carry the engine closure of the other (LV16).

**R8. Lowering tables.** Decision: each program has one table from the named-object
descriptors of its categories to engine constructors (for example `obj.sets.integers` to `ZZ`,
`obj.bil_wform.root_lattice_a` at $n$ to Sage's root lattice of type $A_n$ with the sign of the
catalogue row). The literal Gram matrices of $A_n$, the literal ranks of $A_n$ and $E_8$, the two
tables from named sets to parents and the two countability tables are deleted (FR-034; kernel
record `existing-leaves.md`, section 1.5).

**R9. Protocol peer for tests.** Decision: `just setup` checks that the contract checkout
`/repos/lean-cas-dsl-leaf-contracts` is at the declared tag (`git describe --exact-match`) and
runs `lake build cas-peer` there; it fails when the checkout is at another revision. The harness
calls that binary. Sources: contract FR-020 (`lake exe cas-peer`); one checkout per repository
(`~/gitclones/<repo>`, seen as `/repos/<repo>` in the container).

**R10. Logs and timing records.** Decision: `tests/conftest.py` writes
`tests/logs/<UTC>-<revision>.log` with the pytest report and each backend's standard error, and
appends one JSON line per test and one per handled request to `tests/timing/records.jsonl`
([data-model.md](data-model.md), "Timing record"). Each backend writes one standard-error line
per request with its elapsed time and routine (contract FR-023 format for the SDK lines).
Sources: LV22, LV23; contract plan (`tests/conftest.py` writes logs and records).

**R11. Where tier 1 runs.** Decision: `just test` and `just test-category` run inside the
research container; `test-push` runs `just test` there through the host launcher of the shared
container guide (`AGENTS.md`); `test-commit` and CI keep the manifest and compilation check,
because the CI runner has no research container. Sources: LV17, LV20, LV21.

**R12. Undeclared wire forms.** Decision: the registrations whose answers need a form that the
contract does not declare (FR-033) are not registered until the contract declares the form.
Affected moves: `mor.sets.complex_abs`, `mor.sets.complex_bar`, `mor.sets.complex_im`,
`mor.sets.complex_re`, `mor.sets.real_sqrt`, `bind.sets.integral`, `bind.sets.limit`,
`bind.sets.limit_at_infinity` (FR-004); `mor.sets.polynomial_degree`,
`mor.sets.polynomial_differential`, `mor.sets.companion_matrix`, `mor.sets.polynomial_roots`
(FR-006); `mor.sets.span` (FR-010); `lim.sets.product` with an infinite factor (FR-001).
Source: `DEFECTS.md`, section of 2026-10-21; LV14; RC8.

## Survey record

LV7 fixes the content. Each milestone task completes its section before its implementation:
one row for each part of the generated interface of its categories, with the routine, the
engine version or revision, the decision (use, fallback, reject) and the reasons, and one row
for each gap with its searches. The starting facts of each family are those of the kernel
survey, cited by section; they are not repeated here.

Row format:

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |

| FR | Survey sections that start the record |
| --- | --- |
| FR-001 | Sets; Cardinals; Cross-cutting layer (Catlab.jl) |
| FR-002 | Finite sets, countable sets, enumerated sets |
| FR-003 | Order structures |
| FR-004 | Magmas, semigroups, monoids; Groups; Semirings; Rings and commutative rings; Calculus |
| FR-005 | Groups; Group-valued constructions |
| FR-006 | Rings and commutative rings; Polynomial rings; Linear algebra |
| FR-007 | Polynomial rings (power series) |
| FR-008 | Modules; Linear algebra |
| FR-009 | Bilinear and quadratic modules; Lattices (quadratic forms) |
| FR-010 | Fields; Linear algebra |
| FR-011 | Modules |
| FR-012 | Modules; Linear algebra |
| FR-013 | Bilinear and quadratic modules |
| FR-014 | Calculus |
| FR-015 | Groups |
| FR-016 | Boolean algebras and power sets; Order structures |
| FR-017 | Lattices (quadratic forms) |
| FR-018 | Sets; Pointed sets; Cross-cutting layer; crystals are not in the survey and are surveyed first |
| FR-019 | Order structures; Cardinals (SymPy ordinals) |
| FR-020 | Magmas, semigroups, monoids; Algebras |
| FR-021 | Algebras |
| FR-022 | none: `sage.schemes` is not in the survey and is surveyed first |
| FR-023 | Modules |
| FR-024 | Bilinear and quadratic modules; cusps of `sage.modular` are surveyed first |
| FR-025 | Bilinear and quadratic modules; Lattices (quadratic forms); Group-valued constructions |

## Registrations that move

One row for each `(operation, backend)` of `leaves.json` at `8b181d7`, with its input forms and
the requirement that moves it. The total is 115.

| FR | Operation | v1 backend | Count | Input forms |
| --- | --- | --- | --- | --- |
| FR-001 | `colim.sets.coproduct` | `sage-set-limits` | 1 | `cat.sets` |
| FR-001 | `lim.sets.product` | `sage-set-limits` | 1 | `cat.sets` |
| FR-001 | `lim.sets.pullback` | `sage-set-limits` | 1 | `cat.sets` |
| FR-001 | `meth.cardinality` | `gap` | 2 | `obj.sets.integers_mod`, `obj.sets.integers_mod_power` |
| FR-001 | `meth.cardinality` | `gap-groups` | 1 | `obj.sets.permutations` |
| FR-001 | `meth.cardinality` | `sage` | 6 | `obj.sets.fin`, `obj.sets.naturals`, `obj.sets.positive_naturals`, `obj.sets.primes`, `obj.sets.integers`, `obj.sets.rationals` |
| FR-001 | `meth.cardinality` | `sage-power-set` | 1 | `obj.sets.power_set` |
| FR-001 | `meth.cardinality` | `sage-presentations` | 2 | `obj.sets.f9_x`, `obj.sets.f9_y` |
| FR-001 | `meth.cardinality` | `sage-set-limits` | 1 | `cat.sets` |
| FR-001 | `mor.sets.equality` | `sage-symbolic` | 1 | `mor.sets.equality` |
| FR-001 | `mor.sets.fin_rev` | `sage-fin-rev` | 1 | `mor.sets.fin_rev` |
| FR-001 | `prop.is_finite` | `gap` | 2 | `obj.sets.integers_mod`, `obj.sets.integers_mod_power` |
| FR-001 | `prop.is_finite` | `gap-groups` | 1 | `obj.sets.permutations` |
| FR-001 | `prop.is_finite` | `sage` | 8 | `obj.sets.fin`, `obj.sets.naturals`, `obj.sets.positive_naturals`, `obj.sets.primes`, `obj.sets.integers`, `obj.sets.rationals`, `obj.sets.reals`, `obj.sets.complexes` |
| FR-001 | `prop.is_finite` | `sage-presentations` | 2 | `obj.sets.f9_x`, `obj.sets.f9_y` |
| FR-002 | `meth.cardinality` | `sage` | 1 | `obj.finite_sets.fin` |
| FR-002 | `prop.is_finite` | `sage` | 1 | `obj.finite_sets.fin` |
| FR-004 | `bind.sets.integral` | `sage-symbolic` | 1 | `cat.sets` |
| FR-004 | `bind.sets.limit` | `sage-symbolic` | 1 | `cat.sets` |
| FR-004 | `bind.sets.limit_at_infinity` | `sage-symbolic` | 1 | `cat.sets` |
| FR-004 | `meth.cardinality` | `gap` | 1 | `obj.rings.integers_mod` |
| FR-004 | `meth.cardinality` | `gap-groups` | 4 | `obj.groups.symmetric`, `obj.groups.cyclic`, `obj.groups.units`, `obj.sets.units` |
| FR-004 | `mor.sets.complex_abs` | `sage-symbolic` | 1 | `obj.sets.complexes` |
| FR-004 | `mor.sets.complex_bar` | `sage-symbolic` | 1 | `obj.sets.complexes` |
| FR-004 | `mor.sets.complex_im` | `sage-symbolic` | 1 | `obj.sets.complexes` |
| FR-004 | `mor.sets.complex_re` | `sage-symbolic` | 1 | `obj.sets.complexes` |
| FR-004 | `mor.sets.nat_prime_factors` | `sage-symbolic` | 1 | `obj.sets.positive_naturals` |
| FR-004 | `mor.sets.real_sqrt` | `sage-symbolic` | 1 | `obj.sets.reals` |
| FR-004 | `prop.is_abelian` | `gap-groups` | 3 | `obj.groups.symmetric`, `obj.groups.cyclic`, `obj.groups.units` |
| FR-004 | `prop.is_commutative` | `gap-groups` | 3 | `obj.groups.symmetric`, `obj.groups.cyclic`, `obj.groups.units` |
| FR-004 | `prop.is_finite` | `gap` | 1 | `obj.rings.integers_mod` |
| FR-004 | `prop.is_finite` | `gap-groups` | 4 | `obj.groups.symmetric`, `obj.groups.cyclic`, `obj.groups.units`, `obj.sets.units` |
| FR-006 | `cmp.f9.translation` | `sage-presentations` | 2 | `obj.commutative_rings.f9_x`, `obj.commutative_rings.f9_y` |
| FR-006 | `meth.cardinality` | `sage-presentations` | 2 | `obj.commutative_rings.f9_x`, `obj.commutative_rings.f9_y` |
| FR-006 | `mor.sets.companion_matrix` | `sage-symbolic` | 1 | `obj.sets.monics` |
| FR-006 | `mor.sets.f9_x_constants` | `sage-presentations` | 2 | `mor.sets.f9_x_constants`, `obj.sets.integers_mod` |
| FR-006 | `mor.sets.f9_y_constants` | `sage-presentations` | 2 | `mor.sets.f9_y_constants`, `obj.sets.integers_mod` |
| FR-006 | `mor.sets.mv_total_degree` | `sage-symbolic` | 1 | `obj.sets.mv_polynomials` |
| FR-006 | `mor.sets.polynomial_degree` | `sage-symbolic` | 1 | `obj.sets.polynomials` |
| FR-006 | `mor.sets.polynomial_derivative` | `sage-symbolic` | 1 | `obj.sets.polynomials` |
| FR-006 | `mor.sets.polynomial_differential` | `sage-symbolic` | 1 | `obj.sets.polynomials` |
| FR-006 | `mor.sets.polynomial_factors` | `sage-symbolic` | 1 | `obj.sets.nonzero_polynomials` |
| FR-006 | `mor.sets.polynomial_map` | `sage-symbolic` | 1 | `obj.sets.polynomials` |
| FR-006 | `mor.sets.polynomial_roots` | `sage-symbolic` | 1 | `obj.sets.nonzero_polynomials` |
| FR-006 | `prop.is_finite` | `sage-presentations` | 2 | `obj.commutative_rings.f9_x`, `obj.commutative_rings.f9_y` |
| FR-008 | `meth.cardinality` | `sage-modules` | 2 | `obj.modules.regular`, `obj.modules.vectors` |
| FR-009 | `colim.bil_w_form.cokernel` | `sage-discriminant` | 1 | `cat.bil_wform` |
| FR-009 | `meth.cardinality` | `sage-discriminant` | 1 | `obj.bil_wform.root_lattice_a_discriminant` |
| FR-009 | `meth.cardinality` | `sage-modules` | 2 | `obj.bil_wform.root_lattice_a`, `obj.bil_wform.root_lattice_a_dual` |
| FR-009 | `prop.is_abelian` | `gap-groups` | 3 | `obj.bil_wform.root_lattice_a`, `obj.bil_wform.root_lattice_a_dual`, `obj.bil_wform.root_lattice_a_discriminant` |
| FR-009 | `prop.is_commutative` | `gap-groups` | 3 | `obj.bil_wform.root_lattice_a`, `obj.bil_wform.root_lattice_a_dual`, `obj.bil_wform.root_lattice_a_discriminant` |
| FR-010 | `mor.sets.span` | `sage-symbolic` | 1 | `obj.sets.power_set` |
| FR-011 | `meth.rank` | `sage-modules` | 5 | `obj.modules.regular`, `obj.modules.vectors`, `obj.bil_wform.root_lattice_a`, `obj.bil_wform.root_lattice_a_dual`, `obj.bil_wform.root_lattice_a_discriminant` |
| FR-013 | `lift.bilin_module.restrict#backward` | `sage-bilinear-lift` | 1 | `lift.bilin_module.restrict#input` |
| FR-013 | `lift.bilin_module.restrict#forward` | `sage-bilinear-lift` | 1 | `lift.bilin_module.restrict#input` |
| FR-013 | `lift.bilin_module.restrict#hom` | `sage-bilinear-lift` | 1 | `lift.bilin_module.restrict#input` |
| FR-013 | `lift.bilin_module.restrict#obj` | `sage-bilinear-lift` | 1 | `lift.bilin_module.restrict#input` |
| FR-015 | `fun.arrows_groups.kernel` | `gap-groups` | 1 | `cat.arrows_groups` |
| FR-015 | `meth.cardinality` | `gap-groups` | 3 | `obj.subgroups.alternating`, `obj.subgroups.kernel`, `cat.subobjects_groups` |
| FR-015 | `meth.group_arrow_kernel` | `gap-groups` | 1 | `cat.arrows_groups` |
| FR-015 | `prop.is_abelian` | `gap-groups` | 2 | `obj.subgroups.kernel`, `cat.subobjects_groups` |
| FR-015 | `prop.is_commutative` | `gap-groups` | 3 | `obj.subgroups.alternating`, `obj.subgroups.kernel`, `cat.subobjects_groups` |
| FR-015 | `prop.is_finite` | `gap-groups` | 3 | `obj.subgroups.alternating`, `obj.subgroups.kernel`, `cat.subobjects_groups` |
| FR-017 | `meth.cardinality` | `sage-modules` | 1 | `obj.integral_lattice.e8` |
| FR-017 | `meth.rank` | `sage-modules` | 1 | `obj.integral_lattice.e8` |
| FR-017 | `prop.is_abelian` | `gap-groups` | 1 | `obj.integral_lattice.e8` |
| FR-017 | `prop.is_commutative` | `gap-groups` | 1 | `obj.integral_lattice.e8` |

| FR | Registrations |
| --- | --- |
| FR-001 | 31 |
| FR-002 | 2 |
| FR-004 | 25 |
| FR-006 | 18 |
| FR-008 | 2 |
| FR-009 | 10 |
| FR-010 | 1 |
| FR-011 | 5 |
| FR-013 | 4 |
| FR-015 | 13 |
| FR-017 | 4 |
| Total | 115 |
