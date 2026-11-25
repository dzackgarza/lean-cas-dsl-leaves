# Research: Rings category implementation (`cat.rings`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. One lowering table for $\mathbb{Z}/n$.** The v1 GAP routines for `meth.cardinality` and `prop.is_finite` at `obj.rings.integers_mod` are replaced by Sage `Zmod(n).cardinality()` and `is_finite()` on the value of this module's lowering table (LV1); Sage `Zmod(0)` is `ZZ`, and the v1 rule for $n = 0$ is deleted.

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
