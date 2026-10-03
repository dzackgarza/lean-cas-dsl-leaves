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
    edge, source = constructor(value, "functorAction", 2)
    scalar, = constructor(edge, "fun.integral_lattice.forget_form", 1)
    if scalar != INTEGER or source != E8:
        raise ValueError("no native model for this complete selected integral form")
    # This registered integral-lattice view has value module R itself.
    # Retain its separate dependent role even when its descriptor equals R.
    return SelectedForm(value, scalar, scalar, e8_module(), ZZ)


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
