#!/usr/bin/env python3
"""Focused public-port conformance for the two existing module functors.

Only packet framing, returned-data consumption, selected endpoints/parameters
and ownership are checked. No arithmetic result, equality truth, functor law or
mathematical acceptance outcome is asserted. No kernel or engine code is imported.
"""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path

from completion_smoke import (ONE, Port, equality_reply, fields, identity, invoke,
                              node, owned, payload, require)


FIBRE = "fun.modules.fibre_inclusion"
UNDERLYING = "fun.modules.underlying"


def object_request(operation, parameters, receiver):
    return {"ctor": operation, "args": parameters, "receiver": receiver}


def map_request(operation, parameters, original, image_source, image_target,
                domain=None, argument=None):
    if domain is None:
        domain, argument = image_source, identity(image_source)
    return invoke(operation + "#map", parameters, domain, image_source, image_target,
                  argument, node("map", node(operation, *parameters), original))


def pipeline(port, label, ring, source, target, arrow, point, scalar_kind=None):
    image_source = owned(port.request(label + "/source fibre image", FIBRE,
                                      object_request(FIBRE, [ring], source)))
    image_target = owned(port.request(label + "/target fibre image", FIBRE,
                                      object_request(FIBRE, [ring], target)))
    original = node("typedMap", source, target, arrow)
    request = map_request(FIBRE, [ring], original, image_source, image_target)
    total_map = owned(port.request(label + "/whole fibre map", FIBRE + "#map", request))
    # Reuse the actual returned total arrow as a generalized argument. This
    # preserves its original domain even when the next action is an identity.
    continued = owned(port.request(label + "/reuse total arrow", FIBRE + "#map",
                                    map_request(FIBRE, [ring], identity(target, True),
                                                image_target, image_target,
                                                image_source, total_map)))
    set_source = owned(port.request(label + "/source underlying image", UNDERLYING,
                                    object_request(UNDERLYING, [], image_source)))
    set_target = owned(port.request(label + "/target underlying image", UNDERLYING,
                                    object_request(UNDERLYING, [], image_target)))
    total = node("typedMap", image_source, image_target, continued)
    request = map_request(UNDERLYING, [], total, set_source, set_target)
    set_map = owned(port.request(label + "/whole underlying map", UNDERLYING + "#map", request))
    # This target operation consumes actual callable data. Only its Boolean
    # result shape is checked, never its computed truth value.
    equality_reply(port, label + "/returned callable interface", set_source, set_target,
                   set_map, node("valueData", set_map))
    for suffix, argument in (("raw point", point),
                             ("selected point", node("element", set_source, point))):
        result = port.request(label + "/" + suffix, UNDERLYING + "#map",
                              map_request(UNDERLYING, [], total, set_source, set_target,
                                          ONE, argument))
        if scalar_kind == "rational":
            data = payload(result)
            require(isinstance(data, list) and len(data) == 2 and
                    all(type(value) is int for value in data),
                    label + ": rational result framing changed")
        elif scalar_kind == "modular":
            require(type(payload(result)) is int, label + ": modular result framing changed")
        else:
            require(isinstance(payload(result), list), label + ": vector result framing changed")
    domain = node("obj.sets.fin", 2)
    graph = node("typedMap", domain, set_source,
                 node("finiteGraph", [0, 1], [[0, point], [1, point]]))
    family = owned(port.request(label + "/generalized domain", UNDERLYING + "#map",
                                map_request(UNDERLYING, [], total, set_source, set_target,
                                            domain, graph)))
    continuation = map_request(UNDERLYING, [], identity(image_target, True),
                               set_target, set_target, domain, family)
    owned(port.request(label + "/reuse generalized result", UNDERLYING + "#map", continuation))
    equality_reply(port, label + "/generalized result interface", domain, set_target, family, family)
    return {"ring": ring, "source": source, "target": target, "original": original,
            "fibreSource": image_source, "fibreTarget": image_target,
            "totalMap": total_map, "setSource": set_source, "setTarget": set_target,
            "setMap": set_map, "total": total, "underlyingRequest": request}


def manifest_check(contract):
    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    api = json.loads((contract / "api" / "declared-ports.json").read_text())
    operations = {row["operation"] for row in api["operations"]}
    inputs = {row["input"] for row in api["inputForms"]}
    for functor in (FIBRE, UNDERLYING):
        for operation in (functor, functor + "#map"):
            rows = [row for row in manifest["registrations"] if row["operation"] == operation]
            require(len(rows) == 1 and rows[0]["input"] == functor + "#input",
                    "each module action requires exactly its complete-request registration")
            require(operation in operations and rows[0]["input"] in inputs,
                    "a module registration is absent from the published inventories")


def wrapper_and_legacy_checks(port, case):
    ring, source, target = case["ring"], case["source"], case["target"]
    wrapped_source = node("valueData", case["fibreSource"])
    wrapped_target = node("valueData", case["fibreTarget"])
    actual = owned(port.request("wrapped actual image interfaces", FIBRE + "#map",
                                map_request(FIBRE, [ring], case["original"],
                                            wrapped_source, wrapped_target)))
    set_source = owned(port.request("wrapped source image object", UNDERLYING,
                                    object_request(UNDERLYING, [], wrapped_source)))
    set_target = owned(port.request("wrapped target image object", UNDERLYING,
                                    object_request(UNDERLYING, [], wrapped_target)))
    original = node("typedMap", wrapped_source, wrapped_target, node("valueData", actual))
    result = owned(port.request("reuse complete wrapped map", UNDERLYING + "#map",
                                map_request(UNDERLYING, [], original, set_source, set_target)))
    equality_reply(port, "wrapped callable endpoints", set_source, set_target, result, result)
    # Existing target consumers may still receive the explicitly supported
    # symbolic carrier-map descriptors as nested data. New registrations do
    # not remove those pre-existing readers or replace actual #map images.
    total = node("functorAction", node(FIBRE, ring), source)
    underlying = node("functorAction", node(UNDERLYING), total)
    for typed in (False, True):
        fibre_map = node("map", node(FIBRE, ring), identity(source, typed))
        original = node("typedMap", total, total, fibre_map) if typed else fibre_map
        carrier_map = node("map", node(UNDERLYING), original)
        equality_reply(port, "existing nested symbolic map/%s" % typed,
                       underlying, underlying, carrier_map, carrier_map)
    port.request("symbolic image cannot replace an actual map result", FIBRE + "#map",
                 map_request(FIBRE, [ring], identity(source, True), total, total),
                 expected="unsupported")


def malformed_checks(port, case):
    source, ring = case["source"], case["ring"]
    for operation, parameters, receiver in (
            (FIBRE, [ring], source), (UNDERLYING, [], case["fibreSource"])):
        for label, packet in (
                ("missing receiver", node(operation, *parameters)),
                ("extra parameter", object_request(operation, parameters + [ring], receiver)),
                ("unordered parameters", {"ctor": operation, "args": {}, "receiver": receiver}),
                ("wrong action", object_request("fun.sets.identity", parameters, receiver)),
                ("legacy unsuffixed map", invoke(operation, parameters, receiver, receiver,
                                                 receiver, identity(receiver)))):
            port.request(operation + "/" + label, operation, packet, expected="error")
    proper = map_request(FIBRE, [ring], case["original"], case["fibreSource"], case["fibreTarget"])
    cases = []
    packet = deepcopy(proper)
    packet["args"][1] = []
    cases.append(("changed outer parameters", packet))
    packet = deepcopy(proper)
    packet["args"][1] = [node("obj.rings.integers")]
    packet["args"][2]["args"][0]["args"] = list(packet["args"][1])
    cases.append(("changed retained selection in both copies", packet))
    packet = deepcopy(proper)
    packet["args"][2]["args"][0] = node(UNDERLYING)
    cases.append(("changed map action", packet))
    packet = deepcopy(proper)
    packet["args"][2]["args"][1] = node("typedMap", source, case["target"])
    cases.append(("missing original callable", packet))
    packet = deepcopy(proper)
    packet["args"][2]["args"][1] = identity(source)
    cases.append(("untyped source arrow", packet))
    packet = deepcopy(proper)
    packet["args"][2]["args"][1]["args"][0] = case["target"]
    cases.append(("changed original endpoint", packet))
    packet = deepcopy(proper)
    packet["args"][4], packet["args"][5] = packet["args"][5], packet["args"][4]
    cases.append(("swapped actual images", packet))
    for label, packet in cases:
        port.request(label, FIBRE + "#map", packet, expected="error")
    packet = deepcopy(case["underlyingRequest"])
    packet["args"][1] = [ring]
    packet["args"][2]["args"][0]["args"] = [ring]
    port.request("extra underlying parameter in both copies", UNDERLYING + "#map", packet, expected="error")
    packet = deepcopy(case["underlyingRequest"])
    packet["args"][2]["args"][1]["args"][2] = node("typedMap", case["fibreTarget"],
                                                        case["fibreSource"], case["totalMap"])
    port.request("changed retained callable endpoints", UNDERLYING + "#map", packet, expected="error")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"))
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"))
    arguments = parser.parse_args()
    require(bool(arguments.contract), "the published contract checkout is required")
    contract = Path(arguments.contract).resolve()
    manifest_check(contract)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(contract / "python"))
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    backend = Path(__file__).with_name("backend.py").resolve()
    rational = node("obj.rings.rationals")
    with Port(backend, environment) as port:
        regular = node("obj.modules.regular", rational)
        pipeline(port, "rational regular", rational, regular, regular, identity(regular), [7, 11], "rational")
        modular = node("obj.rings.integers_mod", 9)
        finite_regular = node("finiteData", node("obj.modules.regular", modular), list(range(9)))
        finite_map = node("finiteGraph", list(range(9)),
                          [[point, node("element", finite_regular, point)] for point in range(9)])
        pipeline(port, "finite portable module", modular, finite_regular, finite_regular,
                 finite_map, 4, "modular")
        source = node("obj.modules.vectors", rational, 3)
        target = node("obj.modules.vectors", rational, 2)
        coefficients = [[0, [[0, [2, 1]], [1, [-1, 1]], [2, [3, 1]]]],
                        [1, [[0, [0, 1]], [1, [4, 1]], [2, [5, 1]]]]]
        arrow = node("mor.modules.rectangular_linear_map", 2, 3, rational, coefficients)
        vector = [[0, [3, 7]], [1, [2, 5]], [2, [-1, 9]]]
        case = pipeline(port, "rectangular rational map", rational, source, target, arrow, vector)
        empty = node("obj.modules.vectors", rational, 0)
        empty_map = node("mor.modules.rectangular_linear_map", 2, 0, rational, [[0, []], [1, []]])
        pipeline(port, "zero-dimensional source", rational, empty, target, empty_map, [])
        image_ring = owned(port.request("owned ring coefficient", "fun.commutative_rings.ring",
                                        object_request("fun.commutative_rings.ring", [],
                                                       node("obj.commutative_rings.integers_mod", 5))))
        owned_coefficient_module = node("obj.modules.vectors", image_ring, 2)
        pipeline(port, "owned coefficient vectors", image_ring, owned_coefficient_module,
                 owned_coefficient_module, identity(owned_coefficient_module), [[0, 2], [1, 3]])
        kernel = payload(port.request("actual kernel object", "fun.arrows_modules.kernel",
                                      object_request("fun.arrows_modules.kernel", [rational],
                                                     node("arrow", source, target,
                                                          node("typedMap", source, target, arrow)))))
        kernel_source, kernel_target, inclusion = fields(kernel, "arrow", 3)
        # Reuse the actual returned source and defining inclusion. No kernel
        # dimension, basis, equality or expected map value is asserted.
        kernel_case = pipeline(port, "actual kernel inclusion", rational, kernel_source,
                               kernel_target, inclusion, [[0, [0, 1]], [1, [0, 1]], [2, [0, 1]]])
        commutative = node("obj.commutative_rings.rationals")
        base_map = node("map", node("fun.commutative_rings.ring"),
                        node("mor.commutative_rings.integer_coefficients", commutative))
        scalar_source = node("functorAction", node("fun.commutative_rings.ring"),
                             node("obj.commutative_rings.integers"))
        scalar_target = node("functorAction", node("fun.commutative_rings.ring"), commutative)
        restricted = owned(port.request("actual restricted module", "fun.modules.reindex",
                                        object_request("fun.modules.reindex", [base_map],
                                                       node("obj.modules.regular", scalar_target))))
        pipeline(port, "actual scalar restriction", scalar_source, restricted, restricted,
                 identity(restricted), [5, 13], "rational")
        wrapper_and_legacy_checks(port, case)
        malformed_checks(port, case)
        port.request("unsupported module representation", FIBRE,
                     object_request(FIBRE, [rational], node("obj.modules.unimplemented")),
                     expected="unsupported")
        primary_requests = port.requests
    with Port(backend, environment) as foreign:
        for label, operation, packet in (
                ("closed fibre image", UNDERLYING,
                 object_request(UNDERLYING, [], case["fibreSource"])),
                ("nested closed kernel owner", FIBRE,
                 object_request(FIBRE, [rational], node("valueData", kernel_case["source"]))),
                ("closed mapped callable", UNDERLYING + "#map", case["underlyingRequest"])):
            foreign.request(label, operation, packet, expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"script": Path(__file__).name, "primaryConnectionRequests": primary_requests,
                      "foreignOwnerRequests": foreign_requests,
                      "result": "public protocol conformance completed",
                      "boundary": "No mathematical answer or acceptance outcome asserted."}, indent=2))


if __name__ == "__main__":
    main()
