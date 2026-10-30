"""The two public tuple constructors, using native Python tuple operations.

A tuple at the public ``obj.sets.vectors(X, n)`` interface is a complete callable
on Fin(n). Its entries keep their original public data and opaque owners. The
existing point and callable readers supply the actual entries; no carrier or
arithmetic structure is inferred from them.
"""

from cas_port import morphism_endpoint, point_invocation, typed_map
from wire import Callable, Unsupported, fields, key, node


class TupleInterfaces:
    tuple_operations = {"mor.sets.tuple_empty", "mor.sets.tuple_cons"}

    def tuple_signature(self, operation, parameters):
        """Native codec context from the complete published declaration."""
        count = 1 if operation == "mor.sets.tuple_empty" else 2
        if not isinstance(parameters, list) or len(parameters) != count:
            raise ValueError("the tuple constructor omits or adds a declaration parameter")
        selected = parameters[0]
        if operation == "mor.sets.tuple_empty":
            return (node("obj.sets.fin", 1), node("obj.sets.vectors", selected, 0))
        dimension = self.natural(parameters[1], "the selected tuple dimension")
        return (node("objectProduct", selected, node("obj.sets.vectors", selected, dimension)),
                node("obj.sets.vectors", selected, dimension + 1))

    def endpoint_view(self, selected):
        arrow, side = morphism_endpoint(selected)
        operation = self.tag(arrow)
        if operation in self.tuple_operations:
            source, target = self.tuple_signature(operation, fields(arrow, operation))
            return source if side == "source" else target
        return super().endpoint_view(selected)

    def tuple_context(self, selected):
        """Read a tuple's coefficient descriptor and its complete index size."""
        tag = self.tag(selected)
        if tag == "valueData":
            return self.tuple_context(fields(selected, tag, 1)[0])
        if tag == "finiteData":
            original, _ = fields(selected, tag, 2)
            return self.tuple_context(original)
        if tag == "morphismEndpoint":
            return self.tuple_context(self.endpoint_view(selected))
        if tag == "functorAction":
            action, original = fields(selected, tag, 2)
            if self.carrier_action(action):
                return self.tuple_context(original)
        if tag == "obj.sets.vectors":
            coefficient, dimension = fields(selected, tag, 2)
            return coefficient, self.natural(dimension, "the selected tuple dimension")
        raise Unsupported("this selected point has no tuple coordinate interface")

    def tuple_endpoint(self, actual, expected, arrow, side):
        if self.tag(actual) == "valueData":
            return self.tuple_endpoint(fields(actual, "valueData", 1)[0], expected, arrow, side)
        if self.tag(actual) == "morphismEndpoint":
            original, selector = morphism_endpoint(actual)
            retained = self.retained_map_endpoint(original, selector)
            if retained is not None:
                # Read the supplied callable's actual field. The new Callable
                # still retains ``actual`` and its owner's token verbatim.
                return self.tuple_endpoint(retained, expected, arrow, side)
        self.same_endpoint(actual, expected, arrow, side, "tuple constructor's " + side)

    def tuple_values(self, data, selected):
        """Consume every actual coordinate, checking both callable endpoints."""
        coefficient, dimension = self.tuple_context(selected)
        tag = self.tag(data)
        if tag == "valueData":
            return self.tuple_values(fields(data, tag, 1)[0], selected)
        if tag == "element":
            original, expression = fields(data, tag, 2)
            self.check_element_target(selected, original)
            return self.tuple_values(expression, selected)
        if tag in {"point", "pointView", "admittedPoint", "constrainedPoint"}:
            actual = self.point(data, selected, None)
            if key(actual) == key(data):
                raise Unsupported("the selected tuple point has no implemented callable data")
            return self.tuple_values(actual, selected)
        index = node("obj.sets.fin", dimension)
        actual = self.function(data, index, coefficient)
        read = lambda value, target: self.point(value, target, None)
        return tuple(actual.at_point(i, read) for i in range(dimension))

    @staticmethod
    def tuple_graph(values):
        # This is the existing complete finite-function codec, not a new tuple
        # wire tag or a scalar-coordinate shortcut.
        return [[i, value] for i, value in enumerate(values)]

    def point(self, data, target, domain):
        try:
            coefficient, dimension = self.tuple_context(target)
        except Unsupported:
            return super().point(data, target, domain)
        tag = self.tag(data)
        if tag == "valueData":
            return self.point(fields(data, tag, 1)[0], target, domain)
        if tag == "element":
            selected, expression = fields(data, tag, 2)
            self.check_element_target(target, selected)
            return self.point(expression, target, domain)
        # Coordinate callables are function-valued tuple points. Their Fin(n)
        # source is not the original generalized domain of a point invocation.
        index = node("obj.sets.fin", dimension)
        coordinate_data = isinstance(data, list) or tag == "finiteGraph"
        if tag not in {"point", "pointView", "admittedPoint", "constrainedPoint"}:
            if tag == "typedMap":
                actual_source, actual_target, _ = typed_map(data)
            elif tag == "opaqueData":
                actual = self.session.get(data)
                actual_source = actual.source if isinstance(actual, Callable) else None
                actual_target = actual.target if isinstance(actual, Callable) else None
            elif isinstance(data, dict):
                try:
                    actual_source = self.component_endpoint(data, "source")
                    actual_target = self.component_endpoint(data, "target")
                except Unsupported:
                    actual_source = actual_target = None
            else:
                actual_source = actual_target = None
            coordinate_data = coordinate_data or (key(actual_source) == key(index)
                                                   and key(actual_target) == key(coefficient))
        if coordinate_data:
            self.function(data, index, coefficient)
            return data
        return super().point(data, target, domain)

    def interpret_arrow(self, arrow, source, target):
        operation = self.tag(arrow)
        if operation not in self.tuple_operations:
            return super().interpret_arrow(arrow, source, target)
        parameters = fields(arrow, operation)
        expected_source, expected_target = self.tuple_signature(operation, parameters)
        self.tuple_endpoint(source, expected_source, arrow, "source")
        self.tuple_endpoint(target, expected_target, arrow, "target")
        context = (arrow, parameters, source, target)
        if operation == "mor.sets.tuple_empty":
            def empty(point, read, retained=context):
                self.finite_ordinal(read(point, retained[2]), 1)
                return self.tuple_graph(tuple())
            return Callable(source, target,
                            lambda point: empty(point, lambda value, selected: self.point(value, selected, None)),
                            point_action=empty)
        _, tail = self.product_factors(source)

        def cons(point, read, retained=context):
            head, original_tail = self.product_point(point, retained[2], read)
            # The X-valued field is complete public point data. Native tuple
            # assembly copies it unchanged: it can itself be a retained graph
            # key, an owned value, or a function-valued point. Enumerating X or
            # coercing this field is unnecessary and would lose such data.
            values = (head,) + self.tuple_values(original_tail, tail)
            return self.tuple_graph(values)

        return Callable(source, target,
                        lambda point: cons(point, lambda value, selected: self.point(value, selected, None)),
                        point_action=cons)

    def point_application(self, operation, packet):
        if operation in self.tuple_operations:
            _, parameters, _, _, _, _, _ = point_invocation(packet, operation)
            self.tuple_signature(operation, parameters)
        return super().point_application(operation, packet)
