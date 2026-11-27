# Research: Commutative Rings category implementation (`cat.commutative_rings`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. F9 presentations from the request.** The defining polynomials $t^2 + 1$ and $t^2 + t + 2$ over $\mathbb{F}_3$ and the generator shift of the comparison are literals of the v1 source (`sage_presentations.py:75`, `:147` at `8b181d7`). They are data that no engine constructor builds. The implementation reads them from the unfolded definition that the request carries (K:C22); a request that carries only the names is `unsupported` and a finding against the contract (LV1; CONTRIBUTING MTH001).

**R2. Coefficients over $\mathbb{R}$ and $\mathbb{C}$.** Coefficients in $\mathbb{R}$ and $\mathbb{C}$ are exact values of `AA` and `QQbar`, read from and written to the forms of contract T021 (`sage_symbolic.py:89-92` at `8b181d7` is the v1 reading).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1), T018 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
