"""Finite objects, selected core actions, scalar restriction and lazy series.

This module uses only the public declaration interfaces recorded by the specimen.
Selected category and functor dictionaries stay explicit at every construction.
"""

from dataclasses import dataclass, replace

from sage.all import (QQ, ZZ, IntegerModRing, LazyPowerSeriesRing, Set, Subsets,
                      SymmetricGroup, identity_matrix, matrix, vector)
from sage.libs.gap.libgap import libgap
from sage.sets.finite_set_maps import FiniteSetMaps

from cas_port import (admitted_point, cartesian_map, category_parameter, constructed_category,
                      construction_invocation, core_iso, core_object,
                      functor_parameter, map_data, method_invocation, morphism_endpoint, object_field,
                      presentation_invocation, structured_projection_action, typed_map)
from engine import Engine, Form, Module, RingImage, Scalar, Q, Z
from wire import (Callable, NativeComposition, NativeIdentity, NativeMediator,
                  Unsupported, fields, framed_callable, inventory, key, node, public_data, same)
from native_linear import LinearAction, degree, identity, zero
from native_polynomial import build as polynomial_action
from generic_interfaces import GenericInterfaces
from additive_interfaces import AdditiveInterfaces
from power_interfaces import PowerObjectInterfaces
from module_functor_interfaces import ModuleImage
from carrier_functor_interfaces import CarrierFunctorInterfaces


@dataclass(frozen=True)
class FiniteObject:
    selected: object
    points: tuple
    native: object


@dataclass(frozen=True)
class CyclicPoint:
    selected: object
    modulus: int
    native: object


@dataclass(frozen=True)
class AutomorphismGroup:
    category: object
    receiver: object
    points: tuple
    native: object


@dataclass(frozen=True)
class Automorphism:
    category: object
    receiver: object
    forward: Callable
    backward: Callable
    native_forward: object
    native_backward: object


@dataclass(frozen=True)
class Series:
    coefficient: object
    native: object
    context: object


@dataclass(frozen=True)
class SuccessorFamily:
    """Native family metadata supplied only by the declared full term action."""

    coefficient: object
    index: object
    context: object


@dataclass(frozen=True)
class RegularModule(Module):
    coefficient: object
    context: object


@dataclass(frozen=True)
class RestrictedModule(Module):
    original: object
    base_map: object
    source_ring: object
    target_ring: object
    transport: object
    context: object

    def scale(self, scalar, value):
        encoded = self.transport.encode_scalar(scalar, self.source_ring)
        mapped = self.base_map(encoded)
        native_scalar = self.transport.scalar(mapped, self.target_ring)
        return self.original.scale(native_scalar, value)


class ExtensionEngine(CarrierFunctorInterfaces, PowerObjectInterfaces, AdditiveInterfaces, GenericInterfaces, Engine):
    modular_ids = {"obj.sets.integers_mod", "obj.rings.integers_mod", "obj.commutative_rings.integers_mod"}
    quotient_ids = {"obj.sets.cyclic_quotient", "obj.groups.cyclic_quotient"}
    cyclic_ids = {"obj.groups.cyclic"}
    comparisons = {Engine.comparison, "cmp.sets.fin_reversal", "cmp.groups.cyclic_quotient_residue",
                   "cmp.sets.singleton_terminal"}
    object_operations = {"con.automorphisms", "fun.core_sets.automorphisms", "fun.core_groups.automorphisms",
                         "fun.core_sets.two_subsets", "meth.two_subsets", "meth.cardinality",
                         "fun.modules.reindex", "lim.sets.product", "fun.arrows_modules.kernel",
                         "meth.kernel", "meth.arrow_ker", "fun.additive_groups.additive_monoid",
                         "fun.commutative_rings.ring", "fun.modules.fibre_inclusion",
                         "fun.modules.underlying"} | CarrierFunctorInterfaces.module_action_operations

    def ring(self, selected):
        if self.tag(selected) in self.modular_ids:
            modulus, = fields(selected, self.tag(selected), 1)
            return IntegerModRing(self.natural(modulus, "the selected modulus"))
        return super().ring(selected)

    def scalar(self, data, selected, domain=None):
        parent = self.ring(selected)
        if parent is not QQ and parent is not ZZ and parent not in (self.dual_x, self.dual_y):
            if type(data) is int:
                if data < 0 or data >= int(parent.cardinality()):
                    raise ValueError("a modular literal is outside its selected canonical range")
                return parent(data)
        return super().scalar(data, selected, domain)

    def encode_scalar(self, value, selected):
        parent = self.ring(selected)
        if parent is not QQ and parent is not ZZ and parent not in (self.dual_x, self.dual_y):
            return int(parent(value))
        return super().encode_scalar(value, selected)

    def underlying_receiver(self, selected):
        tag = self.tag(selected)
        if tag == "valueData":
            return self.underlying_receiver(fields(selected, tag, 1)[0])
        if tag == "finiteData":
            original, _ = fields(selected, tag, 2)
            inventory(selected)
            return self.underlying_receiver(original)
        if tag == "morphismEndpoint":
            try:
                return self.underlying_receiver(self.endpoint_view(selected))
            except Unsupported:
                return selected
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            atag = self.tag(action)
            if self.carrier_action(action):
                return self.underlying_receiver(receiver)
        return selected

    def cyclic_context(self, selected):
        original = self.underlying_receiver(selected)
        tag = self.tag(original)
        if tag in self.quotient_ids | self.cyclic_ids:
            modulus, = fields(original, tag, 1)
            self.natural(modulus, "the selected cyclic modulus")
            return modulus, tag in self.quotient_ids
        raise Unsupported("the selected group is not a supported cyclic presentation")

    def cyclic_point(self, data, selected):
        modulus, quotient = self.cyclic_context(selected)
        ring = IntegerModRing(modulus)
        tag = self.tag(data)
        if tag == "valueData":
            return self.cyclic_point(fields(data, tag, 1)[0], selected)
        if tag == "opaqueData":
            value = self.session.get(data)
            if not isinstance(value, CyclicPoint):
                raise ValueError("the owned point is not a cyclic-group element")
            old_modulus, old_quotient = self.cyclic_context(value.selected)
            if (old_modulus, old_quotient) != (modulus, quotient):
                raise ValueError("the cyclic point has a different selected quotient presentation")
            return value.native
        if tag == "element":
            original, expression = fields(data, tag, 2)
            if self.cyclic_context(original) != (modulus, quotient):
                raise ValueError("the cyclic expression changes its selected group")
            return self.cyclic_expression(expression, original)
        if tag == "pointView":
            actual, original, _ = fields(data, tag, 3)
            same(actual, selected, "cyclic point-view target")
            return self.cyclic_point(original, fields(original, "element", 2)[0])
        if not quotient and type(data) is int and (modulus == 0 or 0 <= data < modulus):
            return ring(data)
        raise Unsupported("the selected quotient point needs its published map or owned data")

    def cyclic_expression(self, expression, selected):
        modulus, _ = self.cyclic_context(selected)
        tag = self.tag(expression)
        if tag == "generator":
            fields(expression, tag, 0)
            return IntegerModRing(modulus)(1)
        if tag == "mul":
            left, right = fields(expression, tag, 2)
            return self.cyclic_expression(left, selected) + self.cyclic_expression(right, selected)
        if tag == "operationExpression":
            operation, parameters, operands = fields(expression, tag, 3)
            if operation == "op.groups.inverse" and len(parameters) == 1 and len(operands) == 1:
                same(parameters[0], selected, "cyclic inverse selection")
                return -self.cyclic_expression(operands[0], selected)
        raise Unsupported("this cyclic-group point expression is outside the specimen")

    def encode_cyclic(self, value, selected):
        modulus, quotient = self.cyclic_context(selected)
        native = IntegerModRing(modulus)(value)
        retained = selected
        while self.tag(retained) == "valueData":
            retained = fields(retained, "valueData", 1)[0]
        if self.tag(retained) == "finiteData":
            # Keep the actual supplied point keys, including their tokens.
            # A new token for the same native coordinate is a different graph
            # key and cannot replace this retained finite-data interface.
            for point in inventory(retained):
                if self.cyclic_point(point, selected) == native:
                    return point
            raise ValueError("the cyclic result is absent from the supplied point inventory")
        return self.session.keep(CyclicPoint(selected, modulus, native)) if quotient else int(native)

    def finite_object(self, selected):
        tag = self.tag(selected)
        if tag == "valueData":
            return self.finite_object(fields(selected, tag, 1)[0])
        if tag == "morphismEndpoint":
            # Read an existing callable's native endpoint without changing the
            # public descriptor. Graph inputs still need their own inventory.
            return self.finite_object(self.endpoint_view(selected))
        if tag in {"constructionApex", "constructionField"}:
            return self.finite_object(self.project_field(selected))
        if tag == "opaqueData":
            value = self.session.get(selected)
            if isinstance(value, FiniteObject):
                return value
            if isinstance(value, Module):
                return self.finite_module_object(selected, value)
            if isinstance(value, RingImage):
                try:
                    points = self.retained_point_inventory(selected)
                except Unsupported:
                    if not value.native.is_finite():
                        raise Unsupported("the retained native ring has an infinite carrier")
                    points = tuple(self.encode_scalar(point, selected) for point in value.native)
                return FiniteObject(selected, tuple(points), Set(range(len(points))))
            if isinstance(value, AutomorphismGroup):
                return self.finite_automorphism_object(selected, value)
        try:
            points = inventory(selected)
        except Unsupported:
            points = None
        if points is not None:
            return FiniteObject(selected, tuple(points), Set(range(len(points))))
        if tag in self.modular_ids:
            native = self.ring(selected)
            if not native.is_finite():
                raise Unsupported("the selected zero-modulus ring has an infinite carrier")
            points = tuple(self.encode_scalar(value, selected) for value in native)
        elif tag in {"obj.modules.regular", "obj.modules_r.restricted_regular",
                     "obj.modules.vectors", "obj.sets.vectors"}:
            return self.finite_module_object(selected, self.module(selected))
        elif tag == "obj.sets.terminal":
            fields(selected, tag, 0)
            # The public exposed type is PUnit: its nullary record has no
            # data fields. This is its codec, not a substituted Fin(1) point.
            points = ([],)
        elif tag == "obj.sets.truth_values":
            fields(selected, tag, 0)
            points = (False, True)
        elif tag in {"obj.finite_sets.fin", "obj.linear_orders.fin_ordinary", "obj.linear_orders.fin_reverse"}:
            n, = fields(selected, tag, 1)
            points = tuple(range(self.natural(n, "the selected finite order")))
        elif tag in {"obj.sets.integer_square_bound", "obj.finite_sets.integer_square_bound"}:
            radius, = fields(selected, tag, 1)
            radius = self.natural(radius, "the selected square-bound radius")
            points = tuple(int(x) for x in ZZ.range(-radius, radius + 1))
        elif tag == "obj.sets.two_subsets":
            receiver, = fields(selected, tag, 1)
            original = self.finite_object(receiver)
            pairs = Subsets(range(len(original.points)), 2)
            points = tuple([original.points[int(i)] for i in sorted(pair)] for pair in pairs)
        elif tag == "obj.sets.power_set":
            ambient, = fields(selected, tag, 1)
            points = self.power_inventory(ambient)
        elif tag == "coreObject":
            return self.finite_object(core_object(selected))
        elif tag == "objectProduct":
            left, right = fields(selected, tag, 2)
            x, y = self.finite_object(left), self.finite_object(right)
            points = tuple([a, b] for a in x.points for b in y.points)
        elif tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            if self.tag(action) in {"con.automorphisms", "fun.core_sets.automorphisms", "fun.core_groups.automorphisms"}:
                return self.finite_automorphism_object(selected, self.aut_context(selected))
            if self.tag(action) == "fun.modules.reindex":
                return self.finite_module_object(selected, self.module(selected))
            elif self.tag(action) == "fun.core_sets.two_subsets":
                fields(action, self.tag(action), 0)
                original = self.finite_object(core_object(receiver))
                points = tuple([original.points[int(i)] for i in sorted(pair)]
                               for pair in Subsets(range(len(original.points)), 2))
            else:
                underlying = self.underlying_receiver(selected)
                if key(underlying) == key(selected):
                    raise Unsupported("this selected finite action is outside the specimen")
                return self.finite_object(underlying)
        elif tag == "extent":
            power, ambient, subset = fields(selected, tag, 3)
            if power != "pow.sets":
                raise Unsupported("this selected power-object extent is outside the specimen")
            points = self.finite_subset(subset, ambient, selected).points
        else:
            try:
                context = self.aut_context(selected)
            except Unsupported:
                modulus, quotient = self.cyclic_context(selected)
                if modulus == 0:
                    raise Unsupported("the zero-modulus quotient has an infinite carrier")
                points = tuple(self.encode_cyclic(k, selected) for k in range(modulus))
            else:
                return self.finite_automorphism_object(selected, context)
        if len({key(point) for point in points}) != len(points):
            raise ValueError("the supplied finite object repeats a point")
        return FiniteObject(selected, tuple(points), Set(range(len(points))))

    def finite_module_object(self, selected, native_module):
        if not native_module.native.is_finite():
            raise Unsupported("the actual native module has an infinite carrier")
        points = tuple(native_module.write(value) for value in native_module.native)
        return FiniteObject(selected, points, Set(range(len(points))))

    def finite_automorphism_object(self, selected, context):
        """Enumerate the actual native finite group, retaining every direction."""
        points = []
        if self.category(context.category) == "cat.sets":
            for native_forward in context.native:
                native_backward = native_forward.inverse()
                def action(native):
                    return Callable(context.receiver, context.receiver,
                                    lambda point: context.points[int(native(self.point_index(
                                        point, context.points, context.receiver) + 1)) - 1])
                forward, backward = action(native_forward), action(native_backward)
                points.append(self.session.keep(Automorphism(context.category, context.receiver,
                                                             forward, backward, native_forward, native_backward)))
        else:
            modulus, _ = self.cyclic_context(context.receiver)
            for native_forward in libgap.Elements(context.native):
                native_backward = native_forward ** -1
                group = libgap.Source(native_forward)
                generator = group.GeneratorsOfGroup()[0] if modulus > 1 else group.One()
                elements = libgap([generator ** index for index in range(modulus)])
                def action(native, elements=elements):
                    def evaluate(point):
                        index = int(self.cyclic_point(point, context.receiver))
                        image = libgap.Image(native, elements[index])
                        coordinate = int(libgap.Position(elements, image)) - 1
                        return self.encode_cyclic(coordinate, context.receiver)
                    return Callable(context.receiver, context.receiver, evaluate)
                forward, backward = action(native_forward), action(native_backward)
                points.append(self.session.keep(Automorphism(context.category, context.receiver,
                                                             forward, backward, native_forward, native_backward)))
        return FiniteObject(selected, tuple(points), Set(range(len(points))))

    def function(self, data, source, target):
        public_data([data, source, target], self.session)
        def supplied_inventory(selected):
            if self.uninventoried_endpoint(selected):
                raise Unsupported("a declared endpoint needs its supplied finiteData inventory for a graph")
            return self.finite_object(selected).points
        return framed_callable(data, source, target, self.session, self.interpret_arrow,
                               supplied_inventory, self.product_factors,
                               lambda value, selected: self.point(value, selected, None))

    def category_descriptor(self, descriptor):
        """Check public descriptor framing without erasing a selected category.

        The caller owns dependent typing and category laws. These signatures are
        the seven public constructor argument grammars, not semantic aliases.
        """
        if self.tag(descriptor) == "category":
            category_id, parameters = category_parameter(descriptor)
            if category_id in {"cat.sets", "cat.groups"} and parameters:
                raise ValueError("the selected Sets or Groups dictionary has no explicit parameters")
            return descriptor
        constructor, arguments = constructed_category(descriptor)
        signatures = {
            "ctor.arrow": ("category",), "ctor.core": ("category",),
            "ctor.subobjects": ("category",),
            "ctor.slice": ("category", "object"),
            "ctor.coslice": ("category", "object"),
            "ctor.elements": ("category", "functor"),
            "ctor.functor_category": ("category", "category"),
        }
        if constructor not in signatures:
            raise Unsupported("the selected category constructor is not implemented: " + constructor)
        signature = signatures[constructor]
        if len(arguments) != len(signature):
            raise ValueError("the constructed category omits or adds a declaration parameter")
        for kind, argument in zip(signature, arguments):
            if kind == "category":
                self.category_descriptor(argument)
            elif kind == "functor":
                functor_parameter(argument)
            elif not isinstance(argument, dict) or not isinstance(argument.get("ctor"), str):
                raise ValueError("the constructed category omits its complete selected object")
        return descriptor

    def category(self, descriptor):
        self.category_descriptor(descriptor)
        if self.tag(descriptor) == "constructedCategory":
            constructor, _ = constructed_category(descriptor)
            raise Unsupported("native automorphisms for the complete selected category wrapper are not implemented: " + constructor)
        category_id, parameters = category_parameter(descriptor)
        if parameters or category_id not in {"cat.sets", "cat.groups"}:
            raise Unsupported("this exact selected category is outside the finite Aut implementation")
        return category_id

    def automorphism_group(self, category, receiver):
        category_id = self.category(category)
        if category_id == "cat.sets":
            points = self.finite_object(receiver).points
            native = SymmetricGroup(len(points))
        else:
            modulus, _ = self.cyclic_context(receiver)
            if modulus == 0:
                raise Unsupported("infinite cyclic automorphism objects are outside this finite diagnostic")
            retained = receiver
            while self.tag(retained) == "valueData":
                retained = fields(retained, "valueData", 1)[0]
            points = (tuple(inventory(retained)) if self.tag(retained) == "finiteData"
                      else tuple(self.encode_cyclic(k, receiver) for k in range(modulus)))
            native = libgap.AutomorphismGroup(libgap.CyclicGroup(modulus))
        return AutomorphismGroup(category, receiver, points, native)

    def aut_context(self, selected):
        if self.tag(selected) == "valueData":
            return self.aut_context(fields(selected, "valueData", 1)[0])
        if self.tag(selected) == "opaqueData":
            value = self.session.get(selected)
            if isinstance(value, AutomorphismGroup):
                return value
        underlying = self.underlying_receiver(selected)
        if self.tag(underlying) == "opaqueData":
            value = self.session.get(underlying)
            if isinstance(value, AutomorphismGroup):
                return value
        if self.tag(underlying) == "functorAction":
            action, receiver = fields(underlying, "functorAction", 2)
            atag = self.tag(action)
            if atag in {"con.automorphisms", "fun.core_sets.automorphisms", "fun.core_groups.automorphisms"}:
                if atag == "con.automorphisms":
                    category, = fields(action, atag, 1)
                else:
                    fields(action, atag, 0)
                    category = node("category", "cat.sets" if atag.startswith("fun.core_sets") else "cat.groups", [])
                return self.automorphism_group(category, core_object(receiver))
            if atag in {"fun.core_sets.automorphisms", "fun.core_groups.automorphisms"}:
                fields(action, atag, 0)
                category = node("category", "cat.sets" if atag.startswith("fun.core_sets") else "cat.groups", [])
                return self.automorphism_group(category, core_object(receiver))
        raise Unsupported("the actual selected automorphism group is not retained")

    def automorphism_image(self, selected, category, receiver):
        """Read the supplied image's retained context without replacing it."""
        actual = self.aut_context(selected)
        same(actual.category, category, "construction image's complete category selection")
        same(actual.receiver, receiver, "construction image's complete original receiver")
        return actual

    def point_index(self, point, points, selected):
        try:
            modulus, _ = self.cyclic_context(selected)
        except Unsupported:
            lookup = {key(value): i for i, value in enumerate(points)}
            actual = point
            while key(actual) not in lookup and self.tag(actual) == "valueData":
                actual, = fields(actual, "valueData", 1)
            if key(actual) not in lookup:
                actual = self.point(point, selected, None)
            if key(actual) not in lookup:
                raise ValueError("the actual finite point is outside the supplied inventory")
            return lookup[key(actual)]
        return int(self.cyclic_point(point, selected))

    def make_automorphism(self, category, receiver, forward, backward, context=None):
        context = self.automorphism_group(category, receiver) if context is None else context
        same(context.category, category, "automorphism native context's selected category")
        same(context.receiver, receiver, "automorphism native context's selected receiver")
        points = context.points
        read = lambda point, selected: self.point(point, selected, None)
        forward_images = [self.point_index(forward.at_point(point, read), points, receiver) for point in points]
        backward_images = [self.point_index(backward.at_point(point, read), points, receiver) for point in points]
        if self.category(category) == "cat.sets":
            native_forward = context.native([i + 1 for i in forward_images])
            native_backward = context.native([i + 1 for i in backward_images])
        else:
            n, _ = self.cyclic_context(receiver)
            group = libgap.CyclicGroup(n)
            generator = group.GeneratorsOfGroup()[0] if n > 1 else group.One()
            elements = [generator ** int(self.cyclic_point(point, receiver)) for point in points]
            native_forward = libgap.GroupHomomorphismByImages(group, group, elements,
                                                            [generator ** i for i in forward_images])
            native_backward = libgap.GroupHomomorphismByImages(group, group, elements,
                                                             [generator ** i for i in backward_images])
            if native_forward == libgap.fail or native_backward == libgap.fail:
                raise ValueError("the supplied cyclic-group map has no native homomorphism representation")
        return Automorphism(category, receiver, forward, backward, native_forward, native_backward)

    def automorphism(self, data, category, receiver):
        if self.tag(data) == "valueData":
            return self.automorphism(fields(data, "valueData", 1)[0], category, receiver)
        if self.tag(data) == "opaqueData":
            value = self.session.get(data)
            if not isinstance(value, Automorphism):
                raise ValueError("the owned value is not an automorphism")
            same(value.category, category, "automorphism's selected category")
            same(value.receiver, receiver, "automorphism's selected object")
            return value
        if self.tag(data) == "element":
            _, expression = fields(data, "element", 2)
            if self.tag(expression) == "point":
                raise Unsupported("an automorphism point needs its retained invocation domain")
        if not isinstance(data, list) or len(data) != 2:
            raise ValueError("a complete inline automorphism requires both callable directions")
        forward = self.function(data[0], receiver, receiver)
        backward = self.function(data[1], receiver, receiver)
        return self.make_automorphism(category, receiver, forward, backward)

    def core_comparison(self, data):
        tag = self.tag(data)
        if tag == "valueData":
            return self.core_comparison(fields(data, tag, 1)[0])
        if tag == "typedMap":
            source, target, original = typed_map(data)
            actual_source, actual_target, forward, backward = self.core_comparison(original)
            same(core_object(source), actual_source, "core comparison's complete typed source")
            same(core_object(target), actual_target, "core comparison's complete typed target")
            return actual_source, actual_target, forward, backward
        if tag == "map":
            action, original = fields(data, tag, 2)
            if self.tag(action) != "constructorMap":
                raise Unsupported("this selected action has no native core-comparison adapter")
            constructor, inner = fields(action, "constructorMap", 2)
            if constructor != "ctor.core":
                raise Unsupported("this selected constructor action has no native core adapter")
            old_source, old_target, old_forward, old_backward = self.core_comparison(original)
            source = node("functorAction", inner, old_source)
            target = node("functorAction", inner, old_target)
            forward = node("map", inner, map_data(old_source, old_target, self.session.keep(old_forward)))
            backward = node("map", inner, map_data(old_target, old_source, self.session.keep(old_backward)))
            return source, target, self.function(forward, source, target), self.function(backward, target, source)
        if tag == "coreIso":
            source, target, forward, backward = core_iso(data)
        elif tag == "mor.core_sets.fin_rev":
            dimension, = fields(data, tag, 1)
            source = target = node("obj.sets.fin", dimension)
            forward = backward = node("mor.sets.fin_rev", dimension)
        elif tag == "mor.core_sets.specified_iso":
            source, target, directions = fields(data, tag, 3)
            if not isinstance(directions, list) or len(directions) != 2:
                raise ValueError("the specified core comparison omits a direction")
            forward, backward = directions
        else:
            raise Unsupported("this complete core comparison is outside the specimen")
        return source, target, self.function(forward, source, target), self.function(backward, target, source)

    def module(self, selected):
        if self.tag(selected) == "finiteData":
            original, points = fields(selected, "finiteData", 2)
            actual_module = self.module(original)
            complete = self.finite_module_object(original, actual_module).points
            if len(points) != len(complete) or {key(point) for point in points} != {key(point) for point in complete}:
                raise ValueError("the supplied module inventory differs from its complete native carrier")
            return actual_module
        if self.tag(selected) == "functorAction":
            action, receiver = fields(selected, "functorAction", 2)
            if self.tag(action) == "fun.modules.reindex":
                return self.restricted_module(fields(action, "fun.modules.reindex", 1), receiver)
        if self.tag(selected) == "obj.modules_r.restricted_regular":
            source, target, base_map = fields(selected, "obj.modules_r.restricted_regular", 3)
            actual_source, actual_target, _ = self.base_map(base_map)
            if self.ring(source) is not self.ring(actual_source) or self.ring(target) is not self.ring(actual_target):
                raise ValueError("the named restricted module changes its selected coefficient-map endpoints")
            restricted = self.restricted_module([base_map], node("obj.modules.regular", target))
            return replace(restricted, source_ring=source, target_ring=target,
                           context={**restricted.context, "namedObject": selected,
                                    "declaredParameters": [source, target, base_map]})
        return super().module(selected)

    def regular_module(self, coefficient=Q):
        native = self.ring(coefficient)
        return RegularModule(native, lambda data: self.scalar(data, coefficient),
                             lambda data: self.encode_scalar(data, coefficient), coefficient,
                             {"regularModule": node("obj.modules.regular", coefficient),
                              "coefficient": coefficient})

    def module_scalar_ring(self, actual):
        if isinstance(actual, ModuleImage):
            return actual.scalar_ring
        if isinstance(actual, RestrictedModule):
            return self.ring(actual.source_ring)
        if isinstance(actual, RegularModule):
            return self.ring(actual.coefficient)
        return QQ if actual.native is QQ else actual.native.base_ring()

    def pulled_back_forms(self, arrow):
        scalar, values, changed_values, change_data, original_data, inclusion_data = fields(arrow, self.tag(arrow), 6)
        if self.ring(scalar) is not QQ:
            raise Unsupported("the selected pulled-back form requires rational scalars here")
        self.module(values)
        self.module(changed_values)
        change = self.function(change_data, values, changed_values)
        base, ambient, _ = typed_map(inclusion_data)
        inclusion = self.function(inclusion_data, base, ambient)
        original, actual_base = self.form(original_data), self.form(base)
        context = {"comparison": arrow, "base": base, "ambient": ambient,
                   "original": original_data, "inclusion": inclusion_data}
        pulled_back = Form(actual_base.module,
                           lambda x, y: original.pairing(inclusion(x), inclusion(y)), context)
        changed = Form(actual_base.module,
                       lambda x, y: change(pulled_back.pairing(x, y)), context)
        return changed, actual_base

    def form(self, selected):
        if self.tag(selected) == "morphismEndpoint":
            arrow, side = morphism_endpoint(selected)
            if self.tag(arrow) in {"mor.bilin_module.pulled_back_forward", "mor.bilin_module.pulled_back_backward"}:
                changed, base = self.pulled_back_forms(arrow)
                forward = self.tag(arrow).endswith("_forward")
                return changed if (side == "source") == forward else base
        return super().form(selected)

    def native_linear(self, data):
        if isinstance(data, LinearAction):
            return data
        if isinstance(data, NativeIdentity):
            return identity(self.module(data.source), self.module(data.target),
                            {"identitySource": data.source, "identityTarget": data.target})
        if isinstance(data, NativeComposition):
            return self.native_linear(data.first).then(self.native_linear(data.second))
        if isinstance(data, NativeMediator):
            left, right = self.native_linear(data.left), self.native_linear(data.right)
            if left.source.native != right.source.native:
                raise Unsupported("the actual native mediator domains differ")
            return LinearAction(left.matrix.stack(right.matrix), left.source, self.module(data.target),
                                {"mediatorSource": data.source, "mediatorTarget": data.target,
                                 "left": left.context, "right": right.context})
        raise Unsupported("this callable has no complete native linear-map representation")

    def base_map(self, data):
        if self.tag(data) == "valueData":
            return self.base_map(fields(data, "valueData", 1)[0])
        if self.tag(data) == "opaqueData":
            actual = self.session.get(data)
            if not isinstance(actual, Callable):
                raise ValueError("the retained scalar base-map datum is not a callable")
            return actual.source, actual.target, actual
        if self.tag(data) == "typedMap":
            source, target, _ = typed_map(data)
            return source, target, self.function(data, source, target)
        if self.tag(data) == "mor.commutative_rings.integer_coefficients":
            target, = fields(data, self.tag(data), 1)
            source = node("obj.commutative_rings.integers")
            return source, target, self.function(data, source, target)
        if self.tag(data) == "map":
            action, original = fields(data, "map", 2)
            if self.tag(action) != "fun.commutative_rings.ring":
                raise Unsupported("the selected base-map action is outside the specimen")
            old_source, old_target, original_callable = self.base_map(original)
            return node("functorAction", action, old_source), node("functorAction", action, old_target), original_callable
        raise Unsupported("the scalar base map needs its complete endpoints or a supported declaration")

    def restricted_module(self, parameters, receiver):
        if len(parameters) != 1:
            raise ValueError("module reindexing has exactly one explicit base-map parameter")
        source, target, base_map = self.base_map(parameters[0])
        self.ring(source)
        target_ring = self.ring(target)
        original = self.module(receiver)
        if self.module_scalar_ring(original) is not target_ring:
            raise ValueError("the actual module scalar ring differs from the selected base-map target")
        context = {"action": node("fun.modules.reindex", *parameters), "receiver": receiver,
                   "sourceRing": source, "targetRing": target, "baseMap": parameters[0]}
        return RestrictedModule(original.native, original.read, original.write, original,
                                base_map, source, target, self, context)

    def series_ring(self, coefficient):
        return LazyPowerSeriesRing(self.ring(coefficient), "t")

    def series(self, data, coefficient):
        if self.tag(data) == "valueData":
            return self.series(fields(data, "valueData", 1)[0], coefficient)
        if self.tag(data) == "opaqueData":
            value = self.session.get(data)
            if not isinstance(value, Series):
                raise ValueError("the owned point is not a complete lazy power series")
            same(value.coefficient, coefficient, "power-series coefficient selection")
            return value.native
        raise Unsupported("a complete computed series remains owned on this live connection")

    def successor_family(self, data, coefficient, index):
        if self.tag(data) == "valueData":
            return self.successor_family(fields(data, "valueData", 1)[0], coefficient, index)
        if self.tag(data) == "admittedPoint":
            _, _, _, _, _, original = admitted_point(data)
            return self.successor_family(original, coefficient, index)
        if self.tag(data) == "pointView":
            _, original, _ = fields(data, "pointView", 3)
            return self.successor_family(original, coefficient, index)
        if self.tag(data) == "element":
            _, expression = fields(data, "element", 2)
            return self.successor_family(expression, coefficient, index)
        if self.tag(data) == "point":
            return self.successor_family(fields(data, "point", 1)[0], coefficient, index)
        series_object = node("obj.sets.power_series", coefficient)
        actual = self.function(data, index, series_object)
        metadata = self.native_successor(actual.native)
        same(metadata.coefficient, coefficient, "the actual family coefficient ring")
        same(metadata.index, index, "the actual successor-family index object")
        return actual

    def native_successor(self, native):
        if isinstance(native, SuccessorFamily):
            return native
        if isinstance(native, NativeComposition):
            if (isinstance(native.first, NativeIdentity)
                    and key(native.first.source) == key(native.first.target)):
                return self.native_successor(native.second)
            if (isinstance(native.second, NativeIdentity)
                    and key(native.second.source) == key(native.second.target)):
                return self.native_successor(native.first)
        raise Unsupported("this infinite family has no retained supported native summation model")

    def interpret_arrow(self, arrow, source, target):
        tag = self.tag(arrow)
        if tag == "map":
            action, original = fields(arrow, tag, 2)
            atag = self.tag(action)
            if atag == "structuredProjectionAction":
                category, _ = structured_projection_action(action)
                self.category_descriptor(category)
                raise Unsupported("the selected structured projection requires native Arrow-comparison components")
            if atag == "fun.core_sets.two_subsets":
                fields(action, atag, 0)
                old_source, old_target, forward, backward = self.core_comparison(original)
                def image(subset):
                    if not isinstance(subset, list) or len(subset) != 2:
                        raise ValueError("the selected two-subset omits one of its actual members")
                    actual = [forward(point) for point in subset]
                    return sorted(actual, key=key)
                return Callable(source, target, image)
            if atag in {"con.automorphisms", "fun.core_sets.automorphisms", "fun.core_groups.automorphisms"}:
                if atag == "con.automorphisms":
                    category, = fields(action, atag, 1)
                else:
                    fields(action, atag, 0)
                    category = node("category", "cat.sets" if atag == "fun.core_sets.automorphisms" else "cat.groups", [])
                self.category(category)
                if atag == "con.automorphisms":
                    framed = original
                    while self.tag(framed) == "valueData":
                        framed, = fields(framed, "valueData", 1)
                    typed_map(framed)
                old_source, old_target, forward, backward = self.core_comparison(original)
                source_context = self.automorphism_image(source, category, old_source)
                target_context = self.automorphism_image(target, category, old_target)
                def conjugate(data):
                    automorphism = self.automorphism(data, category, old_source)
                    f = self.postcompose(self.postcompose(backward, automorphism.forward), forward)
                    g = self.postcompose(self.postcompose(backward, automorphism.backward), forward)
                    context = (action, original, source, target, source_context, target_context, automorphism, f, g)
                    forward_image = Callable(old_target, old_target, lambda point, retained=context: retained[-2](point),
                                             f.native, point_action=lambda point, read, retained=context: retained[-2].at_point(point, read))
                    backward_image = Callable(old_target, old_target, lambda point, retained=context: retained[-1](point),
                                              g.native, point_action=lambda point, read, retained=context: retained[-1].at_point(point, read))
                    return self.session.keep(self.make_automorphism(category, old_target, forward_image,
                                                                    backward_image, target_context))
                return Callable(source, target, conjugate)
            if atag == "fun.modules.reindex":
                parameters = fields(action, atag, 1)
                old_source, old_target = self.callable_endpoints(original)
                actual = self.function(original, old_source, old_target)
                restricted_source = self.restricted_module(parameters, old_source)
                restricted_target = self.restricted_module(parameters, old_target)
                retained = (action, original, restricted_source, restricted_target, actual)
                return Callable(source, target, lambda value, context=retained: context[-1](value), actual.native,
                                point_action=actual.at_point)
        if tag == "zero":
            actual_source, actual_target = fields(arrow, tag, 2)
            same(actual_source, source, "the selected zero-map source")
            same(actual_target, target, "the selected zero-map target")
            actual_source, actual_target = self.module(source), self.module(target)
            try:
                native = zero(actual_source, actual_target, arrow)
            except Unsupported:
                return Callable(source, target, lambda _: actual_target.zero())
            return Callable(source, target, native, native)
        if tag in {"mor.bilin_module.pulled_back_forward", "mor.bilin_module.pulled_back_backward"}:
            self.pulled_back_forms(arrow)
            native = identity(self.module(source), self.module(target),
                              {"arrow": arrow, "source": source, "target": target})
            return Callable(source, target, native, native)
        if tag == "presentation":
            comparison, parameters, inverse = fields(arrow, tag, 3)
            if comparison in self.comparisons - {self.comparison}:
                return self.other_comparison(comparison, parameters, inverse, source, target)
        if tag == "mor.sets.fin_rev":
            dimension, = fields(arrow, tag, 1)
            self.natural(dimension, "the selected reversal dimension")
            return Callable(source, target, lambda point: dimension - 1 - self.finite_ordinal(point, dimension))
        if tag in {"op.linear_orders.le", "op.linear_orders.lt"}:
            selected, = fields(arrow, tag, 1)
            selected_tag = self.tag(selected)
            if selected_tag not in {"obj.linear_orders.fin_ordinary", "obj.linear_orders.fin_reverse"}:
                raise Unsupported("this selected linear order is outside the specimen")
            dimension, = fields(selected, selected_tag, 1)
            def compare(pair):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("an order comparison requires both points")
                left, right = [self.finite_ordinal(value, dimension) for value in pair]
                if selected_tag == "obj.linear_orders.fin_reverse":
                    left, right = right, left
                return bool(ZZ(left) < ZZ(right) if tag.endswith(".lt") else ZZ(left) <= ZZ(right))
            return Callable(source, target, compare)
        if tag == "mor.sets.cyclic_quotient_map":
            modulus, = fields(arrow, tag, 1)
            if self.cyclic_context(target) != (modulus, True):
                raise ValueError("the quotient map changes its actual selected modulus")
            return Callable(source, target, lambda value: self.encode_cyclic(self.scalar(value, source), target))
        if tag == "mor.groups.cyclic_quotient_aut_by_unit":
            modulus, = fields(arrow, tag, 1)
            group = node("obj.groups.cyclic_quotient", modulus)
            category = node("category", "cat.groups", [])
            ring_object = node("obj.sets.integers_mod", modulus)
            def by_unit(data):
                if self.tag(data) == "valueData":
                    data = fields(data, "valueData", 1)[0]
                if self.tag(data) == "admittedPoint":
                    _, _, _, original_target, _, original = admitted_point(data)
                    scalar = self.scalar(original, original_target)
                    inverse = scalar.inverse_of_unit()
                elif isinstance(data, list):
                    if len(data) != 2:
                        raise ValueError("a complete unit record requires its value and inverse")
                    scalar = self.scalar(data[0], ring_object)
                    inverse = self.scalar(data[1], ring_object)
                else:
                    scalar = self.scalar(data, ring_object)
                    inverse = scalar.inverse_of_unit()
                f = Callable(group, group, lambda point: self.encode_cyclic(scalar * self.cyclic_point(point, group), group))
                b = Callable(group, group, lambda point: self.encode_cyclic(inverse * self.cyclic_point(point, group), group))
                return self.session.keep(self.make_automorphism(category, group, f, b))
            return Callable(source, target, by_unit)
        if tag == "op.groups.inverse":
            selected, = fields(arrow, tag, 1)
            try:
                additive = self.native_group_carrier(selected)
            except Unsupported:
                pass
            else:
                return Callable(source, target, additive.negate)
            try:
                group = self.aut_context(selected)
            except Unsupported:
                self.cyclic_context(selected)
                return Callable(source, target, lambda value: self.encode_cyclic(-self.cyclic_point(value, selected), selected))
            def inverse(data):
                actual = self.automorphism(data, group.category, group.receiver)
                return self.session.keep(Automorphism(actual.category, actual.receiver, actual.backward,
                                                     actual.forward, actual.native_backward, actual.native_forward))
            return Callable(source, target, inverse)
        if tag in {"mor.sets.automorphism_forward", "mor.sets.automorphism_backward",
                   "mor.groups.automorphism_forward", "mor.groups.automorphism_backward"}:
            receiver, data = fields(arrow, tag, 2)
            category = node("category", "cat.sets" if tag.startswith("mor.sets") else "cat.groups", [])
            actual = self.automorphism(data, category, receiver)
            selected = actual.backward if tag.endswith("_backward") else actual.forward
            return Callable(source, target, selected, point_action=selected.at_point)
        if tag in {"mor.sets.automorphism_evaluation", "mor.sets.automorphism_inverse_evaluation"}:
            category, functor, receiver = fields(arrow, tag, 3)
            category_id = self.category(category)
            functor_id, parameters = functor_parameter(functor)
            if parameters or (category_id, functor_id) not in {("cat.sets", "fun.sets.identity")}:
                raise Unsupported("this selected set-valued functor has no implemented action here")
            def evaluate_point(pair, read):
                pair = self.product_point(pair, source, read)
                datum = pair[0]
                inspected = datum
                while self.tag(inspected) == "valueData":
                    inspected, = fields(inspected, "valueData", 1)
                if self.tag(inspected) in {"element", "point", "compose", "typedMap"}:
                    selected, _ = self.product_factors(source)
                    datum = read(datum, selected)
                actual = self.automorphism(datum, category, receiver)
                selected = actual.backward if tag.endswith("inverse_evaluation") else actual.forward
                return selected.at_point(pair[1], read)
            def evaluate(pair):
                return evaluate_point(pair, lambda point, selected: self.point(point, selected, None))
            return Callable(source, target, evaluate, point_action=evaluate_point)
        if tag == "mor.commutative_rings.integer_coefficients":
            coefficient, = fields(arrow, tag, 1)
            selected_parent = self.ring(coefficient)
            if self.ring(source) is not ZZ or self.ring(target) is not selected_parent:
                raise ValueError("the integer coefficient map changes its selected endpoints")
            native = None
            try:
                source_model, target_model = self.polynomial_model(source), self.polynomial_model(target)
            except Unsupported:
                pass
            else:
                native = polynomial_action(source_model, target_model,
                                           lambda value, coefficients: target_model.symbolic_ring(coefficients)(value),
                                           {"arrow": arrow, "source": source, "target": target})
            return Callable(source, target, lambda value: self.encode_scalar(selected_parent(self.scalar(value, source)), target), native)
        if tag == "cartesianMap":
            reindex, parameters, receiver = cartesian_map(arrow)
            if reindex != "fun.modules.reindex":
                raise Unsupported("this registered cartesian action is outside the specimen")
            restricted = self.restricted_module(parameters, receiver)
            retained = (parameters, receiver, restricted, source, target)
            try:
                native = identity(restricted, restricted.original,
                                  {"cartesian": arrow, "source": source, "target": target,
                                   "restriction": restricted.context})
            except Unsupported:
                native = NativeIdentity(source, target)
            return Callable(source, target, lambda value, context=retained: context[2].original.write(context[2].original.read(value)), native)
        if tag == "op.modules.scalar_action":
            scalar_ring, selected = fields(arrow, tag, 2)
            native_module = self.module(selected)
            if self.ring(scalar_ring) is not self.module_scalar_ring(native_module):
                raise ValueError("the scalar action changes the actual selected module fibre")
            def scale(pair):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("scalar action requires its actual scalar and module point")
                return native_module.scale(self.scalar(pair[0], scalar_ring), pair[1])
            return Callable(source, target, scale)
        if tag == "mor.sets.successor_power_series_terms":
            coefficient, = fields(arrow, tag, 1)
            native_ring = self.series_ring(coefficient)
            generator = native_ring.gen()
            def term(index):
                index = self.natural(index, "the selected series index")
                native = native_ring(self.ring(coefficient)(index + 1)) * generator ** index
                return self.session.keep(Series(coefficient, native, {"family": arrow, "index": index}))
            native = SuccessorFamily(coefficient, source,
                                     {"arrow": arrow, "source": source, "target": target})
            return Callable(source, target, term, native)
        if tag == "bind.sets.power_series_sum":
            coefficient, index = fields(arrow, tag, 2)
            native_ring = self.series_ring(coefficient)
            def summation(data):
                family = self.successor_family(data, coefficient, index)
                if self.ring(coefficient).one() == self.ring(coefficient).zero():
                    native_sum = native_ring.zero()
                else:
                    def nonzero_terms():
                        k = 0
                        while True:
                            # The actual chosen coefficient ring controls which
                            # terms vanish; no finite truncation or closed-form
                            # replacement is used by this infinite iterator.
                            if self.ring(coefficient)(k + 1) != 0:
                                yield self.series(family(k), coefficient)
                            k += 1
                    native_sum = native_ring.sum(nonzero_terms(), True)
                return self.session.keep(Series(coefficient, native_sum,
                                                {"coefficient": coefficient, "index": index, "family": data}))
            return Callable(source, target, summation)
        if tag == "mor.sets.power_series_coefficient":
            coefficient, = fields(arrow, tag, 1)
            def coefficient_at(pair):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("coefficient extraction requires its actual series and degree")
                degree = self.natural(pair[1], "the requested coefficient degree")
                return self.encode_scalar(self.series(pair[0], coefficient)[degree], coefficient)
            return Callable(source, target, coefficient_at)
        if tag == "objectField":
            object_id, field, parameters = object_field(arrow)
            if object_id == "obj.sets.two_subsets" and field in {"presentation", "inversePresentation", "inclusion"}:
                if len(parameters) != 1:
                    raise ValueError("the selected two-subset object requires its complete carrier")
                return Callable(source, target, lambda value: value)
            if object_id == "obj.sets.integer_square_bound" and field == "inclusion":
                if len(parameters) != 1:
                    raise ValueError("the selected square bound requires its radius")
                return Callable(source, target, lambda value: value)
        return super().interpret_arrow(arrow, source, target)

    def finite_ordinal(self, value, dimension):
        if self.tag(value) == "valueData":
            return self.finite_ordinal(fields(value, "valueData", 1)[0], dimension)
        if self.tag(value) == "element":
            _, expression = fields(value, "element", 2)
            value, = fields(expression, "numeral", 1)
        if type(value) is not int or value < 0 or value >= dimension:
            raise ValueError("the finite ordinal is outside its selected range")
        return value

    def other_comparison(self, comparison, parameters, inverse, source, target):
        if comparison == "cmp.sets.singleton_terminal":
            return self.singleton_terminal_comparison(parameters, inverse, source, target)
        if type(inverse) is not bool or len(parameters) != 1:
            raise ValueError("the selected comparison requires its parameter and Boolean direction")
        if comparison == "cmp.sets.fin_reversal":
            dimension = self.natural(parameters[0], "the selected reversal dimension")
            arrow = node("presentation", comparison, parameters, inverse)
            self.same_endpoint(source, node("obj.sets.fin", dimension), arrow, "source", "reversal source")
            self.same_endpoint(target, node("obj.sets.fin", dimension), arrow, "target", "reversal target")
            return Callable(source, target, lambda point: dimension - 1 - self.finite_ordinal(point, dimension))
        modulus = self.natural(parameters[0], "the selected quotient modulus")
        if self.cyclic_context(source) != (modulus, not inverse) or self.cyclic_context(target) != (modulus, inverse):
            raise ValueError("the cyclic comparison changes a selected presentation or direction")
        return Callable(source, target, lambda value: self.encode_cyclic(self.cyclic_point(value, source), target))

    def singleton_terminal_comparison(self, parameters, inverse, source, target):
        if type(inverse) is not bool:
            raise ValueError("the singleton comparison requires its Boolean direction")
        same(parameters, [], "singleton comparison's complete declaration parameters")
        endpoints = (node("obj.sets.fin", 1), node("obj.sets.terminal"))
        expected_source, expected_target = endpoints[::-1] if inverse else endpoints
        same(self.scalar_element_carrier(source), expected_source, "singleton comparison source")
        same(self.scalar_element_carrier(target), expected_target, "singleton comparison target")
        original, image = self.finite_object(source), self.finite_object(target)
        for actual, selected, expected in ((original, source, expected_source),
                                           (image, target, expected_target)):
            if actual.native.cardinality() != 1:
                raise ValueError("a singleton-comparison endpoint needs its single actual point")
            for point in actual.points:
                value = self.point(point, selected, None)
                if self.tag(expected) == "obj.sets.fin":
                    self.finite_ordinal(value, 1)
                elif not isinstance(value, list) or value:
                    raise ValueError("a terminal point requires its empty PUnit data-field array")
        native = FiniteSetMaps(original.native, image.native).from_dict(
            {original.native.an_element(): image.native.an_element()})
        context = (parameters, inverse, source, target, original, image, native)

        def evaluate(point, retained=context):
            index = self.point_index(point, retained[4].points, retained[2])
            return retained[5].points[int(retained[6](index))]

        # Keep exact supplied keys available to the existing finite-point
        # reader before it inspects result envelopes or selected point data.
        return Callable(source, target, evaluate, native,
                        point_action=lambda point, read: evaluate(point))

    def presentation_application(self, packet, comparison=None):
        if comparison is None or comparison == self.comparison:
            return super().presentation_application(packet)
        parameters, inverse, source, target, argument = presentation_invocation(packet)
        public_data(packet, self.session)
        action = self.other_comparison(comparison, parameters, inverse, source, target)
        return self.apply_comparison(action, argument, comparison, parameters, packet)

    def point(self, data, target, domain):
        if self.tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            self.check_element_target(target, selected)
            if self.tag(expression) == "numeral":
                original = self.underlying_receiver(selected)
                if self.tag(original) in {"obj.sets.fin", "obj.finite_sets.fin",
                                          "obj.linear_orders.fin_ordinary", "obj.linear_orders.fin_reverse"}:
                    dimension, = fields(original, self.tag(original), 1)
                    self.natural(dimension, "the selected finite-point dimension")
                    return self.finite_ordinal(data, dimension)
                if self.tag(original) == "obj.sets.naturals":
                    return self.natural(fields(expression, "numeral", 1)[0], "the natural point")
            if self.tag(expression) in {"point", "operationPoint"}:
                return super().point(data, target, domain)
            if (self.tag(expression) == "operationExpression"
                    and fields(expression, "operationExpression", 3)[0]
                    in {"op.monoids.mul", "op.monoids.one"}):
                return super().point(data, target, domain)
            try:
                self.cyclic_context(selected)
            except Unsupported:
                pass
            else:
                return self.encode_cyclic(self.cyclic_point(data, selected), selected)
        return super().point(data, target, domain)

    def point_application(self, operation, packet):
        if operation == "fun.commutative_rings.ring":
            raise ValueError("the underlying-ring object action requires its complete receiver request")
        from cas_port import point_invocation
        _, parameters, arrow, _, source, target, _ = point_invocation(packet, operation)
        descriptor = self.declaration_data(arrow)
        if operation == "fun.modules.reindex#cartesian" and self.tag(descriptor) == "cartesianMap":
            reindex, declaration_parameters, receiver = cartesian_map(descriptor)
            if reindex + "#cartesian" != operation:
                raise ValueError("the cartesian descriptor changes the selected reindex action")
            same(parameters, [declaration_parameters, receiver],
                 "cartesian invocation's complete nested declaration parameters")
        if operation in self.object_operations and self.tag(descriptor) == "map":
            action, _ = fields(descriptor, "map", 2)
            same(fields(action, operation), parameters, "functor map's declaration parameters")
        if operation == "con.automorphisms#map" and self.tag(descriptor) == "map":
            action, original = fields(descriptor, "map", 2)
            same(fields(action, "con.automorphisms", 1), parameters,
                 "the construction map's selected category parameters")
            framed = original
            while self.tag(framed) == "valueData":
                framed, = fields(framed, "valueData", 1)
            typed_map(framed)
            old_source, old_target, _, _ = self.core_comparison(original)
            self.automorphism_image(source, parameters[0], old_source)
            self.automorphism_image(target, parameters[0], old_target)
        return super().point_application(operation, packet)

    def equal(self, left, right, selected):
        tag = self.tag(selected)
        if tag == "valueData":
            return self.equal(left, right, fields(selected, tag, 1)[0])
        if tag == "morphismEndpoint":
            try:
                actual = self.endpoint_view(selected)
            except Unsupported:
                pass
            else:
                return self.equal(left, right, actual)
        if tag == "opaqueData":
            owned = self.session.get(selected)
            if isinstance(owned, FiniteObject):
                return self.equal(left, right, owned.selected)
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            if self.tag(action) == "fun.core_sets.two_subsets":
                fields(action, self.tag(action), 0)
                return self.equal(left, right, node("obj.sets.two_subsets", core_object(receiver)))
            underlying = self.underlying_receiver(selected)
            if key(underlying) != key(selected):
                return self.equal(left, right, underlying)
        if tag == "obj.sets.maps":
            domain, codomain = fields(selected, tag, 2)
            f = self.function(left, domain, codomain)
            g = self.function(right, domain, codomain)
            if f.native is not None and g.native is not None:
                try:
                    native_f, native_g = self.native_linear(f.native), self.native_linear(g.native)
                except Unsupported:
                    pass
                else:
                    return native_f.equal(native_g)
                try:
                    native_f, native_g = self.native_polynomial(f.native), self.native_polynomial(g.native)
                except Unsupported:
                    pass
                else:
                    return native_f.equal(native_g)
            points = self.finite_object(domain).points
            # Every actual domain point is inspected. An infinite domain raises
            # Unsupported above; no finite sample is called whole-map equality.
            read = lambda point, selected: self.point(point, selected, None)
            return all(self.equal(f.at_point(point, read), g.at_point(point, read), codomain) for point in points)
        if tag == "obj.sets.truth_values":
            if type(left) is not bool or type(right) is not bool:
                raise ValueError("a truth-valued point requires a Boolean")
            return left == right
        if tag == "obj.sets.naturals":
            fields(selected, tag, 0)
            return self.natural(left, "the first natural point") == self.natural(right, "the second natural point")
        if tag in {"obj.sets.fin", "obj.finite_sets.fin", "obj.linear_orders.fin_ordinary", "obj.linear_orders.fin_reverse"}:
            dimension, = fields(selected, tag, 1)
            return self.finite_ordinal(left, dimension) == self.finite_ordinal(right, dimension)
        if tag in {"obj.sets.integer_square_bound", "obj.finite_sets.integer_square_bound"}:
            radius, = fields(selected, tag, 1)
            if type(left) is not int or type(right) is not int or abs(left) > radius or abs(right) > radius:
                raise ValueError("a square-bound point is outside its complete selected carrier")
            return left == right
        if tag in {"finiteData", "extent", "obj.sets.terminal"}:
            points = self.finite_object(selected).points
            return self.point_index(left, points, selected) == self.point_index(right, points, selected)
        if tag == "obj.sets.two_subsets":
            receiver, = fields(selected, tag, 1)
            original = self.finite_object(receiver)
            return Set(self.point_index(point, original.points, receiver) for point in left) == Set(self.point_index(point, original.points, receiver) for point in right)
        try:
            self.cyclic_context(selected)
        except Unsupported:
            pass
        else:
            return bool(self.cyclic_point(left, selected) == self.cyclic_point(right, selected))
        try:
            context = self.aut_context(selected)
        except Unsupported:
            pass
        else:
            a = self.automorphism(left, context.category, context.receiver)
            b = self.automorphism(right, context.category, context.receiver)
            read = lambda point, selected: self.point(point, selected, None)
            return all(self.equal(a.forward.at_point(point, read), b.forward.at_point(point, read), context.receiver)
                       and self.equal(a.backward.at_point(point, read), b.backward.at_point(point, read), context.receiver)
                       for point in context.points)
        return super().equal(left, right, selected)

    def object_application(self, operation, packet):
        if operation in self.module_action_operations:
            return self.module_functor_object(operation, packet)
        original_request = packet
        method_parameters = None
        method_functors = {"meth.cardinality": "fun.sets.cardinality",
                           "meth.kernel": "fun.arrows_modules.kernel",
                           "meth.arrow_ker": "fun.arrows_modules.kernel"}
        if operation in method_functors:
            if (self.tag(packet) == operation or isinstance(packet, dict) and "receiver" in packet
                    or isinstance(self.tag(packet), str) and self.tag(packet).startswith("meth.")):
                functor = method_functors[operation]
                _, actions, packet = method_invocation(packet, operation, functor)
                if len(actions) != 1:
                    raise ValueError("an owner-category method requires no residual action descriptors")
                count = 0 if operation == "meth.cardinality" else 1
                method_parameters = fields(actions[0], functor, count)
            elif operation != "meth.cardinality":
                # The published kernel functor has an explicit scalar argument;
                # the zero-parameter legacy receiver exception cannot supply it.
                raise ValueError("a kernel method requires its complete selected functor request")
        if operation == "fun.commutative_rings.ring":
            _, parameters, receiver = construction_invocation(packet, operation)
            if parameters:
                raise ValueError("the underlying-ring functor has no explicit declaration parameters")
            # Forgetting the selected commutative structure keeps the same Sage
            # ring. Retain the actual receiver and every owned dependency; do
            # not replace them with a named ring or an unevaluated action recipe.
            return self.session.keep(RingImage(self.ring(receiver), receiver, packet))
        if operation == self.additive_functor:
            _, parameters, receiver = construction_invocation(packet, operation)
            return self.additive_monoid_object(parameters, receiver)
        if operation in {"fun.arrows_modules.kernel", "meth.kernel", "meth.arrow_ker"}:
            parameters = []
            if operation == "fun.arrows_modules.kernel":
                _, parameters, arrow = construction_invocation(packet, operation)
                if len(parameters) != 1 or self.ring(parameters[0]) is not QQ:
                    raise Unsupported("the native kernel implementation requires the selected rational scalar ring")
            else:
                arrow = packet
                parameters = method_parameters
                if self.ring(parameters[0]) is not QQ:
                    raise Unsupported("the native kernel implementation requires the selected rational scalar ring")
            source, target, defining_map = self.arrow_record(arrow)
            actual_source, actual_target = self.module(source), self.module(target)
            callable_data = self.function(defining_map, source, target)
            native = self.native_linear(callable_data.native)
            if native.source.native != actual_source.native or native.target.native != actual_target.native:
                raise Unsupported("the full native map does not retain the actual selected endpoint modules")
            native_kernel = native.kernel()
            if actual_source.native is QQ:
                read_kernel = lambda data: native_kernel(vector(QQ, [actual_source.read(data)]))
                write_kernel = lambda data: actual_source.write(data[0])
            else:
                read_kernel = lambda data: native_kernel(actual_source.read(data))
                write_kernel = actual_source.write
            kernel_module = Module(native_kernel, read_kernel, write_kernel)
            kernel_object = self.session.keep(kernel_module)
            inclusion = LinearAction(identity_matrix(QQ, degree(kernel_module)), kernel_module,
                                     actual_source, {"kernelOf": arrow, "parameters": parameters,
                                                     "request": original_request})
            inclusion_data = self.session.keep(Callable(kernel_object, source, inclusion, inclusion))
            return node("arrow", kernel_object, source, map_data(kernel_object, source, inclusion_data))
        if operation == "lim.sets.product":
            left, right = fields(packet, "pair", 2)
            apex = node("objectProduct", left, right)
            first_native = second_native = None
            try:
                apex_module, left_module, right_module = self.module(apex), self.module(left), self.module(right)
            except Unsupported:
                pass
            else:
                first_native = LinearAction(matrix(QQ, [[1, 0]]), apex_module, left_module,
                                            {"product": packet, "port": 1, "source": apex, "target": left})
                second_native = LinearAction(matrix(QQ, [[0, 1]]), apex_module, right_module,
                                             {"product": packet, "port": 2, "source": apex, "target": right})
            if first_native is None or second_native is None:
                try:
                    apex_model = self.polynomial_model(apex)
                    left_model, right_model = self.polynomial_model(left), self.polynomial_model(right)
                except Unsupported:
                    pass
                else:
                    first_native = polynomial_action(apex_model, left_model, lambda point, _: point[0],
                                                     {"product": packet, "port": 1})
                    second_native = polynomial_action(apex_model, right_model, lambda point, _: point[1],
                                                      {"product": packet, "port": 2})
            first = self.session.keep(Callable(apex, left, lambda point: point[0], first_native,
                                               point_action=lambda point, read: self.product_point(point, apex, read)[0]))
            second = self.session.keep(Callable(apex, right, lambda point: point[1], second_native,
                                                point_action=lambda point, read: self.product_point(point, apex, read)[1]))
            return node("cone", apex, map_data(apex, left, first), map_data(apex, right, second))
        if operation == "con.automorphisms":
            _, parameters, receiver = construction_invocation(packet, operation)
            if len(parameters) != 1:
                raise ValueError("Aut requires the actual selected category dictionary")
            return self.session.keep(self.automorphism_group(parameters[0], core_object(receiver)))
        if operation in {"fun.core_sets.automorphisms", "fun.core_groups.automorphisms"}:
            _, parameters, receiver = construction_invocation(packet, operation)
            if parameters:
                raise ValueError("the selected core automorphism functor has no explicit parameters")
            category = node("category", "cat.sets" if operation.startswith("fun.core_sets") else "cat.groups", [])
            return self.session.keep(self.automorphism_group(category, core_object(receiver)))
        if operation == "fun.modules.reindex":
            _, parameters, receiver = construction_invocation(packet, operation)
            return self.session.keep(self.restricted_module(parameters, receiver))
        if operation == "fun.core_sets.two_subsets":
            _, parameters, receiver = construction_invocation(packet, operation)
            if parameters:
                raise ValueError("the selected two-subset functor has no explicit parameters")
            descriptor = node("functorAction", node(operation), receiver)
            return self.session.keep(self.finite_object(descriptor))
        if operation == "meth.two_subsets":
            receiver = core_object(packet) if self.tag(packet) == "coreObject" else packet
            return self.session.keep(self.finite_object(node("obj.sets.two_subsets", receiver)))
        if operation == "meth.cardinality":
            receiver = core_object(packet) if self.tag(packet) == "coreObject" else packet
            try:
                group = self.aut_context(receiver)
            except Unsupported:
                count = int(self.finite_object(receiver).native.cardinality())
            else:
                count = int(group.native.cardinality()) if self.category(group.category) == "cat.sets" else int(group.native.Size())
            return node("finite", count)
        raise Unsupported("this object action is outside the specimen")
