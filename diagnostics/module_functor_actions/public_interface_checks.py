"""Public framing and retention checks only; no mathematical answer assertions.

All observations are local leaf engineering diagnostics.  No kernel, acceptance
suite, fixed questions, expected answers, or other worker files are read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "backends"))
from wire import finite_inventory, graph_data

F = "fun.modules.fibre_inclusion"
U = "fun.modules.underlying"
K = "fun.arrows_modules.kernel"
D = "fun.subobjects_modules.domain"
I = "fun.subobjects_modules.inclusion"
MATRIX = "mor.modules.matrix_linear_map"
BASE = "865df49ad0b0b133d5bcfd282f380aa213eb5fff"
CONTRACT = "b805eda94aec95a7962da486c8eaeec14d34f2b2"


def node(tag, *args):
    return {"ctor": tag, "args": list(args)}


def key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def raw(value):
    while isinstance(value, dict) and value.get("ctor") == "valueData":
        value = value["args"][0]
    return value


def opaque_tokens(value):
    if isinstance(value, dict):
        if value.get("ctor") == "opaqueData":
            return [value["args"][0]]
        return [token for field in value.values() for token in opaque_tokens(field)]
    if isinstance(value, list):
        return [token for field in value for token in opaque_tokens(field)]
    return []


def action(operation, parameters, receiver):
    return {"ctor": operation, "args": parameters, "receiver": receiver}


def map_request(operation, parameters, x, y, actual_map, fx, fy, domain=None, argument=None):
    if domain is None:
        domain = fx
        argument = node("identity", fx, fx)
    return node("apply", operation + "#map", parameters,
                node("map", node(operation, *parameters), node("typedMap", x, y, actual_map)),
                domain, fx, fy, argument)


class Checks:
    def __init__(self, output):
        self.output = output
        self.names = []
        self.transcript = (output / "interface-transcript.jsonl").open("w")

    def event(self, **value):
        self.transcript.write(json.dumps(value, sort_keys=True) + "\n")
        self.transcript.flush()

    def require(self, condition, label):
        if not condition:
            raise RuntimeError("public interface check failed: " + label)
        self.names.append(label)

    def complete_map(self, value, source, target, label, finite=False):
        packet = raw(value)
        self.require(isinstance(packet, dict) and packet.get("ctor") == "typedMap"
                     and len(packet.get("args", [])) == 3, label + ": three-field typed map")
        actual_source, actual_target, callable_data = packet["args"]
        self.require(key(actual_source) == key(source), label + ": complete supplied source")
        self.require(key(actual_target) == key(target), label + ": complete supplied target")
        if finite:
            inventory = finite_inventory(raw(source))
            if inventory is None and raw(source).get("ctor") == "obj.sets.fin":
                inventory = list(range(raw(source)["args"][0]))
            graph = graph_data(callable_data)
            self.require({key(p) for p in inventory} == {key(p[0]) for p in graph}
                         and len(graph) == len(inventory), label + ": whole supplied domain inventory")
            target_points = finite_inventory(raw(target))
            self.require(all(key(pair[1]) in {key(p) for p in target_points} for pair in graph),
                         label + ": output representation at supplied target inventory")
        return packet


class Client:
    def __init__(self, checks, label):
        self.checks, self.label, self.number = checks, label, 0
        self.stderr = (checks.output / (label + "-stderr.txt")).open("w")
        self.process = subprocess.Popen([sys.executable, str(HERE / "backend.py")], cwd=HERE,
                                        env=os.environ.copy(), stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=self.stderr)
        ready = self.read()
        checks.event(session=label, direction="ready", packet=ready)
        checks.require(ready.get("op") == "ready" and ready.get("protocol") == 1,
                       label + ": ready frame")

    def read(self):
        header = self.process.stdout.readline()
        if not header.endswith(b"\n") or not header[:-1] or any(c < 48 or c > 57 for c in header[:-1]):
            raise RuntimeError("incomplete or invalid ASCII frame header")
        length = int(header[:-1])
        body = self.process.stdout.read(length)
        if len(body) != length:
            raise RuntimeError("incomplete reply frame")
        return json.loads(body.decode("utf-8"))

    def call(self, operation, argument, status="ok", label=None):
        self.number += 1
        packet = {"request_id": self.number, "op": operation, "args": argument}
        body = json.dumps(packet, separators=(",", ":")).encode("utf-8")
        self.checks.event(session=self.label, direction="request", label=label, packet=packet,
                          utf8_bytes=len(body))
        self.process.stdin.write(str(len(body)).encode("ascii") + b"\n" + body)
        self.process.stdin.flush()
        reply = self.read()
        self.checks.event(session=self.label, direction="reply", label=label, packet=reply)
        self.checks.require(reply.get("request_id") == self.number,
                            (label or operation) + ": request identity")
        self.checks.require(reply.get("status") == status,
                            (label or operation) + ": declared reply stratum")
        if status == "unsupported":
            self.checks.require(reply.get("op") == operation,
                                (label or operation) + ": exact unsupported operation")
        return reply["value"] if status == "ok" else reply

    def close(self):
        self.process.stdin.close()
        self.process.wait(timeout=20)
        self.stderr.close()
        self.checks.event(session=self.label, direction="closed", returncode=self.process.returncode)
        self.checks.require(self.process.returncode == 0, self.label + ": clean process close")


def public_receipt(output):
    contract_path = Path(os.environ["CAS_LEAF_CONTRACT_PATH"]).resolve()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=contract_path, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=contract_path, text=True).strip()
    if revision != CONTRACT or tree != "d87ca1ed7e18cf81373ba835a8a1e54c926f6236":
        raise RuntimeError("the public interface check requires the specified immutable contract")
    contract_files = ["CasContract/Port.lean", "api/manifest.md", "api/wire-examples.md",
                      "api/declared-ports.json", "api/README.md", "python/cas_port.py"]
    leaf_files = ["AGENTS.md", "INTENT.md", "backends/engine_python.py", "backends/wire.py",
                  "backends/sage_modules.py", "backends/sage_bilinear_lift.py"]
    hashes = lambda root, names: {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}
    receipt = {"leaf_base_revision": BASE, "public_contract_revision": revision,
               "public_contract_tree": tree, "contract_files_sha256": hashes(contract_path, contract_files),
               "public_leaf_prior_art_sha256": hashes(ROOT, leaf_files),
               "blindness": "No kernel source, runtime verification, acceptance assertions, fixed questions or expected answers, private diagnostics, protected sage_set_limits.py, or other workers' output was read.",
               "scope": "Public framing, full parameter and endpoint retention, whole/generalized domains, and owner/session interfaces only; no mathematical correctness or acceptance claim."}
    (output / "public-input-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    inventory = json.loads((contract_path / "api/declared-ports.json").read_text())
    ids = {F, U, K, D, I}
    public_functors = {row["id"] for row in inventory["functors"]}
    if not ids <= public_functors:
        raise RuntimeError("a selected functor is absent from the published inventory")
    manifest = json.loads((HERE / "leaves.json").read_text())
    for row in manifest["registrations"]:
        base = row["operation"].removesuffix("#map")
        if base not in ids or row["input"] != base + "#input":
            raise RuntimeError("manifest address does not project one of the selected public functors")
    selected = {"inventory_provenance": inventory["provenance"],
                "functors": [row for row in inventory["functors"] if row["id"] in ids],
                "source_map": [row for row in inventory["entries"] if row["id"] == MATRIX],
                "manifest": manifest,
                "derived_addresses": "The #map/#input rule is the published b805 contract rule; the committed inventory's older export does not enumerate these addresses."}
    (output / "public-address-receipt.json").write_text(json.dumps(selected, indent=2) + "\n")


def run(output):
    output.mkdir(parents=True, exist_ok=True)
    public_receipt(output)
    checks = Checks(output)
    owner = Client(checks, "owner")
    ring = node("obj.rings.integers_mod", 7)
    commutative_ring = node("obj.commutative_rings.integers_mod", 7)
    x = node("obj.modules.vectors", ring, 2)
    matrix_data = [[0, [[0, 2], [1, 1]]], [1, [[0, 0], [1, 0]]]]
    supplied_map = node(MATRIX, 2, commutative_ring, matrix_data)
    fx = owner.call(F, action(F, [ring], x), label="fibre source object")
    fy = owner.call(F, action(F, [ring], x), label="fibre target object")
    mapped = owner.call(F + "#map", map_request(F, [ring], x, x, supplied_map, fx, fy),
                        label="fibre whole map")
    checks.complete_map(mapped, fx, fy, "fibre whole map")
    sx = owner.call(U, action(U, [], fx), label="underlying source object")
    sy = owner.call(U, action(U, [], fy), label="underlying target object")
    for name, packet in [("source", sx), ("target", sy)]:
        checks.require(not opaque_tokens(packet), "portable underlying " + name + ": no opaque dependency")
        checks.require(raw(packet).get("ctor") == "finiteData", "portable underlying " + name + ": complete finite interface")
    set_map = owner.call(U + "#map", map_request(U, [], fx, fy, mapped, sx, sy),
                         label="underlying whole map")
    checks.complete_map(set_map, sx, sy, "underlying whole map", finite=True)
    checks.require(not opaque_tokens(set_map), "underlying whole map: portable complete graph")

    # All output-point observations below are framed against actual returned
    # inventories.  No numeric value, rank, cardinality, kernel equation, or map
    # equation is asserted.
    source_points = finite_inventory(raw(sx))
    actual_domain = node("finiteData", node("obj.sets.fin", 3), [2, 0, 1])
    actual_argument = node("finiteGraph", [2, 0, 1],
                           [[2, source_points[1]], [0, source_points[2]], [1, source_points[3]]])
    generalized = owner.call(U + "#map", map_request(U, [], fx, fy, mapped, sx, sy,
                                                    actual_domain, actual_argument),
                             label="nonconstant generalized Sets demand")
    checks.complete_map(generalized, actual_domain, sy, "generalized Sets map", finite=True)
    scalar = owner.call(U + "#map", map_request(U, [], fx, fy, mapped, sx, sy,
                                               node("obj.sets.fin", 1),
                                               node("element", sx, source_points[0])),
                        label="global point demand")
    checks.require(raw(scalar) in finite_inventory(raw(sy)), "global point: target point-data representation")
    scalar_graph = owner.call(U + "#map", map_request(U, [], fx, fy, mapped, sx, sy,
                                                     node("obj.sets.fin", 1),
                                                     node("finiteGraph", [0], [[0, source_points[0]]])),
                              label="global point supplied as complete callable")
    checks.require(raw(scalar_graph) in finite_inventory(raw(sy)),
                   "global finite argument: target point-data representation")

    original_arrow = node("arrow", x, x, node("typedMap", x, x, supplied_map))
    kernel = owner.call(K, action(K, [ring], original_arrow), label="native kernel record")
    kernel_record = raw(kernel)
    checks.require(kernel_record.get("ctor") == "arrow" and len(kernel_record["args"]) == 3,
                   "kernel: complete Arrow record")
    kernel_object, ambient, defining = kernel_record["args"]
    checks.require(key(ambient) == key(x), "kernel: retained actual ambient")
    checks.complete_map(defining, kernel_object, x, "kernel defining inclusion")
    domain = owner.call(D, action(D, [ring], kernel), label="retained subobject domain")
    inclusion = owner.call(I, action(I, [ring], kernel), label="retained subobject inclusion")
    checks.require(key(raw(domain)) == key(kernel_object), "subobject domain: exact retained object")
    checks.require(key(raw(inclusion)) == key(kernel_record), "subobject inclusion: exact complete retained Arrow")

    fk = owner.call(F, action(F, [ring], domain), label="fibre on computed module")
    sk = owner.call(U, action(U, [], fk), label="underlying computed kernel")
    checks.require(not opaque_tokens(sk), "computed module underlying set: portable reply despite owned input")
    kernel_map = owner.call(F + "#map", map_request(F, [ring], domain, x,
                                                   node("arrowHom", inclusion), fk, fx),
                            label="fibre on actual computed inclusion")
    checks.complete_map(kernel_map, fk, fx, "mapped kernel inclusion")
    set_inclusion = owner.call(U + "#map", map_request(U, [], fk, fx, kernel_map, sk, sx),
                               label="underlying actual computed inclusion")
    checks.complete_map(set_inclusion, sk, sx, "underlying kernel inclusion", finite=True)
    generalized_module = owner.call(F + "#map", map_request(F, [ring], x, x, supplied_map,
                                                           fx, fy, fk, kernel_map),
                                    label="generalized module demand with retained inclusion")
    checks.complete_map(generalized_module, fk, fy, "generalized module map")

    # Both copies are checked, and same-copy arity changes are separately rejected.
    changed = map_request(F, [ring], x, x, supplied_map, fx, fy)
    changed["args"][1] = []
    owner.call(F + "#map", changed, "error", "different ordered parameter copies")
    owner.call(F + "#map", map_request(F, [ring, ring], x, x, supplied_map, fx, fy),
               "error", "extra complete functor parameter")
    owner.call(U + "#map", map_request(U, [ring], fx, fy, mapped, sx, sy),
               "error", "underlying unexpected parameter")
    omitted = map_request(F, [ring], x, x, supplied_map, fx, fy)
    del omitted["args"][5]
    owner.call(F + "#map", omitted, "error", "missing actual image endpoint")
    owner.call(F + "#map", map_request(F, [ring], domain, x, node("arrowHom", inclusion), fx, fx),
               "error", "replacement source image rejected")
    owner.call(F, action(F, [node("obj.rings.integers_mod", 5)], x),
               "unsupported", "different scalar selection remains unsupported")
    owner.call(F, action(F, [], x), "error", "missing object-action parameter")
    owner.call(U + "#map", map_request(U, [], fx, fy, mapped, sx, sy,
                                      node("obj.sets.integers"), actual_argument),
               "unsupported", "unavailable generalized-domain representation")
    owner.call("meth.cardinality", sx, "unsupported", "unregistered target operation")
    owner.call(F + "#map", map_request(F, [ring], x, x,
                                      node("finiteGraph", [], []), fx, fy),
               "unsupported", "unsupported source callable is not interpolated")

    regular = node("obj.modules.regular", ring)
    regular_total = owner.call(F, action(F, [ring], regular), label="regular module object")
    regular_set = owner.call(U, action(U, [], regular_total), label="regular module scalar-point interface")
    regular_map = owner.call(F + "#map", map_request(F, [ring], regular, regular,
                                                   node("identity", regular, regular),
                                                   regular_total, regular_total),
                             label="regular module native identity")
    regular_set_map = owner.call(U + "#map", map_request(U, [], regular_total, regular_total,
                                                       regular_map, regular_set, regular_set),
                                 label="regular module underlying whole map")
    checks.complete_map(regular_set_map, regular_set, regular_set, "regular module callable", finite=True)

    composite_ring = node("obj.rings.integers_mod", 6)
    free = node("obj.modules.vectors", composite_ring, 1)
    tfree = owner.call(F, action(F, [composite_ring], free), label="composite-modulus free module")
    sfree = owner.call(U, action(U, [], tfree), label="composite-modulus portable Sets image")
    tidentity = owner.call(F + "#map", map_request(F, [composite_ring], free, free,
                                                 node("identity", free, free), tfree, tfree),
                           label="composite-modulus native map")
    identity_image = owner.call(U + "#map", map_request(U, [], tfree, tfree, tidentity, sfree, sfree),
                                label="composite-modulus underlying whole map")
    checks.complete_map(identity_image, sfree, sfree, "composite-modulus callable", finite=True)
    owner.call(K, action(K, [composite_ring], node("arrow", free, free, node("identity", free, free))),
               "unsupported", "unsupported native composite-modulus kernel")

    foreign = Client(checks, "foreign")
    rejected = foreign.call(U, action(U, [], fx), "error", "live foreign owner rejected")
    checks.require(rejected.get("kind") == "OwnershipError", "foreign token: ownership unavailable")
    foreign.close()
    owner.close()
    expired = Client(checks, "expired")
    rejected = expired.call(U, action(U, [], fk), "error", "expired owner is not revived")
    checks.require(rejected.get("kind") == "OwnershipError", "expired token: ownership unavailable")
    expired.close()

    portable = {"source_set": sx, "target_set": sy, "kernel_set": sk,
                "whole_map": set_map, "kernel_inclusion": set_inclusion,
                "generalized_map": generalized}
    checks.require(not opaque_tokens(portable), "portable artifact remains independent of closed owners")
    (output / "portable-packets.json").write_text(json.dumps(portable, indent=2) + "\n")
    checks.transcript.close()
    report = {"scope": "Public interface checks only; mathematical correctness and downstream acceptance remain unknown.",
              "checks": checks.names, "result": "All listed framing and retention checks completed.",
              "request_count": owner.number + foreign.number + expired.number}
    (output / "interface-summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"request_count": report["request_count"], "interface_checks": len(checks.names),
                      "output": str(output), "mathematical_correctness": "not assessed"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    run(parser.parse_args().output.resolve())
