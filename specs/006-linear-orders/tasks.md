# Tasks: Linear Orders category implementation (`cat.linear_orders`)

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md); the shared feature [001](../001-category-implementations/tasks.md).

## Execution order

The versions of this feature run at their places in the feature order of [001 tasks](../001-category-implementations/tasks.md#feature-order). Within a version the unchecked tasks run in document order. Inputs follow the rule of [001 tasks](../001-category-implementations/tasks.md#execution-order). **After** names the inputs of a task: a task of this file, a task of another feature as `NNN "Spec Vn complete"`, a task of 001 as `001 Tnnn`, a contract task as "contract Tnnn", a lean-categories task by its ID and issue. **Kernel** names the kernel task that the version serves; it is a reference, not an input of the leaf author (LV14).

Every implementation task follows 001 plan "Tests of each program" and the [backend contract](../001-category-implementations/contracts/backend-program.md). No test asserts a mathematical value (LV18).

Format: `- [ ] ID [Story] description`.

## Phase 1: User Story 1 — V1

**Kernel**: kernel T207 ("Implement Linear orders Spec V1").

- [ ] T001 [US1] Survey record of V1 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.linear_orders` with `cas_interfaces.load_interfaces("/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json").category("cat.linear_orders")`. Write one row for each requirement FR-001 to FR-009 and for the routine of each registration of this version: the engine and routine of the plan's routine table, the command that runs the routine in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/006-linear-orders/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V1, for each moved registration of V1 and for each part of the `cat.linear_orders` entry of `categoryInterfaces` in `/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json` that V1 needs; the command in the column "Container command" of each row that names a routine exits 0 in the research container. **After**: 001 T006, 003 "Spec V1 complete".
- [ ] T002 [US1] Implement Orders and comparison (G1: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009) in `backends/linear_orders.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/linear_orders.py`, `leaves.json`, `tests/test_linear_orders.py`, `tests/scenarios/linear_orders-g1-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category linear_orders g1` passes the six checks of 001 plan "Tests of each program" for the ports of FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001, lean-categories T041 (#195).
- [ ] T003 [US1] Spec V1 complete. Check that every task of V1 above is checked, that each requirement of V1 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category linear_orders`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category linear_orders` passes in under five minutes and its log and timing records are committed. **After**: T002.

## Dependencies

| Task | After |
| --- | --- |
| T001 | 001 T006, 003 "Spec V1 complete" |
| T002 | T001, lean-categories T041 (#195) |
| T003 | T002 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| kernel T207 ("Implement Linear orders Spec V1") | T001–T003 |
