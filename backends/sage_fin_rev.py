"""Sage Permutation realization of the named Fin reversal morphism."""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all")

from cas_port import serve  # noqa: E402
from sage.combinat.permutation import Permutation  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402
from wire import named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"


def op_fin_rev(value):
    ctor, args = named_object(value)
    if ctor != "mor.sets.fin_rev" or len(args) != 1:
        raise ValueError("expected mor.sets.fin_rev with one parameter")
    n = numeral(args[0])
    p = Permutation(list(range(n, 0, -1)))
    return [[i, int(p(i + 1)) - 1] for i in range(n)]


serve("sage", SAGE_VERSION, ADAPTER_VERSION, {"mor.sets.fin_rev": op_fin_rev})
