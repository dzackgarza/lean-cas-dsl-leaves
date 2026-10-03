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
from sage_fixed_forms import carrier, formed, INTEGER


def module_arrow(value):
    """Lower the actual registered Arrow-constructor action without erasing it."""
    if value.get("ctor") == "arrow":
        return constructor(value, "arrow", 3)
    selected, original = constructor(value, "functorAction", 2)
    shape, edge = constructor(selected, "constructorMap", 2)
    if shape != "ctor.arrow":
        raise ValueError("no native model for this constructor action")
    scalar, values = constructor(edge, "fun.bilin_module.forget", 2)
    source, target, arrow = constructor(original, "arrow", 3)
    for endpoint in [source, target]:
        selected_form = formed(endpoint)
        if scalar != selected_form.scalar_descriptor or values != selected_form.value_descriptor:
            raise ValueError("Arrow transport changes the exact scalar or value role")
    mapped = lambda endpoint: {"ctor": "functorAction", "args": [edge, endpoint]}
    return mapped(source), mapped(target), {"ctor": "map", "args": [edge, arrow]}


def module(value):
    if value.get("ctor") == "subobjectApex":
        action, = constructor(value, "subobjectApex", 1)
        edge, receiver = constructor(action, "functorAction", 2)
        if edge != {"ctor": "fun.arrows_modules.kernel", "args": [
                {"ctor": "obj.rings.integers", "args": []}]}:
            raise ValueError("no native model for this selected subobject action")
        source, target, arrow = module_arrow(receiver)
        return linear_map(arrow, source, target).kernel(), edge, receiver
    edge, selected = constructor(value, "functorAction", 2)
    if edge.get("ctor") == "fun.bilin_module.forget":
        selected_form = carrier(value)
        return selected_form.carrier, edge, selected
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
    if ctor == "subobjectInclusion":
        action, = constructor(value, "subobjectInclusion", 1)
        if source != {"ctor": "subobjectApex", "args": [action]}:
            raise ValueError("defining inclusion changes its complete selected apex")
        edge, receiver = constructor(action, "functorAction", 2)
        if edge != {"ctor": "fun.arrows_modules.kernel", "args": [
                {"ctor": "obj.rings.integers", "args": []}]}:
            raise ValueError("unsupported defining inclusion action")
        ambient, _, _ = module_arrow(receiver)
        if target != ambient:
            raise ValueError("defining inclusion changes its full ambient object")
        coefficients = domain.basis_matrix()
    elif ctor in {"zero", "identity"}:
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
        if edge.get("ctor") == "fun.bilin_module.forget":
            original_ctor, _ = named_object(original)
            if original_ctor not in {"identity", "zero"}:
                raise ValueError("no native model for this actual fixed-value arrow")
            if constructor(original, original_ctor, 2) != [source_selected, target_selected]:
                raise ValueError("mapped formed arrow changes its exact selected endpoints")
            if original_ctor == "identity":
                if source_selected != target_selected:
                    raise ValueError("mapped identity has distinct selected forms")
                coefficients = matrix.identity(ZZ, domain.rank())
            else:
                coefficients = matrix(ZZ, domain.rank(), codomain.rank(), 0)
            return domain.hom(coefficients, codomain)
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
    source, target, arrow = module_arrow(receiver)
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


def method_kernel(receiver):
    # The actual outgoing fixture fixes the scalar role through this exact
    # registered constructor action. Other scalar models remain unsupported.
    selected, _ = constructor(receiver, "functorAction", 2)
    shape, edge = constructor(selected, "constructorMap", 2)
    if shape != "ctor.arrow" or constructor(edge, "fun.bilin_module.forget", 2)[0] != INTEGER:
        raise ValueError("no native scalar model for this transported kernel request")
    return op_kernel({"ctor": "fun.arrows_modules.kernel", "args": [
        {"ctor": "obj.rings.integers", "args": []}], "receiver": receiver})


if __name__ == "__main__":
    serve("sage", SAGE_VERSION, "0.1.0", {"fun.arrows_modules.kernel": op_kernel,
                                        "meth.kernel": method_kernel})
