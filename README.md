# Computational leaves of lean-cas-dsl

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a registration: a catalogue operation of
`lean-categories`, an input form, and a backend program that computes the operation's result form.
It contributes no mathematics and ships no Lean. Nothing it says is believed; only its answers are
checked, by `lean-cas-dsl`'s acceptance suite, which this package never sees.

The [constitution](.specify/memory/constitution.md) governs this repository. The unit of work is
the category implementation of the generated interface; a registration is one of its ports
(constitution LV3).

* **`leaves.json`** is the manifest the kernel reads (`CasContract/Registration.lean` of
  `lean-cas-dsl-leaf-contracts`): the backend programs, and for each registration its
  `operation`, `input` form and `backend`, plus optional C6 `preferredRoutes`.
  A preference selects a surviving admitted source route, including an explicit
  identity route `[]`; it asserts no equality. Admission belongs to the kernel.
* **Category interfaces** are generated from the independently accepted declarations.
  The released `cas_port.load_interfaces` SDK exposes complete category signatures,
  object/morphism constructors, operations and immediate functor actions, with
  dependent result and scoped-reference helpers. Supply all selected structures,
  parameters, defining maps, comparisons, callable fields and permitted choices.
  Category constructors are separate. Native datatype metadata supplies no wire codec.
* **`backends/`** holds the programs. Each speaks the contract's port protocol (`cas_port`, put on
  its `PYTHONPATH` by the kernel; constitution LV16 makes the SDK a declared dependency at
  the contract release tag). Providers own their control logic, private engine values and
  private reuse. They are glue over mature engine routines and hand-roll no algorithm that
  an engine supplies (constitution LV5, LV6). They decode the complete prescribed input and
  supply the full result interface, naming the actual engine and routine they invoke.
  Public composition and retained results use
  the released service with its actual ownership and capture checks. Providers contribute
  no mathematical definitions, proofs, semantic authority or acceptance criteria.
  * `sage_backend.py`: Sage, under `CAS_SAGE_PYTHON`;
  * `gap_backend.py`: GAP through Sage's libgap, under `CAS_GAP_PYTHON`;
  * `sage_power_set.py`: `meth.cardinality` on `obj.sets.power_set` by Sage's
    `Subsets(S).cardinality()` (Sage combinatorics), under `CAS_SAGE_PYTHON`;
  * `sage_set_limits.py`: `lim.sets.product`, `colim.sets.coproduct` and `lim.sets.pullback` on
    `cat.sets`, by Sage's `cartesian_product` and `DisjointUnionEnumeratedSets` (Sage
    combinatorics), under `CAS_SAGE_PYTHON`. Factors may be `extent` literals, `constructionApex`
    descriptors or literal lists; a product with an infinite factor answers the
    `objectProduct` apex with connection-local `opaqueData` projections. It also answers
    `meth.cardinality` on `cat.sets` by Sage `cardinality()` of the enumerated carrier, or
    `aleph0` on Sage's countable infinite parents;
  * `sage_symbolic.py`: named maps of `Sets` on `ℂ`, `ℝ`, polynomials, multivariate
    polynomials, monics, positive naturals and finite subsets of vectors (`re`, `im`, `bar`,
    `abs`, `sqrt`, degree, derivative, differential, coefficient change, factors, roots,
    companion matrix, total degree, prime factors, equality, span) and the binders `∫`,
    `lim` and `lim` at infinity, by Sage's symbolic ring, `AA`/`QQbar` and polynomial
    routines, under `CAS_SAGE_PYTHON` with full Sage (`sage.all`).

  The one engine installation is the full SageMath of the research container, through
  its public `sage.all` entrypoint under `/sage/.venv/bin/python3` (constitution LV21).
  The modular passagemath entrypoints that the adapters still try are removed by the
  feature's task list.
  Additional programs implement the published B0 routes:
  `gap_groups.py` uses GAP for symmetric/cyclic groups, selected units,
  subgroup kernels and abelianness; `sage_modules.py` supplies module rank
  and formed-carrier cardinality; `sage_presentations.py` executes the
  published F9 comparison in both directions through native quotient-ring
  homomorphisms. Presentation application retains explicit direction, typed
  descriptor endpoints, native composition, and finite generalized-point data
  at the original domain. Unowned opaque callables and unimplemented selected
  actions fail explicitly. This program needs Sage's PARI dependency; a partial modular
  installation lacking it cannot execute that route.

  The same presentation program now registers the published F9 coefficient
  maps `mor.sets.f9_x_constants` and `mor.sets.f9_y_constants` through native
  quotient-ring coercion maps. It supports their complete finite graphs and
  common pointwise invocation without dropping selected comparison maps.

  `sage_bilinear_lift.py` supplies the four published
  `lift.bilin_module.restrict` fields for finite graph-backed bilinear forms.
  Sage finite maps restrict the actual pairing along the supplied inclusion;
  replies retain nested pairing graphs, actual carrier inventories, and all
  three typed map endpoints. Infinite/foreign-session callables and other
  source presentations remain unsupported. The released contract's
  `api/declared-ports.json` supplies the exact field addresses and public types;
  its `Port.lean` fixes their wire encodings.

  `backends/engine_python.py` still gives both engine variables a default of
  `.venv/bin/python` of the running workspace; LV21 removes that search.
* **`lakefile.toml`** only makes this directory a Lake package; it has no targets. `lean-cas-dsl`
  requires no leaf package: it reads a manifest at run time (`CAS_LEAVES`).

* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`; nothing here
  depends on it, runs it or can reach it. A leaf is never written or changed to make a test pass:
  `lean-cas-dsl`'s harness measures the installed leaves and reports gaps. A leaf's own tests are
  evidence of nothing; they check protocol and data-retention behaviour of a real backend process
  (constitution LV18).
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency of
  the contract, the kernel or `lean-categories`, and name the deficiency in the commit.

Missing mathematics or missing forms go upstream to `lean-categories`; a leaf never absorbs them.
