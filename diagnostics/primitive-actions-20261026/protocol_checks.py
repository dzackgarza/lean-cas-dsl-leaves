#!/usr/bin/env python3
"""Local framing, manifest, field-retention and session checks only.

These checks neither import nor execute a kernel or a mathematical acceptance
suite. No scalar result or law of any returned algebraic object is asserted.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
RING = "fun.rings.semiring"
MONOID = "fun.semirings.monoid"
MULTIPLY = "op.monoids.mul"


def node(name, *args):
    return {"ctor": name, "args": list(args)}


def manifest_fields(value, specification, root):
    """Check the object/array/string vocabulary used by the public manifest schema."""
    if "$ref" in specification:
        assert specification["$ref"].startswith("#/$defs/")
        return manifest_fields(value, root["$defs"][specification["$ref"].split("/")[-1]], root)
    kinds = {"object": dict, "array": list, "string": str}
    assert type(value) is kinds[specification["type"]]
    if isinstance(value, dict):
        assert set(specification.get("required", [])) <= set(value)
        properties = specification.get("properties", {})
        if specification.get("additionalProperties") is False:
            assert set(value) <= set(properties)
        for name in set(value) & set(properties):
            manifest_fields(value[name], properties[name], root)
    elif isinstance(value, list):
        for item in value:
            manifest_fields(item, specification["items"], root)


class Connection:
    def __init__(self, environment):
        self.process = subprocess.Popen(
            [sys.executable, str(HERE / "backend.py")], cwd=HERE,
            env=environment, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        self.next_id = 0
        ready = self.read()
        assert ready["op"] == "ready" and ready["protocol"] == 1
        assert set(ready["capabilities"]) == {RING, MONOID, MULTIPLY}

    def read(self):
        header = self.process.stdout.readline()
        if not header:
            raise RuntimeError(self.process.stderr.read().decode())
        assert header.endswith(b"\n") and header[:-1].isdigit()
        remaining, chunks = int(header), []
        while remaining:
            chunk = self.process.stdout.read(remaining)
            assert chunk, "interrupted protocol frame"
            chunks.append(chunk)
            remaining -= len(chunk)
        return json.loads(b"".join(chunks))

    def call(self, operation, receiver, parameters=None):
        return self.invoke(operation, {"ctor": operation,
                                      "args": [] if parameters is None else parameters,
                                      "receiver": receiver})

    def invoke(self, operation, arguments):
        self.next_id += 1
        request = {"request_id": self.next_id, "op": operation, "args": arguments}
        payload = json.dumps(request, separators=(",", ":")).encode()
        self.process.stdin.write(str(len(payload)).encode() + b"\n" + payload)
        self.process.stdin.flush()
        result = self.read()
        assert result["request_id"] == self.next_id
        return result

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.close()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        assert self.process.returncode == 0, self.process.stderr.read().decode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--engine", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((HERE / "leaves.json").read_text())
    schema = json.loads((args.contract / "api/manifest.schema.json").read_text())
    manifest_fields(manifest, schema, schema)
    assert [(r["operation"], r["input"]) for r in manifest["registrations"]] == [
        (RING, RING + "#input"), (MONOID, MONOID + "#input"), (MULTIPLY, "cat.monoids")]
    environment = dict(os.environ)
    # Preserve a virtualenv's bin/python path; resolving its symlink loses the
    # environment's engine packages.
    environment["CAS_SAGE_PYTHON"] = str(args.engine.absolute())
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = str(args.contract.resolve() / "python")
    with tempfile.TemporaryDirectory(prefix="primitive-actions-protocol-") as temporary:
        environment["DOT_SAGE"] = temporary
        first = Connection(environment)
        try:
            coefficient = node("obj.commutative_rings.rationals")
            rings = [node("obj.rings.integers"), node("obj.rings.rationals"),
                     node("obj.rings.integers_mod", 17),
                     node("obj.rings.polynomials", coefficient),
                     node("obj.rings.mv_polynomials", 3, coefficient),
                     node("obj.rings.matrices", 2, coefficient),
                     node("obj.rings.power_series", coefficient)]
            for ring in rings:
                reply = first.call(RING, ring)
                assert reply["status"] == "ok", reply
                semiring_packet = reply["value"]
                assert semiring_packet["ctor"] == "valueData"
                carrier, structure = semiring_packet["args"][0]
                assert len(structure) == 3 and len(structure[0]) == len(structure[1]) == 3
                mapped = first.call(MONOID, semiring_packet)
                assert mapped["status"] == "ok", mapped
                # Exact retained fields, without reading any native value.
                assert mapped["value"] == node("valueData", [carrier, structure[1]])
            assert first.call(MONOID, node("obj.semirings.naturals"))["status"] == "ok"
            assert first.call(RING, rings[0], [1])["status"] == "error"
            assert first.call(RING + "#map", rings[0])["status"] == "unsupported"
            assert first.call(RING, node("obj.rings.reals"))["status"] == "unsupported"
            unknown = first.call(MONOID, node("opaqueData", "unowned-token"))
            assert unknown["status"] == "error" and unknown["kind"] == "Unavailable"
            second = Connection(environment)
            try:
                stale = second.call(MONOID, semiring_packet)
                assert stale["status"] == "error" and stale["kind"] == "Unavailable"
            finally:
                second.close()
        finally:
            first.close()
    print("Local protocol/schema checks completed; no mathematical acceptance was run.")


if __name__ == "__main__":
    main()
