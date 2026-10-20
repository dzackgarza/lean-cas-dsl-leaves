# Leaf-contract and upstream defects

These findings concern published input forms and engine wiring. No leaf result is correctness evidence.

## Published input review, 2026-10-20

The published contract reviewed is `lean-cas-dsl-leaf-contracts` main
`3c2159b510db2ca63455530ed0f4c28ba27da2f8`; the published catalogue is
`lean-categories` main `a2123729df092e58b6fb0cd39c78db5e1714faf2`.
They were obtained from each repository's main reference. These revisions identify
this review; subsequent builds consume the latest main.

## Discriminant cokernel

The catalogue publishes `obj.bil_wform.root_lattice_a`,
`obj.bil_wform.root_lattice_a_dual`, `mor.bil_wform.root_lattice_a_to_dual`,
`obj.bil_wform.root_lattice_a_discriminant`, and
`mor.bil_wform.root_lattice_a_to_discriminant`, all parameterized by `n : ℕ`
(`LeanCategories/Catalogue/Semantics/Modules/Bilinear/Valued/Lattices.lean`).
The projection's source is the dual lattice. The registered operation
`colim.bil_w_form.cokernel` consumes `parallelPair` with the inclusion and the
zero arrow at the same endpoints. `CasContract/Port.lean` specifies a cocone
reply containing the apex and projection.

The existing Sage adapter supplies these published object and arrow descriptors.
For cardinality it builds the upstream negative root Gram matrix and calls
Sage's `Matrix.elementary_divisors()`. The previous report that named output
forms were missing is obsolete at the reviewed catalogue main. No missing
published input was identified for these existing registrations.

## Fin reversal

`mor.sets.fin_rev` is a published named morphism on `Fin n`. The existing adapter
uses Sage's `Permutation` and emits its graph as a list of pairs, including the
empty graph at `n = 0`. The contract permits this named-morphism form.

## Finite diagrams of sets

The existing registrations are `lim.sets.product`, `colim.sets.coproduct`, and
`lim.sets.pullback` on `cat.sets`. `CasContract/Port.lean` specifies their
`pair` and `cospan` inputs and complete cone/cocone outputs. The adapter calls
Sage's `cartesian_product` and `DisjointUnionEnumeratedSets` and emits finite
graphs. It supports finite primitive carriers and retained input envelopes.
The catalogue publishes `cat.finite_sets`, `obj.finite_sets.fin`,
`graph.finite_sets`, and `lift.finite_sets.pullbacks`; no duplicate registration
of a set limit under the finite-sets category is introduced here.

## Engine entrypoint repaired

The available full Sage runtime reports version `11.0.beta1` and imports
`sage.all`. It lacks the `sage.all__sagemath_modules`,
`sage.all__sagemath_combinat`, and `sage.all__sagemath_gap` entrypoints used by
the existing adapters. This prevented them from announcing the port protocol
before any request could run. Commit `85564f3` uses the public `sage.all`
entrypoint throughout. The loader then retained the previously documented
modular passagemath entrypoints as well: it imports the supported modular
entrypoint when installed, or full Sage's `sage.all` when that entrypoint is
absent. A missing dependency inside an installed entrypoint propagates as an
error. This changes engine loading only. The existing modular Sage interpreter subsequently supplied by the launcher,
`/home/dzack/gitclones/lean-cas-dsl/.venv/bin/python`, was used strictly as an
engine, without inspecting that checkout. All six manifest programs also
completed the same ten independently selected framed requests with both engine
variables set to that interpreter. This exercises both supported engine layouts.

At source revision `f4c0f86`, all six manifest programs were launched by host
`python3`, with `CAS_SAGE_PYTHON` and `CAS_GAP_PYTHON` both set to
`/home/dzack/.local/bin/sage-docker-python` and `PYTHONPATH` set to the
published contract's `python` directory. Ten length-framed requests completed:
Sage cardinality, GAP cardinality, power-set cardinality, set product,
set coproduct, set pullback, discriminant cocone, discriminant cardinality,
and Fin reversal at nonempty and empty input. The check required clean
process exit, a ready frame, matching request ids, and an `ok` response for
each request. It did not compare answers against a mathematical oracle or
exercise kernel decoding. Commit hooks also checked manifest JSON and Python
compilation. These are engine/protocol observations only.

## Source provenance and separation

Published leaf main initially resolved to
`48a99b5bcb2b090e1c778db29f006b612bed02ed`; the clean local main already included
five unpublished commits `def3657`, `06288c0`, `886879d`, `037f1e7`, and
`d522046`. Their git author metadata alone does not establish independent
original authorship. Their existing source was preserved and reviewed against
the published contract, catalogue, and actual engine, without claiming a new
original-author provenance.

The prior version of this defect file included downstream acceptance-specific
requirements, kernel source references, and harness observations. Those are
outside a leaf author's permitted inputs and have been removed from the active
leaf requirements and findings. This review did not inspect the acceptance
suite, kernel source, or harness reports. It establishes engineering observations
only; it does not establish mathematical correctness or B0 acceptance.


## Approved realization inventory, 2026-10-20

The launcher supplied these existing B0 capability requirements without
assertions or expected answers: set/group cardinality and finiteness with
finite constructions; finite reversal and composition; formed-module
discriminants with defining maps; module rank through structural forms;
group-map kernels with complete subgroup data; abelianness; formed-module
cardinality; and nonidentity finite-field presentation transport.

The ordinary manifest now has nine programs and 90 registrations. These
counts describe supplied routes, not correctness or acceptance.

| Assigned capability | Supplied engineering route |
| --- | --- |
| Set/group cardinality and finiteness | Existing primitive sets, residue powers and finite power sets; finite-set ordinals; symmetric/cyclic groups; alternating and kernel subgroups; named F9 presentations; units of selected integer/residue multiplicative monoids. Sage parent routines and GAP `Size`, `IsFinite`, `Units` supply the computations. |
| Finite constructions | Existing finite `pair` product/coproduct and graph `cospan` pullback adapters return full cone/cocone data. Retained finite carrier data can be consumed by the primitive cardinality adapters. |
| Reversal and composition | `sage_fin_rev.py` supports the published graph request and common point invocation. Native permutations execute retained compositions, including pointwise finite-domain graphs. |
| Discriminant construction and reuse | The published root-A inclusion/zero pair returns the named formed quotient and its dual-to-quotient projection. Sage Smith invariants supply cardinality; native GAP abelian groups supply the inherited group-property route. |
| Module rank | `sage_modules.py` registers `meth.rank` for regular/vector modules, root-A lattices and their duals/discriminants, and E8. Native free-module rank and quotient-vector-space dimension consume the selected forms. |
| Group-map kernels | `gap_groups.py` lowers sign, identity, trivial, finite full-graph maps and named-map compositions. GAP `Kernel` supplies the subgroup. Finite replies contain the actual engine-enumerated inclusion graph, the original ambient descriptor, and the published kernel-domain descriptor. Infinite named-map cases retain the published defining inclusion descriptor. |
| Abelianness | GAP `IsAbelian` on the registered symmetric/cyclic/subgroup, selected-units and formed-carrier forms; no leaf claim becomes a formal property. |
| Formed-module cardinality | Sage free-module cardinality and the published root Gram matrix's Smith invariants on root-A, dual, discriminant and E8 forms. |
| Nonidentity finite-field transport | `sage_presentations.py` registers `cmp.f9.translation` on both published F9 presentations, in either direction. Sage quotient-ring homomorphisms execute the selected generator translation and return an element at the exact requested target descriptor. |

At committed source `a990f7d`, all nine manifest programs completed 27
independently selected real-engine requests. The check required process exit,
ready framing, matching request ids, successful reply framing, and that every
registration's operation was advertised by its program. Eight programs used
modular Sage 10.8.13/GAP 4.16.1; the presentation program used full Sage
11.0.beta1. Additional units, finite defining-map and named-composition checks
exercised the subsequent source changes. No result was compared with an
acceptance assertion, and no decoder or mathematical acceptance result is
claimed.

## Remaining boundaries and exact missing inputs

* A composition of two unlabelled group graphs carries no intermediate chosen
  group in the published `compose` envelope. A carrier graph does not determine
  that group structure. Named constituents retain their declared endpoints and
  can be composed; the wholly unlabelled case requires the intermediate
  structured endpoint from the contract owner. The leaf does not infer it.
* `obj.groups.units` and `obj.sets.units` are parameterized by an arbitrary
  chosen monoid. The current lowering supports selected integer/residue-ring
  multiplicative monoids. GAP 4.16.1 has no `Units` method on the native groups
  tried, and no bound `GroupOfUnits` operation in the available installation.
  Such other monoid realizations remain unimplemented; the mathematical form
  already exists. This is an engine/lowering limit, not missing mathematics.
* The generic `cmp.polynomial_quotient.translation` row is not registered here.
  The named F9 comparison is implemented. Arbitrary coefficient-ring and
  defining-polynomial computational presentations have not been lowered by
  this adapter; this is an unimplemented generic route, not a claim that the
  published mathematical comparison is absent.
* The F9 common `apply` branch supports closed singleton-domain points. A
  general non-singleton point needs its pointwise/callable data consumed and
  returned at the original domain; that branch is not implemented. The adapter
  rejects it rather than returning one scalar for a function.
* Modular Sage in the supplied interpreter lacks `sage.libs.pari`; the native
  F9 constructor/hom path reports that missing dependency. Full Docker Sage
  supplies it. For integrated execution, use
  `CAS_SAGE_PYTHON=/home/dzack/.local/bin/sage-docker-python`; GAP can retain
  `CAS_GAP_PYTHON=/home/dzack/gitclones/lean-cas-dsl/.venv/bin/python`.

The kernel owner judges registration admission, returned-form decoding and
all permanent mathematical assertions independently. This leaf inventory
neither declares B0 complete nor substitutes engine checks for that judgment.


## Resumed leaf input-boundary defect

The resumed launcher assignment restricted inputs to released leaf contract
`c603ede9e51adaa3a1365d2d82aeebb3aa0f6d13`, existing native-engine APIs,
and this leaf role's source. I incorrectly treated the standing repository
permission to consume the mathematical catalogue as permission to expand that
narrower assignment, and read upstream catalogue source in the resumed turn.
This was a conduct defect, not an unavailable operation or an owner decision.

Content reads were in `lean-categories`:

* `LeanCategories/Catalogue/Semantics/Modules/Bilinear/Valued/Kernels.lean`,
  lines 38–260;
* `LeanCategories/Catalogue/Semantics/Modules/Bilinear/Valued/Constructions.lean`,
  lines 30–150 and 175–257;
* `LeanCategories/Catalogue/Semantics/Modules/Bilinear/Valued/Alternating.lean`,
  lines 60–100;
* `LeanCategories/Catalogue/Semantics/Modules/Bilinear/Valued/Transport.lean`,
  lines 80–108.

Searches also scanned `LeanCategories/Catalogue/Semantics/Limits/Lifts.lean`
and the glob `LeanCategories/Catalogue/Semantics/Modules/Bilinear/Valued/*.lean`.
Matching source output included `Lattices.lean` and
`CatalogueRegistration.lean` in that directory, in addition to the files above.
An attempted `Literals.lean` read found no file. Upstream git revision and main
reference queries were also made. No upstream repository was edited. No kernel
source, mathematical acceptance assertions, expected answers or downstream
diagnostics were read.

The launcher instructed this author to checkpoint only the released-contract
finite-data helpers and stop. Commit `4f33cee` adds those helpers in `wire.py`,
with independent Python framing checks and the normal manifest/compilation
hook. No new lift source or lift registration was written in this resumed
turn. Existing adapter migration to `finiteData`/`finiteGraph`, prescribed lift
field registration/execution, complete actual component-output retention and
native-engine checks of those paths remain undone. This checkpoint completes
none of those obligations. The remaining work is assigned to a fresh leaf-only
context without the upstream-derived material.


## Contract-only continuation: bilinear pairing data schema missing

The leaf-only continuation consumes released leaf contract main
`1770b6b0fa0e26aee361b6d57f9fd2967e03836a`, this repository's existing source,
and native-engine APIs. It does not consume catalogue source, kernel source,
acceptance assertions, expected answers, or downstream diagnostics.

The released `api/declared-ports.json` resolves the earlier missing-address
finding: `lift.bilin_module.restrict` publishes all four computation fields,
registered on `lift.bilin_module.restrict#input`, with the selected
`fun.bilin_module.forget` action. The `lift.finite_sets.pullbacks` row has no
computation or ports; it is not registered by the leaf.

One concrete data-schema input remains missing. The published
`obj.bilin_module.bilinear_form` constructor takes a
`CasCatalogue.Modules.Bilinear.Valued.Constructions.bilinearMaps R M M W`
argument. That declaration's exported result is only `Type u`; its underlying
computational data fields are not in the exported `datatypes` inventory. The
published `bilinearInclusion` and `admitBilinear` signatures describe conversion
to and admission from a callable, but do not publish the argument's constructor
data encoding. A callable signature alone does not determine that encoding.
The missing input is the public data schema of this alias under the existing
port's proof-erasure and record-field rules. No constructor layout is guessed.
Finite native graph restriction can be developed with the published callable
protocol; publishing its computed object parameter waits on this exact schema.
No upstream implementation is consulted to fill the gap.

The finite-data adapter migration was exercised with 18 independently selected
length-framed native requests across all nine manifest programs, using Sage
`11.0.beta1` and GAP `4.15.1` in the existing Docker engine. Requests covered
structured supplied inventories, cardinality/finiteness consumers, power sets,
finite reversal, set product/coproduct/pullback, a sign-map kernel, and a typed
finite cyclic-group graph kernel. Checks required successful native process
exit, ready/reply framing and matching request ids. Returned set constructions
and group kernels additionally had their actual inventories and defining graph
key coverage inspected. Inline framing checks rejected missing/repeated keys
and an image outside a supplied codomain inventory. These are engineering
observations only; no acceptance suite, expected mathematical answers or kernel
decoder was consulted, and the missing lift implementation remains open.
