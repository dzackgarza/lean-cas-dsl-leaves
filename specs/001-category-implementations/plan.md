# Implementation Plan: Category implementations for the computational milestones

**Branch**: `001-category-implementations` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); [data-model.md](data-model.md);
[contracts/backend-program.md](contracts/backend-program.md); [quickstart.md](quickstart.md)

## Summary

Write one backend program for each computational milestone, as glue over the engines of the
research container, against the released contract `cas-computation/2` and its generated
category interface. Move the 115 existing registrations into those programs, replace their
hand-rolled and lookup answers by engine routines, remove the engine fallbacks, declare the
SDK and Julia dependencies, and add a tier 1 test harness that drives each real backend through
the contract's protocol peer with durable logs and timing records.

## Technical Context

**Language/Version**: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`)
for the backends; Julia 1.12.7 through `juliacall` 0.9.36 for Catlab.jl and Oscar.jl.
**Primary Dependencies**: contract SDK `lean-cas-dsl-leaf-contracts` at tag `v2.0.0`, then
`v2.0.1` (contract FR-022); SageMath 11.0.beta5 with GAP 4.16.1 (`libgap`), PARI 2.17.4
(`cypari2`), Singular 4.4.1, Maxima 5.49.0; SymPy 1.14.0; Macaulay2 1.24.11; Catlab.jl 0.17.7;
Oscar.jl 1.8.2 with Hecke 0.39.22.
**Storage**: committed files only: `leaves.json`, `tests/logs/`, `tests/timing/records.jsonl`.
**Testing**: `just test` (tier 1, `uv run --frozen pytest tests`) after `just setup`; one
category with `just test-category NAME`; `just test-commit` (manifest and compilation) at commit.
**Target Platform**: the research container `ghcr.io/dzackgarza/sage:develop` (LV21).
**Project Type**: provider package: a manifest and backend programs.
**Performance Goals**: tier 1 of one category under five minutes (SC-004).
**Constraints**: permitted inputs only (LV14); no hand-rolled algorithm without a survey gap
(LV6); no field computed that no request demands (LV25).
**Scale/Scope**: 25 milestones, 115 moved registrations, 23 backend programs.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1, FR-034 | Each program has one lowering table; lookups and duplicated data are deleted. |
| LV2, LV14 | No document or test here holds an acceptance statement or expected answer; kernel tasks are named by ID. |
| LV3 | Each milestone task implements the complete generated interface of its categories, less the ports that a later milestone moves. |
| LV4 | Tier 1 checks retention of supplied endpoints and earlier outputs in each reply. |
| LV5–LV7 | Each milestone task starts with its survey record; the routine table names each port's routine. |
| LV8 | Programs that need another category's operation suspend through the SDK and handle `NoImplementation`. |
| LV10, LV11 | `leaves.json` holds no priority; replies use the contract statuses. |
| LV12 | Each moved registration keeps its routine unless the survey records it as wrong (FR-027). |
| LV13 | Tasks follow the kernel order T200–T224, after F. |
| LV16, LV21 | One interpreter; `pyproject.toml`, `uv.lock`, `Project.toml`, `Manifest.toml`; `lakefile.toml` deleted. |
| LV17–LV23 | `tests/conftest.py` writes logs and timing records; scenarios drive real processes. |

Gate result: pass. No violation needs a justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-category-implementations/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/backend-program.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
leaves.json                    manifest: v2 backends only (contract FR-004)
pyproject.toml, uv.lock        contract SDK at its release tag; pytest (dev)
Project.toml, Manifest.toml    Julia project: Catlab.jl 0.17.7, Oscar.jl 1.8.2
justfile                       setup, test-commit, test, test-category, test-push
backends/engine.py             shared start-up, logging, timing, routine observations, serve()
backends/<program>.py          one backend program per row of the milestone table below
tests/conftest.py              run log and timing records (LV22, LV23)
tests/harness.py               starts a backend under /sage/.venv/bin/python3 and runs cas-peer
tests/test_<program>.py        tier 1 of one program
tests/scenarios/<program>-*.json
tests/logs/, tests/timing/records.jsonl
specimens/{missing,wrong,malformed,unavailable}/   deliberately bad v2 packages
```

**Structure Decision**: one backend program for each milestone (research R3): a milestone is
the unit that the kernel consumes, one process keeps one engine session, and a test of one
milestone starts no other program (LV16). The v1 programs (`sage_backend.py`, `gap_backend.py`,
`sage_power_set.py`, `sage_set_limits.py`, `sage_fin_rev.py`, `gap_groups.py`,
`sage_presentations.py`, `sage_symbolic.py`, `sage_modules.py`, `sage_discriminant.py`,
`sage_bilinear_lift.py`), `engine_python.py` and `wire.py` leave the manifest at T003 and are
trashed by the task that moves their last registration (research R4).

## Milestone map

Each row is one requirement of the spec, its backend program, the v1 programs whose
registrations move in, the tests, and the kernel task that consumes it. The engine entry points
are the routines of the spec row; the routine table of each program is written in its survey
record ([research.md](research.md), "Survey record").

| FR | Program (`backends/`) | Moves from | Tests (`tests/`) | Kernel task |
| --- | --- | --- | --- | --- |
| FR-001 | `sets.py` (Sage; Catlab.jl by `juliacall` for `lim.sets.pullback`) | `sage_backend.py`, `gap_backend.py`, `gap_groups.py`, `sage_power_set.py`, `sage_set_limits.py`, `sage_fin_rev.py`, `sage_presentations.py`, `sage_symbolic.py` | `test_sets.py` | T200 |
| FR-002 | `finite_sets.py` | `sage_backend.py` | `test_finite_sets.py` | T201 |
| FR-003 | `orders.py` (Sage posets; GAP Digraphs) | — | `test_orders.py` | T202 |
| FR-004 | `rings.py` (Sage, GAP); `calculus.py` (SymPy, Sage symbolic ring) | `gap_backend.py`, `gap_groups.py`, `sage_symbolic.py` | `test_rings.py`, `test_calculus.py` | T203 |
| FR-005 | `core_groups.py` (GAP) | — | `test_core_groups.py` | T204 |
| FR-006 | `commutative_rings.py` (Sage, Singular) | `sage_presentations.py`, `sage_symbolic.py` | `test_commutative_rings.py` | T205 |
| FR-007 | `topological_monoids.py` | — | `test_topological_monoids.py` | T206 |
| FR-008 | `modules.py` | `sage_modules.py` | `test_modules.py` | T207 |
| FR-009 | `bilinear_forms.py` (Sage, PARI) | `gap_groups.py`, `sage_discriminant.py`, `sage_modules.py` | `test_bilinear_forms.py` | T208 |
| FR-010 | `fields.py` | `sage_symbolic.py` | `test_fields.py` | T209 |
| FR-011 | `module_rank.py` | `sage_modules.py` | `test_module_rank.py` | T210 |
| FR-012 | `module_kernels.py` | — | `test_module_kernels.py` | T211 |
| FR-013 | `formed_modules.py` | `sage_bilinear_lift.py` | `test_formed_modules.py` | T212 |
| FR-014 | the programs of FR-001–FR-013; `calculus.py` gains series | — | the tests of those programs | T213 |
| FR-015 | `group_kernels.py` (GAP) | `gap_groups.py` | `test_group_kernels.py` | T214 |
| FR-016 | `boolean_algebras.py` | — | `test_boolean_algebras.py` | T215 |
| FR-017 | `integral_lattices.py` | `gap_groups.py`, `sage_modules.py` | `test_integral_lattices.py` | T216 |
| FR-018 | `set_constructions.py` (Sage; Catlab.jl) | — | `test_set_constructions.py` | T217 |
| FR-019 | `well_orders.py` (SymPy, Sage) | — | `test_well_orders.py` | T218 |
| FR-020 | `algebraic_structures.py` (Sage, GAP) | — | `test_algebraic_structures.py` | T219 |
| FR-021 | `algebras.py` | — | `test_algebras.py` | T220 |
| FR-022 | `schemes.py` | — | `test_schemes.py` | T221 |
| FR-023 | `module_constructions.py` (Sage; Macaulay2 by `sage.interfaces.macaulay2`) | — | `test_module_constructions.py` | T222 |
| FR-024 | `forms_over_rings.py` (Sage); `forms_over_rings_hecke.py` (Oscar/Hecke, no Sage import) | — | `test_forms_over_rings.py` | T223 |
| FR-025 | `lattices.py` (Sage, PARI); `lattices_hecke.py` (Oscar/Hecke, no Sage import) | — | `test_lattices.py` | T224 |

Every program imports `backends/engine.py` and the SDK, and no other program. A program that
needs an operation of another category asks the kernel (LV8); research R7 gives the rule.

## Tests of each program

Each `tests/test_<program>.py` starts the program under `/sage/.venv/bin/python3` with the SDK
of `.deps/` on `PYTHONPATH` and runs `cas-peer run SCENARIO -- COMMAND` for each scenario. The
scenarios are built from the generated interface of the program's categories. Each test checks:

1. negotiation with the four protocol-2 features and `routine-observations/1`;
2. for each port: a reply at the generated result layout, with the routine observation of the
   routine table;
3. for each port whose request carries selected data: those data in the reply where the layout
   retains them;
4. one unsupported presentation: `status:"unsupported"` with the exact `op`;
5. for a program that suspends: the continuation after a `noImplementation` slot;
6. one log file and one timing record per test.

No test asserts a mathematical value (LV18).

## Sequencing

1. Before F: FR-033 (contract findings) and FR-036 (findings to an issue). They need no release.
2. At contract `v2.0.0` (kernel F): setup, harness, shared engine module, manifest in v2 form
   (FR-026, FR-029–FR-032, FR-034 at the shared level).
3. FR-001 to FR-013 in the kernel order T200–T212; each starts with its survey record (FR-028).
4. At kernel T105: the dependency moves to `v2.0.1`; the public-only check (SC-007) and the
   specimens (FR-035).
5. FR-014 to FR-025 in the kernel order T213–T224.
6. Timing triage (LV24) after all functionality.

## Complexity Tracking

No constitution violation needs a justification.
