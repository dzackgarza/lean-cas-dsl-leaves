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
  "https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts" @ "6588a86ca5d0ade8ffdabf5f7f95640d426d18f4"

require lean_categories from git
  "https://github.com/dzackgarza/lean-categories" @ "c06aeedc8ebc16c787481a5c15a86526341a4b4e"

@[default_target]
lean_lib CasLeaves where
  globs := #[.andSubmodules `CasLeaves]
  leanOptions := #[
    ⟨`relaxedAutoImplicit, false⟩,
    ⟨`weak.linter.mathlibStandardSet, true⟩,
    ⟨`weak.linter.style.header, false⟩,
    ⟨`maxSynthPendingDepth, (3 : Nat)⟩]
