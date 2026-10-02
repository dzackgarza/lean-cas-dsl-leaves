# Remaining released-interface dependencies

The current implementation consumes the public mathematical interface at
`57c85852de8127b9d229878061bfb26c47998814` and port contract at
`e485ad225290cec760da23ee3875c29c07fbddb3`. The complete fixed B0 leaf assignment
remains open. These are engineering interface dependencies; this document is
neither mathematical evidence nor an acceptance result.

- **Selected field transport:** the selected moduli and translation are public
  input data, and their Sage models and homomorphisms execute. The contract needs
  to specify how the hom/inv of a registered presentation comparison occurs as
  an arrow inside `compose`/`map`, and the point encoding for the chosen quotient
  presentations. Named coefficient embeddings already execute in finite
  pullbacks; this does not complete transported-diagram execution.
- **Lattice discriminants:** the registered cokernel consumes
  `parallelPair(f, zero)`. The released catalogue has the named A-family
  `to_dual` arrow, but no named zero arrow on its infinite carriers. It also
  supplies no named/literal finite BilWForm quotient apex. Sage module quotient
  routines are available; their result, defining projection and presentation
  maps need declared result and point forms before they can cross the port.
- **Generic subgroup parameters:** `obj.subgroups.subgroup(G,H)` has a
  Prop-valued carrier in `H : Subgroup G`. Its encoding is not described by the
  finite-function graph rule. Named alternating and kernel subgroup forms are
  implemented without inventing an encoding of that carrier.

Finite group-kernel cones use the released `parallelPair` and presentation
envelopes, with actual GAP isomorphisms to available named cyclic/source group
forms. They emit the defining inclusion and both comparison maps. Kernel-side
validation and independent mathematical acceptance remain outside this package.

An author source read accidentally included theorem bodies after the authorized
FiniteGroups constructor definitions. This was reported to the coordinator;
the existing group implementation preceded that read, and those bodies were
not used as computational expectations. Subsequent input-source extraction was
restricted to explicitly authorized constructor/presentation definitions.
