# Feature Specification: Cardinals category implementation (`cat.cardinals`)

**Feature Branch**: `002-cardinals` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the shared feature [001](../001-category-implementations/spec.md) (FR-026 to FR-036, FR-038, FR-039).

**Input**: the category implementation of `cat.cardinals` against the released contract `cas-computation/2`, in version V1, with the rows, versions and existing registrations of the programme roadmap (001 research R15, R16).

This document is an input of a leaf author (LV14). It names catalogue rows, engines and routines, this repository's registrations and the IDs of the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category

- **Catalogue ID**: `cat.cardinals`.
- **Object**: a cardinal number (Mathlib `Cardinal`).
- **Morphism**: an identity: the catalogue declares the cardinals as a discrete category.
- **Engine**: Sage `Integer` for finite cardinals. No surveyed engine supplies $\aleph_0$ or its arithmetic; this implementation computes them by the known method, with Mathlib's cardinal arithmetic (`Mathlib.SetTheory.Cardinal.Arithmetic`) as its cited reference (LV6).

## Versions

| Version | Content | Rows | Registrations that move |
| --- | --- | ---: | ---: |
| V1 | every computation of the spike and every statement that the kernel V1 definition requires computed | 2 | 0 |

**V3.** The classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds rows to V3 by the same membership rule: a row joins the first version of a computed statement that needs it, and it belongs to the latest category, in the structural order, among its catalogue owners and the categories of its declared parameters. When kernel tasks T140 to T147 produce the classified statements, the rows whose home is `cat.cardinals` join V3 of this spec. This spec plans nothing more for V3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — V1: the computations of the spike and of kernel V1 (Priority: P1)

A researcher reads the size of a finite set as a natural number and the size of a countably infinite set as $\aleph_0$, and reads the size of a product, a sum or a finite power of such sets as a cardinal of the same kind. A researcher writes the cardinal $2^{\kappa}$ of a finite cardinal $\kappa$ when the catalogue declares cardinal exponentiation.

**Why this priority**: the categories that follow this one in the structural order consume it, and the kernel's computational milestone of this version needs a computed result through it (LV13; K:C23).

**Independent Test**: `just test-category cardinals` starts `backends/cardinals.py` under `/sage/.venv/bin/python3` and drives it with `cas-peer` scenarios that the generated interface of `cat.cardinals` builds (001 plan, "Tests of each program"). The acceptance suite of lean-cas-dsl judges the computed results in kernel T201 ("Implement Cardinals Spec V1"); this repository does not hold it (LV2).

**Acceptance Scenarios**:

1. **Given** the generated interface of `cat.cardinals`, **When** the backend receives a request at a port of V1, **Then** it calls the routine of the plan's routine table, names it in its routine observations and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, parameters, cones or earlier outputs, **When** the backend replies, **Then** the reply retains those data where the result layout retains them, and no recomputed substitute (LV4).
3. **Given** a request whose input presentation the implementation does not support, **When** the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no substitute value is sent (LV11).

---

### Edge Cases

The edge cases of 001 apply. This category adds:

| Situation | Required behaviour | Source |
| --- | --- | --- |
| A cardinal above $\aleph_0$ is requested (for example $2^{\aleph_0}$) | `status:"unsupported"`: the catalogue declares no uncountable cardinal literal, and this implementation does not invent one | LV1, LV11 |

## Requirements *(mandatory)*

### Functional Requirements — V1

- **FR-001 — `lit.cardinals`** (operation, V1). Catalogue: A cardinal as the language writes it: a numeral or `ℵ₀`. The implementation MUST return the value of the literal or numeral descriptor at the generated layout.
- **FR-002 — Arithmetic of finite cardinals and $\aleph_0$** (V1). The module MUST supply the sum, the product and the finite power of finite cardinals and $\aleph_0$ as code that the cardinality implementation of `cat.core_sets` (spec 004) calls (LV8, second option). It is the known method, with Mathlib `Mathlib.SetTheory.Cardinal.Arithmetic` as its cited reference (LV6). It is not a port: the catalogue declares no operation of `cat.cardinals` other than `lit.cardinals`. A reply whose computation uses it names this implementation and its reference in its routine observations (contract FR-013).
- **FR-003 — `missing.cardinal_power`** (row that the catalogue lacks, V1): exponentiation of cardinals $2^{\kappa}$ (Mathlib `Cardinal.power`). The implementation MUST compute it once lean-categories declares the row; until then no port answers it (LV1, LV14). Inputs before it: the lean-categories task that declares `missing.cardinal_power` (none at lean-categories `fc549baa`).

### Key Entities

- **Category implementation of `cat.cardinals`**: the module `backends/cardinals.py`, its lowering table, its routine table and its ports (001 data model, "Category implementation").
- **Survey record**: the section "Survey record" of [research.md](research.md) (LV7).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (V1): each of the 3 requirements FR-001 to FR-003 is met: each row has a registered port whose tier 1 scenario passes, or an LV7 gap record of mathematically new work with its searches. A code requirement is met when the implementation that it names calls it.
- **SC-002** (V1): tier 1 of `cardinals` runs in under five minutes in the research container and writes one log and one timing record per test.
- **SC-003** (V1): kernel T201 ("Implement Cardinals Spec V1") consumes the version with no kernel-side evaluation of a row of this version.

## Assumptions

- Kernel readiness F and contract release `v2.0.0` precede V1; contract release `v2.0.1` (kernel T105) precedes V2 (001 FR-026).
- The catalogue is the one that the contract release publishes (mathematics revision `3f8aedf` at the roadmap reading); the rows and their versions are those of 001 research R16.
- Engine versions are those of the research container on 2026-11-25; the survey record of each version records the versions that it uses.
