"""Primitive adapters over public records and native Sage parents.

Record order comes from the published constructor signatures and CasContract's
data-only codec. Native arithmetic stays behind connection-local opaque fields.
This module supplies no laws or mathematical placements.
"""

from dataclasses import dataclass
import operator
import secrets

from cas_port import construction_invocation, opaque_data, value_data
from sage.all import IntegerModRing, LazyPowerSeriesRing, MatrixSpace, NN, PolynomialRing, QQ, ZZ


OPERATIONS = ("fun.rings.semiring", "fun.semirings.monoid", "op.monoids.mul", "mor.sets.equality")


class Unsupported(Exception):
    """No implementation of this public representation in this specimen."""


class Unavailable(Exception):
    """An opaque dependency is absent from this live connection."""


def tag(data):
    return data.get("ctor") if isinstance(data, dict) else None


def fields(data, expected, count):
    if tag(data) != expected:
        raise ValueError("expected the %s envelope" % expected)
    result = data.get("args")
    if not isinstance(result, list) or len(result) != count:
        raise ValueError("%s requires %d ordered fields" % (expected, count))
    return result


def inline(data):
    while tag(data) == "valueData":
        data, = fields(data, "valueData", 1)
    return data


def record(data, name, count):
    result = inline(data)
    if not isinstance(result, list):
        raise Unsupported("%s has no implemented complete record representation" % name)
    if len(result) != count:
        raise ValueError("%s requires %d non-proof fields" % (name, count))
    return result


def natural(data):
    if type(data) is not int or data < 0:
        raise ValueError("the selected parameter requires a natural number")
    return data


@dataclass(frozen=True)
class RetainedNative:
    value: object
    request: object
    field: str
    carrier: object = None
    context: object = None


@dataclass(frozen=True)
class ProductComputation:
    """Private receipt for an actual selected field application, not evidence."""

    parameters: object
    fragment: object
    packet: object
    domain: object
    source: object
    target: object
    field: object
    operands: object


@dataclass(frozen=True)
class PointResult:
    """A returned scalar retains this actual invocation and its computed data."""

    invocation: object
    data: object


@dataclass(frozen=True)
class LiteralPoint:
    fragment: object
    packet: object
    carrier: object


@dataclass(frozen=True)
class FieldComputation:
    field: object
    operands: object
    packet: object


class Session:
    """Only this process can interpret the tokens it supplied."""

    def __init__(self):
        self.prefix = secrets.token_hex(16)
        self.values = {}
        self.completed = []

    def keep(self, value, request, field, carrier=None, context=None):
        token = "%s:%d" % (self.prefix, len(self.values))
        self.values[token] = RetainedNative(value, request, field, carrier, context)
        return opaque_data(token)

    def get(self, data):
        token, = fields(inline(data), "opaqueData", 1)
        if not isinstance(token, str) or not token:
            raise ValueError("an opaque dependency needs a nonempty token")
        if token not in self.values:
            raise Unavailable("the opaque dependency is not owned by this live connection")
        return self.values[token]

    def check_dependencies(self, data):
        if tag(data) == "opaqueData":
            self.get(data)
        if isinstance(data, dict):
            for item in data.values():
                self.check_dependencies(item)
        elif isinstance(data, list):
            for item in data:
                self.check_dependencies(item)


def native_commutative_ring(data):
    """Decode only the exact published coefficient forms implemented here."""
    data = inline(data)
    kind = tag(data)
    parents = {"obj.commutative_rings.integers": ZZ,
               "obj.commutative_rings.rationals": QQ}
    if kind in parents:
        fields(data, kind, 0)
        return parents[kind]
    if kind == "obj.commutative_rings.integers_mod":
        modulus, = fields(data, kind, 1)
        return IntegerModRing(natural(modulus))
    raise Unsupported("this exact coefficient ring has no native reader in the specimen")


def native_ring(data):
    data = inline(data)
    kind = tag(data)
    prefix = "obj.rings."
    if kind in {prefix + "integers", prefix + "rationals"}:
        fields(data, kind, 0)
        return ZZ if kind == prefix + "integers" else QQ
    if kind == prefix + "integers_mod":
        modulus, = fields(data, kind, 1)
        return IntegerModRing(natural(modulus))
    if kind in {prefix + "polynomials", prefix + "power_series"}:
        coefficient, = fields(data, kind, 1)
        parent = native_commutative_ring(coefficient)
        return (PolynomialRing(parent, "x") if kind == prefix + "polynomials"
                else LazyPowerSeriesRing(parent, "t"))
    if kind == prefix + "mv_polynomials":
        dimension, coefficient = fields(data, kind, 2)
        return PolynomialRing(native_commutative_ring(coefficient), natural(dimension), "x")
    if kind == prefix + "matrices":
        dimension, coefficient = fields(data, kind, 2)
        return MatrixSpace(native_commutative_ring(coefficient), natural(dimension))
    raise Unsupported("this exact named ring has no native reader in the specimen")


class Actions:
    def __init__(self):
        self.session = Session()

    def native_monoid(self, parent, request, carrier):
        keep = lambda value, field: self.session.keep(value, request, field, carrier)
        # The single-field Mul, Semigroup, One and NPow records are elided by
        # the public codec. NPow's first argument is the natural exponent.
        multiply = lambda left: lambda right: operator.mul(parent(left), parent(right))
        power = lambda exponent: lambda value: parent(value) ** ZZ(exponent)
        return [keep(multiply, "Monoid.toSemigroup"),
                keep(parent.one(), "Monoid.toOne"),
                keep(power, "Monoid.toNPow")]

    def native_semiring(self, parent, request):
        carrier = self.session.keep(parent, request, "SemiRingCat.carrier")
        keep = lambda value, field: self.session.keep(value, request, field, carrier)
        add = lambda left: lambda right: operator.add(parent(left), parent(right))
        scale = lambda scalar: lambda value: ZZ(scalar) * parent(value)
        cast = lambda scalar: parent(ZZ(scalar))
        additive = [keep(add, "AddMonoid.toAddSemigroup"),
                    keep(parent.zero(), "AddMonoid.toZero"),
                    keep(scale, "AddMonoid.toNSMul")]
        return [carrier,
                [additive, self.native_monoid(parent, request, carrier),
                 keep(cast, "Semiring.toNatCast")]]

    @staticmethod
    def semiring_record(data):
        carrier, structure = record(data, "SemiRingCat", 2)
        additive, multiplicative, cast = record(structure, "Semiring", 3)
        record(additive, "AddCommMonoid/AddMonoid", 3)
        record(multiplicative, "Monoid", 3)
        return carrier, structure, multiplicative

    def run(self, operation, packet):
        if operation not in OPERATIONS:
            raise Unsupported("the operation is not registered by this specimen")
        self.session.check_dependencies(packet)
        if operation == "op.monoids.mul":
            from monoid_multiplication import Multiplication
            result = Multiplication(self.session, packet).run()
            self.session.completed.append((packet, result))
            return result
        if operation == "mor.sets.equality":
            from set_equality import Equality
            result = Equality(self.session, packet).run()
            self.session.completed.append((packet, result))
            return result
        _, parameters, receiver = construction_invocation(packet, operation)
        if parameters:
            raise ValueError("this published primitive has no explicit data parameters")
        actual = inline(receiver)
        if operation == "fun.rings.semiring":
            if isinstance(actual, list):
                carrier, ring = record(actual, "RingCat", 2)
                semiring, _, _, _, _ = record(ring, "Ring", 5)
                self.semiring_record([carrier, semiring])
                output = [carrier, semiring]
            else:
                output = self.native_semiring(native_ring(actual), packet)
        elif tag(actual) == "obj.semirings.naturals":
            fields(actual, "obj.semirings.naturals", 0)
            carrier = self.session.keep(NN, packet, "MonCat.carrier")
            output = [carrier, self.native_monoid(NN, packet, carrier)]
        else:
            carrier, _, multiplicative = self.semiring_record(actual)
            output = [carrier, multiplicative]
        result = value_data(output)
        self.session.completed.append((packet, result))
        return result
