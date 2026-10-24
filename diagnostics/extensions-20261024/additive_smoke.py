#!/usr/bin/env python3
"""Standalone protocol checks for the bounded public additive capability.

Only reply framing, data shapes, complete selections and live ownership are
checked. No expected sum, equality truth or other mathematical answer is used.
"""

import json
import os
from pathlib import Path

from completion_smoke import (ONE, TRUTH, Port, equality_reply, identity,
                              invoke, node, owned, payload, require)
from generic_smoke import whole


ADD = "op.additive_monoids.add"
FUNCTOR = "fun.additive_groups.additive_monoid"
CELL = "cell.additive_groups.carrier"


def image(port, label, receiver):
    return owned(port.request(label, FUNCTOR, {"ctor": FUNCTOR, "args": [], "receiver": receiver}))


def point_shape(port, label, selected, value):
    source = node("objectProduct", selected, selected)
    reply = payload(port.request(label, "mor.sets.equality",
                                 invoke("mor.sets.equality", [selected], ONE, source, TRUTH, [value, value])))
    require(type(reply) is bool, label + ": the equality observation is not Boolean-shaped")


def addition_checks(port, label, selected, operands, whole_equality):
    carrier = node("functorAction", node("fun.additive_monoids.underlying"), selected)
    source = node("objectProduct", carrier, carrier)
    complete = whole(port, label + "/whole binary operation", ADD, [selected], source, carrier)
    result = payload(port.request(label + "/actual returned operation", ADD,
                                  invoke(ADD, [selected], ONE, source, carrier, operands, complete)))
    point_shape(port, label + "/point result shape", carrier, result)
    if whole_equality:
        equality_reply(port, label + "/complete native domain", source, carrier, complete, complete)
    nested = node("element", selected,
                  node("operationExpression", ADD, [selected],
                       [node("operationExpression", ADD, [selected], operands), result]))
    nested_result = payload(port.request(label + "/nested expression with retained operand", ADD,
                                         invoke(ADD, [selected], ONE, source, carrier, [nested, result])))
    point_shape(port, label + "/nested result shape", carrier, nested_result)
    domain = node("obj.sets.fin", 2)
    family = node("finiteGraph", [0, 1], [[0, operands], [1, [result, nested_result]]])
    generalized = owned(port.request(label + "/complete generalized domain", ADD,
                                     invoke(ADD, [selected], domain, source, carrier, family, complete)))
    equality_reply(port, label + "/generalized result shape", domain, carrier, generalized, generalized)
    composed = node("compose", identity(source), node("typedMap", source, carrier, node("valueData", complete)))
    owned(port.request(label + "/wrapped actual callable composition", ADD,
                       invoke(ADD, [selected], source, source, carrier, identity(source), composed)))
    return carrier, source, complete


def ring_checks(port):
    rational = node("obj.rings.rationals")
    rational_group = node("functorAction", node("fun.rings.additive_group"), rational)
    rational_monoid = image(port, "rational/actual additive-monoid object", rational_group)
    carrier, source, complete = addition_checks(port, "rational", rational_monoid, [[4, 3], [-5, 7]], True)
    for size in (0, 1):
        domain = node("obj.sets.fin", size)
        family = node("typedMap", domain, source, [[index, [[4, 3], [-5, 7]]] for index in range(size)])
        result = owned(port.request("rational/empty or singleton retained family", ADD,
                                     invoke(ADD, [rational_monoid], domain, source, carrier, family, complete)))
        equality_reply(port, "rational/complete small-domain result", domain, carrier, result, result)
    modulus = node("obj.rings.integers_mod", 9)
    modular_group = node("functorAction", node("fun.rings.additive_group"), modulus)
    modular_monoid = node("functorAction", node(FUNCTOR), modular_group)
    addition_checks(port, "finite modular", modular_monoid, [2, 6], True)
    dual = node("obj.commutative_rings.rational_dual_x")
    dual_group = node("functorAction", node("fun.rings.additive_group"), dual)
    dual_monoid = image(port, "dual/actual additive-monoid object", dual_group)
    point = owned(port.request("dual/original owned native operand", "mor.sets.rational_dual_x_constants",
                               invoke("mor.sets.rational_dual_x_constants", [], ONE,
                                      node("obj.sets.rationals"), node("obj.sets.rational_dual_x"), [2, 3])))
    addition_checks(port, "dual", dual_monoid, [point, point], True)
    return rational_group, rational_monoid


def module_checks(port):
    rationals = node("obj.rings.rationals")
    rational_commutative = node("obj.commutative_rings.rationals")
    forget = node("fun.commutative_rings.ring")
    target_ring = node("functorAction", forget, rational_commutative)
    base_map = node("map", forget, node("mor.commutative_rings.integer_coefficients", rational_commutative))
    original = node("obj.modules.regular", target_ring)
    module = owned(port.request("module/original owned scalar restriction", "fun.modules.reindex",
                                {"ctor": "fun.modules.reindex", "args": [base_map], "receiver": original}))
    group = node("functorAction", node("fun.modules.additive_group"), module)
    selected = image(port, "module/retain actual module owner", group)
    addition_checks(port, "owned module", selected, [[7, 4], [-3, 5]], False)
    # The native ring/module decoder is exercised at a vector carrier too. Its
    # arbitrary infinite whole-domain equality is intentionally not assumed.
    vectors = node("obj.modules.vectors", rationals, 2)
    vector_group = node("functorAction", node("fun.modules.additive_group"), vectors)
    vector_monoid = image(port, "vector/actual additive-monoid object", vector_group)
    left, right = [[0, [3, 2]], [1, [-1, 3]]], [[0, [-2, 5]], [1, [4, 1]]]
    addition_checks(port, "rational vector", vector_monoid, [left, right], False)


def routes(receiver):
    left = receiver
    for action in (node("fun.additive_groups.to_groups"), node("fun.groups.monoid"),
                   node("fun.monoids.semigroup"), node("classifierForget", "clf.magmas.associative", []),
                   node("classifierForget", "clf.sets.binary_operation", [])):
        left = node("functorAction", action, left)
    right = node("functorAction", node("fun.additive_monoids.underlying"),
                 node("functorAction", node(FUNCTOR), receiver))
    return left, right


def carrier_checks(port, group):
    left, right = routes(group)
    operation = CELL + "#component"
    for inverse in (False, True):
        source, target = (right, left) if inverse else (left, right)
        parameters = [[], group, inverse]
        arrow = node("cellComponent", CELL, [], group, inverse)
        actual = owned(port.request("carrier/whole selected comparison", operation,
                                     invoke(operation, parameters, source, source, target, identity(source), arrow)))
        equality_reply(port, "carrier/whole native response shape", source, target, actual, actual)
        result = payload(port.request("carrier/reuse actual returned comparison", operation,
                                      invoke(operation, parameters, ONE, source, target, [5, 6], actual)))
        point_shape(port, "carrier/point data shape", target, result)
    selected = node("functorAction", node(FUNCTOR), group)
    mapped = node("map", node(FUNCTOR), identity(group))
    actual = owned(port.request("functor/whole actual structural action", FUNCTOR,
                                 invoke(FUNCTOR, [], selected, selected, selected, identity(selected), mapped)))
    equality_reply(port, "functor/retained native structural map", selected, selected, actual, actual)
    malformed = [group, False]
    port.request("carrier/missing nested declaration array", operation,
                 invoke(operation, malformed, left, left, right, identity(left),
                        node("cellComponent", CELL, [], group, False)), expected="error")


def boundary_checks(port, group, selected):
    port.request("functor/unexpected declaration parameter", FUNCTOR,
                 {"ctor": FUNCTOR, "args": [group], "receiver": group}, expected="error")
    multiplicative = node("functorAction", node("fun.rings.multiplicative_monoid"), node("obj.rings.rationals"))
    carrier = node("obj.sets.rationals")
    source = node("objectProduct", carrier, carrier)
    port.request("addition/unsupported different selected structure", ADD,
                 invoke(ADD, [multiplicative], source, source, carrier, identity(source)), expected="unsupported")
    with Port(port.backend, port.environment) as foreign:
        foreign.request("addition/foreign owner remains unavailable here", ADD,
                        invoke(ADD, [selected], source, source, carrier, identity(source)), expected="unsupported")


def main():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    backend = Path(__file__).resolve().with_name("backend.py")
    with Port(backend, environment) as port:
        group, selected = ring_checks(port)
        module_checks(port)
        carrier_checks(port, group)
        boundary_checks(port, group, selected)
        print(json.dumps({"primaryConnectionRequests": port.requests, "foreignOwnerRequests": 1,
                          "checks": "public framing, complete additive selection and live result reuse only"}))


if __name__ == "__main__":
    main()
