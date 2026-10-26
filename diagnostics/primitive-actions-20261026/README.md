# Primitive object-action specimen

This independently authored specimen contains two complete-request object-action
registrations, one generic element-operation registration, and one existing
selected-set observation registration in its own `leaves.json`:

| Operation | Input |
| --- | --- |
| `fun.rings.semiring` | `fun.rings.semiring#input` |
| `fun.semirings.monoid` | `fun.semirings.monoid#input` |
| `op.monoids.mul` | `cat.monoids` |
| `mor.sets.equality` | `mor.sets.equality` |

Both object requests use `{"ctor": OP, "args": [], "receiver": DATA}`. These published
declarations have no explicit non-proof parameters. Nonempty parameter arrays are
rejected. The two map actions are not registered here. The multiplication and
equality ports use the common `apply` envelope described below. Existing extension
and v1 manifests and registrations are unchanged.

## Public inputs and field order

The implementation was authored from the leaf's computational source and
`AGENTS.md`/`INTENT.md`, the public contract at published revision
`3f7a22e0b6afc3e745f3aa60a9ceecf6740948d5` (tree
`3f1b3a79e1fada93c4d69557d0f9876f075dc2e4`), and the supplied pure public
declaration export. The latter records mathematics published at
`f657b90ce37e1fcd8a21c9ec8399ea6a7c5414e1`, tree
`611f8b64ad0dac925d1c258327fc36e273ac75ad`, and actual development exporter
producer `025c957c70f7b14eec1e89a309c8c630e0201b89`. Its SHA-256 is
`6c6e9cb1e9fd46ecbd162bbdc4bf5f32ac16ddf5386ce133c36089a991ca500a`.
That is provisional export provenance, not a relabelled final integrated API.
The older checked-in `api/declared-ports.json` is not the admission source for
these two new addresses.

The contract's `api/wire-examples.md#registered-functor-actions`, complete-input
and ownership sections, `CasContract/Port.lean`, and `python/cas_port.py` specify
the framing. The exported non-proof constructor fields specify these arrays:

| Public record | Data slots in order |
| --- | --- |
| `RingCat` | `[carrier, ring]` |
| `Ring` | `[semiring, neg, sub, zsmul, intCast]` |
| `SemiRingCat` | `[carrier, semiring]` |
| `Semiring` | `[addCommMonoid, monoid, natCast]` |
| `MonCat` | `[carrier, monoid]` |
| `Monoid` | `[mul, one, npow]` after the one-field record elisions |
| `AddCommMonoid` | `[add, zero, nsmul]` after the one-field record elisions |

For complete record inputs the first adapter retains the exact supplied carrier
and semiring field; the second retains the exact supplied carrier and monoid
field. It does not reconstruct callable data, substitute a named representative,
or supply proof fields. An outer `valueData` envelope is supported, including
reuse of the first action's actual result by the second. Nested supplied data
and opaque dependencies are preserved. Only complete visible record structure is
supported; an unknown whole-object opaque token has no reader here.

## Native named inputs

`fun.rings.semiring` additionally supports:

| Receiver | Native parent |
| --- | --- |
| `obj.rings.integers()` | Sage `ZZ` |
| `obj.rings.rationals()` | Sage `QQ` |
| `obj.rings.integers_mod(n)` | Sage `IntegerModRing(n)` |
| `obj.rings.polynomials(R)` | Sage `PolynomialRing(R, "x")` |
| `obj.rings.mv_polynomials(n, R)` | Sage `PolynomialRing(R, n, "x")` |
| `obj.rings.matrices(n, R)` | Sage `MatrixSpace(R, n)` |
| `obj.rings.power_series(R)` | Sage `LazyPowerSeriesRing(R, "t")` |

In the last four rows `R` is exactly one of
`obj.commutative_rings.integers()`, `obj.commutative_rings.rationals()`, or
`obj.commutative_rings.integers_mod(n)`. All natural parameters, complete selected
coefficient descriptors and original request packets are retained. The engine's
private variable names do not add public parameters.

`fun.semirings.monoid` also supports `obj.semirings.naturals()` through Sage `NN`.
Other named forms, including real and complex rings and unimplemented coefficient
presentations, return `unsupported` for the exact dispatched operation.

Native output is the complete public record, with type-valued, scalar and callable
fields represented by owned `opaqueData` tokens. The underlying values use Sage
parents, `zero()`, `one()`, native addition/multiplication, integer scalar action,
exponentiation and coercion. Function slots keep the published currying order,
including `Nat → carrier → carrier` for `npow` and `nsmul`. No arithmetic
algorithm is reimplemented. Each native field retains its full original request.
Completed request/result pairs remain on the same connection.

A portable supplied record remains portable when its retained result fields have
no opaque dependencies. A native result remains session-owned, even under
`valueData`. The second adapter reuses its actual fields on that same connection.
Foreign or expired tokens return an unavailable computation; no serialized field
chooses an owner and a new process cannot revive a token. The generic multiplication
registration below consumes these actual native monoid fields on their owning
connection. The equality registration below also consumes the actual point data
on that connection. Other later operations still need their own admitted
implementation or representation bridge.

## Generic monoid multiplication

The separately added `op.monoids.mul` registration uses `cat.monoids`. The public
`CasCatalogue.Algebra.MonoidOperations.mul` signature has one parameter `M : MonCat`
and source/target `(M.carrier × M.carrier) → M.carrier`. It uses no invented
`op.monoids.mul#input` form. Complete requests have the existing seven fields:

```text
apply("op.monoids.mul", [M], actual_arrow,
      original_domain, actual_product_source, actual_target, actual_argument)
```

The selected `M` is a complete supplied `[carrier, monoid]` record, optionally
under `valueData`. The monoid has all three published data slots. Multiplication
uses its actual first slot, the curried `carrier → carrier → carrier` function.
It does not reconstruct a ring, semiring, source functor, or formal representative.
The actual source must expose its two `objectProduct` factors, directly or through
the supported retained endpoint forms described below. The supplied
source, target, domain, full parameter list, operands and results remain retained.
Typed-map wrappers are checked against those exact endpoints; the native parent
is never used to identify distinct selected descriptors.

The supported multiplication-field forms are:

- An owned native field supplied by this process's object actions. Its stored
  carrier must match the supplied record's carrier. The adapter calls that
  field, including its original currying, on the actual decoded operands.
- A complete curried finite callable: an outer graph whose values are complete
  inner graphs or compatible owned callables. `Fin(n)`, `finiteData`, and native
  finite modular carriers supply supported inventories. As permitted for a
  function-valued record field, `finiteGraph` may supply a missing field-domain
  inventory; the nested copies must agree. Ordinary generalized argument maps
  still require their actual source's inventory, not a sampled field domain.

Native operands support this process's retained zero, unit and prior product
tokens; raw integer/natural/modular points; reduced rational records; and
`element`/`valueData` wrappers retaining the exact selected monoid, actual carrier
or endpoint, or original named ring/semiring descriptor. A nonnegative `numeral`
is read only under that retained original named ring/semiring selection. Generic
monoids acquire no numeral interface. Other native algebraic points, including
matrix, polynomial and power-series points, require retained native tokens;
their alternative literal/expression codecs are not implemented by this port.

The shared callable reader privately reuses only `extensions-20261024/wire.py`, without
importing its backend or registrations. It supports complete finite graphs,
`typedMap`, `valueData`, identity, mediator, composition with retained shared
endpoints, supported `element`/`point` wrappers, and this process's returned
owned callables. A supplied operation descriptor must retain the same complete
`[M]` parameter array. Reusing an owned operation callable also checks its retained
operation and parameter array; it consumes that callable's actual computation.

At the public global-point domain `obj.sets.fin(1)`, a pair of point data or an
explicit generalized argument map yields a point result. Native point results
are owned tokens that the same multiplication port can consume again. At every
other domain, including other singleton representations, the result is
`valueData(typedMap(original_domain, actual_target, owned_callable))`. In
particular an identity argument on the whole product source returns the whole
multiplication map. No representative point or finite sample replaces it.
The returned callable retains the complete invocation and its actual input
callable and multiplication action; later requests use the retained computation.

Unimplemented field formats, whole-object opaque monoids, symbolic operation
families outside this port, and missing callable inventories report unsupported
computation. Foreign or expired nested tokens remain unavailable. No registration
was added for `op.rings.mul`, `op.semirings.mul`,
`fun.rings.multiplicative_monoid`, or another target shortcut.

## Complete point and callable inputs

The subsequent point-reader extension is confined to this specimen. Its shared
`point_calls.py` reads the public contract's scalar-point, pair, callable,
`typedMap`, mediator and composition forms. It preserves the complete request
and selected wrappers in retained closures and invocation records. Native scalar
readers use the selected descriptor or the owned carrier's original request;
native parent identity never determines a selected structure.

| Input position | Supported reading |
| --- | --- |
| A closed product argument | `[left,right]`, recursively reading each actual point field |
| A generalized product argument | The same ordered two fields, each containing its complete callable at the actual shared domain |
| A product field containing a complete callable fragment | `typedMap`, `point`, `compose`, `mediator`, a complete finite graph, or an owned callable; its actual endpoint framing is checked before evaluation |
| A scalar `element(selected,expression)` | Its exact owner remains attached; literals, owned data and supported complete point/callable expressions retain that selection |
| A selected monoid operation expression | `element(M,operationExpression("op.monoids.mul",[M],[left,right]))`, with both operands decoded recursively and the same full `M` |
| A complete callable body | The existing finite graph, `finiteGraph`, `identity`, `typedMap`, `mediator`, `compose`, or compatible owned callable representation |
| A mediator | Both components are complete arrows at the actual shared domain; `element` supplies a complete scalar point arrow at the global domain |
| A composition | The supplied shared endpoint comes from an actual typed/owned constituent, or the supported full declaration of monoid multiplication or equality |

Function-valued point data retain their own function endpoints. They are not
automatically evaluated as arrows out of the invocation's generalized domain.
Conversely, a scalar is not made into a constant map on a non-global domain.
An untagged array inside an explicit `typedMap` body remains in callable position
and uses the graph codec. At an untagged product-argument position the reader
checks the component and graph framings against the actual domain, accepting an
unambiguous complete reading. It does not choose by a computed mathematical value.

A finite graph's product-valued image can retain complete closed point fragments.
Evaluation uses the fragment's actual retained global-point domain. If the
fragment has no retained domain, only the original invocation's actual global
domain is available. A callable on another domain is not evaluated at a sample
point to fill a scalar slot. All original graph rows, endpoints, selected owners
and opaque dependencies remain attached to the computation.

An `objectProduct` can be read through its unchanged `valueData` or `finiteData`
wrapper, or through `morphismEndpoint` whose actual typed/owned field or supported
full declaration supplies the product interface. An abstract `morphismEndpoint`
does not provide a finite inventory. Supplied typed-map and composition endpoints
are compared as complete descriptors, including their retained parameters.
A selected target endpoint of a complete monoid multiplication declaration or
its retained callable also keeps that exact monoid as point-owner context.

Carrier decoding supports the actual owned carrier field and these complete
selected paths, without registering any of their additional actions:

- `fun.semirings.forget` applied to the complete supplied `SemiRingCat` record.
- `fun.monoids.semigroup` applied to the complete supplied `MonCat`, followed by
  `classifierForget("clf.magmas.associative",[])` and then
  `classifierForget("clf.sets.binary_operation",[])`.
- `fun.sets.identity` around a supported selected-set descriptor.

The point wrapper's selected owner must be an exact retained context of that
path. A different monoid or ring wrapper is not accepted merely because Sage
uses the same parent for it. The native scalar named-set bridge reads the exact
stored original ring/semiring descriptor for integers, rationals, modular
integers or naturals; it does not inspect the point's parent to choose a set.

## Selected-set equality observation

The added row is exactly `mor.sets.equality` on the already published
`mor.sets.equality` complete-request input. The supplied public declaration is
`CasCatalogue.Foundation.PowerSets.equality : (X : Type) → (X × X) → omega`.
The contract specifies the truth-value observation codec at
`obj.sets.truth_values`. Requests retain all seven fields:

```text
apply("mor.sets.equality", [X], actual_arrow,
      original_domain, actual_product_source, actual_truth_target, actual_argument)
```

Both source factors retain the complete selected `X`. Its exact parameter array
also remains attached to the named arrow and any reused owned operation callable.
The selected set, original domain, actual arguments, source and target, callable
fragments, returned results and live ownership are retained by the same process.
The result at `obj.sets.fin(1)` is `valueData` containing a JSON Boolean. At any
other domain it is `valueData(typedMap(original_domain,actual_truth_target,token))`;
each evaluation checks the Boolean result shape. Whole-domain identity arguments
use that same interface. A later equality invocation can consume its actual
returned observation callable.

The computation calls existing Sage/Python value equality through `operator.eq`.
It supports:

- Points belonging to this process's actual retained carrier fields, including
  its native zero, unit, numeral and multiplication results. Matrix, polynomial
  and power-series points use their actual native values. Engine equality may
  fail when the engine cannot decide the supplied values; no approximate or
  sampled replacement is used.
- Public scalar data at the selected integer, natural, rational, positive-modulus
  modular and `Fin(n)` sets, with their representation checks, and JSON Boolean
  points at the selected truth-value set.
- The complete carrier-action paths listed above, with the actual native data
  and selected source structures retained.
- Ordered products of supported point interfaces.
- Function-valued points at `obj.sets.maps(D,Y)` when the actual `D` supplies a
  supported complete finite inventory and `Y` has a supported point reader. The
  existing callable helper evaluates the actual two functions on that inventory;
  native equality compares their outputs. Infinite function equality has no
  implementation here.

The common decoder also allows complete named monoid multiplication fragments
and its selected `operationExpression` inside an equality input, using the
fragment's supplied monoid field, complete parameter list and actual endpoints.
An expression retains its original operand fields; it is not retyped as an arrow
or a synthetic common invocation. This does not register or implement a ring/semiring multiplication
shortcut. An observation is an untrusted computational Boolean or Boolean-valued
callable, not a proposition, a certificate, or a declaration that two selected
structures are equal.

## Producer and consumer codec audit

A subsequent public-only audit completed ordinary representation conversions
between these same four ports. It added no registration or public tag.

An owned scalar returned by a closed multiplication invocation can now be used
inside the complete `point` and `typedMap` fragments already accepted in product
components, mediators, compositions and observations. Its private receipt retains
the exact seven-field creating invocation, full ordered selected parameters,
actual input callable, actual action and original returned data. The converter
requires that invocation's exact closed domain. It checks the complete producing
monoid against any selected monoid retained in the requested target or point
owner. Matching native parents, scalar names or carrier data alone cannot
replace that parameter check.

The requested target remains attached verbatim. A supported point-data conversion
can read the exact retained carrier field, the producer's complete carrier-action
path, its named declaration endpoint, its own retained point endpoint, or a named
scalar codec with an explicit matching selected owner. The checks read the actual
creating record and its complete request. They do not infer structure from a
native parent's class. Changed complete parameters are rejected even when their
native parent, carrier field and multiplication field happen to coincide.

This conversion is specific to scalar point data. An already stored whole or
generalized `Callable` continues through the strict original source/target checks.
Its endpoints cannot be relabelled by the scalar converter. A returned point
also cannot become a constant map on another domain. An object record's scalar
unit or zero field has no creating point-arrow domain, so an `element` envelope
must provide its complete point context before it occupies an arrow slot.
An inline result of a supplied complete multiplication graph likewise retains
its `element(M,data)` selection through the actual prior monoid-object receipt;
the consumer reads its exact returned carrier and keeps the original wrapper.

When an earlier owned whole callable is evaluated by a later closed invocation,
the reply's token retains that later invocation and the actual previously
computed native value. Its dependency keeps the earlier callable, producing
fragment, field, selected parameters and operands. The wrapper performs no new
arithmetic and substitutes no formal representative. Literal and native field
results also retain their original fragment or field application. Every receipt
is private implementation data, not a wire certificate or an acceptance claim.

The finite function-observation reader now consumes the specimen's native
function-valued record fields at their published curried interfaces:

| Retained field | Exact callable interface |
| --- | --- |
| `Monoid.toSemigroup`, `AddMonoid.toAddSemigroup` | `carrier → carrier → carrier` |
| `Monoid.toNPow`, `AddMonoid.toNSMul` | `Nat → carrier → carrier` |
| `Semiring.toNatCast` | `Nat → carrier` |

Each field is matched to its exact creating object-action request and its actual
slot in the returned record. The adapter invokes that retained native function.
Partial applications preserve the supplied operands and return compatible owned
callable data; final native values retain the same selected carrier. This does
not curry or reinterpret the separately returned whole multiplication map, whose
source remains its supplied binary product. Function equality still requires a
complete finite domain inventory. In particular, a field with the complete
natural-number source does not acquire a finite observation interface merely
because a finite sample could be supplied.

## Representation boundaries and public framing question

Supported fragments must have enough retained domain and endpoint data to be
read at their actual position. A raw native scalar in an unlabelled composition
slot is not a complete arrow; the public `element`, `point` and `typedMap` forms
provide that context. A missing shared endpoint for an unlabelled composition
is not filled with an inferred native carrier. Graphs still require actual
domain inventories; neither a graph's keys nor a small sample creates one.

The public contract gives untagged arrays both ordered product-data and finite
graph roles, without a general precedence rule for bytes satisfying both
framings. This reader checks both against the complete supplied domain. If both
remain well framed, it reports `unsupported`; `mediator`, `finiteGraph`, or an
explicit `typedMap` callable body resolves the framing. A public precedence rule
would be needed to select one reading in an actually ambiguous untagged case.
This is a framing question, not a request for mathematical answers or a change
to any selected declaration.

Other operation-expression families, `operationPoint`, `pointView`, admission/constrained
wrappers, arbitrary additional carrier paths, unknown whole-object opaque
records, and unsupported native literal codecs remain implementation gaps.
These already have public forms; this specimen does not claim a contract defect
because it lacks their computational readers. Equality of general infinite
callables is also unsupported. Lost or foreign owners remain unavailable even
inside a wrapper, graph, endpoint, selected structure or returned result.

## Running the specimen and local checks

The manifest starts `python3 backend.py`. The existing `backends/engine_python.py`
selector honors `CAS_SAGE_PYTHON`; the host supplies the public `cas_port` helper
on `PYTHONPATH` as documented by the contract.

For local framing/schema checks with a separately supplied public contract and
installed Sage/PassageMath interpreter:

```sh
python3 protocol_checks.py --contract /path/to/leaf-contracts --engine /path/to/sage-python
python3 multiplication_protocol_checks.py --contract /path/to/leaf-contracts --engine /path/to/sage-python
python3 point_observation_protocol_checks.py --contract /path/to/leaf-contracts --engine /path/to/sage-python
python3 composability_protocol_checks.py --contract /path/to/leaf-contracts --engine /path/to/sage-python
```

These self-designed checks cover the exact manifest rows, framing, complete
output field slots, reuse of actual returned fields, unsupported operations,
parameter rejection and isolation between two live sessions. They assert no
mathematical values or laws and are evidence of no mathematical acceptance.
The multiplication checks additionally exercise actual same-session point reuse,
whole maps, generalized maps, later use of returned callables, selected-parameter
and endpoint preservation, and supplied finite-field data. A synthetic graph
fixture checks data lookup only and is not asserted to define a monoid.
The point/observation controls check complete nested fragments, scalar and
generalized product framing, source and target preservation, callable reuse,
selected-owner rejection, Boolean result shape, native point reuse through
equality, and isolation between two live sessions. They assert no Boolean answer
or mathematical result. The shared reader and the equality row are a separate
leaf implementation change from the earlier multiplication-port addition.
The composability controls additionally cover owned scalar point fragments,
later closed results of owned whole callables, declaration and retained-point
endpoints, selected operation expressions in observations, native curried field
observations, exact creating-request retention, and rejection of changed complete
parameters sharing the same carrier. Internal controls inspect retained packet
and data-object identity only; they do not compare native mathematical values.
No kernel, acceptance suite, fixed question corpus or runtime acceptance result
was inspected or run. These controls provide no correctness or acceptance evidence.
