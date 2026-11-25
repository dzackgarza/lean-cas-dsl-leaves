# Tasks: Subset Predicates category implementation (`cat.subsets.subset_predicates`)

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md); the shared feature [001](../001-category-implementations/tasks.md).

## Execution order

The versions of this feature run at their places in the feature order of [001 tasks](../001-category-implementations/tasks.md#feature-order). Within a version the unchecked tasks run in document order. A wait on an unavailable input blocks only its task (constitution, Governance). **After** names the inputs of a task: a task of this file, a task of another feature as `NNN "Spec Vn complete"`, a task of 001 as `001 Tnnn`, a contract task as "contract Tnnn", a lean-categories task by its ID and issue. **Kernel** names the kernel task that the version serves; it is a reference, not an input of the leaf author (LV14).

Every implementation task follows 001 plan "Tests of each program" and the [backend contract](../001-category-implementations/contracts/backend-program.md). No test asserts a mathematical value (LV18).

Format: `- [ ] ID [Story] description`.

## Phase 1: User Story 1 — V1

**Kernel**: kernel T251 ("Implement Subset predicates Spec V1").

- [ ] T001 [US1] Survey record of V1 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.subsets.subset_predicates` with `cas_interfaces.load_interfaces(...).category("cat.subsets.subset_predicates")`. Write one row for each requirement FR-001 and for the routine of each registration of this version: the engine and routine of the plan's routine table, verified in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/033-subsets-subset-predicates/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V1 and each moved registration of V1, each routine marked as verified in the container; each part of the generated interface that V1 needs is covered. **After**: 001 T006, 003 "Spec V1 complete", 023 "Spec V1 complete".
- [ ] T002 [US1] Implement Equality of subsets (G1: FR-001) in `backends/subsets_subset_predicates.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/subsets_subset_predicates.py`, `leaves.json`, `tests/test_subsets_subset_predicates.py`, `tests/scenarios/subsets_subset_predicates-g1-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category subsets_subset_predicates` passes the six checks of 001 plan "Tests of each program" for the ports of FR-001; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001, lean-categories T007 (#200), lean-categories T013 (#191), contract T021.
- [ ] T003 [US1] Spec V1 complete. Check that every task of V1 above is checked, that each requirement of V1 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category subsets_subset_predicates`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category subsets_subset_predicates` passes in under five minutes and its log and timing records are committed; kernel T251 ("Implement Subset predicates Spec V1") consumes this version. **After**: T002.

## Dependencies

| Task | After |
| --- | --- |
| T001 | 001 T006, 003 "Spec V1 complete", 023 "Spec V1 complete" |
| T002 | T001, lean-categories T007 (#200), lean-categories T013 (#191), contract T021 |
| T003 | T002 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| kernel T251 ("Implement Subset predicates Spec V1") | T001–T003 |
