"""The GAP backend: `meth.cardinality` and `prop.is_finite` on `ℤ/n` and `(ℤ/n)^k`.

Engine: GAP, through Sage's libgap (passagemath-gap, `sage.all__sagemath_gap`), run under
`$CAS_GAP_PYTHON` or the workspace's `.venv/bin/python` (`engine_python`). The named sets are sent
to GAP domains, and the operation to GAP's own operation on them:

* `obj.sets.integers_mod` at `n`: `ZmodnZ(n)`, and `Integers` at `n = 0` (the catalogue's `ZMod 0`
  is `ℤ`; GAP's `ZmodnZ` takes `n > 0`);
* `obj.sets.integers_mod_power` at `(n, k)`: `FullRowModule(R, k)` over that ring;
* `meth.cardinality`: `Size`, an integer or `infinity`;
* `prop.is_finite`: `IsFinite`.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

from engine_python import require_engine

require_engine("CAS_GAP_PYTHON", "sage.all__sagemath_gap")

from cas_port import serve  # noqa: E402  the leaf contract's reference port
from sage.libs.gap.libgap import libgap  # noqa: E402

from wire import aleph0, decision, finite_cardinal, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.2.0"
GAP_VERSION = str(libgap.eval("GAPInfo.Version"))


def residue_ring(n):
    n = numeral(n)
    return libgap.Integers if n == 0 else libgap.ZmodnZ(n)


# The GAP domain of each named set, from its numeral parameters.
DOMAINS = {
    "obj.sets.integers_mod": residue_ring,
    "obj.sets.integers_mod_power": lambda n, k: libgap.FullRowModule(residue_ring(n), numeral(k)),
}


def domain(value):
    ctor, params = named_object(value)
    if ctor not in DOMAINS:
        raise ValueError("no GAP domain for %s" % ctor)
    return DOMAINS[ctor](*params)


def op_cardinality(value):
    # GAP: Size. Both named sets are countable, so GAP's `infinity` is read as aleph0.
    size = domain(value).Size()
    return aleph0() if size == libgap.infinity else finite_cardinal(int(size))


def op_is_finite(value):
    # GAP: IsFinite
    return decision(bool(domain(value).IsFinite()))


serve("gap", GAP_VERSION, ADAPTER_VERSION,
      {"meth.cardinality": op_cardinality, "prop.is_finite": op_is_finite})
