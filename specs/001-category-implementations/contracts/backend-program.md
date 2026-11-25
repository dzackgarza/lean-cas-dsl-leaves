# Contract of a backend program of this repository

This file states what every program under `backends/` provides. The wire protocol is the
contract's `cas-computation/2` ([protocol-2][P]); this file adds no frame and no field.

## Start

- Command: `/sage/.venv/bin/python3 -m backends.<program>` in the repository root, with the SDK
  on `PYTHONPATH` (research R1).
- `backends/engine.py` imports the program's engines once, before the ready frame. When an
  engine is absent, the program writes the import error to standard error and exits with a
  nonzero status before the ready frame (LV11, LV21).
- The ready frame advertises `scoped-values/2`, `deferred/2`, `suspend-resume/2`,
  `export-capture-frames/2` and `routine-observations/1` (contract FR-002, FR-013).

## Requests

- A program handles only the `(op, input)` pairs that `leaves.json` registers for it.
- It reads every operand from the request at its generated layout: receiver, residual action
  descriptors and method functor for an inherited method (contract FR-017); the source arrow and
  both image endpoints for a functor map action (contract FR-018); the outputs of earlier fields
  for a lift field.
- It builds engine inputs through its lowering table only (LV1).

## Replies

- A successful reply is built by `cas_interfaces` at the generated result layout, with the
  selected data that the layout retains (LV4).
- Each successful, deferred or suspended reply carries a routine observation naming the engine
  and the routine of the routine table (contract FR-013; LV5).
- An unsupported presentation: `status:"unsupported"` with the exact `op`. An engine failure:
  `status:"error"` with `kind` and `message`. A predicate that the engine cannot establish:
  `status:"unknown"` (contract FR-011, FR-012; LV11).
- A lazy field is an export token with its captures (contract FR-007; LV25).

## Asking the kernel

A program that needs an operation of another category suspends with that call (contract
FR-010). On resume it receives a value or `cas_session.NoImplementation(operation, input)` and
continues under its own control logic (LV8). It never writes `noImplementation`.

## Logs

One line per request on standard error ([data-model.md](../data-model.md), "Backend log line"),
beside the SDK's own lines (contract FR-023).

[P]: https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/blob/main/specs/001-released-contract-v2/contracts/protocol-2.md
