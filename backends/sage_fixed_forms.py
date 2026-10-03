"""Native selected fixed-value formed modules from released public input data.

Engine routines: matrix multiplication and FreeQuadraticModule over ZZ.
The E8 coordinate data and negative sign are the released e8RootNumerator
and e8GramMatrix definitions, not a choice of isomorphic root presentation.
"""
from dataclasses import dataclass

from sage.all__sagemath_modules import ZZ, FreeQuadraticModule
from sage.matrix.constructor import matrix

from wire import constructor

INTEGER = {"ctor": "obj.sets.integers", "args": []}
E8 = {"ctor": "obj.integral_lattice.e8", "args": []}


@dataclass
class SelectedForm:
    descriptor: dict
    scalar_descriptor: dict
    value_descriptor: dict
    carrier: object
    value_module: object


@dataclass
class SelectedSubobject:
    descriptor: dict
    apex: SelectedForm
    ambient: SelectedForm
    inclusion_descriptor: dict
    inclusion: object


def e8_module():
    coordinates = matrix(ZZ, [
        [1, -1, -1, -1, -1, -1, -1, 1],
        [2, 2, 0, 0, 0, 0, 0, 0],
        [-2, 2, 0, 0, 0, 0, 0, 0],
        [0, -2, 2, 0, 0, 0, 0, 0],
        [0, 0, -2, 2, 0, 0, 0, 0],
        [0, 0, 0, -2, 2, 0, 0, 0],
        [0, 0, 0, 0, -2, 2, 0, 0],
        [0, 0, 0, 0, 0, -2, 2, 0]])
    gram = matrix(ZZ, -(coordinates * coordinates.transpose()) / 4)
    return FreeQuadraticModule(ZZ, 8, gram)


def formed(value):
    if value.get("ctor") == "subobjectApex":
        receiver, = constructor(value, "subobjectApex", 1)
        return lifted_subobject(receiver).apex
    edge, source = constructor(value, "functorAction", 2)
    scalar, = constructor(edge, "fun.integral_lattice.forget_form", 1)
    if scalar != INTEGER or source != E8:
        raise ValueError("no native model for this complete selected integral form")
    # This registered integral-lattice view has value module R itself.
    # Retain its separate dependent role even when its descriptor equals R.
    return SelectedForm(value, scalar, scalar, e8_module(), ZZ)


def lifted_subobject(value):
    """Use the actual prescribed restriction, retaining its full defining map."""
    from sage_module_kernels import module_arrow, linear_map
    original, receiver, lifts = constructor(value, "liftedSubobject", 3)
    if lifts != ["lift.bilin_module.restrict"]:
        raise ValueError("no native model for this complete prescribed lift route")
    action, transported = constructor(original, "functorAction", 2)
    if action != {"ctor": "fun.arrows_modules.kernel", "args": [
            {"ctor": "obj.rings.integers", "args": []}]}:
        raise ValueError("unsupported lifted subobject construction or scalar")
    transport, original_receiver = constructor(transported, "functorAction", 2)
    if original_receiver != receiver:
        raise ValueError("lift changes its actual source arrow receiver")
    source, target, arrow = module_arrow(transported)
    ambient_descriptor, _, _ = constructor(receiver, "arrow", 3)
    ambient = formed(ambient_descriptor)
    kernel = linear_map(arrow, source, target).kernel()
    # Sage restricts the ambient quadratic module along the actual kernel basis.
    # This keeps its chosen coordinates and inherited negative bilinear form.
    restricted = ambient.carrier.submodule(kernel.basis_matrix().rows())
    apex_descriptor = {"ctor": "subobjectApex", "args": [value]}
    inclusion_descriptor = {"ctor": "subobjectInclusion", "args": [value]}
    apex = SelectedForm(apex_descriptor, ambient.scalar_descriptor,
                        ambient.value_descriptor, restricted, ambient.value_module)
    inclusion = restricted.hom(restricted.basis_matrix(), ambient.carrier)
    return SelectedSubobject(value, apex, ambient, inclusion_descriptor, inclusion)


def defining_inclusion(value, source, target):
    receiver, = constructor(value, "subobjectInclusion", 1)
    selected = lifted_subobject(receiver)
    if source != selected.apex.descriptor or target != selected.ambient.descriptor:
        raise ValueError("lifted inclusion changes its complete selected endpoints")
    return selected.inclusion


def carrier(value):
    edge, source = constructor(value, "functorAction", 2)
    scalar, values = constructor(edge, "fun.bilin_module.forget", 2)
    selected = formed(source)
    if scalar != selected.scalar_descriptor or values != selected.value_descriptor:
        raise ValueError("carrier action changes its selected scalar or value module")
    return selected


def forget_form(value):
    parameters = constructor(value, "fun.integral_lattice.forget_form", 1)
    if "receiver" not in value:
        raise ValueError("selected formed view requires its complete receiver")
    result = {"ctor": "functorAction", "args": [
        {"ctor": "fun.integral_lattice.forget_form", "args": parameters},
        value["receiver"]]}
    formed(result)
    return result
