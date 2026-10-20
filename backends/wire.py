"""The kernel's structural wire encoding, as the backends read and write it.

An input is a named object of the catalogue at its parameters,
`{"ctor": <object id>, "args": [<parameters>]}`, numeral parameters as JSON numbers. An answer is a
value of the operation's result form, a constructor application `{"ctor": <constructor>,
"args": [...]}` with the constructor spelled by its short name in the form's Lean type:

* `meth.cardinality` lands in `Card`, whose literal form `lit.cardinals` has the type
  `CardinalLiteral` with constructors `finite (n : ℕ)` and `aleph0`;
* a property is decided as `Option Bool`: `some true`, `some false`, or `none`.
"""

import json


def named_object(value):
    """The object id and the parameters of an input."""
    if not isinstance(value, dict) or "ctor" not in value:
        raise ValueError("not a named object: %r" % (value,))
    return value["ctor"], list(value.get("args") or [])


def numeral(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("not a numeral parameter: %r" % (value,))
    return value


def carrier_object(value):
    """Read the retained computational object of a carrier-view request.

    This does not select a formal path, compare presentations, or evaluate a
    functor. Callers use it only for the carrier operations they register.
    """
    ctor, args = named_object(value)
    if ctor in {"functorAction", "objectPresentation"} and len(args) == 2:
        return carrier_object(args[1])
    if ctor in {"subobject", "valueData"} and args:
        return carrier_object(args[0])
    if ctor == "finiteData" and len(args) == 2:
        return carrier_object(args[0])
    return ctor, args


def finite_inventory(value):
    """An actual supplied finite inventory, without enumerating formal objects."""
    ctor, args = named_object(value)
    if ctor == "finiteData" and len(args) == 2:
        if not isinstance(args[1], list):
            raise ValueError("a finite carrier inventory must be a list")
        keys = [json.dumps(point, sort_keys=True) for point in args[1]]
        if len(set(keys)) != len(keys):
            raise ValueError("a finite carrier inventory repeats a point")
        return args[1]
    if ctor in {"functorAction", "objectPresentation"} and len(args) == 2:
        return finite_inventory(args[1])
    if ctor in {"subobject", "valueData"} and args:
        return finite_inventory(args[0])
    if ctor == "liftedSubobject":
        if len(args) != 4 or not args[3]:
            raise ValueError("a completed liftedSubobject needs its actual component outputs")
        # Steps are retained in route order but executed in reverse order.
        # The outermost (first) step supplies the completed result carrier.
        step_ctor, step_args = named_object(args[3][0])
        if step_ctor != "liftStep" or len(step_args) != 5 or len(step_args[4]) != 4:
            raise ValueError("a completed lift step needs all four actual outputs")
        return finite_inventory(step_args[4][0])
    return None


def finite_data(descriptor, points):
    return {"ctor": "finiteData", "args": [descriptor, points]}


def finite_graph(points, graph):
    return {"ctor": "finiteGraph", "args": [points, graph]}


def graph_data(value):
    """Unpack released finite framing; establish no mathematical carrier claim."""
    inventory = None
    if isinstance(value, dict):
        ctor, args = named_object(value)
        if ctor == "typedMap" and len(args) == 3:
            graph = graph_data(args[2])
            source, target = finite_inventory(args[0]), finite_inventory(args[1])
            if source is not None:
                source_keys = {json.dumps(point, sort_keys=True) for point in source}
                graph_keys = {json.dumps(pair[0], sort_keys=True) for pair in graph}
                if source_keys != graph_keys:
                    raise ValueError("a typed graph must contain its supplied domain inventory")
            if target is not None:
                target_keys = {json.dumps(point, sort_keys=True) for point in target}
                if any(json.dumps(pair[1], sort_keys=True) not in target_keys for pair in graph):
                    raise ValueError("a typed graph image is outside its supplied codomain inventory")
            return graph
        if ctor != "finiteGraph" or len(args) != 2:
            raise ValueError("expected a finite graph or its declared framing")
        inventory, value = args
        if not isinstance(inventory, list):
            raise ValueError("a finite graph inventory must be a list")
    if not isinstance(value, list):
        raise ValueError("a finite graph requires point-image pairs")
    keys = []
    for pair in value:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("a graph entry requires its point and image")
        keys.append(json.dumps(pair[0], sort_keys=True))
    if len(set(keys)) != len(keys):
        raise ValueError("a finite graph repeats a domain point")
    if inventory is not None:
        expected = [json.dumps(point, sort_keys=True) for point in inventory]
        if len(set(expected)) != len(expected) or set(keys) != set(expected):
            raise ValueError("a graph must contain exactly its actual supplied domain inventory")
    return value


def finite_cardinal(n):
    return {"ctor": "finite", "args": [int(n)]}


def aleph0():
    return {"ctor": "aleph0", "args": []}


def decision(answer):
    """`answer` is True, False or None (undecided)."""
    if answer is None:
        return {"ctor": "none", "args": []}
    return {"ctor": "some", "args": [{"ctor": "true" if answer else "false", "args": []}]}
