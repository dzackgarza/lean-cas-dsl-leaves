# Independent extension diagnostic

This subtree is a computational registration specimen built and completed from
the public contract, declaration exports and authorized interface documentation
recorded in `public-inputs.json`. No kernel implementation, acceptance assertion,
expected-answer fixture or downstream execution report was consulted. Diagnostic
work stayed in this subtree. It ships no Lean and changes no mathematical or
protocol declaration. The manifest contains 93 public operation/input pairs.

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
| `fun.commutative_rings.ring` on `cat.commutative_rings` | Ordinary object action on the existing integer, rational, modular and rational dual-number native readers. The owned result retains the actual Sage ring, full source receiver and complete request; existing ring operations consume that image directly. |
| `op.rings.add`, `mul`, `pow`, `neg`; dual-number coefficient maps | Integer, rational, modular, and the two published rational dual-number rings, including the explicitly supported carrier views. |
| `cmp.rational_dual.translation` | The actual Sage homomorphisms between the selected dual-number presentations in both directions. |
| `cmp.sets.fin_reversal`, `mor.sets.fin_rev`; finite order `le`, `lt` | The actual selected dimension and order, including the reversal family at dimension zero. |
| `meth.two_subsets`, `fun.core_sets.two_subsets`, `meth.cardinality` | Full finite inventories; primitive finite ordinals, published integer-square bounds, finite products, two-subsets and supported finite cyclic carriers. Two-subset map action consumes the complete selected core comparison and takes direct images. |
| `con.automorphisms`, `con.automorphisms#map`, the Sets/Groups core automorphism functors | Finite Sets use native permutation groups. Finite cyclic Groups use GAP's actual automorphism group of the selected cyclic group. Direct and named functor map actions consume both actual comparison directions. Complete native group enumeration supports whole-map comparison on finite automorphism carriers. The selected category stays explicit. |
| Sets and Groups `automorphism_forward`, `automorphism_backward`; group `inverse` | The actual stored forward or inverse arrow on the selected receiver. Both directions of an inline automorphism are read and retained. |
| General Sets `automorphism_evaluation`, `automorphism_inverse_evaluation` | The selected Sets identity functor. Other set-valued functors are explicitly unsupported. |
| `cmp.groups.cyclic_quotient_residue`, `mor.sets.cyclic_quotient_map`, `mor.groups.cyclic_quotient_aut_by_unit` | Actual quotient/residue transport, integer quotient images and multiplication by the actual selected unit with its native inverse. Finite automorphism computation requires positive modulus. |
| `mor.commutative_rings.integer_coefficients`, `fun.modules.reindex`, `fun.modules.reindex#cartesian`, `op.modules.scalar_action` | Supported native regular and vector modules over integers, rationals, integer-quotient rings and the two rational dual-number rings, together with the existing rational subspaces and formed carriers. Native scalar action applies the actual selected base map. The reindex declaration has one explicit parameter, that map. The named `obj.modules_r.restricted_regular` separately retains `R`, `S`, `q`. A cartesian invocation keeps the nested `[functorParameters,receiver]` array. Reindexed morphisms and cartesian maps retain the complete original map and selected modules. |
| `fun.modules.fibre_inclusion`, `fun.modules.fibre_inclusion#map`, `fun.modules.underlying`, `fun.modules.underlying#map` | Object and map actions consume the existing native module and callable readers in this session, including actual returned subspaces and restrictions. The fibre action retains `[R]`; the underlying action retains `[]`. Object images and whole/generalized callables remain owned, with complete original and actual-image endpoints. |
| `fun.bilin_module.forget`, `fun.bilin_module.forget#map` | Ordinary object and map actions consume the existing complete formed-object and callable readers, with both selected parameters `[R,W]`. The actual carrier module, original form, selected native value module, request and original/image callable endpoints remain retained and reusable. |
| The eight named structural carrier functors and both classifier-forget actions listed below, with their paired map ports | Supported ring/module native carriers, their actual operation callbacks, exact action and original receiver, and complete source/image callable interfaces. Classifier forgetting retains the selected complete descriptor; it supplies no classification law. |
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

## Ordinary bilinear-module forgetting

The two existing actions `fun.bilin_module.forget` and
`fun.bilin_module.forget#map` use their published complete-request input
`fun.bilin_module.forget#input`. Contract publication
`5db631a34c9d4f65a535fad61b6f76af39fb56f6` publishes these addresses, the
ordered explicit parameters `[R,W]`, and the common object/map request framing.
No declaration, mathematical definition or protocol encoding changes here.

The object action reads the actual `Form` through the existing backend reader,
reads both selected parameters through the native ring/module readers, and keeps
their native scalar interfaces consistent. Its owned `BilinearModuleImage`
contains the actual carrier `Module` with its original point codecs and scalar
action, the complete original `Form` including its callable pairing and context,
the actual selected value module, and the entire original request. The formal
caller owns the dependent source-family and parameter typing; the leaf does not
infer a different value module from a carrier or certify a bilinear law.

Supported source representations are those already read by this package: the
four named forms, the supported portable change-value and morphism-endpoint
descriptors, complete subobject-apex descriptors, repeated `valueData` wrappers,
and actual owned forms returned by the existing lifts. The generic
`obj.bilin_module.bilinear_form` constructor has no native form reader here and
is not added by this registration. The public functor's domain is unchanged.

The map action uses `functor_map_invocation`, the existing complete callable
reader, and both actual returned module images. It checks the images' selected
functor, complete ordered parameters and original source objects. It retains the
original source-category callable and both original endpoints without replacing
them by a named map or a sampled matrix. Selected image points keep the original
callable's representation-specific reader; supported formed morphism endpoints
retain their complete descriptor when the image's point codec is read.
Whole maps and generalized replies preserve their exact domains and image
targets through the existing `Callable` and `Invocation` records. Both images
and returned maps can then enter the module fibre, underlying and scalar-action
consumers; a map with native linear data can enter the existing kernel consumer.

`bilinear_forget_smoke.py` checks these public interfaces, including an actual
owned form and arrow returned by a lift, malformed selections and closed nested
owners. It asserts no pairing value, arithmetic answer, equality truth, functor
law or mathematical acceptance outcome. Run it with:

```sh
python3 bilinear_forget_smoke.py --contract /absolute/path/to/public-contract \
  --engine /absolute/path/to/sage/python
```

The final focused run completed 179 primary-connection requests and five
closed-owner controls. The affected existing module and structural-carrier
checks completed 122 and 217 primary requests, respectively, with three
closed-owner controls each. These are interface findings only.

## Module fibre-inclusion and underlying actions

`module_functor_interfaces.py` adds the four existing registered actions to this
backend's session. Each registration uses its published complete-request
`<functor>#input` address. The object actions consume the complete receiver with
`construction_invocation`; the map actions consume the common seven-field request
with `functor_map_invocation`. The fibre functor's one selected ring parameter and
the underlying functor's explicit empty parameter array remain present in every
required position. The addresses and signatures come from public contract
`5db631a34c9d4f65a535fad61b6f76af39fb56f6`.

An object reply retains the existing native `Module`, its original read/write
codec, selected scalar ring, complete receiver and request. Both finite and
infinite images are owned native data; no finite enumeration is required for
these object actions. Existing native module consumers can reuse the result on
the same connection. A restricted module keeps its original scalar-action
callback and actual base map rather than substituting its native parent's ring.

A map consumes the actual original callable with both source-category endpoints
and both returned image objects. The retained images must have the same selected
functor, ordered parameters and original receivers as this request. The supplied
callable performs the entire action through the existing Sage matrix, native
callable or complete graph reader. Sage's `coerce_map_from` supplies the native
scalar identity retained by fibre inclusion. Outputs pass through the existing
target-module codec. No matrix is fitted to samples and no source map is replaced
by a declaration recipe. Whole and generalized replies retain their exact
supplied domains and image targets through the existing `Callable`/`Invocation`
records. Public `valueData` wrappers preserve those same interfaces and owners.

The new map registration requires actual returned image data. Older explicitly
supported symbolic carrier maps remain readable when supplied as nested data to
existing operations. This compatibility reader does not replace the actual
images required at the new map boundary. Foreign or expired native tokens keep
the existing session failure behavior. Other native modules, unsupported
callables and portable image representations without an implemented reader
remain implementation limits.

The leaf-owned `diagnostics/module_functor_actions` specimen supplied prior art
for the public requests and ownership discipline. This addition reuses the
extension backend's existing unbounded native readers instead of installing a
second native process. No kernel, acceptance test or downstream report was read.
The standalone `module_functor_smoke.py` checks public framing, complete selected
data, returned-data reuse and ownership only; it asserts no computed arithmetic
answer, equality truth or functor law.

## Structural carrier actions

`carrier_functor_interfaces.py` extends the same owned-image adapter for ten
published structural actions. It adds their object and map registrations, each
on the exact complete-request input published by the pinned contract:

| Object operation | Complete request parameters | Published source and target |
| --- | --- | --- |
| `fun.modules.additive_group` | `[]` | Total modules to additive groups |
| `fun.additive_groups.to_groups` | `[]` | Additive groups to groups |
| `fun.groups.monoid` | `[]` | Groups to monoids |
| `fun.monoids.semigroup` | `[]` | Monoids to semigroups |
| `fun.rings.additive_commutative_monoid` | `[]` | Rings to additive commutative monoids |
| `fun.additive_commutative_monoids.additive_monoid` | `[]` | Additive commutative monoids to additive monoids |
| `fun.additive_monoids.underlying` | `[]` | Additive monoids to Sets |
| `fun.rings.multiplicative_monoid` | `[]` | Rings to multiplicative monoids |
| `action:{"classifierForget":"clf.magmas.associative"}` | `[classifierForget("clf.magmas.associative", [])]` | Semigroups to magmas |
| `action:{"classifierForget":"clf.sets.binary_operation"}` | `[classifierForget("clf.sets.binary_operation", [])]` | Magmas to Sets |

For each row the map operation appends `#map`, and both registrations use the
input obtained by appending `#input` to the object operation. These concrete
addresses occur in the public `operations` and `inputForms` inventories; the two
classifier actions also occur in `edgeActions`. The derived actions use
`action_invocation` and `action_map_invocation`. Their complete descriptor is
retained both in the invocation parameter array and in the map action, including
the classifier's explicit empty parameter array.

Native scope is the existing supported ring/module carriers. A module's additive
callbacks come from its actual native module. Ring multiplication uses the
existing native multiplicative-monoid adapter. Subsequent structural steps keep
those actual callbacks, point codecs, native object, complete source receiver and
request in a `CarrierImage`. The group, monoid and additive operation readers can
consume the corresponding returned objects through their existing ports; the
group inverse reader uses the native module's existing negation callback. No new
algorithm, public wire constructor, mathematical declaration or law is supplied.

The shared map adapter retains the original callable, original source-category
endpoints, actual image endpoints and generalized domain. It therefore supports
successive module/additive/group/monoid/semigroup/magma/Set actions, as well as the
ring-additive and ring-multiplicative paths, without replacing earlier outputs
with recipes. Repeated `valueData` wrappers are inspected only by private input
readers; the complete original receiver and endpoint packets stay retained.
The existing scalar-addition native model survives ring-additive group inputs,
including wrapped symbolic inputs and their owned image results.

This bounded implementation does not add object-action readers for arbitrary
cyclic groups, automorphism groups, monoids or magmas, even where some existing
primitive operation can independently consume one of those values. Unsupported
native representations remain unsupported. Classifier-forget source structures
must be supplied through the supported actual carrier records or explicit
existing ring/module carrier descriptors. These implementation limits do not
alter any published mathematical domain.

The focused standalone run is:

```sh
python3 carrier_functor_smoke.py --contract /absolute/path/to/public-contract \
  --engine /absolute/path/to/sage/python
```

It completed 217 primary requests and three closed-owner controls. The cases
compose all ten actions, reuse an actual returned kernel inclusion through the
full carrier route, retain owned coefficient rings, consume the resulting
additive/monoid/group interfaces, and preserve whole and generalized callables.
They include wrapped ring-additive groups, native infinite scalar-callable
consumption, malformed action/parameter/endpoint packets, invalid callable
interfaces, and nested expired owners. The affected shared module, generic and
additive checks completed 122, 36 and 66 primary requests, with three and one
closed-owner controls in the module and additive checks. Assertions concern
protocol shapes and data consumption only, not arithmetic values, equality
truth, cardinality answers, laws or mathematical acceptance.

## Ordinary underlying-ring object action

The object action reads the public complete receiver request with
`construction_invocation`. This functor has no explicit declaration parameters.
It retains the same native Sage ring returned by the existing `ring` reader,
together with the complete supplied receiver and request, in one owned
`RingImage`. The existing scalar and ring-operation readers consume the result
on that connection. All nested input tokens still require their original live
owner; no source object is replaced with a familiar named ring or an action recipe.

This addition registers only `fun.commutative_rings.ring` on the already published
source-category input `cat.commutative_rings`. At the earlier public contract publication
`fcefc8ba8296bd4d771cabd8b805c9061ada7513`, the guide documents a map operation
`fun.commutative_rings.ring#map` and complete-request input
`fun.commutative_rings.ring#input`, but `api/declared-ports.json` omits both addresses.
`api/manifest.md` explicitly requires the concrete exported inventories rather
than inferring admission from the address rules. Published contract main
`5db631a34c9d4f65a535fad61b6f76af39fb56f6` now includes both addresses and resolves
that publication gap. The consumed revisions are recorded in `public-inputs.json`.
The bounded object adapter and its subsequent reader corrections add no map registration.
An `apply` packet at the unsuffixed object operation is rejected as malformed.

### Complete ring-point and callable readers

The ring-operation readers also consume complete selected carrier routes around
the supported named rings and owned `RingImage` outputs. The private scalar-codec
reader follows only the explicit supported carrier actions and retained source
data. It does not compare native parents to identify endpoints, select a route,
or rewrite the request. The published additive-commutative and
multiplicative-commutative ring paths retain their exact action descriptors and
parameters, like the previously supported additive-group and monoid paths.

Product readers retain `valueData` and supported carrier-action wrappers while
reading their actual factors. Closed point data inside a generalized callable's
graph use the point arrow's retained or declared source; that source is not
replaced by the graph's domain. Unary ring callbacks use the same complete input
point reader as binary callbacks. Composition continues to execute the supplied
constituents in their original order, with their original endpoints.

A finite owned ring image retains any actual supplied `finiteData` point keys.
The graph consumer uses those exact keys, including complete element envelopes;
it does not replace them by evaluated coordinates before lookup. If no inventory
was supplied and the retained native ring is finite, the existing Sage finite-ring
iteration supplies its complete native carrier. An unenumerated `morphismEndpoint`
still gains no inventory. Native objects and callables keep their original session.

### Owned-result composability

Public point application now follows the actual callable's retained input reader.
A complete finite graph checks its exact original key before inspecting any outer
`valueData` envelope. A native action still receives its ordinary decoded point.
Composition and mediators preserve this distinction separately for each actual
constituent, including returned owned families, explicit closed-point arrows,
comparisons and transparent structural/admission wrappers. This is private
reader metadata; the complete public endpoints, operation parameters, request
and live owner remain unchanged. No operation address selects a graph codec.

Existing direct-image, power-image/predicate and morphism-application readers
also preserve the original point until the actual inner callable consumes it.
Returned product projections retain each original component's framing.
Function-valued elements and closed points retain the complete hom-object
selection. Nested monoid and additive expressions keep the caller's selected
target. A target can expose that exact structure through an explicit supported
forward carrier view; sharing a scalar codec or a native parent does not identify
two selected structures.

`composability_smoke.py` exercises 103 requests and two closed-session owner
controls. Its independently selected chains use ordinary owned ring images as
regular-module coefficients, return restricted modules and additive monoids,
and reuse their actual point/callable data. It consumes complete returned kernel
arrows and product cones through existing ports. It also checks decorated finite
graph keys on a supplied source and on an owned ring image, mixed graph/native
mediators, inner callable readers, typed and untyped closed function points,
exact parameter and endpoint controls, nullary carrier views and nested selection
rejection. The 103-request ring, 36-request generic and
66-request additive protocol checks were rerun for the shared readers, with
their existing ownership controls. These checks assert result shape and public
framing, not arithmetic answers or mathematical correctness.

```sh
CAS_LEAF_CONTRACT_PATH=/absolute/path/to/public-contract \
CAS_SAGE_PYTHON=/absolute/path/to/sage/python \
python3 composability_smoke.py
```

### Public-envelope inventory and consumer follow-up

`envelope-coverage.json` inventories all 67 unchanged operations in nine request
frame groups and fourteen envelope families. Its per-constructor source occurrences
are static coverage clues, separate from executed checks. The consumed published
snapshot omits 25 operation addresses and 19 input addresses from this diagnostic's
manifest; their exact lists are recorded. Several belong to the specimen's earlier
additional declaration exports. The manifest is unchanged, and the inventory makes
no inference about current admission. In particular, this snapshot supplies no
`meth.two_subsets` entry or linked-functor metadata, so its historical reader is
not expanded from a guessed binding.

The published links for `meth.cardinality`, `meth.kernel` and `meth.arrow_ker`
are present. Their complete method requests now use `method_invocation`, retain
the final selected functor descriptor and consume its explicit parameters. These
owner-category registrations require an empty residual route. The kernel methods
require their supplied scalar ring; they cannot infer it from a raw receiver.
Cardinality retains the zero-parameter legacy receiver alternative.

Finite graph codomain checks read actual returned `valueData` and complete point
expressions in the declared target's codec without replacing the retained graph
outputs. Finite-map observations and native automorphism consumers use the actual
callable's point reader. Native finite indexing checks an exact retained key first,
then outer envelopes or the actual receiver's existing point decoder. Returned
automorphism directions and evaluation preserve this reader at both input and
output boundaries. Their native permutation/GAP algorithms are unchanged.

Construction maps consume the complete original typed Core arrow and both
directions, including when nested inside composition. They read the supplied
construction image's retained category and receiver, and use the actual target
image's native group. Returned maps keep that image data, selected action and
original comparison. A symbolic image recipe does not replace an owned image.
Complete cone readers also consume repeated outer `valueData` envelopes.

`envelope_smoke.py` adds 64 requests and three closed-session owner controls.
It exercises actual returned graph outputs, finite observers, returned and
composed automorphisms, typed Core maps using owned images, complete method
requests and the previously unexercised `constructionApex`, `arrowHom`,
`subobjectInclusion` and `subobjectApex` wrappers. Malformed constrained-point
framing is checked; a positive instance remains pending an actual published or
supplied constructor/type selection. No constructor is invented for coverage.

The 103-request composability, 103-request ring, 99-request completion and
74-request original protocol checks were rerun for these shared readers, with
their existing ownership controls. The original smoke's two construction-map
examples now retain the published typed Core source/target fields. All checks
concern framing, selected data, response shape and ownership; no arithmetic or
equality truth, cardinality answer, law or mathematical acceptance is asserted.

```sh
CAS_LEAF_CONTRACT_PATH=/absolute/path/to/public-contract \
CAS_SAGE_PYTHON=/absolute/path/to/sage/python \
python3 envelope_smoke.py
```

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

The public `lift_images` interface at contract `34bb8abb` supplies actual source
and comparison image data independently of the five ordered field arguments.
Both supported lifts read that metadata, retain the complete source Arrow image
for `liftInput` and the source object image for `monoLiftInput` and factors, and
check map prefixes against the actual supplied comparison endpoints. A supplied
`comparisonImage` is never replaced by a `functorAction` descriptor. When a new
forward request omits that optional image, its reply supplies an owned native
image of the actual preceding lifted object: its stored module for restriction,
or the existing change-of-values wrapper for the selected change-value action.
Backward and factor requests retain that exact endpoint. Only omission of both
metadata fields selects the public legacy recipe form.

`lift_images_smoke.py` exercises both registered lift families through their
unchanged field and factor addresses, including returned images used by another
prescribed lift, malformed stage metadata and foreign owners. It checks framing,
exact data passage and successive consumption. Its equality observations check
only the Boolean reply shape; no computed mathematical answer or law is asserted.
The existing native calculations, registration inventory and implementation
limits remain unchanged.

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

### Separate public-interface sufficiency checkpoint, 2026-10-25

This follow-up starts from published leaf commit
`1c41aa80993cc4b799893bd3165ddb64d9f80939`, after the separate V1 completion.
It uses only this specimen and its engineering material, public contract
`90d7d3f1833cff39b77024dcee2dc43213e623ad`, the supplied declaration export
SHA256 `43392ae1c6636276519113d07c4cdc3ce8f8eeead1b4336db574c57269216079`
and its provenance, and the installed engines. All 66 operation/input pairs
occur in that public export, including the derived application, component,
cartesian, construction-map and lift addresses. No absent public registration
was assigned invented semantics. No kernel implementation, protected question,
expected answer, acceptance record, downstream execution result or other
author's work was read. All registration manifests are unchanged. The separate
released-example check below also repairs one V1 scalar reader.

The independent per-pair cases exercise the applicable object/lift or callable
request forms. Callable cases retain point, whole-map, empty, distinct singleton
and two-point domains; exact supplied endpoints and ordered parameters; and
actual returned point and callable data. Object and lift cases retain complete
results, both source-context variants, all four actual preceding outputs,
factor data and subsequent point/map consumers. Every registration also has a
previously successful request containing a real retained native dependency
replayed on a fresh connection, where that old owner is unavailable.

The bounded repairs are in the existing data readers:

- Only the exact registered global-point `Fin(1)` uses the scalar convention,
  including an actual identity or terminal comparison. A distinct singleton
  descriptor retains its whole callable. The two existing singleton engineering
  examples now use explicit `finiteData` when they request the latter interface.
- Complete returned data inside `element`, finite numeral points, matrix
  callable elements and closed matrix points reach the existing native readers.
  Generalized `pointView`, `admittedPoint` and `constrainedPoint` families retain
  their original domain, target and underlying callable. Point views require
  their complete supported carrier action.
- Nested ring and monoid expressions retain their exact selected structure.
  Arrow and cone projections keep the stored map's complete endpoint fields;
  changing a field is rejected before the native map is used. Product leg
  selectors accept the published `left`/`right` constructor data. Complete
  product cones can also supply unlabelled finite graph legs at the actual
  apex and corresponding diagram factor.
- An endpoint wrapped in a structural action still supplies no graph inventory.
  Explicit `finiteData` retains its supplied keys. Supported cyclic object
  data, point envelopes and unit records are consumed completely: both unit
  fields feed the existing GAP automorphism glue, and cyclic finite inventories
  retain their original point keys and owners when native coordinates are read
  or written. The existing GAP group/homomorphism routines are unchanged.
- Non-object request packets and malformed operation fields produce framed
  errors; a subsequent valid request remains usable. Recursive ownership checks
  continue to run before every existing dispatch branch.

The closed engineering run contains 1,305 requests across all 66 pairs, including
66 fresh-connection owner replays; 69 focused data-form requests; 25 framing and
error-recovery requests; and 50 requests from the two updated local engineering
examples. The complete requests, replies, source digests, failed baseline
attempts and per-pair coverage receipt are kept outside the source repository
under `public-extension-sufficiency-checks`. These checks inspect data framing,
retention, callable reuse and error strata only. They assert no computed
mathematical answer or law, and provide no correctness or acceptance evidence.

The released contract's `api/wire-examples.md` was checked separately, without
changing its supplied descriptors or parameters. Eight concrete selected requests
were executed across the V1 and extension specimens. Two use literal illustrative
opaque tokens that were never issued by the live connection; their ordinary
`unsupported` owner outcomes are recorded separately from native routine limits.
The remaining six requests return the published result envelopes. Every one of
the guide's 32 fenced blocks has a recorded disposition: schematic requests with
unbound variables, reply/data-only examples and the unregistered square-root
request are not presented as executed concrete selected requests.

The exact modular power and addition examples exposed a V1 reader mismatch:
`element` retains the selected ring while the common request separately supplies
its scalar carrier. V1 now reads those two fields without replacing the ring,
the operation parameters or the actual payload. A retained callable inside an
element keeps its own domain and target. Twenty-nine independently selected
follow-up requests check actual result/callable reuse, composition, complete
parameter and endpoint rejection, nested ownership and framing. Their receipt
and the failed public-example baseline remain distinct from the 66-pair run.

The source still selects the same Sage/GAP computations, with no new operation,
registration or mathematical algorithm. In particular,
`fun.arrows_modules.kernel` has an implemented **object** action on the stated
rational native matrices, but its **morphism** action on a complete Arrow-category
map has no native adapter and returns `unsupported`. The method registrations
`meth.kernel` and `meth.arrow_ker` use the existing object action. This is an
ordinary implementation boundary, not a missing public type or a reason to
invent a map. The other precise native limits in the table below continue to
apply. The checks found no additional public wire type needed for these repairs.

### Bounded scalar composition closure, 2026-10-25

A separate check from published leaf `4382c4c` exercises the released scalar
examples under composition, complete typed maps, product mediators and actual
returned projections, and at global, empty, distinct singleton, finite and
infinite generalized domains. The public sources are contract `90d7d3f`'s
`api/wire-examples.md` sections on scalar expressions, whole-domain requests,
returned-data reuse and complete results; and `CasContract/Port.lean`'s element,
mediator and complete typed-map interfaces. The external receipt records pinned
source hashes, exact source lines and a citation for every request.

This independently exposed a shared reader mismatch. A selected arithmetic
owner in `element` was sometimes treated as an actual callable endpoint field,
rejecting supported typed/composed forms while a direct point path accepted a
changed scalar modulus. The reader now keeps that owner for arithmetic,
checks the existing named scalar codec context, and consumes the actual
payload's complete endpoints. Returned product/Arrow projections contribute
their stored map fields when a composition needs its intermediate context.
Actual typed and owned fields are compared exactly; native parent equality
does not identify them. Actual callable payloads keep their generalized domain
through element wrappers, and a global scalar-valued graph is read as callable
data rather than a new arithmetic expression.

The repaired run contains 116 complete requests across the extension and V1,
including fresh-connection owner controls. Its assertions cover interface
framing, selected owners and ordered parameters, full endpoint fields,
scalar/callable representation and successive actual-data uses. The two failed
baselines and all requests/replies remain outside source under
`public-scalar-closure-checks`. All seven manifests and native algorithms are
unchanged; the native limits below continue to apply. This bounded check asserts
no mathematical answer, identity or acceptance result.

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
| Kernels and bilinear lifts | The kernel functor's morphism action; kernels without an actual retained rational native matrix; general-ring submodule algorithms; forms and value modules outside the documented rational native representations. Lift evidence-family parameters, base subobject and all prior outputs are required. |
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

The module fibre-inclusion and underlying actions have a focused check:

```sh
python3 module_functor_smoke.py --contract /absolute/path/to/public-contract \
  --engine /absolute/path/to/sage/python
```

The recorded run completed 122 requests on the supplying connection and three
closed-owner controls. It covers finite portable modules and complete source
graphs, infinite rational modules, zero-dimensional vectors, owned coefficient
rings, returned kernel inclusions, scalar restrictions, whole and generalized
maps, wrapped image interfaces, previous nested symbolic carrier-map readers,
and malformed selection/endpoint controls. Existing generic and additive
protocol checks also completed 36 and 66 requests, respectively, with one
additional additive closed-owner control. These are protocol findings only.

The ordinary underlying-ring object action has a focused public-port check:

```sh
python3 ring_image_smoke.py --contract /absolute/path/to/public-contract \
  --engine /absolute/path/to/sage/python
```

The recorded run completed 48 requests on the supplying connection and two
foreign-owner controls after that connection closed. Eight object representations
cover integers, rationals, three selected moduli, a complete finite-data wrapper
and both dual-number presentations. The checks exercise actual image, callable
and scalar reuse, public wrapper reuse, malformed requests, unsupported native
data and distinct retained presentations. They assert response shapes and owner
handling only, with no computed mathematical answer or acceptance claim.

The ring-point and callable reader conformance check uses the same public helper:

```sh
python3 ring_protocol_smoke.py --contract /absolute/path/to/public-contract \
  --engine /absolute/path/to/sage/python
```

The recorded run completed 31 groups and 103 requests on the supplying connection,
followed by two foreign-owner controls after it closed. It covers all four ring
operations; complete multiplicative, additive-commutative and
multiplicative-commutative carrier descriptions; named and owned native rings;
original source point reuse; ordinary and generalized point views; typed and
composed callables; wrapped product mediators; and retained finite graph keys.
Changed callable endpoints, declaration parameters, point-view selections and
graph inventories remain rejected. These are public encoding and data-consumption
checks within the existing native implementation scope; no arithmetic result,
equation, functor law or mathematical acceptance outcome is asserted.

The actual-image lift protocol checks use the same public helper and engine:

```sh
python3 lift_images_smoke.py --contract /absolute/path/to/public-contract \
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
