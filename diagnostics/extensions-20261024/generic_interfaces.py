"""The new generic public interfaces, backed by existing native computations.

Admissions retain their supplied original function; this module neither proves
nor tests a homomorphism law. Finite subset images use Sage sets and the actual
callable. The selected monoid's structural path controls its native operation.
"""

from dataclasses import dataclass

from sage.all import Set, Subsets, ZZ

from cas_port import admitted_point, map_data, object_field
from wire import Callable, NativeIdentity, Unsupported, fields, node, same
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

    def morphism_function(self, data, object_id, parameters, source, target):
        """Use the complete supplied function under its selected admission."""
        if len(parameters) != self.morphism_objects[object_id]:
            raise ValueError("the selected hom object omits or adds a declaration parameter")
        if self.tag(data) == "valueData":
            return self.morphism_function(fields(data, "valueData", 1)[0], object_id,
                                          parameters, source, target)
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
            return Callable(source, target, lambda point, context=retained: context[-1](point), actual.native)
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
        if self.tag(data) == "valueData":
            return self.finite_subset(fields(data, "valueData", 1)[0], ambient, context)
        if self.tag(data) == "opaqueData":
            actual = self.session.get(data)
            if not isinstance(actual, FiniteSubset):
                raise Unsupported("the owned subset has no supported complete finite representation")
            same(actual.ambient, ambient, "owned finite subset's complete ambient selection")
            return actual
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
                                actual_family.native)
        if tag in applications:
            object_id = applications[tag]
            parameters = fields(arrow, tag, self.morphism_objects[object_id])
            hom_object, argument_source = fields(source, "objectProduct", 2)
            same(hom_object, node(object_id, *parameters), "application's complete selected hom object")
            def apply(pair):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("a morphism application requires its actual function and argument")
                actual = self.morphism_function(pair[0], object_id, parameters, argument_source, target)
                return actual(pair[1])
            return Callable(source, target, apply)
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
            same(source, node("obj.sets.power_set", ambient_source), "direct-image power source")
            same(target, node("obj.sets.power_set", ambient_target), "direct-image power target")
            actual = self.function(actual_map, ambient_source, ambient_target)
            def direct_image(data):
                subset = self.finite_subset(data, ambient_source)
                context = {"arrow": arrow, "source": source, "target": target,
                           "actualFunction": actual, "actualSubset": subset}
                image = self.finite_subset([actual(point) for point in subset.points], ambient_target, context)
                return self.session.keep(image)
            return Callable(source, target, direct_image)
        if tag in {"op.monoids.mul", "op.monoids.one"}:
            selected, = fields(arrow, tag, 1)
            multiply, unit, model = self.monoid_operations(selected)
            context = {"arrow": arrow, "source": source, "target": target,
                       "selectedMonoid": selected, "multiply": multiply,
                       "unit": unit, "nativeModel": model}
            if tag == "op.monoids.one":
                return Callable(source, target, lambda _, retained=context: retained["unit"]())
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
                return retained["multiply"](pair[0], pair[1])
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
