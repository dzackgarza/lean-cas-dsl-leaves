# Independent extension diagnostic

This subtree is a computational registration specimen built and completed from
the public contract, declaration exports and authorized interface documentation
recorded in `public-inputs.json`. No kernel implementation, acceptance assertion,
expected-answer fixture or downstream execution report was consulted. Diagnostic
work stayed in this subtree. It ships no Lean and changes no mathematical or
protocol declaration. The manifest contains 66 public operation/input pairs.

Sage 10.8 supplies exact quotient-ring, modular, polynomial, matrix, module and lazy
power-series computations. Sage's permutation groups and native GAP supply the
supported automorphism representations. All native objects, complete formed
objects and returned maps remain owned by one live connection. A formed object
retains its actual carrier module, callable pairing and full selected context.

## Implemented registration scope

`leaves.json` is the exact operation/input inventory. The table describes the
supported selected inputs at those registrations; a category-wide registration
does not claim an implementation for every object of that category.

| Family and public addresses | Supported native computation |
| --- | --- |
| `op.rings.add`, `mul`, `pow`, `neg`; dual-number coefficient maps | Integer, rational, modular, and the two published rational dual-number rings, including the explicitly supported carrier views. |
| `cmp.rational_dual.translation` | The actual Sage homomorphisms between the selected dual-number presentations in both directions. |
| `cmp.sets.fin_reversal`, `mor.sets.fin_rev`; finite order `le`, `lt` | The actual selected dimension and order, including the reversal family at dimension zero. |
| `meth.two_subsets`, `fun.core_sets.two_subsets`, `meth.cardinality` | Full finite inventories; primitive finite ordinals, published integer-square bounds, finite products, two-subsets and supported finite cyclic carriers. Two-subset map action consumes the complete selected core comparison and takes direct images. |
| `con.automorphisms`, `con.automorphisms#map`, the Sets/Groups core automorphism functors | Finite Sets use native permutation groups. Finite cyclic Groups use GAP's actual automorphism group of the selected cyclic group. Direct and named functor map actions consume both actual comparison directions. Complete native group enumeration supports whole-map comparison on finite automorphism carriers. The selected category stays explicit. |
| Sets and Groups `automorphism_forward`, `automorphism_backward`; group `inverse` | The actual stored forward or inverse arrow on the selected receiver. Both directions of an inline automorphism are read and retained. |
| General Sets `automorphism_evaluation`, `automorphism_inverse_evaluation` | The selected Sets identity functor. Other set-valued functors are explicitly unsupported. |
| `cmp.groups.cyclic_quotient_residue`, `mor.sets.cyclic_quotient_map`, `mor.groups.cyclic_quotient_aut_by_unit` | Actual quotient/residue transport, integer quotient images and multiplication by the actual selected unit with its native inverse. Finite automorphism computation requires positive modulus. |
| `mor.commutative_rings.integer_coefficients`, `fun.modules.reindex`, `fun.modules.reindex#cartesian`, `op.modules.scalar_action` | Supported native regular and vector modules over integers, rationals, integer-quotient rings and the two rational dual-number rings, together with the existing rational subspaces and formed carriers. Native scalar action applies the actual selected base map. The reindex declaration has one explicit parameter, that map. The named `obj.modules_r.restricted_regular` separately retains `R`, `S`, `q`. A cartesian invocation keeps the nested `[functorParameters,receiver]` array. Reindexed morphisms and cartesian maps retain the complete original map and selected modules. |
| `mor.sets.successor_power_series_terms`, `bind.sets.power_series_sum`, `mor.sets.power_series_coefficient` | The supplied infinite successor family in the selected coefficient ring, a native lazy infinite sum and requested coefficient observations. The binder also consumes its actual owned whole-family result and identity compositions retaining that native family metadata. No finite truncation or replacement closed-form series is used. |
| `mor.modules.rectangular_linear_map`, `row_linear_map` | Actual matrices read from complete nested finite callables, at all supplied dimensions including zero, over supported coefficient rings. Rational maps retain exact Sage matrix representations. |
| The three published degenerate-plane morphisms; `mor.sets.bilin_module_pairing` | The documented linear actions and four documented forms, together with actual native lifted forms. Scalar and value-module selections remain in the context. |
| `fun.arrows_modules.kernel`, `meth.kernel`, `meth.arrow_ker` | Exact rational native matrix kernels, including kernels of maps on native subspaces. The complete reply is `arrow(K, originalSource, typedMap(K, originalSource, actualInclusion))`. Both the native subspace and actual defining inclusion remain live. |
| `lift.bilin_module.restrict` and `lift.bilin_module.change_value_restriction`: `#obj`, `#hom`, `#forward`, `#backward`, `#factor` | Callable pullback of the original selected pairing along the supplied inclusion. Every explicit evidence-family parameter, complete base subobject and actual preceding output is consumed and retained. Nonidentity change-value maps are supported through actual callable actions, including a returned product projection. |
| `mor.bilin_module.pulled_back_forward`, `pulled_back_backward` | The two publicly documented identity carrier maps between the complete selected formed endpoints, including `morphismEndpoint` descriptors. |
| `lim.sets.product` | A complete cone with its actual apex and both typed projections. The product of two regular rational modules also has retained exact projection matrices. |
| `op.monoids.mul`, `op.monoids.one` | The explicitly selected ring multiplicative monoid, ring/module additive group viewed as a monoid, supported cyclic groups and actual finite native automorphism groups. The selected structural path determines multiplication and unit. Aut multiplication uses the documented function-composition convention and both actual directions. |
| `op.additive_monoids.add`, `fun.additive_groups.additive_monoid` | The explicit additive-group path of supported native rings and modules, including actual returned module objects. The functor has no declaration parameters and returns an owned additive monoid retaining its original group and native object. Addition consumes that selected object or the complete symbolic functor image, both actual operands, nested addition expressions and generalized families. |
| `cell.additive_groups.carrier#component` | Both identity carrier components on the exact two published routes of a supported ring/module additive group. The complete nested parameters are `[[],receiver,inverse]`; the original receiver, route endpoints and every owned dependency remain attached. |
| `mor.sets.direct_image` | The image of the actual supplied finite subset under the complete selected function, including finite subsets of supported infinite carriers. Whole power-object maps retain that function. Complete finite power domains use Sage's full subset inventory. |
| `obj.sets.group_morphisms#application`, `obj.sets.module_morphisms#application` | Application of the original complete admitted function at the supplied group pair or scalar ring/module pair. The inclusion keeps that same function. Generalized admitted families keep their original domain. No group or module law is inferred or manufactured. |
| `mor.sets.equality` | Exact supported scalar, product, module and finite-object points; complete finite-domain maps, including native finite automorphism carriers; complete native rational linear maps; and native polynomial scalar actions as detailed below. |

## Whole-map equality

For `obj.sets.maps(domain, codomain)`, finite-domain equality evaluates both actual
callables at **every point in the complete supported domain** and compares each
result at the supplied codomain. It does not label a finite sample complete.
Owned callables, complete finite graphs and supported named/composed callables
participate in the same path.

For finite integer-quotient regular modules and their restrictions, the full
carrier is enumerated by the actual Sage ring at the supplied modulus. Complete
graphs are checked against that inventory. An opaque returned module morphism or
cartesian map can be compared over every residue without exporting or replacing
its native owned callable. Composite moduli use modular-ring arithmetic directly;
the implementation does not assert that the coefficient ring is a field.

An infinite carrier is supported when both maps carry actual exact rational Sage
matrices at their complete native endpoint modules. This metadata is introduced
by native matrix actions, and is retained through identities, composition,
supported structural map actions, product projections and mediators, kernels,
restriction/change-value lift fields, factors and cartesian maps. Equality on a
native subspace restricts the matrix difference to Sage's complete basis by exact
matrix algebra. No matrix is fitted to an arbitrary callable, and no arbitrary
callable is inferred to be linear from a basis sample.

Exact polynomial metadata additionally supports the implemented ring operations,
coefficient maps and selected dual-number comparison on integer, rational and
rational dual-number carriers and their finite products. `native_polynomial.py`
introduces every coordinate as a formal Sage polynomial generator, applies native
polynomial/quotient-ring arithmetic, and composes by Sage ring homomorphisms.
Equality compares the complete normalized coordinate polynomials. This metadata
is attached only while interpreting an implemented declared native operation; it
is never inferred from observations of an arbitrary callable. Identities,
composition, declared carrier actions, product projections and mediators retain
the actual models and context.

Arbitrary functions on infinite domains, unsupported native linear or polynomial
models and whole infinite power series have no claimed equality algorithm here.
They return the public `unsupported` status when no complete supported
observation applies. A finite graph cannot supply its own completeness claim
for a domain lacking a usable independent inventory; use the complete supplied
`finiteData` or an implemented native finite carrier. In particular, a finite
graph on an unbounded domain is not treated as an equality sample.

## Complete data handling

The reader consumes both endpoints of every `typedMap`, preserves supplied finite
inventories, rejects partial or repeated-key graphs, and keeps opaque tokens on
their supplying connection. Composition uses categorical order and retains its
actual intermediate descriptor. A common point invocation keeps its generalized
domain. An identity argument on the original source requests the complete map,
including sources `Fin(0)` and `Fin(1)`. Both bare identities and typed identities
work. The published nullary `op.monoids.one` point uses the ordinary scalar
convention at the registered global-point domain, after executing its actual
source comparison. At other generalized domains it remains a complete callable.
Generalized results preserve native metadata and all dependencies. Presentation
invocations likewise consume identities, typed generalized arrows and actual
owned callable results. Returned `valueData` maps and bare owned maps can be
used directly in subsequent compositions.

Published `element`, operation expressions, `point`, `pointView`, admitted and
constrained points, generators, selected presentations, typed composition,
mediators, and an explicit set of structural functor actions are consumed
directly. The implementation does not infer a functor from equal carriers.

`arrowHom` and `subobjectInclusion` use the defining map of a complete returned
record. `liftedSubobject` retains the selected route and actual four-output steps.
`constructionField` reads the ordered port from an actual returned cone or
cocone. `constructionApex` retains that complete result, and binary-product
`constructionLeg` reads the actual stored projection. The supported finite-set
pullback creation wrapper retains its source diagram; other creation actions are
implementation gaps. `constructorMap("ctor.core", innerAction)` maps both stored
directions through an explicitly supported inner action. The object and map
readers share the declared carrier-action parameter checks, including supported
classifier-forget actions.

All seven published category-constructor signatures are parsed with complete
ordered arguments and recursive category dictionaries. Parsing never erases a
wrapper or identifies it with Sets or Groups. A well-framed constructed category
without a native implementation returns `unsupported`; missing constructor
arguments remain malformed. Supported structural views of owned automorphism
groups reuse the original native group and connection.

The native kernel result can feed directly into the restriction lift in the same
connection. A lift object retains the actual native base module and pulled-back
pairing. Each map output supplies its required endpoints and a live callable. The
factor consumes both actual input maps and returns the declared underlying base
map action. It also retains all prior outputs. No inverse equation, compatibility
proof, monicity evidence or universal-property certificate is manufactured.

## Generic interface completion

The five additional addresses consume the candidate public API with SHA256
`7bccaf5e7bcfaa682f14ce429bcae158d9c899a66daec214e5ac5a9ad885d615`.
They use the existing `apply` and `admittedPoint` protocol; no wire constructor
was added. This snapshot is a candidate supplied by the public-interface owner,
not a final freeze.

Monoid computation reads the complete selected structural path. For example,
the multiplicative monoid of a rational ring and its additive group viewed as a
monoid retain different multiplication and unit operations despite sharing a
native scalar carrier. Automorphism multiplication consumes both original
directions and composes the forward maps as `(a * b)(x) = a(b(x))`, following the
authorized generic `AutomorphismArrows.forward_mul` interface.

An owned finite subset keeps its complete ambient descriptor, actual points,
native Sage set and all producing context. Direct image uses the actual subset
argument and original function; a global function image is never substituted
for the supplied subset. The whole-map result can be reused by composition or a
generalized subset family. Equality of finite subsets compares their exact
native sets; equality of maps on supported finite power objects enumerates every
subset of the complete ambient inventory.

Group and module morphism application and inclusion preserve the selected
objects, scalar ring, complete original function and admission domain. A
non-singleton admitted family remains a family of its original functions.
Homomorphism and linearity proofs stay the caller's responsibility. Whole
application maps remain owned callables even when their hom-object domain has
no supported finite inventory or symbolic equality model.

## Additive capability follow-up

The bounded follow-up consumes candidate API SHA256
`eecf444f9a3f007684c2c494085b02cbe6945b1add5ea90db2da5ad9a33c7612` and adds only
the three related public addresses in the additive rows above. Addition takes
exactly `[M]` for the selected additive monoid. Its registration input is
`cat.additive_monoids`; the operation name is not an invented input form.
The functor registers on `cat.additive_groups`, and the carrier component uses
its exported complete-request input address.

`additive_interfaces.py` reuses the existing native scalar and module decoders.
A returned monoid retains the original selected additive group, actual native
object, original receiver and live owning connection. Subsequent additions use
that result directly. A complete symbolic input remains supported through the
explicit `fun.additive_groups.additive_monoid` path; a multiplicative structure
with a matching carrier is not accepted as an additive structure. Nested
`element`/`operationExpression` operands preserve the same selection and actual
returned data. No numeral interpretation is added to the additive operation.

The carrier component checks the full existing route through groups, monoids,
semigroups and the two classifier-forget actions against the new route through
additive monoids. Its two directions keep their exact endpoints. These identity
carrier maps do not identify additive and multiplicative operations. The
structural functor map retains the actual original callable and native metadata.

Scalar addition maps retain exact polynomial metadata where the existing scalar
models support it. Complete finite domains retain the full enumeration path.
All implemented addition maps can be returned and reused as owned callables,
including maps whose whole-domain equality is outside those native models.

## Public endpoint consumption follow-up

The existing 66 registration pairs are unchanged. The consumer accepts the
public `morphismEndpoint(actualCallable, source/target)` form where the selected
complete arrow fixes an unnamed endpoint. `objectProduct` remains an explicit
alternative; it is not a required spelling of every binary callable's source.
The selected operation's full public signature supplies native decoding context.
The exact request descriptor remains on the callable and on its returned whole
map. No native decoding view is emitted as a replacement formal object.

`endpoints.py` uses the existing native readers for the supported declared
operation families. A mediator into an unnamed product keeps actual typed or
owned component endpoint fields. It does not replace those fields by a named
carrier chosen from a parameter. A finite endpoint wrapper supplies no point
inventory: a graph still needs the actual complete `finiteData` inventory or an
independently supported explicit finite object.

Whole-callable replies retain their complete original invocation, ordered
parameters, original generalized domain, input callable and actual action. Reuse
under the original operation checks those stored parameters. Typed wrappers and
compositions also consume the selected declaration parameters. Reindex actions
consume actual owned or portable declared maps as well as typed maps, without
substituting a fresh named map for a retained result. Existing comparison
registrations accept both their presentation packet and the common `apply`
packet. Nested endpoint and typed-map framing is checked before use, and nested
opaque dependencies are resolved only on their original live session.

The follow-up uses the current executable protocol and the separately supplied
public extension candidate with SHA256
`eecf444f9a3f007684c2c494085b02cbe6945b1add5ea90db2da5ad9a33c7612`.
The earlier checked-in API snapshot was also inspected and is recorded separately.
Neither generated candidate is relabelled as a final export. Exact source
checkpoints, producer provenance, consulted paths and digests are recorded in
`public-inputs.json`.

`endpoint_smoke.py --protocol-only` checks public framing, retained descriptors,
full callable input passage, explicit graph inventories and session boundaries
without importing Sage. The full script exercises the same public port with
self-selected packets and checks only result forms, parameter retention and
malformed/foreign-owner rejection. These engineering controls contain no expected
mathematical answer and establish no mathematical correctness or acceptance claim.

At source checkpoint `eab9e3aac978087295d5ef9ab0e300edf8096bb2`, the endpoint
run completed 33 primary requests and two sequential foreign-owner requests,
and its 13 protocol-only boundary groups passed. The existing generic controls
completed 36 requests. All 14 existing completion groups completed 99 primary
requests and one foreign-owner request; the foreign request was deferred until
the first engine exited so only one native process ran at a time. Ready frames
reported Sage `10.8.13` and adapter `2026-10-24.6`. The exact runner, logs and
source digests are retained in the receipt. No additional optional native runs
were performed for this follow-up.

## Public contract conformance follow-up, 2026-10-25

This bounded follow-up starts at leaf commit
`fa0856dfc365c497a25e4a94019a1cb08b79c4d1`, consumes public contract
`90d7d3f1833cff39b77024dcee2dc43213e623ad`, and uses the supplied fresh public
declaration export with SHA256
`43392ae1c6636276519113d07c4cdc3ce8f8eeead1b4336db574c57269216079`.
All 66 existing registration pairs occur in that export's operation and input
inventories. Both registration manifests are unchanged. No producer source,
acceptance material or downstream execution report was inspected.

The public terminal-point and complete-expression interfaces exposed a gap in
the earlier decoder: a unit requested with its actual identity comparison could
be returned as a callable and then fail as an operand of the next point operation.
The global unit now returns its ordinary point data, using the supplied comparison.
The same operation at a non-global domain keeps its complete callable. Supported
`operationPoint` data retain their selected operation, ordered parameters, actual
source comparison, original domain and selected target. Nested monoid operation
expressions and the existing group-inverse expression consume their supplied
operands through the already implemented native operations. They add no address
or implementation for an otherwise unsupported monoid or group.

Successive operations also consume `valueData` around actual returned modules,
forms and base maps. Kernel requests read an actual complete returned Arrow
through the same record reader as projections. Native endpoint views retain the
selected Core action for mapped automorphism/two-subset images, module reindexing
and the published cyclic-quotient automorphism target. Typed or owned endpoint
fields remain attached unchanged; a native decoding view supplies no graph
inventory and is never emitted as a replacement object.

The port now checks nested ownership before every operation, including object
and lift requests. An unused source-Arrow field, endpoint wrapper or product
factor cannot carry a foreign token past the connection boundary. Complete
finite graphs additionally check images against an explicitly supplied codomain
inventory or primitive finite codec. These are data-framing checks; they do not
establish a mathematical equation, a group law or the correctness of an inventory.

Independent engineering cases and logs are kept outside this repository. They
exercise global and generalized units, nested expressions, exact returned-data
reuse, unnamed selected endpoints, malformed graphs and foreign owners through
the framed public port. The existing completion, generic, additive, endpoint and
callable-form scripts remain engineering controls only. The native algorithm
scope and ordinary unsupported cases in the following table are unchanged.

## Deliberate limits

### Published power-object callable consumption

The callable-form follow-up keeps all 66 registrations and consumes the five
published `powerObjectMap` fields inside their existing requests. `terminal`
and `truth` retain the selected public arrow and its declared endpoints.
`member`, finite `image`, and finite `transpose` use the existing complete
native inventories and Sage-set representation. These are data-form readers;
there is no new standalone power-map operation or generic application address.

Named power maps, mediators, and point wrappers can supply internal endpoint
context for composition. Actual typed/owned endpoint fields take precedence and
must agree exactly at the shared endpoint. Returned callables retain the
original selected descriptors. Endpoint wrappers still supply no graph inventory,
and nested owned data stay on their original live connection. A retained image
or predicate subset can feed an existing direct-image, membership, equality, or
extent consumer without substituting another function or predicate.

Infinite global images and arbitrary infinite predicate subsets remain outside
the existing finite-set implementation. Malformed field/parameter/endpoint data
are rejected; well-framed unsupported native inputs retain the ordinary
`unsupported` outcome. Exact public input hashes and validation status are in
`public-inputs.json`. No mathematical acceptance assertion is supplied here.

`callable_forms_smoke.py` exercises the five published fields through existing
registrations, including empty/singleton domains, complete generalized results,
unlabelled compositions, mediator inputs, explicit endpoint inventories, retained
subset/extent reuse, and malformed or foreign-session data. The targeted run
completed 35 primary requests and three foreign-owner controls, checking result
shapes and retention only. The protocol-only mode requires no Sage process:

```sh
python3 callable_forms_smoke.py --protocol-only
```

Omit `--protocol-only` with the ordinary contract/engine environment to run the
framed backend controls. A `powerObjectMap` in a map-valued point stays a callable;
an explicit closed `point(...)` stays a point value even when its named domain
can now be read. Actual returned typed/owned endpoints are never renamed. A
supplied terminal target inventory is retained and validated rather than replaced.
The existing endpoint controls also completed 33 primary and two foreign-owner
requests (plus 13 protocol-only groups); the existing generic controls completed
36 requests. These runs check engineering interfaces only.

The manifest addresses remain computational claims on the following precise
native input families; no category-wide address promises arbitrary native data.

| Registered family | Unsupported public inputs |
| --- | --- |
| Ring operations and integer coefficient maps | Rings other than the explicit integer, rational, modular and rational dual-number implementations; arbitrary foreign-session scalar data. |
| Monoid multiplication and unit | Monoids outside the explicit supported ring/additive-module paths, supported cyclic groups and finite native automorphism groups. The implementation does not choose a monoid law merely from a carrier representation. |
| Additive operation, additive-group functor and carrier component | Additive groups without one of the supported explicit ring/module paths, and additive monoids other than those selected functor images or their actual owned results. The separate `obj.additive_monoids.vectors` family is not implemented; module-vector additive groups use their existing module decoder. Carrier components require the complete explicit published route endpoints. Arbitrary infinite vector-addition equality has no additional native model here; the whole callable itself remains usable. |
| Direct image | Infinite subsets, subsets without complete supported finite representations or exact native point keys, and original functions without an implemented complete callable. Arbitrary infinite power-object equality is unsupported. |
| Group/module morphism application and inclusion | Missing complete selection parameters, functions without supported complete representations or matching endpoints, foreign-owned data and unsupported product/endpoint wrappers. Arbitrary hom-object enumeration is not implemented, so equality of a whole application map requires another complete supported native model or finite inventory. |
| Aut construction, core Aut functors, forward/backward and group inverse | Categories other than the exact selected `cat.sets` and `cat.groups` dictionaries; every constructed-category Aut wrapper, including nested Core, Arrow, slice, elements and subobjects; groups other than the supported finite cyclic presentations and the actual returned finite automorphism groups in the operations that consume those groups. Zero-modulus cyclic Aut objects remain unsupported. |
| General automorphism evaluation | Selected set-valued functors other than the actual `fun.sets.identity` at `cat.sets`. A functor with a matching carrier does not become that identity functor. |
| Two-subsets and cardinality | Carriers without a complete supplied or implemented native finite inventory. Native Aut cardinality uses the actual group directly. Infinite cardinality and arbitrary infinite two-subset objects remain unsupported. |
| Module reindexing and scalar action | Native modules or scalar rings outside the implemented regular, vector, rational subspace and formed-carrier readers; base maps without an implemented complete callable. No scalar action is recovered from category membership alone. |
| Matrix and row morphisms | Coefficient rings without an implemented scalar reader; matrices or vectors missing complete finite callable coordinates. Rational native matrix metadata is retained; finite modular equality enumerates the full native carrier. |
| Kernels and bilinear lifts | Kernels without an actual retained rational native matrix; general-ring submodule algorithms; forms and value modules outside the documented rational native representations. Lift evidence-family parameters, base subobject and all prior outputs are required. |
| Infinite series binder | Arbitrary infinite summable families without the retained native successor-family model, or compositions changing that family without supported metadata. The actual callable is used for every generated term. |
| Whole-map equality | Arbitrary infinite callables with neither complete native rational linear metadata nor complete supported polynomial metadata; whole infinite series; arbitrary graph keys on an unbounded or unenumerated domain. |
| Structured comparisons and projections | `structuredProjectionAction` has complete descriptor parsing but no adapter exposing arbitrary Arrow-comparison components. Constructor actions other than the implemented Core adapter, arbitrary creation actions, and non-product diagram-leg indexing remain unsupported. |

An unenumerated `morphismEndpoint` does not gain an invented finite inventory.
The named matrix/form endpoint readers use their actual declared parameters;
other opaque endpoint families require an implemented native reader or explicitly
supplied complete data. Finite graph domains containing owned points should
retain their supplied `finiteData` inventory so that the original tokens remain
the graph's actual keys.

There is enough public wire and mathematical information for the implemented
scope. The additional public `InterfaceCompletion.md` supplied the complete
category-sensitive Aut conjugation orientation and selected pulled-back
comparison telescope. Unimplemented native objects/actions are implementation
limits; no additional wire format or kernel change was requested.

## Running the specimen

The manifest is this directory's `leaves.json`; its process working directory is
this directory. The host provides the public `cas_port` helper on `PYTHONPATH`.
Set `CAS_SAGE_PYTHON` to a Python executable containing Sage, or run the manifest
with such a Python already selected. The launcher respects an existing `DOT_SAGE`
and otherwise creates a temporary writable directory for engine startup.

```sh
CAS_SAGE_PYTHON=/absolute/path/to/sage/python \
PYTHONPATH=/absolute/path/to/public-contract/python \
python3 smoke.py
```

The completion protocol checks can also be run directly:

```sh
python3 completion_smoke.py --contract /absolute/path/to/public-contract \
  --engine /absolute/path/to/sage/python
```

The independently chosen 74-request smoke run checks startup, framing, request
identity, selected packet consumption and live opaque reuse. It includes native
whole-map comparison, complete kernel-to-lift reuse, a nonidentity selected value
projection, finite Sets and cyclic Groups conjugation, reindex/cartesian data and
lazy series over two selected coefficient rings. Separate regular-module inputs
at moduli 12 and 17 exercise integer coefficient maps, both presentations of the
restriction, native scalar action, an owned whole module morphism, its complete
reindexing, full finite-domain equality and owned cartesian maps. It contains no expected
mathematical answers and does not import or invoke the acceptance suite or kernel.
Mathematical acceptance remains independent of this protocol diagnostic.

The completion run exercises 99 requests on the original live connection and
one deliberate foreign-owner request on a second connection. Its 14 groups check
whole callable framing, empty/singleton domains, actual returned map composition,
native polynomial response shapes, retained lazy-series families, finite native
Aut map reuse, selected category framing and complete cartesian parameter arrays.
The generic-interface run adds 36 requests covering complete monoid operations,
different selected structures on a shared carrier, actual finite Aut composition,
direct images and owned subset families, and group/module function application
and inclusion. It includes a non-singleton admission domain and finite subsets
of an infinite native carrier. Run it with the same environment as `smoke.py`:

```sh
CAS_SAGE_PYTHON=/absolute/path/to/sage/python \
PYTHONPATH=/absolute/path/to/public-contract/python \
python3 generic_smoke.py
```

The additive follow-up has its own standalone check:

```sh
CAS_SAGE_PYTHON=/absolute/path/to/sage/python \
PYTHONPATH=/absolute/path/to/public-contract/python \
python3 additive_smoke.py
```

It completes 66 requests on one connection and one deliberate foreign-owner
request. It covers native rational, modular and dual-number operands; an actual
returned scalar-restriction module; module vectors; nested expressions; empty,
singleton and non-singleton generalized domains; whole callable reuse;
structural functor maps; both carrier component directions; and malformed
parameter framing. The 36-request generic run and the 99-request completion run
(plus its one foreign-owner request) were also rerun for the shared decoder
change. The earlier 74-request original smoke remains evidence for the preceding
checkpoint, rather than a newly repeated run.

All 66 registration pairs were checked against the latest candidate public exported
operation and input inventories. These are engineering checks only: no computed
equality truth, cardinality, coefficient or other mathematical answer is asserted.

The endpoint follow-up uses the supplied helper and one native process at a time:

```sh
CAS_LEAF_CONTRACT_PATH=/absolute/path/to/public-contract \
PYTHONPATH=/absolute/path/to/public-contract/python \
python3 endpoint_smoke.py --sage-python /absolute/path/to/sage/python
```

Use `--protocol-only` instead of `--sage-python ...` for the framing and owner
controls that require no Sage process. The full script closes its first process
before checking deliberately foreign tokens on a second process.

## Public inputs and engine documentation

- Latest additive-follow-up contract guide: published `6cf4cda6eb34169a7c34dba4d269bd0212f78383`, read at local `89f514d7a496e3867f24efefc7f71bbda88fba7f`; tree `0cbfe994b2aeb4edf2564b216a3194598eef1443`. The consumed guide includes additive operation/carrier data, terminal-point invocation and actual-data ownership guidance. The public Port and Python helper are unchanged from the preceding consumed contract.
- Earlier consumed documentation update: published `98794d1ac255a51d2396b59f041650f4d564a998`, read at local `c74abb724fd1424d590efc5fd0e21d67aaa55034`; tree `8fdf6a4e6b60f98017f6b967babb0cc180156b39`. This update made the generic Aut multiplication convention explicit in `api/wire-examples.md` and changed no executable protocol.
- Completion contract used for the standalone runs and retained in candidate API provenance: published `80bf36d2131e00e78cba2c8461db7b32d98a86f4`, read at local `aa8477de4aebc83823b88ac4885225e8fc13d9c5`; tree `7de02aec2fd5d89d13683561ee92055909c28eb7`.
- Earlier completion contract consumed during review: published `c6e24107ec84481a8240bb3cae5c31f67a098a71`, local `c97110dbef75cb77d249ae3a51a95cdc8f90af19`; tree `c08793f7c1bb4843ad0f6131ad8c32d9db9c928d`.
- Original contract revision retained in the declaration export provenance: `8397df15042598f5ce9a75cdb22675c65b06fc89`.
- Latest candidate API SHA256: `eecf444f9a3f007684c2c494085b02cbe6945b1add5ea90db2da5ad9a33c7612`; mathematical declaration producer `4acd7aff0350c5a84ce695e42eaadfd583ac343d`, protocol producer `a131843a8c4cd8222814ca3949a27dc41dd7a29e` and exported producer identifier `546cffae249e1d53c66cc7d62aeba74e426c6592`. These identifiers are provenance only; no producer implementation was inspected. This remains a candidate API, not a final freeze.
- Prior candidate API SHA256: `7bccaf5e7bcfaa682f14ce429bcae158d9c899a66daec214e5ac5a9ad885d615`; mathematical declaration producer `4ea82e7cf6f5fd75234fd2ce18255a45ad851379` and exported producer identifier `1dbcaf3af7718d4e7f347eb3bfa1d0aa55a18330`.
- Earlier API SHA256: `691d2b80c2ff4fd6a0e99745beee82117a5f110a288674bb9b58fc930034c22a`, with mathematical declaration revision `7e848db36ff74faf62b00304cc0186a8bac641b7`; complete earlier provenance is retained in `public-inputs.json`.
- Additional public mathematical interface documentation: `InterfaceCompletion.md`, published revision `93e1a738`; its exact content hash is recorded in `public-inputs.json`.
- Authorized public generic multiplication convention: `AutomorphismArrows.lean` at mathematical revision `4ea82e7cf6f5fd75234fd2ce18255a45ad851379`, SHA256 `42494a964a198c8df24c229c68c8a69ed3ccdf85b09bb70db2ffaf9ca5644bd0`. Only that generic source and the authorized interface document were read; no neighboring test or mathematical source was opened.
- The additive follow-up read only the new public API, public contract and this diagnostic subtree. It made no additional mathematical-source, kernel-source, external mathematical-test or downstream-report reads.
- [Sage polynomial quotient rings](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_quotient_ring.html).
- [Sage ring homomorphisms](https://doc.sagemath.org/html/en/reference/rings/sage/rings/morphism.html).
- [Sage integer quotient rings and complete finite iteration](https://doc.sagemath.org/html/en/reference/finite_rings/sage/rings/finite_rings/integer_mod_ring.html).
- [Sage matrix construction](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/constructor.html) and [matrix kernels](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html).
- [Sage lazy power-series rings](https://doc.sagemath.org/html/en/reference/power_series/sage/rings/lazy_series_ring.html) and [lazy series](https://doc.sagemath.org/html/en/reference/power_series/sage/rings/lazy_series.html).
- [Sage permutation groups](https://doc.sagemath.org/html/en/reference/groups/sage/groups/perm_gps/permgroup_named.html) and [native GAP morphisms](https://doc.sagemath.org/html/en/reference/groups/sage/groups/libgap_morphism.html).
