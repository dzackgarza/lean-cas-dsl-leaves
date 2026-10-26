#!/usr/bin/env python3
"""Self-designed point framing, endpoint retention and ownership controls.

No Boolean answer, arithmetic result, equality law or mathematical property is
asserted. Successful observations are checked only for their declared data type.
"""

import argparse
import copy
import os
from pathlib import Path
import tempfile

from protocol_checks import Connection, EQUALITY, MONOID, MULTIPLY, RING, node
from multiplication_protocol_checks import invocation, raw, success


def equality(selected, domain, argument, arrow=None, target=None, source=None):
    return node("apply", EQUALITY, [selected],
                node(EQUALITY, selected) if arrow is None else arrow, domain,
                node("objectProduct", selected, selected) if source is None else source,
                node("obj.sets.truth_values") if target is None else target, argument)


def boolean(reply):
    data = success(reply)
    assert data["ctor"] == "valueData" and type(raw(data)) is bool
    return data


def callable_shape(reply, domain, target):
    data = success(reply)
    assert raw(data)["ctor"] == "typedMap"
    assert raw(data)["args"][:2] == [domain, target]
    assert raw(data)["args"][2]["ctor"] == "opaqueData"
    return data


def monoid_carrier(monoid):
    semigroup = node("functorAction", node("fun.monoids.semigroup"), monoid)
    magma = node("functorAction", node("classifierForget", "clf.magmas.associative", []), semigroup)
    return node("functorAction", node("classifierForget", "clf.sets.binary_operation", []), magma)


def run(environment):
    first = Connection(environment)
    terminal, domain = node("obj.sets.fin", 1), node("obj.sets.fin", 2)
    truth = node("obj.sets.truth_values")
    try:
        origin = node("obj.rings.rationals")
        semiring = success(first.call(RING, origin))
        monoid = success(first.call(MONOID, semiring))
        carrier, structure = raw(monoid)
        one, zero = structure[1], raw(semiring)[1][0][1]
        source = node("objectProduct", carrier, carrier)
        left = node("typedMap", terminal, carrier, [[0, one]])
        right = node("element", origin, node("valueData", zero))
        point = node("element", origin, node("point", node("compose", left,
                           node("identity", carrier, carrier))))
        pair_arrow = node("typedMap", terminal, source, node("mediator", point, right))
        composite = node("point", node("compose", pair_arrow, node(MULTIPLY, monoid)))
        expression = node("element", monoid, node("operationExpression", MULTIPLY,
                          [monoid], [point, right]))
        nested = [point, node("valueData", right)]
        cases = [nested, [composite, one], [expression, zero],
                 node("point", node("mediator", point, right)), pair_arrow,
                 [[0, [one, zero]]],  # The complete raw graph at the actual Fin(1).
                 node("typedMap", terminal, source, [[0, [point, right]]])]
        for actual in cases:
            result = success(first.invoke(MULTIPLY, invocation(monoid, terminal, actual)))
            assert result["ctor"] == "opaqueData"
            boolean(first.invoke(EQUALITY, equality(carrier, terminal, [result, point])))

        # Each array component is the complete original generalized callable.
        f = node("typedMap", domain, carrier, [[0, one], [1, zero]])
        g = node("typedMap", domain, carrier, [[0, zero], [1, one]])
        family = callable_shape(first.invoke(MULTIPLY, invocation(monoid, domain, [f, g])), domain, carrier)
        wrapped_family = node("element", origin, family)
        callable_shape(first.invoke(MULTIPLY, invocation(monoid, domain, [wrapped_family, g])), domain, carrier)
        graph = [[0, [one, zero]], [1, [zero, one]]]
        callable_shape(first.invoke(MULTIPLY, invocation(monoid, domain, graph)), domain, carrier)
        observed = callable_shape(first.invoke(EQUALITY, equality(carrier, domain, [family, f])), domain, truth)
        assert first.invoke(MULTIPLY, invocation(monoid, domain, [one, zero]))["status"] == "unsupported"
        assert first.invoke(EQUALITY, equality(carrier, domain, [one, zero]))["status"] == "unsupported"

        # Whole observations and their actual returned callable are reused.
        whole = callable_shape(first.invoke(EQUALITY, equality(carrier, source,
                                 node("identity", source, source))), source, truth)
        boolean(first.invoke(EQUALITY, equality(carrier, terminal, [one, zero], whole)))
        choose = node("typedMap", terminal, domain, [[0, 1]])
        boolean_point = node("point", node("compose", choose, observed))
        boolean(first.invoke(EQUALITY, equality(truth, terminal, [boolean_point, node("valueData", False)])))
        maps = node("obj.sets.maps", domain, carrier)
        boolean(first.invoke(EQUALITY, equality(maps, terminal, [family, raw(family)["args"][2]])))
        graph_fragments = node("typedMap", domain, source, [[0, [point, right]], [1, [right, point]]])
        fragment_family = callable_shape(first.invoke(MULTIPLY, invocation(monoid, domain, graph_fragments)), domain, carrier)
        boolean(first.invoke(EQUALITY, equality(maps, terminal, [fragment_family, family])))

        # The selected carrier paths retain the complete original structures.
        selected = monoid_carrier(monoid)
        selected_point = node("typedMap", terminal, selected, node("element", monoid, one))
        boolean(first.invoke(EQUALITY, equality(selected, terminal, [selected_point, zero])))
        semiring_set = node("functorAction", node("fun.semirings.forget"), semiring)
        boolean(first.invoke(EQUALITY, equality(semiring_set, terminal,
                              [node("element", semiring, one), zero])))
        boolean(first.invoke(EQUALITY, equality(node("obj.sets.rationals"), terminal,
                              [one, [-5, 9]])))
        endpoint_arrow = node(EQUALITY, carrier)
        endpoint_source = node("morphismEndpoint", endpoint_arrow, "source")
        endpoint_target = node("morphismEndpoint", endpoint_arrow, "target")
        boolean(first.invoke(EQUALITY, equality(carrier, terminal, [one, zero],
                              source=endpoint_source, target=endpoint_target)))
        product_target = node("morphismEndpoint", node(MULTIPLY, monoid), "target")
        boolean(first.invoke(EQUALITY, equality(product_target, terminal,
                              [node("element", monoid, one), zero])))

        # Matrix data are owned engine points, with no invented literal codec.
        matrices = node("obj.rings.matrices", 2, node("obj.commutative_rings.integers_mod", 7))
        matrix_semiring = success(first.call(RING, matrices))
        matrix_monoid = success(first.call(MONOID, matrix_semiring))
        matrix_carrier, matrix_structure = raw(matrix_monoid)
        matrix_one = matrix_structure[1]
        matrix_result = success(first.invoke(MULTIPLY, invocation(matrix_monoid, terminal,
                                      [node("element", matrices, matrix_one), matrix_one])))
        boolean(first.invoke(EQUALITY, equality(matrix_carrier, terminal, [matrix_result, matrix_one])))
        matrix_numeral = node("element", matrices, node("numeral", 3))
        success(first.invoke(MULTIPLY, invocation(matrix_monoid, terminal, [matrix_numeral, matrix_one])))

        # Shape/selection failures are checked independently of computed values.
        other_semiring = success(first.call(RING, origin))
        other_monoid = success(first.call(MONOID, other_semiring))
        wrong_owner = node("element", other_monoid, one)
        assert first.invoke(EQUALITY, equality(selected, terminal, [wrong_owner, zero]))["status"] == "error"
        foreign_carrier_point = raw(other_monoid)[1][1]
        assert first.invoke(EQUALITY, equality(carrier, terminal, [foreign_carrier_point, zero]))["status"] == "error"
        changed = copy.deepcopy(left)
        changed["args"][1] = node("obj.sets.rationals")
        assert first.invoke(MULTIPLY, invocation(monoid, terminal, [changed, zero]))["status"] == "error"
        changed = copy.deepcopy(pair_arrow)
        changed["args"][0] = domain
        assert first.invoke(MULTIPLY, invocation(monoid, terminal, changed))["status"] == "error"
        wrong = equality(carrier, terminal, [one, zero])
        wrong["args"][1].append(carrier)
        assert first.invoke(EQUALITY, wrong)["status"] == "error"
        wrong = equality(carrier, terminal, [one, zero], node(EQUALITY, selected))
        assert first.invoke(EQUALITY, wrong)["status"] == "error"
        assert first.invoke(EQUALITY, equality(carrier, terminal, [one, zero], target=carrier))["status"] == "error"
        assert first.invoke(EQUALITY, equality(node("obj.sets.rationals"), terminal,
                              [[2, 4], [1, 3]]))["status"] == "error"
        assert first.invoke(EQUALITY, equality(maps, terminal, [family, left]))["status"] == "error"

        second = Connection(environment)
        try:
            foreign = second.invoke(EQUALITY, equality(carrier, terminal, [one, zero]))
            assert foreign["status"] == "error" and foreign["kind"] == "Unavailable"
            hidden = second.invoke(EQUALITY, equality(node("obj.sets.rationals"), terminal,
                                  [node("valueData", one), [2, 3]]))
            assert hidden["status"] == "error" and hidden["kind"] == "Unavailable"
        finally:
            second.close()
    finally:
        first.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--engine", type=Path, required=True)
    args = parser.parse_args()
    environment = dict(os.environ, CAS_SAGE_PYTHON=str(args.engine.absolute()),
                       PYTHONPATH=str(args.contract.resolve() / "python"),
                       PYTHONDONTWRITEBYTECODE="1")
    with tempfile.TemporaryDirectory(prefix="primitive-point-observation-protocol-") as temporary:
        environment["DOT_SAGE"] = temporary
        run(environment)
    print("Local point/observation protocol controls completed; no mathematical acceptance was run.")


if __name__ == "__main__":
    main()
