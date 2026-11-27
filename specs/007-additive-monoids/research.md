# Research: Additive Monoids category implementation (`cat.additive_monoids`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Sage parents for vectors.** The family engine of the survey is GAP. The additive monoids that the V1 rows build are vectors over the Sage parents that `backends/sets.py` lowers, so the routine is Sage `cartesian_product([M] * n)` of that parent (one lowering table, LV1). Rejected: GAP `FullRowModule`, which needs a second representation of the parent and a conversion between Sage and GAP for each request.

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
