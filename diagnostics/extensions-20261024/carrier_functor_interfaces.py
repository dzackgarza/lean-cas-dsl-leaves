"""Published structural carrier actions on the existing native ring/modules.

The actual selected action chooses a supported native reader. Returned records
retain source data, operations and codecs from that reader; no native-parent
comparison supplies a category, a law, or an alternative selected structure.
"""

from dataclasses import dataclass

from cas_port import action_address, action_invocation, action_map_invocation
from module_functor_interfaces import ModuleFunctorInterfaces, ModuleImage
from wire import Unsupported, fields, node, same


MODULE_ADDITIVE = "fun.modules.additive_group"
TO_GROUPS = "fun.additive_groups.to_groups"
GROUP_MONOID = "fun.groups.monoid"
SEMIGROUP = "fun.monoids.semigroup"
RING_ADD_COMM = "fun.rings.additive_commutative_monoid"
ADD_COMM_MONOID = "fun.additive_commutative_monoids.additive_monoid"
ADD_UNDERLYING = "fun.additive_monoids.underlying"
RING_MULTIPLICATIVE = "fun.rings.multiplicative_monoid"
ASSOCIATIVE = "clf.magmas.associative"
BINARY_OPERATION = "clf.sets.binary_operation"
ASSOCIATIVE_FORGET = action_address({"classifierForget": ASSOCIATIVE})
BINARY_FORGET = action_address({"classifierForget": BINARY_OPERATION})
CARRIER_FUNCTORS = {MODULE_ADDITIVE, TO_GROUPS, GROUP_MONOID, SEMIGROUP,
                    RING_ADD_COMM, ADD_COMM_MONOID, ADD_UNDERLYING, RING_MULTIPLICATIVE}
CLASSIFIER_ACTIONS = {ASSOCIATIVE_FORGET: ASSOCIATIVE, BINARY_FORGET: BINARY_OPERATION}


@dataclass(frozen=True)
class CarrierImage(ModuleImage):
    """Retained native operations at this exact selected carrier interface."""

    native_operations: object


class CarrierFunctorInterfaces(ModuleFunctorInterfaces):
    module_functors = ModuleFunctorInterfaces.module_functors | CARRIER_FUNCTORS
    module_action_operations = module_functors | set(CLASSIFIER_ACTIONS)

    def module_action(self, action):
        if self.tag(action) == "classifierForget":
            classifier, parameters = fields(action, "classifierForget", 2)
            if classifier in CLASSIFIER_ACTIONS.values():
                if not isinstance(parameters, list):
                    raise ValueError("classifier parameters require their ordered array")
                return action_address({"classifierForget": classifier}), [action]
        return super().module_action(action)

    def module_object_invocation(self, packet, operation):
        if operation in CLASSIFIER_ACTIONS:
            return action_invocation(packet, operation)
        return super().module_object_invocation(packet, operation)

    def module_map_invocation(self, packet, operation):
        if operation in CLASSIFIER_ACTIONS:
            return action_map_invocation(packet, operation)
        return super().module_map_invocation(packet, operation)

    def module_functor_parameters(self, operation, parameters):
        if operation in CLASSIFIER_ACTIONS:
            if len(parameters) != 1:
                raise ValueError("a classifier action requires its complete descriptor")
            classifier, actual = fields(parameters[0], "classifierForget", 2)
            same(classifier, CLASSIFIER_ACTIONS[operation], "selected classifier-forget identity")
            same(actual, [], "classifier-forget declaration parameters")
            return
        return super().module_functor_parameters(operation, parameters)

    def carrier_image(self, selected, operations):
        actual = self.module_image(selected)
        if isinstance(actual, CarrierImage) and actual.operation in operations:
            return actual
        return None

    def carrier_symbolic_source(self, selected, operation):
        while self.tag(selected) == "valueData":
            selected, = fields(selected, "valueData", 1)
        if self.tag(selected) != "functorAction":
            raise Unsupported("this selected carrier has no supported retained native interface")
        action, receiver = fields(selected, "functorAction", 2)
        selected_operation, parameters = self.module_action(action)
        if selected_operation != operation:
            raise Unsupported("the explicit carrier action has a different native interface")
        self.module_functor_parameters(operation, parameters)
        return receiver

    def additive_group_native(self, selected):
        actual = self.carrier_image(selected, {MODULE_ADDITIVE})
        if actual is not None:
            return actual, actual.source
        return super().additive_group_native(selected)

    def additive_commutative_native(self, selected):
        actual = self.carrier_image(selected, {RING_ADD_COMM})
        if actual is not None:
            return actual
        return self.regular_module(self.carrier_symbolic_source(selected, RING_ADD_COMM))

    def additive_monoid_native(self, selected):
        actual = self.carrier_image(selected, {ADD_COMM_MONOID})
        if actual is not None:
            return actual
        if self.tag(selected) == "functorAction":
            action, receiver = fields(selected, "functorAction", 2)
            if self.tag(action) == ADD_COMM_MONOID:
                fields(action, ADD_COMM_MONOID, 0)
                return self.additive_commutative_native(receiver)
        return super().additive_monoid_native(selected)

    def native_group_carrier(self, selected):
        actual = self.carrier_image(selected, {TO_GROUPS})
        if actual is not None:
            return actual
        group = self.carrier_symbolic_source(selected, TO_GROUPS)
        return self.additive_group_native(group)[0]

    def native_monoid_carrier(self, selected):
        actual = self.carrier_image(selected, {GROUP_MONOID, RING_MULTIPLICATIVE})
        if actual is not None:
            return actual
        try:
            group = self.carrier_symbolic_source(selected, GROUP_MONOID)
        except Unsupported:
            ring = self.carrier_symbolic_source(selected, RING_MULTIPLICATIVE)
            return self.regular_module(ring)
        return self.native_group_carrier(group)

    def native_semigroup_carrier(self, selected):
        actual = self.carrier_image(selected, {SEMIGROUP})
        if actual is not None:
            return actual
        return self.native_monoid_carrier(self.carrier_symbolic_source(selected, SEMIGROUP))

    def native_magma_carrier(self, selected):
        actual = self.carrier_image(selected, {ASSOCIATIVE_FORGET})
        if actual is not None:
            return actual
        return self.native_semigroup_carrier(self.carrier_symbolic_source(selected, ASSOCIATIVE_FORGET))

    def module_action_native(self, operation, receiver):
        if operation == MODULE_ADDITIVE:
            return self.module(receiver)
        if operation == TO_GROUPS:
            return self.additive_group_native(receiver)[0]
        if operation == GROUP_MONOID:
            return self.native_group_carrier(receiver)
        if operation == SEMIGROUP:
            return self.native_monoid_carrier(receiver)
        if operation == ASSOCIATIVE_FORGET:
            return self.native_semigroup_carrier(receiver)
        if operation == BINARY_FORGET:
            return self.native_magma_carrier(receiver)
        if operation in {RING_ADD_COMM, RING_MULTIPLICATIVE}:
            return self.regular_module(receiver)
        if operation == ADD_COMM_MONOID:
            return self.additive_commutative_native(receiver)
        if operation == ADD_UNDERLYING:
            return self.additive_monoid_native(receiver)
        return super().module_action_native(operation, receiver)

    def module_image_record(self, actual, operation, parameters, receiver, scalar_ring, packet):
        if operation not in CARRIER_FUNCTORS and operation not in CLASSIFIER_ACTIONS:
            return super().module_image_record(actual, operation, parameters, receiver, scalar_ring, packet)
        if operation == RING_MULTIPLICATIVE:
            selected = node("functorAction", node(RING_MULTIPLICATIVE), receiver)
            native_operations = self.monoid_operations(selected)
        elif operation == TO_GROUPS:
            selected = node("functorAction", node(TO_GROUPS), receiver)
            native_operations = self.group_monoid_operations(selected)
        elif operation in {GROUP_MONOID, SEMIGROUP, ASSOCIATIVE_FORGET, BINARY_FORGET}:
            if isinstance(actual, CarrierImage):
                native_operations = actual.native_operations
            elif operation == GROUP_MONOID:
                native_operations = self.group_monoid_operations(receiver)
            elif operation == SEMIGROUP:
                native_operations = self.monoid_operations(receiver)
            elif operation == ASSOCIATIVE_FORGET:
                native_operations = self.semigroup_operations(receiver)
            else:
                native_operations = self.semigroup_operations(
                    self.carrier_symbolic_source(receiver, ASSOCIATIVE_FORGET))
        else:
            native_operations = actual.add, actual.zero, "module_addition"
        return CarrierImage(actual.native, actual.read, actual.write, operation,
                            parameters, receiver, actual, scalar_ring, packet, native_operations)

    def group_monoid_operations(self, selected):
        actual = self.carrier_image(selected, {TO_GROUPS})
        if actual is not None:
            return actual.native_operations
        if self.tag(selected) == "valueData":
            return self.group_monoid_operations(fields(selected, "valueData", 1)[0])
        if self.tag(selected) == "functorAction":
            action, receiver = fields(selected, "functorAction", 2)
            if self.tag(action) == TO_GROUPS:
                fields(action, TO_GROUPS, 0)
                if self.tag(receiver) == "valueData":
                    # Inspect the original point codec without replacing the
                    # complete receiver stored in the returned image/request.
                    original, = fields(receiver, "valueData", 1)
                    return self.group_monoid_operations(node("functorAction", action, original))
                actual = self.carrier_image(receiver, {MODULE_ADDITIVE})
                if actual is not None:
                    return actual.native_operations
        return super().group_monoid_operations(selected)

    def semigroup_operations(self, selected):
        actual = self.carrier_image(selected, {SEMIGROUP})
        if actual is not None:
            return actual.native_operations
        return self.monoid_operations(self.carrier_symbolic_source(selected, SEMIGROUP))

    def monoid_operations(self, selected):
        actual = self.carrier_image(selected, {GROUP_MONOID, RING_MULTIPLICATIVE})
        if actual is not None:
            return actual.native_operations
        return super().monoid_operations(selected)
