# Research: Arrows of Formed Modules category implementation (`cat.arrows_bilin_module`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Replace the Python restriction.** The v1 restriction loops over pairs of points and answers the comparisons as the identity on point keys (`sage_bilinear_lift.py:94-133` at `8b181d7`). The engine computes the submodule and its Gram matrix, and the comparisons are module homomorphisms (LV5, LV12).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
