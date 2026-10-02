"""The Sage power-set backend: `meth.cardinality` on `obj.sets.power_set`.

Engine: Sage (passagemath, `sage.all__sagemath_combinat`), run under `$CAS_SAGE_PYTHON` or the
workspace's `.venv/bin/python` (`engine_python`). The input `𝒫(X)` is sent to Sage's
`Subsets(S)` (`sage.combinat.subset`), where `S` is the Sage parent of the named set `X`, itself
possibly a power set; the operation goes to `Subsets(S).cardinality()`.

The result form is `lit.cardinals` (`finite n` or `aleph0`). When `X` is infinite, `|𝒫(X)|` is
uncountable and has no value in that form, so the call fails instead of answering. `S` is checked
with Sage's `Parent.is_finite()` before `Subsets(S)` is built, which does not terminate on some
infinite enumerated `S`.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_combinat")

from cas_port import serve  # noqa: E402  the leaf contract's reference port
from sage.all__sagemath_combinat import QQ, ZZ, Zmod  # noqa: E402
from sage.combinat.subset import Subsets  # noqa: E402
from sage.sets.integer_range import IntegerRange  # noqa: E402
from sage.sets.non_negative_integers import NonNegativeIntegers  # noqa: E402
from sage.sets.positive_integers import PositiveIntegers  # noqa: E402
from sage.sets.primes import Primes  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import finite_cardinal, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"

# The Sage parent of each named set accepted as `X`, from its parameters.
PARENTS = {
    "obj.sets.fin": lambda n: IntegerRange(0, numeral(n)),  # {0, …, n-1}
    "obj.sets.integers_mod": lambda n: Zmod(numeral(n)),  # Sage's Zmod(0) is ZZ, as ZMod 0 = ℤ
    "obj.sets.naturals": lambda: NonNegativeIntegers(),
    "obj.sets.positive_naturals": lambda: PositiveIntegers(),
    "obj.sets.primes": lambda: Primes(),
    "obj.sets.integers": lambda: ZZ,
    "obj.sets.rationals": lambda: QQ,
    "obj.sets.power_set": lambda x: subsets(parent(x)),
}


def subsets(S):
    """`𝒫(X)` as Sage's `Subsets(S)`, for a finite `S` only."""
    if not S.is_finite():
        raise ValueError("the power set of an infinite set is uncountable: no value of "
                         "lit.cardinals (finite n | aleph0)")
    return Subsets(S)


def parent(value):
    ctor, params = named_object(value)
    if ctor not in PARENTS:
        raise ValueError("no Sage parent for %s" % ctor)
    return PARENTS[ctor](*params)


def op_cardinality(value):
    ctor, _ = named_object(value)
    if ctor != "obj.sets.power_set":
        raise ValueError("registered on obj.sets.power_set only, not %s" % ctor)
    # Sage: Subsets(S).cardinality(), 2^|S|
    return finite_cardinal(int(parent(value).cardinality()))


serve("sage", SAGE_VERSION, ADAPTER_VERSION, {"meth.cardinality": op_cardinality})
