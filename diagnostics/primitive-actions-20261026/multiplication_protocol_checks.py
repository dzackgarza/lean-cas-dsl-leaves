#!/usr/bin/env python3
"""Public invocation, data-field selection and ownership checks only.

No mathematical scalar answer or algebraic law is asserted. A synthetic graph
fixture checks transport of supplied field data, without claiming it is a monoid.
"""

import argparse
import copy
import os
from pathlib import Path
import tempfile

from protocol_checks import Connection, MONOID, MULTIPLY, RING, node


def success(reply):
    assert reply["status"] == "ok", reply
    return reply["value"]


def raw(packet):
    while isinstance(packet, dict) and packet.get("ctor") == "valueData":
        packet, = packet["args"]
    return packet


def invocation(monoid, domain, argument, arrow=None):
    carrier = raw(monoid)[0]
    source = node("objectProduct", carrier, carrier)
    return node("apply", MULTIPLY, [monoid],
                node(MULTIPLY, monoid) if arrow is None else arrow,
                domain, source, carrier, argument)


def run(environment):
    first = Connection(environment)
    terminal, domain = node("obj.sets.fin", 1), node("obj.sets.fin", 2)
    try:
        origins = [node("obj.rings.rationals"), node("obj.rings.matrices", 2,
                   node("obj.commutative_rings.integers_mod", 5))]
        for origin in origins:
            semiring = success(first.call(RING, origin))
            monoid = success(first.call(MONOID, semiring))
            carrier, structure = raw(monoid)
            one, zero = structure[1], raw(semiring)[1][0][1]
            source = node("objectProduct", carrier, carrier)
            result = success(first.invoke(MULTIPLY, invocation(monoid, terminal, [one, zero])))
            assert result["ctor"] == "opaqueData"
            success(first.invoke(MULTIPLY, invocation(monoid, terminal, [result, one])))
            retained_operand = node("element", origin, node("valueData", one))
            success(first.invoke(MULTIPLY, invocation(monoid, terminal, [retained_operand, zero])))

            whole = success(first.invoke(MULTIPLY, invocation(
                monoid, source, node("identity", source, source))))
            whole_source, whole_target, _ = raw(whole)["args"]
            assert raw(whole)["ctor"] == "typedMap"
            assert whole_source == source and whole_target == carrier
            success(first.invoke(MULTIPLY, invocation(monoid, terminal, [one, zero], whole)))
            wrapped_composite = node("compose", node("identity", source, source), whole)
            success(first.invoke(MULTIPLY, invocation(monoid, terminal, [one, zero], wrapped_composite)))

            graph = node("finiteGraph", [0, 1], [[0, [one, zero]], [1, [zero, one]]])
            family = node("typedMap", domain, source, graph)
            general = success(first.invoke(MULTIPLY, invocation(monoid, domain, family)))
            assert raw(general)["args"][:2] == [domain, carrier]
            singleton = node("finiteData", terminal, [0])
            singleton_map = node("typedMap", singleton, source, [[0, [one, zero]]])
            singleton_result = success(first.invoke(MULTIPLY, invocation(monoid, singleton, singleton_map)))
            assert raw(singleton_result)["args"][:2] == [singleton, carrier]
            # Consume the returned generalized callable's actual data through
            # supplied comparison/mediator frames, keeping their exact domains.
            choose = node("typedMap", terminal, domain, [[0, 0]])
            right = node("typedMap", terminal, carrier, [[0, one]])
            operand = node("mediator", node("compose", choose, general), right)
            success(first.invoke(MULTIPLY, invocation(monoid, terminal, operand)))

            changed = copy.deepcopy(raw(whole))
            changed["args"][1] = source
            assert first.invoke(MULTIPLY, invocation(monoid, terminal, [one, zero], changed))["status"] == "error"
            wrong = node("apply", MULTIPLY, [monoid, monoid], node(MULTIPLY, monoid),
                         terminal, source, carrier, [one, zero])
            assert first.invoke(MULTIPLY, wrong)["status"] == "error"

        # The field is supplied data. This fixture asserts only that the
        # selected entry is used; it asserts no multiplication table or law.
        semiring = success(first.call(RING, node("obj.rings.integers_mod", 2)))
        monoid = success(first.call(MONOID, semiring))
        supplied = copy.deepcopy(monoid)
        rows = [node("finiteGraph", [0, 1], [[0, 1], [1, 0]]),
                node("finiteGraph", [0, 1], [[0, 0], [1, 1]])]
        raw(supplied)[1][0] = node("finiteGraph", [0, 1], [[0, rows[0]], [1, rows[1]]])
        chosen = success(first.invoke(MULTIPLY, invocation(supplied, terminal, [0, 1])))
        assert chosen == node("valueData", rows[0]["args"][1][1][1])
        changed_selection = invocation(supplied, terminal, [0, 1], node(MULTIPLY, monoid))
        assert first.invoke(MULTIPLY, changed_selection)["status"] == "error"

        second = Connection(environment)
        try:
            foreign = second.invoke(MULTIPLY, invocation(monoid, terminal, [0, 1]))
            assert foreign["status"] == "error" and foreign["kind"] == "Unavailable"
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
    with tempfile.TemporaryDirectory(prefix="primitive-multiplication-protocol-") as temporary:
        environment["DOT_SAGE"] = temporary
        run(environment)
    print("Local multiplication protocol checks completed; no mathematical acceptance was run.")


if __name__ == "__main__":
    main()
