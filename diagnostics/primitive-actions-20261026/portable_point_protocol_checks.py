#!/usr/bin/env python3
"""Public-input codec, shape and ownership controls for the same four ports.

These are self-designed engineering controls. No arithmetic result, Boolean
answer, mathematical law, or correctness/acceptance outcome is asserted.
"""

import argparse
import copy
import os
from pathlib import Path
import subprocess
import tempfile

from protocol_checks import Connection, EQUALITY, MONOID, MULTIPLY, RING, node
from multiplication_protocol_checks import invocation, raw, success
from point_observation_protocol_checks import boolean, callable_shape, equality, monoid_carrier


def element(owner, expression):
    return node("element", owner, expression)


def fragments(terminal, target, owner, datum):
    selected = element(owner, datum)
    graph = node("typedMap", terminal, target, [[0, datum]])
    composite = node("compose", graph, node("identity", target, target))
    return [datum, node("valueData", datum), selected, node("point", selected),
            node("typedMap", terminal, target, selected), graph, node("point", graph),
            element(owner, graph), element(owner, node("point", graph)),
            node("typedMap", terminal, target, node("point", selected)),
            node("point", composite), element(owner, node("point", composite))]


def multiplication(selected, terminal, target, argument):
    packet = invocation(selected, terminal, argument)
    packet["args"][4] = node("objectProduct", target, target)
    packet["args"][5] = target
    return packet


def point_shapes(connection, terminal, target, owner, datum, monoid=None):
    product = node("objectProduct", target, target)
    for fragment in fragments(terminal, target, owner, datum):
        # Direct ordered fields and graph images reach the same point codec.
        for argument in ([fragment, datum],
                         node("typedMap", terminal, product, [[0, [fragment, datum]]])):
            boolean(connection.invoke(EQUALITY, equality(target, terminal, argument)))
            if monoid is not None:
                result = success(connection.invoke(MULTIPLY,
                                 multiplication(monoid, terminal, target, argument)))
                assert result["ctor"] == "opaqueData"
        if isinstance(fragment, dict) and fragment["ctor"] != "valueData":
            pair = node("mediator", fragment, element(owner, datum))
            boolean(connection.invoke(EQUALITY, equality(target, terminal, pair)))


def retention_controls():
    """Inspect retained source objects and packet identity, never native answers."""
    from primitive_actions import Actions, PointResult
    from monoid_multiplication import Multiplication
    from point_calls import wire

    actions = Actions()
    terminal = node("obj.sets.fin", 1)
    origin = node("obj.rings.rationals")
    creating = {"ctor": RING, "args": [], "receiver": origin}
    semiring = actions.run(RING, creating)
    selected = actions.run(MONOID, {"ctor": MONOID, "args": [], "receiver": semiring})
    carrier, structure = raw(selected)
    endpoint = node("morphismEndpoint", node(MULTIPLY, selected), "target")
    selected_set = node("functorAction", node("fun.sets.identity"), endpoint)
    literal = [-11, 23]
    fragment = element(selected, node("point", node("typedMap", terminal, selected_set, [[0, literal]])))
    argument = [fragment, element(selected, structure[1])]
    packet = multiplication(selected, terminal, selected_set, argument)
    result = actions.run(MULTIPLY, packet)
    native = actions.session.get(result)
    assert isinstance(native.context, PointResult)
    retained = native.context.invocation
    assert retained.packet is packet and retained.parameters is packet["args"][1]
    assert retained.packet["args"][6] is argument
    assert retained.argument.source is terminal and retained.argument.target is packet["args"][4]
    original = actions.session.get(native.context.data).context
    assert original.fragment is packet["args"][2]
    assert original.target is selected_set and original.parameters[0] is selected
    reader = Multiplication(actions.session, packet)
    view, contexts = reader.endpoint_context(selected_set)
    assert view is carrier
    assert any(context is selected for context in contexts)
    assert any(context is endpoint for context in contexts)
    assert any(context is selected_set for context in contexts)
    point = reader.point_function(fragment, terminal, selected_set)
    assert point.source is terminal and point.target is selected_set
    assert point(0) is literal
    field = reader.point_function(element(selected, node("point", structure[1])), terminal, selected_set)
    assert field(0) is structure[1]
    assert actions.session.get(structure[1]).request is creating

    # An exact native record field can be used without manufacturing an arrow
    # under the generic multiplication address or changing its currying.
    function_target = node("obj.sets.maps", carrier, carrier)
    actual = reader.field_callable(structure[0], carrier, function_target)
    partial = actual(structure[1])
    retained_partial = actions.session.get(partial)
    assert isinstance(retained_partial.value, wire.Callable)
    assert retained_partial.context.field is structure[0]
    assert retained_partial.context.operands[0] is structure[1]
    assert retained_partial.context.packet is packet

    from set_equality import Equality
    from point_calls import point_producer
    scalar_set = node("obj.sets.rationals")
    literal_fragment = element(origin, node("numeral", 4))
    literal_packet = equality(scalar_set, terminal, [literal_fragment, literal])
    observation = Equality(actions.session, literal_packet)
    literal_token = observation.point_context(scalar_set).data(literal_fragment)
    literal_native, _ = point_producer(actions.session, literal_token)
    assert literal_native.request is literal_packet
    assert literal_native.context.fragment is literal_fragment
    assert literal_native.context.carrier is scalar_set


def run(environment):
    first = Connection(environment)
    terminal, family_domain = node("obj.sets.fin", 1), node("obj.sets.fin", 2)
    try:
        # Portable originals use their public scalar records; no previous
        # computation or opaque native point is needed for these forms.
        for selected, datum in [(node("obj.sets.integers"), -17),
                                (node("obj.sets.naturals"), 9),
                                (node("obj.sets.rationals"), [-7, 19]),
                                (node("obj.sets.integers_mod", 3), 2),
                                (node("obj.sets.fin", 4), 1),
                                (node("obj.sets.truth_values"), False)]:
            point_shapes(first, terminal, selected, selected, datum)
        for owner, selected, datum in [(node("obj.rings.integers"), node("obj.sets.integers"), -17),
                                       (node("obj.semirings.naturals"), node("obj.sets.naturals"), 9),
                                       (node("obj.rings.rationals"), node("obj.sets.rationals"), [-7, 19]),
                                       (node("obj.rings.integers_mod", 3), node("obj.sets.integers_mod", 3), 2)]:
            point_shapes(first, terminal, selected, owner, datum)
            boolean(first.invoke(EQUALITY, equality(selected, terminal,
                                  [element(owner, node("numeral", 4)), datum])))
        finite_set = node("obj.sets.fin", 4)
        for image in fragments(terminal, finite_set, finite_set, 1):
            closed = node("typedMap", terminal, finite_set, node("finiteGraph", [0], [[0, image]]))
            boolean(first.invoke(EQUALITY, equality(finite_set, terminal, [closed, 2])))

        origin = node("obj.rings.rationals")
        semiring = success(first.call(RING, origin))
        monoid = success(first.call(MONOID, semiring))
        carrier, structure = raw(monoid)
        datum = [-11, 23]
        for owner in (origin, carrier, monoid):
            point_shapes(first, terminal, carrier, owner, datum, monoid)

        endpoint = node("morphismEndpoint", node(MULTIPLY, monoid), "target")
        selected_set = monoid_carrier(monoid)
        source = node("objectProduct", carrier, carrier)
        declared_point = node("point", node("compose",
                              node("typedMap", terminal, source, [[0, [datum, datum]]]),
                              node(MULTIPLY, monoid)))
        composite_endpoint = node("morphismEndpoint", declared_point, "target")
        identity_endpoint = node("functorAction", node("fun.sets.identity"), endpoint)
        for target in (endpoint, selected_set, composite_endpoint, identity_endpoint,
                       node("valueData", identity_endpoint), node("obj.sets.rationals")):
            point_shapes(first, terminal, target, monoid, datum, monoid)

        # A selected scalar field has its exact object-action receipt. Its
        # element context supplies a closed domain; a raw field does not.
        for field in (structure[1], raw(semiring)[1][0][1]):
            for owner in (origin, monoid):
                for fragment in (element(owner, node("point", field)),
                                 element(owner, node("typedMap", terminal, carrier, field)),
                                 node("point", element(owner, field))):
                    argument = node("typedMap", terminal, source, [[0, [fragment, datum]]])
                    boolean(first.invoke(EQUALITY, equality(carrier, terminal, argument)))
                    success(first.invoke(MULTIPLY, invocation(monoid, terminal, argument)))

        # Closed fragments may occur inside a generalized graph, but their
        # actual retained Fin(1) is preserved instead of sampling that graph.
        complete = element(monoid, node("point", node("typedMap", terminal, carrier, [[0, datum]])))
        general = node("typedMap", family_domain, source,
                       [[0, [complete, datum]], [1, [datum, complete]]])
        family = callable_shape(first.invoke(MULTIPLY, invocation(monoid, family_domain, general)),
                                family_domain, carrier)
        maps = node("obj.sets.maps", family_domain, carrier)
        boolean(first.invoke(EQUALITY, equality(maps, terminal, [family, family])))
        products = node("objectProduct", carrier, node("obj.sets.truth_values"))
        nested = node("typedMap", terminal, node("objectProduct", products, products),
                      [[0, [[complete, False], [element(monoid, datum), True]]]])
        boolean(first.invoke(EQUALITY, equality(products, terminal, nested)))

        # Every native function role is consumed at its published curried
        # interface. Natural-domain fields are applied to explicit closed
        # arguments; this does not attempt equality on an infinite domain.
        finite = success(first.call(RING, node("obj.rings.integers_mod", 3)))
        finite_monoid = success(first.call(MONOID, finite))
        c, s = raw(finite)
        unary = node("obj.sets.maps", c, c)
        binary = node("obj.sets.maps", c, unary)
        finite_point = success(first.invoke(MULTIPLY, invocation(finite_monoid, terminal, [1, 2])))
        inventoried = node("finiteData", c, [0, 1, 2])
        owned_image = element(finite_monoid, node("point", finite_point))
        closed_image = node("typedMap", terminal, inventoried,
                            node("finiteGraph", [0], [[0, owned_image]]))
        boolean(first.invoke(EQUALITY, equality(inventoried, terminal, [closed_image, 0])))
        for field in (s[0][0], s[1][0]):
            closed = node("typedMap", terminal, binary, [[0, field]])
            args = node("typedMap", terminal, node("objectProduct", binary, binary),
                        [[0, [node("point", closed), field]]])
            boolean(first.invoke(EQUALITY, equality(binary, terminal, args)))
            field_target = node("morphismEndpoint", field, "target")
            apply_field = node("compose", node("typedMap", terminal, c, [[0, 1]]), field)
            supplied_function = node("typedMap", c, c, [[0, 1], [1, 0], [2, 2]])
            boolean(first.invoke(EQUALITY, equality(unary, terminal,
                                  [node("point", apply_field), supplied_function])))
            boolean(first.invoke(EQUALITY, equality(field_target, terminal,
                                  [supplied_function, supplied_function])))
            # The endpoint descriptor supplies a function-point interface; it
            # cannot relabel the actual whole native field's target.
            assert first.invoke(EQUALITY, equality(field_target, terminal,
                                [node("point", apply_field), supplied_function]))["status"] == "error"
        naturals = node("obj.sets.naturals")
        choose_natural = node("typedMap", terminal, naturals, [[0, 4]])
        for field in (s[0][2], s[1][2]):
            closed = node("point", node("compose", choose_natural,
                          node("typedMap", naturals, unary, field)))
            supplied = node("typedMap", c, c, [[0, 2], [1, 0], [2, 1]])
            args = node("typedMap", terminal, node("objectProduct", unary, unary),
                        [[0, [closed, supplied]]])
            boolean(first.invoke(EQUALITY, equality(unary, terminal, args)))
        cast = node("point", node("compose", choose_natural,
                    node("typedMap", naturals, c, s[2])))
        boolean(first.invoke(EQUALITY, equality(c, terminal, [cast, 2])))

        # Wrapping the actual native multiplication field retains that field
        # as data through the object projection and the generic consumer.
        supplied = copy.deepcopy(finite)
        raw(supplied)[1][1][0] = node("typedMap", c, unary, s[1][0])
        framed_monoid = success(first.call(MONOID, supplied))
        framed_point = success(first.invoke(MULTIPLY, invocation(framed_monoid, terminal, [1, 2])))
        assert framed_point["ctor"] == "opaqueData"
        boolean(first.invoke(EQUALITY, equality(c, terminal, [node("point", framed_point), 0])))
        graph_rows = [node("typedMap", c, c, node("finiteGraph", [0, 1, 2],
                           [[0, element(node("obj.rings.integers_mod", 3), 2)],
                            [1, node("point", node("typedMap", terminal, c, [[0, 0]]))],
                            [2, 1]])) for _ in range(3)]
        raw(supplied)[1][1][0] = node("typedMap", c, unary,
                                    node("finiteGraph", [0, 1, 2],
                                         [[i, node("valueData", row)] for i, row in enumerate(graph_rows)]))
        framed_graph_monoid = success(first.call(MONOID, supplied))
        graph_point = success(first.invoke(MULTIPLY, invocation(framed_graph_monoid, terminal, [1, 2])))
        assert graph_point["ctor"] == "valueData"
        boolean(first.invoke(EQUALITY, equality(c, terminal,
                              [element(framed_graph_monoid, graph_point), 0])))

        # Exact endpoint and owner failures remain failures after decoding.
        wrong = node("typedMap", terminal, carrier, element(monoid, datum))
        assert first.invoke(EQUALITY, equality(endpoint, terminal, [wrong, datum]))["status"] == "error"
        point = success(first.invoke(MULTIPLY, invocation(monoid, terminal, [datum, datum])))
        changed = copy.deepcopy(monoid)
        raw(changed)[1][2] = raw(changed)[1][0]
        changed_set = monoid_carrier(changed)
        wrong_owner = element(changed, element(monoid, node("point", point)))
        assert first.invoke(EQUALITY, equality(changed_set, terminal, [wrong_owner, datum]))["status"] == "error"
        changed_target = multiplication(monoid, terminal, changed_set, [element(monoid, datum), datum])
        assert first.invoke(MULTIPLY, changed_target)["status"] == "error"
        whole_packet = multiplication(monoid, source, endpoint, node("identity", source, source))
        whole_packet["args"][4] = source
        whole = callable_shape(first.invoke(MULTIPLY, whole_packet), source, endpoint)
        assert first.invoke(MULTIPLY, invocation(monoid, terminal, [datum, datum], whole))["status"] == "error"
        other_domain = node("finiteData", terminal, [0])
        scalar_field = element(monoid, node("typedMap", other_domain, carrier, structure[1]))
        assert first.invoke(MULTIPLY, invocation(monoid, other_domain, [scalar_field, scalar_field]))["status"] == "unsupported"
        assert first.invoke(EQUALITY, equality(carrier, terminal,
                            [node("point", structure[1]), datum]))["status"] == "unsupported"
        assert first.invoke(EQUALITY, equality(carrier, terminal,
                            [node("typedMap", terminal, carrier, datum), datum]))["status"] in {"error", "unsupported"}
        unknown = element(monoid, node("operationExpression", "op.rings.mul", [origin], [datum, datum]))
        assert first.invoke(EQUALITY, equality(carrier, terminal, [unknown, datum]))["status"] == "unsupported"
        other_semiring = success(first.call(RING, origin))
        other_monoid = success(first.call(MONOID, other_semiring))
        assert first.invoke(EQUALITY, equality(carrier, terminal,
                            [element(other_monoid, datum), datum]))["status"] == "error"
        wrong_modulus = element(node("obj.rings.integers_mod", 5), 1)
        assert first.invoke(EQUALITY, equality(node("obj.sets.integers_mod", 3), terminal,
                            [wrong_modulus, 1]))["status"] == "error"
        repeated_inventory = node("finiteGraph", [0, 0], [[0, [1, 2]]])
        assert first.invoke(EQUALITY, equality(node("obj.sets.fin", 4), terminal,
                            repeated_inventory))["status"] == "error"

        second = Connection(environment)
        try:
            portable = fragments(terminal, node("obj.sets.rationals"), node("obj.sets.rationals"), datum)[8]
            boolean(second.invoke(EQUALITY, equality(node("obj.sets.rationals"), terminal, [portable, datum])))
            named_portable = fragments(terminal, node("obj.sets.rationals"), origin, datum)[8]
            boolean(second.invoke(EQUALITY, equality(node("obj.sets.rationals"), terminal, [named_portable, datum])))
            foreign = second.invoke(EQUALITY, equality(identity_endpoint, terminal, [complete, datum]))
            assert foreign["status"] == "error" and foreign["kind"] == "Unavailable"
        finally:
            second.close()
    finally:
        first.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--retained", action="store_true")
    args = parser.parse_args()
    if args.retained:
        retention_controls()
        return
    if args.contract is None or args.engine is None:
        parser.error("--contract and --engine are required")
    environment = dict(os.environ, CAS_SAGE_PYTHON=str(args.engine.absolute()),
                       PYTHONPATH=str(args.contract.resolve() / "python"),
                       PYTHONDONTWRITEBYTECODE="1")
    with tempfile.TemporaryDirectory(prefix="primitive-portable-point-protocol-") as temporary:
        environment["DOT_SAGE"] = temporary
        run(environment)
        subprocess.run([str(args.engine.absolute()), str(Path(__file__).absolute()), "--retained"],
                       env=environment, check=True)
    print("Local portable-point protocol controls completed; no mathematical acceptance was run.")


if __name__ == "__main__":
    main()
