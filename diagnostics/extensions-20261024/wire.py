"""Small computational utilities for the published CasContract wire format.

No declaration is discovered from runtime values here. Every callable retains its
selected endpoints, and opaque values live only in the process that supplied them.
"""

from dataclasses import dataclass
import json
import secrets

from cas_port import opaque_data, typed_map


class Unsupported(Exception):
    """The selected public input is outside this specimen's implementation."""


def node(tag, *arguments):
    return {"ctor": tag, "args": list(arguments)}


def fields(value, tag, count=None):
    if not isinstance(value, dict) or value.get("ctor") != tag:
        raise ValueError("expected the %s envelope" % tag)
    arguments = value.get("args")
    if not isinstance(arguments, list):
        raise ValueError("%s requires ordered data" % tag)
    if count is not None and len(arguments) != count:
        raise ValueError("%s requires %s data fields" % (tag, count))
    return arguments


def key(value):
    """Canonical equality of JSON data, without identifying mathematical objects."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def same(actual, selected, label):
    if key(actual) != key(selected):
        raise ValueError("%s differs from the complete selected descriptor" % label)


def inventory(value):
    """Return only an explicitly supplied finite inventory or primitive Fin data."""
    if isinstance(value, dict) and value.get("ctor") == "finiteData":
        _, points = fields(value, "finiteData", 2)
        if not isinstance(points, list):
            raise ValueError("finiteData requires an actual point inventory")
    elif isinstance(value, dict) and value.get("ctor") == "obj.sets.fin":
        dimension, = fields(value, "obj.sets.fin", 1)
        if type(dimension) is not int or dimension < 0:
            raise ValueError("Fin requires a natural-number dimension")
        points = list(range(dimension))
    else:
        raise Unsupported("no finite inventory is supplied for this exact object")
    if len({key(point) for point in points}) != len(points):
        raise ValueError("a finite inventory repeats a point")
    return points


@dataclass(frozen=True)
class Callable:
    source: object
    target: object
    action: object
    native: object = None

    def __call__(self, point):
        return self.action(point)


@dataclass(frozen=True)
class NativeIdentity:
    source: object
    target: object


@dataclass(frozen=True)
class NativeComposition:
    first: object
    second: object


@dataclass(frozen=True)
class NativeMediator:
    source: object
    target: object
    left: object
    right: object


class Session:
    """Own native engine values and callables on a single live port connection."""

    def __init__(self):
        self._prefix = secrets.token_hex(12)
        self._values = {}

    def keep(self, value):
        token = "%s:%d" % (self._prefix, len(self._values))
        self._values[token] = value
        return opaque_data(token)

    def get(self, data):
        token, = fields(data, "opaqueData", 1)
        if token not in self._values:
            raise Unsupported("the opaque token is not owned by this live connection")
        return self._values[token]


def graph_callable(data, source, target, finite_inventory=inventory):
    """Read a complete finite graph at its actual selected endpoints."""
    if isinstance(data, dict) and data.get("ctor") == "finiteGraph":
        points, graph = fields(data, "finiteGraph", 2)
        if not isinstance(points, list):
            raise ValueError("finiteGraph requires an actual point inventory")
        try:
            selected_points = finite_inventory(source)
        except Unsupported:
            selected_points = points
        if {key(p) for p in points} != {key(p) for p in selected_points}:
            raise ValueError("the graph changes the supplied domain inventory")
    else:
        points, graph = finite_inventory(source), data
    if not isinstance(graph, list):
        raise Unsupported("callable data is not an inline finite graph")
    entries = {}
    for pair in graph:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("a graph entry requires its key and value")
        encoded = key(pair[0])
        if encoded in entries:
            raise ValueError("a callable graph repeats a domain point")
        entries[encoded] = pair[1]
    selected = [key(point) for point in points]
    if len(set(selected)) != len(selected):
        raise ValueError("the graph inventory repeats a point")
    if set(entries) != set(selected):
        raise ValueError("a callable graph omits or adds a domain point")

    def evaluate(point):
        encoded = key(point)
        if encoded not in entries:
            raise ValueError("the supplied point is absent from the actual domain inventory")
        return entries[encoded]

    return Callable(source, target, evaluate)


def framed_callable(data, source, target, session, interpret, finite_inventory=inventory):
    """Consume typed maps, total finite graphs and owned callable data.

    ``interpret`` is the implementation's explicit registered-arrow reader. This
    module never infers an action from an address or from equal carrier data.
    """
    if isinstance(data, dict) and data.get("ctor") == "typedMap":
        actual_source, actual_target, body = typed_map(data)
        same(actual_source, source, "callable source")
        same(actual_target, target, "callable target")
        return framed_callable(body, source, target, session, interpret, finite_inventory)
    if isinstance(data, dict) and data.get("ctor") == "opaqueData":
        native = session.get(data)
        if not isinstance(native, Callable):
            raise ValueError("the owned data is not a callable")
        same(native.source, source, "owned callable source")
        same(native.target, target, "owned callable target")
        return native
    if isinstance(data, list) or isinstance(data, dict) and data.get("ctor") == "finiteGraph":
        return graph_callable(data, source, target, finite_inventory)
    if isinstance(data, dict) and data.get("ctor") == "identity":
        actual_source, actual_target = fields(data, "identity", 2)
        same(actual_source, source, "identity source")
        same(actual_target, target, "identity target")
        same(source, target, "identity endpoints")
        return Callable(source, target, lambda point: point, NativeIdentity(source, target))
    if isinstance(data, dict) and data.get("ctor") == "mediator":
        left, right = fields(data, "mediator", 2)
        left_target, right_target = fields(target, "objectProduct", 2)
        f = framed_callable(left, source, left_target, session, interpret, finite_inventory)
        g = framed_callable(right, source, right_target, session, interpret, finite_inventory)
        native = NativeMediator(source, target, f.native, g.native) if f.native is not None and g.native is not None else None
        return Callable(source, target, lambda point: [f(point), g(point)], native)
    if isinstance(data, dict) and data.get("ctor") == "compose":
        first, second = fields(data, "compose", 2)
        if isinstance(first, dict) and first.get("ctor") == "typedMap":
            first_source, middle, _ = typed_map(first)
            same(first_source, source, "composite source")
        elif isinstance(second, dict) and second.get("ctor") == "typedMap":
            middle, second_target, _ = typed_map(second)
            same(second_target, target, "composite target")
        else:
            # Registered named arrows may have enough independently published
            # endpoint information for the implementation's reader to proceed.
            return interpret(data, source, target)
        f = framed_callable(first, source, middle, session, interpret, finite_inventory)
        g = framed_callable(second, middle, target, session, interpret, finite_inventory)
        native = NativeComposition(f.native, g.native) if f.native is not None and g.native is not None else None
        return Callable(source, target, lambda point: g(f(point)), native)
    return interpret(data, source, target)
