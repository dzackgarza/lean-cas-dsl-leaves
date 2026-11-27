#!/usr/bin/env python3
"""Public tuple-port engineering controls; no mathematical expected answers.

Only framing, complete finite-coordinate shape, selected endpoint/parameter
consumption, result roles, actual returned-data reuse and live ownership are
checked. This script imports neither a kernel nor an acceptance suite.
"""

import argparse
import copy
import json
import os
from pathlib import Path
import selectors
import subprocess
import tempfile


def node(tag, *args):
    return {"ctor": tag, "args": list(args)}


def apply(operation, parameters, arrow, domain, source, target, argument):
    return node("apply", operation, parameters, arrow, domain, source, target, argument)


def vector(selected, dimension):
    return node("obj.sets.vectors", selected, dimension)


def product(left, right):
    return node("objectProduct", left, right)


def graph(values):
    return [[i, value] for i, value in enumerate(values)]


def payload(value):
    while isinstance(value, dict) and value.get("ctor") == "valueData":
        assert len(value["args"]) == 1
        value = value["args"][0]
    return value


def coordinate_shape(value, dimension):
    value = payload(value)
    assert isinstance(value, list) and len(value) == dimension
    assert all(isinstance(row, list) and len(row) == 2 and type(row[0]) is int for row in value)
    assert {row[0] for row in value} == set(range(dimension))


def owned_shape(value):
    assert isinstance(value, dict) and value.get("ctor") == "opaqueData"
    assert len(value["args"]) == 1 and isinstance(value["args"][0], str)


class Port:
    def __init__(self, engine, contract):
        self.log = tempfile.TemporaryFile()
        env = dict(os.environ, PYTHONPATH=str(contract / "python"), CAS_SAGE_PYTHON=str(engine))
        self.process = subprocess.Popen([str(engine), str(Path(__file__).with_name("backend.py"))],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=self.log, env=env)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.buffer = bytearray()
        self.requests = 0
        self.announcement = self.read()
        assert self.announcement["op"] == "ready" and self.announcement["protocol"] == 1

    def read(self):
        while b"\n" not in self.buffer:
            self.receive()
        line, rest = self.buffer.split(b"\n", 1)
        self.buffer = bytearray(rest)
        size = int(line)
        while len(self.buffer) < size:
            self.receive()
        data = bytes(self.buffer[:size])
        del self.buffer[:size]
        return json.loads(data)

    def receive(self):
        if not self.selector.select(timeout=45):
            raise RuntimeError("the native tuple protocol process did not reply")
        data = os.read(self.process.stdout.fileno(), 65536)
        if not data:
            self.log.seek(0)
            raise RuntimeError(self.log.read().decode(errors="replace"))
        self.buffer.extend(data)

    def call(self, operation, arguments, status="ok"):
        self.requests += 1
        packet = {"request_id": self.requests, "op": operation, "args": arguments}
        body = json.dumps(packet, ensure_ascii=False, separators=(",", ":")).encode()
        self.process.stdin.write(str(len(body)).encode() + b"\n" + body)
        self.process.stdin.flush()
        result = self.read()
        assert result["request_id"] == self.requests, result
        assert result["status"] == status, result
        return result.get("value")

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=10)
        self.selector.close()
        self.process.stdout.close()
        self.log.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--engine", type=Path, required=True)
    options = parser.parse_args()
    catalogue = json.loads((options.contract / "api" / "declared-ports.json").read_text())
    operations = {row["operation"] for row in catalogue["operations"]}
    inputs = {row["input"] for row in catalogue["inputForms"]}
    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    empty, cons = "mor.sets.tuple_empty", "mor.sets.tuple_cons"
    for operation in (empty, cons):
        assert operation in operations and operation in inputs
        assert sum(row["operation"] == operation and row["input"] == operation
                   for row in manifest["registrations"]) == 1

    one = node("obj.sets.fin", 1)
    rational = node("obj.sets.rationals")
    finite = node("obj.sets.fin", 5)
    boolean = node("obj.sets.truth_values")

    def empty_request(selected, domain=one, argument=None, source=one, target=None, arrow=None):
        return apply(empty, [selected], node(empty, selected) if arrow is None else arrow,
                     domain, source, vector(selected, 0) if target is None else target,
                     node("identity", one, one) if argument is None else argument)

    def cons_request(selected, dimension, argument, domain=one, source=None, target=None, arrow=None):
        return apply(cons, [selected, dimension], node(cons, selected, dimension) if arrow is None else arrow,
                     domain, product(selected, vector(selected, dimension)) if source is None else source,
                     vector(selected, dimension + 1) if target is None else target, argument)

    primary = Port(options.engine, options.contract)
    try:
        assert {empty, cons} <= set(primary.announcement["capabilities"])
        models = [(rational, [7, 9]), (node("obj.sets.integers"), -11),
                  (finite, 3), (boolean, True), (node("obj.sets.integers_mod", 11), 4),
                  (vector(rational, 2), graph([[2, 5], [-7, 4]])),
                  (node("obj.sets.maps", finite, finite), node("identity", finite, finite))]
        for selected, head in models:
            retained = primary.call(empty, empty_request(selected))
            coordinate_shape(retained, 0)
            for dimension in range(3):
                retained = primary.call(cons, cons_request(selected, dimension, [head, retained]))
                coordinate_shape(retained, dimension + 1)
        empty_set = node("obj.sets.fin", 0)
        coordinate_shape(primary.call(empty, empty_request(empty_set)), 0)
        empty_source = product(empty_set, vector(empty_set, 7))
        owned_shape(primary.call(cons, cons_request(empty_set, 7, node("identity", empty_source, empty_source),
                                                   domain=empty_source)))

        # Complete coordinate callables, native ownership and nested tuple data.
        reverse = "mor.sets.fin_rev"
        owned_coordinates = primary.call(reverse, apply(reverse, [5], node(reverse, 5),
                                                        finite, finite, finite,
                                                        node("identity", finite, finite)))
        owned_shape(owned_coordinates)
        for tail in (owned_coordinates, node("valueData", owned_coordinates),
                     node("typedMap", finite, finite, owned_coordinates),
                     node("compose", node("identity", finite, finite), owned_coordinates),
                     node("finiteGraph", list(range(5)), graph([1, 3, 0, 4, 2]))):
            coordinate_shape(primary.call(cons, cons_request(finite, 5, [2, tail])), 6)
        tail = node("element", vector(rational, 0), node("point", node(empty, rational)))
        coordinate_shape(primary.call(cons, cons_request(rational, 0, [[3, 8], tail])), 1)
        nested = vector(finite, 5)
        coordinate_shape(primary.call(cons, cons_request(nested, 0, [owned_coordinates, []])), 1)

        # Exact finiteData keys remain keys when returned inside a tuple.
        wrapped = node("finiteData", finite, [node("valueData", i) for i in range(5)])
        retained = primary.call(cons, cons_request(wrapped, 0, [node("valueData", 2), []]))
        coordinate_shape(primary.call(cons, cons_request(wrapped, 1, [node("valueData", 4), retained])), 2)

        # The full arrow and both public endpoint selectors retain their fields.
        tuple_arrow = node(cons, rational, 2)
        source, target = product(rational, vector(rational, 2)), vector(rational, 3)
        pair = [[1, 7], graph([[5, 6], [-4, 9]])]
        for actual_source, actual_target in ((source, target),
                (node("valueData", source), node("valueData", target)),
                (node("morphismEndpoint", tuple_arrow, "source"), node("morphismEndpoint", tuple_arrow, "target"))):
            packet = cons_request(rational, 2, node("identity", actual_source, actual_source),
                                  domain=actual_source, source=actual_source, target=actual_target)
            retained = primary.call(cons, packet)
            owned_shape(retained)
            coordinate_shape(primary.call(cons, cons_request(rational, 2, pair, source=actual_source,
                                                               target=actual_target, arrow=retained)), 3)
        whole_cons = primary.call(cons, cons_request(rational, 2, node("identity", source, source),
                                                     domain=source))
        owned_shape(whole_cons)
        coordinate_shape(primary.call(cons, cons_request(rational, 2, pair,
            arrow=node("typedMap", source, target, node("valueData", whole_cons)))), 3)
        coordinate_shape(primary.call(cons, cons_request(rational, 2, pair,
            source=node("morphismEndpoint", whole_cons, "source"),
            target=node("morphismEndpoint", whole_cons, "target"))), 3)

        # Every supplied generalized domain survives, including a distinct singleton.
        for domain in (node("obj.sets.fin", 0), node("obj.sets.fin", 3),
                       node("finiteData", one, [0])):
            points = domain["args"][1] if domain["ctor"] == "finiteData" else list(range(domain["args"][0]))
            family = node("typedMap", domain, source, [[i, pair] for i in points])
            owned_shape(primary.call(cons, cons_request(rational, 2, family, domain=domain)))
            terminal = node("powerObjectMap", "pow.sets", "terminal", [domain])
            owned_shape(primary.call(empty, empty_request(rational, domain=domain, argument=terminal)))
        family = node("mediator", node("identity", rational, rational),
                      node("compose", node("powerObjectMap", "pow.sets", "terminal", [rational]),
                           node(empty, rational)))
        infinite_result = primary.call(cons, cons_request(rational, 0, family, domain=rational))
        owned_shape(infinite_result)
        coordinate_shape(primary.call(cons, cons_request(rational, 0, [5, 11], source=rational,
                                                         arrow=infinite_result)), 1)
        # A tuple-valued element in a mediator keeps its coordinate-callable role.
        tuple_point = node("element", vector(finite, 5), node("typedMap", finite, finite, owned_coordinates))
        pair_point = node("mediator", node("element", finite, node("numeral", 1)), tuple_point)
        coordinate_shape(primary.call(cons, cons_request(finite, 5, pair_point)), 6)

        # Native scalar tokens remain on their original supplier through tuples.
        coefficient_map = "mor.sets.rational_dual_x_constants"
        dual = node("obj.sets.rational_dual_x")
        native_scalar = primary.call(coefficient_map, apply(coefficient_map, [], node(coefficient_map),
                                                            one, rational, dual, [4, 7]))
        owned_shape(payload(native_scalar))
        scalar_tuple = primary.call(cons, cons_request(dual, 0, [native_scalar, []]))
        coordinate_shape(primary.call(cons, cons_request(dual, 1, [native_scalar, scalar_tuple])), 2)

        # Deliberately malformed framing and complete-parameter controls.
        bad = cons_request(rational, 2, pair)
        for replacement in ([], [rational], [rational, 2, 0], [rational, -1], [rational, True]):
            packet = copy.deepcopy(bad)
            packet["args"][1] = replacement
            primary.call(cons, packet, "error")
        for field, replacement in ((2, node(cons, rational, 3)),
                                   (4, product(vector(rational, 2), rational)),
                                   (5, vector(rational, 4))):
            packet = copy.deepcopy(bad)
            packet["args"][field] = replacement
            primary.call(cons, packet, "error")
        packet = copy.deepcopy(bad)
        packet["args"].pop()
        primary.call(cons, packet, "error")
        for tail in (graph([[1, 2]]), [[0, [1, 2]], [0, [2, 3]]],
                     graph([[1, 2], [2, 3], [3, 4]]),
                     node("finiteGraph", [0], graph([[1, 2]])),
                     node("typedMap", node("obj.sets.fin", 3), rational, graph([[1, 2]])),
                     node("typedMap", node("obj.sets.fin", 2), finite, graph([0, 1]))):
            primary.call(cons, cons_request(rational, 2, [[2, 7], tail]), "error")
        primary.call(cons, cons_request(finite, 4, [1, owned_coordinates]), "error")
        primary.call(cons, cons_request(node("obj.sets.fin", 6), 5, [1, owned_coordinates]), "error")
        primary.call(cons, cons_request(rational, 2, pair, arrow=whole_cons,
                                        source=product(rational, vector(rational, 1))), "error")
        primary.call(cons, cons_request(rational, 3, pair, arrow=whole_cons), "error")
        for argument in ([], 1, node("element", one, node("numeral", 2))):
            primary.call(empty, empty_request(rational, argument=argument), "error")
        for parameters in ([], [rational, 0]):
            packet = empty_request(rational)
            packet["args"][1] = parameters
            primary.call(empty, packet, "error")
        primary.call(cons, cons_request(rational, 2, [[1, 2], 3]), "unsupported")
        primary.call(cons, cons_request(dual, 1, [native_scalar, native_scalar]), "error")
        primary_count = primary.requests
    finally:
        primary.close()

    # The supplier is stopped before the second process begins. Wrappers do not
    # resurrect a callable, scalar or coordinate object on the new connection.
    secondary = Port(options.engine, options.contract)
    try:
        for operation, packet in ((cons, cons_request(rational, 2, pair, arrow=whole_cons)),
                                  (cons, cons_request(finite, 5, [2, owned_coordinates])),
                                  (cons, cons_request(dual, 1, [native_scalar, scalar_tuple])),
                                  (cons, cons_request(rational, 0, [5, 11], source=rational,
                                                      arrow=infinite_result)),
                                  (empty, empty_request(node("valueData", native_scalar)))):
            secondary.call(operation, packet, "unsupported")
        secondary_count = secondary.requests
    finally:
        secondary.close()
    print(json.dumps({"primaryConnectionRequests": primary_count,
                      "stoppedOwnerRequests": secondary_count,
                      "boundary": "framing, shape, selection, returned-data reuse and live ownership only"}))


if __name__ == "__main__":
    main()
