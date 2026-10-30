#!/usr/bin/env python3
"""Public-port engineering checks for ordinary bilinear-module forgetting.

Checks cover framing, complete selections, actual returned module/callable reuse,
and live ownership. No pairing value, arithmetic answer, equality truth, functor
law, or mathematical acceptance outcome is asserted. Only the leaf process and
the released public contract are used; no kernel or engine internals are imported.
"""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path

from completion_smoke import (ONE, equality_reply, fields, identity, invoke,
                              node, owned, payload, require)
from lift_images_smoke import LiftPort, image_packet
from module_functor_smoke import FIBRE, UNDERLYING, map_request, object_request


FORGET = "fun.bilin_module.forget"
Q = node("obj.sets.rationals")
SOURCE = node("obj.bilin_module.degenerate_plane")
TARGET = node("obj.bilin_module.degenerate_plane_target")
POINT = [[0, [0, 1]], [1, [0, 1]]]


def manifest_check(contract):
    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    api = json.loads((contract / "api" / "declared-ports.json").read_text())
    operations = {row["operation"] for row in api["operations"]}
    inputs = {row["input"] for row in api["inputForms"]}
    functor, = [row for row in api["functors"] if row["id"] == FORGET]
    require(functor["input"] == FORGET + "#input", "the public request address changed")
    for operation in (FORGET, FORGET + "#map"):
        rows = [row for row in manifest["registrations"] if row["operation"] == operation]
        require(len(rows) == 1 and rows[0]["input"] == functor["input"],
                "each action requires exactly its published complete-request registration")
        require(operation in operations and rows[0]["input"] in inputs,
                "a forgetful registration is absent from the public inventories")


def vector_reply(value, label):
    data = payload(value)
    require(isinstance(data, list), label + ": vector result is not a finite callable")
    for entry in data:
        require(isinstance(entry, list) and len(entry) == 2 and type(entry[0]) is int,
                label + ": vector entry framing changed")
        require(isinstance(entry[1], list) and len(entry[1]) == 2
                and all(type(value) is int for value in entry[1]),
                label + ": rational coefficient framing changed")


def pipeline(port, label, parameters, source, target, original):
    image_source = owned(port.request(label + "/source image", FORGET,
                                      object_request(FORGET, parameters, source)))
    image_target = owned(port.request(label + "/target image", FORGET,
                                      object_request(FORGET, parameters, target)))
    request = map_request(FORGET, parameters, original, image_source, image_target)
    total = owned(port.request(label + "/whole map", FORGET + "#map", request))
    continued = owned(port.request(label + "/reuse whole map", FORGET + "#map",
                                    map_request(FORGET, parameters, identity(target, True),
                                                image_target, image_target, image_source, total)))
    for suffix, argument in (("raw point", POINT),
                             ("selected point", node("element", image_source, POINT))):
        result = port.request(label + "/" + suffix, FORGET + "#map",
                              map_request(FORGET, parameters, original,
                                          image_source, image_target, ONE, argument))
        vector_reply(result, label + "/" + suffix)
    domain = node("obj.sets.fin", 2)
    graph = node("typedMap", domain, image_source,
                 node("finiteGraph", [0, 1], [[0, POINT], [1, POINT]]))
    family = owned(port.request(label + "/generalized argument", FORGET + "#map",
                                map_request(FORGET, parameters, original,
                                            image_source, image_target, domain, graph)))
    reused_family = owned(port.request(label + "/reuse generalized result", FORGET + "#map",
                                       map_request(FORGET, parameters, identity(target, True),
                                                   image_target, image_target, domain, family)))
    equality_reply(port, label + "/generalized callable interface", domain, image_target,
                   family, reused_family)
    # Subsequent registered actions consume the actual returned module and map.
    fibre_source = owned(port.request(label + "/fibre source", FIBRE,
                                      object_request(FIBRE, [parameters[0]], image_source)))
    fibre_target = owned(port.request(label + "/fibre target", FIBRE,
                                      object_request(FIBRE, [parameters[0]], image_target)))
    mapped = owned(port.request(label + "/fibre map reuse", FIBRE + "#map",
                                map_request(FIBRE, [parameters[0]],
                                            node("typedMap", image_source, image_target, continued),
                                            fibre_source, fibre_target)))
    set_source = owned(port.request(label + "/underlying source", UNDERLYING,
                                    object_request(UNDERLYING, [], fibre_source)))
    set_target = owned(port.request(label + "/underlying target", UNDERLYING,
                                    object_request(UNDERLYING, [], fibre_target)))
    set_map = owned(port.request(label + "/underlying map reuse", UNDERLYING + "#map",
                                 map_request(UNDERLYING, [],
                                             node("typedMap", fibre_source, fibre_target, mapped),
                                             set_source, set_target)))
    equality_reply(port, label + "/whole callable interface", set_source, set_target,
                   set_map, node("valueData", set_map))
    scalar = port.request(label + "/native module consumer", "op.modules.scalar_action",
                          invoke("op.modules.scalar_action", [parameters[0], image_source], ONE,
                                 node("objectProduct", parameters[0], image_source), image_source,
                                 [[3, 2], POINT]))
    vector_reply(scalar, label + "/native module consumer")
    return {"parameters": parameters, "source": source, "target": target,
            "original": original, "imageSource": image_source, "imageTarget": image_target,
            "request": request, "total": total, "setSource": set_source}


def owned_form_checks(port, case):
    source, target = case["imageSource"], case["imageTarget"]
    original = node("arrow", source, target, node("typedMap", source, target, case["total"]))
    kernel = payload(port.request("returned map to native kernel", "fun.arrows_modules.kernel",
                                  object_request("fun.arrows_modules.kernel", [Q], original)))
    apex, ambient, inclusion = fields(kernel, "arrow", 3)
    require(ambient == source, "the kernel changed its actual ambient endpoint")
    lift = "lift.bilin_module.restrict"
    parameters = [Q, Q]
    base = node("subobject", apex, ambient, inclusion)
    packet = image_packet("monoLiftInput", lift, node(FORGET, *parameters), SOURCE,
                          base, [], parameters, source)
    formed = owned(port.request("actual owned formed result", lift + "#obj", packet))
    hom_packet = deepcopy(packet)
    hom_packet["args"][4] = [formed]
    hom = port.request("actual owned formed arrow", lift + "#hom", hom_packet)
    actual_source, actual_target, body = fields(hom, "typedMap", 3)
    require(actual_source == formed and actual_target == SOURCE,
            "the returned formed arrow changed an original endpoint")
    owned(body)
    pipeline(port, "owned form and callable", parameters, formed, SOURCE, hom)
    wrapped = node("valueData", node("valueData", formed))
    pipeline(port, "wrapped owned form", parameters, wrapped, wrapped, identity(wrapped, True))
    return formed, hom


def malformed_checks(port, case):
    parameters = case["parameters"]
    for label, packet in (
            ("missing receiver", node(FORGET, *parameters)),
            ("missing W", object_request(FORGET, [Q], SOURCE)),
            ("extra parameter", object_request(FORGET, parameters + [Q], SOURCE)),
            ("unordered parameters", {"ctor": FORGET, "args": {}, "receiver": SOURCE}),
            ("different object action", object_request(UNDERLYING, parameters, SOURCE)),
            ("different scalar ring", object_request(FORGET, [node("obj.sets.integers"), Q], SOURCE)),
            ("different value-module scalars", object_request(FORGET,
                [Q, node("obj.modules.regular", node("obj.rings.integers"))], SOURCE)),
            ("unsuffixed map", invoke(FORGET, parameters, SOURCE, SOURCE, SOURCE, identity(SOURCE)))):
        port.request(label, FORGET, packet, expected="error")
    for label, receiver, values in (("unsupported receiver", node("obj.modules.regular", Q), Q),
                                    ("unsupported W", SOURCE, node("obj.sets.naturals"))):
        port.request(label, FORGET, object_request(FORGET, [Q, values], receiver), expected="unsupported")
    mutations = []
    packet = deepcopy(case["request"])
    packet["args"].pop()
    mutations.append(("missing generalized argument", packet))
    packet = deepcopy(case["request"])
    packet["args"][1] = [Q]
    mutations.append(("changed outer parameters", packet))
    for label, new_parameters in (("wrong arity in both copies", [Q]),
                                  ("changed W in both copies", [Q, node("objectProduct", Q, Q)])):
        packet = deepcopy(case["request"])
        packet["args"][1] = new_parameters
        packet["args"][2]["args"][0]["args"] = new_parameters
        mutations.append((label, packet))
    packet = deepcopy(case["request"])
    packet["args"][2]["args"][0] = node(FIBRE, Q)
    mutations.append(("wrong map action", packet))
    packet = deepcopy(case["request"])
    packet["args"][2]["args"][1] = identity(SOURCE)
    mutations.append(("untyped original", packet))
    packet = deepcopy(case["request"])
    packet["args"][2]["args"][1] = node("typedMap", SOURCE, TARGET)
    mutations.append(("omitted original callable", packet))
    packet = deepcopy(case["request"])
    packet["args"][2]["args"][1]["args"][0] = TARGET
    mutations.append(("changed original source", packet))
    packet = deepcopy(case["request"])
    packet["args"][4], packet["args"][5] = packet["args"][5], packet["args"][4]
    mutations.append(("swapped returned images", packet))
    packet = deepcopy(case["request"])
    packet["args"][4] = case["setSource"]
    mutations.append(("image of another action", packet))
    packet = deepcopy(case["request"])
    packet["args"][2]["args"][1]["args"][2] = identity(TARGET, True)
    mutations.append(("changed retained callable endpoints", packet))
    for label, packet in mutations:
        port.request(label, FORGET + "#map", packet, expected="error")
    symbolic = node("functorAction", node(FORGET, *parameters), SOURCE)
    port.request("symbolic image is not an actual returned image", FORGET + "#map",
                 map_request(FORGET, parameters, identity(SOURCE, True), symbolic, symbolic),
                 expected="unsupported")


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
    with LiftPort(backend, environment) as port:
        arrow = node("mor.bilin_module.degenerate_plane_map")
        original = node("typedMap", SOURCE, TARGET, arrow)
        case = pipeline(port, "named form", [Q, Q], SOURCE, TARGET, original)
        diagonal = node("obj.bilin_module.rational_diagonal_2_3")
        pipeline(port, "other named form", [Q, Q], diagonal, diagonal, identity(diagonal, True))
        paired = node("obj.bilin_module.degenerate_plane_with_dot")
        pipeline(port, "product value module", [Q, node("objectProduct", Q, Q)],
                 paired, paired, identity(paired, True))
        changed = node("functorAction", node("fun.bilin_module.change_value", Q, Q, Q,
                                             identity(Q, True)), SOURCE)
        pipeline(port, "portable change-value form", [Q, Q], changed, changed, identity(changed, True))
        endpoints = [node("morphismEndpoint", arrow, side) for side in ("source", "target")]
        pipeline(port, "portable morphism endpoints", [Q, Q], *endpoints,
                 node("typedMap", *endpoints, arrow))
        selected_apex = node("subobjectApex", node("subobject", SOURCE, SOURCE, identity(SOURCE, True)))
        pipeline(port, "portable subobject apex", [Q, Q], selected_apex, selected_apex,
                 identity(selected_apex, True))
        values = owned(port.request("actual owned value-module parameter", FIBRE,
                                    object_request(FIBRE, [Q], node("obj.modules.regular", Q))))
        owned_parameters = [node("valueData", Q), node("valueData", values)]
        pipeline(port, "complete owned parameters", owned_parameters, SOURCE, SOURCE, identity(SOURCE, True))
        formed, hom = owned_form_checks(port, case)
        malformed_checks(port, case)
        primary_requests = port.requests
    with LiftPort(backend, environment) as foreign:
        for label, operation, packet in (
                ("closed source Form", FORGET, object_request(FORGET, [Q, Q], formed)),
                ("closed nested value module", FORGET, object_request(FORGET, owned_parameters, SOURCE)),
                ("closed returned module", FIBRE, object_request(FIBRE, [Q], case["imageSource"])),
                ("closed callable and images", FORGET + "#map", case["request"]),
                ("closed nested original callable", FORGET,
                 object_request(FORGET, [Q, Q], node("morphismEndpoint", node("valueData", hom), "source")))):
            foreign.request(label, operation, packet, expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"script": Path(__file__).name, "primaryConnectionRequests": primary_requests,
                      "foreignOwnerRequests": foreign_requests,
                      "result": "public protocol conformance completed",
                      "boundary": "No mathematical answer or acceptance outcome asserted."}, indent=2))


if __name__ == "__main__":
    main()
