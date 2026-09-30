/-
Copyright (c) 2026 Dzack Garza. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
module

public import CasContract.Leaf
public import CasLeaves.Algebra.RingTables
public import CasLeaves.Algebra.RingActions
public import Mathlib.Algebra.Category.Grp.Basic
public meta import CasContract.Leaf
public meta import LeanCategories.Catalogue.Semantics.Algebra.Ports

@[expose] public section

/-!
# Rings whose additive port relabels its elements by `Fin.rev`

A second realization of `cat.rings` (backend `relabeled-rings`): a handle is a ring table, and its
category is induced from `RingCat` by the table's ring. Its two ports to structured sets differ
in how they present the underlying set:

* the multiplicative port (`fun.rings.multiplicative_monoid`) is the table's monoid table, with
  the trivial square, exactly as the Lean-native tables have it;
* the additive port (`fun.rings.additive_group`) is the table's additive-group table followed by
  the relabeling of its elements by `Fin.rev`: the additive-group table whose addition, zero and
  negation are the original ones conjugated by `Fin.rev`. It denotes the same additive group up
  to the additive isomorphism `Fin.rev`, so its square is pasted from the relabeling natural
  isomorphism `relabelingFunctor ⋙ additiveGroupDenotation ≅ additiveGroupDenotation`.

A legitimate, non-identity presentation: the two structural routes from rings to sets present
the ring's underlying set up to `Fin.rev`.
-/

open CategoryTheory
open CasCatalogue.Algebra.Actions CasCatalogue.Algebra.RingTables

namespace CasCatalogue.Algebra.RelabeledRings

/-- A ring handle of the relabeled realization: a ring table. -/
structure RelabeledRing where
  table : RingTable

set_option linter.dupNamespace false in
/-- Relabeled ring handles, with the ring homomorphisms between their denotations
(`InducedCategory`). -/
abbrev RelabeledRings : Type :=
  InducedCategory RingCat.{0} fun b : RelabeledRing => RingCat.of b.table.Carrier

/-- A relabeled ring handle denotes the ring of its table. -/
def relabeledDenotation : RelabeledRings ⥤ LeanCategories.Algebra.Rings.{0} := inducedFunctor _

/-! ### Relabeling additive-group tables by `Fin.rev` -/

/-- The additive-group table whose addition, zero and negation are those of `t` conjugated by
`Fin.rev`. -/
def relabelTable (t : AddGroupTable) : AddGroupTable where
  size := t.size
  add a b := (t.add a.rev b.rev).rev
  zero := t.zero.rev
  neg a := (t.neg a.rev).rev
  add_assoc a b c := by simp only [Fin.rev_rev, t.add_assoc]
  zero_add a := by simp only [Fin.rev_rev, t.zero_add]
  neg_add_cancel a := by simp only [Fin.rev_rev, t.neg_add_cancel]

/-- `Fin.rev`, an additive isomorphism from the relabeled table's group onto the original. -/
def relabelEquiv (t : AddGroupTable) : (relabelTable t).Carrier ≃+ t.Carrier where
  toFun := Fin.rev
  invFun := Fin.rev
  left_inv := Fin.rev_rev
  right_inv := Fin.rev_rev
  map_add' a b := (Fin.rev_rev (t.add a.rev b.rev))

/-- The relabeling isomorphism in `AddGrpCat`. -/
def relabelIso (t : AddGroupTable) :
    AddGrpCat.of (relabelTable t).Carrier ≅ AddGrpCat.of t.Carrier :=
  (relabelEquiv t).toAddGrpIso

/-- Relabeling by `Fin.rev`, on additive-group tables: a morphism is conjugated by the two
relabeling isomorphisms. -/
def relabelingFunctor : AddGroupTables ⥤ AddGroupTables where
  obj := relabelTable
  map {s t} φ := InducedCategory.homMk ((relabelIso s).hom ≫ φ.hom ≫ (relabelIso t).inv)
  map_id t := by ext; simp
  map_comp φ ψ := by ext; simp

/-- Relabeling denotes the same additive group, up to the natural isomorphism `Fin.rev`. -/
def relabelingIso : relabelingFunctor ⋙ additiveGroupDenotation ≅ additiveGroupDenotation :=
  NatIso.ofComponents relabelIso fun {s t} φ => by
    change ((relabelIso s).hom ≫ φ.hom ≫ (relabelIso t).inv) ≫ (relabelIso t).hom =
      (relabelIso s).hom ≫ φ.hom
    simp

/-! ### The two ports -/

/-- The multiplicative port: the table's monoid table, with the trivial square. -/
def relabeledToMonoid :
    RealizedAction (Algebra.Ports.ringsMultiplicative.{0}).toFunctor relabeledDenotation
      monoidDenotation :=
  RealizedAction.induced _ (fun b => b.table.toMonoidTable) fun _ => rfl

/-- The table's additive-group table, the Lean-native additive port on relabeled handles. -/
def relabeledToNativeAdditiveGroup :
    RealizedAction (Algebra.Ports.ringsAdditive.{0}).toFunctor relabeledDenotation
      additiveGroupDenotation :=
  RealizedAction.induced _ (fun b => b.table.toAddGroupTable)
    fun b => ringToAdditiveGroup_obj b.table

/-- The additive port: the native additive port followed by relabeling; its square is the native
(strict) square pasted with the relabeling isomorphism. -/
def relabeledToAdditiveGroup :
    RealizedAction (Algebra.Ports.ringsAdditive.{0}).toFunctor relabeledDenotation
      additiveGroupDenotation where
  action := relabeledToNativeAdditiveGroup.action ⋙ relabelingFunctor
  square := ⟨Functor.associator _ _ _ ≪≫
    Functor.isoWhiskerLeft relabeledToNativeAdditiveGroup.action relabelingIso ≪≫
    relabeledToNativeAdditiveGroup.square.iso⟩

end CasCatalogue.Algebra.RelabeledRings

namespace CasCatalogue

register_leaf
  { backend := "relabeled-rings"
    contributions := [
  .realizer
  { id := ⟨"rz.rings.relabeled"⟩, category := ⟨"cat.rings"⟩, backend := "relabeled-rings"
    denotation := `CasCatalogue.Algebra.RelabeledRings.relabeledDenotation },
  .action
  { id := ⟨"act.rings.multiplicative_monoid.relabeled"⟩
    edge := .functor FunctorId.ringsMultiplicative
    realization := `CasCatalogue.Algebra.RelabeledRings.relabeledToMonoid },
  .action
  { id := ⟨"act.rings.additive_group.relabeled"⟩, edge := .functor FunctorId.ringsAdditive
    realization := `CasCatalogue.Algebra.RelabeledRings.relabeledToAdditiveGroup }] }

end CasCatalogue
