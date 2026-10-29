"""Public module fibre-inclusion and underlying object/map actions.

These adapters retain the existing native Module and Callable values. They do
not recover a source object from a functor recipe, enumerate an infinite carrier,
or select a subsequent operation. Every returned image remains session-owned.
"""

from dataclasses import dataclass

from cas_port import construction_invocation, functor_map_invocation, typed_map
from engine import Module
from wire import Callable, Unsupported, fields, same


FIBRE = "fun.modules.fibre_inclusion"
UNDERLYING = "fun.modules.underlying"


@dataclass(frozen=True)
class ModuleImage(Module):
    """An actual native image with its complete selected request retained."""

    operation: str
    parameters: object
    source: object
    original: Module
    scalar_ring: object
    request: object

    def scale(self, scalar, value):
        # A restricted module's action uses its actual retained base map.
        return self.original.scale(scalar, value)


class ModuleFunctorInterfaces:
    module_functors = {FIBRE, UNDERLYING}
    module_action_operations = module_functors

    def module_action(self, action):
        operation = self.tag(action)
        return (operation, fields(action, operation)) if operation in self.module_functors else (None, None)

    def module_object_invocation(self, packet, operation):
        return construction_invocation(packet, operation)

    def module_map_invocation(self, packet, operation):
        return functor_map_invocation(packet, operation)

    def module_action_native(self, operation, receiver):
        return self.module(receiver)

    def module_image_record(self, actual, operation, parameters, receiver, scalar_ring, packet):
        return ModuleImage(actual.native, actual.read, actual.write, operation,
                           parameters, receiver, actual, scalar_ring, packet)

    def module_functor_parameters(self, operation, parameters):
        count = 1 if operation == FIBRE else 0
        if len(parameters) != count:
            raise ValueError("the module functor requires all %d ordered parameters" % count)

    def module_functor_object(self, operation, packet):
        _, parameters, receiver = self.module_object_invocation(packet, operation)
        self.module_functor_parameters(operation, parameters)
        actual = self.module_action_native(operation, receiver)
        scalar_ring = self.module_scalar_ring(actual)
        if operation == FIBRE and self.ring(parameters[0]) is not scalar_ring:
            raise ValueError("the native module differs from the supplied scalar fibre")
        image = self.module_image_record(actual, operation, parameters, receiver, scalar_ring, packet)
        return self.session.keep(image)

    def module_functor_image(self, selected, operation, parameters, source):
        """Read actual image data without replacing its complete endpoint."""
        actual = self.module_image(selected)
        if actual is None:
            raise Unsupported("the selected image needs its actual native object result")
        same(actual.operation, operation, "module image's selected functor")
        same(actual.parameters, parameters, "module image's complete ordered parameters")
        same(actual.source, source, "module image's complete original source")
        return actual

    def module_image(self, selected):
        data = selected
        while self.tag(data) == "valueData":
            data, = fields(data, "valueData", 1)
        if self.tag(data) == "opaqueData":
            actual = self.session.get(data)
            if isinstance(actual, ModuleImage):
                return actual
        return None

    def scalar_element_carrier(self, selected):
        if self.tag(selected) == "opaqueData":
            actual = self.session.get(selected)
            if isinstance(actual, ModuleImage):
                # This is only the retained point codec. The public callable
                # keeps its exact image endpoints and supplying owner.
                return self.scalar_element_carrier(actual.source)
        return super().scalar_element_carrier(selected)

    def polynomial_model(self, selected):
        if self.tag(selected) == "opaqueData":
            actual = self.session.get(selected)
            if isinstance(actual, ModuleImage):
                return self.polynomial_model(actual.source)
        return super().polynomial_model(selected)

    def interpret_arrow(self, arrow, source, target):
        if self.tag(arrow) == "map":
            action, original = fields(arrow, "map", 2)
            operation, parameters = self.module_action(action)
            if operation is not None:
                if self.module_image(source) is None and self.module_image(target) is None:
                    # Existing nested carrier maps keep their original reader.
                    # The new #map boundary separately requires actual images.
                    return super().interpret_arrow(arrow, source, target)
                self.module_functor_parameters(operation, parameters)
                old_source, old_target, _ = typed_map(original)
                image_source = self.module_functor_image(source, operation, parameters, old_source)
                image_target = self.module_functor_image(target, operation, parameters, old_target)
                actual = self.function(original, old_source, old_target)
                # Sage supplies the scalar identity of a fibre inclusion. The
                # original callable supplies the entire point action; no map
                # is reconstructed from samples or from its declared name.
                scalar_map = None
                if operation == FIBRE:
                    scalar = self.ring(parameters[0])
                    scalar_map = scalar.coerce_map_from(scalar)
                    if scalar_map is None:
                        raise Unsupported("Sage did not supply the selected scalar identity")
                retained = (action, original, source, target, image_source,
                            image_target, actual, scalar_map)

                def encode(value, context=retained):
                    point = self.point(value, old_target, None)
                    return context[5].write(context[5].read(point))

                def evaluate(value, context=retained):
                    return encode(context[6](value))

                def evaluate_point(value, read, context=retained):
                    return encode(context[6].at_point(value, read))

                return Callable(source, target, evaluate, actual.native,
                                point_action=evaluate_point)
        return super().interpret_arrow(arrow, source, target)

    def point_application(self, operation, packet):
        if operation in self.module_action_operations:
            raise ValueError("a module object action requires its complete receiver request")
        functor = operation.removesuffix("#map")
        if operation.endswith("#map") and functor in self.module_action_operations:
            _, parameters, arrow, _, source, target, _ = self.module_map_invocation(packet, functor)
            self.module_functor_parameters(functor, parameters)
            _, original = fields(arrow, "map", 2)
            old_source, old_target, _ = typed_map(original)
            self.module_functor_image(source, functor, parameters, old_source)
            self.module_functor_image(target, functor, parameters, old_target)
        return super().point_application(operation, packet)
