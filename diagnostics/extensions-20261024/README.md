# Independent extension diagnostic

This new subtree is a computational registration specimen built from the public
contract and the fresh declaration export recorded in `public-inputs.json`. Its
author did not inspect the kernel, acceptance assertions, an existing leaf, or
another implementation report. It ships no Lean and changes no mathematical or
protocol declaration.

The backend delegates arithmetic to Sage 10.8: polynomial quotient rings and their
selected homomorphisms, exact rational scalars, and native vector and matrix
operations. Native results and complete formed objects remain owned by the live
connection. A formed object retains its module operations, its actual pairing,
and its complete selected input context.

## Implemented registration scope

| Operation | Manifest input | Native implementation |
| --- | --- | --- |
| `cmp.rational_dual.translation` | Same complete-request address | The selected homomorphism between the two published rational dual-number presentations, in either orientation. |
| `op.rings.add`, `mul`, `pow`, `neg` | `cat.rings` | Integer, rational and the two named rational dual-number rings, including their declared carrier views. Other selected rings return `unsupported`. |
| `mor.sets.rational_dual_x_constants`, `rational_dual_y_constants` | Each complete-request address | Rational coefficient inclusions in the selected quotient presentation. |
| `mor.modules.rectangular_linear_map`, `row_linear_map` | Each complete-request address | The actual matrix from the complete nested callable data, at all supplied dimensions and the supported selected coefficient ring. |
| `mor.bilin_module.degenerate_plane_map`, `degenerate_plane_cone`, `degenerate_plane_paired_cone` | Each complete-request address | The published rational linear actions, evaluated on the supplied vector data. |
| `mor.sets.bilin_module_pairing` | Same complete-request address | The four documented named rational forms and actual native lifted forms. |
| `lift.bilin_module.restrict#obj`, `hom`, `forward`, `backward`, `factor` | `lift.bilin_module.restrict#input` | Callable pullback of the selected pairing along the actual supplied base inclusion. |
| `lift.bilin_module.change_value_restriction#obj`, `hom`, `forward`, `backward`, `factor` | `lift.bilin_module.change_value_restriction#input` | The selected change-value lift, retaining all four evidence-family parameters and the actual preceding outputs. |
| `mor.sets.equality` | Same complete-request address | Engine equality on supported exact scalar, product and module point data. |

Category registration does not claim a native implementation for every possible
object. An unsupported selected object or callable produces the public
`unsupported` reply at the original operation address; it never chooses a
replacement structure.

## Complete data handling

The implementation reads both endpoints of every `typedMap`, preserves actual
finite inventories, rejects partial or duplicate-key graphs, and keeps opaque
tokens on their supplying connection. Composition uses categorical order and
retains its selected intermediate descriptor. Common point invocations retain
their domain; a finite generalized point is evaluated pointwise, while an
unbounded supported callable remains native and opaque.

Published `element`, arithmetic operation expressions, `point`, `pointView`,
admitted and constrained points, generators, selected presentations, typed
composition, mediators and a deliberately explicit set of structural functor
actions are consumed directly. Nonidentity presentation comparisons are actual
Sage homomorphisms.

`arrowHom` and `subobjectInclusion` consume the defining map of a complete returned
record. `liftedSubobject` retains each selected step and its actual four outputs.
`constructionField` reads an actual ordered data port of a complete cone or
cocone. The supported finite-set pullback creation wrapper retains its source
diagram; other creation actions are implementation gaps.

The two lift implementations consume the actual source object, complete base
subobject, selection parameters, and every supplied earlier output. Their object
reply contains a native module with a callable pulled-back pairing. Their map
replies contain the exact required endpoints and live callables. The separate
factor consumes both actual typed input maps and returns the declared underlying
base-map action. No inverse equation, compatibility proof, or universal-property
certificate is manufactured.

## Running the specimen

The manifest is this directory's `leaves.json`; the process working directory is
this directory. The host provides the public `cas_port` helper on `PYTHONPATH`.
Set `CAS_SAGE_PYTHON` to a Python executable containing Sage, or run the manifest
with such a Python already selected. The launcher respects an existing `DOT_SAGE`
and otherwise creates a temporary writable directory for Sage startup.

For a standalone protocol diagnostic:

```sh
CAS_SAGE_PYTHON=/absolute/path/to/sage/python \
PYTHONPATH=/absolute/path/to/public-contract/python \
python3 smoke.py
```

`smoke.py` uses independently chosen input packets and checks startup, framing,
request identity, supported packet consumption and live opaque reuse. It contains
no expected mathematical result and does not import or invoke the acceptance
suite or kernel. Correctness remains a separate responsibility of the caller.

## Public inputs

- Contract commit: `8397df15042598f5ce9a75cdb22675c65b06fc89`.
- Mathematical declaration commit: `7e848db36ff74faf62b00304cc0186a8bac641b7`.
- Fresh declaration export SHA256:
  `691d2b80c2ff4fd6a0e99745beee82117a5f110a288674bb9b58fc930034c22a`.
- [Sage polynomial quotient rings](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_quotient_ring.html).
- [Sage ring homomorphisms](https://doc.sagemath.org/html/en/reference/rings/sage/rings/morphism.html).
- [Sage matrix construction](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/constructor.html).

The scope above has enough public mathematical and wire information to implement
it without contract edits. Unlisted mathematical actions and unsupported native
object representations are implementation limits, not requests for a new wire
format.
