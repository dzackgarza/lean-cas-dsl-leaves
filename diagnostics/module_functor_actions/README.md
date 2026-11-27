# Bounded module functor actions

This independent diagnostic leaf implements the primitive object and morphism
actions of `fun.modules.fibre_inclusion` and `fun.modules.underlying`. Its own
`leaves.json` is the only new manifest. Existing sources and manifests are kept
byte-for-byte unchanged.

The implementation is authored only from the published leaf repository at
`865df49ad0b0b133d5bcfd282f380aa213eb5fff`, the public contract at
`b805eda94aec95a7962da486c8eaeec14d34f2b2` (tree
`d87ca1ed7e18cf81373ba835a8a1e54c926f6236`), official Sage documentation, and
installed native Sage interfaces. It does not consume kernel code, downstream
questions, expected answers, acceptance assertions, or other workers' diagnostics.

## Declared ports

| Operation | Complete request input | Ordered parameters | Result data |
| --- | --- | --- | --- |
| `fun.modules.fibre_inclusion` | `fun.modules.fibre_inclusion#input` | `[R]` | Owned total-module object with the exact source object and selected ring retained |
| `fun.modules.fibre_inclusion#map` | `fun.modules.fibre_inclusion#input` | `[R]` in both required positions | Complete `typedMap` at the supplied actual images; owned native map |
| `fun.modules.underlying` | `fun.modules.underlying#input` | `[]` | Portable `finiteData(extent(...), points)` in Sets |
| `fun.modules.underlying#map` | `fun.modules.underlying#input` | `[]` in both required positions | Complete finite callable at the supplied image endpoints, or the ordinary global-point data |
| `fun.arrows_modules.kernel` | `fun.arrows_modules.kernel#input` | `[R]` | `arrow(K, X, typedMap(K, X, inclusion))` with the actual native kernel and inclusion |
| `fun.subobjects_modules.domain` | `fun.subobjects_modules.domain#input` | `[R]` | The stored source module of the supplied complete subobject |
| `fun.subobjects_modules.inclusion` | `fun.subobjects_modules.inclusion#input` | `[R]` | The supplied complete Arrow, retaining both endpoints and its actual defining map |

These are existing functor IDs in `api/declared-ports.json`. Their `#map` and
`#input` address family is published by `CasContract/Port.lean` and
`api/manifest.md` at the pinned contract revision. The checked-in inventory has
older exporter provenance and does not yet enumerate those derived addresses;
this leaf uses the newly published address rule, not a new semantic registration.
The parameter order of `mor.modules.matrix_linear_map` is `[n, K, matrix]`,
where `K` is the complete selected commutative ring. That named map is lowered
only as supplied source-map data; no new registration is added for it here.

## Native scope

The bounded slice is `obj.modules.regular(R)` and `obj.modules.vectors(R,n)`
over the published `obj.rings.integers_mod(m)` forms with `2 <= m <= 64`,
degree at most six, and at most 4096 native points. Matrix coefficients use the
matching published commutative-ring form and the existing nested finite-function
codec. Source callables are the published square matrix map, identity, or a
retained native map, including the kernel's defining inclusion. The public
`arrowHom`, `subobjectInclusion`, `subobjectApex`, chosen-subobject inclusion,
and domain/ambient descriptors can select those actual stored fields.

Native operations used:

- `Zmod` and `FreeModule` construct the private scalar ring and free module.
- `FreeModule.hom(..., side="right")` creates the supplied matrix map using
  native left matrix multiplication; `FreeModule.hom(basis, module)` constructs
  an identity when that actual descriptor is supplied.
- Native module iteration produces the entire bounded finite carrier.
- `FreeModuleMorphism.kernel()` computes a native kernel over the supported
  prime-field rings; the source module's `coerce_map_from(kernel)` supplies its
  actual native inclusion.
- Native morphism multiplication composes a supplied generalized module arrow
  with the primitive action. The retained total morphism also includes its native
  scalar identity map and its actual endpoint objects.
- Sage `FiniteSetMaps(...).from_dict(...)` consumes a supplied complete finite
  generalized point. There is no interpolation from a sample.

Prior art was checked before writing the adapter in the existing leaf helpers
`backends/engine_python.py`, `backends/wire.py`, `backends/sage_modules.py`, and
the native finite-map usage in `backends/sage_bilinear_lift.py`, plus these official
references and the installed Sage interfaces:

- [Sage free modules](https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module.html)
- [Sage free-module morphisms](https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_morphism.html)
- [Sage finite-set maps](https://doc.sagemath.org/html/en/reference/sets/sage/sets/finite_set_maps.html)

No native algorithm is reimplemented. Coordinate and matrix loops translate the
released finite-function codec. No arbitrary target operation is evaluated, no
later operation is advertised, and no inference of formal categories or laws is
made from native classes or parent equality.

## Returned data and reuse

Fibre images are connection-owned native records retaining the complete ordered
parameters and actual receiver. A kernel result retains the native submodule and
its defining native inclusion; subsequent domain, inclusion, fibre, and
underlying actions use those actual values. They do not reconstruct a kernel
from its formal recipe.

Both map actions require the seven-field public `apply` record and the complete
source `typedMap`. They retain both supplied image endpoints exactly. Whole-map
requests use the original source and its identity. A generalized total-module
argument is another actual retained native map; a generalized Sets argument is
a complete finite graph on its actual supplied domain. A non-singleton domain
is returned with its full callable, without collapsing it to a point.

The underlying object image is a complete portable Sets packet using only
`extent`, the published scalar/vector set descriptors, and `finiteData`. It has
no source functor recipe and no nested opaque dependency, even when its input
was an owned kernel. The underlying finite map likewise returns a whole graph
at the actual supplied images. Map and module data containing an opaque token
remain owned by their original connection. Tokens are unique to a live process;
a foreign or expired token reports an unavailable computation and is never
relabelled or reconstructed.

## Explicit limits

Other coefficient rings, large finite carriers, arbitrary external opaque
values, arbitrary source functions, and unsupported generalized domains return
`unsupported` for the dispatched operation. Composite-modulus kernel computation
is explicitly unsupported: installed native free-module kernel support is not
used beyond the prime-field slice. Kernel and subobject morphism actions are
not advertised by this specimen. Formal recipes without actual computed data
are not evaluated as replacement values.

The public interface script in this subtree checks framing, parameter retention,
complete supplied endpoints, owner/session handling, and whole/generalized-domain
interfaces. It records requests and replies without asserting mathematical
answers. Neither those checks nor the native-interface transcript establish
functional correctness or acceptance. Mathematical correctness remains unknown
to this author.

Run `public_interface_checks.py` with `--output` set to a dedicated output
directory and `CAS_LEAF_CONTRACT_PATH` pointing to the immutable contract. Source
the host's engine setup first, then override `PYTHONPATH` to that contract's
`python` directory. The program is launched using this subtree's manifest.
