# Implementation Plan: Arrows of Formed Modules category implementation (`cat.arrows_bilin_module`)

**Branch**: `027-arrows-bilin-module` (on `main`) | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md); [research.md](research.md); the shared [plan](../001-category-implementations/plan.md), [data model](../001-category-implementations/data-model.md), [backend contract](../001-category-implementations/contracts/backend-program.md) and [quickstart](../001-category-implementations/quickstart.md) of 001.

## Summary

Implement `cat.arrows_bilin_module` in `backends/arrows_bilin_module.py` as glue over the engine routines of the routine table below, in version V1, and move the existing registrations that belong to it. Each version starts with its survey record and ends with the task that the kernel consumes.

## Technical Context

The technical context of 001 applies: Python 3.14 of the research container's SageMath (`/sage/.venv/bin/python3`), the contract SDK at its release tag, tier 1 through `cas-peer`, the research container as the one platform.

**Engine**: Sage free modules with an inner product matrix (`submodule`, `gram_matrix()`, inclusion homomorphisms and their sections) (engine survey, "Bilinear and quadratic modules").
**Module**: `backends/arrows_bilin_module.py`, run as `/sage/.venv/bin/python3 -m backends.arrows_bilin_module` (001 research R3).
**Code dependencies** (LV8, second option; LV16): `backends/bilin_module.py` (spec 026). The module imports their lowering tables or functions; it imports no other category module.
**Tests**: `tests/test_arrows_bilin_module.py`, `tests/scenarios/arrows_bilin_module-*.json`.

## Constitution Check

| Article | Plan conformance |
| --- | --- |
| LV1 | One lowering table in `backends/arrows_bilin_module.py`; named objects whose data no engine constructor builds read the unfolded definition of the request. |
| LV2, LV14 | No acceptance statement or expected answer; kernel tasks are named by ID or title. |
| LV3 | Each row of each version has a port, or a gap record of mathematically new work. |
| LV4 | Each routine computes from the selected data of the request; tier 1 checks their retention. |
| LV5–LV7 | Each row names its engine routine; each version starts with its survey record. |
| LV8 | Dependent inputs arrive as operands, through declared code dependencies or by a kernel request (column "Dependent inputs"). |
| LV12 | Each moved registration has a decision (table "Registrations that move"). |
| LV13 | The survey task of each version follows the versions of the categories that its rows reach. |

Gate result: pass.

## Project Structure

```text
specs/027-arrows-bilin-module/
├── spec.md
├── plan.md
├── research.md          decisions and the survey record (LV7)
├── checklists/requirements.md
└── tasks.md

backends/arrows_bilin_module.py
tests/test_arrows_bilin_module.py
tests/scenarios/arrows_bilin_module-*.json
```

**Structure Decision**: the data model, the backend contract and the quickstart of 001 apply unchanged; this feature adds no document of those kinds.

## Routine table

The starting choice of each row. The survey record of its version confirms it in the research container or replaces it with its reasons (LV7).

### V1

| FR | Row | Kind | Engine and routine | Dependent inputs (C22) | Inputs before it |
| --- | --- | --- | --- | --- | --- |
| FR-001 | `lift.bilin_module.restrict` | lift | `#obj`: Sage `submodule` of the supplied inclusion image with `gram_matrix()` of the restricted form; `#hom`: the Sage inclusion homomorphism; `#forward` and `#backward`: the Sage homomorphisms between the restricted object and the base apex, built from the supplied inclusion | the four fields with the outputs of the preceding fields that the request supplies; descriptors lowered by the lowering table of `backends/bilin_module.py` (LV8, second option) | lean-categories T029 (#192) |
| FR-002 | `lift.bilin_module.change_value_restriction` | lift | the routines of `lift.bilin_module.restrict` applied to the form that `fun.bilin_module.change_value` returns | the selected change of values and the fields of the lift; asks the kernel for the action of `fun.bilin_module.change_value` (LV8, third option); receives the result or `NoImplementation` | lean-categories T029 (#192) |

## Registrations that move

Each row is one registration of `leaves.json` at `8b181d7`. Its version is the later of the versions of its operation row and its input row, and not earlier than the first version of this spec (001 research R15).

| Operation | Input | v1 backend | Version | v1 routine | Decision |
| --- | --- | --- | --- | --- | --- |
| `lift.bilin_module.restrict#backward` | `lift.bilin_module.restrict#input` | `sage-bilinear-lift` | V1 | FiniteSetMaps(points).one()  [identity map of the point set] | Replace a lookup by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the leaf answers the comparison between the image of the restricted object and the base apex as the identity on point keys (sage_bilinear_lift.py:128-133)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `lift.bilin_module.restrict#forward` | `lift.bilin_module.restrict#input` | `sage-bilinear-lift` | V1 | FiniteSetMaps(points).one()  [identity map of the point set] | Replace a lookup by the routine of the routine table (LV6, LV12); delete the leaf-held datum (the leaf answers the comparison between the image of the restricted object and the base apex as the identity on point keys (sage_bilinear_lift.py:128-133)): the routine runs on the engine value of this module's lowering table or on the data of the request (LV1). |
| `lift.bilin_module.restrict#hom` | `lift.bilin_module.restrict#input` | `sage-bilinear-lift` | V1 | none: the supplied inclusion graph is returned as a typedMap | Replace a lookup by the routine of the routine table (LV6, LV12). |
| `lift.bilin_module.restrict#obj` | `lift.bilin_module.restrict#input` | `sage-bilinear-lift` | V1 | FiniteSetMaps(...).from_dict(table)  [lookup of a supplied graph]; cartesian_product(points, points) | Replace a hand-rolled algorithm by the routine of the routine table (LV6, LV12). |

| Version | Registrations |
| --- | ---: |
| V1 | 4 |
| Total | 4 |

The move task of the version named here moves the last registration of these v1 programs and trashes them:

| v1 program | Version |
| --- | --- |
| `backends/sage_bilinear_lift.py` | V1 |

## Hand-rolled code

No row of this plan needs hand-rolled mathematics: each routine is an engine routine or control logic over engine routines (LV6). Where the survey record finds no engine for a row, the row is known mathematics with a cited reference, or a gap record of mathematically new work; mathematically new work is out of scope (LV6).

## Engine survey

The survey record of each version starts from these sections of the kernel engine survey of 2026-11-25: "Bilinear and quadratic modules".

## Complexity Tracking

No constitution violation needs a justification.
