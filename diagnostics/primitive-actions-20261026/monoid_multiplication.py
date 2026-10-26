"""Apply the actual curried multiplication field of a supplied MonCat record."""

from cas_port import operation_expression, point_invocation
from primitive_actions import ProductComputation, Unsupported, fields, inline, tag
from point_calls import (MULTIPLY, NativePoints, NativeValues, PointCall,
                        monoid_fields, named_set, set_carrier, wire)


OPERATION = MULTIPLY


class Multiplication(PointCall):
    operation = OPERATION
    result_field = "Monoid.callable"

    def __init__(self, session, packet):
        super().__init__(session, packet)
        self.prepare()

    @classmethod
    def at_arrow(cls, session, packet, arrow, source, target):
        """Read a nested complete arrow at its actual supplied endpoints.

        The outer packet and original arrow remain attached; no synthetic
        invocation, new registration or replacement endpoint is introduced.
        """
        selected, = fields(arrow, OPERATION, 1)
        result = cls.__new__(cls)
        result.session, result.packet, result.arrow = session, packet, arrow
        result.selected, result.parameters = selected, [selected]
        result.source, result.target = source, target
        result.domain = point_invocation(packet)[3]
        result.native_values = NativeValues(session)
        result.prepare()
        return result

    @classmethod
    def at_expression(cls, session, packet, expression, domain, target):
        operation, parameters, operands = operation_expression(expression)
        if operation != OPERATION:
            raise Unsupported("this expression does not select monoid multiplication")
        if len(parameters) != 1 or len(operands) != 2:
            raise ValueError("multiplication needs its complete monoid and two operands")
        result = cls.__new__(cls)
        result.session, result.packet, result.arrow = session, packet, expression
        result.selected, result.parameters = parameters[0], parameters
        # An expression has operand fields, not an arrow-source field. Retain
        # that distinction instead of fabricating or retyping an invocation.
        result.source, result.target, result.domain = None, target, domain
        result.native_values = NativeValues(session)
        result.prepare(factors=(target, target))
        return result

    def prepare(self, factors=None):
        self.carrier, self.multiplication, _, _ = monoid_fields(self.selected)
        self.left, self.right = self.product_factors(self.source) if factors is None else factors
        self.points = NativePoints(self.session, self.packet, self.carrier,
                                   [self.selected, self.left, self.right, self.target])
        for endpoint in (self.left, self.right, self.target):
            if wire.key(inline(endpoint)) == wire.key(inline(self.carrier)):
                continue
            actual, _ = set_carrier(self.endpoint_view(endpoint))
            if wire.key(inline(actual)) == wire.key(inline(self.carrier)):
                continue
            if self.points.origin is not None and self.points.kind is not None:
                wire.same(inline(actual), named_set(self.points.origin),
                          "multiplication's explicit scalar carrier")
            else:
                raise ValueError("multiplication changed its selected carrier data")
        self.field_points = None

    def point_context(self, target):
        if any(wire.key(target) == wire.key(context)
               for context in (self.carrier, self.left, self.right, self.target)):
            return self.points
        return super().point_context(target)

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

    def product(self, pair, fragment=None):
        pair = inline(pair)
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("monoid multiplication requires both actual operand fields")
        pair = [self.resolve_value(point, target) for point, target in zip(pair, (self.left, self.right))]
        multiplication = inline(self.multiplication)
        if tag(multiplication) == "opaqueData":
            native = self.session.get(multiplication)
            if native.field != "Monoid.toSemigroup" or not callable(native.value):
                raise Unsupported("this owned multiplication field has no curried native reader")
            wire.same(inline(native.carrier), inline(self.carrier), "multiplication's retained carrier")
            left, right = (self.points.read(point) for point in pair)
            result = native.value(left)(right)
            context = ProductComputation(self.parameters, self.arrow if fragment is None else fragment,
                                         self.packet, self.domain, self.source, self.target,
                                         self.multiplication, pair)
            return self.session.keep(result, self.packet, "Monoid.product", self.carrier, context)
        # Mul's published field is curried: carrier -> carrier -> carrier.
        maps = wire.node("obj.sets.maps", self.carrier, self.carrier)
        row = self.field_function(multiplication, maps)(self.points.data(pair[0]))
        result = self.field_function(row, self.carrier)(self.points.data(pair[1]))
        try:
            points = self.inventory(self.carrier)
        except Unsupported:
            points = self.field_points
        if points is not None and wire.key(result) not in {wire.key(p) for p in points}:
            raise ValueError("the field returned a point outside its actual supplied inventory")
        return result

    def expression_function(self, expression, domain, target):
        operation, parameters, operands = operation_expression(expression)
        if operation != OPERATION:
            raise Unsupported("this monoid point expression names an unimplemented operation")
        wire.same(parameters, self.parameters, "expression's complete selected monoid")
        if len(operands) != 2:
            raise ValueError("monoid multiplication requires two expression operands")
        self.check_owner(self.selected, target)
        left = self.point_function(operands[0], domain, self.left)
        right = self.point_function(operands[1], domain, self.right)
        return wire.Callable(domain, target, lambda point, retained=(expression, left, right):
                             self.product([retained[1](point), retained[2](point)], retained[0]))

    def interpret(self, arrow, source, target):
        if tag(arrow) == OPERATION:
            self.selection(arrow)
            # A nested named occurrence still consumes the selected record's
            # actual multiplication field at the supplied endpoint framing.
            actual = self.at_arrow(self.session, self.packet, arrow, source, target)
            return wire.Callable(source, target, actual.product)
        raise Unsupported("this callable expression has no implemented reader in the primitive provider")
