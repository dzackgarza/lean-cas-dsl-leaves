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
from sage.combinat.root_system.cartan_type import CartanType  # noqa: E402
from sage.modules.free_module import FreeModule  # noqa: E402
from sage.rings.integer_ring import ZZ  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import aleph0, constructor, decision, finite_cardinal, named_object, numeral  # noqa: E402
from sage_fixed_forms import e8_module, formed, carrier, forget_form  # noqa: E402


def lattice(value):
    ctor, args = named_object(value)
    if ctor == "obj.integral_lattice.e8":
        if args:
            raise ValueError("E8 has no explicit parameters")
        return e8_module()
    routines = {"obj.bil_wform.root_lattice_a": "root_lattice",
                "obj.bil_wform.root_lattice_a_dual": "weight_lattice"}
    if ctor not in routines or len(args) != 1:
        raise ValueError("expected a released A-family object with one numeral")
    root_system = RootSystem(["A", numeral(args[0])])
    return getattr(root_system, routines[ctor])()


def underlying_module(value):
    underlying, total = constructor(value, "functorAction", 2)
    if underlying != {"ctor": "fun.modules.underlying", "args": []}:
        raise ValueError("expected the exact zero-parameter Module underlying edge")
    inclusion, fibre = constructor(total, "functorAction", 2)
    if inclusion != {"ctor": "fun.modules.fibre_inclusion", "args": [
            {"ctor": "obj.rings.integers", "args": []}]}:
        raise ValueError("no native module model for this selected scalar ring")
    carrier, formed = constructor(fibre, "functorAction", 2)
    if carrier.get("ctor") == "fun.bilin_module.forget":
        from sage_fixed_forms import carrier as fixed_carrier
        return fixed_carrier(fibre).carrier
    if carrier != {"ctor": "fun.bil_wform.carrier", "args": [
            {"ctor": "obj.sets.integers", "args": []}]}:
        raise ValueError("no native formed-module carrier model for this exact edge")
    return canonical_quotient(formed) if formed.get("ctor") == "limitApex" else lattice(formed)


def parent(value):
    ctor, _ = named_object(value)
    if ctor == "subobjectApex":
        return formed(value).carrier
    if ctor == "functorAction":
        edge, _ = constructor(value, "functorAction", 2)
        if edge.get("ctor") == "fun.integral_lattice.forget_form":
            return formed(value).carrier
        if edge.get("ctor") == "fun.bilin_module.forget":
            return carrier(value).carrier
        return underlying_module(value)
    return canonical_quotient(value) if ctor == "limitApex" else lattice(value)


def op_cardinality(value):
    size = parent(value).cardinality()
    return aleph0() if size == Infinity else finite_cardinal(size)


def op_rank(value):
    return finite_cardinal(lattice(value).rank())


def op_is_finite(value):
    return decision(bool(parent(value).is_finite()))


def a_quotient(diagram):
    inclusion, zero = constructor(diagram, "parallelPair", 2)
    n, = constructor(inclusion, "mor.bil_wform.root_lattice_a_to_dual", 1)
    n = numeral(n)
    source = {"ctor": "obj.bil_wform.root_lattice_a", "args": [n]}
    target = {"ctor": "obj.bil_wform.root_lattice_a_dual", "args": [n]}
    if constructor(zero, "zero", 2) != [source, target]:
        raise ValueError("cokernel zero arrow changes the selected lattice endpoints")
    gram = CartanType(["A", n]).cartan_matrix()
    # In the chosen dual basis, the inclusion is the Cartan Gram map.
    # Sage owns the row-module and quotient computations.
    return FreeModule(ZZ, gram.nrows()).quotient(gram.row_module())


def canonical_quotient(value):
    operation, diagram = constructor(value, "limitApex", 2)
    if operation != "colim.bil_w_form.cokernel":
        raise ValueError("no Sage quotient translation for this canonical apex")
    return a_quotient(diagram)


def op_cokernel(diagram):
    # Construct the engine quotient, then raise it in the declared canonical
    # presentation. These are references to independently registered data,
    # not engine objects or a leaf proof of a universal property.
    a_quotient(diagram)
    operation = "colim.bil_w_form.cokernel"
    apex = {"ctor": "limitApex", "args": [operation, diagram]}
    projection = {"ctor": "limitLeg", "args": [operation, diagram, {"ctor": "one", "args": []}]}
    return {"ctor": "cocone", "args": [apex, projection]}


serve("sage", SAGE_VERSION, "0.1.0",
      {"meth.cardinality": op_cardinality, "meth.rank": op_rank,
       "prop.is_finite": op_is_finite, "colim.bil_w_form.cokernel": op_cokernel,
       "fun.integral_lattice.forget_form": forget_form})
