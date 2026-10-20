"""The published nonidentity F9 comparison through Sage finite-field homs.

Native routines: PolynomialRing, quotient, quotient-ring hom and the
result's polynomial coordinates. The two moduli and selected generator
translation are published in Algebra/Concrete/PolynomialPresentation.lean.
"""
from __future__ import annotations

import json

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_modules", "sage.all"))

from cas_port import point_invocation, serve, value_data
from sage.categories.homset import Hom
from sage.categories.morphism import IdentityMorphism, SetMorphism
from sage.categories.sets_cat import Sets
from sage.sets.finite_set_maps import FiniteSetMaps
from sage.version import version as SAGE_VERSION
from wire import decision, finite_cardinal, finite_graph, finite_inventory, graph_data, named_object, numeral


def descriptor(value: object) -> str:
    ctor, args = named_object(value)
    if ctor in {"functorAction", "objectPresentation"} and len(args) == 2:
        return descriptor(args[1])
    if ctor in {"finiteData", "valueData", "subobject"} and args:
        return descriptor(args[0])
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
    if ctor == "generator" and len(args) == 1:
        return F.gen(numeral(args[0]))
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


def point(value: object, selected: str, F, domain: object):
    ctor, args = named_object(value)
    if ctor == "element" and len(args) == 2:
        if descriptor(args[0]) != selected:
            raise ValueError("a point belongs to another selected field presentation")
        return arithmetic(args[1], F)
    if ctor == "pointView" and len(args) == 3:
        if descriptor(args[0]) != selected or (domain is not None and args[2] != domain):
            raise ValueError("a point view differs from the selected presentation or original domain")
        return point(args[1], selected, F, domain)
    if ctor == "admittedPoint" and len(args) == 6:
        if descriptor(args[4]) != selected or (domain is not None and args[2] != domain):
            raise ValueError("an admitted point differs from the selected presentation or original domain")
        return point(args[5], selected, F, domain)
    if ctor == "valueData" and len(args) == 1:
        if isinstance(args[0], dict):
            return point(args[0], selected, F, domain)
        return F(args[0])
    if ctor == "operationPoint" and len(args) == 5:
        raise ValueError("no native F9 point lowering for the supplied nullary operation %s" % args[0])
    if ctor == "opaqueData":
        raise ValueError("the F9 comparison has no native point owned by this opaque session token")
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


def comparison_map(source: object, target: object, inverse: bool):
    selected_source, selected_target = descriptor(source), descriptor(target)
    if (selected_source, selected_target) != (("y", "x") if inverse else ("x", "y")):
        raise ValueError("the comparison's chosen endpoints disagree with its direction")
    F, E = field(selected_source), field(selected_target)
    shift = -2 if inverse else 2
    return F.hom([E.gen() + E(shift)], E)


def arrow_endpoints(arrow: object) -> tuple[object, object] | None:
    """Read exact endpoints supplied or fixed by the published declaration."""
    ctor, args = named_object(arrow)
    if ctor == "typedMap" and len(args) == 3:
        return args[0], args[1]
    if ctor == "presentation" and len(args) == 3:
        comparison, parameters, inverse = args
        if comparison == "cmp.f9.translation" and parameters == [] and isinstance(inverse, bool):
            x = {"ctor": "obj.commutative_rings.f9_x", "args": []}
            y = {"ctor": "obj.commutative_rings.f9_y", "args": []}
            return (y, x) if inverse else (x, y)
    if ctor == "identity" and len(args) == 2:
        return args[0], args[1]
    if ctor == "map" and len(args) == 2:
        inner = arrow_endpoints(args[1])
        if inner is not None:
            return ({"ctor": "functorAction", "args": [args[0], inner[0]]},
                    {"ctor": "functorAction", "args": [args[0], inner[1]]})
    if ctor == "compose" and len(args) == 2:
        first, second = arrow_endpoints(args[0]), arrow_endpoints(args[1])
        if first is not None and second is not None and first[1] == second[0]:
            return first[0], second[1]
    return None


def native_arrow(arrow: object, source: object, target: object):
    ctor, args = named_object(arrow)
    if ctor == "typedMap" and len(args) == 3:
        if args[:2] != [source, target]:
            raise ValueError("the typed comparison map differs from the complete requested endpoints")
        callable_value = args[2]
        if isinstance(callable_value, list) or (isinstance(callable_value, dict) and
                                               callable_value.get("ctor") == "finiteGraph"):
            F, E = field(descriptor(source)), field(descriptor(target))
            rows = graph_data(arrow)
            native_rows = [(point(x, descriptor(source), F, None),
                            point(y, descriptor(target), E, None)) for x, y in rows]
            table = dict(native_rows)
            if len(table) != len(rows):
                raise ValueError("the supplied map repeats a native source point")
            lookup = FiniteSetMaps(list(table), list(dict.fromkeys(table.values()))).from_dict(table)
            return SetMorphism(Hom(F, E, Sets()), lookup)
        return native_arrow(callable_value, source, target)
    if ctor == "presentation" and len(args) == 3:
        comparison, parameters, inverse = args
        if comparison != "cmp.f9.translation" or parameters != [] or not isinstance(inverse, bool):
            raise ValueError("no native lowering for the supplied presentation descriptor")
        return comparison_map(source, target, inverse)
    if ctor == "cmp.f9.translation" and not args:
        return comparison_map(source, target, descriptor(source) == "y")
    if ctor == "identity" and args == [source, target] and source == target:
        return IdentityMorphism(Hom(field(descriptor(source)), field(descriptor(target)), Sets()))
    if ctor == "compose" and len(args) == 2:
        first, second = arrow_endpoints(args[0]), arrow_endpoints(args[1])
        if first is None or second is None:
            raise ValueError("a composite comparison lacks complete declared intermediate endpoint data")
        if first[0] != source or second[1] != target or first[1] != second[0]:
            raise ValueError("the complete comparison constituents disagree at an endpoint")
        f = native_arrow(args[0], source, first[1])
        g = native_arrow(args[1], second[0], target)
        return g * f
    if ctor == "map" and len(args) == 2:
        action, inner_arrow = args
        edge, parameters = named_object(action)
        if edge != "fun.commutative_rings.ring" or parameters != []:
            raise ValueError("no native action lowering for the supplied selected functor descriptor")
        inner = arrow_endpoints(inner_arrow)
        if inner is None:
            raise ValueError("the mapped comparison lacks its complete declared inner endpoints")
        expected_source = {"ctor": "functorAction", "args": [action, inner[0]]}
        expected_target = {"ctor": "functorAction", "args": [action, inner[1]]}
        if source != expected_source or target != expected_target:
            raise ValueError("the mapped comparison differs from its exact selected action endpoints")
        hom = native_arrow(inner_arrow, inner[0], inner[1])
        # Sage quotient-ring homomorphisms already implement the native Ring map.
        # Preserve the actual nonidentity hom while exposing its point action.
        return SetMorphism(Hom(hom.domain(), hom.codomain(), Sets()), hom)
    raise ValueError("no native lowering for the supplied comparison arrow descriptor %s" % ctor)


def invocation_payload(value: object, source: object, domain: object) -> object:
    """Read retained callable data without changing its original domain."""
    if not isinstance(value, dict):
        return value
    ctor, args = named_object(value)
    if ctor == "valueData" and len(args) == 1:
        return invocation_payload(args[0], source, domain)
    if ctor == "pointView" and len(args) == 3:
        if descriptor(args[0]) != descriptor(source) or args[2] != domain:
            raise ValueError("a point view differs from the selected source or original domain")
        return invocation_payload(args[1], source, domain)
    if ctor == "admittedPoint" and len(args) == 6:
        if descriptor(args[4]) != descriptor(source) or args[2] != domain:
            raise ValueError("an admitted point differs from the selected source or original domain")
        return invocation_payload(args[5], source, domain)
    return value


def translation(value: object) -> dict[str, object]:
    ctor, args = named_object(value)
    if ctor == "presentationApply" and len(args) == 5:
        parameters, inverse, source, target, data = args
        if parameters != [] or not isinstance(inverse, bool):
            raise ValueError("the named F9 comparison has no explicit parameters")
        hom = comparison_map(source, target, inverse)
        return encode(hom(point(data, descriptor(source), hom.domain(), None)), target)
    if ctor != "apply":
        raise ValueError("a comparison requires its published invocation envelope")
    operation, parameters, arrow, domain, source, target, data = point_invocation(
        value, "cmp.f9.translation")
    if parameters != []:
        raise ValueError("the named F9 comparison has no explicit parameters")
    hom = native_arrow(arrow, source, target)
    F = hom.domain()
    original_data = data
    inline_wrapper = isinstance(data, dict) and data.get("ctor") == "valueData"
    data = invocation_payload(data, source, domain)
    closed_domains = ({"ctor": "obj.sets.fin", "args": [1]},
                      {"ctor": "obj.sets.terminal", "args": []})
    raw_graph = isinstance(data, list) and (domain not in closed_domains or not inline_wrapper or
                (bool(data) and all(isinstance(pair, list) and len(pair) == 2 for pair in data)))
    if raw_graph or (isinstance(data, dict) and
                    data.get("ctor") in {"finiteGraph", "typedMap"}):
        if isinstance(data, dict) and data.get("ctor") == "typedMap":
            if data.get("args", [])[:2] != [domain, source]:
                raise ValueError("the supplied point graph differs from its original domain or selected source")
            rows = graph_data(data)
        else:
            rows = graph_data({"ctor": "typedMap", "args": [domain, source, data]})
        result = [[x, encode(hom(point(y, descriptor(source), F, None)), target)] for x, y in rows]
        return value_data(finite_graph([x for x, _ in rows], result))
    if domain not in closed_domains:
        raise ValueError("a non-closed comparison invocation requires its actual callable data")
    return value_data(encode(hom(point(original_data, descriptor(source), F, domain)), target))


def cardinality(value: object) -> dict[str, object]:
    inventory = finite_inventory(value)
    if inventory is not None:
        from sage.sets.finite_enumerated_set import FiniteEnumeratedSet
        return finite_cardinal(FiniteEnumeratedSet([json.dumps(p, sort_keys=True) for p in inventory]).cardinality())
    return finite_cardinal(field(descriptor(value)).cardinality())


def finiteness(value: object) -> dict[str, object]:
    inventory = finite_inventory(value)
    if inventory is not None:
        from sage.sets.finite_enumerated_set import FiniteEnumeratedSet
        return decision(bool(FiniteEnumeratedSet([json.dumps(p, sort_keys=True) for p in inventory]).is_finite()))
    return decision(bool(field(descriptor(value)).is_finite()))


serve("sage", SAGE_VERSION, "0.1.0", {
    "cmp.f9.translation": translation,
    "meth.cardinality": cardinality,
    "prop.is_finite": finiteness,
})
