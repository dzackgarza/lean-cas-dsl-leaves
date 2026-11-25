# Tasks: Rings category implementation (`cat.rings`)

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md); the shared feature [001](../001-category-implementations/tasks.md).

## Execution order

The versions of this feature run at their places in the feature order of [001 tasks](../001-category-implementations/tasks.md#feature-order). Within a version the unchecked tasks run in document order. A wait on an unavailable input blocks only its task (constitution, Governance). **After** names the inputs of a task: a task of this file, a task of another feature as `NNN "Spec Vn complete"`, a task of 001 as `001 Tnnn`, a contract task as "contract Tnnn", a lean-categories task by its ID and issue. **Kernel** names the kernel task that the version serves; it is a reference, not an input of the leaf author (LV14).

Every implementation task follows 001 plan "Tests of each program" and the [backend contract](../001-category-implementations/contracts/backend-program.md). No test asserts a mathematical value (LV18).

Format: `- [ ] ID [Story] description`.

## Phase 1: User Story 1 — V1

**Kernel**: kernel T218 ("Implement Rings Spec V1").

- [ ] T001 [US1] Survey record of V1 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.rings` with `cas_interfaces.load_interfaces(...).category("cat.rings")`. Write one row for each requirement FR-001 to FR-016 and for the routine of each registration of FR-017: the engine and routine of the plan's routine table, verified in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/015-rings/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V1 and each moved registration of V1, each routine marked as verified in the container; each part of the generated interface that V1 needs is covered. **After**: 001 T006, 003 "Spec V1 complete", 009 "Spec V1 complete", 011 "Spec V1 complete", 013 "Spec V1 complete", 014 "Spec V1 complete".
- [ ] T002 [US1] Implement Named rings and arithmetic (G1: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011) in `backends/rings.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/rings.py`, `leaves.json`, `tests/test_rings.py`, `tests/scenarios/rings-g1-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category rings` passes the six checks of 001 plan "Tests of each program" for the ports of FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001, lean-categories T017 (#194), lean-categories T005 (#193), lean-categories T064 (#211), contract T021.
- [ ] T003 [US1] Implement Forgets and the carrier comparison (G2: FR-012, FR-013, FR-014, FR-015, FR-016) in `backends/rings.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/rings.py`, `leaves.json`, `tests/test_rings.py`, `tests/scenarios/rings-g2-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category rings` passes the six checks of 001 plan "Tests of each program" for the ports of FR-012, FR-013, FR-014, FR-015, FR-016; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001.
- [ ] T004 [US1] Move the 2 existing registrations of V1 (FR-017; plan "Registrations that move") into `backends/rings.py` on protocol 2, with the decision of each row. Trash `backends/gap_backend.py`: this task moves its last registration. **Files**: `backends/rings.py`, `leaves.json`, `tests/test_rings.py`, `tests/scenarios/rings-moved-*.json`, `backends/gap_backend.py`. **Acceptance**: each moved registration has a scenario in `tests/scenarios/rings-moved-*.json` that `just test-category rings` passes, and its reply names the routine of its decision; `git ls-files backends/gap_backend.py` returns nothing. **After**: T002, T003.
- [ ] T005 [US1] Spec V1 complete. Check that every task of V1 above is checked, that each requirement of V1 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category rings`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category rings` passes in under five minutes and its log and timing records are committed; kernel T218 ("Implement Rings Spec V1") consumes this version. **After**: T002, T003, T004.

## Dependencies

| Task | After |
| --- | --- |
| T001 | 001 T006, 003 "Spec V1 complete", 009 "Spec V1 complete", 011 "Spec V1 complete", 013 "Spec V1 complete", 014 "Spec V1 complete" |
| T002 | T001, lean-categories T017 (#194), lean-categories T005 (#193), lean-categories T064 (#211), contract T021 |
| T003 | T001 |
| T004 | T002, T003 |
| T005 | T002, T003, T004 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| kernel T218 ("Implement Rings Spec V1") | T001–T005 |
| kernel T257 ("Implement Rings Spec V2"; no row of this spec is in V2) | T001–T005 |
