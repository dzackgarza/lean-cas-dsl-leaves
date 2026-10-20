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
