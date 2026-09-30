/-
Copyright (c) 2026 Dzack Garza. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
module

public import CasLeaves
public import Lean.Util.CollectAxioms

/-!
# Kernel-axiom audit

Elaborating this module checks every declaration defined in a `CasLeaves` module against the
standard Lean axiom budget, after `LeanCategories.Tools.AxiomAudit` in `lean-categories`.
Declarations are selected by defining module, not namespace: this package shares the
`CasCatalogue` namespace with its dependencies. It is a kernel-assumption audit only; it does not
establish that a Lean statement has the intended mathematical meaning.
-/

open Lean Elab Command

namespace CasLeaves.AxiomAudit

/-- The standard Lean axioms. -/
def permitted : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]

run_cmd do
  let env ← getEnv
  let ours (name : Name) : Bool := match env.getModuleIdxFor? name with
    | some idx => (`CasLeaves).isPrefixOf env.header.moduleNames[idx.toNat]!
    | none => false
  let mut violations : Array (Name × Array Name) := #[]
  for (name, _) in env.constants.toList do
    if !ours name then continue
    let unexpected := (← collectAxioms name).filter (!permitted.contains ·)
    if !unexpected.isEmpty then
      violations := violations.push (name, unexpected.qsort Name.lt)
  if !violations.isEmpty then
    throwError m!"nonstandard axiom dependencies: {violations.toList}"

end CasLeaves.AxiomAudit
