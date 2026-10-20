"""The published nonidentity F9 comparison through Sage finite-field homs.

Native routines: PolynomialRing, quotient, quotient-ring hom and the
result's polynomial coordinates. The two moduli and selected generator
translation are published in Algebra/Concrete/PolynomialPresentation.lean.
"""
from __future__ import annotations

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_modules", "sage.all"))

from cas_port import point_invocation, serve
from sage.version import version as SAGE_VERSION
from wire import decision, finite_cardinal, named_object, numeral


def descriptor(value: object) -> str:
    ctor, args = named_object(value)
    if ctor == "functorAction" and len(args) == 2:
        return descriptor(args[1])
    if ctor in {"obj.sets.f9_x", "obj.commutative_rings.f9_x"}:
        return "x"
    if ctor in {"obj.sets.f9_y", "obj.commutative_rings.f9_y"}:
        return "y"
    raise ValueError("no native field for the selected presentation %s" % ctor)


def field(selected: str):
    P = engine.PolynomialRing(engine.GF(3), "t")
    t = P.gen()
    modulus = t ** 2 + 1 if selected == "x" else t ** 2 + t + 2
    return P.quotient(modulus, names=(selected,))


def arithmetic(value: object, F):
    ctor, args = named_object(value)
    if ctor == "numeral" and len(args) == 1:
        return F(numeral(args[0]))
    if ctor == "generator" and not args:
        return F.gen()
    if ctor == "neg" and len(args) == 1:
        return -arithmetic(args[0], F)
    if ctor in {"add", "mul"} and len(args) == 2:
        left, right = (arithmetic(arg, F) for arg in args)
        return left + right if ctor == "add" else left * right
    if ctor == "operationExpression" and len(args) == 3:
        operation, parameters, operands = args
        values = [arithmetic(arg, F) for arg in operands]
        if operation == "op.rings.pow" and len(values) == 1:
            return values[0] ** numeral(parameters[-1])
        if operation == "op.rings.add" and len(values) == 2:
            return values[0] + values[1]
        if operation == "op.rings.mul" and len(values) == 2:
            return values[0] * values[1]
        if operation == "op.rings.neg" and len(values) == 1:
            return -values[0]
    raise ValueError("no native lowering for the supplied field expression %s" % ctor)


def point(value: object, selected: str, F):
    ctor, args = named_object(value)
    if ctor == "element" and len(args) == 2:
        if descriptor(args[0]) != selected:
            raise ValueError("a point belongs to another selected field presentation")
        return arithmetic(args[1], F)
    if ctor == "pointView" and len(args) == 3:
        return point(args[1], selected, F)
    if ctor == "admittedPoint" and len(args) == 6:
        return point(args[5], selected, F)
    if ctor == "valueData" and len(args) == 1:
        return F(args[0])
    raise ValueError("a comparison requires the complete selected point data")


def encode(value: object, target: object) -> dict[str, object]:
    coefficients = list(value.lift())
    coefficients += [0] * (2 - len(coefficients))
    constant = {"ctor": "numeral", "args": [int(coefficients[0])]}
    linear = {"ctor": "mul", "args": [
        {"ctor": "numeral", "args": [int(coefficients[1])]},
        {"ctor": "generator", "args": []}]}
    return {"ctor": "element", "args": [target,
        {"ctor": "add", "args": [constant, linear]}]}


def translation(value: object) -> dict[str, object]:
    ctor, args = named_object(value)
    if ctor == "presentationApply" and len(args) == 5:
        parameters, inverse, source, target, data = args
        if parameters != [] or not isinstance(inverse, bool):
            raise ValueError("the named F9 comparison has no explicit parameters")
    elif ctor == "apply":
        operation, parameters, arrow, domain, source, target, data = point_invocation(
            value, "cmp.f9.translation")
        arrow_id, arrow_parameters = named_object(arrow)
        if arrow_id != "cmp.f9.translation" or arrow_parameters or parameters:
            raise ValueError("no native lowering for the supplied comparison arrow descriptor")
        if domain != {"ctor": "obj.sets.fin", "args": [1]}:
            raise ValueError("a non-singleton comparison invocation requires pointwise data")
        inverse = descriptor(source) == "y"
    else:
        raise ValueError("a comparison requires its published invocation envelope")
    selected_source, selected_target = descriptor(source), descriptor(target)
    if (selected_source, selected_target) != (("y", "x") if inverse else ("x", "y")):
        raise ValueError("the comparison's chosen endpoints disagree with its direction")
    F, E = field(selected_source), field(selected_target)
    shift = -2 if inverse else 2
    hom = F.hom([E.gen() + E(shift)], E)
    return encode(hom(point(data, selected_source, F)), target)


def cardinality(value: object) -> dict[str, object]:
    return finite_cardinal(field(descriptor(value)).cardinality())


def finiteness(value: object) -> dict[str, object]:
    return decision(bool(field(descriptor(value)).is_finite()))


serve("sage", SAGE_VERSION, "0.1.0", {
    "cmp.f9.translation": translation,
    "meth.cardinality": cardinality,
    "prop.is_finite": finiteness,
})
