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
  "https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts" @ "32e01399fd182b4dc9faf06ae8f7534042a5e1c9"

require lean_categories from git
  "https://github.com/dzackgarza/lean-categories" @ "9ab8693e97ac0c6ec76ac8b4b696ddc3455becd7"

@[default_target]
lean_lib CasLeaves where
  globs := #[.andSubmodules `CasLeaves]
  leanOptions := #[
    ⟨`relaxedAutoImplicit, false⟩,
    ⟨`weak.linter.mathlibStandardSet, true⟩,
    ⟨`weak.linter.style.header, false⟩,
    ⟨`maxSynthPendingDepth, (3 : Nat)⟩]
