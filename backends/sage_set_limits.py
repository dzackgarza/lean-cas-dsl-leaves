"""The Sage set-limits backend: `lim.sets.product`, `colim.sets.coproduct` and `lim.sets.pullback`
on `cat.sets`.

Engine: Sage (`sage.all`), run under `$CAS_SAGE_PYTHON` or the
workspace's `.venv/bin/python` (`engine_python`). Routines:

* `lim.sets.product` on `pair X Y`: `cartesian_product([S, T])` (`sage.sets.cartesian_product`);
* `colim.sets.coproduct` on `pair X Y`: `DisjointUnionEnumeratedSets(..., keepkey=True)`
  (`sage.sets.disjoint_union_enumerated_sets`);
* `lim.sets.pullback` on `cospan f g`: the pairs `(x, y)` with `f x = g y`, selected from Sage's
  enumeration of `cartesian_product([dom f, dom g])` (`FiniteEnumeratedSet` of each domain).

Wire (`CasContract/Port.lean`, "The wire encoding of inputs and answers"): a diagram is
`{"ctor": "pair", "args": [X, Y]}` with complete object descriptors (including retained
`functorAction` and `objectPresentation`), or `{"ctor": "cospan", "args": [f, g]}`
with morphisms as graphs `[[x, f x], ...]`. The answer is `{"ctor": "cone" | "cocone",
"args": [apex, leg, leg]}`, the two legs of Mathlib's `BinaryFan.mk`, `BinaryCofan.mk` and
`PullbackCone.mk`. The returned computational apex uses `finiteData` around `obj.sets.fin`
in Sage's enumeration order, and every defining leg uses `finiteGraph` with its
actual domain inventory. Supplied finite inventories are retained as point data
instead of being reconstructed from the object descriptor. Only finite diagrams
are answered, and anything else fails.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

import json

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_combinat", "sage.all"))

from cas_port import serve  # noqa: E402  the leaf contract's reference port
Zmod = engine.Zmod
cartesian_product = engine.cartesian_product
from sage.sets.disjoint_union_enumerated_sets import DisjointUnionEnumeratedSets  # noqa: E402
from sage.sets.family import Family  # noqa: E402
from sage.sets.finite_enumerated_set import FiniteEnumeratedSet  # noqa: E402
from sage.combinat.permutation import Permutation  # noqa: E402
from sage.sets.integer_range import IntegerRange  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import finite_data, finite_graph, finite_inventory, graph_data, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"


def residues(n):
    if numeral(n) == 0:
        raise ValueError("ZMod 0 = ℤ is infinite: its maps have no finite graph")
    return Zmod(n)


# The finite primitive sets accepted as objects of a `pair`: their Sage parent, and the wire encoding
# of an element (a point of `Fin n`, and of `ZMod n = Fin n` for n > 0, is its number).
PARENTS = {
    "obj.sets.fin": (lambda n: IntegerRange(0, numeral(n)), int),
    "obj.finite_sets.fin": (lambda n: IntegerRange(0, numeral(n)), int),
    "obj.sets.integers_mod": (residues, lambda r: int(r.lift())),
    "obj.rings.integers_mod": (residues, lambda r: int(r.lift())),
}


def finite_set(value):
    inventory = finite_inventory(value)
    if inventory is not None:
        keys = [json.dumps(point, sort_keys=True) for point in inventory]
        return FiniteEnumeratedSet(keys), json.loads
    ctor, params = named_object(value)
    if ctor == "functorAction":
        if len(params) != 2:
            raise ValueError("functorAction requires an edge and a source object")
        edge, source = params
        if not isinstance(edge, dict) or not isinstance(edge.get("ctor"), str):
            raise ValueError("functorAction has no edge descriptor")
        # Compute an enumeration of the selected source's points. The retained
        # edge is semantic data validated by the caller, not a leaf assertion
        # that the source and image are identified.
        return finite_set(source)
    if ctor == "objectPresentation":
        if len(params) != 2:
            raise ValueError("objectPresentation requires an action and actual data")
        action, actual = params
        if not isinstance(action, dict) or action.get("ctor") != "functorAction":
            raise ValueError("objectPresentation has no selected action")
        return finite_set(actual)
    if ctor == "subobject":
        if len(params) != 3:
            raise ValueError("subobject requires apex, ambient, and inclusion")
        return finite_set(params[0])
    if ctor == "valueData":
        if len(params) != 1:
            raise ValueError("valueData requires its data")
        return finite_set(params[0])
    if ctor not in PARENTS:
        raise ValueError("no finite Sage parent for %s" % ctor)
    make, encode = PARENTS[ctor]
    return make(*params), encode


def diagram(value, shape, arity):
    if not isinstance(value, dict) or value.get("ctor") != shape:
        raise ValueError("expected a %s diagram: %r" % (shape, value))
    args = list(value.get("args") or [])
    if len(args) != arity:
        raise ValueError("%s takes %d arguments, got %d" % (shape, arity, len(args)))
    return args


def fin(m):
    return {"ctor": "obj.sets.fin", "args": [int(m)]}


def answer(kind, apex_size, *legs):
    return {"ctor": kind, "args": [finite_data(fin(apex_size), list(range(apex_size))),
                                    *[finite_graph([p[0] for p in leg], leg) for leg in legs]]}


def op_product(value):
    X, Y = diagram(value, "pair", 2)
    (S, ex), (T, ey) = finite_set(X), finite_set(Y)
    # Sage: cartesian_product([S, T]), enumerated
    P = list(cartesian_product([S, T]))
    return answer("cone", len(P),
                  [[k, ex(p[0])] for k, p in enumerate(P)],
                  [[k, ey(p[1])] for k, p in enumerate(P)])


def op_coproduct(value):
    X, Y = diagram(value, "pair", 2)
    (S, ex), (T, ey) = finite_set(X), finite_set(Y)
    # Sage: DisjointUnionEnumeratedSets with keepkey, elements (i, x) for i in {0, 1}
    U = list(DisjointUnionEnumeratedSets(Family([S, T]), keepkey=True))
    encode = (ex, ey)
    position = {(int(i), json.dumps(encode[int(i)](x), sort_keys=True)): k
                for k, (i, x) in enumerate(U)}
    return answer("cocone", len(U),
                  [[ex(x), position[(0, json.dumps(ex(x), sort_keys=True))]] for x in S],
                  [[ey(y), position[(1, json.dumps(ey(y), sort_keys=True))]] for y in T])


def graph(value):
    """A morphism's graph as a dict over canonical JSON keys, with its domain in order."""
    if isinstance(value, dict) and value.get("ctor") == "mor.sets.fin_rev":
        _, args = named_object(value)
        if len(args) != 1:
            raise ValueError("Fin reversal requires its complete parameter")
        n = numeral(args[0])
        p = Permutation(list(range(n, 0, -1)))
        value = finite_graph(list(range(n)), [[i, int(p(i + 1)) - 1] for i in range(n)])
    value = graph_data(value)
    table = {}
    for pair in value:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("not a pair [x, f x]: %r" % (pair,))
        key = json.dumps(pair[0], sort_keys=True)
        if key in table:
            raise ValueError("the graph lists %s twice" % key)
        table[key] = json.dumps(pair[1], sort_keys=True)
    return table


def op_pullback(value):
    f, g = (graph(m) for m in diagram(value, "cospan", 2))
    # Sage: the pairs of cartesian_product([dom f, dom g]) with f x = g y
    P = [p for p in cartesian_product([FiniteEnumeratedSet(f), FiniteEnumeratedSet(g)])
         if f[p[0]] == g[p[1]]]
    return answer("cone", len(P),
                  [[k, json.loads(p[0])] for k, p in enumerate(P)],
                  [[k, json.loads(p[1])] for k, p in enumerate(P)])


serve("sage", SAGE_VERSION, ADAPTER_VERSION,
      {"lim.sets.product": op_product, "colim.sets.coproduct": op_coproduct,
       "lim.sets.pullback": op_pullback})
