"""Small computational utilities for the published CasContract wire format.

No declaration is discovered from runtime values here. Every callable retains its
selected endpoints, and opaque values live only in the process that supplied them.
"""

from dataclasses import dataclass
import json
import secrets

from cas_port import morphism_endpoint, object_product, opaque_data, typed_map


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


def power_object_map(data):
    """Read the five callable field spellings published by the power port."""
    power, field, parameters = fields(data, "powerObjectMap", 3)
    if not isinstance(power, str) or not power or not isinstance(field, str) or not field:
        raise ValueError("a power-object map requires its declared power and field names")
    if not isinstance(parameters, list):
        raise ValueError("a power-object map requires its ordered declaration parameters")
    if power != "pow.sets":
        raise Unsupported("this selected power object has no implemented callable reader")
    counts = {"member": 1, "terminal": 1, "transpose": 2, "image": 3, "truth": 0}
    if field not in counts:
        raise Unsupported("this power-object field has no published callable implementation here")
    if len(parameters) != counts[field]:
        raise ValueError("the power-object field omits or adds a declaration parameter")
    return power, field, parameters


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
    invocation: object = None
    point_action: object = None

    def __call__(self, point):
        return self.action(point)

    def at_point(self, point, read):
        """Use this callable's actual input reader for a public point packet.

        Native actions keep their ordinary point decoder. Graphs and structural
        combinations retain their own framing before a native reader sees it.
        """
        if self.point_action is not None:
            return self.point_action(point, read)
        return self.action(read(point, self.source))


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


@dataclass(frozen=True)
class Invocation:
    """The actual complete request and both retained computational dependencies."""

    operation: str
    parameters: object
    packet: object
    argument: object
    action: object


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
        if not isinstance(token, str) or not token:
            raise ValueError("an opaque computational value requires a nonempty token")
        if token not in self._values:
            raise Unsupported("the opaque token is not owned by this live connection")
        return self._values[token]


def public_data(data, session):
    """Check nested public framing and live owners, without interpreting types."""
    if isinstance(data, list):
        for item in data:
            public_data(item, session)
    elif isinstance(data, dict):
        tag = data.get("ctor")
        if tag == "morphismEndpoint":
            morphism_endpoint(data)
        elif tag == "typedMap":
            typed_map(data)
        elif tag == "objectProduct":
            object_product(data)
        elif tag == "finiteData":
            inventory(data)
        elif tag == "powerObjectMap":
            power_object_map(data)
        elif tag in {"compose", "mediator"}:
            fields(data, tag, 2)
        elif tag == "opaqueData":
            session.get(data)
        for item in data.values():
            public_data(item, session)


def retained_endpoint(data, side, session):
    """Read an actual supplied map field; never manufacture a carrier name."""
    tag = data.get("ctor") if isinstance(data, dict) else None
    if tag in {"valueData", "point"}:
        return retained_endpoint(fields(data, tag, 1)[0], side, session)
    if tag == "typedMap":
        source, target, _ = typed_map(data)
        return source if side == "source" else target
    if tag == "opaqueData":
        actual = session.get(data)
        if isinstance(actual, Callable):
            return actual.source if side == "source" else actual.target
    if tag == "identity":
        source, target = fields(data, tag, 2)
        same(source, target, "identity endpoints")
        return source if side == "source" else target
    if tag == "element":
        # The selected arithmetic owner is not an actual typed-map field.
        # A retained callable payload, when present, keeps its own endpoints.
        return retained_endpoint(fields(data, tag, 2)[1], side, session)
    if tag == "compose":
        first, second = fields(data, tag, 2)
        return retained_endpoint(first if side == "source" else second, side, session)
    return None


def product_fields(selected, components=None):
    return object_product(selected)


def graph_callable(data, source, target, finite_inventory=inventory, read_point=None):
    """Read a complete finite graph at its actual selected endpoints."""
    if isinstance(data, dict) and data.get("ctor") == "finiteGraph":
        points, graph = fields(data, "finiteGraph", 2)
        if not isinstance(points, list):
            raise ValueError("finiteGraph requires an actual point inventory")
        # The graph's keys cannot certify that its domain is finite or complete.
        # Its source must independently supply a full inventory (for example
        # Fin(n), finiteData, or a complete native finite carrier).
        selected_points = finite_inventory(source)
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
    try:
        target_points = inventory(target)
    except Unsupported:
        pass
    else:
        target_keys = {key(point) for point in target_points}
        for value in entries.values():
            actual = value
            while key(actual) not in target_keys and isinstance(actual, dict) and actual.get("ctor") == "valueData":
                actual, = fields(actual, "valueData", 1)
            if key(actual) not in target_keys and read_point is not None:
                actual = read_point(value, target)
            if key(actual) not in target_keys:
                raise ValueError("a callable graph has an image outside the supplied codomain inventory")
        # The private check above never replaces the retained output packets.

    def evaluate(point):
        encoded = key(point)
        if encoded not in entries:
            raise ValueError("the supplied point is absent from the actual domain inventory")
        return entries[encoded]

    def evaluate_point(point, read):
        actual = point
        while True:
            # A valueData envelope can itself be an explicitly supplied key.
            # Check the exact key before inspecting an outer result envelope.
            if key(actual) in entries:
                return evaluate(actual)
            if not isinstance(actual, dict) or actual.get("ctor") != "valueData":
                break
            actual, = fields(actual, "valueData", 1)
        return evaluate(read(point, source))

    return Callable(source, target, evaluate, point_action=evaluate_point)


def framed_callable(data, source, target, session, interpret, finite_inventory=inventory,
                    product_factors=product_fields, read_point=None):
    """Consume typed maps, total finite graphs and owned callable data.

    ``interpret`` is the implementation's explicit registered-arrow reader. This
    module never infers an action from an address or from equal carrier data.
    """
    if isinstance(data, dict) and data.get("ctor") == "valueData":
        return framed_callable(fields(data, "valueData", 1)[0], source, target,
                               session, interpret, finite_inventory, product_factors, read_point)
    if isinstance(data, dict) and data.get("ctor") == "typedMap":
        actual_source, actual_target, body = typed_map(data)
        same(actual_source, source, "callable source")
        same(actual_target, target, "callable target")
        return framed_callable(body, source, target, session, interpret, finite_inventory, product_factors, read_point)
    if isinstance(data, dict) and data.get("ctor") == "opaqueData":
        native = session.get(data)
        if not isinstance(native, Callable):
            raise ValueError("the owned data is not a callable")
        same(native.source, source, "owned callable source")
        same(native.target, target, "owned callable target")
        return native
    if isinstance(data, list) or isinstance(data, dict) and data.get("ctor") == "finiteGraph":
        return graph_callable(data, source, target, finite_inventory, read_point)
    if isinstance(data, dict) and data.get("ctor") == "identity":
        actual_source, actual_target = fields(data, "identity", 2)
        same(actual_source, source, "identity source")
        same(actual_target, target, "identity target")
        same(source, target, "identity endpoints")
        return Callable(source, target, lambda point: point, NativeIdentity(source, target),
                        point_action=lambda point, read: point)
    if isinstance(data, dict) and data.get("ctor") == "mediator":
        left, right = fields(data, "mediator", 2)
        left_target, right_target = product_factors(target, (left, right))
        f = framed_callable(left, source, left_target, session, interpret, finite_inventory, product_factors, read_point)
        g = framed_callable(right, source, right_target, session, interpret, finite_inventory, product_factors, read_point)
        native = NativeMediator(source, target, f.native, g.native) if f.native is not None and g.native is not None else None
        return Callable(source, target, lambda point: [f(point), g(point)], native,
                        point_action=lambda point, read: [f.at_point(point, read), g.at_point(point, read)])
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
        f = framed_callable(first, source, middle, session, interpret, finite_inventory, product_factors, read_point)
        g = framed_callable(second, middle, target, session, interpret, finite_inventory, product_factors, read_point)
        native = NativeComposition(f.native, g.native) if f.native is not None and g.native is not None else None
        return Callable(source, target, lambda point: g(f(point)), native,
                        point_action=lambda point, read: g.at_point(f.at_point(point, read), read))
    if isinstance(data, dict) and data.get("ctor") == "morphismEndpoint":
        morphism_endpoint(data)
        raise ValueError("a morphism endpoint is object data, not a callable")
    return interpret(data, source, target)
