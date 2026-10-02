"""Sage root-lattice operations on the released named A-family form.

Interface: released-interface-b249 registry, obj.bil_wform.root_lattice_a and
obj.bil_wform.root_lattice_a_dual, the public rootA/rootADual declarations
with parameter (n : Nat). Cardinality and rank return lit.cardinals.

Engine routines: RootSystem(['A', n]).root_lattice(), Parent.cardinality(),
Parent.rank(), Parent.is_finite(); the A-family dual uses weight_lattice().
No engine value crosses the port.
"""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_combinat")

from cas_port import serve  # noqa: E402
from sage.all__sagemath_combinat import Infinity  # noqa: E402
from sage.combinat.root_system.root_system import RootSystem  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import aleph0, decision, finite_cardinal, named_object, numeral  # noqa: E402


def lattice(value):
    ctor, args = named_object(value)
    if ctor == "obj.integral_lattice.e8":
        if args:
            raise ValueError("E8 has no explicit parameters")
        return RootSystem(["E", 8]).root_lattice()
    routines = {"obj.bil_wform.root_lattice_a": "root_lattice",
                "obj.bil_wform.root_lattice_a_dual": "weight_lattice"}
    if ctor not in routines or len(args) != 1:
        raise ValueError("expected a released A-family object with one numeral")
    root_system = RootSystem(["A", numeral(args[0])])
    return getattr(root_system, routines[ctor])()


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
