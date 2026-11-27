# Research: Rings category implementation (`cat.rings`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. One lowering table for $\mathbb{Z}/n$.** The v1 GAP routines for `meth.cardinality` and `prop.is_finite` at `obj.rings.integers_mod` are replaced by Sage `Zmod(n).cardinality()` and `is_finite()` on the value of this module's lowering table (LV1); Sage `Zmod(0)` is `ZZ`, and the v1 rule for $n = 0$ is deleted.

**R2. The V1 ring operations are the rows of universe 0.** The rows `op.rings.add`, `op.rings.mul`, `op.rings.neg` and `op.rings.pow` of the catalogue at `3f8aedf` are declared for rings of universe 0, and V1 implements them. lean-categories T064 (#211) declares them at every universe for the construction classification of lean-cas-dsl #23 (kernel T146, first consumer T143); no V1 row consumes that change, so it is an input of no V1 task (001 research R17).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
