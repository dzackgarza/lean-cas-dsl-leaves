"""Apply the actual multiplication field of a supplied public MonCat record.

The existing leaf wire helper supplies finite graphs and framed callables. Native
arithmetic is the owned field itself; no source ring or functor is reconstructed.
"""

import importlib.util
from itertools import product
from pathlib import Path
import sys

from cas_port import map_data, object_product, point_invocation, typed_map, value_data
from sage.all import NN, QQ, ZZ
from primitive_actions import Unsupported, fields, inline, natural, record, tag


# Load the existing computational helper by its exact path. Do not import its
# backend, engine, manifest, or any other registrations.
_path = Path(__file__).resolve().parents[1] / "extensions-20261024" / "wire.py"
_spec = importlib.util.spec_from_file_location("_primitive_actions_public_wire", _path)
wire = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = wire
_spec.loader.exec_module(wire)

OPERATION = "op.monoids.mul"


class NativeValues:
    def __init__(self, session):
        self.session = session

    def get(self, data):
        return self.session.get(data).value


class Multiplication:
    def __init__(self, session, packet):
        self.session, self.packet = session, packet
        _, self.parameters, self.arrow, self.domain, self.source, self.target, self.argument = (
            point_invocation(packet, OPERATION))
        if len(self.parameters) != 1:
            raise ValueError("monoid multiplication requires its complete selected monoid")
        self.selected, = self.parameters
        self.carrier, structure = record(self.selected, "MonCat", 2)
        self.multiplication, _, _ = record(structure, "Monoid", 3)
        self.left, self.right = object_product(inline(self.source))
        self.native_values = NativeValues(session)
        self.field_points = None
        self.parent, self.origin = None, None
        if tag(inline(self.carrier)) == "opaqueData":
            native = session.get(self.carrier)
            if native.field not in {"SemiRingCat.carrier", "MonCat.carrier"}:
                raise Unsupported("this owned field has no native carrier reader")
            self.parent = native.value
            self.origin = native.request["receiver"]

    @staticmethod
    def closed(domain):
        if tag(domain) != "obj.sets.fin":
            return False
        size, = fields(domain, "obj.sets.fin", 1)
        return type(size) is int and size == 1

    def inventory(self, selected):
        selected = inline(selected)
        try:
            return wire.inventory(selected)
        except wire.Unsupported:
            pass
        if tag(selected) == "objectProduct":
            left, right = object_product(selected)
            return [list(pair) for pair in product(self.inventory(left), self.inventory(right))]
        if (wire.key(inline(selected)) == wire.key(inline(self.carrier))
                and self.parent is not None
                and tag(inline(self.origin)) == "obj.rings.integers_mod"
                and self.parent.is_finite()):
            return [int(value) for value in self.parent]
        raise Unsupported("this callable source has no supported complete point inventory")

    def check_owner(self, selected):
        contexts = [self.selected, self.carrier, self.target, self.left, self.right]
        if self.origin is not None:
            contexts.append(self.origin)
        if not any(wire.key(selected) == wire.key(context) for context in contexts):
            raise ValueError("the element changed its complete selected context")

    def point_data(self, data):
        data = inline(data)
        if tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            self.check_owner(selected)
            if tag(expression) == "numeral":
                # Only the retained named ring/semiring origin supplies this
                # numeral reader; the generic monoid declares no numerals.
                if self.origin is None or wire.key(selected) != wire.key(self.origin):
                    raise Unsupported("a generic monoid does not supply numeral literals")
                number, = fields(expression, "numeral", 1)
                return self.session.keep(self.parent(natural(number)), self.packet,
                                         "Monoid.product", self.carrier)
            return self.point_data(expression)
        return data

    def native_point(self, data):
        data = self.point_data(data)
        if tag(data) == "opaqueData":
            native = self.session.get(data)
            if native.field not in {"AddMonoid.toZero", "Monoid.toOne", "Monoid.product"}:
                raise ValueError("the owned operand is not a retained native point")
            wire.same(inline(native.carrier), inline(self.carrier), "operand's retained carrier")
            return native.value
        if self.parent is QQ:
            numerator, denominator = record(data, "rational point", 2)
            if (type(numerator) is not int or type(denominator) is not int
                    or denominator <= 0 or ZZ(numerator).gcd(denominator) != 1):
                raise ValueError("a rational point requires its reduced public record")
            return QQ(numerator) / QQ(denominator)
        if self.parent is ZZ and type(data) is int:
            return ZZ(data)
        if self.parent is NN and type(data) is int:
            return NN(natural(data))
        if (tag(inline(self.origin)) == "obj.rings.integers_mod" and type(data) is int
                and self.parent.is_finite()):
            if data < 0 or data >= self.parent.cardinality():
                raise ValueError("the modular point is outside its supplied carrier")
            return self.parent(data)
        raise Unsupported("this native operand needs an owned point or a supported public literal")

    def field_function(self, data, target):
        data = inline(data)
        if tag(data) == "opaqueData":
            return self.function(data, self.carrier, target)
        try:
            points = self.inventory(self.carrier)
        except Unsupported:
            if self.field_points is None:
                if tag(data) != "finiteGraph":
                    raise Unsupported("a function-valued field needs its actual inventory")
                self.field_points, _ = fields(data, "finiteGraph", 2)
            points = self.field_points
        try:
            return wire.graph_callable(data, self.carrier, target,
                                       finite_inventory=lambda _: points)
        except wire.Unsupported as error:
            raise Unsupported(str(error)) from error

    def product(self, pair):
        pair = inline(pair)
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("monoid multiplication requires both actual operand fields")
        multiplication = inline(self.multiplication)
        if tag(multiplication) == "opaqueData":
            native = self.session.get(multiplication)
            if native.field != "Monoid.toSemigroup" or not callable(native.value):
                raise Unsupported("this owned multiplication field has no curried native reader")
            wire.same(inline(native.carrier), inline(self.carrier), "multiplication's retained carrier")
            left, right = (self.native_point(point) for point in pair)
            result = native.value(left)(right)
            return self.session.keep(result, self.packet, "Monoid.product", self.carrier)
        # Mul's published field is curried: carrier -> carrier -> carrier.
        maps = wire.node("obj.sets.maps", self.carrier, self.carrier)
        row = self.field_function(multiplication, maps)(self.point_data(pair[0]))
        result = self.field_function(row, self.carrier)(self.point_data(pair[1]))
        try:
            points = self.inventory(self.carrier)
        except Unsupported:
            points = self.field_points
        if points is not None and wire.key(result) not in {wire.key(p) for p in points}:
            raise ValueError("the field returned a point outside its actual supplied inventory")
        return result

    def selection(self, arrow):
        arrow = inline(arrow)
        if tag(arrow) == "typedMap":
            return self.selection(typed_map(arrow)[2])
        if tag(arrow) == OPERATION:
            selected, = fields(arrow, OPERATION, 1)
            wire.same([selected], self.parameters, "multiplication's complete parameter list")
        elif tag(arrow) == "opaqueData":
            actual = self.session.get(arrow).value
            if not isinstance(actual, wire.Callable) or actual.invocation is None:
                raise Unsupported("the owned operation arrow has no retained invocation")
            wire.same(actual.invocation.operation, OPERATION, "owned operation")
            wire.same(actual.invocation.parameters, self.parameters, "owned operation parameters")
        elif tag(arrow) == "compose":
            for part in fields(arrow, "compose", 2):
                self.selection(part)

    def function(self, data, source, target):
        try:
            return wire.framed_callable(data, source, target, self.native_values, self.interpret,
                                        finite_inventory=self.inventory,
                                        product_factors=lambda selected, components=None:
                                            object_product(inline(selected)))
        except wire.Unsupported as error:
            raise Unsupported(str(error)) from error

    def callable_argument(self, data):
        data = inline(data)
        if tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            self.check_owner(selected)
            return self.callable_argument(expression)
        if tag(data) == "opaqueData":
            return isinstance(self.session.get(data).value, wire.Callable)
        return tag(data) in {"typedMap", "identity", "compose", "mediator", "finiteGraph", "point"}

    def interpret(self, arrow, source, target):
        if tag(arrow) == "compose":
            first, second = fields(arrow, "compose", 2)
            middle = wire.retained_endpoint(first, "target", self.native_values)
            following = wire.retained_endpoint(second, "source", self.native_values)
            if middle is not None and following is not None:
                wire.same(middle, following, "composition's retained shared endpoint")
            if middle is None:
                middle = following
            if middle is None:
                raise Unsupported("composition needs an actual retained shared endpoint")
            left, right = self.function(first, source, middle), self.function(second, middle, target)
            return wire.Callable(source, target, lambda point: right(left(point)))
        if tag(arrow) == OPERATION:
            self.selection(arrow)
            return wire.Callable(source, target, self.product)
        if tag(arrow) == "point":
            return self.function(fields(arrow, "point", 1)[0], source, target)
        if tag(arrow) == "element":
            selected, expression = fields(arrow, "element", 2)
            self.check_owner(selected)
            if not self.closed(source) or self.callable_argument(expression):
                return self.function(expression, source, target)
            return wire.Callable(source, target, lambda _: arrow)
        raise Unsupported("this callable expression has no implemented reader in the primitive provider")

    def run(self):
        self.selection(self.arrow)
        action = self.function(self.arrow, self.source, self.target)
        if self.closed(self.domain) and not self.callable_argument(self.argument):
            data = action(self.argument)
            return data if tag(data) in {"opaqueData", "valueData"} else value_data(data)
        argument = self.function(self.argument, self.domain, self.source)
        if self.closed(self.domain):
            data = action(argument(self.inventory(self.domain)[0]))
            return data if tag(data) in {"opaqueData", "valueData"} else value_data(data)
        retained = wire.Invocation(OPERATION, self.parameters, self.packet, argument, action)
        result = wire.Callable(self.domain, self.target,
                               lambda point: action(argument(point)), invocation=retained)
        token = self.session.keep(result, self.packet, "Monoid.callable", self.carrier)
        return value_data(map_data(self.domain, self.target, token))
