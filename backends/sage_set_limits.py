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

from cas_port import point_invocation, serve, value_data  # noqa: E402
Zmod = engine.Zmod
cartesian_product = engine.cartesian_product
from sage.sets.disjoint_union_enumerated_sets import DisjointUnionEnumeratedSets  # noqa: E402
from sage.sets.family import Family  # noqa: E402
from sage.sets.finite_enumerated_set import FiniteEnumeratedSet  # noqa: E402
from sage.combinat.permutation import Permutation  # noqa: E402
from sage.sets.integer_range import IntegerRange  # noqa: E402
from sage.sets.non_negative_integers import NonNegativeIntegers  # noqa: E402
from sage.sets.positive_integers import PositiveIntegers  # noqa: E402
from sage.sets.primes import Primes  # noqa: E402
from sage.rings.integer_ring import ZZ  # noqa: E402
from sage.rings.rational_field import QQ  # noqa: E402
from sage.rings.infinity import Infinity  # noqa: E402
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import aleph0, finite_cardinal, finite_data, finite_graph, finite_inventory, graph_data, named_object, numeral  # noqa: E402

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


# Infinite named sets accepted as product factors. Sage's `cardinality()` of each countable
# parent confirms it is infinite, and Sage's `+Infinity` is read as `aleph0` only on these
# countable parents (`ZZ`, `QQ`, the enumerated sets of naturals, polynomial rings over them).
# `ℝ` and `ℂ` are uncountable: they are product factors, but have no `lit.cardinals` value.
COUNTABLE = {
    "obj.sets.naturals": NonNegativeIntegers,
    "obj.sets.positive_naturals": PositiveIntegers,
    "obj.sets.primes": Primes,
    "obj.sets.integers": lambda: ZZ,
    "obj.sets.rationals": lambda: QQ,
}
UNCOUNTABLE = {"obj.sets.reals", "obj.sets.complexes"}
COUNTABLE_COEFFICIENTS = {"integers": ZZ, "rationals": QQ}


def polynomial_parent(args):
    ctor, params = named_object(args[0])
    kind = ctor.rsplit(".", 1)[-1]
    if kind in COUNTABLE_COEFFICIENTS:
        return PolynomialRing(COUNTABLE_COEFFICIENTS[kind], "x"), True
    if kind == "integers_mod" and params and numeral(params[0]) > 0:
        return PolynomialRing(Zmod(numeral(params[0])), "x"), True
    raise ValueError("no countable Sage polynomial ring over %s" % ctor)


def member_key(point):
    """A canonical key for a literal member: integer arithmetic data by Sage's `ZZ`,
    anything else by its canonical JSON."""
    try:
        return json.dumps(int(integer_point(point)))
    except ValueError:
        return json.dumps(point, sort_keys=True)


def integer_point(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return ZZ(value)
    ctor, args = named_object(value)
    if ctor == "element" and len(args) == 2:
        return integer_point(args[1])
    if ctor == "valueData" and len(args) == 1:
        return integer_point(args[0])
    if ctor == "numeral" and len(args) == 1:
        return ZZ(numeral(args[0]))
    if ctor == "neg" and len(args) == 1:
        return -integer_point(args[0])
    if ctor in {"add", "mul"} and len(args) == 2:
        a, b = (integer_point(x) for x in args)
        return a + b if ctor == "add" else a * b
    raise ValueError("not integer arithmetic data: %s" % ctor)


def literal_set(points):
    """The distinct members of a finite literal, in order, as Sage's `FiniteEnumeratedSet`."""
    members = {}
    for p in points:
        members.setdefault(member_key(p), p)
    return FiniteEnumeratedSet(list(members)), lambda key: members[key]


def carrier(value):
    """("finite", Sage set, point encoder) or ("infinite", Sage parent, countable)."""
    if isinstance(value, list):
        return ("finite",) + literal_set(value)
    inventory = finite_inventory(value)
    if inventory is not None:
        keys = [json.dumps(point, sort_keys=True) for point in inventory]
        return "finite", FiniteEnumeratedSet(keys), json.loads
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
        return carrier(source)
    if ctor == "objectPresentation":
        if len(params) != 2:
            raise ValueError("objectPresentation requires an action and actual data")
        action, actual = params
        if not isinstance(action, dict) or action.get("ctor") != "functorAction":
            raise ValueError("objectPresentation has no selected action")
        return carrier(actual)
    if ctor == "subobject":
        if len(params) != 3:
            raise ValueError("subobject requires apex, ambient, and inclusion")
        return carrier(params[0])
    if ctor == "valueData":
        if len(params) != 1:
            raise ValueError("valueData requires its data")
        return carrier(params[0])
    if ctor == "extent":
        if len(params) != 3 or not isinstance(params[2], list):
            raise ValueError("extent requires its power object, ambient set and literal members")
        return ("finite",) + literal_set(params[2])
    if ctor == "constructionApex":
        if len(params) != 3:
            raise ValueError("constructionApex requires its limit, diagram and computed cone")
        cone_ctor, cone = named_object(params[2])
        if cone_ctor not in {"cone", "cocone"} or not cone:
            raise ValueError("constructionApex requires the computed cone or cocone")
        return carrier(cone[0])
    if ctor == "objectProduct":
        if len(params) != 2:
            raise ValueError("objectProduct requires both factors")
        factors = [carrier(x) for x in params]
        if all(f[0] == "finite" for f in factors):
            P = cartesian_product([factors[0][1], factors[1][1]])
            return "finite", FiniteEnumeratedSet(list(P)), lambda p: [factors[0][2](p[0]),
                                                                        factors[1][2](p[1])]
        if any(f[0] == "finite" and f[1].cardinality() == 0 for f in factors):
            return "finite", FiniteEnumeratedSet([]), json.loads
        return "infinite", value, all(f[0] == "finite" or f[2] for f in factors)
    if ctor in {"obj.sets.polynomials"} and len(params) == 1:
        R, countable = polynomial_parent(params)
        if R.cardinality() != Infinity:
            raise ValueError("Sage reports a finite polynomial ring %s" % R)
        return "infinite", value, countable
    if ctor in COUNTABLE:
        if COUNTABLE[ctor]().cardinality() != Infinity:
            raise ValueError("Sage reports %s finite" % ctor)
        return "infinite", value, True
    if ctor in UNCOUNTABLE:
        return "infinite", value, False
    if ctor in {"obj.sets.integers_mod", "obj.rings.integers_mod"} and params == [0]:
        return "infinite", value, True  # ZMod 0 = ℤ
    if ctor not in PARENTS:
        raise ValueError("no Sage parent for %s" % ctor)
    make, encode = PARENTS[ctor]
    S = make(*params)
    if S.cardinality() == Infinity:
        return "infinite", value, True
    return "finite", S, encode


def finite_set(value):
    kind, S, encode = carrier(value)
    if kind != "finite":
        raise ValueError("this construction requires finite factors")
    return S, encode


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


# Projections of a symbolic product apex, owned by this connection: token -> leg index.
PROJECTIONS = {}


def op_product(value):
    if isinstance(value, dict) and value.get("ctor") == "apply":
        return project(value)
    X, Y = diagram(value, "pair", 2)
    (kx, S, ex), (ky, T, ey) = carrier(X), carrier(Y)
    if kx == ky == "finite":
        # Sage: cartesian_product([S, T]), enumerated
        P = list(cartesian_product([S, T]))
        return answer("cone", len(P),
                      [[k, ex(p[0])] for k, p in enumerate(P)],
                      [[k, ey(p[1])] for k, p in enumerate(P)])
    # An infinite factor: the apex is the declared product descriptor of the two factors and
    # each leg is a connection-local projection callable (an `opaqueData` token).
    legs, cone_id = [], len(PROJECTIONS) // 2
    for index in (0, 1):
        token = "product-projection-%d-%d" % (cone_id, index)
        PROJECTIONS[token] = index
        legs.append({"ctor": "opaqueData", "args": [token]})
    return {"ctor": "cone", "args": [{"ctor": "objectProduct", "args": [X, Y]}, *legs]}


def project(value):
    """A projection leg invoked on a point `[x, y]` of the symbolic product apex."""
    _, _, arrow, domain, _, _, data = point_invocation(value, "lim.sets.product")
    ctor, args = named_object(arrow)
    if ctor != "opaqueData" or len(args) != 1 or args[0] not in PROJECTIONS:
        raise ValueError("this connection owns no projection for %r" % (arrow,))
    while isinstance(data, dict) and data.get("ctor") == "valueData":
        data = data["args"][0]
    if not isinstance(data, list) or len(data) != 2:
        raise ValueError("a point of a binary product is the pair of its components")
    return value_data(data[PROJECTIONS[args[0]]])


def op_cardinality(value):
    """`meth.cardinality` on an object of `Sets`: Sage `cardinality()` of its enumerated
    carrier, or `aleph0` on Sage's infinite countable parents."""
    kind, S, extra = carrier(value)
    if kind == "finite":
        return finite_cardinal(S.cardinality())
    if not extra:
        raise ValueError("the set is uncountable: no value of lit.cardinals (finite n | aleph0)")
    return aleph0()


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
       "meth.cardinality": op_cardinality,
       "lim.sets.pullback": op_pullback})
