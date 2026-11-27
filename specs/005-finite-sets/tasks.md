# Tasks: Finite Sets category implementation (`cat.finite_sets`)

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md); the shared feature [001](../001-category-implementations/tasks.md).

## Execution order

The versions of this feature run at their places in the feature order of [001 tasks](../001-category-implementations/tasks.md#feature-order). Within a version the unchecked tasks run in document order. Inputs follow the rule of [001 tasks](../001-category-implementations/tasks.md#execution-order). **After** names the inputs of a task: a task of this file, a task of another feature as `NNN "Spec Vn complete"`, a task of 001 as `001 Tnnn`, a contract task as "contract Tnnn", a lean-categories task by its ID and issue. **Kernel** names the kernel task that the version serves; it is a reference, not an input of the leaf author (LV14).

Every implementation task follows 001 plan "Tests of each program" and the [backend contract](../001-category-implementations/contracts/backend-program.md). No test asserts a mathematical value (LV18).

Format: `- [ ] ID [Story] description`.

## Phase 1: User Story 1 — V1

**Kernel**: kernel T204 ("Implement Finite sets Spec V1").

- [ ] T001 [US1] Survey record of V1 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.finite_sets` with `cas_interfaces.load_interfaces("/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json").category("cat.finite_sets")`. Write one row for each requirement FR-001 to FR-003 and for the routine of each registration of this version: the engine and routine of the plan's routine table, the command that runs the routine in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/005-finite-sets/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V1, for each moved registration of V1 and for each part of the `cat.finite_sets` entry of `categoryInterfaces` in `/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json` that V1 needs; the command in the column "Container command" of each row that names a routine exits 0 in the research container. **After**: 001 T006, 003 "Spec V1 complete".
- [ ] T002 [US1] Implement Refinement and graphs (G1: FR-001, FR-002, FR-003) in `backends/finite_sets.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/finite_sets.py`, `leaves.json`, `tests/test_finite_sets.py`, `tests/scenarios/finite_sets-g1-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category finite_sets g1` passes the six checks of 001 plan "Tests of each program" for the ports of FR-001, FR-002, FR-003; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001, lean-categories T033 (#197).
- [ ] T003 [US1] Spec V1 complete. Check that every task of V1 above is checked, that each requirement of V1 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category finite_sets`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category finite_sets` passes in under five minutes and its log and timing records are committed. **After**: T002.

## Phase 2: User Story 2 — V2

**Kernel**: kernel T255 ("Implement Finite sets Spec V2").

- [ ] T004 [US2] Survey record of V2 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.finite_sets` with `cas_interfaces.load_interfaces("/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json").category("cat.finite_sets")`. Write one row for each requirement FR-004 and FR-005 and for the routine of each registration of FR-006: the engine and routine of the plan's routine table, the command that runs the routine in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/005-finite-sets/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V2, for each moved registration of V2 and for each part of the `cat.finite_sets` entry of `categoryInterfaces` in `/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json` that V2 needs; the command in the column "Container command" of each row that names a routine exits 0 in the research container. **After**: 001 T035, T003, 003 "Spec V1 complete".
- [ ] T005 [US2] Implement Category structure and Fin (G2: FR-004, FR-005) in `backends/finite_sets.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/finite_sets.py`, `leaves.json`, `tests/test_finite_sets.py`, `tests/scenarios/finite_sets-g2-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category finite_sets g2` passes the six checks of 001 plan "Tests of each program" for the ports of FR-004, FR-005; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T004.
- [ ] T006 [US2] Move the 2 existing registrations of V2 (FR-006; plan "Registrations that move") into `backends/finite_sets.py` on protocol 2, with the decision of each row. Trash `backends/sage_backend.py`: this task moves its last registration. **Files**: `backends/finite_sets.py`, `leaves.json`, `tests/test_finite_sets.py`, `tests/scenarios/finite_sets-moved-v2-*.json`, `backends/sage_backend.py`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: each moved registration has a scenario in `tests/scenarios/finite_sets-moved-v2-*.json` that `just test-category finite_sets moved-v2` passes, and its reply names the routine of its decision; `git ls-files backends/sage_backend.py` returns nothing. **After**: T005.
- [ ] T007 [US2] Spec V2 complete. Check that every task of V2 above is checked, that each requirement of V2 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category finite_sets`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category finite_sets` passes in under five minutes and its log and timing records are committed. **After**: T005, T006.

## Dependencies

| Task | After |
| --- | --- |
| T001 | 001 T006, 003 "Spec V1 complete" |
| T002 | T001, lean-categories T033 (#197) |
| T003 | T002 |
| T004 | 001 T035, T003, 003 "Spec V1 complete" |
| T005 | T004 |
| T006 | T005 |
| T007 | T005, T006 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| kernel T204 ("Implement Finite sets Spec V1") | T001–T003 |
| kernel T255 ("Implement Finite sets Spec V2") | T004–T007 |
