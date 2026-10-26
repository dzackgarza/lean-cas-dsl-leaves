"""Public point/callable framing shared by the two primitive point ports.

This is a data reader, not a type inference or registration service. Every
callable keeps its supplied endpoints; every computation keeps the original
request, selected wrappers and live dependencies in its closure or session.
"""

import importlib.util
from itertools import product
from pathlib import Path
import sys

from cas_port import (construction_invocation, map_data, morphism_endpoint, object_product, operation_expression,
                      point_invocation, typed_map, value_data)
from sage.all import IntegerModRing, NN, QQ, ZZ
from primitive_actions import (FieldComputation, LiteralPoint, PointResult, ProductComputation, Unsupported,
                               fields, inline, natural, record, tag)


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


def record_field(session, data):
    """Find the exact creating request's actual returned record field."""
    native = session.get(data)
    operation = tag(native.request)
    if operation not in {"fun.rings.semiring", "fun.semirings.monoid"}:
        raise Unsupported("the native field has no supported object-action creator")
    _, parameters, _ = construction_invocation(native.request, operation)
    wire.same(parameters, [], "native field's complete object-action parameters")
    for packet, result in session.completed:
        if packet is not native.request:
            continue
        carrier, structure = record(result, "returned native record", 2)
        if operation == "fun.rings.semiring":
            additive, monoid, cast = record(structure, "returned Semiring", 3)
            add, zero, scale = record(additive, "returned AddMonoid", 3)
            slots = {"SemiRingCat.carrier": carrier, "AddMonoid.toAddSemigroup": add,
                     "AddMonoid.toZero": zero, "AddMonoid.toNSMul": scale,
                     "Semiring.toNatCast": cast}
        else:
            monoid = structure
            slots = {"MonCat.carrier": carrier}
        multiply, one, power = record(monoid, "returned Monoid", 3)
        slots.update({"Monoid.toSemigroup": multiply, "Monoid.toOne": one, "Monoid.toNPow": power})
        if native.field in slots and wire.key(inline(slots[native.field])) == wire.key(inline(data)):
            if native.carrier is not None:
                wire.same(native.carrier, carrier, "native field's actual returned carrier")
            return native, result, carrier
    raise ValueError("the native field is absent from its exact creating request's returned record")


def point_producer(session, data):
    """Read a native point's exact retained producing parameters and fragments.

    These are connection-private computational receipts. No native-parent
    comparison, carrier-name match, or arbitrary packet traversal supplies them.
    """
    native = session.get(data)
    context = native.context
    if native.field == "Point.result":
        if not isinstance(context, PointResult):
            raise ValueError("the returned point has no retained creating invocation")
        invocation = context.invocation
        operation, parameters, _, _, _, _, _ = point_invocation(native.request, MULTIPLY)
        wire.same(invocation.operation, operation, "point-result operation")
        wire.same(invocation.parameters, parameters, "point-result complete parameters")
        wire.same(invocation.packet, native.request, "point-result creating request")
        prior, _ = point_producer(session, context.data)
        if prior.value is not native.value:
            raise ValueError("the point-result receipt changed its actual native value")
        if len(parameters) != 1:
            raise ValueError("the point-result invocation lost its full selected parameter")
        selected, = parameters
        carrier, _, _, _ = monoid_fields(selected)
        wire.same(native.carrier, carrier, "point-result invocation's selected carrier")
        wire.same(native.carrier, prior.carrier, "point-result retained carrier")
        return native, selected
    if native.field in {"AddMonoid.toZero", "Monoid.toOne"}:
        record_field(session, data)
        return native, None
    if native.field == "Point.value" and isinstance(context, LiteralPoint):
        selected, expression = fields(context.fragment, "element", 2)
        natural(fields(inline(expression), "numeral", 1)[0])
        wire.same(context.packet, native.request, "literal point's creating request")
        wire.same(context.carrier, native.carrier, "literal point's retained carrier")
        if tag(inline(native.carrier)) == "opaqueData":
            creator, _, _ = record_field(session, native.carrier)
            wire.same(selected, creator.request["receiver"], "literal's exact selected creator")
        else:
            wire.same(selected, native.carrier, "literal's complete selected scalar set")
        return native, None
    if native.field == "Point.field" and isinstance(context, FieldComputation):
        field, _, carrier = record_field(session, context.field)
        arity = 1 if field.field == "Semiring.toNatCast" else 2
        if len(context.operands) != arity:
            raise ValueError("the field result lost an actual curried argument")
        wire.same(context.packet, native.request, "field result's actual creating request")
        wire.same(native.carrier, carrier, "field result's selected carrier")
        return native, None
    if native.field != "Monoid.product" or not isinstance(context, ProductComputation):
        raise Unsupported("this native datum is not a retained multiplication point result")
    if len(context.parameters) != 1:
        raise ValueError("the producing multiplication lost its selected parameter")
    selected, = context.parameters
    carrier, multiplication, _, _ = monoid_fields(selected)
    wire.same(native.request, context.packet, "point's exact creating packet")
    wire.same(native.carrier, carrier, "point's selected producing carrier")
    wire.same(context.field, multiplication, "point's actual producing multiplication field")
    fragment = inline(context.fragment)
    if tag(fragment) == MULTIPLY:
        wire.same(fields(fragment, MULTIPLY, 1), context.parameters,
                  "point's complete producing arrow parameters")
    elif tag(fragment) == "operationExpression":
        operation, parameters, operands = operation_expression(fragment)
        wire.same(operation, MULTIPLY, "point's producing expression operation")
        wire.same(parameters, context.parameters, "point's producing expression parameters")
        if len(operands) != 2:
            raise ValueError("the producing expression lost an operand")
    else:
        raise Unsupported("the point has no supported complete producing fragment")
    field, _, _ = record_field(session, multiplication)
    if field.field != "Monoid.toSemigroup" or not callable(field.value):
        raise ValueError("the point did not retain its actual native multiplication field")
    wire.same(inline(field.carrier), inline(carrier), "producing field's retained carrier")
    return native, selected


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
            native, _, _ = record_field(session, data)
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
                                         "Point.value", self.carrier,
                                         LiteralPoint(data, self.packet, self.carrier))
            return self.data(expression)
        return data

    def read(self, data):
        data = self.data(data)
        if tag(data) == "opaqueData":
            native, _ = point_producer(self.session, data)
            actual = inline(native.carrier)
            if wire.key(actual) != wire.key(inline(self.carrier)):
                # This bridge reads the stored origin descriptor, never the
                # native value's parent or another structure with that parent.
                if tag(actual) != "opaqueData":
                    raise ValueError("the point changed its retained carrier")
                stored, _, _ = record_field(self.session, actual)
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
                token = self.fragment_token(arrow)
                if token is not None and self.session.get(token).field == "Point.result":
                    native, _ = point_producer(self.session, token)
                    creating = point_invocation(native.request, MULTIPLY)
                    actual = creating[3 if side == "source" else 5]
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
                native = self.session.get(arrow)
                actual = native.value
                if (isinstance(actual, wire.Callable) and actual.invocation is not None
                        and actual.invocation.operation == MULTIPLY):
                    owners.extend(actual.invocation.parameters)
                elif native.field == "Point.result":
                    _, selected = point_producer(self.session, arrow)
                    owners.append(selected)
        return NativePoints(self.session, self.packet, carrier, [target, *owners])

    def check_owner(self, selected, target):
        if wire.key(selected) == wire.key(target):
            return
        self.point_context(target).check_owner(selected)

    def monoid_receivers(self, selected):
        """Actual earlier object-action receipts, not reconstructed objects."""
        receivers = []
        for packet, result in self.session.completed:
            if tag(packet) == "fun.semirings.monoid" and wire.key(inline(result)) == wire.key(inline(selected)):
                _, parameters, receiver = construction_invocation(packet, "fun.semirings.monoid")
                wire.same(parameters, [], "retained monoid projection parameters")
                receivers.append(receiver)
        return receivers

    def point_target(self, native, selected, target, owner=None):
        """Check a point-data conversion against its exact producing selection."""
        carrier, _, _, _ = monoid_fields(selected)
        wire.same(inline(native.carrier), inline(carrier), "converted point's producing carrier")
        target_monoid = self.selected_monoid(target)
        if target_monoid is not None:
            wire.same(target_monoid, selected, "point conversion's complete target selection")
        receivers = self.monoid_receivers(selected)
        carrier_native, _, _ = record_field(self.session, carrier)
        origin = carrier_native.request["receiver"]
        allowed = [selected, carrier, target, origin, *receivers]
        if isinstance(native.context, PointResult):
            original_target = point_invocation(native.request, MULTIPLY)[5]
            allowed.append(original_target)
        else:
            original_target = native.context.target
            allowed.append(original_target)
        if owner is not None and not any(wire.key(owner) == wire.key(item) for item in allowed):
            raise ValueError("the point conversion changed its complete selected owner")
        plain_target = inline(target)
        while tag(plain_target) == "finiteData":
            plain_target = inline(fields(plain_target, "finiteData", 2)[0])
        if wire.key(target) == wire.key(original_target) or wire.key(plain_target) == wire.key(inline(carrier)):
            return
        points = self.point_context(target)
        if wire.key(inline(points.carrier)) == wire.key(inline(carrier)):
            contexts = [selected, *receivers]
            if any(wire.key(context) == wire.key(actual) for context in contexts for actual in points.owners):
                return
        # Named scalar codecs need an explicit selected owner as well as the
        # complete producing invocation and exact object-action receipt.
        if owner is not None and any(wire.key(owner) == wire.key(item) for item in [selected, origin, *receivers]):
            wire.same(self.endpoint_view(target), named_set(origin), "point conversion's selected scalar codec")
            return
        raise ValueError("the point conversion has no retained binding to this selected endpoint")

    @staticmethod
    def fragment_token(data):
        data = inline(data)
        while tag(data) in {"point", "typedMap"}:
            data = inline(fields(data, "point", 1)[0] if tag(data) == "point" else typed_map(data)[2])
        return data if tag(data) == "opaqueData" else None

    def fragment_selection(self, data):
        """Read the actual output fragment's full selection, never search a packet."""
        data = inline(data)
        while tag(data) in {"point", "typedMap", "compose"}:
            if tag(data) == "point":
                data = fields(data, "point", 1)[0]
            elif tag(data) == "typedMap":
                data = typed_map(data)[2]
            else:
                data = fields(data, "compose", 2)[1]
            data = inline(data)
        if tag(data) == MULTIPLY:
            return fields(data, MULTIPLY, 1)[0]
        if tag(data) == "operationExpression":
            operation, parameters, operands = operation_expression(data)
            if operation == MULTIPLY:
                if len(parameters) != 1 or len(operands) != 2:
                    raise ValueError("the output expression lost its selected monoid or operands")
                return parameters[0]
        if tag(data) == "opaqueData":
            actual = self.session.get(data).value
            if isinstance(actual, wire.Callable):
                if actual.invocation is not None and actual.invocation.operation == MULTIPLY:
                    if len(actual.invocation.parameters) != 1:
                        raise ValueError("the output callable lost its complete selected monoid")
                    return actual.invocation.parameters[0]
            else:
                return point_producer(self.session, data)[1]
        return None

    def selected_monoid(self, target):
        """Read only an explicitly retained MonCat in a public target form."""
        data = inline(target)
        while True:
            if tag(data) == "finiteData":
                data = inline(fields(data, "finiteData", 2)[0])
            elif tag(data) == "functorAction" and tag(fields(data, "functorAction", 2)[0]) == "fun.sets.identity":
                action, receiver = fields(data, "functorAction", 2)
                fields(action, "fun.sets.identity", 0)
                data = inline(receiver)
            else:
                break
        if tag(data) == "morphismEndpoint":
            arrow, side = morphism_endpoint(data)
            if side == "target":
                return self.fragment_selection(arrow)
        if tag(data) == "functorAction":
            action, _ = fields(data, "functorAction", 2)
            if tag(action) == "classifierForget" and fields(action, "classifierForget", 2)[0] == "clf.sets.binary_operation":
                _, owners = set_carrier(data)
                return owners[-1]
        return None

    def check_element(self, selected, expression, target):
        try:
            producing_monoid = self.fragment_selection(expression)
        except Unsupported:
            producing_monoid = None
        if producing_monoid is not None:
            target_monoid = self.selected_monoid(target)
            if target_monoid is not None:
                wire.same(producing_monoid, target_monoid, "element's complete target monoid")
            if self.operation == MULTIPLY and wire.key(selected) == wire.key(self.selected):
                wire.same(producing_monoid, selected, "element's exact producing monoid")
        try:
            self.check_owner(selected, target)
            return
        except (Unsupported, ValueError) as original_error:
            producer = self.fragment_selection(expression)
            if producer is not None:
                wire.same(selected, producer, "element's complete producing monoid")
                carrier, _, _, _ = monoid_fields(producer)
                actual_carrier, _ = set_carrier(self.endpoint_view(target))
                if wire.key(inline(actual_carrier)) == wire.key(inline(carrier)):
                    return
                native, _, _ = record_field(self.session, carrier)
                wire.same(self.endpoint_view(target), named_set(native.request["receiver"]),
                          "element's explicitly selected scalar codec")
                return
            if not isinstance(inline(expression), dict) and self.monoid_receivers(selected):
                carrier, _, _, _ = monoid_fields(selected)
                target_monoid = self.selected_monoid(target)
                if target_monoid is not None:
                    wire.same(selected, target_monoid, "portable element's complete selected monoid")
                actual, _ = set_carrier(self.endpoint_view(target))
                wire.same(inline(actual), inline(carrier), "portable element's actual returned carrier")
                return
            token = self.fragment_token(expression)
            if token is None:
                raise original_error
            native, producer = point_producer(self.session, token)
            if producer is not None:
                wire.same(selected, producer, "element's complete producing monoid")
                self.point_target(native, producer, target, selected)
                return
            # Object fields have an actual returned record, but no invented
            # point-arrow domain. An element envelope supplies that context.
            if native.field not in {"AddMonoid.toZero", "Monoid.toOne"}:
                raise original_error
            record_field(self.session, token)
            if not self.monoid_receivers(selected):
                raise original_error
            target_monoid = self.selected_monoid(target)
            if target_monoid is not None:
                wire.same(selected, target_monoid, "record field element's complete selected monoid")
            carrier, _, unit, _ = monoid_fields(selected)
            if native.field == "Monoid.toOne":
                wire.same(inline(unit), inline(token), "element's actual returned unit field")
            wire.same(inline(native.carrier), inline(carrier), "element's exact returned carrier")
            points = self.point_context(target)
            wire.same(inline(points.carrier), inline(carrier), "element's actual selected set")

    def point_callable(self, data, source, target, owner):
        native, selected = point_producer(self.session, data)
        if native.field != "Point.result" or not isinstance(native.context, PointResult):
            raise Unsupported("a scalar field needs an element envelope before use as a point arrow")
        original_domain = point_invocation(native.request, MULTIPLY)[3]
        if not self.closed(original_domain):
            raise Unsupported("the retained value has no closed-point creating invocation")
        wire.same(source, original_domain, "point's exact creating domain")
        if self.operation == MULTIPLY:
            wire.same(self.parameters, [selected], "point conversion's complete multiplication parameters")
        self.point_target(native, selected, target, owner)
        return wire.Callable(source, target, lambda _, retained=(data, native.context, owner): retained[0])

    def field_callable(self, data, source, target):
        """Use the public curried interface of this process's actual field."""
        native, record_data, carrier = record_field(self.session, data)
        natural_source = wire.node("obj.sets.naturals")
        arguments = {
            "Monoid.toSemigroup": (carrier, carrier),
            "AddMonoid.toAddSemigroup": (carrier, carrier),
            "Monoid.toNPow": (natural_source, carrier),
            "AddMonoid.toNSMul": (natural_source, carrier),
            "Semiring.toNatCast": (natural_source,),
        }.get(native.field)
        if arguments is None or not callable(native.value):
            raise Unsupported("this record field has no native callable interface")

        def build(actual, remaining, operands):
            domain = remaining[0]
            codomain = carrier
            for argument in reversed(remaining[1:]):
                codomain = wire.node("obj.sets.maps", argument, codomain)
            points = NativePoints(self.session, self.packet, domain)

            def evaluate(point, retained=(data, record_data, operands, actual)):
                original, original_record, previous, function = retained
                value = points.read(self.resolve_value(point, domain))
                output = function(value)
                inputs = (*previous, point)
                context = FieldComputation(original, inputs, self.packet)
                if len(remaining) == 1:
                    return self.session.keep(output, self.packet, "Point.field", carrier, context)
                partial = build(output, remaining[1:], inputs)
                return self.session.keep(partial, self.packet, "Field.callable", carrier, context)

            return wire.Callable(domain, codomain, evaluate)

        result = build(native.value, arguments, ())
        wire.same(source, result.source, "native field's complete source")
        wire.same(target, result.target, "native field's complete target")
        return result

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
            self.check_element(selected, expression, target)
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

    def point_function(self, data, domain, target, owner=None):
        """Read a generalized point in its declared point-data position.

        Product arrays contain ordered component data here; raw arrays inside
        an explicit callable/typedMap body keep the finite-graph convention.
        """
        original, data = data, inline(data)
        if tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            self.check_element(selected, expression, target)
            if (not self.closed(domain) or self.callable_data(expression)
                    or tag(inline(expression)) in {"element", "operationExpression"}):
                actual = self.point_function(expression, domain, target, owner=selected)
                return wire.Callable(domain, target, lambda point, retained=(original, actual): retained[1](point))
            if tag(inline(expression)) == "opaqueData":
                try:
                    point_producer(self.session, expression)
                except Unsupported:
                    pass
                else:
                    return wire.Callable(domain, target,
                                         lambda _, retained=(original, expression): retained[1])
            if not isinstance(inline(expression), dict) and self.monoid_receivers(selected):
                return wire.Callable(domain, target,
                                     lambda _, retained=(original, expression): retained[1])
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
            return self.function(data, domain, target, owner=owner)
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

    def function(self, data, source, target, owner=None):
        data = inline(data)
        # Keep a typed body's callable position explicit, including raw graphs.
        if tag(data) == "typedMap":
            actual_source, actual_target, body = typed_map(data)
            wire.same(actual_source, source, "callable source")
            wire.same(actual_target, target, "callable target")
            actual = self.function(body, source, target, owner=owner)
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
            f, g = self.function(first, source, middle), self.function(second, middle, target, owner=owner)
            return wire.Callable(source, target, lambda point, retained=(data, f, g): retained[2](retained[1](point)))
        if tag(data) == "mediator":
            left, right = fields(data, "mediator", 2)
            a, b = self.product_factors(target, (left, right))
            f, g = self.function(left, source, a), self.function(right, source, b)
            return wire.Callable(source, target, lambda point, retained=(data, f, g):
                                 [retained[1](point), retained[2](point)])
        if tag(data) in {"point", "element", "operationExpression"}:
            return (self.function(fields(data, "point", 1)[0], source, target, owner=owner) if tag(data) == "point"
                    else self.point_function(data, source, target, owner=owner))
        if tag(data) == "opaqueData" and not isinstance(self.session.get(data).value, wire.Callable):
            if self.session.get(data).field in {"Monoid.toSemigroup", "AddMonoid.toAddSemigroup",
                                                "Monoid.toNPow", "AddMonoid.toNSMul", "Semiring.toNatCast"}:
                return self.field_callable(data, source, target)
            return self.point_callable(data, source, target, owner)
        try:
            return wire.framed_callable(data, source, target, self.native_values, self.interpret,
                                        finite_inventory=self.inventory, product_factors=self.product_factors)
        except wire.Unsupported as error:
            raise Unsupported(str(error)) from error

    def expression_function(self, expression, domain, target):
        from monoid_multiplication import Multiplication
        actual = Multiplication.at_expression(self.session, self.packet, expression, domain, target)
        return actual.expression_function(expression, domain, target)

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

    def finish(self, data, invocation):
        if self.operation == MULTIPLY and tag(inline(data)) == "opaqueData":
            native = self.session.get(data)
            if native.field in {"Monoid.product", "Point.result", "Point.value", "Point.field",
                                "AddMonoid.toZero", "Monoid.toOne"}:
                point_producer(self.session, data)
                return self.session.keep(native.value, self.packet, "Point.result", native.carrier,
                                         PointResult(invocation, data))
        return data if tag(data) in {"opaqueData", "valueData"} else value_data(data)

    def result_data(self, data):
        return data

    def run(self):
        self.selection(self.arrow)
        action = self.function(self.arrow, self.source, self.target)
        argument = self.point_function(self.argument, self.domain, self.source)
        retained = wire.Invocation(self.operation, self.parameters, self.packet, argument, action)
        if self.closed(self.domain):
            return self.finish(self.result_data(action(argument(self.inventory(self.domain)[0]))), retained)
        result = wire.Callable(self.domain, self.target,
                               lambda point: self.result_data(action(argument(point))), invocation=retained)
        token = self.session.keep(result, self.packet, self.result_field, self.target)
        return value_data(map_data(self.domain, self.target, token))
