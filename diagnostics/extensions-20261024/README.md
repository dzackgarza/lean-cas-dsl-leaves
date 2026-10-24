# Independent extension diagnostic

This new subtree is a computational registration specimen built from the public
contract and fresh declaration export recorded in `public-inputs.json`. Its author
did not inspect the kernel, acceptance assertions or outcomes, an existing leaf,
or another implementation report. It ships no Lean and changes no mathematical
or protocol declaration. The manifest contains 58 public operation/input pairs.

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
work. Generalized results remain owned callables, preserving native metadata and
all dependencies; no point is substituted for the complete map. Presentation
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

## Deliberate limits

The manifest addresses remain computational claims on the following precise
native input families; no category-wide address promises arbitrary native data.

| Registered family | Unsupported public inputs |
| --- | --- |
| Ring operations and integer coefficient maps | Rings other than the explicit integer, rational, modular and rational dual-number implementations; arbitrary foreign-session scalar data. |
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
The original 58 registration pairs were checked against the public exported
operation and input inventories. These are engineering checks only: no computed
equality truth, cardinality, coefficient or other mathematical answer is asserted.

## Public inputs and engine documentation

- Completion contract: published `80bf36d2131e00e78cba2c8461db7b32d98a86f4`, read at local `aa8477de4aebc83823b88ac4885225e8fc13d9c5`; tree `7de02aec2fd5d89d13683561ee92055909c28eb7`.
- Earlier completion contract consumed during review: published `c6e24107ec84481a8240bb3cae5c31f67a098a71`, local `c97110dbef75cb77d249ae3a51a95cdc8f90af19`; tree `c08793f7c1bb4843ad0f6131ad8c32d9db9c928d`.
- Original contract revision retained in the declaration export provenance: `8397df15042598f5ce9a75cdb22675c65b06fc89`.
- Fresh mathematical declaration revision: `7e848db36ff74faf62b00304cc0186a8bac641b7`.
- Fresh API SHA256: `691d2b80c2ff4fd6a0e99745beee82117a5f110a288674bb9b58fc930034c22a`.
- Additional public mathematical interface documentation: `InterfaceCompletion.md`, published revision `93e1a738`; its exact content hash is recorded in `public-inputs.json`.
- [Sage polynomial quotient rings](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_quotient_ring.html).
- [Sage ring homomorphisms](https://doc.sagemath.org/html/en/reference/rings/sage/rings/morphism.html).
- [Sage integer quotient rings and complete finite iteration](https://doc.sagemath.org/html/en/reference/finite_rings/sage/rings/finite_rings/integer_mod_ring.html).
- [Sage matrix construction](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/constructor.html) and [matrix kernels](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html).
- [Sage lazy power-series rings](https://doc.sagemath.org/html/en/reference/power_series/sage/rings/lazy_series_ring.html) and [lazy series](https://doc.sagemath.org/html/en/reference/power_series/sage/rings/lazy_series.html).
- [Sage permutation groups](https://doc.sagemath.org/html/en/reference/groups/sage/groups/perm_gps/permgroup_named.html) and [native GAP morphisms](https://doc.sagemath.org/html/en/reference/groups/sage/groups/libgap_morphism.html).
