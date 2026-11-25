# Tasks: Modules category implementation (`cat.modules_r`)

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md); the shared feature [001](../001-category-implementations/tasks.md).

## Execution order

The versions of this feature run at their places in the feature order of [001 tasks](../001-category-implementations/tasks.md#feature-order). Within a version the unchecked tasks run in document order. A wait on an unavailable input blocks only its task (constitution, Governance). **After** names the inputs of a task: a task of this file, a task of another feature as `NNN "Spec Vn complete"`, a task of 001 as `001 Tnnn`, a contract task as "contract Tnnn", a lean-categories task by its ID and issue. **Kernel** names the kernel task that the version serves; it is a reference, not an input of the leaf author (LV14).

Every implementation task follows 001 plan "Tests of each program" and the [backend contract](../001-category-implementations/contracts/backend-program.md). No test asserts a mathematical value (LV18).

Format: `- [ ] ID [Story] description`.

## Phase 1: User Story 1 — V1

**Kernel**: kernel T224 ("Implement Modules Spec V1").

- [ ] T001 [US1] Survey record of V1 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.modules_r` with `cas_interfaces.load_interfaces(...).category("cat.modules_r")`. Write one row for each requirement FR-001 to FR-011 and for the routine of each registration of FR-012: the engine and routine of the plan's routine table, verified in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/019-modules-r/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V1 and each moved registration of V1, each routine marked as verified in the container; each part of the generated interface that V1 needs is covered. **After**: 001 T006, 015 "Spec V1 complete", 016 "Spec V1 complete", 018 "Spec V1 complete".
- [ ] T002 [US1] Implement Modules, scalars and linear maps (G1: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006) in `backends/modules_r.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-g1-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category modules_r` passes the six checks of 001 plan "Tests of each program" for the ports of FR-001, FR-002, FR-003, FR-004, FR-005, FR-006; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001, lean-categories T064 (#211), contract T021.
- [ ] T003 [US1] Implement Restriction of scalars (G2: FR-007, FR-008) in `backends/modules_r.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-g2-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category modules_r` passes the six checks of 001 plan "Tests of each program" for the ports of FR-007, FR-008; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T001.
- [ ] T004 [US1] Implement `missing.linear_map_from_formula` (FR-009) in `backends/modules_r.py` at the row that lean-categories declares, with the routine of the plan, and register its port. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-linear_map_from_formula-*.json`. **Acceptance**: `just test-category modules_r` passes the six checks for the port of `missing.linear_map_from_formula` under its catalogue ID `mor.modules.formula_linear_map`. **After**: T001, lean-categories T074 (#217), which declares `missing.linear_map_from_formula` as `mor.modules.formula_linear_map` (kernel T333).
- [ ] T005 [US1] Implement `missing.cyclic_module_object` (FR-010) in `backends/modules_r.py` at the row that lean-categories declares, with the routine of the plan, and register its port. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-cyclic_module_object-*.json`. **Acceptance**: `just test-category modules_r` passes the six checks for the port of `missing.cyclic_module_object` under its catalogue ID `obj.modules.integers_mod`. **After**: T001, lean-categories T075 (#222), which declares `missing.cyclic_module_object` as `obj.modules.integers_mod` (kernel T338).
- [ ] T006 [US1] Implement `missing.derivative_linear` (FR-011) in `backends/modules_r.py` at the row that lean-categories declares, with the routine of the plan, and register its port. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-derivative_linear-*.json`. **Acceptance**: `just test-category modules_r` passes the six checks for the port of `missing.derivative_linear` under its catalogue ID `mor.modules.polynomial_derivative`. **After**: T001, lean-categories T076 (#223), which declares `missing.derivative_linear` as `mor.modules.polynomial_derivative` (kernel T339).
- [ ] T007 [US1] Move the 2 existing registrations of V1 (FR-012; plan "Registrations that move") into `backends/modules_r.py` on protocol 2, with the decision of each row. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-moved-*.json`. **Acceptance**: each moved registration has a scenario in `tests/scenarios/modules_r-moved-*.json` that `just test-category modules_r` passes, and its reply names the routine of its decision. **After**: T002, T003, T004, T005, T006.
- [ ] T008 [US1] Spec V1 complete. Check that every task of V1 above is checked, that each requirement of V1 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category modules_r`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category modules_r` passes in under five minutes and its log and timing records are committed; kernel T224 ("Implement Modules Spec V1") consumes this version. **After**: T002, T003, T004, T005, T006, T007.

## Phase 2: User Story 2 — V2

**Kernel**: kernel T259 ("Implement Modules Spec V2").

- [ ] T009 [US2] Survey record of V2 (FR-028 of 001; LV7). List the parts of the generated interface of `cat.modules_r` with `cas_interfaces.load_interfaces(...).category("cat.modules_r")`. Write one row for each requirement FR-013 and for the routine of each registration of this version: the engine and routine of the plan's routine table, verified in the research container, its version, the decision and the reasons; one row for each gap with its searches. **Files**: `specs/019-modules-r/research.md`. **Acceptance**: `research.md` "Survey record" has a row for each requirement of V2 and each moved registration of V2, each routine marked as verified in the container; each part of the generated interface that V2 needs is covered. **After**: 001 T035, T008, 003 "Spec V1 complete", 015 "Spec V1 complete", 016 "Spec V2 complete", 018 "Spec V1 complete".
- [ ] T010 [US2] Implement Bilinear maps (G3: FR-013) in `backends/modules_r.py` with the routines of the plan's routine table, register each port in `leaves.json` with `preferredRoutes: []`, and add the scenarios of these ports. **Files**: `backends/modules_r.py`, `leaves.json`, `tests/test_modules_r.py`, `tests/scenarios/modules_r-g3-*.json`, `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category modules_r` passes the six checks of 001 plan "Tests of each program" for the ports of FR-013; each reply names the routine of the routine table; the run writes its log and one timing record per test and per handled request. **After**: T009.
- [ ] T011 [US2] Spec V2 complete. Check that every task of V2 above is checked, that each requirement of V2 has a registered port or an LV7 gap record of mathematically new work, and run `just test-category modules_r`. **Files**: `tests/logs/`, `tests/timing/records.jsonl`. **Acceptance**: `just test-category modules_r` passes in under five minutes and its log and timing records are committed; kernel T259 ("Implement Modules Spec V2") consumes this version. **After**: T010.

## Dependencies

| Task | After |
| --- | --- |
| T001 | 001 T006, 015 "Spec V1 complete", 016 "Spec V1 complete", 018 "Spec V1 complete" |
| T002 | T001, lean-categories T064 (#211), contract T021 |
| T003 | T001 |
| T004 | T001, lean-categories T074 (#217), which declares `missing.linear_map_from_formula` as `mor.modules.formula_linear_map` (kernel T333) |
| T005 | T001, lean-categories T075 (#222), which declares `missing.cyclic_module_object` as `obj.modules.integers_mod` (kernel T338) |
| T006 | T001, lean-categories T076 (#223), which declares `missing.derivative_linear` as `mor.modules.polynomial_derivative` (kernel T339) |
| T007 | T002, T003, T004, T005, T006 |
| T008 | T002, T003, T004, T005, T006, T007 |
| T009 | 001 T035, T008, 003 "Spec V1 complete", 015 "Spec V1 complete", 016 "Spec V2 complete", 018 "Spec V1 complete" |
| T010 | T009 |
| T011 | T010 |

## Kernel consumers

| Kernel task | Tasks here |
| --- | --- |
| kernel T224 ("Implement Modules Spec V1") | T001–T008 |
| kernel T259 ("Implement Modules Spec V2") | T009–T011 |
