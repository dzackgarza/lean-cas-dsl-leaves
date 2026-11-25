# Research: Additive Monoids category implementation (`cat.additive_monoids`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Survey choice for vectors.** The family engine is GAP. The additive monoids that the V1 rows build are vectors over Sage parents that `cat.sets` lowers; the survey record of T001 confirms Sage `cartesian_product` or replaces it with GAP `FullRowModule`.

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
