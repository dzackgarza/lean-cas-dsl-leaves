# Research: Groups category implementation (`cat.groups`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. The unit-group functor.** The actions of `fun.monoids.units` return the complete group result: its carrier, its group operations and the defining inclusion of the units into the monoid, for the later group and map operations (kernel T155). The GAP session of `libgap` in this program supplies `Units` and the group operations; the leaf that hosts `libgap` stays an out-of-process Python program (lean-cas-dsl#3). The functor is not structural, so its home is `cat.groups`, the later of its two ends (001 research R16).

**R2. Integers mod zero.** The v1 rule that $\mathbb{Z}/0$ is the free group of rank $1$ (`gap_groups.py:46` at `8b181d7`) is a datum of the leaf. The lowering of `obj.groups.cyclic` at $n = 0$ is GAP `CyclicGroup(infinity)`, which builds the group of the catalogue row from the request (plan, "Cyclic groups"; LV1).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1), T006 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
