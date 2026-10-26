#!/usr/bin/env python3
"""Producer/consumer framing and live-owner controls for the four existing ports.

No equality answer or arithmetic value is asserted. Controls inspect only reply
shape, exact selected framing, token ownership and the retained actual receipts.
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


def retention_controls():
    """Inspect private data retention only; never compare native values."""
    from primitive_actions import Actions, PointResult, ProductComputation
    from monoid_multiplication import Multiplication

    actions = Actions()
    terminal = node("obj.sets.fin", 1)
    ring = node("obj.rings.matrices", 3, node("obj.commutative_rings.integers_mod", 5))
    object_packet = {"ctor": RING, "args": [], "receiver": ring}
    semiring = actions.run(RING, object_packet)
    monoid_packet = {"ctor": MONOID, "args": [], "receiver": semiring}
    monoid = actions.run(MONOID, monoid_packet)
    carrier, structure = raw(monoid)
    one = structure[1]
    assert actions.session.get(one).request is object_packet
    assert actions.session.get(carrier).request["receiver"] is ring
    operands = [one, one]
    packet = invocation(monoid, terminal, operands)
    result = actions.run(MULTIPLY, packet)
    native = actions.session.get(result)
    assert isinstance(native.context, PointResult)
    retained = native.context.invocation
    assert native.request is packet and retained.packet is packet
    assert retained.parameters is packet["args"][1]
    assert retained.parameters[0] is monoid and retained.packet["args"][6] is operands
    original = actions.session.get(native.context.data)
    assert native.value is original.value
    assert isinstance(original.context, ProductComputation)
    assert original.context.packet is packet and original.context.fragment is packet["args"][2]
    assert original.context.parameters[0] is monoid
    assert original.context.field is structure[0]

    source = node("objectProduct", carrier, carrier)
    whole_packet = invocation(monoid, source, node("identity", source, source))
    whole = actions.run(MULTIPLY, whole_packet)
    later_packet = invocation(monoid, terminal, operands, whole)
    later = actions.run(MULTIPLY, later_packet)
    later_native = actions.session.get(later)
    assert later_native.request is later_packet
    assert later_native.context.invocation.action.invocation.packet is whole_packet
    original_later = actions.session.get(later_native.context.data)
    assert original_later.context.packet is whole_packet
    assert later_native.value is original_later.value
    reader = Multiplication(actions.session, later_packet)
    converted = reader.point_callable(later, terminal, carrier, monoid)
    assert converted.source is terminal and converted.target is carrier
    assert converted(0) is later  # Exact retained data, not a mathematical answer.


def run(environment):
    first = Connection(environment)
    terminal = node("obj.sets.fin", 1)
    try:
        semiring = success(first.call(RING, node("obj.rings.rationals")))
        monoid = success(first.call(MONOID, semiring))
        natural_monoid = success(first.call(MONOID, node("obj.semirings.naturals")))
        for selected in (monoid, natural_monoid):
            carrier, structure = raw(selected)
            one = structure[1]
            source = node("objectProduct", carrier, carrier)
            point = success(first.invoke(MULTIPLY, invocation(selected, terminal, [one, one])))
            fragments = [node("point", point), node("typedMap", terminal, carrier, point),
                         node("element", selected, node("point", point)),
                         node("element", selected, node("typedMap", terminal, carrier, point))]
            for fragment in fragments:
                result = success(first.invoke(MULTIPLY, invocation(selected, terminal, [fragment, one])))
                assert result["ctor"] == "opaqueData"
                boolean(first.invoke(EQUALITY, equality(carrier, terminal, [fragment, result])))
            retained_endpoint = node("morphismEndpoint", node("point", point), "target")
            boolean(first.invoke(EQUALITY, equality(retained_endpoint, terminal,
                                  [node("element", selected, node("point", point)), one])))

            # An actual whole callable stays owned; its later scalar result
            # retains the new creating invocation as well as that dependency.
            whole = callable_shape(first.invoke(MULTIPLY, invocation(selected, source,
                                      node("identity", source, source))), source, carrier)
            later = success(first.invoke(MULTIPLY, invocation(selected, terminal, [one, one], whole)))
            boolean(first.invoke(EQUALITY, equality(carrier, terminal, [node("point", later), point])))

            endpoint = node("morphismEndpoint", node(MULTIPLY, selected), "target")
            original = invocation(selected, terminal, [one, one])
            original["args"][5] = endpoint
            endpoint_point = success(first.invoke(MULTIPLY, original))
            reused = node("element", selected, node("typedMap", terminal, carrier, endpoint_point))
            success(first.invoke(MULTIPLY, invocation(selected, terminal, [reused, one])))
            selected_set = monoid_carrier(selected)
            selected_fragment = node("typedMap", terminal, selected_set, point)
            boolean(first.invoke(EQUALITY, equality(selected_set, terminal, [selected_fragment, one])))
            boolean(first.invoke(EQUALITY, equality(carrier, terminal,
                                  [node("element", selected, one), point])))

            expression = node("element", selected, node("operationExpression", MULTIPLY,
                              [selected], [node("point", point), one]))
            boolean(first.invoke(EQUALITY, equality(carrier, terminal, [expression, point])))
            supplied_pair = node("typedMap", terminal, source,
                                 node("mediator", node("element", selected, node("point", point)),
                                      node("element", selected, one)))
            complete = node("element", selected, node("point", node("compose", supplied_pair, whole)))
            boolean(first.invoke(EQUALITY, equality(carrier, terminal, [complete, point])))

            changed = copy.deepcopy(selected)
            # Same actual native parent, carrier and multiplication field;
            # a different complete selected parameter remains different.
            raw(changed)[1][2] = raw(changed)[1][0]
            wrong = invocation(changed, terminal, [node("point", point), one])
            assert first.invoke(MULTIPLY, wrong)["status"] == "error"
            wrong_owner = node("element", changed, node("point", point))
            assert first.invoke(EQUALITY, equality(monoid_carrier(changed), terminal,
                                [wrong_owner, one]))["status"] == "error"
            changed_endpoint = node("morphismEndpoint", node(MULTIPLY, changed), "target")
            assert first.invoke(EQUALITY, equality(changed_endpoint, terminal,
                                [node("point", point), one]))["status"] == "error"

            # A whole callable never takes the scalar point conversion path.
            whole_at_endpoint = invocation(selected, source, node("identity", source, source))
            whole_at_endpoint["args"][5] = endpoint
            returned = callable_shape(first.invoke(MULTIPLY, whole_at_endpoint), source, endpoint)
            assert first.invoke(MULTIPLY, invocation(selected, terminal, [one, one], returned))["status"] == "error"
            other_domain = node("finiteData", terminal, [0])
            changed_point = node("typedMap", other_domain, carrier, point)
            assert first.invoke(MULTIPLY, invocation(selected, other_domain,
                                [changed_point, changed_point]))["status"] == "error"

        # Native operation fields are curried function data at the exact
        # carrier field of their actual returned object, with no new address.
        finite_semiring = success(first.call(RING, node("obj.rings.integers_mod", 2)))
        finite_monoid = success(first.call(MONOID, finite_semiring))
        carrier, structure = raw(finite_monoid)
        functions = node("obj.sets.maps", carrier, node("obj.sets.maps", carrier, carrier))
        row_a = node("finiteGraph", [0, 1], [[0, 1], [1, 0]])
        row_b = node("finiteGraph", [0, 1], [[0, 0], [1, 1]])
        supplied = node("finiteGraph", [0, 1], [[0, row_a], [1, row_b]])
        for field in (structure[0], raw(finite_semiring)[1][0][0]):
            boolean(first.invoke(EQUALITY, equality(functions, terminal, [field, supplied])))
        supplied_semiring = copy.deepcopy(finite_semiring)
        raw(supplied_semiring)[1][1][0] = supplied
        supplied_monoid = success(first.call(MONOID, supplied_semiring))
        portable = success(first.invoke(MULTIPLY, invocation(supplied_monoid, terminal, [0, 1])))
        assert portable["ctor"] == "valueData"  # Only the wire alternative is asserted.
        portable_element = node("element", supplied_monoid, portable)
        boolean(first.invoke(EQUALITY, equality(carrier, terminal, [portable_element, 0])))
        success(first.invoke(MULTIPLY, invocation(supplied_monoid, terminal, [portable_element, 1])))
        wrong_functions = node("obj.sets.maps", node("obj.sets.fin", 2),
                               node("obj.sets.maps", carrier, carrier))
        assert first.invoke(EQUALITY, equality(wrong_functions, terminal,
                            [structure[0], supplied]))["status"] == "error"

        second_semiring = success(first.call(RING, node("obj.rings.rationals")))
        second_monoid = success(first.call(MONOID, second_semiring))
        old_carrier, old_structure = raw(monoid)
        foreign_shape = success(first.invoke(MULTIPLY, invocation(second_monoid, terminal,
                                    [raw(second_monoid)[1][1], raw(second_monoid)[1][1]])))
        assert first.invoke(EQUALITY, equality(old_carrier, terminal,
                            [node("point", foreign_shape), old_structure[1]]))["status"] == "error"
        second = Connection(environment)
        try:
            reply = second.invoke(EQUALITY, equality(old_carrier, terminal,
                                  [node("point", foreign_shape), old_structure[1]]))
            assert reply["status"] == "error" and reply["kind"] == "Unavailable"
        finally:
            second.close()
    finally:
        first.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--retained", action="store_true")
    args = parser.parse_args()
    if args.retained:
        retention_controls()
        return
    environment = dict(os.environ, CAS_SAGE_PYTHON=str(args.engine.absolute()),
                       PYTHONPATH=str(args.contract.resolve() / "python"),
                       PYTHONDONTWRITEBYTECODE="1")
    with tempfile.TemporaryDirectory(prefix="primitive-composability-protocol-") as temporary:
        environment["DOT_SAGE"] = temporary
        run(environment)
        retained = subprocess.run([str(args.engine.absolute()), str(Path(__file__).absolute()),
                                   "--contract", str(args.contract.resolve()),
                                   "--engine", str(args.engine.absolute()), "--retained"],
                                  env=environment, capture_output=True, text=True)
        assert retained.returncode == 0, retained.stderr
    print("Local composability protocol controls completed; no mathematical acceptance was run.")


if __name__ == "__main__":
    main()
