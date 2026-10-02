"""Native Sage Module kernels, returned through released canonical subobject projections.

No formed structure is chosen here: the consumer owns the prescribed MonoLift.
Engine routines: FreeModule.hom(matrix, target).kernel(), kernel.basis_matrix().
"""
from engine_python import require_engine
require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_modules")
from cas_port import serve
from sage.all__sagemath_modules import ZZ, FreeModule
from sage.matrix.constructor import matrix
from sage.combinat.root_system.cartan_type import CartanType
from sage.version import version as SAGE_VERSION
from wire import constructor, named_object, numeral


def module(value):
    edge, selected = constructor(value, "functorAction", 2)
    scalar_type, = constructor(edge, "fun.bil_wform.carrier", 1)
    if scalar_type != {"ctor": "obj.sets.integers", "args": []}:
        raise ValueError("selected integral root lattices require the exact integer scalar type")
    ctor, args = named_object(selected)
    if ctor not in {"obj.bil_wform.root_lattice_a", "obj.bil_wform.root_lattice_a_dual"} or len(args) != 1:
        raise ValueError("no Sage Module carrier model for this selected object")
    n = numeral(args[0])
    return FreeModule(ZZ, n), edge, selected


def linear_map(value, source, target):
    domain, source_edge, source_selected = module(source)
    codomain, target_edge, target_selected = module(target)
    ctor, args = named_object(value)
    if ctor in {"zero", "identity"}:
        if constructor(value, ctor, 2) != [source, target]:
            raise ValueError("module arrow changes its selected endpoints")
        if ctor == "identity":
            if source != target:
                raise ValueError("identity has distinct selected endpoints")
            coefficients = matrix.identity(ZZ, domain.rank())
        else:
            coefficients = matrix(ZZ, domain.rank(), codomain.rank(), 0)
    elif ctor == "map":
        edge, original = constructor(value, "map", 2)
        if edge != source_edge or edge != target_edge:
            raise ValueError("mapped module arrow changes its selected carrier edge")
        n, = constructor(original, "mor.bil_wform.root_lattice_a_to_dual", 1)
        n = numeral(n)
        if source_selected != {"ctor": "obj.bil_wform.root_lattice_a", "args": [n]} or target_selected != {
                "ctor": "obj.bil_wform.root_lattice_a_dual", "args": [n]}:
            raise ValueError("named inclusion changes its selected lattice parameters")
        coefficients = CartanType(["A", n]).cartan_matrix()
    else:
        raise ValueError("no native matrix model for this module arrow")
    return domain.hom(coefficients, codomain)


def op_kernel(value):
    operation, parameters = named_object(value)
    if operation != "fun.arrows_modules.kernel" or len(parameters) != 1 or "receiver" not in value:
        raise ValueError("expected the registered kernel object action with its explicit ring")
    if parameters != [{"ctor": "obj.rings.integers", "args": []}]:
        raise ValueError("selected integral Module kernel requires the exact integer ring")
    receiver = value["receiver"]
    source, target, arrow = constructor(receiver, "arrow", 3)
    hom = linear_map(arrow, source, target)
    kernel = hom.kernel()
    # Sage constructs the complete submodule and its inclusion basis. The wire
    # projections refer to the independently declared mathematical action at
    # the exact original receiver; no engine type or proof crosses the port.
    kernel.basis_matrix()
    action = {"ctor": "functorAction", "args": [
        {"ctor": operation, "args": parameters}, receiver]}
    return {"ctor": "subobject", "args": [
        {"ctor": "subobjectApex", "args": [action]}, source,
        {"ctor": "subobjectInclusion", "args": [action]}]}


if __name__ == "__main__":
    serve("sage", SAGE_VERSION, "0.1.0", {"fun.arrows_modules.kernel": op_kernel})
