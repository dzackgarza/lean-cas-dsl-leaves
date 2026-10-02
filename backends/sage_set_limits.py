"""The Sage set-limits backend: `lim.sets.product`, `colim.sets.coproduct` and `lim.sets.pullback`
on `cat.sets`.

Engine: Sage (passagemath, `sage.all__sagemath_combinat`), run under `$CAS_SAGE_PYTHON` or the
workspace's `.venv/bin/python` (`engine_python`). Routines:

* `lim.sets.product` on `pair X Y`: `cartesian_product([S, T])` (`sage.sets.cartesian_product`);
* `colim.sets.coproduct` on `pair X Y`: `DisjointUnionEnumeratedSets(..., keepkey=True)`
  (`sage.sets.disjoint_union_enumerated_sets`);
* `lim.sets.pullback` on `cospan f g`: the pairs `(x, y)` with `f x = g y`, selected from Sage's
  enumeration of `cartesian_product([dom f, dom g])` (`FiniteEnumeratedSet` of each domain).

Wire (`CasContract/Port.lean`, "The wire encoding of inputs and answers"): a diagram is
`{"ctor": "pair", "args": [X, Y]}` with named objects, or `{"ctor": "cospan", "args": [f, g]}`
with morphisms as graphs `[[x, f x], ...]`. The answer is `{"ctor": "cone" | "cocone",
"args": [apex, leg, leg]}`, the two legs of Mathlib's `BinaryFan.mk`, `BinaryCofan.mk` and
`PullbackCone.mk`. The catalogue names no object of `cat.sets` for `X × Y`, `X ⊕ Y` or a pullback,
so the apex is `Fin m` (`obj.sets.fin`) in Sage's enumeration order, and each leg is a finite graph:
only finite diagrams are answered, and anything else fails.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

import json

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_combinat")

from cas_port import serve  # noqa: E402  the leaf contract's reference port
from sage.all__sagemath_combinat import Zmod, cartesian_product  # noqa: E402
from sage.sets.disjoint_union_enumerated_sets import DisjointUnionEnumeratedSets  # noqa: E402
from sage.sets.family import Family  # noqa: E402
from sage.sets.finite_enumerated_set import FiniteEnumeratedSet  # noqa: E402
from sage.sets.integer_range import IntegerRange  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"


def residues(n):
    if numeral(n) == 0:
        raise ValueError("ZMod 0 = ℤ is infinite: its maps have no finite graph")
    return Zmod(n)


# The finite named sets accepted as objects of a `pair`: their Sage parent, and the wire encoding
# of an element (a point of `Fin n`, and of `ZMod n = Fin n` for n > 0, is its number).
PARENTS = {
    "obj.sets.fin": (lambda n: IntegerRange(0, numeral(n)), int),
    "obj.sets.integers_mod": (residues, lambda r: int(r.lift())),
}


def finite_set(value):
    ctor, params = named_object(value)
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
    return {"ctor": kind, "args": [fin(apex_size), *legs]}


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
    position = {(int(i), encode[int(i)](x)): k for k, (i, x) in enumerate(U)}
    return answer("cocone", len(U),
                  [[ex(x), position[(0, ex(x))]] for x in S],
                  [[ey(y), position[(1, ey(y))]] for y in T])


def graph(value):
    """A morphism's graph as a dict over canonical JSON keys, with its domain in order."""
    if not isinstance(value, list):
        raise ValueError("a morphism is a list of pairs: %r" % (value,))
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
