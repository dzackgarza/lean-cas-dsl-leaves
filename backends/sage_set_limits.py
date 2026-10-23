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
`functorAction` and explicit projections of `objectPresentation`), or
`{"ctor": "cospan", "args": [f, g]}`
with morphisms as graphs `[[x, f x], ...]`, `finiteGraph` data, or complete
`typedMap(source, target, callable)` wrappers around those existing callable forms.
Nested typed wrappers retain the same complete endpoints, and two typed cospan
arrows retain the same complete target. Source/codomain inventories validate
supplied graph framing only; they establish no mathematical carrier or map law.
The answer is `{"ctor": "cone" | "cocone",
"args": [apex, leg, leg]}`, the two legs of Mathlib's `BinaryFan.mk`, `BinaryCofan.mk` and
`PullbackCone.mk`. The returned computational apex uses `finiteData` around `obj.sets.fin`
in Sage's enumeration order, and every defining leg uses `finiteGraph` with its
actual domain inventory. Supplied finite inventories are retained as point data
instead of being reconstructed from the object descriptor. Finite complete objects
and returned maps are reusable inside these same four operations. The existing infinite-product branch retains its symbolic apex and
connection-owned projections; it does not enumerate an infinite callable.

Consumer scope is the frozen public contract 6780f9f (Port and declared-ports.json):
complete product/coproduct/pullback records; valueData, finiteData, objectProduct;
selected point-preserving functor actions; constructionApex/Leg, including the
published finite-set pullback creation packet and nested retained contexts; and
actual Arrow/subobject presentations and completed lift fields through their
explicit projections. Stored graph/typedMap/owned projection callables and finite
compositions are read at their retained endpoints. Native Sage SetMorphism
composition uses private inventory indices; these indices never identify public
objects. Unknown actions, unstored pullback-center legs, unreified formal limit
references, and missing inventories or endpoint contexts remain unsupported.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

import json

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_combinat", "sage.all"))

from cas_port import point_invocation, serve, typed_map, value_data  # noqa: E402
Zmod = engine.Zmod
cartesian_product = engine.cartesian_product
from sage.sets.disjoint_union_enumerated_sets import DisjointUnionEnumeratedSets  # noqa: E402
from sage.sets.family import Family  # noqa: E402
from sage.categories.homset import Hom  # noqa: E402
from sage.categories.morphism import SetMorphism  # noqa: E402
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

ADAPTER_VERSION = "0.2.0"


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
    "obj.commutative_rings.integers_mod": (residues, lambda r: int(r.lift())),
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
    "obj.semirings.naturals": NonNegativeIntegers,
    "obj.rings.integers": lambda: ZZ,
    "obj.rings.rationals": lambda: QQ,
    "obj.commutative_rings.integers": lambda: ZZ,
    "obj.commutative_rings.rationals": lambda: QQ,
}
UNCOUNTABLE = {"obj.sets.reals", "obj.sets.complexes", "obj.rings.reals",
               "obj.rings.complexes", "obj.commutative_rings.reals",
               "obj.commutative_rings.complexes"}
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


class UnsupportedCarrier(ValueError):
    """No existing native codec; a finiteGraph may still supply its own domain."""


def fields(value, ctor, arity):
    if not isinstance(value, dict) or value.get("ctor") != ctor:
        raise ValueError("expected complete %s data" % ctor)
    args = value.get("args")
    if not isinstance(args, list) or len(args) != arity:
        raise ValueError("%s requires %d complete fields" % (ctor, arity))
    return args


def unbox(value):
    while isinstance(value, dict) and value.get("ctor") == "valueData":
        value, = fields(value, "valueData", 1)
    return value


def node(ctor, *args):
    return {"ctor": ctor, "args": list(args)}


def inventory_keys(inventory):
    keys = [json.dumps(point, sort_keys=True) for point in inventory]
    if len(set(keys)) != len(keys):
        raise ValueError("a supplied endpoint inventory repeats a point")
    return keys


# Native codecs for these exact published actions keep their point data. This is
# an implementation boundary, not a rule for arbitrary functors with similar names.
POINT_ACTIONS = {
    "fun.sets.identity", "fun.semirings.forget", "fun.commutative_rings.ring",
    "fun.rings.multiplicative_monoid", "fun.monoids.semigroup",
}
CLASSIFIER_ACTIONS = {
    "clf.sets.finite", "clf.sets.binary_operation", "clf.magmas.associative",
}
FINITE_FORGET = node("classifierForget", "clf.sets.finite", [])


def preserving_action(edge):
    ctor, args = named_object(edge)
    if ctor in POINT_ACTIONS and args == []:
        return
    if (ctor == "classifierForget" and len(args) == 2
            and args[0] in CLASSIFIER_ACTIONS and args[1] == []):
        return
    raise ValueError("no point-data codec for selected action %r" % (edge,))


def selected_endpoint(expected, *actual):
    """Match complete descriptors or explicitly retained projection receivers only."""
    available = [x for x in actual if x is not None]
    if expected is None:
        return available[0] if available else None
    if available and expected not in available:
        raise ValueError("a callable changed its complete endpoint")
    return expected


def arrow_record(value):
    """Read returned fields, without executing a construction or choosing a lift."""
    value = unbox(value)
    ctor, args = named_object(value)
    if ctor == "objectPresentation":
        action, returned = fields(value, ctor, 2)
        fields(action, "functorAction", 2)
        return arrow_record(returned)
    if ctor == "liftedSubobject":
        base, original, route, steps = fields(value, ctor, 4)
        if (not isinstance(route, list) or not route or not isinstance(steps, list)
                or len(route) != len(steps)):
            raise ValueError("a completed lift requires its ordered route and every step")
        original_fields = arrow_record(original)
        current = arrow_record(base)
        for lift_id, step in reversed(list(zip(route, steps))):
            actual_id, action, source, supplied_base, outputs = fields(step, "liftStep", 5)
            if lift_id != actual_id or not isinstance(lift_id, str) or not lift_id:
                raise ValueError("a completed lift changed its prescribed step")
            if lift_id != "lift.bilin_module.restrict":
                raise ValueError("no completed-subobject codec for this selected lift")
            if not isinstance(outputs, list) or len(outputs) != 4:
                raise ValueError("a completed lift must retain all four outputs")
            source_fields = arrow_record(source)
            if arrow_record(supplied_base) != current:
                raise ValueError("a completed lift changed its preceding actual base")
            obj, inclusion, forward, backward = outputs
            image = node("functorAction", action, obj)
            for data, domain, codomain in ((inclusion, obj, source_fields[0]),
                                           (forward, image, current[0]),
                                           (backward, current[0], image)):
                a, b, _callable = typed_map(unbox(data))
                if (a, b) != (domain, codomain):
                    raise ValueError("a completed lift changed a retained map endpoint")
            current = (obj, source_fields[0], inclusion)
        if current[1] != original_fields[0]:
            raise ValueError("a completed lift changed its original source ambient")
        return current
    if ctor not in {"arrow", "subobject"}:
        raise ValueError("a projection requires a complete returned Arrow record")
    source, target, arrow = fields(value, ctor, 3)
    # Check typed wrappers, but do not evaluate the stored map or its laws.
    callable_wrappers(arrow, source, target)
    return source, target, arrow


CONSTRUCTION_FORMS = {
    "lim.sets.product": ("pair", "cone"),
    "colim.sets.coproduct": ("pair", "cocone"),
    "lim.sets.pullback": ("cospan", "cone"),
}


def construction_data(operation, source_diagram, complete):
    """Retain each creation layer's own diagram and read the actual result ports.

    BinaryFan.mk, BinaryCofan.mk and PullbackCone.mk each publish two
    non-propositional defining maps in the frozen public declaration snapshot.
    """
    if operation not in CONSTRUCTION_FORMS:
        raise ValueError("no complete-cone codec for %r" % (operation,))
    shape, kind = CONSTRUCTION_FORMS[operation]
    diagram(source_diagram, shape, 2)
    complete = unbox(complete)
    if isinstance(complete, dict) and complete.get("ctor") == "createdCone":
        lift_id, retained, returned = fields(complete, "createdCone", 3)
        if operation != "lim.sets.pullback" or lift_id != "lift.finite_sets.pullbacks":
            raise ValueError("no codec for this selected creation lift and operation")
        if retained != source_diagram:
            raise ValueError("a created cone changed its retained source diagram")
        returned = unbox(returned)
        mapped_diagram = node("cospan", *[node("map", FINITE_FORGET, arrow)
                                         for arrow in diagram(retained, "cospan", 2)])
        next_diagram = mapped_diagram
        if isinstance(returned, dict) and returned.get("ctor") == "createdCone":
            # Retain the next layer's own diagram. Supplied endpoint contexts
            # must still agree with this layer's selected mapped diagram; equal
            # carrier inventories do not identify different selected objects.
            _, next_diagram, _ = fields(returned, "createdCone", 3)
            for expected, actual in zip(diagram(mapped_diagram, "cospan", 2),
                                        diagram(next_diagram, "cospan", 2)):
                a, b = callable_context(expected), callable_context(actual)
                for x, y in zip(a[1:], b[1:]):
                    if x is not None and y is not None and x != y:
                        raise ValueError("a nested created cone changed its mapped endpoint context")
        cone, actual_diagram, _ = construction_data(operation, next_diagram, returned)
        return cone, actual_diagram, True
    cone = fields(complete, kind, 3)
    sides = diagram_sides(operation, source_diagram)
    for side, leg in zip(sides, cone[1:]):
        domain, codomain = (side, cone[0]) if kind == "cocone" else (cone[0], side)
        callable_wrappers(leg, domain, codomain)
    return cone, source_diagram, False


def diagram_sides(operation, source_diagram):
    shape, _ = CONSTRUCTION_FORMS[operation]
    sides = diagram(source_diagram, shape, 2)
    if shape == "pair":
        return sides
    contexts = [callable_context(arrow) for arrow in sides]
    targets = [c[2] for c in contexts if c[2] is not None]
    if len(targets) == 2 and targets[0] != targets[1]:
        raise ValueError("a retained cospan changed its complete common target")
    return [c[1] for c in contexts]


def construction_leg(value):
    operation, source_diagram, complete, index = fields(value, "constructionLeg", 4)
    cone, actual_diagram, created = construction_data(operation, source_diagram, complete)
    if operation == "lim.sets.pullback":
        index, = fields(index, "some", 1)
    if index == node("left"):
        number = 0
    elif index == node("right"):
        number = 1
    else:
        raise ValueError("the published constructor has no stored leg at this index")
    actual_side = diagram_sides(operation, actual_diagram)[number]
    source_side = diagram_sides(operation, source_diagram)[number]
    apex = cone[0]
    leg = cone[number + 1]
    if operation == "colim.sets.coproduct":
        actual_source, actual_target = actual_side, apex
    else:
        actual_source, actual_target = apex, actual_side
    _data, actual_source, actual_target = callable_context(leg, actual_source, actual_target)
    if actual_source is None or actual_target is None:
        raise ValueError("a returned leg needs its actual complete endpoint context")
    projection_apex = node("constructionApex", operation, source_diagram, complete)
    if operation == "colim.sets.coproduct":
        source_aliases, target_aliases = [source_side, actual_source], [projection_apex, apex]
    else:
        source_aliases = [projection_apex, apex]
        target_aliases = [source_side, actual_target] if created else [actual_target]
    return leg, actual_source, actual_target, source_aliases, target_aliases


def carrier(value):
    """("finite", Sage set, point encoder) or ("infinite", Sage parent, countable)."""
    if isinstance(value, list):
        return ("finite",) + literal_set(value)
    inventory = (finite_inventory(value) if isinstance(value, dict)
                 and value.get("ctor") == "finiteData" else None)
    if inventory is not None:
        keys = inventory_keys(inventory)
        return "finite", FiniteEnumeratedSet(keys), json.loads
    ctor, params = named_object(value)
    if ctor == "functorAction":
        edge, source = fields(value, "functorAction", 2)
        preserving_action(edge)
        return carrier(source)
    if ctor == "subobjectApex":
        receiver, = fields(value, ctor, 1)
        return carrier(arrow_record(receiver)[0])
    if ctor == "subobject":
        return carrier(arrow_record(value)[0])
    if ctor in {"arrow", "objectPresentation", "liftedSubobject"}:
        raise ValueError("an Arrow record needs its explicit object projection")
    if ctor == "valueData":
        if len(params) != 1:
            raise ValueError("valueData requires its data")
        return carrier(params[0])
    if ctor == "extent":
        if len(params) != 3 or not isinstance(params[2], list):
            raise ValueError("extent requires its power object, ambient set and literal members")
        return ("finite",) + literal_set(params[2])
    if ctor == "constructionApex":
        operation, source_diagram, complete = fields(value, ctor, 3)
        cone, _actual_diagram, _created = construction_data(operation, source_diagram, complete)
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
    if ctor in {"obj.sets.polynomials", "obj.rings.polynomials"} and len(params) == 1:
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
    if ctor in {"obj.sets.integers_mod", "obj.rings.integers_mod",
                "obj.commutative_rings.integers_mod"} and params == [0]:
        return "infinite", value, True  # ZMod 0 = ℤ
    if ctor not in PARENTS:
        raise UnsupportedCarrier("no Sage parent for %s" % ctor)
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


def callable_wrappers(value, source=None, target=None):
    """Unbox only explicit callable wrappers, preserving exact typed endpoints."""
    while isinstance(value, dict):
        if value.get("ctor") == "valueData":
            value, = fields(value, "valueData", 1)
        elif value.get("ctor") == "typedMap":
            actual_source, actual_target, value = typed_map(value)
            source = selected_endpoint(source, actual_source)
            target = selected_endpoint(target, actual_target)
        else:
            break
    return value, source, target


def unmapped_endpoint(value, edge):
    if value is None:
        return None
    if isinstance(value, dict) and value.get("ctor") == "functorAction":
        actual_edge, source = fields(value, "functorAction", 2)
        if actual_edge == edge:
            return source
    raise ValueError("a mapped callable needs its selected action on the endpoint")


def composition_context(value, source=None, target=None):
    first, second = fields(value, "compose", 2)
    a = callable_context(first, source)
    b = callable_context(second, a[2], target)
    a = callable_context(first, source, b[1])
    if a[2] is None or b[1] is None or a[2] != b[1]:
        raise ValueError("composition requires its complete shared intermediate endpoint")
    return a, b


def callable_context(value, source=None, target=None):
    """Read public projections/actions as data, keeping selected and actual endpoints."""
    value, source, target = callable_wrappers(value, source, target)
    if not isinstance(value, dict):
        return value, source, target
    ctor = value.get("ctor")
    if ctor == "constructionLeg":
        _leg, _a, _b, sources, targets = construction_leg(value)
        source = selected_endpoint(source, *sources)
        target = selected_endpoint(target, *targets)
    elif ctor in {"arrowHom", "subobjectInclusion"}:
        receiver, = fields(value, ctor, 1)
        a, b, _arrow = arrow_record(receiver)
        source = selected_endpoint(source, a, node("subobjectApex", receiver)
                                   if ctor == "subobjectInclusion" else a)
        target = selected_endpoint(target, b)
    elif ctor == "map":
        edge, arrow = fields(value, ctor, 2)
        preserving_action(edge)
        _data, a, b = callable_context(arrow, unmapped_endpoint(source, edge),
                                     unmapped_endpoint(target, edge))
        source = selected_endpoint(source, node("functorAction", edge, a) if a is not None else None)
        target = selected_endpoint(target, node("functorAction", edge, b) if b is not None else None)
    elif ctor == "compose":
        a, b = composition_context(value, source, target)
        source, target = a[1], b[2]
    elif ctor == "identity":
        a, b = fields(value, ctor, 2)
        if a != b:
            raise ValueError("an identity must retain equal complete endpoints")
        source, target = selected_endpoint(source, a), selected_endpoint(target, b)
    return value, source, target


def endpoint_inventory(value):
    """Use supplied object data or an existing native codec; never graph images."""
    if value is None:
        return None
    try:
        kind, S, encode = carrier(value)
    except UnsupportedCarrier:
        return None
    if kind != "finite":
        return None
    return set(inventory_keys([encode(point) for point in S]))


def checked_graph(table, source, target, explicit_inventory=False):
    domain = endpoint_inventory(source)
    if source is not None and domain is None and not explicit_inventory:
        raise ValueError("a typed graph needs a source inventory or complete finiteGraph data")
    if domain is not None and set(table) != domain:
        raise ValueError("the graph must cover its supplied complete source exactly once")
    codomain = endpoint_inventory(target)
    if codomain is not None and not set(table.values()).issubset(codomain):
        raise ValueError("the graph has an output outside its supplied target inventory")
    return table


def native_map(table, target):
    """Translate supplied finite inventories to Sage's native index morphisms."""
    codomain = endpoint_inventory(target)
    if codomain is None:
        raise ValueError("native finite map composition needs the complete target inventory")
    source_keys = FiniteEnumeratedSet(sorted(table))
    target_keys = FiniteEnumeratedSet(sorted(codomain))
    images = Family([ZZ(target_keys.rank(table[key])) for key in source_keys])
    native = SetMorphism(Hom(IntegerRange(0, len(source_keys)),
                            IntegerRange(0, len(target_keys))), images.__getitem__)
    return native, source_keys, target_keys


def graph(value, source=None, target=None):
    """Consume stored callables; native Sage maps perform finite composition."""
    value, source, target = callable_context(value, source, target)
    if isinstance(value, dict):
        ctor = value.get("ctor")
        if ctor == "constructionLeg":
            leg, actual_source, actual_target, _sources, _targets = construction_leg(value)
            return checked_graph(graph(leg, actual_source, actual_target), source, target, True)
        if ctor in {"arrowHom", "subobjectInclusion"}:
            receiver, = fields(value, ctor, 1)
            a, b, arrow = arrow_record(receiver)
            return checked_graph(graph(arrow, a, b), source, target, True)
        if ctor == "map":
            edge, arrow = fields(value, ctor, 2)
            table = graph(arrow, unmapped_endpoint(source, edge), unmapped_endpoint(target, edge))
            return checked_graph(table, source, target, True)
        if ctor == "compose":
            a, b = composition_context(value, source, target)
            first, second = graph(*a), graph(*b)
            f, source_keys, _middle = native_map(first, a[2])
            g, _middle, target_keys = native_map(second, b[2])
            composed = g * f
            table = {key: target_keys.unrank(composed(ZZ(source_keys.rank(key)))) for key in first}
            return checked_graph(table, source, target, True)
        if ctor == "identity":
            domain = endpoint_inventory(source)
            if domain is None:
                raise ValueError("finite identity data needs its supplied source inventory")
            keys = FiniteEnumeratedSet(sorted(domain))
            S = IntegerRange(0, len(keys))
            identity = Hom(S, S).identity()
            table = {key: keys.unrank(identity(ZZ(keys.rank(key)))) for key in keys}
            return checked_graph(table, source, target, True)
        if ctor == "opaqueData":
            token, = fields(value, ctor, 1)
            if token not in PROJECTIONS:
                raise ValueError("this connection owns no such projection callable")
            domain = endpoint_inventory(source)
            if domain is None:
                raise ValueError("a projection graph requires its actual finite source inventory")
            table = {}
            for key in sorted(domain):
                point = json.loads(key)
                if not isinstance(point, list) or len(point) != 2:
                    raise ValueError("a product point requires both component data")
                table[key] = json.dumps(Family(point)[PROJECTIONS[token]], sort_keys=True)
            return checked_graph(table, source, target, True)
        if ctor == "mor.sets.fin_rev":
            args = fields(value, ctor, 1)
            n = numeral(args[0])
            p = Permutation(list(range(n, 0, -1)))
            value = finite_graph(list(range(n)), [[i, int(p(i + 1)) - 1] for i in range(n)])
    explicit_inventory = isinstance(value, dict) and value.get("ctor") == "finiteGraph"
    value = graph_data(value)
    table = {}
    for pair in value:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("not a pair [x, f x]: %r" % (pair,))
        key = json.dumps(pair[0], sort_keys=True)
        if key in table:
            raise ValueError("the graph lists %s twice" % key)
        table[key] = json.dumps(pair[1], sort_keys=True)
    return checked_graph(table, source, target, explicit_inventory)


def op_pullback(value):
    first, second = (callable_context(m) for m in diagram(value, "cospan", 2))
    if first[2] is not None and second[2] is not None and first[2] != second[2]:
        raise ValueError("a cospan must retain its complete common target")
    common_target = first[2] if first[2] is not None else second[2]
    f, g = (graph(data, source, common_target) for data, source, _target in (first, second))
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
