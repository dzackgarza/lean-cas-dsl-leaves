# Computational leaves of lean-cas-dsl

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a registration: a catalogue operation of
`lean-categories`, an input form, and a backend program that computes the operation's result form.
It contributes no mathematics and ships no Lean. Nothing it says is believed; only its answers are
checked, by `lean-cas-dsl`'s acceptance suite, which this package never sees.

* **`leaves.json`** is the manifest the kernel reads (`CasContract/Registration.lean` of
  `lean-cas-dsl-leaf-contracts`): the backend programs, and for each registration exactly its
  `operation`, `input` form and `backend`. Which registrations are admitted is the kernel's
  decision, against the catalogue.
* **`backends/`** holds the programs. Each speaks the contract's port protocol (`cas_port`, put on
  its `PYTHONPATH` by the kernel) and is glue over an existing engine: it decodes the kernel's
  encoding of the input, calls the engine's routine, and encodes the engine's answer in the result
  form. Each names the engine and routine it calls.
  * `sage_backend.py`: Sage (passagemath), under `CAS_SAGE_PYTHON`;
  * `gap_backend.py`: GAP through Sage's libgap (passagemath-gap), under `CAS_GAP_PYTHON`;
    residue-domain operations and released named group/subgroup properties use GAP's
    domain, homomorphism and kernel routines. Finite group-kernel cones include the
    defining inclusion and both maps from GAP's computed isomorphism to an available
    named group presentation.
  * `sage_power_set.py`: `meth.cardinality` on `obj.sets.power_set` by Sage's
    `Subsets(S).cardinality()` (passagemath-combinat), under `CAS_SAGE_PYTHON`;
  * `sage_set_limits.py`: `lim.sets.product`, `colim.sets.coproduct` and `lim.sets.pullback` on
    `cat.sets`, finite diagrams only, by Sage's `cartesian_product` and
    `DisjointUnionEnumeratedSets` and `ConditionSet` (passagemath-combinat), under
    `CAS_SAGE_PYTHON`. Finite residue-power inputs use Sage's `FreeModule`.
  * `sage_root_lattices.py`: rank, cardinality and finiteness on the released named
    `A(n)`, `A_dual(n)` and `E8` forms, by Sage's `RootSystem(...).root_lattice()` or
    `.weight_lattice()` and its parent methods,
    under `CAS_SAGE_PYTHON`.
  * `sage_field_presentations.py`: cardinality and finiteness of the released named
    polynomial quotient presentations, by Sage `GF` with each selected modulus.

  Both default to `.venv/bin/python` of the running workspace (`backends/engine_python.py`).

The modular passagemath environment uses version `10.8.12`. Root-system matrix routines
also require `passagemath-graphs==10.8.12`; finite extension fields require
`passagemath-pari==10.8.12` (with `conway-polynomials==0.10`). These are engine
dependencies, installed in the ignored `.venv`, rather than declarations of mathematical
operations. Engine initialization must import the matching `sage.all__sagemath_*`
module before importing low-level extension modules such as `sage.libs.gap.libgap`.
* **`lakefile.toml`** only makes this directory a Lake package; it has no targets. `lean-cas-dsl`
  requires no leaf package: it reads a manifest at run time (`CAS_LEAVES`).

* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`; nothing here
  depends on it, runs it or can reach it. A leaf is never written or changed to make a test pass:
  `lean-cas-dsl`'s harness measures the installed leaves and reports gaps. A leaf's own tests are
  evidence of nothing.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency of
  the contract, the kernel or `lean-categories`, and name the deficiency in the commit.

Missing mathematics or missing forms go upstream to `lean-categories`; a leaf never absorbs them.

At the released `57c858` mathematical interface and `e485ad2` port contract, the remaining
required interfaces are the presentation-comparison hom/inv arrow encoding and quotient-field
point encoding for selected F9 transport; a zero arrow on infinite BilWForm carriers and a
finite BilWForm quotient apex/point form for discriminants; and the Prop-valued carrier encoding
for generic `Subgroup` parameters. Named F9 coefficient maps and named alternating/kernel
subgroup inputs already have engine translations. These dependencies leave the complete B0
assignment open; local engineering probes provide no mathematical acceptance evidence.

An author source read accidentally included theorem bodies beyond the authorized FiniteGroups
constructor definitions. This was reported; those bodies were not used as computational
expectations. Later extraction was restricted to the authorized input-model definitions.
