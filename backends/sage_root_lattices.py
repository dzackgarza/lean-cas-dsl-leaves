"""Sage root-lattice operations on the released named A-family form.

Interface: released-interface-b249 registry, obj.bil_wform.root_lattice_a,
LeanCategories.Lattices.Integral.rootA (n : Nat). The input is a named object
with one numeral parameter. Cardinality and rank return lit.cardinals.

Engine routines: RootSystem(['A', n]).root_lattice(), Parent.cardinality(),
Parent.rank(), Parent.is_finite(). No engine value crosses the port.
"""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_combinat")

from cas_port import serve  # noqa: E402
from sage.all__sagemath_combinat import Infinity  # noqa: E402
from sage.combinat.root_system.root_system import RootSystem  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import aleph0, constructor, decision, finite_cardinal, numeral  # noqa: E402


def lattice(value):
    n, = constructor(value, "obj.bil_wform.root_lattice_a", 1)
    return RootSystem(["A", numeral(n)]).root_lattice()


def op_cardinality(value):
    size = lattice(value).cardinality()
    return aleph0() if size == Infinity else finite_cardinal(size)


def op_rank(value):
    return finite_cardinal(lattice(value).rank())


def op_is_finite(value):
    return decision(bool(lattice(value).is_finite()))


serve("sage", SAGE_VERSION, "0.1.0",
      {"meth.cardinality": op_cardinality, "meth.rank": op_rank,
       "prop.is_finite": op_is_finite})
