# Research: Bilinear Forms category implementation (`cat.bil_wform`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Lowering of the root lattices.** One lowering table maps `obj.bil_wform.root_lattice_a` at $n$ to Sage's root lattice of type $A_n$ with the sign of the catalogue row; its dual and discriminant are Sage `dual_lattice()` and `discriminant_group()`. The three literal Gram matrices of $A_n$ (`sage_discriminant.py:33`, `sage_modules.py:60-61`, `gap_groups.py:61-62` at `8b181d7`) and the literal ranks (`sage_modules.py:50-52`, `gap_groups.py:55-57`) are deleted (LV1).

**R2. The cokernel is computed, not named.** The v1 cokernel answers two catalogue names (`sage_discriminant.py:49-50`). The cocone reply carries the engine's quotient and projection of the selected pair (LV4, LV12).

**R3. Abelianness of a form.** `prop.is_abelian` and `prop.is_commutative` at a form are inherited methods through the module and its additive group. The implementation asks the kernel for the residual actions and for the property of the image group (LV8, third option), in place of the v1 GAP `AbelianGroup` built from a literal rank.

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V1), T005 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
