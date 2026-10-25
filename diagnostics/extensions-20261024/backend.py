#!/usr/bin/env python3
"""Live public-protocol diagnostic backend; no Lean executable or kernel import."""

import os
from pathlib import Path
import sys
import tempfile


def select_engine():
    selected = os.environ.get("CAS_SAGE_PYTHON")
    # Virtual environments can share the same underlying executable symlink;
    # their invocation paths still select different installed engine packages.
    if selected and Path(selected).absolute() != Path(sys.executable).absolute():
        os.execv(selected, [selected, str(Path(__file__).resolve()), *sys.argv[1:]])
    if "DOT_SAGE" not in os.environ:
        os.environ["DOT_SAGE"] = tempfile.mkdtemp(prefix="cas-extension-sage-")


def main():
    select_engine()
    import json
    import sage.version
    from cas_port import read_frame, value_data, write_frame
    from extensions import ExtensionEngine
    import lifts
    from wire import Unsupported, public_data

    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    operations = {row["operation"] for row in manifest["registrations"]}
    engine = ExtensionEngine()
    write_frame({"op": "ready", "protocol": 1,
                 "backend": "independent-extensions-sage",
                 "backend_version": sage.version.version,
                 "adapter_version": "2026-10-25.2",
                 "capabilities": sorted(operations)})
    while True:
        packet = read_frame()
        if packet is None:
            return
        request_id, operation = None, None
        try:
            if not isinstance(packet, dict):
                raise ValueError("a request requires its complete JSON object")
            request_id, operation = packet.get("request_id"), packet.get("op")
            if not isinstance(operation, str) or not operation:
                raise ValueError("a request requires its nonempty registered operation id")
            if operation not in operations:
                raise Unsupported("unregistered diagnostic operation")
            if "args" not in packet:
                raise ValueError("the request omitted its actual args data")
            argument = packet["args"]
            # Every retained dependency belongs to this request, including an
            # object field or source Arrow that a native routine need not visit.
            # A JSON wrapper never makes another connection's token portable.
            public_data(argument, engine.session)
            if operation.startswith("lift."):
                result = lifts.factor(engine, operation, argument) if operation.endswith("#factor") else lifts.field(engine, operation, argument)
            else:
                if operation in engine.comparisons and engine.tag(argument) != "apply":
                    data = engine.presentation_application(argument, operation)
                elif operation in engine.object_operations and engine.tag(argument) != "apply":
                    data = engine.object_application(operation, argument)
                else:
                    data = engine.point_application(operation, argument)
                result = data if engine.tag(data) == "opaqueData" else value_data(data)
            write_frame({"request_id": request_id, "status": "ok", "value": result})
        except Unsupported:
            write_frame({"request_id": request_id, "status": "unsupported", "op": operation})
        except Exception as error:
            write_frame({"request_id": request_id, "status": "error",
                         "kind": type(error).__name__, "message": str(error)})


if __name__ == "__main__":
    main()
