# Quickstart: Category implementations

All commands run inside the research container (`ghcr.io/dzackgarza/sage:develop`), in
`/repos/lean-cas-dsl-leaves`, unless a step says otherwise.

## Setup (explicit, outside the ordinary loop)

1. The contract checkout `/repos/lean-cas-dsl-leaf-contracts` is at the declared release tag
   (`v2.0.0` until kernel T105, then `v2.0.1`).
2. `just setup`: installs the locked SDK for `/sage/.venv/bin/python3` into `.deps/`, instantiates
   the Julia project, and builds `cas-peer` in the contract checkout (research R1, R2, R9).

## Ordinary loop

- `just test-category sets`: tier 1 of `backends/sets.py`; writes one log under `tests/logs/`
  and one timing record per test and per handled request to `tests/timing/records.jsonl`.
- `just test-commit`: manifest and compilation check, run by the commit hook.

## Milestone run

- `just test`: tier 1 of every program. `test-push` runs it through the host launcher of the
  shared container guide.

## Add a category implementation

1. Load the interface: `cas_interfaces.load_interfaces("/repos/lean-cas-dsl-leaf-contracts/api/declared-ports.json").category("cat.<id>")`.
2. Complete the survey record of the version in the category spec's `research.md` (LV7; spec
   FR-028).
3. Write `backends/<slug>.py` as glue over the routines of the spec's routine table, with one
   lowering table (LV1, LV5).
4. Register each port in `leaves.json` with `preferredRoutes: []`.
5. Write `tests/test_<slug>.py` and the scenarios `tests/scenarios/<slug>-<CASES>-*.json` of the
   task; run `just test-category <slug> <CASES>`.
6. Commit with the survey section cited in the body.

## Check the public-only path (SC-007)

In a container started from the image with only `/repos/lean-cas-dsl-leaves` and
`/repos/lean-cas-dsl-leaf-contracts` mounted, so that no lean-cas-dsl checkout is visible, run
Setup and `just test-category sets`. Every command passes; the run log and the timing records
are committed.
