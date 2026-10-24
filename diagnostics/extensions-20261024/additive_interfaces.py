"""The public additive-monoid operation and its selected carrier route.

Only explicitly selected ring/module additive groups use the existing native
decoders. Returned monoids retain the original group, native object and owner.
No additive structure is inferred from equality of underlying carriers.
"""

from dataclasses import dataclass

from cas_port import operation_expression, point_invocation
from engine import Module
from native_polynomial import build as polynomial_action
from wire import Callable, NativeIdentity, Unsupported, fields, key, node, same


@dataclass(frozen=True)
class AdditiveMonoid(Module):
    selected: object
    group: object
    original: object
    context: object


class AdditiveInterfaces:
    additive_functor = "fun.additive_groups.additive_monoid"
    additive_operation = "op.additive_monoids.add"
    additive_cell = "cell.additive_groups.carrier"

    def additive_group_native(self, selected):
        if self.tag(selected) == "valueData":
            return self.additive_group_native(fields(selected, "valueData", 1)[0])
        if self.tag(selected) == "functorAction":
            action, original = fields(selected, "functorAction", 2)
            if self.tag(action) == "fun.rings.additive_group":
                fields(action, "fun.rings.additive_group", 0)
                return self.regular_module(original), original
            if self.tag(action) == "fun.modules.additive_group":
                fields(action, "fun.modules.additive_group", 0)
                return self.module(original), original
        raise Unsupported("this selected additive group has no implemented native ring/module decoder")

    def additive_monoid_native(self, selected):
        tag = self.tag(selected)
        if tag == "valueData":
            return self.additive_monoid_native(fields(selected, tag, 1)[0])
        if tag == "opaqueData":
            actual = self.session.get(selected)
            if isinstance(actual, AdditiveMonoid):
                return actual
            raise Unsupported("the owned object is not a retained selected additive monoid")
        if tag == "functorAction":
            action, group = fields(selected, tag, 2)
            if self.tag(action) == self.additive_functor:
                fields(action, self.additive_functor, 0)
                actual, original = self.additive_group_native(group)
                context = {"selected": selected, "group": group, "original": original,
                           "nativeObject": actual}
                return AdditiveMonoid(actual.native, actual.read, actual.write,
                                      selected, group, original, context)
        raise Unsupported("this selected additive monoid has no implemented native additive decoder")

    def additive_monoid_object(self, parameters, receiver):
        same(parameters, [], "additive-group functor's complete declaration parameters")
        selected = node("functorAction", node(self.additive_functor), receiver)
        return self.session.keep(self.additive_monoid_native(selected))

    def polynomial_model(self, selected):
        if self.tag(selected) == "valueData":
            return self.polynomial_model(fields(selected, "valueData", 1)[0])
        if self.tag(selected) == "opaqueData":
            actual = self.session.get(selected)
            if isinstance(actual, AdditiveMonoid):
                return self.polynomial_model(actual.original)
        return super().polynomial_model(selected)

    def additive_value(self, data, selected, domain=None):
        """Read actual operand data, including complete released expressions."""
        actual = self.additive_monoid_native(selected)
        tag = self.tag(data)
        if tag == "valueData":
            return self.additive_value(fields(data, tag, 1)[0], selected, domain)
        if tag == "element":
            original, expression = fields(data, tag, 2)
            same(original, selected, "additive expression's complete selected monoid")
            return self.additive_value(expression, selected, domain)
        if tag == "operationExpression":
            operation, parameters, operands = operation_expression(data)
            if operation != self.additive_operation:
                raise Unsupported("this selected additive expression has no implemented operation")
            same(parameters, [selected], "additive expression's ordered parameters")
            if len(operands) != 2:
                raise ValueError("binary addition requires both actual operands")
            left, right = (self.additive_value(value, selected, domain) for value in operands)
            return left + right
        if tag in {"point", "pointView", "admittedPoint", "constrainedPoint", "compose", "typedMap"}:
            original_domain = domain if domain is not None else self.callable_domain(data)
            lowered = self.point(data, selected, original_domain)
            if key(lowered) == key(data):
                raise Unsupported("the additive operand has no supported complete point data")
            return actual.read(lowered)
        return actual.read(data)

    def point(self, data, target, domain):
        if self.tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            if self.tag(expression) == "operationExpression":
                operation, _, _ = operation_expression(expression)
                if operation == self.additive_operation:
                    actual = self.additive_monoid_native(selected)
                    return actual.write(self.additive_value(data, selected, domain))
        if self.tag(data) == "operationExpression":
            operation, parameters, _ = operation_expression(data)
            if operation == self.additive_operation:
                if len(parameters) != 1:
                    raise ValueError("addition omits or adds its selected additive monoid")
                actual = self.additive_monoid_native(parameters[0])
                return actual.write(self.additive_value(data, parameters[0], domain))
        return super().point(data, target, domain)

    def additive_carrier_routes(self, receiver):
        left = receiver
        for action in (node("fun.additive_groups.to_groups"), node("fun.groups.monoid"),
                       node("fun.monoids.semigroup"), node("classifierForget", "clf.magmas.associative", []),
                       node("classifierForget", "clf.sets.binary_operation", [])):
            left = node("functorAction", action, left)
        right = node("functorAction", node("fun.additive_monoids.underlying"),
                     node("functorAction", node(self.additive_functor), receiver))
        return left, right

    def interpret_arrow(self, arrow, source, target):
        tag = self.tag(arrow)
        if tag == self.additive_operation:
            selected, = fields(arrow, tag, 1)
            actual = self.additive_monoid_native(selected)
            context = {"arrow": arrow, "source": source, "target": target,
                       "selected": selected, "nativeObject": actual}
            native = None
            try:
                source_model, target_model = self.polynomial_model(source), self.polynomial_model(target)
            except Unsupported:
                pass
            else:
                native = polynomial_action(source_model, target_model,
                                           lambda value, _: value[0] + value[1], context)
            def add(pair, retained=context):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("binary addition requires both actual operands")
                left, right = (self.additive_value(value, retained["selected"]) for value in pair)
                return retained["nativeObject"].write(left + right)
            return Callable(source, target, add, native)
        if tag == "cellComponent":
            cell, parameters, receiver, inverse = fields(arrow, tag, 4)
            if cell == self.additive_cell:
                same(parameters, [], "additive carrier component's declaration parameters")
                if type(inverse) is not bool:
                    raise ValueError("the additive carrier component requires a Boolean orientation")
                actual, original = self.additive_group_native(receiver)
                left, right = self.additive_carrier_routes(receiver)
                expected_source, expected_target = (right, left) if inverse else (left, right)
                self.same_endpoint(source, expected_source, arrow, "source",
                                   "additive carrier component's complete source route")
                self.same_endpoint(target, expected_target, arrow, "target",
                                   "additive carrier component's complete target route")
                context = (arrow, receiver, actual, original, source, target)
                return Callable(source, target, lambda value, retained=context: value,
                                NativeIdentity(source, target))
        return super().interpret_arrow(arrow, source, target)

    def point_application(self, operation, packet):
        if operation == self.additive_cell + "#component":
            _, parameters, arrow, _, _, _, _ = point_invocation(packet, operation)
            if len(parameters) != 3 or not isinstance(parameters[0], list) or type(parameters[2]) is not bool:
                raise ValueError("the additive carrier invocation requires [declarationParameters,receiver,inverse]")
            same(parameters[0], [], "additive carrier invocation's declaration parameters")
            descriptor = self.declaration_data(arrow)
            if self.tag(descriptor) == "cellComponent":
                cell, declaration_parameters, receiver, inverse = fields(descriptor, "cellComponent", 4)
                same(cell, self.additive_cell, "additive carrier component identifier")
                same(parameters, [declaration_parameters, receiver, inverse],
                     "additive carrier invocation's complete nested parameters")
        return super().point_application(operation, packet)
