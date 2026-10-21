"""Sage realizations of named maps of `Sets` on number systems and polynomials, and the
real-analysis binders.

Engine: full Sage (`sage.all`), run under `$CAS_SAGE_PYTHON` (`engine_python`). These routes
need Sage's symbolic ring, `QQbar`/`AA` and PARI/FLINT factorization, which the modular
passagemath installation lacks. Each operation names the Sage routine it calls:

* `mor.sets.complex_re|im|bar|abs`: `real_part`, `imag_part`, `conjugate`, `abs` on `SR`;
* `mor.sets.real_sqrt`: `sqrt` on `SR`;
* `mor.sets.polynomial_degree|derivative`: `Polynomial.degree`, `Polynomial.derivative`;
* `mor.sets.polynomial_differential`: `Polynomial.derivative`, answered as `p' dx` through the
  published `mor.sets.kaehler_from_coordinate`;
* `mor.sets.polynomial_map`: `Polynomial.change_ring` along the named coefficient arrow;
* `mor.sets.polynomial_factors`: `Polynomial.factor` (over `AA`/`QQbar` for `ℝ`/`ℂ`);
* `mor.sets.polynomial_roots`: `Polynomial.roots` (over `AA`/`QQbar` for `ℝ`/`ℂ`), algebraic
  roots by `radical_expression`;
* `mor.sets.companion_matrix`: `sage.matrix.special.companion_matrix` (format `right`);
* `mor.sets.mv_total_degree`: `MPolynomial.total_degree`;
* `mor.sets.nat_prime_factors`: `Integer.prime_divisors`;
* `mor.sets.equality`: Sage `==` in the decoded parent (`bool` of the symbolic relation);
* `bind.sets.integral`, `bind.sets.limit`, `bind.sets.limit_at_infinity`: `integrate` and
  `limit` on the symbolic integrand.

Wire (`CasContract/Port.lean`): points arrive in the common `apply` envelope, as `element`
arithmetic data (`numeral`, `generator`, `add`, `mul`, `neg`, `operationExpression`, `point`),
possibly inside `valueData`, `admittedPoint` or `pointView`. Answers are `valueData` of the
target's encoding: `element` arithmetic at the exact target descriptor for ring points, JSON
numbers for natural numbers, JSON lists for finite subsets, and nested graphs for matrices.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

from __future__ import annotations

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all",))

from cas_port import point_invocation, serve, value_data  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import finite_graph, graph_data, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"

ZZ, QQ, AA, QQbar, SR = engine.ZZ, engine.QQ, engine.AA, engine.QQbar, engine.SR
Integer, Infinity, I, pi, e = engine.Integer, engine.Infinity, engine.I, engine.pi, engine.e
PolynomialRing, Zmod = engine.PolynomialRing, engine.Zmod
operator = __import__("operator")

CLOSED_DOMAINS = ({"ctor": "obj.sets.fin", "args": [1]},
                  {"ctor": "obj.sets.terminal", "args": []})

# --- descriptors -------------------------------------------------------------------------

NUMBER_SYSTEMS = {"integers": ZZ, "rationals": QQ, "reals": SR, "complexes": SR,
                  "naturals": ZZ, "positive_naturals": ZZ}
CATEGORY_PREFIXES = ("obj.sets.", "obj.rings.", "obj.commutative_rings.", "obj.fields.",
                     "obj.semirings.", "obj.linear_orders.")


def strip(value):
    """The selected descriptor beneath retained structural framing."""
    ctor, args = named_object(value)
    if ctor in {"functorAction", "objectPresentation"} and len(args) == 2:
        return strip(args[1])
    if ctor in {"finiteData", "valueData", "subobject"} and args:
        return strip(args[0])
    return value


def system(value):
    """The number system a descriptor names (`integers`, ..., `complexes`), or None."""
    ctor, _ = named_object(strip(value))
    for prefix in CATEGORY_PREFIXES:
        if ctor.startswith(prefix) and ctor[len(prefix):] in NUMBER_SYSTEMS:
            return ctor[len(prefix):]
    return None


def coefficient_ring(value):
    """Sage's exact parent for a coefficient ring descriptor."""
    ctor, args = named_object(strip(value))
    kind = system(value)
    if kind in {"integers", "naturals"}:
        return ZZ
    if kind == "rationals":
        return QQ
    if kind == "reals":
        return AA
    if kind == "complexes":
        return QQbar
    if ctor.endswith(".integers_mod") and len(args) == 1:
        n = numeral(args[0])
        return ZZ if n == 0 else Zmod(n)
    raise ValueError("no Sage coefficient ring for the descriptor %s" % ctor)


def parent(value):
    """Sage's parent for the points of a set descriptor."""
    ctor, args = named_object(strip(value))
    if ctor in {"obj.sets.polynomials", "obj.sets.nonzero_polynomials"} and len(args) == 1:
        return PolynomialRing(coefficient_ring(args[0]), "x")
    if ctor == "obj.sets.monics" and len(args) == 2:
        return PolynomialRing(coefficient_ring(args[1]), "x")
    if ctor == "obj.sets.mv_polynomials" and len(args) == 2:
        n = numeral(args[0])
        return PolynomialRing(coefficient_ring(args[1]), "x", n)
    kind = system(value)
    if kind is not None:
        return NUMBER_SYSTEMS[kind]
    if ctor.endswith(".integers_mod") and len(args) == 1:
        return coefficient_ring(value)
    raise ValueError("no Sage parent for the descriptor %s" % ctor)


def ring_descriptor(value):
    """The `cat.rings` descriptor of the ring whose points a set descriptor carries."""
    ctor, args = named_object(strip(value))
    for prefix in CATEGORY_PREFIXES:
        if ctor.startswith(prefix):
            return {"ctor": "obj.rings." + ctor[len(prefix):], "args": args}
    raise ValueError("no ring descriptor for %s" % ctor)


# --- decoding points and maps --------------------------------------------------------------

def point(value, P):
    """A closed point's Sage value in the parent `P`."""
    if isinstance(value, bool):
        raise ValueError("a truth value is not a point of %s" % P)
    if isinstance(value, int):
        return P(value)
    if isinstance(value, list):
        if P is QQ and len(value) == 2 and all(isinstance(v, int) for v in value):
            return QQ(value[0]) / QQ(value[1])  # the record encoding of `Rat`: [num, den]
        raise ValueError("a list is not a closed point of %s: %r" % (P, value))
    ctor, args = named_object(value)
    if ctor == "valueData" and len(args) == 1:
        return point(args[0], P)
    if ctor == "element" and len(args) == 2:
        return arithmetic(args[1], parent(args[0]) if P is None else P)
    if ctor == "admittedPoint" and len(args) == 6:
        return point(args[5], P)
    if ctor == "pointView" and len(args) == 3:
        return point(args[1], P)
    if ctor == "point" and len(args) == 1:
        return closed(args[0], P)
    return closed(value, P)


def arithmetic(value, P):
    """Element arithmetic data (`CasContract/Port.lean`) evaluated by Sage in `P`."""
    if isinstance(value, int) and not isinstance(value, bool):
        return P(value)
    ctor, args = named_object(value)
    if ctor == "numeral" and len(args) == 1:
        return P(numeral(args[0]))
    if ctor == "generator" and not args:
        return P.gen()
    if ctor == "generator" and len(args) == 1:
        return P.gen(numeral(args[0]))
    if ctor == "neg" and len(args) == 1:
        return -arithmetic(args[0], P)
    if ctor in {"add", "mul"} and len(args) == 2:
        left, right = (arithmetic(a, P) for a in args)
        return left + right if ctor == "add" else left * right
    if ctor == "point" and len(args) == 1:
        return closed(args[0], P)
    if ctor == "operationExpression" and len(args) == 3:
        operation, parameters, operands = args
        values = [arithmetic(a, P) for a in operands]
        kind = operation.rsplit(".", 1)[-1]
        if operation.startswith(("op.rings.", "op.semirings.")):
            if kind == "add" and len(values) == 2:
                return values[0] + values[1]
            if kind == "mul" and len(values) == 2:
                return values[0] * values[1]
            if kind == "neg" and len(values) == 1:
                return -values[0]
            if kind == "pow" and len(values) == 1:
                return values[0] ** numeral(parameters[-1])
        if operation == "mor.sets.divide" and len(values) == 2:
            return values[0] / values[1]
        if operation.startswith("mor.sets.") and len(values) == 1:
            return P(apply_map({"ctor": operation, "args": parameters}, values[0]))
        raise ValueError("no Sage lowering for the operation %s" % operation)
    if ctor in {"element", "valueData", "admittedPoint", "pointView"}:
        return point(value, P)
    raise ValueError("no Sage lowering for the arithmetic datum %s" % ctor)


def closed(arrow, P):
    """A closed point `1 → X` given by its morphism encoding."""
    if isinstance(arrow, list):
        if len(arrow) == 2:  # a mediator of two closed points is the pair of their data
            return (point(arrow[0], None), point(arrow[1], None))
        raise ValueError("a closed point is not the list %r" % (arrow,))
    ctor, args = named_object(arrow)
    if ctor in {"element", "valueData", "admittedPoint", "pointView"}:
        return point(arrow, P)
    if ctor == "mor.sets.complex_i" and not args:
        return lift(P, I)
    if ctor == "mor.sets.real_pi" and not args:
        return lift(P, pi)
    if ctor == "mor.sets.infinity" and not args:
        return +Infinity
    if ctor == "mor.sets.neg_infinity" and not args:
        return -Infinity
    if ctor == "generator" and len(args) == 2:
        return parent({"ctor": args[0], "args": args[1]}).gen()
    if ctor == "compose" and len(args) == 2:
        return lift(P, apply_map(args[1], closed(args[0], None)))
    if ctor == "mediator" and len(args) == 2:
        return (closed(args[0], None), closed(args[1], None))
    raise ValueError("no Sage lowering for the closed point %s" % ctor)


def lift(P, x):
    return x if P is None else P(x)


MAPS = {
    "mor.sets.real_sqrt": lambda x: engine.sqrt(SR(x)),
    "mor.sets.real_sin": lambda x: engine.sin(SR(x)),
    "mor.sets.real_cos": lambda x: engine.cos(SR(x)),
    "mor.sets.real_exp": lambda x: engine.exp(SR(x)),
    "mor.sets.complex_re": lambda x: SR(x).real_part(),
    "mor.sets.complex_im": lambda x: SR(x).imag_part(),
    "mor.sets.complex_bar": lambda x: SR(x).conjugate(),
    "mor.sets.complex_abs": lambda x: SR(x).abs(),
}


def apply_map(arrow, x):
    """Apply a map of `Sets`, given by its morphism encoding, to a Sage value."""
    ctor, args = named_object(arrow)
    if ctor in MAPS:
        return MAPS[ctor](x)
    if ctor == "identity" and len(args) == 2:
        return x
    if ctor == "typedMap" and len(args) == 3:
        return apply_map(args[2], x)
    if ctor == "compose" and len(args) == 2:
        return apply_map(args[1], apply_map(args[0], x))
    if ctor == "mediator" and len(args) == 2:
        return (apply_map(args[0], x), apply_map(args[1], x))
    if ctor in {"objectField", "incl.sets.naturals_integers", "incl.sets.integers_rationals",
                "incl.sets.rationals_reals", "incl.sets.reals_complexes"}:
        return x  # inclusions and constants: Sage's coercion carries the value unchanged
    if ctor in {"mor.sets.terminal", "terminal"}:
        return Integer(0)
    if ctor == "operationExpression" and len(args) == 3:
        # A pointwise operation of maps: its operands are maps out of the same domain.
        operation, parameters, operands = args
        values = [apply_map(a, x) if is_map(a) else arithmetic(a, SR) for a in operands]
        kind = operation.rsplit(".", 1)[-1]
        if kind == "add" and len(values) == 2:
            return values[0] + values[1]
        if kind == "mul" and len(values) == 2:
            return values[0] * values[1]
        if kind == "neg" and len(values) == 1:
            return -values[0]
        if kind == "pow" and len(values) == 1:
            return values[0] ** numeral(parameters[-1])
        if operation == "mor.sets.divide" and len(values) == 2:
            return values[0] / values[1]
        raise ValueError("no pointwise Sage lowering for the operation %s" % operation)
    if ctor in {"element", "point", "valueData"}:
        return point(arrow, SR)  # a constant map
    if ctor in {"add", "mul", "neg", "numeral"}:
        return arithmetic(arrow, SR)
    raise ValueError("no Sage lowering for the map %s" % ctor)


def is_map(value):
    if not isinstance(value, dict):
        return False
    ctor = value.get("ctor")
    return ctor in MAPS or ctor in {"identity", "typedMap", "compose", "mediator", "objectField",
                                    "operationExpression", "terminal", "mor.sets.terminal"}


def function_of(value, t):
    """A map `ℝ → ℝ` (an admitted or retained callable) as a symbolic expression in `t`."""
    ctor, args = named_object(value)
    if ctor == "admittedPoint" and len(args) == 6:
        return function_of(args[5], t)
    if ctor in {"valueData", "point"} and len(args) == 1:
        return function_of(args[0], t)
    if ctor == "opaqueData":
        raise ValueError("this backend owns no callable behind a foreign opaque token")
    return SR(apply_map(value, t))


# --- encoding answers ----------------------------------------------------------------------

def numeral_data(n):
    n = Integer(n)
    datum = {"ctor": "numeral", "args": [int(abs(n))]}
    return datum if n >= 0 else {"ctor": "neg", "args": [datum]}


def symbolic_data(x, target):
    """A Sage value as element arithmetic data at the target descriptor."""
    if x in QQ:
        q = QQ(x)
        if q.denominator() == 1:
            return numeral_data(q)
        return {"ctor": "operationExpression", "args": [
            "mor.sets.divide", [monoid_descriptor(target)],
            [numeral_data(q.numerator()), numeral_data(q.denominator())]]}
    x = SR(x)
    op = x.operator()
    kind = getattr(op, "__name__", "")
    if op is None and x.is_numeric() and x.imag_part() != 0:
        # A Gaussian numeric constant, Sage's atom `a + b*I`: split as re + im·i.
        real, imaginary = x.real_part(), x.imag_part()
        unit = {"ctor": "point", "args": [{"ctor": "mor.sets.complex_i", "args": []}]}
        imaginary_part = unit if imaginary == 1 else {
            "ctor": "mul", "args": [symbolic_data(imaginary, target), unit]}
        return imaginary_part if real == 0 else {
            "ctor": "add", "args": [symbolic_data(real, target), imaginary_part]}
    if op is operator.add or kind == "add_vararg":
        terms = [symbolic_data(t, target) for t in x.operands()]
        out = terms[0]
        for term in terms[1:]:
            out = {"ctor": "add", "args": [out, term]}
        return out
    if op is operator.mul or kind == "mul_vararg":
        factors = list(x.operands())
        negative = False
        rest = []
        for f in factors:
            if f == -1:
                negative = not negative
            else:
                rest.append(symbolic_data(f, target))
        out = rest[0]
        for f in rest[1:]:
            out = {"ctor": "mul", "args": [out, f]}
        return {"ctor": "neg", "args": [out]} if negative else out
    if op is operator.pow:
        base, exponent = x.operands()
        if exponent in ZZ and exponent > 0:
            return {"ctor": "operationExpression", "args": [
                "op.rings.pow", [ring_descriptor(target), int(exponent)],
                [symbolic_data(base, target)]]}
        if exponent == QQ(1) / 2:
            return closed_through(base, "mor.sets.real_sqrt", target)
        if exponent in ZZ and exponent < 0:
            return {"ctor": "operationExpression", "args": [
                "mor.sets.divide", [monoid_descriptor(target)],
                [numeral_data(1), symbolic_data(base ** (-exponent), target)]]}
        raise ValueError("no declared encoding of the power %s" % x)
    if x == I:
        return {"ctor": "point", "args": [{"ctor": "mor.sets.complex_i", "args": []}]}
    if x == pi:
        return {"ctor": "point", "args": [{"ctor": "mor.sets.real_pi", "args": []}]}
    if x == e:
        return closed_through(SR(1), "mor.sets.real_exp", target)
    name = getattr(op, "name", lambda: None)()
    named = {"sin": "mor.sets.real_sin", "cos": "mor.sets.real_cos", "exp": "mor.sets.real_exp",
             "sqrt": "mor.sets.real_sqrt"}
    if name in named:
        return closed_through(x.operands()[0], named[name], target)
    raise ValueError("no declared element encoding of the Sage value %s" % x)


def closed_through(argument, arrow, target):
    """The point `1 → ℝ → X` given by a real argument and a named real map."""
    reals = {"ctor": "obj.sets.reals", "args": []}
    composite = {"ctor": "compose", "args": [
        {"ctor": "element", "args": [reals, symbolic_data(argument, reals)]},
        {"ctor": arrow, "args": []}]}
    if system(target) == "complexes":
        composite = {"ctor": "compose", "args": [
            composite, {"ctor": "incl.sets.reals_complexes", "args": []}]}
    return {"ctor": "point", "args": [composite]}


def monoid_descriptor(target):
    return {"ctor": "functorAction", "args": [
        {"ctor": "fun.rings.multiplicative_monoid", "args": []}, ring_descriptor(target)]}


def element(x, target):
    return {"ctor": "element", "args": [target, symbolic_data(x, target)]}


def polynomial_data(p, target):
    """A Sage polynomial as element arithmetic in the generator of the target."""
    ring = ring_descriptor(target)
    coefficient_target = named_object(strip(target))[1][-1]
    if p.parent().ngens() != 1:
        raise ValueError("multivariate answers are not produced by this backend")
    terms = [monomial(c, k, ring, coefficient_target) for k, c in sorted(p.dict().items())]
    if not terms:
        return numeral_data(0)
    out = terms[0]
    for term in terms[1:]:
        out = {"ctor": "add", "args": [out, term]}
    return out


def coefficient_data(c, coefficient_target):
    """A coefficient as element arithmetic: residues by their representative in `0..n-1`,
    algebraic numbers by Sage's `radical_expression`."""
    if c.parent() in (AA, QQbar):
        return symbolic_data(c.radical_expression(), coefficient_target)
    if c.parent() not in (ZZ, QQ) and hasattr(c, "lift"):
        return numeral_data(int(c.lift()))
    return symbolic_data(QQ(c), coefficient_target)


def monomial(c, k, ring, coefficient_target):
    power = ({"ctor": "generator", "args": []} if k == 1 else
             {"ctor": "operationExpression", "args": [
                 "op.rings.pow", [ring, int(k)], [{"ctor": "generator", "args": []}]]})
    coefficient = coefficient_data(c, coefficient_target)
    if k == 0:
        return coefficient
    if c == 1:
        return power
    return {"ctor": "mul", "args": [coefficient, power]}


def polynomial_element(p, target):
    return {"ctor": "element", "args": [target, polynomial_data(p, target)]}


# --- the invocation envelope --------------------------------------------------------------

def invoke(operation, value, compute, multiple=False):
    """Run `compute(parameters, source, target, x)` on a closed or generalized point."""
    ctor, _ = named_object(value)
    if ctor != "apply":
        raise ValueError("%s requires the common apply envelope" % operation)
    _, parameters, arrow, domain, source, target, data = point_invocation(value, operation)
    payload = data
    while isinstance(payload, dict) and payload.get("ctor") == "valueData":
        payload = payload["args"][0]
    if isinstance(payload, dict) and payload.get("ctor") in {"finiteGraph", "typedMap"} or (
            isinstance(payload, list) and domain not in CLOSED_DOMAINS and not multiple):
        rows = graph_data(payload)
        return value_data(finite_graph([x for x, _ in rows],
                                       [[x, compute(parameters, source, target, y)]
                                        for x, y in rows]))
    if domain not in CLOSED_DOMAINS:
        raise ValueError("a non-closed invocation requires its actual pointwise data")
    return value_data(compute(parameters, source, target, data))


def scalar(operation):
    def compute(parameters, source, target, data):
        return element(MAPS[operation](point(data, SR)), target)
    return lambda value: invoke(operation, value, compute)


def polynomial(data, source):
    return parent(source)(point(data, parent(source)))


def degree(parameters, source, target, data):
    d = polynomial(data, source).degree()
    return {"ctor": "none", "args": []} if d < 0 else {"ctor": "some", "args": [int(d)]}


def derivative(parameters, source, target, data):
    return polynomial_element(polynomial(data, source).derivative(), target)


def differential(parameters, source, target, data):
    polynomials = {"ctor": "obj.sets.polynomials", "args": list(parameters)}
    coordinate = polynomial_element(polynomial(data, source).derivative(), polynomials)
    return {"ctor": "point", "args": [{"ctor": "compose", "args": [
        coordinate, {"ctor": "mor.sets.kaehler_from_coordinate", "args": list(parameters)}]}]}


COEFFICIENT_ARROWS = {"mor.commutative_rings.integer_coefficients",
                      "mor.commutative_rings.rational_real_coefficients",
                      "mor.commutative_rings.rational_complex_coefficients",
                      "mor.commutative_rings.real_complex_coefficients",
                      "mor.rings.identity", "identity"}


def change_ring(parameters, source, target, data):
    if len(parameters) != 3:
        raise ValueError("map requires its rings and coefficient arrow")
    arrow, _ = named_object(parameters[2])
    if arrow not in COEFFICIENT_ARROWS:
        raise ValueError("no Sage coefficient map for the arrow %s" % arrow)
    p = polynomial(data, source)
    return polynomial_element(p.change_ring(coefficient_ring(parameters[1])), target)


def nonzero(data, source):
    p = polynomial(data, source)
    if p == 0:
        raise ValueError("the zero polynomial is not in the nonzero polynomials")
    return p


def factors(parameters, source, target, data):
    p = nonzero(data, source)
    polynomials = {"ctor": "obj.sets.polynomials", "args": list(parameters[:1])}
    return [polynomial_element(f, polynomials) for f, _ in p.factor()]


def roots(parameters, source, target, data):
    p = nonzero(data, source)
    return [element(r.radical_expression() if r.parent() in (AA, QQbar) else r, parameters[0])
            for r in p.roots(multiplicities=False)]


def companion(parameters, source, target, data):
    n = numeral(parameters[0])
    p = polynomial(data, source)
    if not p.is_monic() or p.degree() != n:
        raise ValueError("the companion matrix requires a monic polynomial of degree %d" % n)
    C = engine.companion_matrix(p, format="right")
    K = parameters[1]
    return finite_graph(list(range(n)),
                        [[i, finite_graph(list(range(n)),
                                          [[j, element_ring(C[i, j], K)] for j in range(n)])]
                         for i in range(n)])


def element_ring(c, K):
    return {"ctor": "element", "args": [K, coefficient_data(c, K)]}


def total_degree(parameters, source, target, data):
    d = parent(source)(point(data, parent(source))).total_degree()
    return max(int(d), 0)  # Sage's -1 for 0 is the empty supremum, 0 in ℕ


def prime_factors(parameters, source, target, data):
    n = Integer(point(data, ZZ))
    if n <= 0:
        raise ValueError("prime factors are defined on positive naturals, not %s" % n)
    return [int(p) for p in n.prime_divisors()]


def equality(value):
    ctor, _ = named_object(value)
    if ctor != "apply":
        raise ValueError("equality requires the common apply envelope")
    _, parameters, arrow, domain, source, target, data = point_invocation(value, "mor.sets.equality")
    if domain not in CLOSED_DOMAINS:
        raise ValueError("a non-closed equality invocation requires its pointwise data")
    ctor, args = named_object(source)
    if ctor != "objectProduct" or len(args) != 2 or args[0] != args[1]:
        raise ValueError("equality requires the product of one set with itself")
    while isinstance(data, dict) and data.get("ctor") == "valueData":
        data = data["args"][0]
    if not isinstance(data, list) or len(data) != 2:
        raise ValueError("equality requires the ordered pair of its two points")
    P = parent(args[0])
    x, y = (point(d, P) for d in data)
    return value_data(bool(x == y))


def vector(value, K, n):
    """A point of `Fin n → K`: its finite graph (plain or `finiteGraph`) or its entry list."""
    while isinstance(value, dict) and value.get("ctor") == "valueData":
        value = value["args"][0]
    pairs = isinstance(value, list) and all(isinstance(r, list) and len(r) == 2 for r in value)
    if pairs or isinstance(value, dict):
        rows = {numeral(i): y for i, y in graph_data(value)}
        if sorted(rows) != list(range(n)):
            raise ValueError("a vector of Fin %d needs exactly its %d entries" % (n, n))
        return [point(rows[i], K) for i in range(n)]
    if isinstance(value, list) and len(value) == n:
        return [point(y, K) for y in value]
    raise ValueError("no vector of length %d in %r" % (n, value))


def span(parameters, source, target, data):
    """`Submodule.span` by Sage `VectorSpace.span`, answered as the image of the matrix whose
    columns are an echelon basis of the span (`powerObjectMap` `image`)."""
    if len(parameters) != 2:
        raise ValueError("span requires its field and length")
    Kd, n = parameters[0], numeral(parameters[1])
    K = coefficient_ring(Kd)
    while isinstance(data, dict) and data.get("ctor") in {"valueData", "point"}:
        data = data["args"][0]
    ctor, args = named_object(data)
    if ctor != "extent" or len(args) != 3 or not isinstance(args[2], list):
        raise ValueError("span requires a finite subset given by its extent literal")
    vectors = [vector(v, K, n) for v in args[2]]
    basis = (K ** n).span(vectors).basis()
    columns = [list(b) for b in basis] + [[K(0)] * n] * (n - len(basis))
    matrix = finite_graph(list(range(n)), [
        [i, finite_graph(list(range(n)), [[j, element_ring(columns[j][i], Kd)] for j in range(n)])]
        for i in range(n)])
    vectors_object = {"ctor": "obj.sets.vectors", "args": [Kd, n]}
    constant = {"ctor": "compose", "args": [
        {"ctor": "mor.sets.terminal", "args": [vectors_object]}, [[0, matrix]]]}
    f = {"ctor": "compose", "args": [
        {"ctor": "mediator", "args": [constant, {"ctor": "identity",
                                                 "args": [vectors_object, vectors_object]}]},
        {"ctor": "obj.sets.matrices#application", "args": [n, Kd]}]}
    return {"ctor": "powerObjectMap", "args": ["pow.sets", "image",
                                              [vectors_object, vectors_object, f]]}


# --- binders --------------------------------------------------------------------------------

def binder(operation, compute):
    def run(value):
        ctor, args = named_object(value)
        if ctor == "apply":
            _, parameters, _, domain, _, target, data = point_invocation(value, operation)
            if domain not in CLOSED_DOMAINS:
                raise ValueError("a non-closed binder invocation requires its pointwise data")
        elif ctor == operation and len(args) >= 1:
            parameters, data = args[:-1], args[-1]
            target = {"ctor": "obj.sets.reals", "args": []}
        else:
            raise ValueError("%s requires its bounds and its map" % operation)
        t = SR.var("t")
        return value_data(element(compute(parameters, function_of(data, t), t), target))
    return run


def integral(parameters, f, t):
    if len(parameters) != 2:
        raise ValueError("the integral requires both bounds")
    a, b = (point(p, SR) for p in parameters)
    return engine.integrate(f, t, a, b)


def real_limit(parameters, f, t):
    if len(parameters) != 1:
        raise ValueError("the limit requires its point")
    return engine.limit(f, t=point(parameters[0], SR))


def infinite_limit(parameters, f, t):
    if len(parameters) != 1:
        raise ValueError("the limit at infinity requires its infinity")
    a = point(parameters[0], None)
    if a not in (+Infinity, -Infinity):
        raise ValueError("the limit at infinity requires ∞ or -∞")
    return engine.limit(f, t=engine.oo if a == +Infinity else -engine.oo)


serve("sage", SAGE_VERSION, ADAPTER_VERSION, {
    "mor.sets.complex_re": scalar("mor.sets.complex_re"),
    "mor.sets.complex_im": scalar("mor.sets.complex_im"),
    "mor.sets.complex_bar": scalar("mor.sets.complex_bar"),
    "mor.sets.complex_abs": scalar("mor.sets.complex_abs"),
    "mor.sets.real_sqrt": scalar("mor.sets.real_sqrt"),
    "mor.sets.polynomial_degree": lambda v: invoke("mor.sets.polynomial_degree", v, degree),
    "mor.sets.polynomial_derivative": lambda v: invoke("mor.sets.polynomial_derivative", v,
                                                       derivative),
    "mor.sets.polynomial_differential": lambda v: invoke("mor.sets.polynomial_differential", v,
                                                         differential),
    "mor.sets.polynomial_map": lambda v: invoke("mor.sets.polynomial_map", v, change_ring),
    "mor.sets.polynomial_factors": lambda v: invoke("mor.sets.polynomial_factors", v, factors),
    "mor.sets.polynomial_roots": lambda v: invoke("mor.sets.polynomial_roots", v, roots),
    "mor.sets.companion_matrix": lambda v: invoke("mor.sets.companion_matrix", v, companion),
    "mor.sets.mv_total_degree": lambda v: invoke("mor.sets.mv_total_degree", v, total_degree),
    "mor.sets.nat_prime_factors": lambda v: invoke("mor.sets.nat_prime_factors", v,
                                                   prime_factors),
    "mor.sets.equality": equality,
    "mor.sets.span": lambda v: invoke("mor.sets.span", v, span, multiple=True),
    "bind.sets.integral": binder("bind.sets.integral", integral),
    "bind.sets.limit": binder("bind.sets.limit", real_limit),
    "bind.sets.limit_at_infinity": binder("bind.sets.limit_at_infinity", infinite_limit),
})
