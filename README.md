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
    `CAS_SAGE_PYTHON`. Finite residue-power inputs use Sage's `FreeModule`. The primitive
    `mor.sets.fin_rev` uses Sage `Permutations(n).first().reverse()` and returns
    its graph on the selected zero-based Fin carrier.
  * `sage_root_lattices.py`: rank, cardinality and finiteness on the released named
    `A(n)`, `A_dual(n)` and `E8` forms, by Sage's `RootSystem(...).root_lattice()` or
    `.weight_lattice()` and its parent methods,
    under `CAS_SAGE_PYTHON`. The Module-underlying image preserves the complete
    registered fibre inclusion and carrier actions and computes quotient carrier
    cardinality through the same native Sage quotient model.
  * `sage_module_kernels.py`: `fun.arrows_modules.kernel` on selected root-A
    Module carrier actions and zero, identity or mapped named inclusion arrows,
    by Sage's `FreeModule.hom(...).kernel()` and `basis_matrix()`. The complete
    subobject uses the released canonical apex and inclusion projections at the
    original action. The consumer performs the prescribed formed-structure lift.
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

The released `b76ec3d` mathematical interface and updated port provide selected F9
comparison arrows, generator-relative element data, instantiated carrier-forget edges,
and canonical BilWForm cokernel apex/legs. The field adapter evaluates presentation
transport with Sage homomorphisms; the lattice adapter constructs the integer module
quotient with Sage's quotient routine. The set adapter evaluates selected F9 constants,
generators and transported arrows through the documented carrier-forget route.
Generic constructor-mapped arrows require a native model of the actual constructor;
they are rejected rather than erased. Generic Prop-valued subgroup parameters still
require a supplied carrier encoding. Local protocol probes are engineering checks and
provide no mathematical acceptance evidence.

An author source read accidentally included theorem bodies beyond the authorized FiniteGroups
constructor definitions. This was reported; those bodies were not used as computational
expectations. Later extraction was restricted to the authorized input-model definitions.

Released-interface engineering coverage:

Input source: `released-interface-feb09e0-b1525e5`, mathematics revision
`feb09e0f4d13ad40850b6bc9e5213c5dee85d1c7`, contract revision
`b1525e5fae0ad28ec4cf95ef9cdbba7c9124c082`.
The snapshot identifies a source-assessed candidate with protected admission pending.
This note describes computational translation gaps only. It supplies no mathematical
acceptance evidence, status, certificate, or proof for any computation.

The public `module-underlying-cardinality` input can be decoded by the current
root-lattice adapter. Its complete fibre inclusion, carrier action, canonical
cokernel diagram and zero-arrow endpoints are retained. Native Sage quotient and
cardinality routines execute in the modular engine environment. Native
`FreeModule.hom(...).kernel().basis_matrix()` also executes there.

The metadata-generated `fixed-w-view`, `fixed-w-object` and `fixed-w-carrier`
inputs now have a native model in `sage_fixed_forms.py`. The chosen E8 form is
negative in its released simple-root coordinates. Sage matrix multiplication and
`FreeQuadraticModule` construct that exact form; the complete object, scalar and
value descriptors remain distinct retained fields. The registered integral-lattice
view returns the complete structural action. Changing the selected value-module
descriptor is rejected. These input decoding and native execution checks are
engineering observations only. Other fixed-value structures remain unsupported.

Required trusted public input fixtures, without expected answers:

- A defining arrow at its exact endpoints, including any retained subobject or
  construction inclusion needed by subsequent computation.
- A chosen coefficient arrow and a chosen presentation arrow with complete
  parameters and endpoints. In particular, `fun.bilin_module.change_value` has
  explicit parameters `(R, W, W', f)`; the map `f` cannot be discarded.
- A complete `pointView` with its source element and generalized-point domain.
- A complete `operationPoint` with its actual presentation comparison, original
  domain and selected target.
- A complete `createdCone` inside a `constructionLeg`, including the original
  source diagram, returned target cone, realized source apex and typed leg index.

The contract documents these envelopes but the released public-wire directory
now additionally provides the three selected fixed-W E8 inputs described above. Unsupported descriptors remain computational gaps; no carrier-based
reconstruction or guessed envelope is introduced.

The subsequent released `feb09e0-4b93ebb` public `fixed-w-kernel-request`
provides the actual `meth.kernel` request at `cat.arrows_modules_r`. The native
module adapter retains its Arrow constructor action, complete selected fixed-W
endpoints, scalar and value arguments, and actual mapped arrow. Supported
identity and zero arrow data is evaluated through Sage module homomorphisms;
other original arrow data is explicitly unsupported. Sage computes the kernel
and its defining basis. The complete returned subobject uses the canonical
apex/inclusion projections of the original transported request, with its exact
mapped ambient object. Subsequent native lowering of those projections computes
the same kernel and defining inclusion through Sage's basis and hom routines.
No alternative apex or presentation identification is chosen; optional
presentation maps are not fabricated. General returned/lifted subobjects with
noncanonical presentations still require actual public lowering input data.
The public request and subsequent projection lowering execute in the native
engine; changed scalar/value arguments and unsupported arrow data reject.
`just test-ci` checks the manifest JSON and Python compilation. These checks
provide engineering execution findings only.
