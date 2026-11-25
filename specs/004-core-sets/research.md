# Research: Core Sets category implementation (`cat.core_sets`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Cardinals from the engine.** A finite set gives Sage `cardinality()`, an integer. A set for which Sage gives `cardinality()` $= +\infty$ and which is in `EnumeratedSets()` gives $\aleph_0$. Sums, products and finite powers use the arithmetic of spec 002. A free module of finite rank $n$ over a ring $R$, which Sage does not put in `EnumeratedSets()`, gives $\lvert R \rvert^{n}$, the finite power of spec 002, from Sage `rank()` and `base_ring()`. Any other set that Sage presents as infinite and not as an enumerated set is `unsupported`. Sources: kernel engine survey, "Cardinals" (no surveyed engine has infinite cardinal arithmetic) and "Finite sets, countable sets, enumerated sets" (countability is the membership of `InfiniteEnumeratedSets`); kernel constitution 4.0.1, policy "Established computational implementations"; LV6.

**R2. One lowering table.** The named sets reach this module through the lowering table of `backends/sets.py`. The v1 GAP routines for $\mathbb{Z}/n$ and $(\mathbb{Z}/n)^k$ and the v1 table `COUNTABLE` are deleted; the v1 rule that $\mathbb{Z}/0$ is $\mathbb{Z}$ is Sage's own `Zmod(0)` (LV1).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- |
