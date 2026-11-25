# Implementation Plan: Category implementations — the shared foundation and the spec list

**Branch**: `001-category-implementations` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); [data-model.md](data-model.md);
[contracts/backend-program.md](contracts/backend-program.md); [quickstart.md](quickstart.md)

## Summary

Build what every category implementation shares: the declared SDK and Julia dependencies, the
engine bridge `backends/engine.py` under the one interpreter of the research container, the tier 1
harness that drives each real backend through the contract's protocol peer with durable logs and
timing records, and the protocol-2 manifest. Then the 33 category specs (002 to 034) implement
their categories, one module and program for each, as glue over the engines of the research
container, against the released contract `cas-computation/2` and its generated category
interface; they move the 115 existing registrations, replace their hand-rolled and lookup answers
by engine routines and delete the data held in the source. This feature closes with the move to
the release `v2.0.1`, the removal of the engine fallbacks, the specimens on protocol 2 and the
timing triage.

## Technical Context

**Language/Version**: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`)
for the backends; Julia 1.12.7 through `juliacall` 0.9.36 for Catlab.jl.
**Primary Dependencies**: contract SDK `lean-cas-dsl-leaf-contracts` at tag `v2.0.0`, then
`v2.0.1` (contract FR-022); SageMath 11.0.beta5 with GAP 4.16.1 (`libgap`), PARI 2.17.4
(`cypari2`), Singular 4.4.1, Maxima 5.49.0; SymPy 1.14.0; Catlab.jl 0.17.7. Macaulay2 and
Oscar.jl with Hecke enter with the first V3 row that needs them (table "Categories with no
spec").
**Storage**: committed files only: `leaves.json`, `tests/logs/`, `tests/timing/records.jsonl`.
**Testing**: `just test` (tier 1, `uv run --frozen pytest tests`) after `just setup`; one
category with `just test-category NAME`; `just test-commit` (manifest and compilation) at commit.
**Target Platform**: the research container `ghcr.io/dzackgarza/sage:develop` (LV21).
**Project Type**: provider package: a manifest and backend programs.
**Performance Goals**: tier 1 of one category under five minutes (SC-004).
**Constraints**: permitted inputs only (LV14); a computation that no engine provides is the known
method with its cited reference (LV6); no field computed that no request demands (LV25).
**Scale/Scope**: 33 category specs (257 V1 rows, of which 14 wait for a catalogue declaration;
25 V2 rows), 115 moved registrations, one backend program for each category implementation.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1, FR-034 | Each program has one lowering table; lookups and duplicated data are deleted. |
| LV2, LV14 | No document or test here holds an acceptance statement or expected answer; kernel tasks are named by ID. |
| LV3 | Each category spec implements, version by version, the rows of its category's generated interface that its versions need; V3 adds rows by the membership rule. |
| LV4 | Tier 1 checks retention of supplied endpoints and earlier outputs in each reply. |
| LV5–LV7 | Each version of each category spec starts with its survey record; the routine table of its plan names each port's routine; known mathematics with no engine is listed in its section "Hand-rolled code" with its reference. |
| LV8 | Programs that need another category's operation suspend through the SDK and handle `NoImplementation`. |
| LV10, LV11 | `leaves.json` holds no priority; replies use the contract statuses. |
| LV12 | Each moved registration has a decision in the plan of its category spec (FR-027, FR-039). |
| LV13 | The feature order of [tasks.md](tasks.md#feature-order) follows the structural order, after F; each version names its kernel task. |
| LV16, LV21 | One interpreter; `pyproject.toml`, `uv.lock`, `Project.toml`, `Manifest.toml`; `lakefile.toml` deleted; each category module imports only the engines and the category modules that its plan declares. |
| LV17–LV23 | `tests/conftest.py` writes logs and timing records; scenarios drive real processes. |

Gate result: pass. No violation needs a justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-category-implementations/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/backend-program.md
├── checklists/requirements.md
└── tasks.md
specs/002-cardinals/ … specs/034-ideals-r/   one feature for each category spec (table below)
├── spec.md, plan.md, research.md, tasks.md
└── checklists/requirements.md
```

### Source Code (repository root)

```text
leaves.json                    manifest: v2 backends only (contract FR-004)
pyproject.toml, uv.lock        contract SDK at its release tag; pytest (dev)
Project.toml, Manifest.toml    Julia project: Catlab.jl 0.17.7
justfile                       setup, test-commit, test, test-category, test-push
backends/engine.py             shared start-up, logging, timing, routine observations, serve()
backends/<slug>.py             one category implementation and its program (table "Category specs")
tests/conftest.py              run log and timing records (LV22, LV23)
tests/harness.py               starts a backend under /sage/.venv/bin/python3 and runs cas-peer
tests/test_<slug>.py           tier 1 of one category implementation
tests/scenarios/<slug>-*.json
tests/logs/, tests/timing/records.jsonl
specimens/{missing,wrong,malformed,unavailable}/   deliberately bad v2 packages
```

**Structure Decision**: one module and backend program for each category implementation
(research R3): the category is the unit of responsibility (LV3), a test of one category starts
no other program (LV16), and a category module imports another category module only where its
plan declares the code dependency (LV8). The v1 programs (`sage_backend.py`, `gap_backend.py`,
`sage_power_set.py`, `sage_set_limits.py`, `sage_fin_rev.py`, `gap_groups.py`,
`sage_presentations.py`, `sage_symbolic.py`, `sage_modules.py`, `sage_discriminant.py`,
`sage_bilinear_lift.py`) leave the manifest at T006 and are trashed by the move task of the
category spec version that moves their last registration (research R4); `engine_python.py` and
`wire.py` are trashed by T044.

## Category specs

One feature for each category with a row in V1 or V2, in the structural order (research R16).
A row count includes the rows that the catalogue lacks; each of those waits for the lean-categories
task that declares it: lean-categories T065 to T078 (#212 to #225, the kernel upstream tasks T328 to
T341), whose plan gives each row its catalogue ID. The registrations are those of research R15. A
spec with no V2 row has no V2: the full-B0 statements whose rows have their latest home in its
category need only V1 rows, and its V1 kernel task accepts them.

| Directory | Category | V1 rows | of which the catalogue lacks | V2 rows | Registrations V1 | Registrations V2 | Kernel tasks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [`002-cardinals`](../002-cardinals/spec.md) | `cat.cardinals` | 2 | 1 | 0 | 0 | 0 | T201 (V1) |
| [`003-sets`](../003-sets/spec.md) | `cat.sets` | 74 | 2 | 0 | 31 | 0 | T202 (V1) |
| [`004-core-sets`](../004-core-sets/spec.md) | `cat.core_sets` | 6 | 0 | 0 | 13 | 0 | T203 (V1) |
| [`005-finite-sets`](../005-finite-sets/spec.md) | `cat.finite_sets` | 3 | 0 | 2 | 0 | 2 | T204 (V1), T255 (V2) |
| [`006-linear-orders`](../006-linear-orders/spec.md) | `cat.linear_orders` | 9 | 0 | 0 | 0 | 0 | T207 (V1) |
| [`007-additive-monoids`](../007-additive-monoids/spec.md) | `cat.additive_monoids` | 4 | 0 | 0 | 0 | 0 | T210 (V1) |
| [`008-magmas`](../008-magmas/spec.md) | `cat.magmas` | 3 | 0 | 0 | 0 | 0 | T211 (V1) |
| [`009-additive-commutative-monoids`](../009-additive-commutative-monoids/spec.md) | `cat.additive_commutative_monoids` | 1 | 0 | 0 | 0 | 0 | T212 (V1) |
| [`010-semigroups`](../010-semigroups/spec.md) | `cat.semigroups` | 2 | 0 | 0 | 0 | 0 | T213 (V1) |
| [`011-monoids`](../011-monoids/spec.md) | `cat.monoids` | 7 | 0 | 0 | 2 | 0 | T214 (V1) |
| [`012-groups`](../012-groups/spec.md) | `cat.groups` | 10 | 0 | 8 | 6 | 6 | T215 (V1), T256 (V2) |
| [`013-semirings`](../013-semirings/spec.md) | `cat.semirings` | 7 | 0 | 0 | 0 | 0 | T216 (V1) |
| [`014-additive-groups`](../014-additive-groups/spec.md) | `cat.additive_groups` | 2 | 0 | 0 | 0 | 0 | T217 (V1) |
| [`015-rings`](../015-rings/spec.md) | `cat.rings` | 16 | 0 | 0 | 2 | 0 | T218 (V1) |
| [`016-commutative-rings`](../016-commutative-rings/spec.md) | `cat.commutative_rings` | 50 | 6 | 2 | 13 | 1 | T221 (V1), T258 (V2) |
| [`017-hausdorff-topological-commutative-monoids`](../017-hausdorff-topological-commutative-monoids/spec.md) | `cat.hausdorff_topological_commutative_monoids` | 4 | 0 | 0 | 0 | 0 | T222 (V1) |
| [`018-modules-total`](../018-modules-total/spec.md) | `cat.modules_total` | 3 | 0 | 0 | 0 | 0 | T223 (V1) |
| [`019-modules-r`](../019-modules-r/spec.md) | `cat.modules_r` | 11 | 3 | 1 | 2 | 0 | T224 (V1), T259 (V2) |
| [`020-bil-wform`](../020-bil-wform/spec.md) | `cat.bil_wform` | 3 | 0 | 3 | 5 | 5 | T235 (V1), T260 (V2) |
| [`021-fields`](../021-fields/spec.md) | `cat.fields` | 5 | 0 | 0 | 1 | 0 | T236 (V1) |
| [`022-core-modules-r`](../022-core-modules-r/spec.md) | `cat.core_modules_r` | 1 | 0 | 2 | 0 | 5 | T237 (V1), T261 (V2) |
| [`023-subobjects-sets`](../023-subobjects-sets/spec.md) | `cat.subobjects_sets` | 1 | 0 | 0 | 0 | 0 | T238 (V1) |
| [`024-arrows-modules-r`](../024-arrows-modules-r/spec.md) | `cat.arrows_modules_r` | 3 | 0 | 0 | 0 | 0 | T241 (V1) |
| [`025-core-subobjects-modules-r`](../025-core-subobjects-modules-r/spec.md) | `cat.core_subobjects_modules_r` | 1 | 0 | 0 | 0 | 0 | T242 (V1) |
| [`026-bilin-module`](../026-bilin-module/spec.md) | `cat.bilin_module` | 15 | 0 | 1 | 0 | 0 | T243 (V1), T262 (V2) |
| [`027-arrows-bilin-module`](../027-arrows-bilin-module/spec.md) | `cat.arrows_bilin_module` | 2 | 0 | 0 | 4 | 0 | T244 (V1) |
| [`028-subobjects-groups`](../028-subobjects-groups/spec.md) | `cat.subobjects_groups` | 0 | 0 | 2 | 0 | 11 | T263 (V2) |
| [`029-arrows-groups`](../029-arrows-groups/spec.md) | `cat.arrows_groups` | 0 | 0 | 2 | 0 | 2 | T264 (V2) |
| [`030-boolean-algebras`](../030-boolean-algebras/spec.md) | `cat.boolean_algebras` | 7 | 0 | 0 | 0 | 0 | T249 (V1) |
| [`031-integral-lattice`](../031-integral-lattice/spec.md) | `cat.integral_lattice` | 0 | 0 | 2 | 0 | 4 | T265 (V2) |
| [`032-enumerated-sets`](../032-enumerated-sets/spec.md) | `cat.enumerated_sets` | 2 | 1 | 0 | 0 | 0 | T250 (V1) |
| [`033-subsets-subset-predicates`](../033-subsets-subset-predicates/spec.md) | `cat.subsets.subset_predicates` | 1 | 0 | 0 | 0 | 0 | T251 (V1) |
| [`034-ideals-r`](../034-ideals-r/spec.md) | `cat.ideals_r` | 2 | 1 | 0 | 0 | 0 | T252 (V1) |
| Total | 33 categories | 257 | 14 | 25 | 79 | 36 | |

## Categories with no spec

These categories have no row in V1 or V2: no computed statement of V1 or V2 needs a row whose
home is the category at catalogue `3f8aedf`, and the kernel task list has no category task for
them. Each enters V3 of its own spec by the membership rule when kernel tasks T140 to T147 produce
rows for it; the kernel then adds its V3 category task. The engine and the upstream inputs are
those that the former milestone of the kernel plan named; the survey of the future spec starts
from them.

| Former milestone | Categories | Engine of the former milestone | Notes |
| --- | --- | --- | --- |
| Sets | `cat.cardinalities` | Sage | — |
| Orders | `cat.preorders`, `cat.partial_orders` | Sage posets (`Poset`, `is_lequal`, `is_less_than`, `is_chain`); GAP Digraphs `IsPreorderDigraph` through `libgap` for preorders, because Sage has no preorder category in the survey's index | lean-categories T041 (#195) registers the order categories |
| Rings | `cat.additive_magmas`, `cat.additive_semigroups` | GAP and Sage | not structural steps at catalogue `3f8aedf`; lean-categories T005 (#193) registers the additive chain |
| Group automorphisms | `cat.core_groups` | GAP `AutomorphismGroup`, `ConjugatorAutomorphism`, `InverseGeneralMapping` | on the routes of V1 statements as the core named by rows whose home is `cat.groups` (spec 012) |
| Commutative rings | `cat.commutative_monoids` | Sage | — |
| Module kernels | `cat.subobjects_modules_r` | Sage module `hom`, `kernel()`, `submodule` | owner of rows whose homes are specs 024 and 025 |
| Boolean algebras | `cat.join_semilattices`, `cat.meet_semilattices`, `cat.order_lattices`, `cat.bounded_order_lattices` | Sage `posets.BooleanLattice`, `LatticePoset` `meet`, `join`, `complements` | not structural steps at catalogue `3f8aedf`; lean-categories T041 (#195) |
| Set constructions | `cat.arrows_sets`, `cat.slice_sets`, `cat.coslice_sets`, `cat.endofunctors_sets`, `cat.walking_pair`, `cat.sets.pair_diagrams`, `cat.pointed_sets`, `cat.core_pointed_sets`, `cat.countable_sets`, `cat.core_subobjects_sets`, `cat.subsets.point_predicates`, `cat.crystals` | Sage sets with a stored base point, `EnumeratedSets`, `crystals`; Catlab.jl slices, coslices and diagrams | crystals are not in the engine survey and are surveyed from their Sage source first; lean-categories T043, T044 (#201) give crystals their structural functor; `cat.core_subobjects_sets` owns `meth.set_eq`, whose home is spec 033 |
| Well orders | `cat.well_ordered_sets`, `cat.core_well_ordered_sets`, `cat.enumerated_monotone_sets`, `cat.ordinals` | SymPy `sympy.sets.ordinals` (`Ordinal`, `OmegaPower`); Sage posets for finite well orders | lean-categories T041 (#195) |
| Algebraic structures | `cat.magmaswithtwooperations`, `cat.division_rings` | Sage `QuaternionAlgebra`; GAP `MagmaByMultiplicationTable` | lean-categories T005 (#193) |
| Algebras | `cat.algebras` | Sage `Algebras(R)`, `FreeAlgebra`, `GroupAlgebra` | read only by typing judgements at catalogue `3f8aedf` |
| Schemes | `cat.schemes`, `cat.schemes_over`, `cat.schemes_over_ring` | Sage `sage.schemes` (`Spec`, `AffineSpace`, `ProjectiveSpace`) | not in the engine survey; surveyed from its Sage source first; lean-categories T023 (#198) and T045, T046 (#202); `cat.schemes_over_ring` is read only by typing judgements |
| Module constructions | `cat.module_points`, `cat.based_module`, `cat.based_module_indexed`, `cat.coord`, `cat.coord_indexed`, `cat.finite_projective_lattice`, `cat.finitelygeneratedmodules`, `cat.finiterankmodules`, `cat.free_cover`, `cat.free_cover_indexed`, `cat.freemodules`, `cat.quotients_modules_r`, `cat.torsion_free_modules` | Sage `fg_pid` modules and quotient modules; Macaulay2 1.24.11 through `sage.interfaces.macaulay2`, a separate process, for modules over polynomial rings (Oscar inside the Sage process is rejected: Oscar loads its own GAP, Singular and FLINT, untested beside Sage's copies) | lean-categories T047, T048 (#203); `cat.ideals_r` has spec 034 |
| Forms over rings | `cat.modules_over_rings_ext`, `cat.bilin_forms_over_rings`, `cat.quad_forms_over_rings`, `cat.integral_forms`, `cat.lattices_over_rings`, `cat.finite_projective_lattices_over_rings`, `cat.finite_free_lattices_over_rings`, `cat.unimodular_lattices_over_rings`, `cat.integral_lattices`, `cat.even_integral_lattices`, `cat.cusps` | Sage `QuadraticForm`; Hecke 0.39.22 through Oscar 1.8.2 in a program that loads Oscar through `juliacall` and imports no Sage module | the cusps of `sage.modular` are surveyed from their Sage source first; lean-categories T049 to T058 (#204 to #208) |
| Lattices and quadratic modules | `cat.quad_module`, `cat.quad_wform`, `cat.alternating_forms`, `cat.lattice`, `cat.subobjects_bilin_module`, `cat.coord_lattice`, `cat.fraction_field_perfect_finite_projective_lattice`, `cat.definite_lattice`, `cat.indefinite_lattice`, `cat.even_lattice`, `cat.finite_free_lattice`, `cat.unimodular_lattice` | Sage `IntegralLattice`, `TorsionQuadraticModule`; Hecke through Oscar for genus and isometry, in a program with no Sage import; PARI `qfauto` for definite lattices | the gap of generators of $O(L)$ for an indefinite $L$ of rank at least 3 keeps the survey's searches; lean-categories T059 to T062 (#209, #210) |

| Quantity | Count |
| --- | ---: |
| Categories with a spec | 33 |
| Categories with no spec | 70 |

## Tests of each program

Each `tests/test_<slug>.py` starts the program under `/sage/.venv/bin/python3` with the SDK
of `.deps/` on `PYTHONPATH` and runs `cas-peer run SCENARIO -- COMMAND` for each scenario. The
scenarios are built from the generated interface of the program's category. Each test checks:

1. negotiation with the four protocol-2 features and `routine-observations/1`;
2. for each port: a reply at the generated result layout, with the routine observation of the
   routine table;
3. for each port whose request carries selected data: those data in the reply where the layout
   retains them;
4. one unsupported presentation: `status:"unsupported"` with the exact `op`;
5. for a program that suspends: the continuation after a `noImplementation` slot;
6. one log file and one timing record per test.

No test asserts a mathematical value (LV18).

## Sequencing

1. Before F: FR-033 (contract findings) and FR-036 (findings to an issue). They need no release.
2. At contract `v2.0.0` (kernel F): setup, harness, shared engine module, manifest in v2 form
   (FR-026, FR-029–FR-032, FR-034 at the shared level).
3. The V1 versions of the category specs 002 to 034 in the structural order, each starting with
   its survey record (FR-028); the public-only check (SC-007) after Sets V1.
4. At kernel T105: the dependency moves to `v2.0.1`.
5. The V2 versions of the specs that have one, in the structural order; then the removal of the
   engine fallbacks (FR-031) and the specimens (FR-035).
6. Timing triage (LV24) after all functionality.

The [feature order](tasks.md#feature-order) of the task list is the binding sequence.

## Complexity Tracking

No constitution violation needs a justification.
