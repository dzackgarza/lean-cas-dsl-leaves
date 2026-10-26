# Primitive object-action specimen

This independently authored specimen contains two complete-request object-action
registrations and one generic element-operation registration in its own `leaves.json`:

| Operation | Input |
| --- | --- |
| `fun.rings.semiring` | `fun.rings.semiring#input` |
| `fun.semirings.monoid` | `fun.semirings.monoid#input` |
| `op.monoids.mul` | `cat.monoids` |

Both object requests use `{"ctor": OP, "args": [], "receiver": DATA}`. These published
declarations have no explicit non-proof parameters. Nonempty parameter arrays are
rejected. The two map actions are not registered here. The multiplication port
uses the common `apply` envelope described below. Existing extension and v1
manifests and registrations are unchanged.

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
connection. Other later operations still need their own admitted implementation
or representation bridge.

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
The actual source must expose its two `objectProduct` factors. The supplied
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

The callable reader privately reuses only `extensions-20261024/wire.py`, without
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

## Running the specimen and local checks

The manifest starts `python3 backend.py`. The existing `backends/engine_python.py`
selector honors `CAS_SAGE_PYTHON`; the host supplies the public `cas_port` helper
on `PYTHONPATH` as documented by the contract.

For local framing/schema checks with a separately supplied public contract and
installed Sage/PassageMath interpreter:

```sh
python3 protocol_checks.py --contract /path/to/leaf-contracts --engine /path/to/sage-python
python3 multiplication_protocol_checks.py --contract /path/to/leaf-contracts --engine /path/to/sage-python
```

These self-designed checks cover the exact manifest rows, framing, complete
output field slots, reuse of actual returned fields, unsupported operations,
parameter rejection and isolation between two live sessions. They assert no
mathematical values or laws and are evidence of no mathematical acceptance.
The multiplication checks additionally exercise actual same-session point reuse,
whole maps, generalized maps, later use of returned callables, selected-parameter
and endpoint preservation, and supplied finite-field data. A synthetic graph
fixture checks data lookup only and is not asserted to define a monoid.
No kernel, acceptance suite, fixed question corpus or runtime acceptance result
was inspected or run. The public encoding was sufficient for these supported forms.
