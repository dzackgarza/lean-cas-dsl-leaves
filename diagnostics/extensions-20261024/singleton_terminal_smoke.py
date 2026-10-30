#!/usr/bin/env python3
"""Public singleton-comparison framing, reuse, and ownership checks.

Only the leaf process and released public contract are used. No computed
arithmetic value, equality truth, inverse law, or acceptance outcome is asserted.
"""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path

from completion_smoke import (ONE, Port, comparison, equality_reply, fields,
                              identity, invoke, node, owned, payload, require)


COMPARISON = "cmp.sets.singleton_terminal"
TERMINAL = node("obj.sets.terminal")
TRUTH = node("obj.sets.truth_values")


def arrow(inverse=False):
    return node("presentation", COMPARISON, [], inverse)


def manifest_check(contract):
    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    api = json.loads((contract / "api" / "declared-ports.json").read_text())
    rows = [row for row in manifest["registrations"] if row["operation"] == COMPARISON]
    require(len(rows) == 1 and rows[0]["input"] == COMPARISON,
            "the comparison requires its own complete-request registration")
    require(COMPARISON in {row["operation"] for row in api["operations"]}
            and COMPARISON in {row["input"] for row in api["inputForms"]},
            "the comparison pair is absent from the public inventories")
    declaration, = [row for row in api["entries"] if row["id"] == COMPARISON]
    require(len(declaration["declarations"]) == 1, "the published comparison declaration changed")


def point_shape(value, inverse, label):
    data = payload(value)
    require(type(data) is int if inverse else isinstance(data, list) and not data,
            label + ": result is not in its declared point-data shape")


def point_checks(port):
    value = port.request("named forward point", COMPARISON, comparison([], False, ONE, TERMINAL, 0))
    point_shape(value, False, "named forward point")
    backward = port.request("reuse returned terminal point", COMPARISON,
                            comparison([], True, TERMINAL, ONE, value))
    point_shape(backward, True, "returned terminal point")
    point_shape(port.request("reuse returned singleton point", COMPARISON,
                             comparison([], False, ONE, TERMINAL, backward)), False, "returned singleton point")
    # The registered global-point source keeps its published scalar convention.
    point_shape(port.request("named global-domain identity", COMPARISON,
                             comparison([], False, ONE, TERMINAL, identity(ONE, True))),
                False, "global-domain convention")
    for inverse, source, target, point in ((False, ONE, TERMINAL, 0),
                                            (True, TERMINAL, ONE, [])):
        for label, argument in (("selected point", node("element", source, point)),
                                 ("wrapped point", node("valueData", point))):
            result = port.request(label + "/" + str(inverse), COMPARISON,
                                  invoke(COMPARISON, [], ONE, source, target, argument, arrow(inverse)))
            point_shape(result, inverse, label)


def pipeline(port, label, source, target, source_point, target_point):
    forward = owned(port.request(label + "/whole forward", COMPARISON,
                                  comparison([], False, source, target, identity(source, True))))
    backward = owned(port.request(label + "/whole inverse", COMPARISON,
                                   comparison([], True, target, source, identity(target, True))))
    forward_map = node("typedMap", source, target, forward)
    backward_map = node("typedMap", target, source, backward)
    equality_reply(port, label + "/forward interface", source, target, forward_map,
                   node("valueData", forward_map))
    equality_reply(port, label + "/inverse interface", target, source, backward_map,
                   node("valueData", backward_map))
    reused = owned(port.request(label + "/returned callable input", COMPARISON,
                                 comparison([], True, target, source, forward_map)))
    equality_reply(port, label + "/retained original domain", source, source, reused, reused)
    composite = node("typedMap", source, source, node("compose", forward_map, backward_map))
    composed = owned(port.request(label + "/actual callable composition", COMPARISON,
                                   comparison([], False, source, target, composite)))
    equality_reply(port, label + "/composite interface", source, target, composed, composed)
    for inverse, domain, codomain, point in ((False, source, target, source_point),
                                             (True, target, source, target_point)):
        result = port.request(label + "/point data reuse/" + str(inverse), COMPARISON,
                              comparison([], inverse, domain, codomain, node("valueData", point)))
        point_shape(result, inverse, label)
        common = owned(port.request(label + "/whole common apply/" + str(inverse), COMPARISON,
                                     invoke(COMPARISON, [], domain, domain, codomain,
                                            identity(domain, True), arrow(inverse))))
        equality_reply(port, label + "/common callable interface/" + str(inverse),
                       domain, codomain, common, common)
    domain = node("obj.sets.fin", 3)
    family = node("typedMap", domain, source,
                  node("finiteGraph", [0, 1, 2], [[index, source_point] for index in range(3)]))
    generalized = owned(port.request(label + "/generalized forward", COMPARISON,
                                      comparison([], False, source, target, family)))
    continued = owned(port.request(label + "/generalized inverse reuse", COMPARISON,
                                    comparison([], True, target, source,
                                               node("typedMap", domain, target, generalized))))
    equality_reply(port, label + "/generalized retained domain", domain, source, continued, continued)
    return {"source": source, "target": target, "forward": forward_map, "backward": backward_map}


def infinite_domain_checks(port, source):
    domain = node("obj.sets.rationals")
    terminal_map = node("powerObjectMap", "pow.sets", "terminal", [domain])
    original = node("typedMap", domain, source, terminal_map)
    result = owned(port.request("infinite generalized domain", COMPARISON,
                                comparison([], False, source, TERMINAL, original)))
    actual = node("typedMap", domain, TERMINAL, result)
    continued = owned(port.request("infinite returned callable reuse", COMPARISON,
                                   comparison([], True, TERMINAL, source, actual)))
    # A complete typed use checks the retained infinite domain. A closed point
    # consumer exercises the original native callable without sampling equality
    # of an infinite map or asserting the truth of any computed equality.
    point = node("typedMap", ONE, domain, node("finiteGraph", [0], [[0, [2, 7]]]))
    forward_point = node("point", node("typedMap", ONE, TERMINAL, node("compose", point, actual)))
    observed = port.request("closed consumer of infinite callable", "mor.sets.equality",
                            invoke("mor.sets.equality", [TERMINAL], ONE,
                                   node("objectProduct", TERMINAL, TERMINAL), TRUTH,
                                   [forward_point, forward_point]))
    require(type(payload(observed)) is bool, "terminal equality consumer did not return Boolean data")
    original = node("typedMap", domain, source, continued)
    owned(port.request("second infinite continuation", COMPARISON,
                       comparison([], False, source, TERMINAL, original)))
    return actual


def malformed_checks(port, case):
    source, target = case["source"], case["target"]
    proper = comparison([], False, source, target, identity(source, True))
    cases = []
    packet = deepcopy(proper)
    packet["args"].pop()
    cases.append(("missing argument", packet))
    packet = deepcopy(proper)
    packet["args"].append(None)
    cases.append(("extra field", packet))
    for bad in (0, 1, "false", None):
        packet = deepcopy(proper)
        packet["args"][1] = bad
        cases.append(("nonboolean direction/" + repr(bad), packet))
    for parameters in ([ONE], {}, None):
        packet = deepcopy(proper)
        packet["args"][0] = parameters
        cases.append(("wrong parameters/" + repr(parameters), packet))
    cases.extend((
        ("inverse without swapped endpoints", comparison([], True, source, target, 0)),
        ("wrong singleton dimension", comparison([], False, node("obj.sets.fin", 2), target, 0)),
        ("substituted terminal object", comparison([], False, source, ONE, 0)),
        ("empty source inventory", comparison([], False, node("finiteData", ONE, []), target, 0)),
        ("wrong source point inventory", comparison([], False, node("finiteData", ONE, [True]), target, True)),
        ("empty target inventory", comparison([], False, source, node("finiteData", TERMINAL, []), 0)),
        ("wrong terminal point inventory", comparison([], False, source, node("finiteData", TERMINAL, [0]), 0)),
        ("malformed source literal", comparison([], False, source, target, False)),
        ("malformed terminal literal", comparison([], True, target, source, 0)),
        ("changed owned callable endpoint", comparison([], False, source, target,
            node("typedMap", target, source, case["forward"]))),
        ("changed common-apply parameters", invoke(COMPARISON, [ONE], source, source, target,
                                                    identity(source), arrow())),
        ("changed common-apply action", invoke(COMPARISON, [], source, source, target,
                                              identity(source), node("presentation", "cmp.sets.fin_reversal", [1], False))),
    ))
    for label, packet in cases:
        port.request(label, COMPARISON, packet, expected="error")


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
    with Port(backend, environment) as port:
        point_checks(port)
        source = node("finiteData", ONE, [0])
        case = pipeline(port, "supplied singleton inventory", source, TERMINAL, 0, [])
        wrapped_source = node("valueData", node("finiteData", ONE, [node("valueData", 0)]))
        wrapped_target = node("valueData", node("finiteData", TERMINAL, [node("valueData", [])]))
        pipeline(port, "retained wrapped keys", wrapped_source, wrapped_target,
                 node("valueData", 0), node("valueData", []))
        endpoint_source = node("morphismEndpoint", arrow(), "source")
        endpoint_target = node("morphismEndpoint", arrow(), "target")
        pipeline(port, "complete endpoint fields", endpoint_source, endpoint_target, 0, [])
        infinite = infinite_domain_checks(port, source)
        malformed_checks(port, case)
        primary_requests = port.requests
    with Port(backend, environment) as foreign:
        for label, packet in (
                ("closed returned comparison", comparison([], True, TERMINAL, source, case["forward"])),
                ("closed nested endpoint owner", comparison([], False,
                    node("morphismEndpoint", node("valueData", case["forward"]), "source"), TERMINAL, 0)),
                ("closed infinite family", comparison([], True, TERMINAL, source,
                    node("valueData", infinite)))):
            foreign.request(label, COMPARISON, packet, expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"script": Path(__file__).name, "primaryConnectionRequests": primary_requests,
                      "foreignOwnerRequests": foreign_requests,
                      "result": "public protocol conformance completed",
                      "boundary": "No mathematical answer or acceptance outcome asserted."}, indent=2))


if __name__ == "__main__":
    main()
