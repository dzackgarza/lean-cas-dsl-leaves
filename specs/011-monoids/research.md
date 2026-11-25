# Research: Monoids category implementation (`cat.monoids`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Registrations at `obj.sets.units`.** `meth.cardinality` and `prop.is_finite` at `obj.sets.units` move here, not to Sets or Core Sets: the input row `obj.sets.units` has its home in `cat.monoids` (parameter `cat.monoids`), and its lowering is in this module (LV1, one lowering table). Decision of 001 research R15.

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
