# Computational leaves of lean-cas-dsl

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a registration: a catalogue operation of
`lean-categories`, an input form, and a backend program that computes the operation's result form.
It contributes no mathematics and ships no Lean. Registration is a computational claim checked
against the published contract, not a theorem that the implementation is correct. The kernel uses
declarations and outputs for dispatch and computation; they carry no semantic authority. Independent
`lean-cas-dsl` acceptance checks observed answers against mathematics; this package never sees it.
A well-formed wrong answer remains possible.

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
  not independent mathematical acceptance evidence.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency of
  the contract, the kernel or `lean-categories`, and name the deficiency in the commit.

Missing mathematics and abstract computational obligations belong to `lean-categories`, which may
improve its API without tailoring meaning to a backend. Concrete representations and invocation
belong to the leaf contract; generic interpretation, composition and result lifting belong to the
kernel. Leaves preserve required selected data and implement declared operations. They do not
reproduce generic inheritance or forwarding mechanisms. Complete callable interfaces need not
eagerly enumerate infinite objects or evaluate forms on every pair, and computational structure
is never promoted into a proof of its laws. Available verified Lean computations may be used
within their scope; theoretical Lean implementability does not bar external engines.

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

The `58f753b-7a25454` public lifted-subobject, lifted-apex and
lifted-inclusion inputs now lower through the exact `lift.bilin_module.restrict`
route. Native Sage computes the original transported kernel, restricts the
chosen ambient quadratic module with `submodule(kernel.basis_matrix().rows())`,
and constructs its actual inclusion with the restricted basis and `hom`.
The complete source receiver must match the retained transported action; changed
scalar/value roles or lift routes are rejected. The selected apex retains its
complete descriptor, chosen restricted form, separate scalar/value descriptors
and value module. Native cardinality and vector `inner_product` routines execute
on that restricted module. The root adapter can lower its apex and the exact
fixed-W carrier under the existing full module-underlying route. General
noncanonical presentations remain unsupported, including supplied comparisons
for which no native model exists; they are not silently discarded. Actual
outgoing apex/inclusion and pairing application request fixtures are needed
before adding their dispatch registrations or point-wire parsers. These observations are native engineering execution findings only.

The actual public `fixed-w-lifted-cardinality-request` dispatches through the
existing `meth.cardinality` / `fun.modules.underlying` registration. Its full
forward route additionally retains `fun.subobjects_bilin_module.domain(R,W)`;
the native decoder checks both roles against the chosen lifted apex before
retaining that complete structural descriptor. The exact manifest-selected
backend and request have executed through the released contract's framed
`cas_port.py` protocol, and its structural reply envelope decodes. No
mathematical output expectation was used. `just test-ci` and `git diff --check`
also pass. Pairing/point and further operation request fixtures remain pending.

The released `11da81d-7a25454` public `fixed-w-pairing-request.json`
(SHA256 `817d923d144e2379f243ff31019edc5864b9b732a105234c5b3375407e5260c5`)
provides the complete `mor.sets.bilin_module_pairing(R,W,L)` request. Its
public declaration returns a Sets morphism from the product of two selected
carrier sets to the chosen value module. It does not supply two points or ask
for a pairing value. The chosen integer ring, its regular module through the
full ring functor action, and the full formed E8 receiver are retained.
Native Sage lowering of that receiver and `inner_product_matrix()` execute;
the native value parent is the integer ring and the resulting matrix has
shape 8 by 8. No expected mathematical result was consulted.

This request exposes a result-representation gap for a computational leaf.
The released Port permits a function graph when its domain has an independently
synthesized finite enumeration, and permits a registered named morphism
encoding. This request's carrier is infinite. Returning its original named
morphism descriptor would defer reconstruction of the already formal pairing
to the kernel rather than transmit an engine-computed function. No released
representation for a computed infinite pairing function, or actual pairing
application request with its two typed points, is provided. An engine matrix
is not the declared Sets morphism result. No matrix, guessed point envelope,
new operation, or echo-only registration has been introduced.

The exact input was sent through the released framed port to the existing
native Sage module backend: it announced Sage 10.8.12, returned the existing
`unsupported` response for this unregistered operation, and exited cleanly.
This is an engineering gap observation, not successful realization or result
decode. `just test-ci` passes. Completing pairing evaluation needs an actual
public point/application request or a public computed-function result encoding;
the existing mathematical signature does not require enumerating its infinite domain. A callable
representation and its invocation belong to the contract and generic kernel machinery. Completing
that interface requires its owner to provide the representation and execution path, not a new
mathematical operation, a proof of backend correctness or one workaround per leaf.

The separate public `ring-view-product-request.json` (SHA256
`a8dc4cabf5be590674e434020be4378c895eb83145bcb0141c8556f42147d79d`)
now executes through the existing `lim.sets.product` / `cat.sets` registration.
Finite input lowering retains each complete `functorAction`, its exact supported
forget edge, and its selected source, down to `obj.rings.integers_mod(3)`.
Sage `Zmod` supplies the selected ring parent and `cartesian_product` supplies
product enumeration. The product path retains those structured native input
nodes while encoding the existing cone and its projection graphs. No new
registration or inferred semantic route is introduced. Unsupported classifier
arguments reject. A native inspection retains all four actual action nodes and
the full selected ring descriptor.

The exact public request was dispatched through the released framed port under
Sage 10.8.12 and returned `ok`; its cone, finite apex and both complete graph
shapes decoded structurally. No expected mathematical answer was provided or
used. `just test-ci` and `git diff --check` pass. These are engineering execution
checks only; the infinite pairing result-representation gap above remains open.

The `sage-polynomials` adapter uses the released common `apply` point-invocation
contract and retains native Sage values on their supplying live connection. The
registered polynomial factorization returns the engine-computed unit and repeated
factors; subsequent unit, factors and product operations consume that same data.
Polynomial roots, degree, coefficient change, companion matrices and matrix
characteristic polynomial, determinant and trace use Sage routines. Coefficient
change currently lowers actual identity maps and the released integer-coefficient
map; other selected maps remain computational gaps rather than endpoint casts.

Python compilation, manifest JSON, and a framed same-process engineering probe
cover construction, factorization, product/unit reuse, roots, companion and
characteristic polynomial, with clean process exit. These are engineering checks,
not independent mathematical acceptance evidence. The actual kernel-produced
factor request (SHA256 `c04c75c5cd5dca50262b4a292ee49dffbbe3d4c923150559bdb619020d5eb95c`)
now executes through the framed adapter and returns a computational packet with
clean process exit. Its complete admission and selected power-expression context
needed no adapter framing change. This establishes caller/protocol integration,
not mathematical acceptance. Unsupported inline coefficient data, general selected maps and
other point representations are reported as computational gaps. Opaque factor
collections remain native data; their further use requires an existing admitted
operation, and tokens never create new mathematical interfaces.

Matrix determinant and trace at published integer or positive-modulus residue
endpoints return portable `valueData` numerals instead of session-local tokens.
Other scalar representations await their actual published caller encoding; the
adapter does not invent rational serialization. The subsequently published truth-observation
contract permits a JSON Boolean as computational data, never a proposition proof.

The polynomial adapter also consumes the published `admittedPoint` context by
lowering its actual original data at the retained original endpoint. Published
`operationExpression` ring addition, multiplication, negation and power lower to
Sage native operators at supported full selected named-ring parameters. No
structural action or coefficient map is inferred from a carrier. Unknown selected
actions remain unsupported pending the actual kernel input-only packet.

The existing `mor.sets.equality` address consumes the published complete pair
record at its explicit selected type and produces the contract's computational
Boolean observation. A scalar Boolean is supported only for the published
singleton/terminal generalized domains; other truth-valued points require further
published pointwise or callable support. Native expression/parser and framing
checks do not establish mathematical acceptance. The actual input-only factorization/product/degree/equality packet now
executes in order on one live connection. Degree data lower to native Sage
naturals or minus infinity, and the selected `incl.sets.naturals_degrees` route
retains its preceding natural identity maps. Other maps are unsupported, rather
than erased or inferred from their endpoints. The equality reply is checked only
for its published computational Boolean shape, not against an expected answer.
Polynomial-application packets remain pending; polynomial application is not
registered using a guessed algebra or coefficient map.
