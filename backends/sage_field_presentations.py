"""Sage finite-field models for the released named polynomial presentations.

Input data comes from the public 57c858 PolynomialPresentations definitions:
the two selected moduli over ZMod 3 and their selected translation parameter.
Engine routines: PolynomialRing, GF with an explicit modulus, cardinality,
is_finite and field hom construction. No engine objects cross the port.
"""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_modules")

from cas_port import serve  # noqa: E402
from sage.rings.finite_rings.finite_field_constructor import GF  # noqa: E402
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing  # noqa: E402
from sage.rings.integer_ring import ZZ  # noqa: E402
from sage.rings.rational_field import QQ  # noqa: E402
from sage.rings.finite_rings.integer_mod_ring import Zmod  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import constructor, decision, finite_cardinal, named_object, numeral  # noqa: E402


def arithmetic(value, parent):
    ctor, args = named_object(value)
    if ctor == "numeral" and len(args) == 1:
        return parent(numeral(args[0]))
    if ctor == "generator" and (not args or args == [0]):
        return parent.gen()
    if ctor in {"add", "mul"} and len(args) == 2:
        left, right = (arithmetic(x, parent) for x in args)
        return left + right if ctor == "add" else left * right
    if ctor == "neg" and len(args) == 1:
        return -arithmetic(args[0], parent)
    raise ValueError("unsupported arithmetic data for the selected field presentation")


def selected_element(value, descriptor, parent):
    if isinstance(value, dict) and value.get("ctor") == "generator":
        object_id, parameters = constructor(value, "generator", 2)
        selected_id, selected_parameters = named_object(descriptor)
        underlying = {"obj.commutative_rings.f9_x": "obj.sets.f9_x",
                      "obj.commutative_rings.f9_y": "obj.sets.f9_y",
                      "obj.commutative_rings.polynomial_quotient": "obj.sets.polynomial_quotient"}
        expected = underlying.get(selected_id, selected_id)
        if object_id != expected or parameters != selected_parameters:
            raise ValueError("generator arrow changes its declared object or parameters")
        return parent.gen()
    selected, expression = constructor(value, "element", 2)
    if selected != descriptor:
        raise ValueError("element changes the exact selected endpoint descriptor")
    return arithmetic(expression, parent)


def base_ring(descriptor):
    ctor, args = named_object(descriptor)
    if ctor in {"obj.commutative_rings.integers", "obj.rings.integers"} and not args:
        return ZZ
    if ctor in {"obj.commutative_rings.rationals", "obj.rings.rationals"} and not args:
        return QQ
    if ctor in {"obj.commutative_rings.integers_mod", "obj.rings.integers_mod"}:
        n, = args
        return Zmod(numeral(n))
    raise ValueError("no Sage coefficient-ring translation for %s" % ctor)


def defining_polynomial(value, descriptor, ring):
    selected = {"ctor": "obj.sets.polynomials", "args": [descriptor]}
    return selected_element(value, selected, ring)


def field(value):
    ctor, args = named_object(value)
    moduli = {"obj.sets.f9_x": ("x", [1, 0, 1]),
              "obj.commutative_rings.f9_x": ("x", [1, 0, 1]),
              "obj.sets.f9_y": ("y", [2, 1, 1]),
              "obj.commutative_rings.f9_y": ("y", [2, 1, 1])}
    if ctor in {"obj.commutative_rings.polynomial_quotient", "obj.sets.polynomial_quotient"}:
        coefficient_ring, polynomial = args
        ring = PolynomialRing(base_ring(coefficient_ring), "t")
        return ring.quotient(defining_polynomial(polynomial, coefficient_ring, ring), "a")
    if ctor not in moduli or args:
        raise ValueError("expected a parameter-free released F9 presentation")
    name, coefficients = moduli[ctor]
    polynomials = PolynomialRing(GF(3), "t")
    return GF(9, name, modulus=polynomials(coefficients))


def integer_data(n):
    n = int(n)
    literal = {"ctor": "numeral", "args": [abs(n)]}
    return literal if n >= 0 else {"ctor": "neg", "args": [literal]}


def arithmetic_data(value):
    # Sage supplies the generator-relative polynomial coordinates. This loop
    # serializes those coordinates into the declared arithmetic grammar.
    polynomial = value.polynomial() if hasattr(value, "polynomial") else value.lift()
    terms = []
    for exponent, coefficient in enumerate(polynomial.list()):
        c = int(coefficient)
        if coefficient != c:
            raise ValueError("coefficient is not expressible in the released numeral grammar")
        if not c:
            continue
        term = integer_data(c)
        for _ in range(exponent):
            term = {"ctor": "mul", "args": [term, {"ctor": "generator", "args": []}]}
        terms.append(term)
    if not terms:
        return integer_data(0)
    result = terms[0]
    for term in terms[1:]:
        result = {"ctor": "add", "args": [result, term]}
    return result


def presentation_apply(value, comparison):
    parameters, inverse, source, target, point = constructor(value, "presentationApply", 5)
    if not isinstance(inverse, bool):
        raise ValueError("presentation direction must be a JSON boolean")
    if comparison == "cmp.f9.translation":
        if parameters:
            raise ValueError("the selected F9 comparison has no parameters")
        expected_source = "obj.commutative_rings.f9_y" if inverse else "obj.commutative_rings.f9_x"
        expected_target = "obj.commutative_rings.f9_x" if inverse else "obj.commutative_rings.f9_y"
        if source != {"ctor": expected_source, "args": []} or target != {"ctor": expected_target, "args": []}:
            raise ValueError("F9 comparison changes its selected endpoints")
        shift = 2
    else:
        if len(parameters) != 3:
            raise ValueError("polynomial translation retains coefficient ring, polynomial and scalar")
        ring_descriptor, polynomial, scalar = parameters
        coefficients = base_ring(ring_descriptor)
        shift = (selected_element(scalar, ring_descriptor, coefficients)
                 if isinstance(scalar, dict) else coefficients(scalar))
        # The complete selected endpoint descriptors provide both chosen
        # polynomial presentations; the comparison retains the original f,c.
        original = target if inverse else source
        if original != {"ctor": "obj.commutative_rings.polynomial_quotient",
                        "args": [ring_descriptor, polynomial]}:
            raise ValueError("polynomial comparison changes its selected source parameters")
    domain, codomain = field(source), field(target)
    image = codomain.gen() - shift if inverse else codomain.gen() + shift
    hom = domain.hom([image], codomain)
    result = hom(selected_element(point, source, domain))
    return {"ctor": "element", "args": [target, arithmetic_data(result)]}


def op_cardinality(value):
    return finite_cardinal(field(value).cardinality())


def op_is_finite(value):
    return decision(bool(field(value).is_finite()))


if __name__ == "__main__":
    serve("sage", SAGE_VERSION, "0.1.0",
          {"meth.cardinality": op_cardinality, "prop.is_finite": op_is_finite,
           "cmp.f9.translation": lambda value: presentation_apply(value, "cmp.f9.translation"),
           "cmp.polynomial_quotient.translation": lambda value: presentation_apply(
               value, "cmp.polynomial_quotient.translation")})
