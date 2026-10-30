"""Bounded public module-functor actions, backed by native Sage values.

This diagnostic program supplies computations, not mathematical evidence.  Its
finite slice is stated in README.md.  Only the registered primitive actions below
are dispatched; this is not an evaluator for downstream target operations.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import secrets
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backends"))
from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_modules", "sage.all"))

from cas_port import (functor_map_invocation, map_data, opaque_data, read_frame,
                      typed_map, value_data, write_frame)
from sage.rings.finite_rings.integer_mod_ring import Zmod
from sage.sets.finite_set_maps import FiniteSetMaps
from sage.version import version as SAGE_VERSION
from wire import finite_data, finite_graph, finite_inventory, graph_data, numeral

FIBRE = "fun.modules.fibre_inclusion"
UNDERLYING = "fun.modules.underlying"
KERNEL = "fun.arrows_modules.kernel"
DOMAIN = "fun.subobjects_modules.domain"
INCLUSION = "fun.subobjects_modules.inclusion"
MATRIX = "mor.modules.matrix_linear_map"
MAX_POINTS = 4096
MAX_DEGREE = 6
MAX_MODULUS = 64


class Unsupported(Exception):
    """The actual supplied representation is outside this diagnostic slice."""


class OwnershipError(Exception):
    """The token does not belong to this live process."""


def node(tag, *args):
    return {"ctor": tag, "args": list(args)}


def key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def same(left, right):
    return key(left) == key(right)


def fields(value, tag, count):
    if not isinstance(value, dict) or value.get("ctor") != tag:
        raise ValueError("expected the public %s envelope" % tag)
    result = value.get("args")
    if not isinstance(result, list) or len(result) != count:
        raise ValueError("%s requires all %d ordered fields" % (tag, count))
    return result


def data(value):
    """Read returned data; never evaluate a retained functorAction recipe."""
    while isinstance(value, dict):
        if value.get("ctor") == "valueData":
            value = fields(value, "valueData", 1)[0]
        elif value.get("ctor") == "objectPresentation":
            value = fields(value, "objectPresentation", 2)[1]
        else:
            break
    return value


SESSION = secrets.token_hex(16)
VALUES = {}


def keep(value):
    token = "%s:%d" % (SESSION, len(VALUES))
    VALUES[token] = value
    return opaque_data(token)


def owned(value, expected):
    token = fields(data(value), "opaqueData", 1)[0]
    if not isinstance(token, str) or token not in VALUES:
        raise OwnershipError("opaque data are foreign to, or expired on, this connection")
    result = VALUES[token]
    if not isinstance(result, expected):
        raise Unsupported("the retained native value has a different computational interface")
    return result


def ring(value):
    raw = data(value)
    if not isinstance(raw, dict) or raw.get("ctor") not in {
        "obj.rings.integers_mod", "obj.commutative_rings.integers_mod"
    }:
        raise Unsupported("only the published finite integer-modulus rings are supported")
    modulus = numeral(fields(raw, raw["ctor"], 1)[0])
    if not 2 <= modulus <= MAX_MODULUS:
        raise Unsupported("the selected modulus is outside the bounded native slice")
    return Zmod(modulus), modulus


@dataclass
class ModuleValue:
    native: object
    scalar_data: object
    modulus: int
    degree: int
    scalar_points: bool
    ambient_set: object
    original: object

    def encode(self, point):
        point = self.native(point)
        if self.scalar_points:
            return int(point[0])
        return [[i, int(point[i])] for i in range(self.degree)]

    def decode(self, point):
        point = data(point)
        if self.scalar_points:
            if type(point) is not int or not 0 <= point < self.modulus:
                raise ValueError("a residue point must have its complete finite scalar encoding")
            return self.native([point])
        rows = indexed(point, self.degree)
        if any(type(x) is not int or not 0 <= x < self.modulus for x in rows):
            raise ValueError("a vector coefficient is outside its scalar representation")
        return self.native(rows)


@dataclass
class ModuleMap:
    native: object
    source: ModuleValue
    target: ModuleValue
    original: object


@dataclass
class TotalValue:
    parameters: list
    source_data: object
    module: ModuleValue


@dataclass
class TotalMap:
    native: object
    base_map: object
    source: TotalValue
    target: TotalValue
    source_data: object
    target_data: object
    original: object


def indexed(value, count):
    """Translate the released finite-function codec, without filling missing keys."""
    rows = graph_data(data(value))
    if len(rows) != count or any(type(x) is not int for x, _ in rows):
        raise ValueError("a finite coordinate callable has the wrong index interface")
    table = dict(rows)
    if set(table) != set(range(count)):
        raise ValueError("a finite coordinate callable omitted an actual index")
    return [table[i] for i in range(count)]


def complete_arrow(value):
    raw = data(value)
    if not isinstance(raw, dict) or raw.get("ctor") not in {"arrow", "subobject"}:
        raise Unsupported("a retained complete Arrow or subobject record is required")
    return fields(raw, raw["ctor"], 3)


def module(value, selected_ring):
    raw = data(value)
    if isinstance(raw, dict) and raw.get("ctor") == "opaqueData":
        result = owned(raw, ModuleValue)
        if not same(result.scalar_data, selected_ring):
            raise Unsupported("the selected ring differs from the retained module parameter")
        return result
    if isinstance(raw, dict) and raw.get("ctor") == "subobjectApex":
        return module(complete_arrow(fields(raw, "subobjectApex", 1)[0])[0], selected_ring)
    if isinstance(raw, dict) and raw.get("ctor") in {
        "obj.modules.subobject_domain", "obj.modules.subobject_ambient"
    }:
        scalar, subobject = fields(raw, raw["ctor"], 2)
        if not same(scalar, selected_ring):
            raise Unsupported("the subobject selector changed its scalar parameter")
        index = 0 if raw["ctor"] == "obj.modules.subobject_domain" else 1
        return module(complete_arrow(subobject)[index], selected_ring)
    if not isinstance(raw, dict) or raw.get("ctor") not in {
        "obj.modules.regular", "obj.modules.vectors"
    }:
        raise Unsupported("only published free modules and actual retained native modules are supported")
    scalar_points = raw["ctor"] == "obj.modules.regular"
    args = fields(raw, raw["ctor"], 1 if scalar_points else 2)
    if not same(args[0], selected_ring):
        raise Unsupported("the supplied free module has a different complete scalar parameter")
    native_ring, modulus = ring(selected_ring)
    degree = 1 if scalar_points else numeral(args[1])
    if degree > MAX_DEGREE:
        raise Unsupported("the supplied free-module degree exceeds this diagnostic bound")
    native = engine.FreeModule(native_ring, degree)
    if native.cardinality() > MAX_POINTS:
        raise Unsupported("the supplied module exceeds this diagnostic enumeration bound")
    coefficient_set = node("obj.sets.integers_mod", modulus)
    ambient = coefficient_set if scalar_points else node("obj.sets.vectors", coefficient_set, degree)
    return ModuleValue(native, selected_ring, modulus, degree, scalar_points, ambient, value)


def compatible(actual, expected):
    """Native representation compatibility only; formal endpoints are caller-owned."""
    if (not same(actual.scalar_data, expected.scalar_data)
            or actual.scalar_points != expected.scalar_points
            or actual.degree != expected.degree or actual.native != expected.native):
        raise Unsupported("the retained map is incompatible with the supplied native endpoint data")


def module_map(value, source, target, selected_ring):
    raw = data(value)
    if isinstance(raw, dict) and raw.get("ctor") == "typedMap":
        x, y, actual = typed_map(raw)
        compatible(module(x, selected_ring), source)
        compatible(module(y, selected_ring), target)
        return module_map(actual, source, target, selected_ring)
    if isinstance(raw, dict) and raw.get("ctor") == "opaqueData":
        result = owned(raw, ModuleMap)
        compatible(result.source, source)
        compatible(result.target, target)
        return result
    if isinstance(raw, dict) and raw.get("ctor") in {"arrowHom", "subobjectInclusion"}:
        x, y, actual = complete_arrow(fields(raw, raw["ctor"], 1)[0])
        return module_map(map_data(x, y, actual), source, target, selected_ring)
    if isinstance(raw, dict) and raw.get("ctor") == "incl.modules.chosen_subobject":
        scalar, subobject = fields(raw, raw["ctor"], 2)
        if not same(scalar, selected_ring):
            raise Unsupported("the defining inclusion has a different scalar parameter")
        x, y, actual = complete_arrow(subobject)
        return module_map(map_data(x, y, actual), source, target, selected_ring)
    if isinstance(raw, dict) and raw.get("ctor") == "identity":
        x, y = fields(raw, "identity", 2)
        compatible(module(x, selected_ring), source)
        compatible(module(y, selected_ring), target)
        compatible(source, target)
        native = source.native.hom(source.native.basis(), target.native)
        return ModuleMap(native, source, target, value)
    if not isinstance(raw, dict) or raw.get("ctor") != MATRIX:
        raise Unsupported("this specimen lowers only the published matrix map or a retained native map")
    dimension, commutative_ring, encoded = fields(raw, MATRIX, 3)
    dimension = numeral(dimension)
    if not isinstance(data(commutative_ring), dict) or data(commutative_ring).get("ctor") != "obj.commutative_rings.integers_mod":
        raise Unsupported("the matrix declaration requires its complete selected commutative ring")
    native_ring, _ = ring(commutative_ring)
    if (source.scalar_points or target.scalar_points or dimension != source.degree
            or dimension != target.degree or native_ring != source.native.base_ring()
            or native_ring != target.native.base_ring()):
        raise Unsupported("the selected matrix map is outside the supplied free-module representation")
    rows = [indexed(row, dimension) for row in indexed(encoded, dimension)]
    if any(type(x) is not int or not 0 <= x < source.modulus for row in rows for x in row):
        raise ValueError("a matrix coefficient has an invalid finite-ring representation")
    native = source.native.hom(engine.matrix(native_ring, dimension, dimension, sum(rows, [])),
                               target.native, side="right")
    return ModuleMap(native, source, target, value)


def object_request(value, operation, arity):
    if not isinstance(value, dict) or value.get("ctor") != operation or "receiver" not in value:
        raise ValueError("the action requires its exact id and complete actual receiver")
    parameters = fields(value, operation, arity)
    return parameters, value["receiver"]


def fibre_object(value):
    parameters, receiver = object_request(value, FIBRE, 1)
    actual = module(receiver, parameters[0])
    return keep(TotalValue(parameters, receiver, actual))


def underlying_object(value):
    _, receiver = object_request(value, UNDERLYING, 0)
    actual = owned(receiver, TotalValue).module
    # Sage performs the full enumeration.  The reply has only existing Sets
    # data forms, and contains neither a source recipe nor a native token.
    points = [actual.encode(point) for point in actual.native]
    descriptor = node("extent", "pow.sets", actual.ambient_set, points)
    return value_data(finite_data(descriptor, points))


def total_map(value, source_data, target_data):
    source, target = owned(source_data, TotalValue), owned(target_data, TotalValue)
    raw = data(value)
    if isinstance(raw, dict) and raw.get("ctor") == "typedMap":
        x, y, actual = typed_map(raw)
        if not same(x, source_data) or not same(y, target_data):
            raise ValueError("a supplied actual total map changed its complete endpoint descriptors")
        return total_map(actual, source_data, target_data)
    if isinstance(raw, dict) and raw.get("ctor") == "identity":
        x, y = fields(raw, "identity", 2)
        if not same(x, source_data) or not same(y, target_data) or source is not target:
            raise ValueError("the identity must retain both actual total endpoints")
        native = source.module.native.hom(source.module.native.basis(), target.module.native)
        base_map = source.module.native.base_ring().coerce_map_from(source.module.native.base_ring())
        return TotalMap(native, base_map, source, target, source_data, target_data, value)
    result = owned(raw, TotalMap)
    if result.source is not source or result.target is not target:
        raise Unsupported("the retained total morphism belongs to different actual objects")
    if not same(result.source_data, source_data) or not same(result.target_data, target_data):
        raise ValueError("the retained total morphism cannot replace its complete endpoint descriptors")
    return result


def whole(domain, source, argument):
    if isinstance(argument, dict) and argument.get("ctor") == "identity":
        x, y = fields(argument, "identity", 2)
        if not same(domain, source) or not same(x, source) or not same(y, source):
            raise ValueError("the whole-domain identity must retain the actual supplied source")
        return True
    return False


def fibre_map(value):
    _, parameters, arrow, domain, image_x, image_y, argument = functor_map_invocation(value, FIBRE)
    if len(parameters) != 1:
        raise ValueError("fibre inclusion requires its one complete ring parameter")
    x, y, actual = typed_map(arrow["args"][1])
    source, target = module(x, parameters[0]), module(y, parameters[0])
    original = module_map(actual, source, target, parameters[0])
    fx, fy = owned(image_x, TotalValue), owned(image_y, TotalValue)
    if (not same(fx.parameters, parameters) or not same(fy.parameters, parameters)
            or not same(fx.source_data, x) or not same(fy.source_data, y)):
        raise ValueError("both actual image endpoints must retain the selected parameters and source objects")
    compatible(fx.module, source)
    compatible(fy.module, target)
    base_map = source.native.base_ring().coerce_map_from(source.native.base_ring())
    result = TotalMap(original.native, base_map, fx, fy, image_x, image_y, value)
    if not whole(domain, image_x, argument):
        before = total_map(argument, domain, image_x)
        result = TotalMap(result.native * before.native, result.base_map * before.base_map, before.source, fy,
                          domain, image_y, value)
    return value_data(map_data(domain, image_y, keep(result)))


def inventory(value):
    raw = data(value)
    if isinstance(raw, dict):
        supplied = finite_inventory(raw)
        if supplied is not None:
            return supplied
        if raw.get("ctor") == "obj.sets.fin":
            count = numeral(fields(raw, "obj.sets.fin", 1)[0])
            if count <= MAX_POINTS:
                return list(range(count))
    raise Unsupported("the actual generalized domain needs its complete finite inventory")


def point_argument(argument, source):
    raw = data(argument)
    if isinstance(raw, dict) and raw.get("ctor") == "element":
        selected, raw = fields(raw, "element", 2)
        if not same(selected, source):
            raise ValueError("the supplied element changed its selected image endpoint")
        if isinstance(raw, dict) and raw.get("ctor") == "numeral":
            raw = fields(raw, "numeral", 1)[0]
    return raw


def underlying_map(value):
    _, parameters, arrow, domain, image_x, image_y, argument = functor_map_invocation(value, UNDERLYING)
    if parameters:
        raise ValueError("the published total-module underlying functor has no explicit parameters")
    x, y, actual = typed_map(arrow["args"][1])
    original = total_map(actual, x, y)
    source_points, target_points = inventory(image_x), inventory(image_y)
    target_keys = {key(point) for point in target_points}

    def apply_native(point):
        result = original.target.module.encode(original.native(original.source.module.decode(point)))
        if key(result) not in target_keys:
            raise ValueError("a map output is outside the supplied actual target inventory")
        return result

    if whole(domain, image_x, argument):
        domain_points = source_points
        graph = [[point, apply_native(point)] for point in domain_points]
    elif same(domain, node("obj.sets.fin", 1)) and not (
            isinstance(data(argument), dict) and data(argument).get("ctor") in {"typedMap", "finiteGraph"}):
        point = point_argument(argument, image_x)
        if key(point) not in {key(x) for x in source_points}:
            raise ValueError("a point is outside the supplied actual source inventory")
        return value_data(apply_native(point))
    else:
        domain_points = inventory(domain)
        raw = data(argument)
        if isinstance(raw, dict) and raw.get("ctor") == "typedMap":
            d, s, raw = typed_map(raw)
            if not same(d, domain) or not same(s, image_x):
                raise ValueError("a generalized argument changed its supplied complete endpoints")
        rows = graph_data(raw)
        table = {key(a): key(b) for a, b in rows}
        if set(table) != {key(a) for a in domain_points}:
            raise ValueError("a generalized argument omitted its actual domain inventory")
        # Existing Sage finite maps consume the supplied complete graph.  No
        # values are interpolated from samples or inferred from a formal arrow.
        native_argument = FiniteSetMaps([key(a) for a in domain_points],
                                       [key(a) for a in source_points]).from_dict(table)
        graph = [[point, apply_native(json.loads(native_argument(key(point))))]
                 for point in domain_points]
        if same(domain, node("obj.sets.fin", 1)):
            return value_data(graph[0][1])
    return value_data(map_data(domain, image_y, finite_graph(domain_points, graph)))


def kernel_object(value):
    parameters, receiver = object_request(value, KERNEL, 1)
    x, y, actual = complete_arrow(receiver)
    source, target = module(x, parameters[0]), module(y, parameters[0])
    original = module_map(actual, source, target, parameters[0])
    if not source.native.base_ring().is_field():
        raise Unsupported("native kernel support here is restricted to the finite prime-field slice")
    native_kernel = original.native.kernel()
    native_inclusion = source.native.coerce_map_from(native_kernel)
    if native_inclusion is None:
        raise Unsupported("Sage did not supply the defining native kernel inclusion")
    kernel = ModuleValue(native_kernel, source.scalar_data, source.modulus, source.degree,
                         source.scalar_points, source.ambient_set, value)
    kernel_data = keep(kernel)
    inclusion = keep(ModuleMap(native_inclusion, kernel, source, value))
    return value_data(node("arrow", kernel_data, x, map_data(kernel_data, x, inclusion)))


def subobject_field(value, operation, index):
    parameters, receiver = object_request(value, operation, 1)
    x, y, actual = complete_arrow(receiver)
    source, target = module(x, parameters[0]), module(y, parameters[0])
    module_map(actual, source, target, parameters[0])
    return value_data(x if index == 0 else data(receiver))


OPERATIONS = {
    FIBRE: fibre_object,
    FIBRE + "#map": fibre_map,
    UNDERLYING: underlying_object,
    UNDERLYING + "#map": underlying_map,
    KERNEL: kernel_object,
    DOMAIN: lambda value: subobject_field(value, DOMAIN, 0),
    INCLUSION: lambda value: subobject_field(value, INCLUSION, 2),
}


def main():
    write_frame({"op": "ready", "protocol": 1, "backend": "sage-module-functor-actions",
                 "backend_version": SAGE_VERSION, "adapter_version": "0.1.0",
                 "capabilities": sorted(OPERATIONS)})
    while True:
        request = read_frame()
        if request is None:
            return
        rid, operation = request.get("request_id"), request.get("op")
        try:
            if operation not in OPERATIONS:
                raise Unsupported("this primitive action is not registered by the specimen")
            if "args" not in request:
                raise ValueError("the request omitted its complete args")
            reply = {"request_id": rid, "status": "ok", "value": OPERATIONS[operation](request["args"])}
        except Unsupported as exc:
            sys.stderr.write("unsupported %s: %s\n" % (operation, exc))
            reply = {"request_id": rid, "status": "unsupported", "op": operation}
        except Exception as exc:
            reply = {"request_id": rid, "status": "error", "kind": type(exc).__name__, "message": str(exc)}
        write_frame(reply)


if __name__ == "__main__":
    main()
