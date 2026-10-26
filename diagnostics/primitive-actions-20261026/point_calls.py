"""Public point/callable framing shared by the two primitive point ports.

This is a data reader, not a type inference or registration service. Every
callable keeps its supplied endpoints; every computation keeps the original
request, selected wrappers and live dependencies in its closure or session.
"""

import importlib.util
from itertools import product
from pathlib import Path
import sys

from cas_port import map_data, morphism_endpoint, object_product, point_invocation, typed_map, value_data
from sage.all import IntegerModRing, NN, QQ, ZZ
from primitive_actions import Unsupported, fields, inline, natural, record, tag


# Privately reuse the existing computational helper, without its backend or
# registrations. Its Callable type is shared by both ports on this connection.
_path = Path(__file__).resolve().parents[1] / "extensions-20261024" / "wire.py"
_spec = importlib.util.spec_from_file_location("_primitive_actions_public_wire", _path)
wire = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = wire
_spec.loader.exec_module(wire)

MULTIPLY = "op.monoids.mul"
EQUALITY = "mor.sets.equality"


class NativeValues:
    def __init__(self, session):
        self.session = session

    def get(self, data):
        return self.session.get(data).value


def named_set(origin):
    """Read an implemented literal codec from its explicit public selection."""
    origin = inline(origin)
    names = {"obj.rings.integers": "obj.sets.integers",
             "obj.rings.rationals": "obj.sets.rationals",
             "obj.rings.integers_mod": "obj.sets.integers_mod",
             "obj.semirings.naturals": "obj.sets.naturals"}
    kind = tag(origin)
    if kind in names:
        return wire.node(names[kind], *fields(origin, kind, 1 if kind.endswith("integers_mod") else 0))
    return origin


def monoid_fields(selected):
    carrier, structure = record(selected, "MonCat", 2)
    multiplication, unit, power = record(structure, "Monoid", 3)
    return carrier, multiplication, unit, power


def set_carrier(selected):
    """Read only the explicitly supported complete public carrier paths.

    The descriptors in ``owners`` remain attached. No native-parent comparison
    identifies two structures, and no new descriptor replaces ``selected``.
    """
    data = inline(selected)
    if tag(data) == "finiteData":
        original, _ = fields(data, "finiteData", 2)
        wire.inventory(data)
        carrier, owners = set_carrier(original)
        return carrier, [selected, *owners]
    if tag(data) != "functorAction":
        return selected, [selected]
    action, receiver = fields(data, "functorAction", 2)
    if tag(action) == "fun.sets.identity":
        fields(action, "fun.sets.identity", 0)
        carrier, owners = set_carrier(receiver)
        return carrier, [selected, *owners]
    if tag(action) == "fun.semirings.forget":
        fields(action, "fun.semirings.forget", 0)
        carrier, semiring = record(receiver, "SemiRingCat", 2)
        additive, monoid, _ = record(semiring, "Semiring", 3)
        record(additive, "AddCommMonoid/AddMonoid", 3)
        record(monoid, "Monoid", 3)
        return carrier, [selected, receiver]
    if tag(action) == "classifierForget":
        classifier, parameters = fields(action, "classifierForget", 2)
        if classifier != "clf.sets.binary_operation":
            raise Unsupported("this classifier path has no selected-set point reader")
        wire.same(parameters, [], "binary-operation forget parameters")
        associative, semigroup = fields(inline(receiver), "functorAction", 2)
        kind, parameters = fields(associative, "classifierForget", 2)
        wire.same(kind, "clf.magmas.associative", "semigroup carrier action")
        wire.same(parameters, [], "associative forget parameters")
        forget, monoid = fields(inline(semigroup), "functorAction", 2)
        fields(forget, "fun.monoids.semigroup", 0)
        carrier, _, _, _ = monoid_fields(monoid)
        return carrier, [selected, receiver, semigroup, monoid]
    raise Unsupported("this complete carrier action has no point reader here")


class NativePoints:
    """Native values at an explicitly selected carrier, never a guessed owner."""

    def __init__(self, session, packet, carrier, owners=()):
        self.session, self.packet, self.carrier = session, packet, carrier
        self.owners = [carrier, *owners]
        self.parent, self.origin, self.kind, self.limit = None, None, None, None
        data = inline(carrier)
        if tag(data) == "opaqueData":
            native = session.get(data)
            if native.field not in {"SemiRingCat.carrier", "MonCat.carrier"}:
                raise Unsupported("this owned object has no native carrier reader")
            self.parent = native.value
            self.origin = native.request["receiver"]
            self.owners.append(self.origin)
            data = named_set(self.origin)
        kind = tag(data)
        parents = {"obj.sets.integers": ZZ, "obj.sets.rationals": QQ,
                   "obj.sets.naturals": NN}
        if kind in parents:
            fields(data, kind, 0)
            self.kind = kind
            if self.parent is None:
                self.parent = parents[kind]
        elif kind in {"obj.sets.integers_mod", "obj.sets.fin"}:
            size, = fields(data, kind, 1)
            self.limit = natural(size)
            self.kind = kind
            if self.parent is None:
                self.parent = IntegerModRing(self.limit) if kind.endswith("integers_mod") else ZZ

    def check_owner(self, selected):
        if not any(wire.key(selected) == wire.key(owner) for owner in self.owners):
            raise ValueError("the element changed its complete selected context")

    def data(self, data):
        data = inline(data)
        if tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            self.check_owner(selected)
            if tag(inline(expression)) == "numeral":
                # A monoid has no numeral interface. A known retained named
                # ring/semiring or named scalar set supplies this literal codec.
                literal_owner = self.origin if self.origin is not None else self.carrier
                named_literal = self.origin is not None or self.kind in {
                    "obj.sets.integers", "obj.sets.rationals", "obj.sets.naturals", "obj.sets.integers_mod"}
                if (wire.key(selected) != wire.key(literal_owner) or self.parent is None
                        or not named_literal):
                    raise Unsupported("this selected owner has no numeral reader")
                number, = fields(inline(expression), "numeral", 1)
                return self.session.keep(self.parent(natural(number)), self.packet,
                                         "Point.value", self.carrier)
            return self.data(expression)
        return data

    def read(self, data):
        data = self.data(data)
        if tag(data) == "opaqueData":
            native = self.session.get(data)
            if native.field not in {"AddMonoid.toZero", "Monoid.toOne", "Monoid.product", "Point.value"}:
                raise ValueError("the owned operand is not a retained native point")
            actual = inline(native.carrier)
            if wire.key(actual) != wire.key(inline(self.carrier)):
                # This bridge reads the stored origin descriptor, never the
                # native value's parent or another structure with that parent.
                if tag(actual) != "opaqueData":
                    raise ValueError("the point changed its retained carrier")
                stored = self.session.get(actual)
                if stored.field not in {"SemiRingCat.carrier", "MonCat.carrier"}:
                    raise ValueError("the point has no retained carrier descriptor")
                wire.same(named_set(stored.request["receiver"]), inline(self.carrier),
                          "point's explicitly selected scalar set")
            return native.value
        if self.kind == "obj.sets.rationals":
            numerator, denominator = record(data, "rational point", 2)
            if (type(numerator) is not int or type(denominator) is not int
                    or denominator <= 0 or ZZ(numerator).gcd(denominator) != 1):
                raise ValueError("a rational point requires its reduced public record")
            return QQ(numerator) / QQ(denominator)
        if self.kind == "obj.sets.integers" and type(data) is int:
            return ZZ(data)
        if self.kind == "obj.sets.naturals" and type(data) is int:
            return NN(natural(data))
        if self.kind in {"obj.sets.integers_mod", "obj.sets.fin"} and type(data) is int:
            if data < 0 or (self.limit and data >= self.limit) or (self.limit == 0 and self.kind.endswith("fin")):
                raise ValueError("the point is outside its supplied carrier")
            if self.limit == 0:
                raise Unsupported("modulus-zero literals need their integer representation")
            return self.parent(data)
        raise Unsupported("this point needs owned data or a supported public literal")


class PointCall:
    operation = None
    result_field = "Point.callable"

    def __init__(self, session, packet):
        self.session, self.packet = session, packet
        _, self.parameters, self.arrow, self.domain, self.source, self.target, self.argument = (
            point_invocation(packet, self.operation))
        self.native_values = NativeValues(session)
        if len(self.parameters) != 1:
            raise ValueError("this operation requires its one complete selected parameter")
        self.selected, = self.parameters

    @staticmethod
    def closed(domain):
        if tag(domain) != "obj.sets.fin":
            return False
        size, = fields(domain, "obj.sets.fin", 1)
        return type(size) is int and size == 1

    def endpoint_view(self, selected):
        data = inline(selected)
        if tag(data) == "finiteData":
            original, _ = fields(data, "finiteData", 2)
            wire.inventory(data)
            return self.endpoint_view(original)
        if tag(data) == "morphismEndpoint":
            arrow, side = morphism_endpoint(data)
            actual = wire.retained_endpoint(arrow, side, self.native_values)
            if actual is None:
                actual = self.declared_endpoint(arrow, side)
            if actual is None:
                raise Unsupported("the endpoint needs a supported full declaration or retained field")
            return self.endpoint_view(actual)
        return data

    def declared_endpoint(self, arrow, side):
        arrow = inline(arrow)
        if tag(arrow) == MULTIPLY:
            monoid, = fields(arrow, MULTIPLY, 1)
            carrier, _, _, _ = monoid_fields(monoid)
            return wire.node("objectProduct", carrier, carrier) if side == "source" else carrier
        if tag(arrow) == EQUALITY:
            selected, = fields(arrow, EQUALITY, 1)
            return wire.node("objectProduct", selected, selected) if side == "source" else wire.node("obj.sets.truth_values")
        return None

    def product_factors(self, selected, components=None):
        data = self.endpoint_view(selected)
        if tag(data) != "objectProduct":
            raise Unsupported("the selected endpoint has no supported public product interface")
        return object_product(data)

    def point_context(self, target):
        carrier, owners = set_carrier(self.endpoint_view(target))
        original = inline(target)
        while tag(original) == "finiteData":
            original = inline(fields(original, "finiteData", 2)[0])
        if tag(original) == "morphismEndpoint":
            arrow, side = morphism_endpoint(original)
            # A target endpoint of the complete multiplication declaration
            # retains its selected MonCat parameter as point-owner context.
            # The carrier still comes from the actual retained target field.
            while tag(inline(arrow)) in {"point", "typedMap", "compose"}:
                arrow = inline(arrow)
                if tag(arrow) == "typedMap":
                    arrow = typed_map(arrow)[2]
                elif tag(arrow) == "compose":
                    arrow = fields(arrow, "compose", 2)[0 if side == "source" else 1]
                else:
                    arrow, = fields(arrow, "point", 1)
            arrow = inline(arrow)
            if side == "target" and tag(arrow) == MULTIPLY:
                owners.extend(fields(arrow, MULTIPLY, 1))
            elif side == "target" and tag(arrow) == "opaqueData":
                actual = self.session.get(arrow).value
                if (isinstance(actual, wire.Callable) and actual.invocation is not None
                        and actual.invocation.operation == MULTIPLY):
                    owners.extend(actual.invocation.parameters)
        return NativePoints(self.session, self.packet, carrier, [target, *owners])

    def check_owner(self, selected, target):
        if wire.key(selected) == wire.key(target):
            return
        self.point_context(target).check_owner(selected)

    def inventory(self, selected):
        data = inline(selected)
        try:
            return wire.inventory(data)
        except wire.Unsupported:
            pass
        if tag(data) == "objectProduct":
            left, right = object_product(data)
            return [list(pair) for pair in product(self.inventory(left), self.inventory(right))]
        if tag(data) == "morphismEndpoint":
            raise Unsupported("a declared endpoint does not supply a point inventory")
        points = self.point_context(selected)
        if points.kind == "obj.sets.integers_mod" and points.limit:
            return [int(value) for value in points.parent]
        raise Unsupported("this callable source has no supported complete point inventory")

    def callable_data(self, data):
        data = inline(data)
        if tag(data) == "opaqueData":
            return isinstance(self.session.get(data).value, wire.Callable)
        return tag(data) in {"typedMap", "identity", "compose", "mediator", "finiteGraph", "point",
                             MULTIPLY, EQUALITY}

    def resolve_value(self, data, target):
        """Consume complete closed fragments in an actual scalar-data field.

        A graph's image can itself contain complete point expressions. Their
        actual retained domain, or the original closed invocation domain, is
        required; a non-singleton callable is never sampled as one point.
        """
        value = inline(data)
        if tag(value) == "element":
            selected, expression = fields(value, "element", 2)
            self.check_owner(selected, target)
            expression = inline(expression)
            computational = self.callable_data(expression) or tag(expression) in {"element", "operationExpression"}
        else:
            computational = self.callable_data(value) or tag(value) == "operationExpression"
        if not computational:
            return data
        domain = wire.retained_endpoint(value, "source", self.native_values)
        if domain is None:
            domain = getattr(self, "domain", None)
        if domain is None or not self.closed(domain):
            raise Unsupported("a scalar field's callable fragment needs its actual closed domain")
        actual = self.point_function(data, domain, target)
        return actual(self.inventory(domain)[0])

    def point_function(self, data, domain, target):
        """Read a generalized point in its declared point-data position.

        Product arrays contain ordered component data here; raw arrays inside
        an explicit callable/typedMap body keep the finite-graph convention.
        """
        original, data = data, inline(data)
        if tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            self.check_owner(selected, target)
            if (not self.closed(domain) or self.callable_data(expression)
                    or tag(inline(expression)) in {"element", "operationExpression"}):
                actual = self.point_function(expression, domain, target)
                return wire.Callable(domain, target, lambda point, retained=(original, actual): retained[1](point))
            return wire.Callable(domain, target, lambda _, retained=original: retained)
        if tag(data) == "operationExpression":
            return self.expression_function(data, domain, target)
        view = self.endpoint_view(target)
        if tag(view) == "objectProduct" and isinstance(data, list):
            return self.product_point_function(original, domain, target)
        if tag(view) == "obj.sets.maps" and self.closed(domain):
            source, codomain = fields(view, "obj.sets.maps", 2)
            # An actual function-valued point has its own endpoints. A map
            # from the global domain into that function object is different.
            actual_source = wire.retained_endpoint(data, "source", self.native_values)
            actual_target = wire.retained_endpoint(data, "target", self.native_values)
            if isinstance(data, list) or tag(data) == "finiteGraph" or (
                    wire.key(actual_source) == wire.key(source) and wire.key(actual_target) == wire.key(codomain)):
                return wire.Callable(domain, target, lambda _, retained=original: retained)
        if self.callable_data(data) or isinstance(data, list) and not self.closed(domain):
            return self.function(data, domain, target)
        if not self.closed(domain):
            raise Unsupported("scalar point data cannot replace a generalized callable")
        return wire.Callable(domain, target, lambda _, retained=original: retained)

    def product_point_function(self, original, domain, target):
        data = inline(original)
        components, graph, component_error, graph_error = None, None, None, None
        try:
            if len(data) != 2:
                raise ValueError("a product point requires both ordered components")
            left, right = self.product_factors(target)
            components = (self.point_function(data[0], domain, left),
                          self.point_function(data[1], domain, right))
        except (ValueError, Unsupported) as error:
            component_error = error
        # A raw graph is also a published callable representation. Check its
        # framing using the actual domain inventory, without evaluating it or
        # choosing between two well-framed readings by their computed values.
        try:
            graph = self.function(data, domain, target)
        except (ValueError, Unsupported) as error:
            graph_error = error
        if components is not None and graph is not None:
            raise Unsupported("a bare product array has both point-component and graph readings; use mediator or finiteGraph")
        if components is not None:
            f, g = components
            return wire.Callable(domain, target, lambda point, retained=(original, f, g):
                                 [retained[1](point), retained[2](point)])
        if graph is not None:
            return graph
        raise component_error if component_error is not None else graph_error

    def function(self, data, source, target):
        data = inline(data)
        # Keep a typed body's callable position explicit, including raw graphs.
        if tag(data) == "typedMap":
            actual_source, actual_target, body = typed_map(data)
            wire.same(actual_source, source, "callable source")
            wire.same(actual_target, target, "callable target")
            actual = self.function(body, source, target)
            return wire.Callable(source, target, lambda point, retained=(data, actual): retained[1](point),
                                 invocation=actual.invocation)
        if tag(data) == "compose":
            first, second = fields(data, "compose", 2)
            before = wire.retained_endpoint(first, "target", self.native_values)
            after = wire.retained_endpoint(second, "source", self.native_values)
            if before is not None and after is not None:
                wire.same(before, after, "composition's retained shared endpoint")
            middle = before if before is not None else after
            if middle is None:
                middle = self.declared_endpoint(second, "source")
            if middle is None:
                middle = self.declared_endpoint(first, "target")
            if middle is None:
                raise Unsupported("composition needs an actual retained or declared shared endpoint")
            f, g = self.function(first, source, middle), self.function(second, middle, target)
            return wire.Callable(source, target, lambda point, retained=(data, f, g): retained[2](retained[1](point)))
        if tag(data) == "mediator":
            left, right = fields(data, "mediator", 2)
            a, b = self.product_factors(target, (left, right))
            f, g = self.function(left, source, a), self.function(right, source, b)
            return wire.Callable(source, target, lambda point, retained=(data, f, g):
                                 [retained[1](point), retained[2](point)])
        if tag(data) in {"point", "element", "operationExpression"}:
            return (self.function(fields(data, "point", 1)[0], source, target) if tag(data) == "point"
                    else self.point_function(data, source, target))
        try:
            return wire.framed_callable(data, source, target, self.native_values, self.interpret,
                                        finite_inventory=self.inventory, product_factors=self.product_factors)
        except wire.Unsupported as error:
            raise Unsupported(str(error)) from error

    def expression_function(self, expression, domain, target):
        raise Unsupported("this selected operation expression has no reader in the port")

    def selection(self, arrow):
        arrow = inline(arrow)
        if tag(arrow) == "typedMap":
            return self.selection(typed_map(arrow)[2])
        if tag(arrow) == self.operation:
            selected, = fields(arrow, self.operation, 1)
            wire.same([selected], self.parameters, "operation's complete parameter list")
        elif tag(arrow) == "opaqueData":
            actual = self.session.get(arrow).value
            if not isinstance(actual, wire.Callable) or actual.invocation is None:
                raise Unsupported("the owned operation arrow has no retained invocation")
            wire.same(actual.invocation.operation, self.operation, "owned operation")
            wire.same(actual.invocation.parameters, self.parameters, "owned operation parameters")
        elif tag(arrow) == "compose":
            for part in fields(arrow, "compose", 2):
                self.selection(part)

    def finish(self, data):
        return data if tag(data) in {"opaqueData", "valueData"} else value_data(data)

    def result_data(self, data):
        return data

    def run(self):
        self.selection(self.arrow)
        action = self.function(self.arrow, self.source, self.target)
        argument = self.point_function(self.argument, self.domain, self.source)
        if self.closed(self.domain):
            return self.finish(self.result_data(action(argument(self.inventory(self.domain)[0]))))
        retained = wire.Invocation(self.operation, self.parameters, self.packet, argument, action)
        result = wire.Callable(self.domain, self.target,
                               lambda point: self.result_data(action(argument(point))), invocation=retained)
        token = self.session.keep(result, self.packet, self.result_field, self.target)
        return value_data(map_data(self.domain, self.target, token))
