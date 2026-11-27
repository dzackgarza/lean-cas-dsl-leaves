# Research: Core Modules category implementation (`cat.core_modules_r`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Ranks are computed.** The v1 ranks of $A_n$, $A_n^\vee$ and $E_8$ are literals that the engine returns unchanged (`sage_modules.py:50-52` at `8b181d7`). The rank is Sage `rank()` of the module that the lowering of the form builds (LV1, LV12).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1), T004 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
