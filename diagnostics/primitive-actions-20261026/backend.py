#!/usr/bin/env python3
"""Persistent public port for exactly two primitive object actions."""

from pathlib import Path
import sys

# Reuse the existing interpreter selector, without importing any registrations.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backends"))
from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", ("sage.all",))

from cas_port import read_frame, write_frame
from sage.version import version as SAGE_VERSION
from primitive_actions import Actions, OPERATIONS, Unsupported


def main():
    actions = Actions()
    write_frame({"op": "ready", "protocol": 1,
                 "backend": "sage-primitive-actions-20261026",
                 "backend_version": SAGE_VERSION, "adapter_version": "0.1.0",
                 "capabilities": list(OPERATIONS)})
    while True:
        request = read_frame()
        if request is None:
            return
        request_id, operation = request.get("request_id"), request.get("op")
        try:
            if operation not in OPERATIONS:
                raise Unsupported("unregistered operation")
            if "args" not in request:
                raise ValueError("the request omitted its args field")
            result = actions.run(operation, request["args"])
            reply = {"request_id": request_id, "status": "ok", "value": result}
        except Unsupported:
            reply = {"request_id": request_id, "status": "unsupported", "op": operation}
        except Exception as exc:
            reply = {"request_id": request_id, "status": "error",
                     "kind": type(exc).__name__, "message": str(exc)}
        write_frame(reply)


if __name__ == "__main__":
    main()
