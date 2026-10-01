"""The Sage backend: `meth.cardinality` and `prop.is_finite` on named sets of the catalogue.

Engine: Sage (passagemath, `sage.all__sagemath_modules`), run under `$CAS_SAGE_PYTHON` or the
workspace's `.venv/bin/python` (`engine_python`). Each named set is sent to the Sage parent that
models it, and the operation to that parent's own routine:

* `meth.cardinality`: `Parent.cardinality()`, an integer or `+Infinity`;
* `prop.is_finite`: `Parent.is_finite()`.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_modules")

from cas_port import serve  # noqa: E402  the leaf contract's reference port
from sage.all__sagemath_modules import QQ, ZZ, Infinity  # noqa: E402
from sage.rings.cc import CC  # noqa: E402
from sage.rings.real_mpfr import RR  # noqa: E402
from sage.sets.integer_range import IntegerRange  # noqa: E402
from sage.sets.non_negative_integers import NonNegativeIntegers  # noqa: E402
from sage.sets.positive_integers import PositiveIntegers  # noqa: E402
from sage.sets.primes import Primes  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import aleph0, decision, finite_cardinal, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.2.0"

# The Sage parent of each named set, from its numeral parameters.
PARENTS = {
    "obj.sets.fin": lambda n: IntegerRange(0, numeral(n)),  # {0, …, n-1}: sage.sets.integer_range
    "obj.sets.naturals": lambda: NonNegativeIntegers(),  # sage.sets.non_negative_integers
    "obj.sets.positive_naturals": lambda: PositiveIntegers(),  # sage.sets.positive_integers
    "obj.sets.primes": lambda: Primes(),  # sage.sets.primes
    "obj.sets.integers": lambda: ZZ,  # sage.rings.integer_ring
    "obj.sets.rationals": lambda: QQ,  # sage.rings.rational_field
    "obj.sets.reals": lambda: RR,  # sage.rings.real_mpfr
    "obj.sets.complexes": lambda: CC,  # sage.rings.cc
}

# Sage's `cardinality()` answers `+Infinity` for every infinite parent, which does not say which
# infinite cardinal. It is read as `aleph0` only on the countable named sets; on the others this
# backend answers no cardinality (it is not registered there).
COUNTABLE = {"obj.sets.fin", "obj.sets.naturals", "obj.sets.positive_naturals",
             "obj.sets.primes", "obj.sets.integers", "obj.sets.rationals"}


def parent(value):
    ctor, params = named_object(value)
    if ctor not in PARENTS:
        raise ValueError("no Sage parent for %s" % ctor)
    return ctor, PARENTS[ctor](*params)


def op_cardinality(value):
    # Sage: Parent.cardinality()
    ctor, S = parent(value)
    if ctor not in COUNTABLE:
        raise ValueError("Sage's cardinality() does not distinguish infinite cardinals on %s"
                         % ctor)
    c = S.cardinality()
    return aleph0() if c == Infinity else finite_cardinal(int(c))


def op_is_finite(value):
    # Sage: Parent.is_finite()
    _, S = parent(value)
    return decision(bool(S.is_finite()))


serve("sage", SAGE_VERSION, ADAPTER_VERSION,
      {"meth.cardinality": op_cardinality, "prop.is_finite": op_is_finite})
