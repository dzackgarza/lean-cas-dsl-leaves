#!/usr/bin/env python3
"""Self-designed reader and data-retention checks; no mathematical acceptance.

Run with Sage/PassageMath and the public contract's python directory on PYTHONPATH.
This file imports computational leaf code only. It reads no other checks or tests.
"""

import copy

from sage.all import QQ
from cas_port import map_data, value_data
from engine import Engine, Scalar
from wire import Unsupported, node


def image(action, receiver):
    return node("functorAction", action, receiver)


def multiplicative_carrier(selected):
    result = image(node("fun.rings.multiplicative_monoid"), selected)
    result = image(node("fun.monoids.semigroup"), result)
    result = image(node("classifierForget", "clf.magmas.associative", []), result)
    return image(node("classifierForget", "clf.sets.binary_operation", []), result)


def additive_carrier(selected):
    result = image(node("fun.rings.additive_group"), selected)
    result = image(node("fun.additive_groups.additive_monoid"), result)
    return image(node("fun.additive_monoids.underlying"), result)


def rejected(call):
    try:
        call()
    except (ValueError, Unsupported):
        return
    raise AssertionError("a different or unsupported selected context was accepted")


def main():
    engine = Engine()
    selected = node("obj.rings.rationals")
    terminal = node("obj.sets.fin", 1)
    domain = node("obj.sets.fin", 2)
    for carrier in (multiplicative_carrier(selected), additive_carrier(selected)):
        original_carrier = copy.deepcopy(carrier)
        # Actual inline operands remain their supplied records. No arithmetic
        # result is compared with an asserted mathematical value.
        actual = [11, 13]
        point = node("element", selected, value_data(actual))
        packet = map_data(terminal, carrier, point)
        function = engine.function(packet, terminal, carrier)
        assert function.source is terminal and function.target is carrier
        assert function(0) is actual
        assert engine.intermediate(packet) is carrier
        assert engine.endpoint_view(node("morphismEndpoint", packet, "target")) is carrier

        # An opaque computational operand must remain the exact owned token.
        owned = engine.session.keep(Scalar(selected, QQ(17) / QQ(19)))
        owned_packet = map_data(terminal, carrier, node("element", selected, owned))
        owned_function = engine.function(owned_packet, terminal, carrier)
        assert owned_function(0) is owned
        rejected(lambda: Engine().function(owned_packet, terminal, carrier))

        # A generalized point retains its domain, complete endpoints and graph.
        points = [[23, 29], [31, 37]]
        graph = node("finiteGraph", [0, 1], [[0, points[0]], [1, points[1]]])
        family = map_data(domain, carrier, node("element", selected, value_data(graph)))
        general = engine.function(family, domain, carrier)
        assert general.source is domain and general.target is carrier
        assert general(0) is points[0] and general(1) is points[1]

        operation = "op.rings.neg"
        invocation = node("apply", operation, [selected], node(operation, selected),
                          domain, carrier, carrier, family)
        computed = engine.point_application(operation, invocation)
        retained = engine.session.get(computed)
        assert retained.source is domain and retained.target is carrier
        assert retained.invocation.packet is invocation
        assert retained.invocation.argument.source is domain
        assert retained.invocation.argument.target is carrier
        assert carrier == original_carrier

        # Distinct selected structures are not identified through a shared QQ
        # native parent. Nor is an unrecognized action treated as forgetting.
        different = node("obj.commutative_rings.rationals")
        rejected(lambda: engine.check_element_target(carrier, different))
        rejected(lambda: engine.check_element_target(
            image(node("fun.monoids.units"), selected), selected))
        rejected(lambda: engine.check_element_target(
            image(node("fun.rings.additive_group", selected), selected), selected))

    print("Local carrier-point reader checks completed; no mathematical acceptance was run.")


if __name__ == "__main__":
    main()
