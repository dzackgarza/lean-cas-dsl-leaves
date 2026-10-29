"""The new generic public interfaces, backed by existing native computations.

Admissions retain their supplied original function; this module neither proves
nor tests a homomorphism law. Finite subset images use Sage sets and the actual
callable. The selected monoid's structural path controls its native operation.
"""

from dataclasses import dataclass

from sage.all import Set, Subsets, ZZ

from cas_port import admitted_point, map_data, object_field, operation_expression
from wire import (Callable, NativeIdentity, Unsupported, fields, inventory, key,
                  node, public_data, same)
from native_polynomial import build as polynomial_action


@dataclass(frozen=True)
class FiniteSubset:
    ambient: object
    points: tuple
    native: object
    context: object


class GenericInterfaces:
    morphism_objects = {"obj.sets.group_morphisms": 2,
                        "obj.sets.module_morphisms": 3}

    def operation_point_callable(self, data):
        """Consume the supported nullary point's actual source comparison."""
        operation, parameters, comparison, domain, selected = fields(data, "operationPoint", 5)
        if not isinstance(operation, str) or not operation or not isinstance(parameters, list):
            raise ValueError("a nullary point requires its operation and ordered parameters")
        if operation != "op.monoids.one":
            if operation in {"op.monoids.mul", "op.groups.inverse", "op.additive_monoids.add"} | self.ring_operations:
                raise ValueError("operationPoint requires a nullary operation")
            raise Unsupported("this nullary operation has no implemented point adapter")
        if len(parameters) != 1:
            raise ValueError("the nullary monoid point requires its complete selected monoid")
        same(parameters[0], selected, "nullary point's complete selected structure")
        if isinstance(comparison, list) or self.tag(comparison) == "finiteGraph":
            # The operation's published categorical source is Fin(1); the
            # supplied graph still provides every actual comparison value.
            source = node("obj.sets.fin", 1)
        else:
            source = self.component_endpoint(comparison, "target")
        actual = self.function(comparison, domain, source)
        action = self.function(node(operation, *parameters), source, selected)
        context = (data, actual, action)
        return Callable(domain, selected,
                        lambda point, retained=context: retained[2](retained[1](point)),
                        point_action=lambda point, read: action.at_point(actual.at_point(point, read), read))

    def point(self, data, target, domain):
        tag = self.tag(data)
        if tag == "element":
            selected, expression = fields(data, tag, 2)
            self.check_element_target(target, selected)
            expression_tag = self.tag(expression)
            if expression_tag == "operationPoint":
                return self.point(expression, target, domain)
            if expression_tag == "operationExpression":
                operation, _, _ = operation_expression(expression)
                if operation in {"op.monoids.mul", "op.monoids.one", "op.groups.inverse"}:
                    return self.point(expression, target, domain)
            if expression_tag == "mul":
                try:
                    self.monoid_operations(selected)
                except Unsupported:
                    pass
                else:
                    operands = fields(expression, "mul", 2)
                    return self.point(node("operationExpression", "op.monoids.mul", [selected], operands),
                                      target, domain)
        if tag == "operationPoint":
            actual = self.operation_point_callable(data)
            self.check_structure_target(target, actual.target)
            if domain is not None:
                same(actual.source, domain, "nullary point's original generalized domain")
            if not self.closed_domain(actual.source):
                raise Unsupported("a non-global nullary point retains its original callable domain")
            return actual.at_point(inventory(actual.source)[0],
                                   lambda point, selected: self.point(point, selected, actual.source))
        if tag == "operationExpression":
            operation, parameters, operands = operation_expression(data)
            if operation in {"op.monoids.mul", "op.monoids.one", "op.groups.inverse"}:
                if len(parameters) != 1:
                    raise ValueError("the operation expression omits its complete selected structure")
                arity = {"op.monoids.mul": 2, "op.monoids.one": 0, "op.groups.inverse": 1}[operation]
                if len(operands) != arity:
                    raise ValueError("the operation expression has a different operand count")
                selected = parameters[0]
                self.check_structure_target(target, selected)
                values = [self.point(value, target, domain) for value in operands]
                if operation == "op.groups.inverse":
                    return self.function(node(operation, selected), selected, selected)(values[0])
                multiply, unit, _ = self.monoid_operations(selected)
                return unit() if arity == 0 else multiply(*values)
        return super().point(data, target, domain)

    def morphism_function(self, data, object_id, parameters, source, target, read=None):
        """Use the complete supplied function under its selected admission."""
        if len(parameters) != self.morphism_objects[object_id]:
            raise ValueError("the selected hom object omits or adds a declaration parameter")
        if self.tag(data) == "valueData":
            return self.morphism_function(fields(data, "valueData", 1)[0], object_id,
                                          parameters, source, target, read)
        if self.tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            same(selected, node(object_id, *parameters), "function-valued point's selected hom object")
            return self.morphism_function(expression, object_id, parameters, source, target, read)
        if self.tag(data) == "point":
            selected = node(object_id, *parameters)
            actual = read(data, selected) if read is not None else self.point(data, selected, None)
            return self.morphism_function(actual, object_id, parameters, source, target, read)
        if self.tag(data) == "admittedPoint":
            selected_id, selected_parameters, domain, original_type, admitted, original = admitted_point(data)
            if selected_id != object_id:
                raise ValueError("the admitted morphism changes its selected hom-object declaration")
            same(selected_parameters, parameters, "admitted morphism's complete selection")
            same(admitted, node(object_id, *parameters), "admitted morphism's selected hom object")
            actual_source, actual_target = fields(original_type, "obj.sets.maps", 2)
            same(actual_source, source, "admitted function's original source")
            same(actual_target, target, "admitted function's original target")
            actual = self.function(original, actual_source, actual_target)
            retained = (object_id, parameters, domain, original_type, admitted, original, actual)
            return Callable(source, target, lambda point, context=retained: context[-1](point), actual.native,
                            point_action=actual.at_point)
        return self.function(data, source, target)

    def subset_key(self, point, ambient):
        """Lower a supported point to its existing exact native hashable value."""
        tag = self.tag(ambient)
        if tag == "objectProduct":
            left, right = fields(ambient, tag, 2)
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError("a product-valued subset point omits a component")
            return (self.subset_key(point[0], left), self.subset_key(point[1], right))
        if tag == "obj.sets.naturals":
            fields(ambient, tag, 0)
            return ZZ(self.natural(point, "a natural-number subset point"))
        try:
            self.ring(ambient)
        except Unsupported:
            pass
        else:
            return self.scalar(point, ambient)
        try:
            self.cyclic_context(ambient)
        except Unsupported:
            pass
        else:
            return self.cyclic_point(point, ambient)
        try:
            module = self.module(ambient)
        except Unsupported:
            pass
        else:
            value = module.read(point)
            try:
                hash(value)
            except TypeError:
                return tuple(value)
            return value
        if tag == "obj.sets.truth_values":
            if type(point) is not bool:
                raise ValueError("a truth-valued subset point is not Boolean")
            return point
        try:
            group = self.aut_context(ambient)
        except Unsupported:
            pass
        else:
            actual = self.automorphism(point, group.category, group.receiver)
            try:
                hash(actual.native_forward)
                hash(actual.native_backward)
            except (TypeError, ValueError, NotImplementedError) as error:
                raise Unsupported("this native automorphism has no supported finite-set key") from error
            return (actual.native_forward, actual.native_backward)
        finite = self.finite_object(ambient)
        return self.point_index(point, finite.points, ambient)

    def finite_subset(self, data, ambient, context=None):
        public_data([data, ambient], self.session)
        if self.tag(data) == "valueData":
            return self.finite_subset(fields(data, "valueData", 1)[0], ambient, context)
        if self.tag(data) == "opaqueData":
            actual = self.session.get(data)
            if not isinstance(actual, FiniteSubset):
                raise Unsupported("the owned subset has no supported complete finite representation")
            same(actual.ambient, ambient, "owned finite subset's complete ambient selection")
            return actual
        if self.tag(data) in {"element", "point", "powerObjectMap", "compose", "typedMap"}:
            actual = self.point(data, node("obj.sets.power_set", ambient), node("obj.sets.fin", 1))
            if key(actual) == key(data):
                raise Unsupported("the selected subset point has no implemented callable reader")
            return self.finite_subset(actual, ambient, {"point": data, "context": context})
        if not isinstance(data, list):
            raise Unsupported("this subset has no complete supported finite representation")
        keys = [self.subset_key(point, ambient) for point in data]
        native = Set(keys)
        # Dict insertion order only chooses representatives for equal native
        # points. Sage's complete native set remains the comparison data.
        representatives = dict(zip(keys, data))
        return FiniteSubset(ambient, tuple(representatives.values()), native,
                            {"selection": ambient, "input": data, "context": context})

    def power_inventory(self, ambient):
        finite = self.finite_object(ambient)
        return tuple([finite.points[int(index)] for index in sorted(subset)]
                     for subset in Subsets(range(len(finite.points))))

    def monoid_operations(self, selected):
        """Read the actual supported selected monoid, without erasing its law."""
        tag = self.tag(selected)
        if tag == "valueData":
            return self.monoid_operations(fields(selected, tag, 1)[0])
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            atag = self.tag(action)
            if atag == "fun.rings.multiplicative_monoid":
                fields(action, atag, 0)
                native = self.ring(receiver)
                return (lambda left, right: self.encode_scalar(
                            self.scalar(left, receiver) * self.scalar(right, receiver), receiver),
                        lambda: self.encode_scalar(native.one(), receiver), "scalar_multiplication")
            if atag == "fun.groups.monoid":
                fields(action, atag, 0)
                return self.group_monoid_operations(receiver)
        return self.group_monoid_operations(selected)

    def group_monoid_operations(self, selected):
        if self.tag(selected) == "functorAction":
            action, receiver = fields(selected, "functorAction", 2)
            if self.tag(action) == "fun.additive_groups.to_groups":
                fields(action, "fun.additive_groups.to_groups", 0)
                additive_action, original = fields(receiver, "functorAction", 2)
                if self.tag(additive_action) == "fun.rings.additive_group":
                    fields(additive_action, "fun.rings.additive_group", 0)
                    native = self.ring(original)
                    return (lambda left, right: self.encode_scalar(
                                self.scalar(left, original) + self.scalar(right, original), original),
                            lambda: self.encode_scalar(native.zero(), original), "scalar_addition")
                if self.tag(additive_action) == "fun.modules.additive_group":
                    fields(additive_action, "fun.modules.additive_group", 0)
                    actual = self.module(original)
                    return actual.add, actual.zero, "module_addition"
                raise Unsupported("this selected additive-group carrier has no native monoid adapter")
        try:
            self.cyclic_context(selected)
        except Unsupported:
            pass
        else:
            return (lambda left, right: self.encode_cyclic(
                        self.cyclic_point(left, selected) + self.cyclic_point(right, selected), selected),
                    lambda: self.encode_cyclic(0, selected), "cyclic_addition")
        try:
            group = self.aut_context(selected)
        except Unsupported:
            pass
        else:
            def multiply(left, right):
                a = self.automorphism(left, group.category, group.receiver)
                b = self.automorphism(right, group.category, group.receiver)
                # The public generic AutomorphismArrows.forward_mul convention
                # is (a*b)(x)=a(b(x)); categorical composition is first b, then a.
                forward = self.postcompose(b.forward, a.forward)
                backward = self.postcompose(a.backward, b.backward)
                return self.session.keep(self.make_automorphism(group.category, group.receiver,
                                                                forward, backward))
            def unit():
                actual = Callable(group.receiver, group.receiver, lambda point: point,
                                  NativeIdentity(group.receiver, group.receiver))
                return self.session.keep(self.make_automorphism(group.category, group.receiver,
                                                                actual, actual))
            return multiply, unit, "native_automorphism_composition"
        raise Unsupported("this selected monoid has no implemented native multiplication and unit")

    def interpret_arrow(self, arrow, source, target):
        tag = self.tag(arrow)
        if tag == "operationPoint":
            actual = self.operation_point_callable(arrow)
            same(actual.source, source, "nullary callable's original generalized domain")
            same(actual.target, target, "nullary callable's complete selected target")
            return actual
        applications = {identifier + "#application": identifier
                        for identifier in self.morphism_objects}
        if tag == "admittedPoint":
            object_id, parameters, domain, original_type, admitted, original = admitted_point(arrow)
            if object_id in self.morphism_objects:
                if len(parameters) != self.morphism_objects[object_id]:
                    raise ValueError("the admitted family omits a complete hom-object parameter")
                same(domain, source, "admitted function family's original domain")
                same(admitted, target, "admitted function family's selected target")
                same(admitted, node(object_id, *parameters), "admitted family's hom-object selection")
                if self.closed_domain(domain) and not self.callable_argument(original, domain, original_type):
                    return Callable(source, target,
                                    lambda _: self.point(original, original_type, domain))
                actual_family = self.function(original, domain, original_type)
                retained = (arrow, actual_family)
                return Callable(source, target, lambda point, context=retained: context[1](point),
                                actual_family.native, point_action=actual_family.at_point)
        if tag in applications:
            object_id = applications[tag]
            parameters = fields(arrow, tag, self.morphism_objects[object_id])
            hom_object, argument_source = self.product_factors(source)
            same(hom_object, node(object_id, *parameters), "application's complete selected hom object")
            if self.tag(source) == "morphismEndpoint":
                self.same_endpoint(source, None, arrow, "source", "application's complete source")
            argument_target = target
            if self.tag(target) == "morphismEndpoint":
                self.same_endpoint(target, None, arrow, "target", "application's complete target")
                argument_target = parameters[-1]
            def apply_point(pair, read):
                pair = self.product_point(pair, source, read)
                actual = self.morphism_function(pair[0], object_id, parameters, argument_source, argument_target, read)
                return actual.at_point(pair[1], read)
            def apply(pair):
                return apply_point(pair, lambda point, selected: self.point(point, selected, None))
            return Callable(source, target, apply, point_action=apply_point)
        if tag == "objectField":
            object_id, selector, parameters = object_field(arrow)
            if object_id in self.morphism_objects and selector == "inclusion":
                same(source, node(object_id, *parameters), "hom inclusion's complete selected source")
                actual_source, actual_target = fields(target, "obj.sets.maps", 2)
                def include(data):
                    actual = self.morphism_function(data, object_id, parameters, actual_source, actual_target)
                    return map_data(actual.source, actual.target, self.session.keep(actual))
                return Callable(source, target, include)
        if tag == "mor.sets.direct_image":
            ambient_source, ambient_target, actual_map = fields(arrow, tag, 3)
            self.same_endpoint(source, node("obj.sets.power_set", ambient_source),
                               arrow, "source", "direct-image power source")
            self.same_endpoint(target, node("obj.sets.power_set", ambient_target),
                               arrow, "target", "direct-image power target")
            actual = self.function(actual_map, ambient_source, ambient_target)
            def direct_image(data):
                subset = self.finite_subset(data, ambient_source)
                context = {"arrow": arrow, "source": source, "target": target,
                           "actualFunction": actual, "actualSubset": subset}
                image = self.finite_subset([actual.at_point(point, lambda value, selected: self.point(value, selected, None))
                                           for point in subset.points], ambient_target, context)
                return self.session.keep(image)
            return Callable(source, target, direct_image)
        if tag in {"op.monoids.mul", "op.monoids.one"}:
            selected, = fields(arrow, tag, 1)
            multiply, unit, model = self.monoid_operations(selected)
            context = {"arrow": arrow, "source": source, "target": target,
                       "selectedMonoid": selected, "multiply": multiply,
                       "unit": unit, "nativeModel": model}
            if tag == "op.monoids.one":
                def identity_point(point, retained=context):
                    # The published operation has Fin(1) as its categorical
                    # source. Consume the comparison's actual image; do not
                    # invent a replacement terminal point or domain.
                    self.finite_ordinal(point, 1)
                    return retained["unit"]()
                return Callable(source, target, identity_point)
            native = None
            if model in {"scalar_multiplication", "scalar_addition"}:
                try:
                    source_model, target_model = self.polynomial_model(source), self.polynomial_model(target)
                except Unsupported:
                    pass
                else:
                    def symbolic(value, coefficients):
                        return value[0] * value[1] if model == "scalar_multiplication" else value[0] + value[1]
                    native = polynomial_action(source_model, target_model, symbolic, context)
            def multiplication(pair, retained=context):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("monoid multiplication requires both actual operands")
                left, right = (self.point(value, retained["selectedMonoid"], None) for value in pair)
                return retained["multiply"](left, right)
            return Callable(source, target, multiplication, native)
        return super().interpret_arrow(arrow, source, target)

    def equal(self, left, right, selected):
        tag = self.tag(selected)
        if tag == "obj.sets.power_set":
            ambient, = fields(selected, tag, 1)
            return bool(self.finite_subset(left, ambient).native == self.finite_subset(right, ambient).native)
        if tag in self.morphism_objects:
            parameters = fields(selected, tag, self.morphism_objects[tag])
            source, target = parameters[-2:]
            f = self.morphism_function(left, tag, parameters, source, target)
            g = self.morphism_function(right, tag, parameters, source, target)
            return self.equal(self.session.keep(f), self.session.keep(g), node("obj.sets.maps", source, target))
        return super().equal(left, right, selected)
