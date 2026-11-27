# Research: Integral Lattices category implementation (`cat.integral_lattice`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. No literal rank.** The v1 rank of $E_8$ is a literal of the leaf (`sage_modules.py:52`, `gap_groups.py:57` at `8b181d7`). The rank and the size come from the Sage lattice that the lowering builds; abelianness is asked of the kernel through the residual actions (LV1, LV8).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
