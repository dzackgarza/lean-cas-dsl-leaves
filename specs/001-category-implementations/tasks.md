# Tasks: Category implementations — the shared foundation and the spec list

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/backend-program.md](contracts/backend-program.md),
[quickstart.md](quickstart.md).

## Execution order

The unchecked tasks of this file run at their steps of the [feature order](#feature-order); within
a step, in the order of this file (constitution, Governance). A wait on an unavailable input blocks only its task; work continues
with the next task whose inputs are present, and the waiting task keeps its position (K:C16,
K:C21). Each task names its **Files**, its **Acceptance**, its inputs (**After**: a task of this
file, a contract task as "contract T0nn", a kernel task as "kernel T0nn") and the kernel task that
it serves (**Kernel**). A kernel task ID is a reference, not an input of the leaf author (LV14).

The tasks of the category implementations are in the category specs 002 to 034. Their survey
tasks fill the survey record of their spec with the row format of [research.md](research.md),
"Survey record" (FR-028); their implementation tasks follow the plan's "Tests of each program" and
the contract [backend-program.md](contracts/backend-program.md); their move tasks move the
registrations of research R15 and trash each v1 program whose last registration they move
(research R4).

Format: `- [ ] ID [P?] [Story] description`.

## Phase 1: Findings that need no release

- [x] T001 [P] Record the undeclared wire forms and missing inputs of FR-033: they are the ten
  items of lean-cas-dsl-leaf-contracts issue
  [#14](https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/issues/14), each with the
  registration that needs it, the leaf-chosen encoding of `DEFECTS.md` and the contract rule that
  leaves it undeclared; contract task T021 declares them. Research R12 links the issue.
  **Files**: `specs/001-category-implementations/research.md`. **Acceptance**: the issue exists on
  the contract repository with the `enhancement` label and names all ten items of FR-033; R12
  links it. **After**: none. **Kernel**: the kernel tasks of Sets V1, Monoids V1, Commutative Rings V1 and Fields V1, whose rows need the forms of contract T021.
- [ ] T002 Record the findings of `DEFECTS.md` in an issue of this repository (FR-036): one
  section per finding, each with its commit references, and the open items as a checklist.
  Compare the issue with the file paragraph by paragraph, then trash `DEFECTS.md` and remove its
  name from `AGENTS.md`, `README.md`, `CONTRIBUTING.md` and the constitution's Governance
  (patch amendment). **Files**: `DEFECTS.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`,
  `.specify/memory/constitution.md`. **Acceptance**: the issue holds every finding;
  `git ls-files DEFECTS.md` and `git grep -n DEFECTS.md -- ':!specs'` return nothing.
  **After**: T001. **Kernel**: kernel task "Implement Cardinals Spec V1" (`cat.cardinals`), the first version of the feature order.

## Phase 2: Foundation at kernel readiness F

- [ ] T003 Declare the dependencies (FR-032; research R1, R2, R9). Write `pyproject.toml` (the
  contract package at `git+https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts@v2.0.0`;
  `pytest` as a dev dependency) and `uv.lock` with `uv lock`; write `Project.toml` and
  `Manifest.toml` with Catlab.jl 0.17.7 (research R2); add the `setup` and `check-engine`
  recipes to `justfile`; add `.deps/` to `.gitignore`; trash `lakefile.toml` and its paragraph of
  `README.md`. **Files**: `pyproject.toml`, `uv.lock`, `Project.toml`, `Manifest.toml`,
  `justfile`, `.gitignore`, `lakefile.toml`, `README.md`. **Acceptance**: in the research
  container `just setup` exits 0, and `just check-engine` imports `cas_session`,
  `cas_interfaces`, `sage.all` and `juliacall` with Catlab under the backend command.
  **After**: kernel F; contract T019. **Kernel**: kernel task "Implement Cardinals Spec V1" (`cat.cardinals`), the first version of the feature order.
- [ ] T004 Write `backends/engine.py` (FR-026, FR-029, FR-031; contract backend-program): engine
  import once before the ready frame and exit before it when an engine is absent; the ready
  features with `routine-observations/1`; the handler table of a program; the per-request log
  line and timing of [data-model.md](data-model.md); the routine-observation helper; the
  suspension helper that returns `NoImplementation` to the handler; the `juliacall` variables of
  R2. **Files**: `backends/engine.py`. **Acceptance**: T005's engine tests pass. **After**: T003.
  **Kernel**: kernel task "Implement Cardinals Spec V1" (`cat.cardinals`), the first version of the feature order.
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
  **Kernel**: kernel task "Implement Cardinals Spec V1" (`cat.cardinals`), the first version of the feature order.
- [ ] T006 Rewrite `leaves.json` in the protocol-2 form with no v1 backend (research R4;
  FR-026), and make `test-commit` decode it with `cas-peer manifest`. **Files**: `leaves.json`,
  `justfile`. **Acceptance**: `cas-peer manifest leaves.json` accepts it; `git grep -n
  '"python3"' leaves.json` returns nothing. **After**: T005; contract T005. **Kernel**: kernel task "Implement Cardinals Spec V1" (`cat.cardinals`), the first version of the feature order.

## Feature order

The features run in this order; within a feature, its tasks run in document order (constitution,
Governance). The first step with an unchecked task is active. A wait on an unavailable input
blocks only its task, and the work continues with the next task whose inputs are present
(research R17).

| Step | Task or feature | Content | Kernel task |
| ---: | --- | --- | --- |
| 1 | 001 T001–T006 | findings, dependencies, engine bridge, harness, protocol-2 manifest | see each task |
| 2 | [002-cardinals](../002-cardinals/tasks.md) V1 | `cat.cardinals` V1 | "Implement Cardinals Spec V1" (`cat.cardinals`) |
| 3 | [003-sets](../003-sets/tasks.md) V1 | `cat.sets` V1 | "Implement Sets Spec V1" (`cat.sets`) |
| 4 | 001 T009 | public-only check on the Sets implementation (SC-007) | the Sets V1 kernel task |
| 5 | [004-core-sets](../004-core-sets/tasks.md) V1 | `cat.core_sets` V1 | "Implement Core Sets Spec V1" (`cat.core_sets`) |
| 6 | [005-finite-sets](../005-finite-sets/tasks.md) V1 | `cat.finite_sets` V1 | "Implement Finite Sets Spec V1" (`cat.finite_sets`) |
| 7 | [006-linear-orders](../006-linear-orders/tasks.md) V1 | `cat.linear_orders` V1 | "Implement Linear Orders Spec V1" (`cat.linear_orders`) |
| 8 | [007-additive-monoids](../007-additive-monoids/tasks.md) V1 | `cat.additive_monoids` V1 | "Implement Additive Monoids Spec V1" (`cat.additive_monoids`) |
| 9 | [008-magmas](../008-magmas/tasks.md) V1 | `cat.magmas` V1 | "Implement Magmas Spec V1" (`cat.magmas`) |
| 10 | [009-additive-commutative-monoids](../009-additive-commutative-monoids/tasks.md) V1 | `cat.additive_commutative_monoids` V1 | "Implement Additive Commutative Monoids Spec V1" (`cat.additive_commutative_monoids`) |
| 11 | [010-semigroups](../010-semigroups/tasks.md) V1 | `cat.semigroups` V1 | "Implement Semigroups Spec V1" (`cat.semigroups`) |
| 12 | [011-monoids](../011-monoids/tasks.md) V1 | `cat.monoids` V1 | "Implement Monoids Spec V1" (`cat.monoids`) |
| 13 | [012-groups](../012-groups/tasks.md) V1 | `cat.groups` V1 | "Implement Groups Spec V1" (`cat.groups`) |
| 14 | [013-semirings](../013-semirings/tasks.md) V1 | `cat.semirings` V1 | "Implement Semirings Spec V1" (`cat.semirings`) |
| 15 | [014-additive-groups](../014-additive-groups/tasks.md) V1 | `cat.additive_groups` V1 | "Implement Additive Groups Spec V1" (`cat.additive_groups`) |
| 16 | [015-rings](../015-rings/tasks.md) V1 | `cat.rings` V1 | "Implement Rings Spec V1" (`cat.rings`) |
| 17 | [016-commutative-rings](../016-commutative-rings/tasks.md) V1 | `cat.commutative_rings` V1 | "Implement Commutative Rings Spec V1" (`cat.commutative_rings`) |
| 18 | [017-hausdorff-topological-commutative-monoids](../017-hausdorff-topological-commutative-monoids/tasks.md) V1 | `cat.hausdorff_topological_commutative_monoids` V1 | "Implement Hausdorff Topological Commutative Monoids Spec V1" (`cat.hausdorff_topological_commutative_monoids`) |
| 19 | [018-modules-total](../018-modules-total/tasks.md) V1 | `cat.modules_total` V1 | "Implement Total Modules Spec V1" (`cat.modules_total`) |
| 20 | [019-modules-r](../019-modules-r/tasks.md) V1 | `cat.modules_r` V1 | "Implement Modules Spec V1" (`cat.modules_r`) |
| 21 | [020-bil-wform](../020-bil-wform/tasks.md) V1 | `cat.bil_wform` V1 | "Implement Bilinear Forms Spec V1" (`cat.bil_wform`) |
| 22 | [021-fields](../021-fields/tasks.md) V1 | `cat.fields` V1 | "Implement Fields Spec V1" (`cat.fields`) |
| 23 | [022-core-modules-r](../022-core-modules-r/tasks.md) V1 | `cat.core_modules_r` V1 | "Implement Core Modules Spec V1" (`cat.core_modules_r`) |
| 24 | [023-subobjects-sets](../023-subobjects-sets/tasks.md) V1 | `cat.subobjects_sets` V1 | "Implement Subobjects of Sets Spec V1" (`cat.subobjects_sets`) |
| 25 | [024-arrows-modules-r](../024-arrows-modules-r/tasks.md) V1 | `cat.arrows_modules_r` V1 | "Implement Arrows of Modules Spec V1" (`cat.arrows_modules_r`) |
| 26 | [025-core-subobjects-modules-r](../025-core-subobjects-modules-r/tasks.md) V1 | `cat.core_subobjects_modules_r` V1 | "Implement Core Subobjects of Modules Spec V1" (`cat.core_subobjects_modules_r`) |
| 27 | [026-bilin-module](../026-bilin-module/tasks.md) V1 | `cat.bilin_module` V1 | "Implement Formed Modules Spec V1" (`cat.bilin_module`) |
| 28 | [027-arrows-bilin-module](../027-arrows-bilin-module/tasks.md) V1 | `cat.arrows_bilin_module` V1 | "Implement Arrows of Formed Modules Spec V1" (`cat.arrows_bilin_module`) |
| 29 | [030-boolean-algebras](../030-boolean-algebras/tasks.md) V1 | `cat.boolean_algebras` V1 | "Implement Boolean Algebras Spec V1" (`cat.boolean_algebras`) |
| 30 | [032-enumerated-sets](../032-enumerated-sets/tasks.md) V1 | `cat.enumerated_sets` V1 | "Implement Enumerated Sets Spec V1" (`cat.enumerated_sets`) |
| 31 | [033-subsets-subset-predicates](../033-subsets-subset-predicates/tasks.md) V1 | `cat.subsets.subset_predicates` V1 | "Implement Subset Predicates Spec V1" (`cat.subsets.subset_predicates`) |
| 32 | [034-ideals-r](../034-ideals-r/tasks.md) V1 | `cat.ideals_r` V1 | "Implement Ideals Spec V1" (`cat.ideals_r`) |
| 33 | 001 T035 | SDK dependency `v2.0.1` | kernel T105 |
| 34 | [005-finite-sets](../005-finite-sets/tasks.md) V2 | `cat.finite_sets` V2 | "Implement Finite Sets Spec V2" (`cat.finite_sets`) |
| 35 | [012-groups](../012-groups/tasks.md) V2 | `cat.groups` V2 | "Implement Groups Spec V2" (`cat.groups`) |
| 36 | [016-commutative-rings](../016-commutative-rings/tasks.md) V2 | `cat.commutative_rings` V2 | "Implement Commutative Rings Spec V2" (`cat.commutative_rings`) |
| 37 | [019-modules-r](../019-modules-r/tasks.md) V2 | `cat.modules_r` V2 | "Implement Modules Spec V2" (`cat.modules_r`) |
| 38 | [020-bil-wform](../020-bil-wform/tasks.md) V2 | `cat.bil_wform` V2 | "Implement Bilinear Forms Spec V2" (`cat.bil_wform`) |
| 39 | [022-core-modules-r](../022-core-modules-r/tasks.md) V2 | `cat.core_modules_r` V2 | "Implement Core Modules Spec V2" (`cat.core_modules_r`) |
| 40 | [026-bilin-module](../026-bilin-module/tasks.md) V2 | `cat.bilin_module` V2 | "Implement Formed Modules Spec V2" (`cat.bilin_module`) |
| 41 | [028-subobjects-groups](../028-subobjects-groups/tasks.md) V2 | `cat.subobjects_groups` V2 | "Implement Subobjects of Groups Spec V2" (`cat.subobjects_groups`) |
| 42 | [029-arrows-groups](../029-arrows-groups/tasks.md) V2 | `cat.arrows_groups` V2 | "Implement Arrows of Groups Spec V2" (`cat.arrows_groups`) |
| 43 | [031-integral-lattice](../031-integral-lattice/tasks.md) V2 | `cat.integral_lattice` V2 | "Implement Integral Lattices Spec V2" (`cat.integral_lattice`) |
| 44 | 001 T044 | engine fallbacks and the v1 wire codec removed | kernel T105 |
| 45 | 001 T061 | specimens on protocol 2 | kernel T108 |
| 46 | 001 T062 | timing triage and the optimization it selects | kernel T103 |

## Phase 3: Shared checks during the category specs

- [ ] T009 [US1] Run the public-only check of the quickstart (SC-007) on `backends/sets.py`.
  **Files**: `specs/001-category-implementations/quickstart.md` where a command differs;
  `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: every command passes in a container
  with no lean-cas-dsl checkout mounted; the log and records are committed. **After**: 003 "Spec V1 complete".
  **Kernel**: kernel task "Implement Sets Spec V1" (`cat.sets`).
- [ ] T035 Move the SDK dependency to `v2.0.1` (FR-026; contract FR-022): `pyproject.toml`,
  `uv.lock`, the tag check of `just setup`; run `just test`. **Files**: `pyproject.toml`,
  `uv.lock`, `justfile`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: tier 1 of
  every program passes on `v2.0.1`; the log and records are committed. **After**: 034 "Spec V1 complete"
  (the last V1 version of the feature order); contract T020. **Kernel**: T105.

## Phase 4: User Story 2 and closing

- [ ] T044 Trash `backends/engine_python.py` and `backends/wire.py`, and remove the
  `CAS_SAGE_PYTHON`, `CAS_GAP_PYTHON` and modular-entrypoint paragraphs of `README.md` and
  `AGENTS.md` (FR-031). **Files**: `backends/engine_python.py`, `backends/wire.py`, `README.md`,
  `AGENTS.md`. **Acceptance**: SC-002, SC-003 and SC-005 hold. **After**: 031 "Spec V2 complete"
  (its move task moves the last registrations of the v1 programs). **Kernel**: T105.
- [ ] T061 [US2] Move the four specimen packages to protocol 2 (FR-035), keeping their bad
  behaviour, and test them through `cas-peer`. **Files**: `specimens/*/backend.py`,
  `specimens/*/leaves.json`, `specimens/README.md`, `tests/test_specimens.py`,
  `tests/scenarios/specimens-*.json`. **Acceptance**: `just test-category specimens` shows no
  implementation for `missing`, a well-framed reply for `wrong`, `malformed` for `malformed` and
  `unavailable` for `unavailable`. **After**: T044. **Kernel**: T108.
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
| 002 V1 to 034 V1 | T006 and the predecessors named in each spec's tasks |
| T009 | 003 "Spec V1 complete" |
| T035 | 034 "Spec V1 complete"; contract T020 |
| V2 of 005, 012, 016, 019, 020, 022, 026, 028, 029, 031 | T035 and the predecessors named in each spec's tasks |
| T044 | 031 "Spec V2 complete" |
| T061 | T044 |
| T062 | T061 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| "Implement Cardinals Spec V1" (`cat.cardinals`) | T002–T006 |
| "Implement Sets Spec V1" (`cat.sets`) | T009 |
| the V1 kernel tasks of Sets, Monoids, Commutative Rings and Fields | T001 |
| T105 | T035, T044 |
| T108 | T061 |
| T103 | T062 |
| each "Implement <Category> Spec V<n>" | the tasks of that version in its spec |
