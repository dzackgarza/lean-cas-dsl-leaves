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
from sage.version import version as SAGE_VERSION  # noqa: E402

from wire import decision, finite_cardinal, named_object  # noqa: E402


def field(value):
    ctor, args = named_object(value)
    moduli = {"obj.sets.f9_x": ("x", [1, 0, 1]),
              "obj.commutative_rings.f9_x": ("x", [1, 0, 1]),
              "obj.sets.f9_y": ("y", [2, 1, 1]),
              "obj.commutative_rings.f9_y": ("y", [2, 1, 1])}
    if ctor not in moduli or args:
        raise ValueError("expected a parameter-free released F9 presentation")
    name, coefficients = moduli[ctor]
    polynomials = PolynomialRing(GF(3), "t")
    return GF(9, name, modulus=polynomials(coefficients))


def op_cardinality(value):
    return finite_cardinal(field(value).cardinality())


def op_is_finite(value):
    return decision(bool(field(value).is_finite()))


if __name__ == "__main__":
    serve("sage", SAGE_VERSION, "0.1.0",
          {"meth.cardinality": op_cardinality, "prop.is_finite": op_is_finite})
