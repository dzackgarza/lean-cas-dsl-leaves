#!/usr/bin/env python3
"""Exercise framing and live ownership with self-selected public input packets.

This is a diagnostic smoke run, not a mathematical correctness suite. It contains
no expected mathematical answers and never launches the kernel or Lean.
"""

import json
import os
from pathlib import Path
import subprocess
import sys


def node(tag, *arguments):
    return {"ctor": tag, "args": list(arguments)}


def apply(operation, parameters, domain, source, target, argument):
    return node("apply", operation, parameters, node(operation, *parameters),
                domain, source, target, argument)


def read_frame(stream):
    line = stream.readline()
    if not line or not line[:-1].isdigit():
        raise RuntimeError("the backend did not provide a framed reply")
    length = int(line)
    payload = stream.read(length)
    if len(payload) != length:
        raise RuntimeError("the backend closed inside its framed reply")
    return json.loads(payload)


def main():
    root = Path(__file__).resolve().parent
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    child = subprocess.Popen([sys.executable, str(root / "backend.py")], cwd=root,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=None, env=environment)
    try:
        ready = read_frame(child.stdout)
        if ready.get("op") != "ready" or ready.get("protocol") != 1:
            raise RuntimeError("the public ready announcement is incomplete")
        print(json.dumps({"announcement": ready["backend"], "capabilityCount": len(ready["capabilities"])}))
        request_id = 0

        def invoke(operation, arguments):
            nonlocal request_id
            request_id += 1
            frame = {"request_id": request_id, "op": operation, "args": arguments}
            payload = json.dumps(frame, separators=(",", ":")).encode()
            child.stdin.write(str(len(payload)).encode() + b"\n" + payload)
            child.stdin.flush()
            reply = read_frame(child.stdout)
            if reply.get("request_id") != request_id:
                raise RuntimeError("the backend changed a request identity")
            print(json.dumps({"request": request_id, "operation": operation,
                              "status": reply.get("status"),
                              "envelope": reply.get("value", {}).get("ctor") if isinstance(reply.get("value"), dict) else None}))
            if reply.get("status") != "ok":
                raise RuntimeError(json.dumps(reply))
            return reply["value"]

        one = node("obj.sets.fin", 1)
        q = node("obj.sets.rationals")
        qr = node("obj.rings.rationals")
        qc = node("obj.commutative_rings.rationals")
        x = node("obj.sets.rational_dual_x")
        y = node("obj.sets.rational_dual_y")
        xr = node("functorAction", node("fun.commutative_rings.ring"), node("obj.commutative_rings.rational_dual_x"))
        point = node("element", x, node("add", node("generator"), node("numeral", 7)))
        shifted = invoke("cmp.rational_dual.translation", node("presentationApply", [], False, x, y, point))
        invoke("cmp.rational_dual.translation", node("presentationApply", [], True, y, x, shifted))
        invoke("op.rings.pow", apply("op.rings.pow", [xr, 5], one, x, x, point))
        finite_domain = node("obj.sets.fin", 3)
        family = [[0, point], [1, node("element", x, node("generator"))], [2, node("element", x, node("numeral", 4))]]
        invoke("op.rings.pow", apply("op.rings.pow", [xr, 2], finite_domain, x, x, family))

        rows = [[0, [[0, [2, 3]], [1, [-5, 7]]]],
                [1, [[0, [1, 1]], [1, [4, 9]]]],
                [2, [[0, [0, 1]], [1, [3, 2]]]]]
        v2, v3 = node("obj.modules.vectors", qr, 2), node("obj.modules.vectors", qr, 3)
        invoke("mor.modules.rectangular_linear_map", apply(
            "mor.modules.rectangular_linear_map", [3, 2, qc, rows], one, v2, v3,
            [[0, [11, 5]], [1, [-2, 1]]]))

        lift = "lift.bilin_module.change_value_restriction"
        value_map = node("typedMap", q, q, node("identity", q, q))
        parameters = [q, q, q, value_map]
        action = node("fun.bilin_module.change_value", *parameters)
        source = node("obj.bilin_module.degenerate_plane_target")
        base_apex = node("obj.bilin_module.degenerate_plane")
        ambient = node("functorAction", action, source)
        inclusion = node("typedMap", base_apex, ambient, node("mor.bilin_module.degenerate_plane_map"))
        base = node("subobject", base_apex, ambient, inclusion)
        outputs = []
        for component in ("obj", "hom", "forward", "backward"):
            packet = node("monoLiftInput", lift, action, source, base, outputs[:])
            packet["parameters"] = parameters
            outputs.append(invoke(lift + "#" + component, packet))

        factor = node("liftFactorInput", lift, action, source, base, outputs[:], outputs[2], outputs[1])
        factor["parameters"] = parameters
        invoke(lift + "#factor", factor)
        pairing = "mor.sets.bilin_module_pairing"
        object_data = outputs[0]
        invoke(pairing, apply(pairing, [qc, node("obj.modules.regular", qr), object_data],
                             one, node("objectProduct", object_data, object_data), q,
                             [[[0, [3, 4]], [1, [8, 3]]],
                              [[0, [-1, 2]], [1, [6, 5]]]]))
        print(json.dumps({"completedRequests": request_id, "checks": "framing, startup, selected packet consumption and live opaque reuse only"}))
    finally:
        child.stdin.close()
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            child.terminate()
            child.wait(timeout=10)


if __name__ == "__main__":
    main()
