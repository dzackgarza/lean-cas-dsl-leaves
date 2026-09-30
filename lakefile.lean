import Lake
open Lake DSL

/-
Computational leaves of `lean-cas-dsl`: realizations only. A leaf registers, through
`register_leaf`, how presentations of already-formal objects are computed; it contributes no
mathematics (that is `lean-categories`') and never sees the tests it is measured by (those are
`lean-cas-dsl`'s, which depends on this package, not the reverse). It is written against the leaf
contract alone. See `AGENTS.md`.
-/
package «cas_leaves» where
  version := v!"0.1.0"

require cas_leaf_contracts from git
  "https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts" @ "98462f4024f2db39a160ce9a8b84544f26ecde47"

require lean_categories from git
  "https://github.com/dzackgarza/lean-categories" @ "3a84ea38274c683f0c632ccd1c2f0617d5d45fec"

@[default_target]
lean_lib CasLeaves where
  globs := #[.andSubmodules `CasLeaves]
  leanOptions := #[
    ⟨`relaxedAutoImplicit, false⟩,
    ⟨`weak.linter.mathlibStandardSet, true⟩,
    ⟨`weak.linter.style.header, false⟩,
    ⟨`maxSynthPendingDepth, (3 : Nat)⟩]
