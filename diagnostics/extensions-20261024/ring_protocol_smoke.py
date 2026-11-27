#!/usr/bin/env python3
"""Public ring-port encoding checks, without expected mathematical answers."""

import argparse
import json
import os
from pathlib import Path

from completion_smoke import (ONE, Port, identity, invoke, node, owned, payload,
                              require)


FUNCTOR = "fun.commutative_rings.ring"
OPERATIONS = ("op.rings.add", "op.rings.mul", "op.rings.neg", "op.rings.pow")
MULTIPLICATIVE = (node("fun.rings.multiplicative_monoid"), node("fun.monoids.semigroup"),
                  node("classifierForget", "clf.magmas.associative", []),
                  node("classifierForget", "clf.sets.binary_operation", []))
ADDITIVE = (node("fun.rings.additive_commutative_monoid"),
            node("fun.additive_commutative_monoids.additive_monoid"),
            node("fun.additive_monoids.underlying"))
COMMUTATIVE = (node("fun.commutative_rings.multiplicative_commutative_monoid"),
               node("fun.commutative_monoids.monoid"), *MULTIPLICATIVE[1:])


def image(source, actions):
    for action in actions:
        source = node("functorAction", action, source)
    return source


def numeral(selected, number):
    return node("element", selected, node("numeral", number))


def endpoint(arrow, side):
    return node("morphismEndpoint", arrow, side)


def scalar_shape(reply):
    value = payload(reply)
    require(isinstance(value, list) and len(value) == 2
            and all(type(item) is int for item in value) and value[1] > 0,
            "the rational result lost its public scalar-record shape")
    return value


class Checks:
    def __init__(self):
        self.completed = 0
        self.failures = []

    def run(self, label, check):
        try:
            check()
        except Exception as error:
            self.failures.append({"label": label, "kind": type(error).__name__, "message": str(error)})
        else:
            self.completed += 1


def operation_check(port, label, selected, carrier, operation):
    parameters = [selected, 3] if operation == "op.rings.pow" else [selected]
    binary = operation in {"op.rings.add", "op.rings.mul"}
    source = node("objectProduct", carrier, carrier) if binary else carrier
    argument = (node("mediator", numeral(selected, 2), numeral(selected, 5))
                if binary else numeral(selected, 2))
    scalar_shape(port.request(label + "/complete point", operation,
                             invoke(operation, parameters, ONE, source, carrier, argument)))
    actual = owned(port.request(label + "/whole callable", operation,
                                invoke(operation, parameters, source, source, carrier, identity(source))))
    raw = [[2, 3], [4, 5]] if binary else [2, 3]
    scalar_shape(port.request(label + "/reuse exact endpoints", operation,
                             invoke(operation, parameters, ONE, source, carrier, raw,
                                    node("valueData", node("typedMap", source, carrier, actual)))))


def composition_checks(port, selected, carrier):
    operation = "op.rings.neg"
    arrow = node(operation, selected)
    typed = node("typedMap", carrier, carrier, arrow)
    for index, action in enumerate((node("compose", identity(carrier), typed),
                                    node("compose", node("valueData", typed), identity(carrier)))):
        scalar_shape(port.request("composition/typed constituent " + str(index), operation,
                                 invoke(operation, [selected], ONE, carrier, carrier,
                                        numeral(selected, 4), action)))
    closed = node("point", node("compose", numeral(selected, 4), typed))
    scalar_shape(port.request("composition/closed point", operation,
                             invoke(operation, [selected], ONE, carrier, carrier, closed)))
    domain = node("finiteData", node("obj.sets.fin", 2), [0, 1])
    graph = node("typedMap", domain, carrier,
                 node("finiteGraph", [0, 1], [[0, closed], [1, closed]]))
    family = owned(port.request("composition/generalized closed-point data", operation,
                                invoke(operation, [selected], domain, carrier, carrier, graph)))
    # Application of the actual returned family forces consumption of its
    # retained graph data without asserting a scalar answer.
    scalar_shape(port.request("composition/reuse generalized callable", operation,
                             invoke(operation, [selected], ONE, domain, carrier, 0, family)))


def wrapped_product_check(port, selected, carrier):
    operation = "op.rings.add"
    source = node("valueData", node("objectProduct", carrier, carrier))
    arguments = node("mediator", numeral(selected, 2), numeral(selected, 5))
    scalar_shape(port.request("product/value-data wrapper", operation,
                             invoke(operation, [selected], ONE, source, carrier, arguments)))
    action = node("fun.sets.identity")
    target = image(carrier, [action])
    product = node("objectProduct", carrier, carrier)
    mapped_product = image(product, [action])
    mapped_arrow = node("map", action, node("typedMap", product, carrier, node(operation, selected)))
    scalar_shape(port.request("product/explicit carrier action", operation,
                             invoke(operation, [selected], ONE, mapped_product, target, arguments, mapped_arrow)))


def point_view_check(port, selected):
    original = numeral(selected, 2)
    target = selected
    for action in ADDITIVE:
        target = image(target, [action])
        view = node("pointView", target, original, ONE)
        original = node("element", target, view)
    scalar_shape(port.request("point-view/actual selected structural action", "op.rings.neg",
                             invoke("op.rings.neg", [selected], ONE, target, target, view)))


def original_point_check(port, selected, original):
    carrier = image(selected, MULTIPLICATIVE)
    scalar_shape(port.request("ordinary image/original supplied point", "op.rings.neg",
                             invoke("op.rings.neg", [selected], ONE, carrier, carrier,
                                    numeral(original, 2))))


def generalized_view_check(port, selected):
    domain = node("finiteData", node("obj.sets.fin", 2), [0, 1])
    original = node("element", selected, node("typedMap", domain, selected,
                    node("finiteGraph", [0, 1], [[0, [2, 3]], [1, [4, 5]]])))
    target = selected
    for action in ADDITIVE:
        target = image(target, [action])
        view = node("pointView", target, original, domain)
        original = node("element", target, view)
    actual = owned(port.request("point-view/complete generalized data", "op.rings.neg",
                                invoke("op.rings.neg", [selected], domain, target, target, view)))
    scalar_shape(port.request("point-view/reuse original generalized domain", "op.rings.neg",
                             invoke("op.rings.neg", [selected], ONE, domain, target, 0, actual)))


def finite_image_check(port):
    original = node("obj.commutative_rings.integers_mod", 3)
    keys = [numeral(original, number) for number in range(3)]
    keys[1] = node("valueData", keys[1])
    selected = owned(port.request("finite image/original inventory", FUNCTOR,
                                  {"ctor": FUNCTOR, "args": [],
                                   "receiver": node("finiteData", original, keys)}))
    carrier = image(selected, MULTIPLICATIVE)
    graph = node("finiteGraph", keys, [[key, numeral(selected, 2)] for key in keys])
    operation = "op.rings.neg"
    actual = owned(port.request("finite image/complete original graph keys", operation,
                                invoke(operation, [selected], carrier, carrier, carrier, graph)))
    for key in keys[:2]:
        result = payload(port.request("finite image/reuse original point key", operation,
                                      invoke(operation, [selected], ONE, carrier, carrier, key, actual)))
        require(type(result) is int, "the finite ring result lost its integer-shaped codec")
    product = node("objectProduct", carrier, carrier)
    product_keys = [[left, right] for left in keys for right in keys]
    product_graph = node("finiteGraph", product_keys,
                         [[key, [numeral(selected, 1), numeral(selected, 2)]] for key in product_keys])
    for binary in ("op.rings.add", "op.rings.mul"):
        binary_map = owned(port.request("finite image/paired original graph keys", binary,
                                        invoke(binary, [selected], product, product, carrier, product_graph)))
        result = payload(port.request("finite image/reuse paired original key", binary,
                                      invoke(binary, [selected], ONE, product, carrier,
                                             [keys[1], keys[0]], binary_map)))
        require(type(result) is int, "the binary finite ring result lost its integer-shaped codec")
    port.request("finite image/replacement graph keys", operation,
                 invoke(operation, [selected], carrier, carrier, carrier,
                        node("finiteGraph", [0, 1, 2], [[number, 2] for number in range(3)])),
                 expected="error")
    arrow = node(operation, selected)
    source, target = endpoint(arrow, "source"), endpoint(arrow, "target")
    port.request("finite endpoint/no invented inventory", operation,
                 invoke(operation, [selected], source, source, target, graph), expected="unsupported")
    native = owned(port.request("finite image/native complete carrier", FUNCTOR,
                                {"ctor": FUNCTOR, "args": [],
                                 "receiver": node("obj.commutative_rings.integers_mod", 3)}))
    native_carrier = image(native, MULTIPLICATIVE)
    native_graph = node("finiteGraph", [0, 1, 2], [[number, 2] for number in range(3)])
    complete = owned(port.request("finite image/native graph consumer", operation,
                                  invoke(operation, [native], native_carrier, native_carrier,
                                         native_carrier, native_graph)))
    value = payload(port.request("finite image/native result reuse", operation,
                                 invoke(operation, [native], ONE, native_carrier, native_carrier, 0, complete)))
    require(type(value) is int, "the native finite ring result lost its integer-shaped codec")
    mixed = node("objectProduct", carrier, native_carrier)
    mixed_keys = [[left, right] for left in keys for right in range(3)]
    mixed_graph = node("finiteGraph", mixed_keys,
                       [[key, [numeral(selected, 1), numeral(native, 2)]] for key in mixed_keys])
    mixed_map = owned(port.request("finite image/mixed retained and native product keys", "op.rings.mul",
                                   invoke("op.rings.mul", [selected], mixed, mixed, carrier, mixed_graph)))
    value = payload(port.request("finite image/reuse mixed product key", "op.rings.mul",
                                 invoke("op.rings.mul", [selected], ONE, mixed, carrier,
                                        [keys[1], 1], mixed_map)))
    require(type(value) is int, "the mixed-product ring result lost its integer-shaped codec")


def boundary_checks(port, selected, carrier, actual):
    operation = "op.rings.neg"
    shadow = owned(port.request("boundaries/separate actual image", FUNCTOR,
                                {"ctor": FUNCTOR, "args": [],
                                 "receiver": node("obj.commutative_rings.rationals")}))
    replaced = image(shadow, MULTIPLICATIVE)
    port.request("boundaries/changed returned callable endpoint", operation,
                 invoke(operation, [selected], ONE, carrier, replaced, [2, 3], actual), expected="error")
    port.request("boundaries/changed returned callable parameter", operation,
                 invoke(operation, [node("obj.rings.rationals")], ONE, carrier, carrier,
                        [2, 3], actual), expected="error")
    malformed = image(selected, [node("fun.rings.multiplicative_monoid", 0), *MULTIPLICATIVE[1:]])
    port.request("boundaries/changed action declaration parameters", operation,
                 invoke(operation, [selected], ONE, malformed, malformed, numeral(selected, 2)),
                 expected="error")
    target = selected
    original = numeral(shadow, 2)
    for action in ADDITIVE:
        target = image(target, [action])
        view = node("pointView", target, original, ONE)
        original = node("element", target, view)
    port.request("boundaries/changed point-view source selection", operation,
                 invoke(operation, [selected], ONE, target, target, view), expected="error")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"), required=False)
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"))
    arguments = parser.parse_args()
    require(bool(arguments.contract), "a published contract checkout is required")
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                       PYTHONPATH=str(Path(arguments.contract).resolve() / "python"))
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    backend = Path(__file__).resolve().with_name("backend.py")
    checks = Checks()
    with Port(backend, environment) as port:
        named = node("obj.rings.rationals")
        returned = owned(port.request("ordinary object action", FUNCTOR,
                                      {"ctor": FUNCTOR, "args": [],
                                       "receiver": node("obj.commutative_rings.rationals")}))
        checks.run("owned/original source point", lambda:
                   original_point_check(port, returned, node("obj.commutative_rings.rationals")))
        checks.run("owned/finite source inventory", lambda: finite_image_check(port))
        for kind, selected in (("named", named), ("owned", returned)):
            for route, actions in (("multiplicative", MULTIPLICATIVE), ("additive", ADDITIVE)):
                carrier = image(selected, actions)
                for operation in OPERATIONS:
                    label = kind + "/" + route + "/" + operation
                    checks.run(label, lambda label=label, selected=selected, carrier=carrier, operation=operation:
                               operation_check(port, label, selected, carrier, operation))
            carrier = image(selected, MULTIPLICATIVE)
            checks.run(kind + "/composition", lambda selected=selected, carrier=carrier:
                       composition_checks(port, selected, carrier))
            checks.run(kind + "/wrapped product", lambda selected=selected, carrier=carrier:
                       wrapped_product_check(port, selected, carrier))
            checks.run(kind + "/point view", lambda selected=selected: point_view_check(port, selected))
            checks.run(kind + "/generalized point view", lambda selected=selected:
                       generalized_view_check(port, selected))
        original = node("obj.commutative_rings.rationals")
        selected = image(original, [node(FUNCTOR)])
        carrier = image(original, COMMUTATIVE)
        for operation in OPERATIONS:
            checks.run("commutative carrier/" + operation, lambda operation=operation:
                       operation_check(port, "commutative carrier/" + operation, selected, carrier, operation))
        carrier = image(returned, MULTIPLICATIVE)
        actual = owned(port.request("boundaries/actual whole callable", "op.rings.neg",
                                    invoke("op.rings.neg", [returned], carrier, carrier, carrier,
                                           identity(carrier))))
        checks.run("retained descriptor boundaries", lambda:
                   boundary_checks(port, returned, carrier, actual))
        request_count = port.requests
    with Port(backend, environment) as foreign:
        foreign.request("ownership/closed-session ring image", "op.rings.neg",
                        invoke("op.rings.neg", [returned], ONE, carrier, carrier, [2, 3]),
                        expected="unsupported")
        foreign.request("ownership/nested returned callable", "op.rings.neg",
                        invoke("op.rings.neg", [returned], ONE, carrier, carrier, [2, 3],
                               node("valueData", node("typedMap", carrier, carrier, actual))),
                        expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"completedGroups": checks.completed, "requests": request_count,
                      "foreignOwnerRequests": foreign_requests,
                      "failures": checks.failures,
                      "scope": "public packet shapes, selected descriptors and actual returned data only"}))
    require(not checks.failures, "one or more public ring-port encoding checks failed")


if __name__ == "__main__":
    main()
