#!/usr/bin/env python3
"""Public-port checks for the ordinary commutative-ring object action.

Checks concern registration addresses, framing, native result reuse, selected
presentation data and live ownership. No computed mathematical answer or law is
asserted. This script imports only the leaf's existing public-port harness.
"""

import argparse
import json
import os
from pathlib import Path

from completion_smoke import (ONE, Port, identity, invoke, node, owned,
                              payload, require)


FUNCTOR = "fun.commutative_rings.ring"


def object_request(receiver):
    return {"ctor": FUNCTOR, "args": [], "receiver": receiver}


def scalar_shape(value, kind, label):
    value = payload(value)
    if kind == "integer":
        require(type(value) is int, label + ": expected integer-shaped scalar data")
    elif kind == "rational":
        require(isinstance(value, list) and len(value) == 2
                and all(type(field) is int for field in value) and value[1] > 0,
                label + ": expected rational-shaped scalar data")
    else:
        owned(value)
    return value


def consume_image(port, label, receiver, operands, kind):
    selected = owned(port.request(label + "/object action", FUNCTOR, object_request(receiver)))
    if operands is None:
        operands = [node("element", selected, node("numeral", number)) for number in (2, 3)]
    source = node("objectProduct", selected, selected)
    operation = "op.rings.add"
    complete = owned(port.request(label + "/whole ring operation", operation,
                                  invoke(operation, [selected], source, source, selected,
                                         identity(source))))
    result = scalar_shape(port.request(label + "/reuse actual image and callable", operation,
                                       invoke(operation, [selected], ONE, source, selected,
                                              operands, complete)), kind, label)
    operation = "op.rings.neg"
    scalar_shape(port.request(label + "/reuse returned scalar", operation,
                              invoke(operation, [selected], ONE, selected, selected, result)),
                 kind, label)
    # The result's ownership survives ordinary public value-data wrappers.
    wrapped = node("valueData", selected)
    scalar_shape(port.request(label + "/wrapped actual image", operation,
                              invoke(operation, [wrapped], ONE, wrapped, wrapped, result)),
                 kind, label)
    return selected, result, complete


def manifest_check(contract):
    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    registrations = [row for row in manifest["registrations"] if row["operation"] == FUNCTOR]
    require(len(registrations) == 1 and registrations[0]["input"] == "cat.commutative_rings",
            "the ordinary action requires exactly its source-category registration")
    require(not any(row["operation"] == FUNCTOR + "#map" for row in manifest["registrations"]),
            "the map action is outside this object-action specimen")
    reference = json.loads((contract / "api" / "declared-ports.json").read_text())
    require(any(row["operation"] == FUNCTOR for row in reference["operations"]),
            "the object operation is absent from the supplied public inventory")
    require(any(row["input"] == "cat.commutative_rings" for row in reference["inputForms"]),
            "the source-category input is absent from the supplied public inventory")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"),
                        help="published contract checkout containing python/cas_port.py")
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"),
                        help="installed Sage-compatible Python executable")
    arguments = parser.parse_args()
    require(bool(arguments.contract), "a published contract checkout is required")
    contract = Path(arguments.contract).resolve()
    manifest_check(contract)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    environment["PYTHONPATH"] = str(contract / "python")
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    backend = Path(__file__).resolve().with_name("backend.py")
    with Port(backend, environment) as port:
        examples = [
            ("integers", node("obj.commutative_rings.integers"), [17, -5], "integer"),
            ("rationals", node("obj.commutative_rings.rationals"), [[2, 3], [-4, 5]], "rational"),
            ("zero modulus", node("obj.commutative_rings.integers_mod", 0), [6, -2], "integer"),
            ("unit modulus", node("obj.commutative_rings.integers_mod", 1), [0, 0], "integer"),
            ("composite modulus", node("obj.commutative_rings.integers_mod", 8), [3, 7], "integer"),
            ("wrapped finite data", node("valueData", node("finiteData",
                node("obj.commutative_rings.integers_mod", 3), [0, 1, 2])), [1, 2], "integer"),
            ("dual x", node("obj.commutative_rings.rational_dual_x"), None, "owned"),
            ("dual y", node("obj.commutative_rings.rational_dual_y"), None, "owned"),
        ]
        images = [consume_image(port, *example) for example in examples]
        x_image, x_scalar, _ = images[-2]
        y_image, _, _ = images[-1]
        port.request("different retained quotient presentation", "op.rings.neg",
                     invoke("op.rings.neg", [y_image], ONE, y_image, y_image, x_scalar),
                     expected="error")
        receiver = examples[0][1]
        for label, request in (
                ("extra parameter", {"ctor": FUNCTOR, "args": [receiver], "receiver": receiver}),
                ("unordered parameters", {"ctor": FUNCTOR, "args": {}, "receiver": receiver}),
                ("missing receiver", node(FUNCTOR)),
                ("wrong action", {"ctor": "fun.sets.identity", "args": [], "receiver": receiver}),
                ("legacy unsuffixed map", invoke(FUNCTOR, [], receiver, receiver, receiver,
                                                 identity(receiver)))):
            port.request(label, FUNCTOR, request, expected="error")
        port.request("unsupported selected native ring", FUNCTOR,
                     object_request(node("obj.commutative_rings.reals")), expected="unsupported")
        port.request("map action is not registered", FUNCTOR + "#map",
                     invoke(FUNCTOR + "#map", [], x_image, x_image, x_image, identity(x_image),
                            node("map", node(FUNCTOR), identity(examples[-2][1], True))),
                     expected="unsupported")
        primary_requests = port.requests
    # The supplying connection has closed before another engine is started.
    # Neither a wrapper nor reusing an operation transfers one of its tokens.
    with Port(backend, environment) as foreign:
        foreign.request("foreign image on target operation", "op.rings.neg",
                        invoke("op.rings.neg", [x_image], ONE, x_image, x_image, x_scalar),
                        expected="unsupported")
        foreign.request("nested foreign input dependency", FUNCTOR,
                        object_request(node("valueData", x_image)), expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"objectRepresentations": len(examples),
                      "primaryConnectionRequests": primary_requests,
                      "foreignOwnerRequests": foreign_requests,
                      "checks": "public framing, actual image/scalar reuse and ownership only"}))


if __name__ == "__main__":
    main()
