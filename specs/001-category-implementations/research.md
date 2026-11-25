# Research: Category implementations — the shared foundation and the spec list

Each decision names its source. The facts about engines and the container come from the engine
survey of 2026-11-25 (lean-cas-dsl `specs/001-categorical-research-language/research/engine-survey.md`,
marks [C] verified in the container, [W] read in a web source). The facts about this
repository's registrations come from `leaves.json` at `8b181d7`, equal to `efecce8`.

## Decisions

**R1. Interpreter and SDK.** Decision: every backend runs as
`/sage/.venv/bin/python3 -m backends.<slug>`, in the repository root (R3). `just setup` installs
the locked dependencies of `pyproject.toml` (the contract package at tag `v2.0.0`, with the
SDK and its `pydantic`) for that interpreter into `.deps/`:
`uv export --frozen --no-dev --format requirements-txt | uv pip install --python /sage/.venv/bin/python3 --target .deps -r -`.
The test harness puts `.deps` on `PYTHONPATH`; in production the kernel puts the `python`
directory of the contract revision that it pins on `PYTHONPATH` (`README.md`), and kernel T105
checks that it is the same release. Sources: LV16, LV21; survey "Container result" (SageMath
importable from `/sage/.venv/bin/python3` [C], Python 3.14.10 [C], no passagemath [C]);
contract plan "Technical Context" (`pydantic` is the SDK's frame-model dependency, `uv sync
--frozen`). Rejected: a second virtual environment that must import Sage, because the survey
shows Sage only in `/sage/.venv` and a derived environment's access to its site packages is
not established by any record.

**R2. Julia packages.** Decision: `Project.toml` and `Manifest.toml` at the repository root
declare Catlab.jl 0.17.7, which the pullback of `cat.sets` uses (spec 003); a Julia package
enters the project with the first row whose routine needs it (Oscar.jl with Hecke for the
categories of forms and lattices; plan, "Categories with no spec"); `just setup` runs
`julia --project=. -e 'using Pkg; Pkg.instantiate()'`. `backends/engine.py` sets
`PYTHON_JULIACALL_EXE=/usr/local/bin/julia` and `PYTHON_JULIACALL_PROJECT` to the repository
root in its own process before it imports `juliacall`. Sources: the kernel engine survey: Catlab.jl 0.17.7 with the category of finite sets and its
limits [W S57], `juliacall` 0.9.36 and Julia 1.12.7 [C], Catlab source in the depot but not in the default project [C], `juliacall` can use an
existing Julia through those two variables [W S44].

**R3. One module and program per category implementation.** Decision: the category
implementation of `cat.<id>` is the module `backends/<slug>.py` and its program
`/sage/.venv/bin/python3 -m backends.<slug>`, one backend row of `leaves.json`. Reasons: the
category is the unit of responsibility (LV3) and of a spec (FR-038); a tier 1 test of one category
starts one program (LV16); a module imports another category module only where its plan declares
the code dependency (LV8, second option). C23 requires no process per category; the engine
start-up of each process is a measured cost for the timing triage (LV24, LV25), and grouping
several category modules in one process is a remedy that the triage may select after
functionality.

**R4. The v1 programs leave the manifest at setup.** Decision: the setup task rewrites
`leaves.json` to the protocol-2 form with only protocol-2 programs. The v1 programs stay in
`backends/` as the source of their moves. The move task of the category spec version that moves
the last registration of a v1 program trashes it:

| v1 program | Trashed by the move task of |
| --- | --- |
| `backends/gap_backend.py` | 015-rings V1 |
| `backends/gap_groups.py` | 031-integral-lattice V2 |
| `backends/sage_backend.py` | 005-finite-sets V2 |
| `backends/sage_bilinear_lift.py` | 027-arrows-bilin-module V1 |
| `backends/sage_discriminant.py` | 020-bil-wform V1 |
| `backends/sage_fin_rev.py` | 003-sets V1 |
| `backends/sage_modules.py` | 031-integral-lattice V2 |
| `backends/sage_power_set.py` | 004-core-sets V1 |
| `backends/sage_presentations.py` | 016-commutative-rings V1 |
| `backends/sage_set_limits.py` | 004-core-sets V1 |
| `backends/sage_symbolic.py` | 016-commutative-rings V2 |

Reasons: the contract admits a manifest all or none and requires `preferredRoutes` on every
registration (contract FR-004, T005); a v1 `ready` frame fails negotiation (contract FR-002).

**R7. Operations of another category.** Decision: a module computes the operations of its own
category. For an operation of another category it either imports the code of that category's
module, where its plan declares the code dependency (LV8, second option; for example the lowering
table of `backends/sets.py`), or asks the kernel by an adaptive suspension or a deferred program
(LV8, third option; contract FR-009, FR-010). The column "Dependent inputs" of each routine table
names the choice. A module never imports a module of a later category in the structural order.

**R8. Lowering tables.** Decision: each category module has one table from the named-object
descriptors of its category to engine constructors (LV1). A named object whose defining data no
engine constructor builds reads them from the unfolded definition of the request (K:C22). Each
category spec names the v1 tables and literal data that its moves delete, with their source lines
at `8b181d7`.

**R9. Protocol peer for tests.** Decision: `just setup` checks that the contract checkout
`/repos/lean-cas-dsl-leaf-contracts` is at the declared tag (`git describe --exact-match`) and
runs `lake build cas-peer` there; it fails when the checkout is at another revision. The harness
calls that binary. Sources: contract FR-020 (`lake exe cas-peer`); one checkout per repository
(`~/gitclones/<repo>`, seen as `/repos/<repo>` in the container).

**R10. Logs and timing records.** Decision: `tests/conftest.py` writes
`tests/logs/<UTC>-<revision>.log` with the pytest report and each backend's standard error, and
appends one JSON line per test and one per handled request to `tests/timing/records.jsonl`
([data-model.md](data-model.md), "Timing record"). Each backend writes one standard-error line
per request with its elapsed time and routine (contract FR-023 format for the SDK lines).
Sources: LV22, LV23; contract plan (`tests/conftest.py` writes logs and records).

**R11. Where tier 1 runs.** Decision: `just test` and `just test-category` run inside the
research container; `test-push` runs `just test` there through the host launcher of the shared
container guide (`AGENTS.md`); `test-commit` and CI keep the manifest and compilation check,
because the CI runner has no research container. Sources: LV17, LV20, LV21.

**R12. Undeclared wire forms.** Decision: a row whose answer needs a form that the contract does
not declare (FR-033) is not registered until the contract declares the form. The forms are the
ten items of
[lean-cas-dsl-leaf-contracts#14](https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/issues/14);
contract task T021 declares them before the release `v2.0.0`. Each routine table names contract
T021 in the column "Inputs before it" of each row that needs one of them. Source: `DEFECTS.md`,
section of 2026-10-21; LV14; RC8.

**R15. Placement and version of the existing registrations.** Decision: a registration belongs to
the latest category, in the structural order, among the category that the roadmap record assigns
to it, the home of its operation row and the home of its input row (a field address `row#field`
counts as its row). Its version is the later of the versions of its operation row and its input
row, where each is a row of the roadmap, and not earlier than the first version of its spec.
Reasons: a registration answers its operation at its input form, and the lowering of that input
is in the implementation of the input row's home (LV1, one lowering table); a registration moves
when its rows are implemented. Consequence: `meth.cardinality` and `prop.is_finite` at
`obj.sets.units` move to Monoids (spec 011), not to Core Sets and Sets, because `obj.sets.units`
has its home in `cat.monoids`. Every registration has exactly one place (FR-039).

**R16. Categories, rows and versions.** Decision: the categories, their structural order, their
rows, the version of each row and the home rule are those of the roadmap record of lean-cas-dsl
at `0e6ccbd` (`specs/001-categorical-research-language/research/category-scope.json`, read on
2026-11-25). That record is the planner's input; it holds statement identifiers of the
acceptance corpus and is not an input of a leaf author (LV14). The category specs hold its rows
and versions and none of its statements. A category whose record has no row has no spec
(plan, "Categories with no spec"). A non-structural functor belongs to the later of its two
ends (for example `fun.monoids.units` belongs to `cat.groups`). The rows that a computation needs
and the catalogue lacks are assigned by the same home rule to the category whose rows they
extend; their assignment is a reading of their descriptions, since the catalogue has no row for
them yet.

**R17. Feature order.** Decision: the feature order of [tasks.md](tasks.md#feature-order) runs the
V1 versions in the structural order, starting with Sets (spec 003); Cardinals (spec 002), which has
no structural chain to `cat.sets` and no input category, enters directly before Core of sets (spec
004), the first version that consumes it. Then comes the move to the release `v2.0.1`, then the V2
versions in the structural order. Reasons: the work starts with `cat.sets` (LV13; K:C23); a
category with no inputs enters with the first milestone that needs it; V2 holds the full-B0
statements, which follow kernel T105 as the full-B0 milestone did; each V1 version follows the V1
versions of the categories that its rows reach (LV13). The directory number is not the order. A leaf task names a lean-categories task only where a
row of the task consumes a declaration that the lean-categories task adds or changes; the other
upstream tasks of the kernel's milestones are inputs of the kernel tasks, not of the leaf tasks.

## Survey record

LV7 fixes the content. Each version of each category spec completes the survey record in the
spec's `research.md` before its implementation tasks: one row for each part of the generated
interface that its rows need, with the routine, the engine version or revision, the decision
(use, fallback, reject) and the reasons, and one row for each gap with its searches. The starting
facts of each family are those of the kernel engine survey, cited by section in the plan of the
spec. That survey (lean-cas-dsl `specs/001-categorical-research-language/research/engine-survey.md`)
holds engine and container facts only, with no workload statement, expected answer or kernel
source, so it is a backend resource of the leaf author (LV14); the kernel category tasks name it as
the planning survey from which each survey record starts.

Row format:

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |

A gap row has the engine column empty and names each search.

## Registrations that move

The 115 registrations of `leaves.json` at `8b181d7` move into the category specs by R15. The
[plan](plan.md#category-specs) gives the count of each spec and version, and the plan of each spec
lists its registrations with their versions and decisions.
