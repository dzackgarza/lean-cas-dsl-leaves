# Tasks: Category implementations for the computational milestones

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/backend-program.md](contracts/backend-program.md),
[quickstart.md](quickstart.md).

## Execution order

The unchecked tasks are executed in the order of this file; the first unchecked task is active
(constitution, Governance). A wait on an unavailable input blocks only its task; work continues
with the next task whose inputs are present, and the waiting task keeps its position (K:C16,
K:C21). Each task names its **Files**, its **Acceptance**, its inputs (**After**: a task of this
file, a contract task as "contract T0nn", a kernel task as "kernel T0nn") and the kernel task that
it serves (**Kernel**). A kernel task ID is a reference, not an input of the leaf author (LV14).

Every implementation task follows the plan's "Tests of each program" and the contract
[backend-program.md](contracts/backend-program.md); every survey task fills its section of
[research.md](research.md), "Survey record", with the row format given there (FR-028). A survey task lists
the parts of the generated interface with `cas_interfaces.load_interfaces(...).category(<id>)`
for each category of its requirement. An implementation task implements every part of that list
that no subsequent requirement moves (LV3), moves the registrations of its rows of the research
table "Registrations that move", replaces the hand-rolled, partial and lookup answers that FR-027
names for those rows by the routines of its survey record, deletes the duplicated data that
FR-034 names for them, and trashes each v1 program whose last registration it moves.

Format: `- [ ] ID [P?] [Story] description`.

## Phase 1: Findings that need no release

- [ ] T001 [P] Report the undeclared wire forms and missing inputs of FR-033 to
  lean-cas-dsl-leaf-contracts as one issue: for each form, the registration that needs it, the
  leaf-chosen encoding of `DEFECTS.md` and the contract rule that leaves it undeclared (RC8;
  `api/declared-ports.json`). Write the issue URL into research R12. **Files**:
  `specs/001-category-implementations/research.md`. **Acceptance**: the issue exists on the
  contract repository with the `enhancement` label and names all ten items of FR-033; R12 links
  it. **After**: none. **Kernel**: T203, T205, T209.
- [ ] T002 Record the findings of `DEFECTS.md` in an issue of this repository (FR-036): one
  section per finding, each with its commit references, and the open items as a checklist.
  Compare the issue with the file paragraph by paragraph, then trash `DEFECTS.md` and remove its
  name from `AGENTS.md`, `README.md`, `CONTRIBUTING.md` and the constitution's Governance
  (patch amendment). **Files**: `DEFECTS.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`,
  `.specify/memory/constitution.md`. **Acceptance**: the issue holds every finding;
  `git ls-files DEFECTS.md` and `git grep -n DEFECTS.md -- ':!specs'` return nothing.
  **After**: T001. **Kernel**: T200.

## Phase 2: Foundation at kernel readiness F

- [ ] T003 Declare the dependencies (FR-032; research R1, R2, R9). Write `pyproject.toml` (the
  contract package at `git+https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts@v2.0.0`;
  `pytest` as a dev dependency) and `uv.lock` with `uv lock`; write `Project.toml` and
  `Manifest.toml` with Catlab.jl 0.17.7 and Oscar.jl 1.8.2; add the `setup` and `check-engine`
  recipes to `justfile`; add `.deps/` to `.gitignore`; trash `lakefile.toml` and its paragraph of
  `README.md`. **Files**: `pyproject.toml`, `uv.lock`, `Project.toml`, `Manifest.toml`,
  `justfile`, `.gitignore`, `lakefile.toml`, `README.md`. **Acceptance**: in the research
  container `just setup` exits 0, and `just check-engine` imports `cas_session`,
  `cas_interfaces`, `sage.all` and `juliacall` with Catlab under the backend command.
  **After**: kernel F; contract T019. **Kernel**: T200.
- [ ] T004 Write `backends/engine.py` (FR-026, FR-029, FR-031; contract backend-program): engine
  import once before the ready frame and exit before it when an engine is absent; the ready
  features with `routine-observations/1`; the handler table of a program; the per-request log
  line and timing of [data-model.md](data-model.md); the routine-observation helper; the
  suspension helper that returns `NoImplementation` to the handler; the `juliacall` variables of
  R2. **Files**: `backends/engine.py`. **Acceptance**: T005's engine tests pass. **After**: T003.
  **Kernel**: T200.
- [ ] T005 Write the tier 1 harness (FR-029, FR-030; LV17, LV18; research R10, R11):
  `tests/conftest.py` (run log, timing records), `tests/harness.py` (starts a program under
  `/sage/.venv/bin/python3` with `.deps` on `PYTHONPATH`, runs `cas-peer run`), the recipes
  `test`, `test-category` and `test-push` in `justfile`, and `tests/test_engine.py` with the
  programs `tests/programs/empty.py` (no ports) and `tests/programs/absent_engine.py` (requires an
  uninstalled module). **Files**: `tests/conftest.py`, `tests/harness.py`,
  `tests/test_engine.py`, `tests/programs/empty.py`, `tests/programs/absent_engine.py`,
  `tests/scenarios/engine-*.json`, `tests/logs/`, `tests/timing/records.jsonl`, `justfile`.
  **Acceptance**: `just test-category engine` shows a negotiation with the five features and an
  exit before the ready frame for the absent engine; the run writes one log and one timing record
  per test; it finishes in under five minutes (SC-004). **After**: T004; contract T003.
  **Kernel**: T200.
- [ ] T006 Rewrite `leaves.json` in the protocol-2 form with no v1 backend (research R4;
  FR-026), and make `test-commit` decode it with `cas-peer manifest`. **Files**: `leaves.json`,
  `justfile`. **Acceptance**: `cas-peer manifest leaves.json` accepts it; `git grep -n
  '"python3"' leaves.json` returns nothing. **After**: T005; contract T005. **Kernel**: T200.

## Phase 3: User Story 1 and User Story 2 — the V1 milestones

- [ ] T007 [US1] Survey FR-001 (sets, core sets, cardinals, cardinalities). **Files**:
  `specs/001-category-implementations/research.md`. **Acceptance**: a row for each part of the
  four category interfaces; the pullback row names Catlab.jl `pullback`; the cardinal row names
  the `EnumeratedSets` rule and the gap of infinite cardinals other than $\aleph_0$ with the
  survey's searches. **After**: T006; kernel T119, T120, T121, T123, T129, T134. **Kernel**: T200.
- [ ] T008 [US1] Implement FR-001 in `backends/sets.py` with the 31 registrations of FR-001 (the
  infinite-factor product of R12 excepted), and the computations that move in from the kernel:
  equality of elements, application and composition of maps, the projections of a product, the
  graph of a map. Replace the Python pullback by Catlab.jl (FR-027). Trash `sage_power_set.py`
  and `sage_fin_rev.py`. **Files**: `backends/sets.py`, `leaves.json`, `tests/test_sets.py`,
  `tests/scenarios/sets-*.json`, `backends/sage_power_set.py`, `backends/sage_fin_rev.py`.
  **Acceptance**: `just test-category sets` passes the six checks of the plan; the pullback
  reply's routine observation names Catlab.jl. **After**: T007. **Kernel**: T200.
- [ ] T009 [US1] Run the public-only check of the quickstart (SC-007) on `backends/sets.py`.
  **Files**: `specs/001-category-implementations/quickstart.md` where a command differs;
  `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: every command passes in a container
  with no lean-cas-dsl checkout mounted; the log and records are committed. **After**: T008.
  **Kernel**: T200.
- [ ] T010 [US2] Survey FR-002 (finite sets). **Files**: `research.md`. **Acceptance**: a row
  for each part of the `cat.finite_sets` interface. **After**: T008; kernel T119, T135.
  **Kernel**: T201.
- [ ] T011 [US2] Implement FR-002 in `backends/finite_sets.py` with its 2 registrations and the
  list of the elements of a finite carrier; trash `sage_backend.py`. **Files**:
  `backends/finite_sets.py`, `leaves.json`, `tests/test_finite_sets.py`,
  `tests/scenarios/finite_sets-*.json`, `backends/sage_backend.py`. **Acceptance**:
  `just test-category finite_sets` passes. **After**: T010. **Kernel**: T201.
- [ ] T012 [US2] Survey FR-003 (preorders, partial and linear orders). **Files**:
  `research.md`. **Acceptance**: a row for each part of the three interfaces; preorders name GAP
  Digraphs (R6). **After**: T008; kernel T133. **Kernel**: T202.
- [ ] T013 [US2] Implement FR-003 in `backends/orders.py`, with $<$ and $\le$ on $\mathbb{N}$.
  **Files**: `backends/orders.py`, `leaves.json`, `tests/test_orders.py`,
  `tests/scenarios/orders-*.json`. **Acceptance**: `just test-category orders` passes.
  **After**: T012. **Kernel**: T202.
- [ ] T014 [US2] Survey FR-004 (the eleven categories of the ring chain and the binders).
  **Files**: `research.md`. **Acceptance**: a row for each part of the eleven interfaces and for
  each binder, with SymPy and the Sage symbolic ring named for integrals and limits. **After**:
  T008; kernel T122, T131, T132. **Kernel**: T203.
- [ ] T015 [US2] Implement FR-004 in `backends/rings.py` and `backends/calculus.py` with the 25
  registrations of FR-004 (the eight of R12 excepted), and the arithmetic of $\mathbb{N}$,
  $\mathbb{Z}$, $\mathbb{Z}/n$, gcd, primality, and the multiplication, unit and inverse of an
  instance; trash `gap_backend.py`. **Files**: `backends/rings.py`, `backends/calculus.py`,
  `leaves.json`, `tests/test_rings.py`, `tests/test_calculus.py`, `tests/scenarios/rings-*.json`,
  `tests/scenarios/calculus-*.json`, `backends/gap_backend.py`. **Acceptance**:
  `just test-category rings` and `just test-category calculus` pass. **After**: T014.
  **Kernel**: T203.
- [ ] T016 [US2] Survey FR-005 (core groups). **Files**: `research.md`. **Acceptance**: a row for
  each part of the `cat.core_groups` interface. **After**: T015; kernel T134. **Kernel**: T204.
- [ ] T017 [US2] Implement FR-005 in `backends/core_groups.py`. **Files**:
  `backends/core_groups.py`, `leaves.json`, `tests/test_core_groups.py`,
  `tests/scenarios/core_groups-*.json`. **Acceptance**: `just test-category core_groups` passes.
  **After**: T016. **Kernel**: T204.
- [ ] T018 [US2] Survey FR-006 (commutative monoids and rings). **Files**: `research.md`.
  **Acceptance**: a row for each part of the two interfaces and of the generic
  `cmp.polynomial_quotient.translation`. **After**: T015. **Kernel**: T205.
- [ ] T019 [US2] Implement FR-006 in `backends/commutative_rings.py` with the 18 registrations of
  FR-006 (the four of R12 excepted); trash `sage_presentations.py`. **Files**:
  `backends/commutative_rings.py`, `leaves.json`, `tests/test_commutative_rings.py`,
  `tests/scenarios/commutative_rings-*.json`, `backends/sage_presentations.py`. **Acceptance**:
  `just test-category commutative_rings` passes; the F9 translation reply retains both typed
  endpoints of the request. **After**: T018. **Kernel**: T205.
- [ ] T020 [US2] Survey FR-007 (Hausdorff topological commutative monoids). **Files**:
  `research.md`. **Acceptance**: a row for each part of the interface. **After**: T019;
  kernel T128. **Kernel**: T206.
- [ ] T021 [US2] Implement FR-007 in `backends/topological_monoids.py`. **Files**:
  `backends/topological_monoids.py`, `leaves.json`, `tests/test_topological_monoids.py`,
  `tests/scenarios/topological_monoids-*.json`. **Acceptance**:
  `just test-category topological_monoids` passes; a coefficient is computed only when a request
  demands it (LV25). **After**: T020. **Kernel**: T206.
- [ ] T022 [US2] Survey FR-008 (modules). **Files**: `research.md`. **Acceptance**: a row for
  each part of the two interfaces. **After**: T019. **Kernel**: T207.
- [ ] T023 [US2] Implement FR-008 in `backends/modules.py` with its 2 registrations and the scalar
  action of an instance. **Files**: `backends/modules.py`, `leaves.json`,
  `tests/test_modules.py`, `tests/scenarios/modules-*.json`. **Acceptance**:
  `just test-category modules` passes. **After**: T022. **Kernel**: T207.
- [ ] T024 [US2] Survey FR-009 (bilinear forms). **Files**: `research.md`. **Acceptance**: a row
  for each part of the `cat.bil_wform` interface; the discriminant rows name Sage
  `discriminant_group` and PARI `matsnf`. **After**: T023. **Kernel**: T208.
- [ ] T025 [US2] Implement FR-009 in `backends/bilinear_forms.py` with its 10 registrations;
  replace the lookup cokernel and the literal Gram matrices (FR-027, FR-034); trash
  `sage_discriminant.py`. **Files**: `backends/bilinear_forms.py`, `leaves.json`,
  `tests/test_bilinear_forms.py`, `tests/scenarios/bilinear_forms-*.json`,
  `backends/sage_discriminant.py`. **Acceptance**: `just test-category bilinear_forms` passes;
  the cocone reply carries the engine's quotient, not two catalogue names. **After**: T024.
  **Kernel**: T208.
- [ ] T026 [US2] Survey FR-010 (fields). **Files**: `research.md`. **Acceptance**: a row for
  each part of the `cat.fields` interface. **After**: T019. **Kernel**: T209.
- [ ] T027 [US2] Implement FR-010 in `backends/fields.py` (`mor.sets.span` waits on R12, T034).
  **Files**: `backends/fields.py`, `leaves.json`, `tests/test_fields.py`,
  `tests/scenarios/fields-*.json`. **Acceptance**: `just test-category fields` passes.
  **After**: T026. **Kernel**: T209.
- [ ] T028 [US2] Survey FR-011 (core modules). **Files**: `research.md`. **Acceptance**: a row
  for each part of the `cat.core_modules_r` interface. **After**: T023. **Kernel**: T210.
- [ ] T029 [US2] Implement FR-011 in `backends/module_rank.py` with its 5 registrations; replace
  the three literal ranks by Sage `rank()` (FR-027). **Files**: `backends/module_rank.py`,
  `leaves.json`, `tests/test_module_rank.py`, `tests/scenarios/module_rank-*.json`.
  **Acceptance**: `just test-category module_rank` passes. **After**: T028. **Kernel**: T210.
- [ ] T030 [US2] Survey FR-012 (subobjects and arrows of modules, subobjects of sets).
  **Files**: `research.md`. **Acceptance**: a row for each part of the four interfaces.
  **After**: T023; kernel T134, T138. **Kernel**: T211.
- [ ] T031 [US2] Implement FR-012 in `backends/module_kernels.py`, with membership in a subset.
  **Files**: `backends/module_kernels.py`, `leaves.json`, `tests/test_module_kernels.py`,
  `tests/scenarios/module_kernels-*.json`. **Acceptance**: `just test-category module_kernels`
  passes; the kernel reply carries the inclusion map at the request's ambient module.
  **After**: T030. **Kernel**: T211.
- [ ] T032 [US2] Survey FR-013 (formed modules and their arrows). **Files**: `research.md`.
  **Acceptance**: a row for each part of the two interfaces and each field of
  `lift.bilin_module.restrict`. **After**: T025; kernel T130, T134. **Kernel**: T212.
- [ ] T033 [US2] Implement FR-013 in `backends/formed_modules.py` with its 4 registrations;
  replace the Python restriction by Sage `submodule` and `gram_matrix` (FR-027); trash
  `sage_bilinear_lift.py`. **Files**: `backends/formed_modules.py`, `leaves.json`,
  `tests/test_formed_modules.py`, `tests/scenarios/formed_modules-*.json`,
  `backends/sage_bilinear_lift.py`. **Acceptance**: `just test-category formed_modules` passes;
  each field reply carries the outputs of the preceding fields that the request supplied.
  **After**: T032. **Kernel**: T212.
- [ ] T034 [US2] Register the parts of R12 with the forms that the contract task answering T001 declares: the
  infinite-factor product (sets), the four complex maps, `mor.sets.real_sqrt` and the three
  binders (rings, calculus), `mor.sets.polynomial_degree`, `mor.sets.polynomial_differential`,
  `mor.sets.companion_matrix`, `mor.sets.polynomial_roots` (commutative rings) and
  `mor.sets.span` (fields), with the forms of that contract release; trash `sage_symbolic.py` and
  `sage_set_limits.py`. **Files**: `backends/sets.py`, `backends/rings.py`,
  `backends/calculus.py`, `backends/commutative_rings.py`, `backends/fields.py`, `leaves.json`,
  their tests and scenarios, `backends/sage_symbolic.py`, `backends/sage_set_limits.py`.
  **Acceptance**: the tier 1 tests of the five programs pass; `git ls-files backends/sage_symbolic.py
  backends/sage_set_limits.py` returns nothing. **After**: T008, T015, T019, T027; the contract
  task that answers T001's issue. **Kernel**: T200, T203, T205, T209.
- [ ] T035 Move the SDK dependency to `v2.0.1` (FR-026; contract FR-022): `pyproject.toml`,
  `uv.lock`, the tag check of `just setup`; run `just test`. **Files**: `pyproject.toml`,
  `uv.lock`, `justfile`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: tier 1 of
  every program passes on `v2.0.1`; the log and records are committed. **After**: T033, T034;
  contract T020. **Kernel**: T105.

## Phase 4: User Story 2 — the full-B0 and coverage milestones

- [ ] T036 [US2] Survey FR-014 (series, limits and integrals across the V1 categories).
  **Files**: `research.md`. **Acceptance**: a row for each part of the V1 interfaces that T008 to
  T033 recorded as a gap or left to FR-014. **After**: T035; kernel T124, T125, T128, T136, T137.
  **Kernel**: T213.
- [ ] T037 [US2] Implement FR-014 in the programs of FR-001 to FR-013 and in
  `backends/calculus.py`; the product $\aleph_0 \cdot \aleph_0$ follows the answer to kernel owner
  question Q1. **Files**: those programs, `leaves.json`, their tests and scenarios.
  **Acceptance**: the tier 1 tests of the changed programs pass. **After**: T036; kernel owner
  question Q1 for the cardinal part. **Kernel**: T213.
- [ ] T038 [US2] Survey FR-015 (arrows and subobjects of groups). **Files**: `research.md`.
  **Acceptance**: a row for each part of the two interfaces. **After**: T035; kernel T134.
  **Kernel**: T214.
- [ ] T039 [US2] Implement FR-015 in `backends/group_kernels.py` with its 13 registrations; the
  kernel reply builds the subgroup from the supplied inclusion images (CONTRIBUTING DAT001).
  **Files**: `backends/group_kernels.py`, `leaves.json`, `tests/test_group_kernels.py`,
  `tests/scenarios/group_kernels-*.json`. **Acceptance**: `just test-category group_kernels`
  passes. **After**: T038. **Kernel**: T214.
- [ ] T040 [US2] Survey FR-016 (semilattices, lattices of orders, Boolean algebras). **Files**:
  `research.md`. **Acceptance**: a row for each part of the five interfaces. **After**: T035;
  kernel T133, T136. **Kernel**: T215.
- [ ] T041 [US2] Implement FR-016 in `backends/boolean_algebras.py`. **Files**:
  `backends/boolean_algebras.py`, `leaves.json`, `tests/test_boolean_algebras.py`,
  `tests/scenarios/boolean_algebras-*.json`. **Acceptance**:
  `just test-category boolean_algebras` passes. **After**: T040. **Kernel**: T215.
- [ ] T042 [US2] Survey FR-017 (integral lattices). **Files**: `research.md`. **Acceptance**: a
  row for each part of the `cat.integral_lattice` interface. **After**: T035. **Kernel**: T216.
- [ ] T043 [US2] Implement FR-017 in `backends/integral_lattices.py` with its 4 registrations;
  the $E_8$ rank and cardinality come from Sage `IntegralLattice` (FR-027); trash
  `gap_groups.py` and `sage_modules.py`. **Files**: `backends/integral_lattices.py`,
  `leaves.json`, `tests/test_integral_lattices.py`, `tests/scenarios/integral_lattices-*.json`,
  `backends/gap_groups.py`, `backends/sage_modules.py`. **Acceptance**:
  `just test-category integral_lattices` passes. **After**: T042, T039. **Kernel**: T216.
- [ ] T044 Trash `backends/engine_python.py` and `backends/wire.py`, and remove the
  `CAS_SAGE_PYTHON`, `CAS_GAP_PYTHON` and modular-entrypoint paragraphs of `README.md` and
  `AGENTS.md` (FR-031). **Files**: `backends/engine_python.py`, `backends/wire.py`, `README.md`,
  `AGENTS.md`. **Acceptance**: SC-002, SC-003 and SC-005 hold. **After**: T034, T043.
  **Kernel**: T105.
- [ ] T045 [US2] Survey FR-018 (set constructions), with crystals surveyed from their Sage
  source. **Files**: `research.md`. **Acceptance**: a row for each part of the fourteen
  interfaces. **After**: T035; kernel T134. **Kernel**: T217.
- [ ] T046 [US2] Implement FR-018 in `backends/set_constructions.py`. **Files**:
  `backends/set_constructions.py`, `leaves.json`, `tests/test_set_constructions.py`,
  `tests/scenarios/set_constructions-*.json`. **Acceptance**:
  `just test-category set_constructions` passes. **After**: T045. **Kernel**: T217.
- [ ] T047 [US2] Survey FR-019 (well orders, ordinals). **Files**: `research.md`.
  **Acceptance**: a row for each part of the four interfaces. **After**: T046; kernel T133.
  **Kernel**: T218.
- [ ] T048 [US2] Implement FR-019 in `backends/well_orders.py`. **Files**:
  `backends/well_orders.py`, `leaves.json`, `tests/test_well_orders.py`,
  `tests/scenarios/well_orders-*.json`. **Acceptance**: `just test-category well_orders`
  passes. **After**: T047. **Kernel**: T218.
- [ ] T049 [US2] Survey FR-020 (magmas with two operations, division rings). **Files**:
  `research.md`. **Acceptance**: a row for each part of the two interfaces. **After**: T035;
  kernel T131. **Kernel**: T219.
- [ ] T050 [US2] Implement FR-020 in `backends/algebraic_structures.py`. **Files**:
  `backends/algebraic_structures.py`, `leaves.json`, `tests/test_algebraic_structures.py`,
  `tests/scenarios/algebraic_structures-*.json`. **Acceptance**:
  `just test-category algebraic_structures` passes. **After**: T049. **Kernel**: T219.
- [ ] T051 [US2] Survey FR-021 (algebras). **Files**: `research.md`. **Acceptance**: a row for
  each part of the `cat.algebras` interface. **After**: T035. **Kernel**: T220.
- [ ] T052 [US2] Implement FR-021 in `backends/algebras.py`. **Files**: `backends/algebras.py`,
  `leaves.json`, `tests/test_algebras.py`, `tests/scenarios/algebras-*.json`. **Acceptance**:
  `just test-category algebras` passes. **After**: T051. **Kernel**: T220.
- [ ] T053 [US2] Survey FR-022 (schemes), with `sage.schemes` surveyed from its Sage source.
  **Files**: `research.md`. **Acceptance**: a row for each part of the three interfaces.
  **After**: T035; kernel T136. **Kernel**: T221.
- [ ] T054 [US2] Implement FR-022 in `backends/schemes.py`. **Files**: `backends/schemes.py`,
  `leaves.json`, `tests/test_schemes.py`, `tests/scenarios/schemes-*.json`. **Acceptance**:
  `just test-category schemes` passes. **After**: T053. **Kernel**: T221.
- [ ] T055 [US2] Survey FR-023 (module constructions). **Files**: `research.md`.
  **Acceptance**: a row for each part of the fourteen interfaces; modules over polynomial rings
  name Macaulay2 (R6). **After**: T035, T031; kernel T118. **Kernel**: T222.
- [ ] T056 [US2] Implement FR-023 in `backends/module_constructions.py`. **Files**:
  `backends/module_constructions.py`, `leaves.json`, `tests/test_module_constructions.py`,
  `tests/scenarios/module_constructions-*.json`. **Acceptance**:
  `just test-category module_constructions` passes. **After**: T055. **Kernel**: T222.
- [ ] T057 [US2] Survey FR-024 (forms over rings), with the cusps of `sage.modular` surveyed from
  their Sage source. **Files**: `research.md`. **Acceptance**: a row for each part of the eleven
  interfaces. **After**: T035. **Kernel**: T223.
- [ ] T058 [US2] Implement FR-024 in `backends/forms_over_rings.py` and
  `backends/forms_over_rings_hecke.py`. **Files**: those programs, `leaves.json`,
  `tests/test_forms_over_rings.py`, `tests/scenarios/forms_over_rings-*.json`. **Acceptance**:
  `just test-category forms_over_rings` passes; the Hecke program imports no `sage` module.
  **After**: T057. **Kernel**: T223.
- [ ] T059 [US2] Survey FR-025 (lattices and quadratic modules). **Files**: `research.md`.
  **Acceptance**: a row for each part of the twelve interfaces; the gap of generators of $O(L)$
  for indefinite $L$ of rank at least 3 keeps the survey's searches. **After**: T043, T056.
  **Kernel**: T224.
- [ ] T060 [US2] Implement FR-025 in `backends/lattices.py` and `backends/lattices_hecke.py`.
  **Files**: those programs, `leaves.json`, `tests/test_lattices.py`,
  `tests/scenarios/lattices-*.json`. **Acceptance**: `just test-category lattices` passes; the
  Hecke program imports no `sage` module. **After**: T059. **Kernel**: T224.

## Phase 5: User Story 3 and final performance

- [ ] T061 [US3] Move the four specimen packages to protocol 2 (FR-035), keeping their bad
  behaviour, and test them through `cas-peer`. **Files**: `specimens/*/backend.py`,
  `specimens/*/leaves.json`, `specimens/README.md`, `tests/test_specimens.py`,
  `tests/scenarios/specimens-*.json`. **Acceptance**: `just test-category specimens` shows no
  implementation for `missing`, a well-framed reply for `wrong`, `malformed` for `malformed` and
  `unavailable` for `unavailable`. **After**: T060. **Kernel**: T108.
- [ ] T062 Write the timing triage table of LV24 from `tests/timing/records.jsonl` into
  [research.md](research.md), and do the optimization that it selects. **Files**: `research.md`
  and the programs that the table selects. **Acceptance**: the table has every LV24 column and
  each optimization row has its remaining measured cost. **After**: T061. **Kernel**: T103.

## Dependencies

| Task | After |
| --- | --- |
| T001 | — |
| T002 | T001 |
| T003 | kernel F; contract T019 |
| T004–T006 | each the previous task; T005 also contract T003, T006 also contract T005 |
| T007, T008 | T006 and the upstream kernel tasks of FR-001; T008 after T007 |
| T009 | T008 |
| survey T010–T032 (even IDs) | the implementation tasks of its requirement's predecessors, and its upstream kernel tasks |
| implementation T011–T033 (odd IDs) | its survey task |
| T034 | T008, T015, T019, T027; the contract task that answers T001 |
| T035 | T033, T034; contract T020 |
| T036–T060 | T035 and the predecessors named in each task |
| T061 | T060 |
| T062 | T061 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| T200 | T002–T009, T034 |
| T201 | T010, T011 |
| T202 | T012, T013 |
| T203 | T001, T014, T015, T034 |
| T204 | T016, T017 |
| T205 | T001, T018, T019, T034 |
| T206 | T020, T021 |
| T207 | T022, T023 |
| T208 | T024, T025 |
| T209 | T001, T026, T027, T034 |
| T210 | T028, T029 |
| T211 | T030, T031 |
| T212 | T032, T033 |
| T105 | T035, T044 |
| T213 | T036, T037 |
| T214 | T038, T039 |
| T215 | T040, T041 |
| T216 | T042, T043 |
| T217 | T045, T046 |
| T218 | T047, T048 |
| T219 | T049, T050 |
| T220 | T051, T052 |
| T221 | T053, T054 |
| T222 | T055, T056 |
| T223 | T057, T058 |
| T224 | T059, T060 |
| T108 | T061 |
| T103 | T062 |
