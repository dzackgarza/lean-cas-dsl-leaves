"""The Sage set-limits backend: `lim.sets.product`, `colim.sets.coproduct` and `lim.sets.pullback`
on `cat.sets`.

Engine: Sage (passagemath, `sage.all__sagemath_combinat`), run under `$CAS_SAGE_PYTHON` or the
workspace's `.venv/bin/python` (`engine_python`). Routines:

* `lim.sets.product` on `pair X Y`: `cartesian_product([S, T])` (`sage.sets.cartesian_product`);
* `colim.sets.coproduct` on `pair X Y`: `DisjointUnionEnumeratedSets(..., keepkey=True)`
  (`sage.sets.disjoint_union_enumerated_sets`);
* `lim.sets.pullback` on `cospan f g`: the pairs `(x, y)` with `f x = g y`, selected from Sage's
  `cartesian_product([dom f, dom g])` by Sage's `ConditionSet` enumeration
  (`FiniteEnumeratedSet` of each domain).

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
from sage.sets.condition_set import ConditionSet  # noqa: E402
from sage.sets.family import Family  # noqa: E402
from sage.sets.finite_enumerated_set import FiniteEnumeratedSet  # noqa: E402
from sage.sets.integer_range import IntegerRange  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402
from sage.modules.free_module import FreeModule  # noqa: E402

from wire import constructor, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"


def residues(n):
    if numeral(n) == 0:
        raise ValueError("ZMod 0 = ℤ is infinite: its maps have no finite graph")
    return Zmod(n)


# The finite named sets accepted as objects of a `pair`: their Sage parent, and the wire encoding
# of an element (a point of `Fin n`, and of `ZMod n = Fin n` for n > 0, is its number).
PARENTS = {
    "obj.sets.fin": (lambda n: IntegerRange(0, numeral(n)), int),
    "obj.finite_sets.fin": (lambda n: IntegerRange(0, numeral(n)), int),
    "obj.sets.integers_mod": (residues, lambda r: int(r.lift())),
    "obj.sets.integers_mod_power": (
        lambda n, k: FreeModule(residues(n), numeral(k)),
        lambda row: [int(r.lift()) for r in row]),
}


def finite_set(value):
    ctor, params = named_object(value)
    if ctor not in PARENTS:
        raise ValueError("no finite Sage parent for %s" % ctor)
    make, encode = PARENTS[ctor]
    return make(*params), encode


def diagram(value, shape, arity):
    return constructor(value, shape, arity)


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


def native_point(value):
    """Decode field arithmetic before comparing points or applying a native map."""
    if isinstance(value, dict) and value.get("ctor") == "element":
        from sage_field_presentations import field, selected_element
        descriptor, _ = constructor(value, "element", 2)
        return selected_element(value, descriptor, field(descriptor))
    return json.dumps(value, sort_keys=True)


def field_arrow(value):
    """Released selected F9 arrow, evaluated as a Sage homomorphism."""
    from sage_field_presentations import field
    comparison, parameters, inverse = constructor(value, "presentation", 3)
    if comparison != "cmp.f9.translation" or parameters or not isinstance(inverse, bool):
        raise ValueError("no selected field arrow model for this comparison")
    source = field({"ctor": "obj.sets.f9_y" if inverse else "obj.sets.f9_x", "args": []})
    target = field({"ctor": "obj.sets.f9_x" if inverse else "obj.sets.f9_y", "args": []})
    return source.hom([target.gen() - 2 if inverse else target.gen() + 2], target)


def carrier_edge(value):
    """Only released forgetful routes with unchanged underlying points."""
    ctor, args = named_object(value)
    if ctor == "classifierForget":
        if len(args) != 2 or args[1] != [] or args[0] not in {
                "clf.magmas.associative", "clf.sets.binary_operation"}:
            raise ValueError("no carrier model for this instantiated classifier")
    elif ctor not in {"fun.commutative_rings.ring", "fun.rings.multiplicative_monoid",
                      "fun.monoids.semigroup"} or args:
        raise ValueError("no carrier model for this functor edge")


def graph(value):
    """A morphism's graph as a dict over canonical JSON keys, with its domain in order."""
    if isinstance(value, dict):
        ctor, params = named_object(value)
        if ctor == "map":
            edge, arrow = constructor(value, "map", 2)
            carrier_edge(edge)
            return graph(arrow)
        if ctor == "compose":
            first, second = constructor(value, "compose", 2)
            table = graph(first)
            # A presentation is applied by its selected native Sage field map.
            mapped = second
            while isinstance(mapped, dict) and mapped.get("ctor") == "map":
                edge, mapped = constructor(mapped, "map", 2)
                carrier_edge(edge)
            if isinstance(mapped, dict) and mapped.get("ctor") == "presentation":
                hom = field_arrow(mapped)
                return {key: hom(point) for key, point in table.items()}
            later = graph(second)
            return {key: later[json.dumps(point, sort_keys=True)] for key, point in table.items()}
        if ctor == "presentation":
            hom = field_arrow(value)
            from sage_field_presentations import arithmetic_data
            source_id = "obj.sets.f9_y" if params[2] else "obj.sets.f9_x"
            descriptor = {"ctor": source_id, "args": []}
            return {json.dumps({"ctor": "element", "args": [descriptor, arithmetic_data(x)]},
                               sort_keys=True): hom(x) for x in hom.domain()}
        if ctor == "generator":
            object_id, explicit = constructor(value, "generator", 2)
            if object_id not in {"obj.sets.f9_x", "obj.sets.f9_y"} or explicit:
                raise ValueError("no selected field generator arrow model")
            from sage_field_presentations import field
            return {"0": field({"ctor": object_id, "args": []}).gen()}
        fields = {"mor.sets.f9_x_constants": "obj.sets.f9_x",
                  "mor.sets.f9_y_constants": "obj.sets.f9_y"}
        if ctor in fields and not params:
            from sage_field_presentations import field
            target = field({"ctor": fields[ctor], "args": []})
            # The released constant map has domain ZMod 3. Sage performs the
            # coefficient embedding into the selected quotient field model.
            return {json.dumps(int(x.lift())): target(int(x.lift())) for x in Zmod(3)}
        raise ValueError("no Sage finite graph translation for %s" % ctor)
    if not isinstance(value, list):
        raise ValueError("a morphism is a list of pairs: %r" % (value,))
    table = {}
    for pair in value:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("not a pair [x, f x]: %r" % (pair,))
        key = json.dumps(pair[0], sort_keys=True)
        if key in table:
            raise ValueError("the graph lists %s twice" % key)
        table[key] = native_point(pair[1])
    return table


def op_pullback(value):
    f, g = (graph(m) for m in diagram(value, "cospan", 2))
    # Sage owns the constrained-set enumeration; the predicate applies the wire graphs.
    universe = cartesian_product([FiniteEnumeratedSet(f), FiniteEnumeratedSet(g)])
    P = list(ConditionSet(universe, lambda p: f[p[0]] == g[p[1]]))
    return answer("cone", len(P),
                  [[k, json.loads(p[0])] for k, p in enumerate(P)],
                  [[k, json.loads(p[1])] for k, p in enumerate(P)])


if __name__ == "__main__":
    serve("sage", SAGE_VERSION, ADAPTER_VERSION,
          {"lim.sets.product": op_product, "colim.sets.coproduct": op_coproduct,
           "lim.sets.pullback": op_pullback})
