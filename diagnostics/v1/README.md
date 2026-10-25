# V1 computational composition specimen

This directory is an independently authored, deliberately small Sage/passagemath
backend. It is a separate leaf package: use **this directory's `leaves.json`**.
It does not change or extend the repository's main manifest.

The specimen computes with native Sage rings, selected finite-field presentations,
matrices, polynomials and Cartesian products. Its nineteen registrations exercise
repeated use of returned data, actual presentation maps, and callable fields in a
complete structured result. The implementation contains no
Lean, mathematical declarations, denotations, certificates or acceptance tests.
Registration and successful execution are computational claims, not correctness
evidence. The independent kernel and its permanent assertions remain responsible
for mathematical acceptance.

## Public inputs and provenance

The public contract inputs were:

- `README.md` and `CasContract/Port.lean`;
- `python/cas_port.py`;
- `api/README.md`, `api/declared-ports.json`, `api/wire-examples.md`, and
  `api/manifest.md`.

The selected F9 extension additionally used the independently owned mathematical
definitions and public registrations in these two upstream files, read with
`git show` at published main revision
`ee957329414a58759d26e23fa22e8d0a31040fc8`:

- `LeanCategories/Algebra/Concrete/PolynomialPresentation.lean`;
- `LeanCategories/Catalogue/Semantics/Algebra/PolynomialPresentations.lean`.

Those sources supply the selected defining polynomials and the actual comparison
map. Their mathematical declarations and proof procedures are not implemented,
copied or replaced by this leaf.

Outside the supplied `diagnostics/v1` specimen, no old leaf source, kernel
source, acceptance suite, expected-answer file, other agent's engineering probe,
or other agent's implementation was consulted.
Sage's installed public API documentation was used for its native computational
objects and methods. The engine exercised locally was passagemath 10.8.13.

The declaration snapshot read during authoring records mathematics revision
`805208138f016368f6a4eac415f25f3922a5807d` and protocol revision
`1770b6b0fa0e26aee361b6d57f9fd2967e03836a`. The separately evolving public Port
and wire documentation supplied the new V1 envelopes. These are provenance
observations, not runtime dependency pins or a claim that the snapshot includes
every subsequently published metadata field.

The public Python helper read during authoring had SHA-256
`9193274cbb9a1878ab4294c998be513290703f95fbf59fdc513e6130a6ad3d34`.
The helper is loaded directly from an explicitly configured public contract
checkout; it is neither copied into this leaf nor obtained from kernel internals.
Normal subsequent use loads the host's selected helper, without enforcing this
historical digest.

### Predecessor public-data completion provenance

The predecessor completion used public contract revision
`63e074c82c433bf30c79d41d8ef69947b3af8ee4`, including its existing API snapshot,
wire examples and reference helper. The helper digest at completion was
`3c130a548c4c644a26f827bba37a3bee09993f905d75f7d118d047ed3ad8f618`.
Only declaration headers and the application-field registration in
`LeanCategories/Catalogue/Semantics/Algebra/Polynomials.lean` were inspected at
current mathematics revision `5e3ffca6377b7293616df802af50c01b79ef3e44`.
No operational definition body or proof was read in that completion. The
supplied specimen's selected F9 parameters above remain unchanged.

The current polynomial application field is `evaluation(R, A : Under R)`, whereas
the separately named `ownEvaluation(R)` has one parameter. Both operations have
ordinary separate registrations here. The application implementation consumes the
actual selected target ring and coefficient map; it does not alias the field to
one-parameter evaluation. The public snapshot's earlier revision metadata above
is retained as provenance and is not relabelled as current mathematics.

### Consumer follow-through provenance

The additive consumer follow-through read only the public contract documentation,
`CasContract/Port.lean`, reference Python helper and API export at
`63e074c82c433bf30c79d41d8ef69947b3af8ee4`, the required repository authority
files, and this predecessor specimen at
`fae4c1090f081eff5e7042d85a1b5f541625cf33`. It inspected no kernel source,
question files, acceptance assertions, runtime outcome reports or additional
mathematical implementation. The nineteen registrations and every other leaf
remain unchanged. All additions below consume already published data forms.

### Complete cone consumer provenance

The complete product/pullback consumer repair used the fresh public declaration
snapshot at contract revision `ba8b91a70561c3e0888c66de30f0e6b2907c01e5`, whose
`api/declared-ports.json` SHA-256 is
`f3a17fd1d2fa98d72513fbe9ac333834f64b6b160a9ccd5206b97a5991802b19`.
It also used the public creation-diagram clarification in `api/wire-examples.md`
at the frozen contract revision `6780f9f0e0ac9acb7355d9281993df44f0d13b54`.
The earlier snapshot omitted the complete pullback constructor metadata; its
field order was not inferred. The refreshed export supplies `BinaryFan.mk`,
`PullbackCone.mk`, `diagramIsoPair`, `diagramIsoCospan`, and the declared index
types. Only those public interfaces and this existing diagnostic were used.

The previous product-only consumer gate made the pullback-creation branch
unreachable for its declared operation. The current decoder handles the two
published constructors separately and consumes their actual returned fields.
The finite-set pullback creation row is no longer accepted as a product creation
row. This repairs a computational consumer; it adds no pullback construction
registration or mathematical evidence.

### Public-contract conformance completion, 2026-10-25

This bounded completion starts from the published leaf revision
`51e0e6ebd25a2f2a88097ae3081a3c34970cc29d` and uses public contract revision
`90d7d3f1833cff39b77024dcee2dc43213e623ad`. Its additional declaration input is
the separately supplied public export with SHA-256
`43392ae1c6636276519113d07c4cdc3ce8f8eeead1b4336db574c57269216079` and its
public producer provenance. The producer metadata identifies mathematics
`82d1370de372a00a86391b74fc2566c9547dfcb6` and kernel producer
`da6af543a8e71e9400f5438ee40a4e395af2f299`; neither implementation was read.

Only this existing specimen, its repository instructions and engineering
material, the public contract and supplied interface export, and the installed
Sage runtime were used. No mathematical questions, expected answers, acceptance
records, kernel implementation, downstream execution reports or other agent's
work were inspected. The selected F9 constructor and comparison parameters
remain exactly those already present in the specimen. All nineteen registration
pairs and every manifest remain unchanged; the extension specimen is unchanged.

The repairs concern common public data translation: a missing result envelope
on compact presentation replies; whole-callable versus global-point framing;
actual returned native values and callables; complete endpoint fields and
parameter arrays; recursively retained owners; coefficient carrier endpoints;
and object/map projections from complete supplied records. They add no engine
algorithm, mathematical declaration, proof, certificate or acceptance signal.

## Launch

Set the public contract checkout and the real Sage-capable interpreter in the
host environment before loading this directory's manifest:

```bash
export CAS_LEAF_CONTRACT_PATH=/absolute/path/to/lean-cas-dsl-leaf-contracts
export CAS_SAGE_PYTHON=/absolute/path/to/sage-capable/python
```

The manifest starts `python3 sage_backend.py` with this directory as its working
directory. The program re-executes the configured `CAS_SAGE_PYTHON` when needed.
Alternatively, start it directly with the engine interpreter:

```bash
/absolute/path/to/sage-capable/python sage_backend.py \
  --contract /absolute/path/to/lean-cas-dsl-leaf-contracts
```

An explicit `--contract` overrides the environment selector. A missing public
contract path prevents startup. The contract's `PYTHONPATH` injection is not used
to discover a different helper implicitly. `DOT_SAGE`, when configured, is
respected; otherwise the backend allocates a writable temporary Sage cache.
Standard output contains length-prefixed protocol frames only. Clean input EOF
ends the process and destroys its native-value store.

## Registrations and native computations

The morphism, presentation and matrix-application registrations use their own published
complete-request addresses as `input` forms. The four element operations use
`cat.rings`, retaining the actual selected ring in their complete requests.
The product construction uses `cat.sets`. The manifest has no overlapping rows,
priority field or hidden routing instruction. The category registrations do not
claim that every object in those categories has an engine adapter here; the
supported computational parent scope is stated below.

| Published operation | Complete ordered parameters | Native computation | Reply data |
| --- | --- | --- | --- |
| `mor.sets.matrix_rows` | `[n, K]` | Sage matrix construction over `K` from the complete nested callable | Owned matrix |
| `obj.sets.matrices#application` | `[n, K]` | Native matrix/vector multiplication | Complete vector graph |
| `mor.sets.matrix_charpoly` | `[n, K]` | `matrix.charpoly("x")` | Owned polynomial |
| `mor.sets.polynomial_derivative` | `[K]` | `polynomial.derivative()` | Owned polynomial |
| `mor.sets.polynomial_degree` | `[K]` | Native zero observation and `polynomial.degree()` | Public `none`/`some(n)` data |
| `mor.sets.polynomial_own_evaluation` | `[K]` | Native polynomial application in `K` | Exact coefficient data or an owned native value |
| `obj.sets.polynomials#application` | `[R, A]`, with the complete selected `Under R` data | `polynomial.map_coefficients(actual_map, new_base_ring=target)` followed by native evaluation | Exact target coefficient data or an owned native value |
| `op.rings.add` | `[R]` | Addition of native elements in selected `R` | Exact scalar data or owned polynomial/F9 value |
| `op.rings.mul` | `[R]` | Multiplication of native elements in selected `R` | Exact scalar data or owned polynomial/F9 value |
| `op.rings.pow` | `[R, exponent]` | Native nonnegative power | Exact scalar data or owned polynomial/F9 value |
| `op.rings.neg` | `[R]` | Native additive inverse | Exact scalar data or owned polynomial/F9 value |
| `mor.sets.equality` | `[X]` | Equality observation on supplied native computational values | JSON boolean |
| `mor.sets.divide` | `[M]` | Native division for the original admitted denominator, or native multiplication by the inverse field of a complete supplied Units record, in the selected parent | Exact scalar data or an owned native value |
| `mor.sets.f9_x_constants` | `[]` | Native coefficient-field embedding into the selected first presentation | Owned F9 value |
| `mor.sets.f9_y_constants` | `[]` | Native coefficient-field embedding into the selected second presentation | Owned F9 value |
| `cmp.f9.translation` | `[]`, with direction in the retained presentation arrow | Native homomorphism with the independently published generator image | Owned F9 value under `apply`; `valueData(element(exact_target,...))` under `presentationApply` |
| `mor.sets.tuple_empty` | `[X]` | Sage's empty Cartesian-product element | Empty complete graph |
| `mor.sets.tuple_cons` | `[X, n]` | Native Cartesian-product tuple construction from the supplied head and tail | Complete graph, recursively retaining its component data |
| `lim.sets.product` | Diagram `pair(X,Y)` | Sage `cartesian_product` and its two native `cartesian_projection` maps | Complete cone with both `typedMap` legs |

Here `K` is the complete selected commutative-ring descriptor and `R` is the
complete selected ring descriptor. Dimensions and exponents are retained in
their declared parameter positions. No operation is added for a private helper,
native class, returned token or construction projection.

### Selected F9 presentations

The upstream mathematical sources cited above fix the following construction
parameters. The adapter passes these to existing Sage constructors and maps:

| Published selection | Native configuration from the upstream definition |
| --- | --- |
| `obj.sets.f9_x` / `obj.commutative_rings.f9_x` | `GF(9)` with the specified modulus `t^2 + 1` over `GF(3)` |
| `obj.sets.f9_y` / `obj.commutative_rings.f9_y` | `GF(9)` with the specified modulus `t^2 + t + 2` over `GF(3)` |
| Forward `cmp.f9.translation` | `first.hom([second.gen() + 2], second)` |
| Inverse `cmp.f9.translation` | `second.hom([first.gen() - 2], first)` |

These are independently selected presentation data, not answers deduced from
tests or an arbitrary engine-selected isomorphism. The two native parents remain
distinct. An explicit retained comparison is required when moving a native value
between them; native coercion is not used to invent that map. Named generators,
coefficient maps, arithmetic, and equality consume those selected parents.
The adapter neither serializes nor treats native homomorphism construction as a
mathematical certificate.

### Useful compositions

The implementation supports the following independently chosen computational
workflows without a separate registration for each workflow:

1. Construct a matrix from row graphs, apply it to a vector, and apply the same
   retained matrix to the returned vector again.
2. Compute a matrix's characteristic polynomial, differentiate the retained
   polynomial repeatedly, and evaluate or observe the degree of a returned
   polynomial.
3. Construct polynomial arithmetic using the public generator and operation
   expression forms, then use the same polynomial derivative/evaluation ports.
4. Construct an infinite or finite product, retain the complete cone, and consume
   a returned projection inside a `compose`/`point` argument of a subsequent
   registered computation such as equality.
5. Apply a registered ring operation pointwise to a complete generalized point
   with a non-singleton finite domain, preserving that domain's inventory.
6. Compute through the selected F9 comparison, continue field arithmetic on the
   returned opaque value, and consume the actual inverse or a retained mapped
   comparison in a later computation on the same live connection.
7. Build vectors and rows with the declared empty/cons maps, transfer their
   portable graph data to another connection, and continue matrix computations.

These are workflows to exercise the interface. This document supplies no
expected mathematical outputs for them.

## Exact supported wire scope

### Invocation and ownership

Point operations use the public seven-field `apply` envelope. Its operation id
must match the outer dispatch id. Supported named and composed point data are
decoded as their actual actions. An outer arrow containing supported retained
`compose`, `map` and presentation actions is executed in its supplied order;
the adapter does not discard those actions and call only the final operation.
Unsupported descriptors return `unsupported` under the unchanged dispatch id.

The F9 comparison additionally accepts the public five-field `presentationApply`
packet. That interface returns `valueData(element(...))` at exactly the requested target,
serializing Sage's native polynomial representative with existing arithmetic
constructors. Common `apply` replies keep native F9 results opaque, supporting
successive use without reconstruction as formal mathematical values.

Inline replies use `valueData`. Matrices, polynomials, F9 values and projection callables
use `opaqueData` where listed above. Tokens have a random connection prefix and
refer only to live native values in that process. The local store retains the
supplied target descriptor and generalized domain; projection entries additionally
retain the complete source descriptor and actual native source parent. Every
callable entry retains both complete endpoints, including a deferred native
callable returned by a whole-map request. It contains no reconstructed formal term.
A token from another connection is unsupported, including after a restart. Owners
are checked throughout all supplied fields before dispatch, even a retained field
which the selected native routine will not read. Tokens
do not choose their owner or add a registration.

The current published global-point source `obj.sets.fin(1)` accepts ordinary
point data. Other `obj.sets.fin(n)` domains accept complete callable graphs or
supported retained symbolic/owned callables. Finite generalized input can retain
`typedMap`, `compose`, `map` and `mediator` actions; a closed scalar point cannot
stand for a nonconstant map.
The public `obj.finite_sets.fin(n)` descriptor and its selected finite-set forget
action are also supported. Positive-modulus scalar parents use Sage's own finite
iteration; `Zmod(0)` is not given a finite inventory. Binary products of supported
finite parents use Sage's Cartesian-product iteration, including a returned
`constructionApex` retained through a supported `createdCone` and structural
view. An infinite factor is not enumerated to manufacture a finite domain.
`finiteData(descriptor, inventory)` domains accept graphs at exactly that actual
inventory, including a singleton inventory or an inventory around a returned
apex. Generalized finite replies are
`valueData(finiteGraph(inventory, graph))`; graph values may themselves retain
owned data. A whole-callable request uses the supplied identity at the exact
original domain. When no finite inventory is available, supported symbolic or
owned inputs retain an owned native callable which invokes the same existing
engine routines when later applied. This covers supported infinite generalized
domains without enumeration. An endpoint descriptor alone supplies no inventory,
even when its declared endpoint is finite or it is carried through a supported
structural action. Such a request remains callable data unless actual
`finiteData` is supplied. The registered global-point domain keeps the existing
scalar convention, including an actual supplied identity comparison; a different
singleton inventory retains its full graph.

Both endpoints in supplied `typedMap` and owned callable data are checked before
native work is deferred. Compositions retain the intermediate endpoint context;
mediators pass each selected target to its actual component. Full parameter
counts are checked, and a directly selected named callable must retain the same
parameters as its request, including the exponent or dimension. Result encoding
uses the actual final target of a supplied composition. These are computational
framing checks; they do not re-elaborate formal types or prove that a selected
operation or structural action applies.

### Objects and values

Supported named scalar parents are the public integers, rationals and
integers-modulo objects in Sets, Rings and Commutative Rings, together with
`obj.sets.naturals` and `obj.semirings.naturals`. The adapter uses Sage `ZZ`,
`QQ`, `Zmod` and `NN` selected from those full descriptors. The selected
F9 parents described above are also supported for field arithmetic, equality,
generators, coefficients and the registered comparison. The adapter also handles
the public naturals, finite sets, bottom-valued polynomial degrees, truth
observations, univariate polynomial objects, matrix objects, vector objects and
binary `objectProduct` descriptors composed from supported parents.
The supported structural actions are the published Sets identity,
`fun.semirings.forget`, the zero-parameter classifier-forget edge for
`clf.sets.finite`, and the carrier-preserving route already used for the selected
rings and F9 presentations: `fun.commutative_rings.ring`,
`fun.rings.multiplicative_monoid`, `fun.monoids.semigroup`, and the zero-parameter
classifier-forget edges for `clf.magmas.associative` and
`clf.sets.binary_operation`. Their mapped arrows retain and execute the actual
underlying comparison, named map or complete finite graph. A mapped unlabelled
graph needs the original endpoints supplied in its matching `functorAction`
context. An unknown action is not erased when lowering a point view, a retained
element, or a mapped callable; incompatible supplied actions are rejected.
Other structural actions remain unsupported and are not inferred from a native
carrier.

| Public representation | Support |
| --- | --- |
| Integer and modular point | JSON integer, lowered into the independently selected native parent; a positive-modulus residue is already in its canonical nonnegative range |
| Rational record | Two integer data fields `[numerator, denominator]`; the denominator is positive and the record is already reduced; output uses Sage's normalized exact record |
| Polynomial degree | `none()` and `some(n)` lower to Sage's minus infinity and nonnegative integers; returned degree data can be consumed again by equality |
| Vector | Complete graph, supported symbolic callable or same-session owned callable on `Fin(n)`; coordinate scalars retain their declared forms |
| Matrix | Complete nested finite callable data, including typed and same-session owned row callables; graph key order is immaterial |
| `finiteGraph` | Explicit inventory plus complete graph; duplicate, missing and foreign keys are rejected |
| `element` | Complete selected object plus supported arithmetic expression or actual retained computational data, including nested ownership |
| Arithmetic expressions | `numeral`, polynomial or selected F9 `generator`, `add`, `mul`, `neg`, the four ring `operationExpression` forms, and selected semiring addition, multiplication and power expressions |
| `point` | Complete retained point arrow using the supported descriptors below |
| `pointView` | Consume its original complete element data; retain nested ownership |
| `admittedPoint` | Consume the original data at its supplied original target; an admitted unit retains its exact selected monoid and original native value, including nested ownership; supply no admission evidence |
| `constrainedPoint` | Consume the actual original data at its original type, retaining the supplied constructor name, original generalized domain and selected target; the native parent conversion supplies no predicate evidence |
| Complete `Units` record | Its two non-proof fields `[value,inverse]`, each in the selected monoid's declared point form; neither inverse equation is checked or asserted |
| Returned `valueData`/`opaqueData` | Reusable as later point input on the applicable connection |
| Complete polynomial record | The exposed one-field wrappers retain the two `Finsupp` data slots: finite support and the full coefficient callable on `Nat`; proofs are absent |
| `typedMap` | Its actual source, target and complete graph, supported symbolic map or same-session owned callable |
| `morphismEndpoint` | Object data at a supported actual callable's source or target; all callable parameters and owners remain retained, and this descriptor is neither callable nor an inventory |

The ordinary inline vector result contains a complete graph of exact scalar
coordinates. Empty/cons results recursively retain complete vector component
graphs, with locally owned data for any component that has no supported inline
output codec. Polynomial arithmetic and derivatives remain native rather than
using a private sparse-polynomial wire encoding. Matrix and polynomial computations use only the supported selected native
coefficient parents; this is not a registration expansion to every public
coefficient object. Real/complex analytic values, unrelated arbitrary functions,
factorization, subobject lifts and other presentation comparisons remain outside
this specimen.

Portable row/vector graphs and scalar records contain no opaque token and can be
consumed on another connection. Public polynomial arithmetic expressions are
also portable inputs. Matrix creation, characteristic-polynomial and derivative
results retain their existing owned representations; their tokens are not made
portable or revived in another process. A complete matrix-to-polynomial-to-value
chain therefore retains the owning connection until it produces inline data.

### Structured results and retained arrows

A product reply has this complete shape, with actual endpoint descriptors:

```text
valueData(cone(objectProduct(X,Y),
               typedMap(objectProduct(X,Y), X, opaqueData(left-token)),
               typedMap(objectProduct(X,Y), Y, opaqueData(right-token))))
```

This notation abbreviates the ordinary public JSON constructor envelopes.
Both callables are Sage's native projection objects. The backend does not
enumerate an infinite product or implement a substitute projection algorithm.
The cone's apex and both map endpoints are retained exactly in the reply.

Supported retained arrow data are `compose`, `mediator`, a supported named
operation with its parameters, a complete `typedMap` with a locally owned
callable, `arrowHom` of a complete `arrow` receiver, the published polynomial and
F9 generators, the named empty-tuple point, and the polynomial
`objectField(...,"constants",...)` map. The published units-inclusion field
consumes the supplied unit's value field in its exact selected monoid. An
admitted unit retains its original computational value; a complete `Units`
record retains both supplied non-proof fields. Division on the latter uses the
supplied inverse field in native multiplication. The adapter neither replaces
that field with an inferred inverse nor treats the record as membership evidence.
An admitted denominator uses native division in the selected monoid parent;
engine failure is a computational failure and supplies no membership conclusion. The selected `presentation` arrow and
`map` actions along the route listed above are supported. An identity retains
its exact endpoint fields and forwards the already decoded native value,
including complete native records; it does not reconstruct or replace a Units
operand. The declared
`incl.sets.naturals_integers`, `incl.sets.integers_rationals`,
`incl.sets.naturals_degrees` and parameterized `incl.sets.fin_integers_mod(n)`
arrows use native inclusions and coercions when supplied inside these
expressions. Selected `op.semirings.add`, `op.semirings.mul` and
`op.semirings.pow` are also consumed as retained arrows or arithmetic
expressions over the supported natural semiring. They add no standalone
registration here.

`constructionApex` and `constructionLeg` consume the complete supplied cones of
both `lim.sets.product` and `lim.sets.pullback`. Their published data constructors
expose the same three non-proof slots, with different diagram and index types:

| Selected construction | Complete diagram | Complete returned data | Stored leg indices |
| --- | --- | --- | --- |
| `lim.sets.product` / `BinaryFan.mk` | `pair(X,Y)` | `cone(apex,left,right)` | `left()` and `right()` in `WalkingPair` |
| `lim.sets.pullback` / `PullbackCone.mk` | `cospan(f,g)` | `cone(apex,fst,snd)` | `some(left())` and `some(right())` in `Option WalkingPair` |

The one-field `Discrete` wrapper of the product index follows the ordinary
record codec. Pullback commutation is a proof field and is absent from the
packet. The pullback center index `none()` has no separately supplied defining
map in these slots; this specimen leaves that projection unsupported rather
than choosing a composite or asserting that the two composites agree.

A leg consumer uses the actual supplied apex and callable. Plain graphs,
explicit `finiteGraph` data, and mixed typed/untyped legs are supported when
their selected parents and callables have adapters. For a product graph leg,
the complete `pair` object supplies its target. For a pullback graph leg, the
source endpoint of the corresponding retained cospan arrow supplies its target.

The common `constructionField` interface reads the same actual complete packet:
data-port index zero is its object field, and one and two are its stored maps.
These natural-number port indices are distinct from `constructionLeg`'s typed
shape indices. The object readers also consume `subobjectApex`, and map readers
consume `subobjectInclusion` or `arrowHom` from complete Arrow records, including
an `objectPresentation` wrapper. Actual endpoint and map fields remain attached;
an optional retained source presentation is neither executed nor asserted to be
an identification by reading these fields.

The endpoint reader handles `typedMap`, complete `arrowHom` receivers, explicit
identity arrows, supported `map` actions, compositions retaining their endpoint
context, and the four scalar inclusions already supported above. Explicit
common cospan targets and intermediate composition endpoints must agree as
complete descriptors. A graph's outputs do not determine any missing object.

A supplied `typedMap` leg must use the actual returned apex as its source and
must preserve the complete target selected by an ordinary diagram when that
context is present. It can itself retain an otherwise absent target descriptor,
including when the cospan's arrows are bare graphs. The consumer never compares
native carrier equality to choose a map, substitutes a canonical `limitLeg`,
or recomputes a supplied pullback or projection.

For `createdCone(L,D,C)`, the outer `constructionApex`/`constructionLeg` retains
exactly the source diagram `D`. The target limit id still names the registered
operation that produced `C`. The supported lift is
`lift.finite_sets.pullbacks`, only with `lim.sets.pullback`; its selected action
is `classifierForget("clf.sets.finite",[])`. A plain graph in `C` uses the actual
returned apex inventory and the target prescribed by this action on the source
cospan. A typed target leg retains its actual complete computational endpoints;
the consumer does not manufacture a preferred spelling for a target object or
recover a named source apex from it. Complete `valueData` wrappers are unboxed
without replacing their stored fields.

Each nested creation packet is read using its own retained lift and source
diagram. An unknown lift or interpreted action remains unsupported. The
finite-set forget action may surround a retained apex or leg, and `finiteData`
may supply the actual apex inventory. An existing native Sage product can use
that supplied pullback apex as either factor, and its native projection can be
composed with the original supplied pullback leg on the same connection.
Neither packet decoding nor native execution establishes that a creation lift
applies, that an inventory is a mathematical carrier, that a cone commutes, or
that an apex is universal. Those remain independent formal questions.

There is no generic HomSet application address in the public surface used here.
A construction leg therefore has no invented standalone operation id and is
not dispatched under `lim.sets.product` as an application. It is consumed inside
a later supported declared operation's point/composition input. Named input
graphs and arbitrary native callables are not a universal function evaluator.

### Complete polynomial inputs and selected algebra application

The published constructor snapshot exposes a polynomial through
`Polynomial.ofFinsupp`, `AddMonoidAlgebra.ofCoeff`, and `Finsupp.mk`. The first two
have one data slot each, so the existing record codec exposes
`[support, coefficientCallable]`. The leaf passes the supplied support indices
and the results of that supplied callable to Sage's polynomial constructor.
A complete coefficient callable can be typed, symbolic or owned; a graph only
on the finite support is rejected because its domain is the natural numbers.
When a typed or owned coefficient callable retains its actual carrier endpoint,
that endpoint is used for application. It is not replaced by the structured
coefficient-ring object. Sage's selected polynomial constructor consumes the
native coefficient values. Matrix row and column callables make the same
distinction between their actual coefficient carrier and the selected matrix
ring parameter, retaining typed endpoints and native returned components.
There is no private sparse-polynomial wire tag and no implicit zero-extension
of a supplied graph. Native polynomials and public arithmetic expressions remain
ordinary supported alternatives.

For the separately published `obj.sets.polynomials#application`, the parameters
are `[R, A]`, including the actual selected `A : Under R`. The published type
alias exposes `Under R` as a `Comma` record. Its three data fields are the left
`Discrete PUnit` value, the right target commutative ring, and the actual
coefficient map from `R`. Under the existing record codec, the supported complete
representation is `[[], targetRing, coefficientMap]`: `PUnit` has no data fields,
and `Discrete` has one. A `typedMap` coefficient field retains exactly `R` and
`targetRing` as its complete endpoints. This is the published record codec, not
a new algebra tag.

The native routine is `map_coefficients` followed by polynomial application in
the target parent. A selected nonidentity F9 presentation map is consumed as
that actual map. A complete finite coefficient graph at a supported finite
scalar parent is lowered through Sage `Family` lookup; typed and composed
maps retain their supplied endpoints and actual action. This also applies when
the source and target native carriers are the same. The adapter never chooses
a coefficient homomorphism or an identity map from endpoint similarity.
A missing, unsupported or incomplete map is not filled in. A finite table is
computational data and does not establish any homomorphism law. Named algebra descriptors whose actual right object and
coefficient map are not supplied by a supported public representation return
`unsupported`; the adapter does not infer their defining fields from a name.
The one-parameter own-evaluation morphism continues to evaluate in its selected
coefficient parent.

## Engineering checks and their limit

The predecessor completion ran a bounded thirty-four-request framing and native-invocation
exercise across two live processes using independently chosen inputs. It covered
exact rational records; admitted units and their declared inclusion; nested
owned values inside selected points/views; matrix construction/application;
characteristic polynomials, derivatives, degrees and both evaluation ports;
returned product projections; complete typed row callables; nonconstant finite
`typedMap` and mediator inputs; retained composition and map actions; both F9
comparison directions; and the public `presentationApply` packet. It checked
request identities, reply frame lengths, public result envelopes and process EOF.
Malformed rational records, incomplete graphs, foreign tokens and an unrelated
operation were checked only for their corresponding protocol error/unsupported
strata.

Separate direct native API exercises consumed actual same-session Sage row and
matrix callables, a complete polynomial record with Sage's native coefficient
callable, and the supplied nonidentity F9 coefficient map in generalized
polynomial evaluation. Sage `Family` supplies finite graph lookup; native matrix
construction consumes fully lowered rows; `map_coefficients` applies the
supplied coefficient map. A support-only coefficient graph was rejected. Python
syntax and the manifest's operation/input addresses were checked against the
public API snapshot.

The additive consumer follow-through ran a separate thirty-request framing and
native-invocation exercise with independently chosen inputs. It covered natural
semiring expressions and retained callables through exact scalar inclusions;
finite products with both named and selected-action descriptors; created apices
and actual left/right callables; finite generalized product domains and explicit
inventories; complete finite coefficient maps in `Under` records, including a
composed map and identical endpoint carriers; admitted and complete-record unit
data, their inclusion and nested owned values; and a retained matrix to
polynomial to evaluation chain. The assertions inspected frame lengths, request
identities, reply envelopes, unchanged registration scope and the declared
error/unsupported strata. The finite coefficient table was deliberately only
wire data; no homomorphism law or numerical output was asserted for it.

Nine final direct engineering checks exercised the matching-action graph path,
unknown and incompatible action rejection, owned data under selected elements,
retained creation-apex lowering, source-diagram preservation, the actual
nonidentity F9 coefficient map, incomplete finite coefficient graph rejection,
and connection-local ownership inside admitted units. Python syntax and the
unchanged nineteen operation addresses were checked separately. These earlier
framing checks did not resolve the product-only gate's mismatch with the
published pullback creation row; they are not evidence for that shape selection.

The complete cone repair first ran seven bounded product framing requests for
plain graphs, `finiteGraph`, mixed typed/untyped legs, exact source preservation,
incomplete graph rejection, and the existing native product constructor. After
the fresh constructor export and creation-diagram clarification were published,
a separate twenty-eight-request exercise used independently chosen public
packets in one live Sage process. It covered both product legs and both stored
pullback legs; actual typed target descriptors; source cospans with typed maps,
identity/composition and complete Arrow fields; explicit finite-set mapped
cospans; the published finite-to-residue inclusion as endpoint context; created
raw, typed and mixed target legs; a created apex in a native Sage product; and
a native product projection composed with the retained created pullback leg.

The same exercise checked changed source diagrams, changed complete typed
endpoints despite equal native carriers or matching inventories, missing cone
fields, incomplete graph data, absent target context, unknown lifts/actions,
using the pullback lift for a product, incorrect shape indices, and the unstored
center projection only for their `error`/`unsupported` strata. It also confirmed
that dispatching `lim.sets.pullback` remains unsupported: consuming its retained
data adds no operation registration. Assertions inspected frame lengths,
request identities, result envelopes, exact retained descriptor fields, the
unchanged nineteen advertised operations, and clean EOF. The supplied apex and
cone fields were arbitrary computational records; no numerical result,
commutation equation or universal property was asserted.

Four direct metadata-only checks additionally inspected exact nested apex/leg
retention and the inner packet's endpoint context, rejection of an unknown inner
lift, and rejection of changed common and intermediate endpoints. These checks
did not execute the cospan arrows or assert that the selected nested creation
route was mathematically applicable.

These checks assert engineering status, representation and native API use only.
They assert no numerical answers, algebraic identities, universality, semantic
placement or acceptance truth. No acceptance suite or shared Lake process was
run. The checks earn no trust and are not shipped as mathematical assertions.
Unsupported shapes and unrelated operations retain the exact dispatched id in
an `unsupported` reply. Engine failures and malformed request data produce
`error`, using the public helper's frame codec.

### Remaining interface scope

No additional public wire type was needed for this completion. The existing
nineteen registrations retain these ordinary implementation limits:

- Native object and coefficient adapters are the selected scalar, F9, polynomial,
  matrix, vector and product forms listed above. Other rings or arbitrary
  structured objects are not implemented by a category-wide registration alone.
  In particular, consuming a complete or admitted Units point for division does
  not supply a native Units parent for a product-construction factor.
- An infinite callable must be composed from the supported retained public
  actions or an actual callable owned here. The adapter does not interpret
  arbitrary functions, revive another process's token, or extend a finite
  support table to a total infinite function. Deferred native invocation can
  still report an unavailable native computation when actually applied.
- Finite graphs need their actual inventory, a supported primitive finite
  descriptor, or factors with those forms. An endpoint descriptor does not
  enumerate itself. Native `Family` and finite-parent operations require their
  usual supported native key representations.
- Unlabelled graph compositions need supplied intermediate endpoint context.
  A pullback with both unlabelled cospan arrows and unlabelled cone legs has no
  supplied target context and remains unsupported. Other named diagram arrows
  need a supported explicit endpoint wrapper. The unstored pullback center leg
  remains unsupported, and there is no pullback-construction registration here.
- General polynomial algebra application needs the actual complete `Under`
  record and coefficient map. A name without those supplied fields is not an
  implementation of that record. Only the existing selected F9 comparison is
  registered; other comparisons, factorization, analytic functions and unrelated
  declared operations remain unregistered.

These limits do not narrow a mathematical domain or supply acceptance evidence.

### Completion engineering checkpoint

The completion exercised 143 independently selected requests with the installed
Sage/passagemath runtime: 57 requests across an initial process, a foreign owner
and a restart; 57 callable/operand cases in another process; and 28 retained-data
requests plus one malformed request frame. The cases include all nineteen
operation/input pairs, the callable form of every callable registration, actual
returned matrix/vector/polynomial chains, whole finite and infinite maps, full
coefficient functions, complete selected algebra records, retained native
matrix rows, F9 components, both comparison packet forms, global and other
singleton domains, endpoint objects, supplied product/pullback packets, complete
Arrow fields, explicit selected actions, and owner rejection.

Assertions checked decimal byte framing (including UTF-8), natural request
identities, ready/reply envelopes, exact retained endpoint and inventory fields,
error/unsupported strata, unchanged registration scope and clean process EOF.
They did not assert any computed number, polynomial, equality truth, support
property, algebra law, cone equation or universal property. These scratch
engineering cases and their logs are outside the source repository and are not
mathematical acceptance assertions. Python syntax and the nineteen addresses
were checked separately against the supplied public declaration export.

### Released scalar examples follow-up

The later extension sufficiency checkpoint separately executes the concrete
selected requests from public contract `90d7d3f`'s `api/wire-examples.md` as
written. Five of those requests select existing V1 addresses. The exact modular
power and addition examples retain `element(selectedRing, expression)` while
their common invocation supplies the scalar carrier endpoint. The original
reader incorrectly required those two descriptors to be identical.

The reader now checks the existing named scalar carrier layout while retaining
the complete selected structure for expression interpretation and full operation
parameters. Actual returned payloads are decoded at the supplied endpoint;
typed maps and owned callables keep their exact stored endpoints and original
domain. A complete element can therefore contain the actual returned callable
without becoming a newly fabricated closed point. Changed selected structures
inside an operation expression, changed typed/owned endpoints and foreign nested
owners are still rejected. The native routines and all nineteen registrations
are unchanged.

The five verbatim V1 requests have their expected interface outcomes. The F9
comparison and matrix-application examples contain illustrative opaque tokens,
so their as-written requests report unavailable owners. Their literals were not
replaced with invented live tokens. Twenty-nine separate derived requests check
the affected scalar, composition, actual-data and callable readers and rejection
controls; they assert no computed value or mathematical law. Full transcripts,
the two failed scalar-example replies and a subsequent retained-callable
endpoint-reader failure are preserved outside source under
`public-extension-sufficiency-checks`. These engineering observations have no
mathematical acceptance standing.
