# Research: Sets category implementation (`cat.sets`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. `lim.sets.product` belongs to Sets.** The projections of a product are the legs of the product cone of `lim.sets.product`, and `cat.sets` owns the operation (LV3).

**R2. Lowering of the number sets.** One lowering table in `backends/sets.py` maps the named sets to Sage parents. The two v1 tables from named sets to parents (`sage_backend.py:36-46`, `sage_power_set.py:38-48`, `sage_set_limits.py:63-68` at `8b181d7`) and the two countability tables (`sage_backend.py:51-52`, `sage_set_limits.py:75-83`) are deleted (LV1). Exact real and complex values replace the 53-bit `RR` and `CC` models.

**R3. Finite sums as deferred programs.** A finite sum or product folds the operation of the selected structure. That operation belongs to a later category implementation (monoids, rings). This module returns a deferred program of those calls, so that the kernel routes each call (LV8; contract FR-009).

**R4. Calculus engines.** SymPy is the primary engine for limits, integrals and series; the Sage symbolic ring (Maxima) receives the same request where SymPy returns an unevaluated form (engine survey, "Calculus"). The v1 interpreter of composites (`sage_symbolic.py:235-293` at `8b181d7`) is replaced by the lowering of the published rows of the binder form of contract T021.

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
