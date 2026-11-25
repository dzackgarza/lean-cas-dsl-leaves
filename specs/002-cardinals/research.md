# Research: Cardinals category implementation (`cat.cardinals`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Arithmetic as code, not as a port.** The catalogue declares only `lit.cardinals` on `cat.cardinals`. The sum, product and finite power of cardinals are needed inside the cardinality of constructed sets (products, power sets, spans). They are the known method of LV6 and live in `backends/cardinals.py` as code that `backends/core_sets.py` imports. Source: kernel constitution 4.0.1, policy "Established computational implementations"; engine survey, "Cardinals".

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
