# Data model: Category implementations

## Manifest (`leaves.json`)

The shape is the contract's (contract FR-004): exactly the root arrays `backends` and
`registrations`.

| Entity | Fields | Rules |
| --- | --- | --- |
| Backend | `name`, `command`, `args` | `name` is the module slug of the plan's table "Category specs"; `command` is `/sage/.venv/bin/python3`; `args` is `["-m", "backends.<slug>"]` (research R1, R3). |
| Registration | `operation`, `input`, `backend`, `preferredRoutes` | `operation` and `input` are published addresses; `preferredRoutes` is present, `[]` unless a C6 route is declared (LV10). No priority, order or cost field. |

## Category implementation

| Field | Content |
| --- | --- |
| Category | The `cat.*` id of its category spec (spec FR-038) |
| Ports | One registration for each implemented part of the generated interface |
| Lowering table | Named-object descriptor to engine constructor, one per program (LV1, research R8) |
| Routine table | For each port: engine, routine, version; written in the survey record and sent as routine observations |
| Survey record | The section "Survey record" of its spec's `research.md`, in the row format of [research.md](research.md) (LV7) |
| Gaps | Parts with no engine routine and no admissible hand-rolled algorithm, with their searches |

## Survey record row

`part`, `engine and routine`, `version or revision`, `decision` (`use`, `fallback`, `reject`),
`reasons`, `gap searches`. A gap row has the engine column empty and names each search.

## Run log

`tests/logs/<UTC>-<revision>.log`: the pytest report and the standard error of each backend that
the run started, in order. Committed.

## Timing record

One JSON object per line in `tests/timing/records.jsonl`. Committed.

| Field | Content |
| --- | --- |
| `run` | UTC start time and a run id shared by the records of one run |
| `revision` | `git rev-parse HEAD` and the dirty flag |
| `environment` | container image digest, SageMath version, Python version, contract tag |
| `kind` | `test` or `computation` |
| `id` | the pytest node id, or the request id with its `op` and `input` |
| `input` | the scenario path and its SHA-256 |
| `engine_startup_s`, `setup_s`, `construction_s`, `request_s`, `total_s` | measured seconds; `request_s` and `construction_s` come from the backend's per-request log line |
| `outcome` | `passed`, `failed`, or the reply status of a computation |

## Backend log line

One line on standard error per handled request:
`<UTC> <slug> request=<id> op=<op> input=<input> routine=<engine>:<routine> elapsed_s=<s> status=<status>`.
The SDK's own frame, handler, export, suspension, resume and disposal lines (contract FR-023)
come in the same stream.

## Scenario

A JSON file of `tests/scenarios/` in the format of the contract's `cas-peer run`: the frames that
the driver sends and the frames or outcomes that it expects. Request bodies come from the
generated interface (`cas_interfaces`); expected replies fix layout, retained selected data,
routine observation and status, never a mathematical value (LV18).
