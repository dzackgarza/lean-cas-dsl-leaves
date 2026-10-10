# Leaf-contract and upstream defects

These are requests for the owning formalization or kernel, not permissions for leaves to invent semantics. No leaf result is correctness evidence.

## Discriminant cokernel

The formal mathematics includes `BilWFormCat.cokernelIsColimit` in `LeanCategories/Modules/Bilinear/Valued/Cokernel.lean` and discriminant objects in `LeanCategories/Lattices/Valued/Discriminant.lean`. This does **not** by itself provide a wire-decodable, registered presentation of an arbitrary integral lattice specified by its Gram matrix, nor a named input form for the formed-module arrow `L → L♯`. Until a released input form for that arrow and a result form for its cokernel are identified, registering `colim.bil_w_form.cokernel` on ad hoc JSON Gram matrices would invent a leaf-side presentation. Upstream owner: `lean-categories` for missing forms/constructors; kernel owner for decoding of already registered forms.

## Fin reversal

`mor.sets.fin_rev` **is** a released named-morphism row, declared by `CasCatalogue.Foundation.Morphisms.finRev` in `LeanCategories/Catalogue/Semantics/Foundation/Morphisms.lean`, with parameter `n : ℕ` and type `Fin n ⟶ Fin n`. It is not an external computation: its declaration is `TypeCat.ofHom Fin.rev`, and composing it twice is entirely a Lean computation. Per `AGENTS.md` evidence-model item 6, it must be discharged in `lean-categories` or by the generic kernel, not implemented by a leaf. The morphism row is not an independently backend-registered operation on an input form. Upstream owner: kernel for generic composition/Lean computation.

## Finite diagrams of sets

`leaves.json` already registers `lim.sets.product`, `colim.sets.coproduct` and `lim.sets.pullback` on `cat.sets`, with `sage_set_limits.py` emitting `cone`/`cocone` envelopes. These rows are explicitly present in `LeanCategories/Catalogue/Semantics/Limits/Registration.lean` and the `pair`/`cospan` input envelopes are declared in `CasContract/Port.lean`. `CasCatalogue.Foundation.Morphisms.ofGraph`, registered as `graph.sets`, **does** support raw list-of-pairs graph morphisms, subject to complete-domain and no-duplicate proofs checked by the decoder. Thus lack of a graph form is *not* the reason to reject this leaf. The remaining specific rejection requires inspecting the kernel diagnostic for the exact constructed diagram and its attempted cone; without this diagnostic, changing the leaf's encoding would be speculative. The source claims that the existing Sage product input form was rejected, but the published contract itself requires exactly the current `pair` representation. Upstream owner: kernel if its released decoder rejects a genuinely valid descriptor, otherwise this leaf's precise mismatching field.

For the finite-sets restatements, the pinned `lean-categories` already registers `cat.finite_sets`, `obj.finite_sets.fin`, `graph.finite_sets`, and the creation lift `lift.finite_sets.pullbacks` (`Semantics/Limits/Lifts.lean`, `Semantics/Foundation/FiniteObjects.lean`). Thus the expected route is **the registered creation lift from the `cat.sets` pullback**, not a duplicate `lim.sets.pullback` registration under `cat.finite_sets`. The unresolved issue is whether the kernel actually routes a valid `cat.sets` computational cone through that lift. Upstream owner for creation dispatch failures: kernel, not leaves.

## Pending admission evidence

No new registration is claimed conforming until the exact released catalogue rows, input forms and output decoding are checked. The existing manifest entries remain unchanged; do not count them as new coverage.
