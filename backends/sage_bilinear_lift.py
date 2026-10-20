"""Published bilinear-module restriction fields over supplied finite graphs.

Sage FiniteSetMaps.from_dict, FiniteSetMaps.one and cartesian_product execute
restriction of the supplied pairing along the actual base inclusion. No law,
monicity, inverse equation or universal property is checked or reconstructed.
"""
from __future__ import annotations

import json

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_combinat", "sage.all"))

from cas_port import serve
from sage.sets.finite_set_maps import FiniteSetMaps
from sage.version import version as SAGE_VERSION
from wire import finite_data, finite_graph, finite_inventory, graph_data, named_object

LIFT = "lift.bilin_module.restrict"
FIELDS = ("obj", "hom", "forward", "backward")


def named(identifier: str, *parameters: object) -> dict[str, object]:
    return {"ctor": identifier, "args": list(parameters)}


def key(point: object) -> str:
    return json.dumps(point, sort_keys=True)


def callable_data(value: object) -> object:
    ctor, args = named_object(value) if isinstance(value, dict) else (None, [])
    if ctor == "valueData" and len(args) == 1:
        return callable_data(args[0])
    if ctor == "admittedPoint" and len(args) == 6:
        return callable_data(args[5])
    return value


def context(value: object, field: str) -> tuple[object, object, object, object, list[object]]:
    ctor, args = named_object(value)
    if ctor != "liftInput" or len(args) != 5 or args[0] != LIFT:
        raise ValueError("expected all five fields of the published restriction liftInput")
    _, action, arrow, base, outputs = args
    if not isinstance(outputs, list) or len(outputs) != FIELDS.index(field):
        raise ValueError("a lift field requires its exact preceding actual output prefix")
    edge, parameters = named_object(action)
    if edge != "fun.bilin_module.forget" or len(parameters) != 2:
        raise ValueError("restriction requires the complete selected bilinear forget action")
    arrow_ctor, arrow_args = named_object(arrow)
    base_ctor, base_args = named_object(base)
    if arrow_ctor != "arrow" or len(arrow_args) != 3:
        raise ValueError("restriction requires the complete original source Arrow")
    if base_ctor != "subobject" or len(base_args) != 3:
        raise ValueError("restriction requires the actual complete base subobject")
    return action, arrow_args[0], base_args[0], base_args[2], outputs


def native_map(graph: object):
    rows = graph_data(callable_data(graph))
    table = {key(x): key(y) for x, y in rows}
    return FiniteSetMaps(list(table), list(dict.fromkeys(table.values()))).from_dict(table)


def object_output(value: object) -> dict[str, object]:
    action, source, apex, inclusion, outputs = context(value, "obj")
    action_id, parameters = named_object(action)
    ring, values = parameters
    source_data = source
    if isinstance(source_data, dict) and source_data.get("ctor") == "finiteData":
        source_data = source_data["args"][0]
    ctor, args = named_object(source_data)
    if ctor != "obj.bilin_module.bilinear_form" or len(args) != 4:
        raise ValueError("no finite graph lowering for the supplied bilinear-module object")
    if args[0] != ring or args[2] != values:
        raise ValueError("the source bilinear module differs from the selected ring/value module")
    inclusion_rows = graph_data(inclusion)
    points = finite_inventory(apex)
    if points is None:
        points = [point for point, _ in inclusion_rows]
    if {key(x) for x, _ in inclusion_rows} != {key(x) for x in points}:
        raise ValueError("the base inclusion does not cover its actual apex inventory")
    inc = native_map(inclusion)
    pairing_data = args[3]
    while isinstance(pairing_data, dict) and pairing_data.get("ctor") == "valueData":
        pairing_data = pairing_data["args"][0]
    admitted = isinstance(pairing_data, dict) and pairing_data.get("ctor") == "admittedPoint"
    if admitted and pairing_data["args"][0] != "obj.sets.bilinear_maps":
        raise ValueError("no callable lowering for a different admitted pairing interface")
    pairing = native_map(pairing_data)
    pairs = list(engine.cartesian_product([list(map(key, points)), list(map(key, points))]))
    pulled = []
    for pair in pairs:
        x, y = pair
        if admitted:
            image_pair = key([json.loads(inc(x)), json.loads(inc(y))])
            result = json.loads(pairing(image_pair))
        else:
            # The published alias is a curried LinearMap M (LinearMap M W).
            inner = native_map(json.loads(pairing(inc(x))))
            result = json.loads(inner(inc(y)))
        pulled.append([[json.loads(x), json.loads(y)], result])
    rows = []
    for point in points:
        inner_rows = [[pair[1], result] for pair, result in pulled if pair[0] == point]
        rows.append([point, finite_graph(points, inner_rows)])
    actual_pairing = finite_graph(points, rows)
    return finite_data(named("obj.bilin_module.bilinear_form", ring, apex, values,
                             actual_pairing), points)


def map_output(value: object, field: str) -> dict[str, object]:
    action, source, apex, inclusion, outputs = context(value, field)
    obj = outputs[0]
    points = finite_inventory(obj)
    if points is None:
        raise ValueError("the actual preceding object output has no finite inventory")
    if field == "hom":
        rows = graph_data(inclusion)
        if {key(x) for x, _ in rows} != {key(x) for x in points}:
            raise ValueError("the inclusion graph differs from the actual object inventory")
        return named("typedMap", obj, source, finite_graph(points, rows))
    image = named("functorAction", action, obj)
    base_points = finite_inventory(apex)
    if base_points is None:
        base_points = [point for point, _ in graph_data(inclusion)]
    if {key(x) for x in points} != {key(x) for x in base_points}:
        raise ValueError("the actual object and base inventories differ")
    identity = FiniteSetMaps(list(map(key, points))).one()
    graph = finite_graph(points, [[p, json.loads(identity(key(p)))] for p in points])
    domain, codomain = (image, apex) if field == "forward" else (apex, image)
    return named("typedMap", domain, codomain, graph)


def hom_output(value: object) -> dict[str, object]:
    return map_output(value, "hom")


def forward_output(value: object) -> dict[str, object]:
    return map_output(value, "forward")


def backward_output(value: object) -> dict[str, object]:
    return map_output(value, "backward")


serve("sage", SAGE_VERSION, "0.1.0", {
    LIFT + "#obj": object_output,
    LIFT + "#hom": hom_output,
    LIFT + "#forward": forward_output,
    LIFT + "#backward": backward_output,
})
