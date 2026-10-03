"""Thin Sage adapters for released polynomial point operations.

Native objects stay on this live port. Tokens are computational storage, never
mathematical identities. Formal signatures, arrows and composition are caller-owned.
"""

from engine_python import require_engine
require_engine("CAS_SAGE_PYTHON", "sage.all__sagemath_modules")

from cas_port import opaque_data, point_invocation, serve, value_data
from sage.matrix.constructor import companion_matrix
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.version import version as SAGE_VERSION
from sage_field_presentations import arithmetic, base_ring
from wire import constructor, named_object, numeral


POLYNOMIAL_FORMS = {"obj.sets.polynomials", "obj.rings.polynomials",
                    "obj.sets.nonzero_polynomials"}
FACTORIZATION_FORM = "obj.sets.polynomial_factorization_data"
MULTISET_FORM = "obj.sets.polynomial_factor_multisets"
OPERATIONS = {
    "mor.sets.polynomial_degree": ["obj.sets.polynomials"],
    "mor.sets.polynomial_factors": ["obj.sets.nonzero_polynomials"],
    "mor.sets.polynomial_factorization": ["obj.sets.nonzero_polynomials"],
    "mor.sets.polynomial_roots": ["obj.sets.nonzero_polynomials"],
    "mor.sets.polynomial_factorization_unit": [FACTORIZATION_FORM],
    "mor.sets.polynomial_factorization_factors": [FACTORIZATION_FORM],
    "mor.sets.polynomial_factorization_product": [FACTORIZATION_FORM],
    "mor.sets.polynomial_factorization_map": [FACTORIZATION_FORM],
    "mor.sets.polynomial_map": ["obj.sets.polynomials"],
    "mor.sets.companion_matrix": ["obj.sets.monics"],
    "mor.sets.matrix_charpoly": ["obj.sets.matrices"],
    "mor.sets.matrix_det": ["obj.sets.matrices"],
    "mor.sets.matrix_trace": ["obj.sets.matrices"],
}


class NativeValues:
    def __init__(self):
        self.values = {}

    def retain(self, descriptor, native):
        token = str(len(self.values) + 1)
        self.values[token] = (descriptor, native)
        return opaque_data(token)

    def lower(self, data, descriptor):
        if isinstance(data, dict) and data.get("ctor") == "valueData":
            data, = constructor(data, "valueData", 1)
        if isinstance(data, dict) and data.get("ctor") == "opaqueData":
            token, = constructor(data, "opaqueData", 1)
            if not isinstance(token, str) or token not in self.values:
                raise ValueError("unknown token on this live polynomial connection")
            original, native = self.values[token]
            if original != descriptor:
                # The caller may supply the formal nonzero/monic view of a polynomial.
                # Preserve its exact coefficient ring; do not recover it from a carrier.
                if polynomial_coefficient(original) != polynomial_coefficient(descriptor):
                    raise ValueError("opaque value changes its selected computational endpoint")
            return native
        form, parameters = named_object(descriptor)
        if form in POLYNOMIAL_FORMS or form == "obj.sets.monics":
            ring = PolynomialRing(base_ring(polynomial_coefficient(descriptor)), "t")
            if isinstance(data, dict) and data.get("ctor") == "element":
                selected, data = constructor(data, "element", 2)
                if selected != descriptor:
                    raise ValueError("element changes its full selected polynomial endpoint")
            return arithmetic(data, ring)
        raise ValueError("no published inline lowering for this selected endpoint")


def polynomial_coefficient(descriptor):
    form, parameters = named_object(descriptor)
    if form in POLYNOMIAL_FORMS and len(parameters) == 1:
        return parameters[0]
    if form == "obj.sets.monics" and len(parameters) == 2:
        numeral(parameters[0])
        return parameters[1]
    raise ValueError("not a published selected polynomial endpoint")


def coefficient_change(parameters):
    if len(parameters) != 3:
        raise ValueError("coefficient change needs both selected rings and the actual map")
    source, target, arrow = parameters
    # Identity is an actual published arrow descriptor, not an endpoint rename.
    form, arguments = named_object(arrow)
    if form == "identity" and source == target and arguments == [source, target]:
        return base_ring(target)
    if (form == "mor.commutative_rings.integer_coefficients"
            and source == {"ctor": "obj.commutative_rings.integers", "args": []}
            and arguments == [target]):
        return base_ring(target)
    raise ValueError("no native lowering for this selected coefficient map")


class PolynomialAdapter:
    def __init__(self):
        self.native = NativeValues()

    def invoke(self, operation, request):
        _, parameters, arrow, domain, source, target, argument = point_invocation(request, operation)
        form, _ = named_object(source)
        if form not in OPERATIONS[operation]:
            raise ValueError("operation has no registration for this input form")
        # The common contract fixes arrow and generalized domain upstream. Neither
        # is synthesized, interpreted as mathematics, or rewritten by this adapter.
        value = self.native.lower(argument, source)
        if operation == "mor.sets.polynomial_degree":
            result = value_data({"ctor": "none", "args": []} if not value
                                else {"ctor": "some", "args": [int(value.degree())]})
            return result
        if operation in {"mor.sets.polynomial_factorization", "mor.sets.polynomial_factors"}:
            if not value:
                raise ValueError("zero is outside the published factorization input")
            factorization = value.factor()
            parent = value.parent()
            unit = parent(factorization.unit())
            factors = [(parent(factor), count) for factor, count in factorization]
            # Sage represents a constant integer polynomial as scalar content.
            # Factor that content with its native integer engine as well, so the
            # published unit field does not silently become a nonunit scalar.
            if not unit.is_unit():
                content = factorization.unit().factor()
                unit = parent(content.unit())
                factors = [(parent(factor), count) for factor, count in content] + factors
            if operation.endswith("_factors"):
                result = tuple(factor for factor, _ in factors)
            else:
                result = (unit, tuple(factor for factor, count in factors for _ in range(count)))
        elif operation == "mor.sets.polynomial_roots":
            if not value:
                raise ValueError("zero is outside the published finite roots input")
            result = tuple(value.roots(multiplicities=False))
        elif operation == "mor.sets.polynomial_factorization_unit":
            result = value[0]
        elif operation == "mor.sets.polynomial_factorization_factors":
            result = value[1]
        elif operation == "mor.sets.polynomial_factorization_product":
            unit, factors = value
            result = unit * unit.parent().prod(factors)
        elif operation == "mor.sets.polynomial_factorization_map":
            base = coefficient_change(parameters)
            unit, factors = value
            result = (unit.change_ring(base), tuple(f.change_ring(base) for f in factors))
        elif operation == "mor.sets.polynomial_map":
            result = value.change_ring(coefficient_change(parameters))
        elif operation == "mor.sets.companion_matrix":
            degree, coefficient = named_object(source)[1]
            if value.degree() != degree or not value.is_monic():
                raise ValueError("native polynomial does not conform to the selected monic degree")
            result = companion_matrix(value, format="right")
        elif operation == "mor.sets.matrix_charpoly":
            result = value.charpoly()
        elif operation == "mor.sets.matrix_det":
            result = value.det()
        elif operation == "mor.sets.matrix_trace":
            result = value.trace()
        else:
            raise ValueError("unsupported released polynomial operation")
        return self.native.retain(target, result)


if __name__ == "__main__":
    adapter = PolynomialAdapter()
    serve("sage-polynomials", SAGE_VERSION, "0.1.0",
          {op: (lambda request, op=op: adapter.invoke(op, request)) for op in OPERATIONS})
