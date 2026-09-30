/-
Copyright (c) 2026 Dzack Garza. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
module

public import CasContract.Leaf
public import LeanCategories.Catalogue.Semantics.Foundation.Objects
public import LeanCategories.Catalogue.Semantics.Algebra.NamedRings
public import LeanCategories.Catalogue.Semantics.Limits.Registration
public import CasLeaves.Foundation.Cardinality
public meta import CasContract.Leaf
public meta import LeanCategories.Catalogue.Semantics.Foundation.Objects
public meta import LeanCategories.Catalogue.Semantics.Limits.Registration

@[expose] public section

/-!
# Presented named sets and their products

The named sets of `lean-categories` (`obj.sets.fin`, `obj.sets.integers_mod`,
`obj.sets.integers_mod_power`) are presented by the handles `.finite n`, `.zmod n` and
`.zmodPow n k`, `obj.sets.integers` by `.zmod 0` (`ZMod 0` is `ℤ`), and `obj.sets.naturals`,
`obj.sets.rationals` by `.naturals`, `.rationals`, whose denotations are those sets exactly
(`Iso.refl`). The registered product
`lim.sets.product` of two presented sets is presented by `.prod a b`, whose denotation is the
product exactly; its projections and mediators are the core's.
-/

open CategoryTheory Limits
open CasCatalogue.Foundation.Actions

namespace CasCatalogue.Foundation.PresentedObjects

def presentFin (n : ℕ) :
    Σ a : SetHandles, setDenotation.obj a ≅ Foundation.Objects.fin n :=
  ⟨.finite n, by exact Iso.refl _⟩

def presentIntegersMod (n : ℕ) :
    Σ a : SetHandles, setDenotation.obj a ≅ Foundation.Objects.integersMod n :=
  ⟨.zmod n, by exact Iso.refl _⟩

def presentIntegers :
    Σ a : SetHandles, setDenotation.obj a ≅ Foundation.Objects.integers :=
  ⟨.zmod 0, by exact Iso.refl _⟩

def presentNaturals :
    Σ a : SetHandles, setDenotation.obj a ≅ Foundation.Objects.naturals :=
  ⟨.naturals, by exact Iso.refl _⟩

def presentRationals :
    Σ a : SetHandles, setDenotation.obj a ≅ Algebra.NamedRings.rationals :=
  ⟨.rationals, by exact Iso.refl _⟩

def presentIntegersModPower (n k : ℕ) :
    Σ a : SetHandles, setDenotation.obj a ≅ Foundation.Objects.integersModPower n k :=
  ⟨.zmodPow n k, by exact Iso.refl _⟩

/-- The apex of the product of two presented sets. -/
def presentProduct (a b : SetHandle) :
    Σ c : SetHandles, setDenotation.obj c ≅
      (Limits.Registration.setsProduct a.carrier b.carrier).cone.pt :=
  ⟨.prod a b, by exact Iso.refl _⟩

end CasCatalogue.Foundation.PresentedObjects

namespace CasCatalogue

register_leaf
  { backend := "lean"
    contributions := [
  .presentation
  { id := ⟨"pres.sets.fin"⟩, object := ⟨"obj.sets.fin"⟩, realizer := ⟨"rz.sets.presented"⟩
    presentation := `CasCatalogue.Foundation.PresentedObjects.presentFin },
  .presentation
  { id := ⟨"pres.sets.integers_mod"⟩, object := ⟨"obj.sets.integers_mod"⟩
    realizer := ⟨"rz.sets.presented"⟩
    presentation := `CasCatalogue.Foundation.PresentedObjects.presentIntegersMod },
  .presentation
  { id := ⟨"pres.sets.integers"⟩, object := ⟨"obj.sets.integers"⟩
    realizer := ⟨"rz.sets.presented"⟩
    presentation := `CasCatalogue.Foundation.PresentedObjects.presentIntegers },
  .presentation
  { id := ⟨"pres.sets.naturals"⟩, object := ⟨"obj.sets.naturals"⟩
    realizer := ⟨"rz.sets.presented"⟩
    presentation := `CasCatalogue.Foundation.PresentedObjects.presentNaturals },
  .presentation
  { id := ⟨"pres.sets.rationals"⟩, object := ⟨"obj.sets.rationals"⟩
    realizer := ⟨"rz.sets.presented"⟩
    presentation := `CasCatalogue.Foundation.PresentedObjects.presentRationals },
  .presentation
  { id := ⟨"pres.sets.integers_mod_power"⟩, object := ⟨"obj.sets.integers_mod_power"⟩
    realizer := ⟨"rz.sets.presented"⟩
    presentation := `CasCatalogue.Foundation.PresentedObjects.presentIntegersModPower },
  .limitRealization
  { id := ⟨"limr.sets.product.presented"⟩, limit := ⟨"lim.sets.product"⟩
    realizer := ⟨"rz.sets.presented"⟩
    realization := `CasCatalogue.Foundation.PresentedObjects.presentProduct }] }

end CasCatalogue
