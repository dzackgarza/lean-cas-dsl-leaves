#!/usr/bin/env python3
"""Public lift-image framing and live-data checks, with no mathematical assertions.

Only this leaf and the published port are launched. Checks concern packet shape,
exact supplied endpoints, subsequent consumption and live ownership; they do not
assert a computed pairing, equality answer, inverse equation or universal law.
"""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import sys

from completion_smoke import Port, equality_reply, fields, identity, owned, require
from smoke import node, read_frame


ABSENT = object()
Q = node("obj.sets.rationals")
SOURCE = node("obj.bilin_module.degenerate_plane")
MODULE = node("obj.modules.vectors", Q, 2)
RESTRICTION = "lift.bilin_module.restrict"
CHANGE_VALUE = "lift.bilin_module.change_value_restriction"


class LiftPort(Port):
    """The existing framed connection, accepting the lift's typed-map replies."""

    def request(self, label, operation, argument, expected="ok"):
        self.requests += 1
        packet = {"request_id": self.requests, "op": operation, "args": argument}
        encoded = json.dumps(packet, separators=(",", ":")).encode("utf-8")
        self.process.stdin.write(str(len(encoded)).encode("ascii") + b"\n" + encoded)
        self.process.stdin.flush()
        reply = read_frame(self.process.stdout)
        require(isinstance(reply, dict), label + ": reply is not a JSON object")
        require(reply.get("request_id") == self.requests, label + ": request identity changed")
        require(reply.get("status") == expected, label + ": " + json.dumps(reply))
        if expected == "unsupported":
            require(reply.get("op") == operation, label + ": unsupported operation changed")
            return None
        if expected == "error":
            require(isinstance(reply.get("kind"), str) and isinstance(reply.get("message"), str),
                    label + ": error framing is incomplete")
            return None
        require("value" in reply, label + ": successful reply has no value")
        return reply["value"]


def image_packet(kind, lift, action, source, base, outputs, parameters,
                 source_image=ABSENT, comparison_image=ABSENT):
    packet = node(kind, lift, action, source, base, outputs[:])
    packet["parameters"] = parameters
    if source_image is not ABSENT:
        packet["sourceImage"] = source_image
    if comparison_image is not ABSENT:
        packet["comparisonImage"] = comparison_image
    return packet


def endpoints(value, source, target, label):
    actual_source, actual_target, body = fields(value, "typedMap", 3)
    require(actual_source == source and actual_target == target,
            label + ": a retained endpoint changed")
    owned(body)


def selection(lift):
    if lift == RESTRICTION:
        parameters = [Q, Q]
        return parameters, node("fun.bilin_module.forget", *parameters), MODULE
    parameters = [Q, Q, Q, identity(Q, True)]
    return parameters, node("fun.bilin_module.change_value", *parameters), SOURCE


def cycle(port, lift, kind, actual, source=SOURCE, ambient=None, preselected=ABSENT):
    parameters, action, default_ambient = selection(lift)
    if ambient is None:
        ambient = default_ambient if actual else node("functorAction", action, source)
    base = node("subobject", ambient, ambient, identity(ambient, True))
    original = node("arrow", source, source, identity(source, True)) if kind == "liftInput" else source
    source_image = (node("arrow", ambient, ambient, identity(ambient, True))
                    if kind == "liftInput" else ambient) if actual else ABSENT
    outputs, packets = [], []
    changed = ABSENT
    label = lift + "/" + kind + ("/actual" if actual else "/legacy")
    for component in ("obj", "hom", "forward", "backward"):
        comparison_image = preselected if component == "forward" else ABSENT
        if component == "backward" and actual:
            comparison_image = changed
        packet = image_packet(kind, lift, action, original, base, outputs, parameters,
                              source_image, comparison_image)
        packets.append(packet)
        output = port.request(label + "/" + component, lift + "#" + component, packet)
        outputs.append(output)
        if component == "obj":
            owned(output)
        elif component == "hom":
            endpoints(output, outputs[0], source, label + "/hom")
        elif component == "forward":
            changed = fields(output, "typedMap", 3)[0]
            if preselected is not ABSENT:
                require(changed == preselected, label + ": supplied image was replaced")
            elif actual:
                owned(changed)
            else:
                require(changed == node("functorAction", action, outputs[0]),
                        label + ": legacy image recipe changed")
            endpoints(output, changed, ambient, label + "/forward")
        else:
            endpoints(output, ambient, changed, label + "/backward")

    factor = node("liftFactorInput", lift, action, source, base, outputs[:], outputs[2], outputs[1])
    factor["parameters"] = parameters
    if actual:
        factor.update(sourceImage=ambient, comparisonImage=changed)
    factor_output = port.request(label + "/factor", lift + "#factor", factor)
    endpoints(factor_output, outputs[0], outputs[0], label + "/factor")
    # Exercise the owned image's native reader without asserting the Boolean.
    equality_reply(port, label + "/owned comparison reuse", changed, changed,
                   node("compose", outputs[2], outputs[3]), identity(changed, True))
    return {"lift": lift, "parameters": parameters, "action": action, "source": source,
            "base": base, "ambient": ambient, "outputs": outputs, "image": changed,
            "packets": packets, "factor": factor}


def malformed_checks(port, actual, prescribed):
    lift = actual["lift"]
    obj, hom, forward, backward = actual["packets"]
    cases = []

    packet = deepcopy(obj)
    packet["sourceImage"] = None
    cases.append(("null source", "obj", packet))
    packet = deepcopy(obj)
    del packet["sourceImage"]
    packet["comparisonImage"] = actual["image"]
    cases.append(("comparison without source", "obj", packet))
    for stage, original in (("obj", obj), ("hom", hom)):
        packet = deepcopy(original)
        packet["comparisonImage"] = actual["image"]
        cases.append(("premature comparison " + stage, stage, packet))
    packet = deepcopy(forward)
    packet["comparisonImage"] = None
    cases.append(("null comparison", "forward", packet))
    packet = deepcopy(backward)
    del packet["comparisonImage"]
    cases.append(("missing retained comparison", "backward", packet))
    packet = deepcopy(backward)
    packet["comparisonImage"] = MODULE
    cases.append(("replacement comparison endpoint", "backward", packet))
    packet = deepcopy(obj)
    packet["sourceImage"] = node("obj.modules.vectors", Q, 3)
    cases.append(("replacement source endpoint", "obj", packet))
    packet = deepcopy(prescribed["packets"][0])
    packet["sourceImage"] = prescribed["ambient"]
    cases.append(("prescribed image without Arrow", "obj", packet))
    packet = deepcopy(actual["factor"])
    del packet["comparisonImage"]
    cases.append(("factor missing comparison", "factor", packet))
    packet = deepcopy(actual["factor"])
    packet["sourceImage"] = node("obj.modules.vectors", Q, 3)
    cases.append(("factor replacement source", "factor", packet))
    packet = deepcopy(actual["factor"])
    del packet["sourceImage"]
    del packet["comparisonImage"]
    cases.append(("actual endpoints relabelled legacy", "factor", packet))
    for label, component, packet in cases:
        port.request("metadata/" + label, lift + "#" + component, packet, expected="error")
    return len(cases)


def ownership_checks(port, actual):
    with LiftPort(port.backend, port.environment) as foreign:
        packet = deepcopy(actual["packets"][0])
        packet["sourceImage"] = actual["image"]
        foreign.request("owner/actual source image", actual["lift"] + "#obj", packet,
                        expected="unsupported")
        # Preserve a foreign owner in a source Arrow field unused by pullback.
        packet = deepcopy(actual["packets"][0])
        source = actual["source"]
        packet["ctor"] = "liftInput"
        packet["args"][2] = node("arrow", source, source, identity(source, True))
        packet["sourceImage"] = node("arrow", actual["ambient"], actual["ambient"],
                                     actual["outputs"][2])
        foreign.request("owner/nested source-image callable", actual["lift"] + "#obj", packet,
                        expected="unsupported")
        # All other dependencies now belong to this connection.
        packet = deepcopy(actual["packets"][0])
        obj = foreign.request("owner/local obj", actual["lift"] + "#obj", packet)
        packet["args"][4] = [obj]
        hom = foreign.request("owner/local hom", actual["lift"] + "#hom", packet)
        packet["args"][4] = [obj, hom]
        packet["comparisonImage"] = actual["image"]
        foreign.request("owner/actual comparison image", actual["lift"] + "#forward", packet,
                        expected="unsupported")
        return foreign.requests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"))
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"))
    arguments = parser.parse_args()
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    if arguments.contract:
        public_python = str(Path(arguments.contract).resolve() / "python")
        environment["PYTHONPATH"] = public_python + os.pathsep + environment.get("PYTHONPATH", "")
    with LiftPort(Path(__file__).resolve().with_name("backend.py"), environment) as port:
        contexts = []
        for lift in (RESTRICTION, CHANGE_VALUE):
            cycle(port, lift, "monoLiftInput", False)
            actual = cycle(port, lift, "monoLiftInput", True)
            prescribed = cycle(port, lift, "liftInput", True, source=actual["outputs"][0],
                               ambient=actual["image"], preselected=actual["image"])
            contexts.append((actual, prescribed))
        malformed = malformed_checks(port, *contexts[0])
        foreign = ownership_checks(port, contexts[0][0])
        summary = {"primary_connection_requests": port.requests,
                   "separate_connection_requests": foreign,
                   "complete_lift_factor_reuse_cycles": 6,
                   "malformed_metadata_controls": malformed,
                   "foreign_owner_controls": 3,
                   "boundary": "Contract framing and reuse only; no mathematical answers asserted."}
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
