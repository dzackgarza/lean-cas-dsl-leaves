# Research: Modules category implementation (`cat.modules_r`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. The V1 scalar action is the row of one universe.** The row `op.modules.scalar_action` of the catalogue at `3f8aedf` takes a ring and a module of one universe, and V1 implements it. lean-categories T064 (#211) declares it for independent universes for the construction classification of lean-cas-dsl #23 (kernel T146, first consumer T143); no V1 row consumes that change, so it is an input of no V1 task (001 research R17).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1), T009 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
