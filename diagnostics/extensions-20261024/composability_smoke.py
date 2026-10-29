#!/usr/bin/env python3
"""Owned-result and callable-reader conformance through public framed requests.

Inputs are selected from the published declarations. Checks concern packet
shape, exact selections, complete data reuse and ownership, never mathematical
answers, equalities, cardinalities or laws. No engine internals are imported.
"""

import argparse
import json
import os
from pathlib import Path

from completion_smoke import (ONE, TRUTH, Port, fields, identity, invoke, node,
                              owned, payload, require)


RING = "fun.commutative_rings.ring"
DIRECT = "mor.sets.direct_image"
ADDITIVE = "fun.additive_groups.additive_monoid"


def object_request(operation, parameters, receiver):
    return {"ctor": operation, "args": parameters, "receiver": receiver}


def numeral(selected, value):
    return node("element", selected, node("numeral", value))


def ring_carrier(selected):
    for action in (node("fun.rings.multiplicative_monoid"), node("fun.monoids.semigroup"),
                   node("classifierForget", "clf.magmas.associative", []),
                   node("classifierForget", "clf.sets.binary_operation", [])):
        selected = node("functorAction", action, selected)
    return selected


def scalar_shape(value, rational):
    value = payload(value)
    if rational:
        require(isinstance(value, list) and len(value) == 2
                and all(type(item) is int for item in value) and value[1] > 0,
                "a rational result lost its public scalar-record shape")
    else:
        require(type(value) is int, "a modular result lost its integer-shaped codec")


def ordinary_chain(port, rational):
    original = (node("obj.commutative_rings.rationals") if rational
                else node("obj.commutative_rings.integers_mod", 9))
    ring = owned(port.request("ordinary ring image", RING, object_request(RING, [], original)))
    regular = node("obj.modules.regular", ring)
    base_map = node("typedMap", ring, ring, identity(ring))
    module = owned(port.request("owned ring coefficient in reindex", "fun.modules.reindex",
                                object_request("fun.modules.reindex", [base_map], regular)))
    operation = "op.modules.scalar_action"
    scalar, value = ([2, 3], [4, 5]) if rational else (2, 4)
    source = node("objectProduct", ring, module)
    scaled = port.request("owned restricted-module scalar action", operation,
                          invoke(operation, [ring, module], ONE, source, module, [scalar, value]))
    scalar_shape(scaled, rational)
    whole = owned(port.request("whole action on returned module", operation,
                                invoke(operation, [ring, module], source, source, module, identity(source))))
    scalar_shape(port.request("reuse owned scalar action and returned data", operation,
                             invoke(operation, [ring, module], ONE, source, module,
                                    [scalar, scaled], node("valueData", node("typedMap", source, module, whole)))), rational)
    group = node("functorAction", node("fun.modules.additive_group"), module)
    additive = owned(port.request("owned module to additive monoid", ADDITIVE,
                                  object_request(ADDITIVE, [], group)))
    addition = "op.additive_monoids.add"
    sum_value = port.request("add actual returned module points", addition,
                            invoke(addition, [additive], ONE, node("objectProduct", additive, additive),
                                   additive, [scaled, scaled]))
    scalar_shape(sum_value, rational)
    scalar_shape(port.request("reuse actual additive result as module data", operation,
                             invoke(operation, [ring, module], ONE, source, module, [scalar, sum_value])), rational)
    monoid = node("functorAction", node("fun.rings.multiplicative_monoid"), ring)
    product = port.request("owned ring in selected multiplicative monoid", "op.monoids.mul",
                           invoke("op.monoids.mul", [monoid], ONE, node("objectProduct", monoid, monoid),
                                  monoid, [scaled, sum_value]))
    scalar_shape(product, rational)
    scalar_shape(port.request("consume actual multiplicative result in ring port", "op.rings.neg",
                             invoke("op.rings.neg", [ring], ONE, ring, ring, product)), rational)
    return ring, module, additive, whole


def family_checks(port, domain, points):
    ambient = node("obj.sets.fin", 2)
    power = node("obj.sets.power_set", ambient)
    parameters = [ambient, ambient, identity(ambient, typed=True)]
    graph = node("typedMap", domain, power,
                 node("finiteGraph", points, [[point, [0]] for point in points]))
    actual = owned(port.request("complete direct-image family", DIRECT,
                                invoke(DIRECT, parameters, domain, power, power, graph)))
    variants = (actual, node("valueData", node("typedMap", domain, power, actual)),
                node("compose", identity(domain, typed=True), actual),
                node("compose", node("typedMap", domain, power, actual), identity(power)))
    for arrow in variants:
        for point in points[:2]:
            subset = port.request("reuse retained exact graph key", DIRECT,
                                  invoke(DIRECT, parameters, ONE, domain, power, point, arrow))
            owned(subset)
            owned(port.request("consume actual returned subset", DIRECT,
                               invoke(DIRECT, parameters, ONE, power, power, subset)))
    owned(port.request("outer envelope around an exact key", DIRECT,
                       invoke(DIRECT, parameters, ONE, domain, power, node("valueData", points[1]), actual)))
    chained = owned(port.request("returned family through another registered action", DIRECT,
                                 invoke(DIRECT, parameters, domain, power, power, actual)))
    owned(port.request("reuse twice-returned family's original key", DIRECT,
                       invoke(DIRECT, parameters, ONE, domain, power, points[0], chained)))
    point_map = node("typedMap", ONE, domain, node("finiteGraph", [0], [[0, points[1]]]))
    closed = node("compose", point_map, node("typedMap", domain, power, actual))
    for argument in (node("point", closed), closed, node("typedMap", ONE, power, closed)):
        owned(port.request("closed evaluation retains inner readers", DIRECT,
                           invoke(DIRECT, parameters, ONE, power, power, argument)))
    wrong_parameters = [ambient, ambient, node("valueData", parameters[2])]
    port.request("owned invocation keeps exact parameter descriptor", DIRECT,
                 invoke(DIRECT, wrong_parameters, ONE, domain, power, points[0], actual), expected="error")
    port.request("owned invocation keeps exact source descriptor", DIRECT,
                 invoke(DIRECT, parameters, ONE, node("valueData", domain), power, points[0], actual), expected="error")
    return parameters, domain, power, points[0], actual


def mixed_reader_checks(port):
    selected = node("obj.sets.fin", 2)
    points = [numeral(selected, 0), node("valueData", numeral(selected, 1))]
    domain = node("finiteData", selected, points)
    graph = node("typedMap", domain, selected,
                 node("finiteGraph", points, [[points[0], 0], [points[1], 1]]))
    native = node("typedMap", domain, selected, node("mor.sets.fin_rev", 2))
    pair = node("objectProduct", selected, selected)
    actual = owned(port.request("mixed graph and native mediator", "mor.sets.equality",
                                invoke("mor.sets.equality", [selected], domain, pair, TRUTH,
                                       node("mediator", graph, native))))
    for point in points:
        result = port.request("each mediator branch keeps its reader", "mor.sets.equality",
                              invoke("mor.sets.equality", [selected], ONE, domain, TRUTH, point, actual))
        require(type(payload(result)) is bool, "the comparison result lost its Boolean shape")
    cone = port.request("product cone over decorated point data", "lim.sets.product", node("pair", domain, domain))
    apex, left, right = fields(payload(cone), "cone", 3)
    projected = node("mediator", node("compose", left, graph), node("compose", right, native))
    projected_family = owned(port.request("returned projections retain component readers", "mor.sets.equality",
                                          invoke("mor.sets.equality", [selected], apex, pair, TRUTH, projected)))
    for point in ([points[0], points[1]], node("mediator", points[1], points[0])):
        result = port.request("returned projection preserves original graph component", "mor.sets.equality",
                              invoke("mor.sets.equality", [selected], ONE, apex, TRUTH, point, projected_family))
        require(type(payload(result)) is bool, "the projected comparison lost its Boolean shape")
    whole = owned(port.request("native callable on a decorated domain", "mor.sets.fin_rev",
                               invoke("mor.sets.fin_rev", [2], domain, domain, selected, identity(domain), native)))
    for point in points:
        result = port.request("native reader still decodes owned inputs", "mor.sets.fin_rev",
                              invoke("mor.sets.fin_rev", [2], ONE, domain, selected, point, whole))
        require(type(payload(result)) is int, "the finite-point result lost its integer shape")
    closed = node("compose", node("typedMap", ONE, domain,
                                   node("finiteGraph", [0], [[0, points[1]]])),
                  node("typedMap", domain, selected, whole))
    result = port.request("comparison closed-evaluation reader", "cmp.sets.fin_reversal",
                          node("presentationApply", [2], False, selected, selected, closed))
    require(type(payload(result)) is int, "the comparison result lost its finite-point shape")
    source_power = node("obj.sets.power_set", domain)
    target_power = node("obj.sets.power_set", selected)
    owned(port.request("direct-image inner native reader", DIRECT,
                       invoke(DIRECT, [domain, selected, native], ONE, source_power, target_power, points)))
    image = node("powerObjectMap", "pow.sets", "image", [domain, selected, native])
    owned(port.request("power image inner native reader", DIRECT,
                       invoke(DIRECT, [selected, selected, identity(selected)], ONE,
                              target_power, target_power, node("point", image))))
    predicate = node("typedMap", domain, TRUTH,
                     node("finiteGraph", points, [[points[0], True], [points[1], False]]))
    transpose = node("powerObjectMap", "pow.sets", "transpose", [domain, predicate])
    owned(port.request("power transpose inner graph reader", DIRECT,
                       invoke(DIRECT, [domain, domain, identity(domain)], ONE,
                              source_power, source_power, node("point", transpose))))


def returned_record_checks(port, ring):
    module = node("obj.modules.regular", ring)
    original = node("arrow", module, module, identity(module, typed=True))
    result = port.request("owned ring in complete kernel request", "fun.arrows_modules.kernel",
                          object_request("fun.arrows_modules.kernel", [ring], original))
    kernel, retained_target, inclusion = fields(payload(result), "arrow", 3)
    owned(kernel)
    require(retained_target == module, "the returned Arrow changed its supplied target")
    point = port.request("returned kernel object in scalar action", "op.modules.scalar_action",
                         invoke("op.modules.scalar_action", [ring, kernel], ONE,
                                node("objectProduct", ring, kernel), kernel, [[2, 3], [0, 1]]))
    scalar_shape(point, True)
    parameters = [ring, kernel, module]
    selected = node("obj.sets.module_morphisms", *parameters)
    operation = "obj.sets.module_morphisms#application"
    scalar_shape(port.request("actual returned inclusion and kernel point", operation,
                             invoke(operation, parameters, ONE, node("objectProduct", selected, kernel),
                                    module, [inclusion, point])), True)
    carrier = node("functorAction", node("fun.modules.underlying"), module)
    diagram = node("pair", carrier, carrier)
    cone = port.request("complete returned product cone", "lim.sets.product", diagram)
    apex, _, _ = fields(payload(cone), "cone", 3)
    leg = node("constructionLeg", "lim.sets.product", diagram, cone, node("left"))
    owned(port.request("actual returned cone leg in direct image", DIRECT,
                       invoke(DIRECT, [apex, carrier, leg], ONE,
                              node("obj.sets.power_set", apex), node("obj.sets.power_set", carrier),
                              [[[2, 3], [4, 5]]])))


def morphism_reader_check(port, ring):
    regular = node("obj.modules.regular", ring)
    points = [node("valueData", index) for index in range(3)]
    module = node("finiteData", regular, points)
    graph = node("typedMap", module, module,
                 node("finiteGraph", points, [[point, point] for point in points]))
    parameters = [ring, module, module]
    selected = node("obj.sets.module_morphisms", *parameters)
    admission = node("admittedPoint", "obj.sets.module_morphisms", parameters, ONE,
                     node("obj.sets.maps", module, module), selected, graph)
    operation = "obj.sets.module_morphisms#application"
    hom_point = node("point", node("typedMap", ONE, selected,
                                   node("finiteGraph", [0], [[0, admission]])))
    for argument in ([admission, points[1]], node("mediator", admission, points[1]),
                     [node("element", selected, admission), points[1]], [hom_point, points[1]],
                     [node("point", node("finiteGraph", [0], [[0, admission]])), points[1]]):
        result = port.request("application preserves the actual inner graph key", operation,
                              invoke(operation, parameters, ONE, node("objectProduct", selected, module),
                                     module, argument))
        scalar_shape(result, False)


def nested_selection_checks(port, ring, additive):
    group = node("functorAction", node("fun.rings.additive_group"), ring)
    other = owned(port.request("distinct selected additive object", ADDITIVE,
                               object_request(ADDITIVE, [], group)))
    operation = "op.additive_monoids.add"
    nested = node("operationExpression", operation, [other], [[2, 3], [4, 5]])
    for datum in (nested, node("element", other, nested)):
        port.request("nested additive selection is retained", operation,
                     invoke(operation, [additive], ONE, node("objectProduct", additive, additive),
                            additive, [datum, [2, 3]]), expected="error")
    first = node("functorAction", node("fun.rings.multiplicative_monoid"), ring)
    carrier = ring_carrier(ring)
    nullary = node("operationPoint", "op.monoids.one", [first], identity(ONE), ONE, first)
    scalar_shape(port.request("nullary selected structure keeps its carrier view", "op.monoids.mul",
                             invoke("op.monoids.mul", [first], ONE, node("objectProduct", carrier, carrier),
                                    carrier, [node("element", first, nullary), [2, 3]])), True)
    # Select two distinct retained ring images with the same native scalar codec.
    other_ring = owned(port.request("second ordinary ring image", RING,
                                    object_request(RING, [], node("obj.commutative_rings.rationals"))))
    second = node("functorAction", node("fun.rings.multiplicative_monoid"), other_ring)
    nested = node("element", second, node("operationExpression", "op.monoids.mul", [second],
                                           [[2, 3], [4, 5]]))
    port.request("nested monoid selection is retained", "op.monoids.mul",
                 invoke("op.monoids.mul", [first], ONE, node("objectProduct", first, first),
                        first, [nested, [2, 3]]), expected="error")
    nullary = node("operationPoint", "op.monoids.one", [second], identity(ONE), ONE, second)
    port.request("nested nullary selection is retained", "op.monoids.mul",
                 invoke("op.monoids.mul", [first], ONE, node("objectProduct", carrier, carrier),
                        carrier, [node("element", second, nullary), [2, 3]]), expected="error")
    nullary = node("operationPoint", "op.monoids.one", [second], identity(ONE), ONE, first)
    port.request("nullary parameter and selected structure must agree", "op.monoids.mul",
                 invoke("op.monoids.mul", [first], ONE, node("objectProduct", carrier, carrier),
                        carrier, [node("element", first, nullary), [2, 3]]), expected="error")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"))
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"))
    arguments = parser.parse_args()
    require(bool(arguments.contract), "a published contract checkout is required")
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                       PYTHONPATH=str(Path(arguments.contract).resolve() / "python"))
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    backend = Path(__file__).resolve().with_name("backend.py")
    with Port(backend, environment) as port:
        ordinary_chain(port, False)
        ring, module, additive, scalar_action = ordinary_chain(port, True)
        original = node("obj.commutative_rings.integers_mod", 3)
        points = [numeral(original, index) for index in range(3)]
        points[1] = node("valueData", points[1])
        finite = node("finiteData", original, points)
        image = owned(port.request("ordinary image retains actual source inventory", RING,
                                   object_request(RING, [], finite)))
        family_checks(port, finite, points)
        parameters, domain, power, point, actual = family_checks(port, ring_carrier(image), points)
        mixed_reader_checks(port)
        returned_record_checks(port, ring)
        morphism_reader_check(port, image)
        nested_selection_checks(port, ring, additive)
        requests = port.requests
    with Port(backend, environment) as foreign:
        foreign.request("closed-session nested ring and module owners", "op.modules.scalar_action",
                        invoke("op.modules.scalar_action", [ring, module], ONE,
                               node("objectProduct", ring, module), module, [[2, 3], [4, 5]], scalar_action),
                        expected="unsupported")
        foreign.request("closed-session nested family owners", DIRECT,
                        invoke(DIRECT, parameters, ONE, domain, power, point,
                               node("valueData", node("typedMap", domain, power, actual))), expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"requests": requests, "foreignOwnerRequests": foreign_requests,
                      "scope": "public owned-result chains, exact callable readers, selected framing and result shapes"}))


if __name__ == "__main__":
    main()
