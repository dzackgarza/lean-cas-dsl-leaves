# Tasks: Subobjects of Groups category implementation (`cat.subobjects_groups`)

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md); the shared feature [001](../001-category-implementations/tasks.md).

## Execution order

The versions of this feature run at their places in the feature order of [001 tasks](../001-category-implementations/tasks.md#feature-order). Within a version the unchecked tasks run in document order. No task waits: the workstream does each input task first, in its repository and role, and then returns (constitution, Governance). **After** names the inputs of a task: a task of this file, a task of another feature as `NNN "Spec Vn complete"`, a task of 001 as `001 Tnnn`, a contract task as "contract Tnnn", a lean-categories task by its ID and issue. **Kernel** names the kernel task that the version serves; it is a reference, not an input of the leaf author (LV14).

Every implementation task follows 001 plan "Tests of each program" and the [backend contract](../001-category-implementations/contracts/backend-program.md). No test asserts a mathematical value (LV18).

Format: `- [ ] ID [Story] description`.

## Phase 1: User Story 1 — V2

**Kernel**: kernel T263 ("Implement Subgroups Spec V2").

- [ ] T001 [US1] Survey record of V2 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.subobjects_groups` with `cas_interfaces.load_interfaces(...).category("cat.subobjects_groups")`. Write one row for each requirement FR-001 and FR-002 and for the routine of each registration of FR-003: the engine and routine of the plan's routine table, verified in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/028-subobjects-groups/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V2 and each moved registration of V2, each routine marked as verified in the container; each part of the generated interface that V2 needs is covered. **After**: 001 T035, 012 "Spec V2 complete".
- [ ] T002 [US1] Implement Subgroups (G1: FR-001, FR-002) in `backends/subobjects_groups.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/subobjects_groups.py`, `leaves.json`, `tests/test_subobjects_groups.py`, `tests/scenarios/subobjects_groups-g1-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category subobjects_groups` passes the six checks of 001 plan "Tests of each program" for the ports of FR-001, FR-002; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001.
- [ ] T003 [US1] Move the 11 existing registrations of V2 (FR-003; plan "Registrations that move") into `backends/subobjects_groups.py` on protocol 2, with the decision of each row. **Files**: `backends/subobjects_groups.py`, `leaves.json`, `tests/test_subobjects_groups.py`, `tests/scenarios/subobjects_groups-moved-*.json`. **Acceptance**: each moved registration has a scenario in `tests/scenarios/subobjects_groups-moved-*.json` that `just test-category subobjects_groups` passes, and its reply names the routine of its decision. **After**: T002.
- [ ] T004 [US1] Spec V2 complete. Check that every task of V2 above is checked, that each requirement of V2 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category subobjects_groups`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category subobjects_groups` passes in under five minutes and its log and timing records are committed; kernel T263 ("Implement Subgroups Spec V2") consumes this version. **After**: T002, T003.

## Dependencies

| Task | After |
| --- | --- |
| T001 | 001 T035, 012 "Spec V2 complete" |
| T002 | T001 |
| T003 | T002 |
| T004 | T002, T003 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| kernel T263 ("Implement Subgroups Spec V2") | T001–T004 |
