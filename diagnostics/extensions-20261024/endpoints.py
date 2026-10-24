"""Computational views of the existing declared callable endpoints.

These views select existing native readers from the public full signatures. They
never replace a request endpoint, choose a different callable, or supply a finite
inventory. Every Callable continues to retain the exact original descriptors.
"""

from cas_port import cartesian_map, morphism_endpoint, object_product, typed_map
from wire import (Callable, Unsupported, fields, inventory, key, node,
                  power_object_map, retained_endpoint, same)


class EndpointInterfaces:
    def power_endpoints(self, arrow):
        """Native decoding context from the complete public power-field types."""
        _, field, parameters = power_object_map(arrow)
        terminal = node("obj.sets.fin", 1)
        truth = node("obj.sets.truth_values")
        if field == "truth":
            return terminal, truth
        selected = parameters[0]
        if field == "terminal":
            return selected, terminal
        if field == "member":
            return node("objectProduct", selected, node("obj.sets.power_set", selected)), truth
        ambient = parameters[1] if field == "image" else selected
        return terminal, node("obj.sets.power_set", ambient)

    def component_endpoint(self, arrow, side):
        actual = retained_endpoint(arrow, side, self.session)
        if actual is not None:
            return actual
        return self.endpoint_view(node("morphismEndpoint", arrow, side))

    def endpoint_view(self, selected):
        """Read native input context while leaving ``selected`` attached verbatim."""
        arrow, side = morphism_endpoint(selected)
        tag = self.tag(arrow)
        if tag in {"valueData", "point"}:
            return self.endpoint_view(node("morphismEndpoint", fields(arrow, tag, 1)[0], side))
        if tag == "typedMap":
            # Use the actual retained field for native decoding. This helper
            # neither emits nor substitutes a new wrapper around a typed map.
            source, target, _ = typed_map(arrow)
            return source if side == "source" else target
        if tag == "opaqueData":
            actual = self.session.get(arrow)
            if not isinstance(actual, Callable):
                raise ValueError("the endpoint's owned datum is not a callable")
            return actual.source if side == "source" else actual.target
        if tag in {"identity", "zero"}:
            source, target = fields(arrow, tag, 2)
            if tag == "identity":
                same(source, target, "endpoint identity's selected objects")
            return source if side == "source" else target
        if tag == "compose":
            first, second = fields(arrow, tag, 2)
            return node("morphismEndpoint", first if side == "source" else second, side)
        if tag == "mediator":
            left, right = fields(arrow, tag, 2)
            if side == "source":
                actual = self.component_endpoint(left, "source")
                same(self.component_endpoint(right, "source"), actual,
                     "mediator's complete shared domain")
                return actual
            return node("objectProduct", self.component_endpoint(left, "target"),
                        self.component_endpoint(right, "target"))
        if tag == "element":
            original, _ = fields(arrow, tag, 2)
            return node("obj.sets.fin", 1) if side == "source" else original
        if tag == "powerObjectMap":
            source, target = self.power_endpoints(arrow)
            return source if side == "source" else target
        if tag == "map":
            action, original = fields(arrow, tag, 2)
            if self.carrier_action(action):
                return node("functorAction", action, node("morphismEndpoint", original, side))
            raise Unsupported("the selected mapped endpoint has no implemented native reader")
        if tag == "cellComponent":
            cell, parameters, receiver, inverse = fields(arrow, tag, 4)
            if cell == self.additive_cell:
                same(parameters, [], "the endpoint component's declaration parameters")
                if type(inverse) is not bool:
                    raise ValueError("the endpoint component requires a Boolean orientation")
                left, right = self.additive_carrier_routes(receiver)
                return (right if inverse else left) if side == "source" else (left if inverse else right)
        if tag == "cartesianMap":
            reindex, parameters, receiver = cartesian_map(arrow)
            if reindex == "fun.modules.reindex":
                if len(parameters) != 1:
                    raise ValueError("the cartesian endpoint requires its complete selected base map")
                return node("functorAction", node(reindex, *parameters), receiver) if side == "source" else receiver
        if tag == "presentation":
            comparison, parameters, inverse = fields(arrow, tag, 3)
            if not isinstance(parameters, list) or type(inverse) is not bool:
                raise ValueError("a comparison endpoint requires ordered parameters and Boolean direction")
            if comparison == "cmp.rational_dual.translation":
                same(parameters, [], "the comparison endpoint's declaration parameters")
                use_y = (side == "source") == inverse
                return node("obj.sets.rational_dual_y" if use_y else "obj.sets.rational_dual_x")
            if comparison in {"cmp.sets.fin_reversal", "cmp.groups.cyclic_quotient_residue"}:
                if len(parameters) != 1:
                    raise ValueError("the comparison endpoint requires its selected size parameter")
                size = self.natural(parameters[0], "the comparison endpoint size")
                if comparison == "cmp.sets.fin_reversal":
                    return node("obj.sets.fin", size)
                quotient = (side == "source") != inverse
                return node("obj.groups.cyclic_quotient" if quotient else "obj.groups.cyclic", size)

        if tag in {"op.rings.add", "op.rings.mul", "op.rings.neg", "op.rings.pow"}:
            parameters = fields(arrow, tag, 2 if tag == "op.rings.pow" else 1)
            selected_ring = parameters[0]
            if tag == "op.rings.pow":
                self.natural(parameters[1], "the selected endpoint exponent")
            if side == "source" and tag in {"op.rings.add", "op.rings.mul"}:
                return node("objectProduct", selected_ring, selected_ring)
            return selected_ring
        if tag in {"op.monoids.mul", "op.additive_monoids.add"}:
            monoid, = fields(arrow, tag, 1)
            return node("objectProduct", monoid, monoid) if side == "source" else monoid
        if tag == "op.monoids.one":
            monoid, = fields(arrow, tag, 1)
            if side == "source":
                # A native reader does not manufacture the terminal point or
                # its inventory; the actual request supplies that comparison.
                raise Unsupported("the terminal endpoint needs its supplied point data")
            return monoid
        if tag == "op.groups.inverse":
            return fields(arrow, tag, 1)[0]
        if tag in {"mor.sets.equality", "op.linear_orders.le", "op.linear_orders.lt"}:
            receiver, = fields(arrow, tag, 1)
            return node("objectProduct", receiver, receiver) if side == "source" else node("obj.sets.truth_values")
        if tag == "op.modules.scalar_action":
            ring, module = fields(arrow, tag, 2)
            return node("objectProduct", ring, module) if side == "source" else module
        if tag == "mor.sets.bilin_module_pairing":
            _, values, formed = fields(arrow, tag, 3)
            return node("objectProduct", formed, formed) if side == "source" else values
        if tag == "mor.commutative_rings.integer_coefficients":
            ring, = fields(arrow, tag, 1)
            return node("obj.commutative_rings.integers") if side == "source" else ring
        if tag in {"mor.sets.rational_dual_x_constants", "mor.sets.rational_dual_y_constants"}:
            fields(arrow, tag, 0)
            if side == "source":
                return node("obj.sets.rationals")
            return node("obj.sets.rational_dual_x" if tag.endswith("_x_constants") else "obj.sets.rational_dual_y")
        if tag == "mor.sets.direct_image":
            source, target, _ = fields(arrow, tag, 3)
            return node("obj.sets.power_set", source if side == "source" else target)
        if tag in {"obj.sets.group_morphisms#application", "obj.sets.module_morphisms#application"}:
            object_id = tag.removesuffix("#application")
            parameters = fields(arrow, tag, self.morphism_objects[object_id])
            return (node("objectProduct", node(object_id, *parameters), parameters[-2])
                    if side == "source" else parameters[-1])
        if tag == "mor.sets.power_series_coefficient":
            ring, = fields(arrow, tag, 1)
            return (node("objectProduct", node("obj.sets.power_series", ring), node("obj.sets.naturals"))
                    if side == "source" else ring)
        if tag == "mor.sets.successor_power_series_terms":
            ring, = fields(arrow, tag, 1)
            return node("obj.sets.naturals") if side == "source" else node("obj.sets.power_series", ring)
        if tag == "mor.sets.fin_rev":
            dimension, = fields(arrow, tag, 1)
            return node("obj.sets.fin", self.natural(dimension, "the selected endpoint dimension"))
        if tag == "mor.sets.cyclic_quotient_map":
            modulus, = fields(arrow, tag, 1)
            self.natural(modulus, "the selected endpoint modulus")
            return node("obj.sets.integers") if side == "source" else node("obj.sets.cyclic_quotient", modulus)
        if tag in {"mor.sets.automorphism_forward", "mor.sets.automorphism_backward",
                   "mor.groups.automorphism_forward", "mor.groups.automorphism_backward"}:
            receiver, _ = fields(arrow, tag, 2)
            return receiver
        raise Unsupported("this complete declared endpoint has no additional native view")

    def product_factors(self, selected, components=None):
        """Consume either public product form without rewriting its descriptor."""
        tag = self.tag(selected)
        if tag == "objectProduct":
            return object_product(selected)
        if tag == "finiteData":
            original, _ = fields(selected, tag, 2)
            return self.product_factors(original, components)
        if tag == "morphismEndpoint":
            actual = self.endpoint_view(selected)
            if key(actual) == key(selected):
                raise Unsupported("the endpoint has no independently retained product context")
            factors = self.product_factors(actual)
            if components is None:
                return factors
            # An unnamed endpoint supplies no extra component spelling. Keep
            # actual typed/owned component fields, when supplied, instead of
            # replacing them by a native carrier view of a declaration parameter.
            retained = [retained_endpoint(component, "target", self.session)
                        for component in components]
            return tuple(factor if endpoint is None else endpoint
                         for factor, endpoint in zip(factors, retained))
        raise Unsupported("the selected endpoint is not a supported public product")

    def same_endpoint(self, actual, explicit, arrow, side, label):
        """Accept the exact declaration endpoint or an explicitly supplied field."""
        if explicit is not None and key(actual) == key(explicit):
            return
        if self.tag(actual) == "finiteData":
            original, _ = fields(actual, "finiteData", 2)
            inventory(actual)
            return self.same_endpoint(original, explicit, arrow, side, label)
        if self.tag(actual) == "morphismEndpoint":
            selected_arrow, selected_side = morphism_endpoint(actual)
            if key(selected_arrow) != key(arrow) and self.tag(selected_arrow) in {
                    "compose", "mediator", "point", "valueData", "typedMap"}:
                # Structural endpoint projections retain the original packet;
                # only their supplied field is used for this internal check.
                return self.same_endpoint(self.endpoint_view(actual), explicit,
                                          arrow, side, label)
            same(selected_arrow, arrow, label + " callable")
            same(selected_side, side, label + " selector")
        else:
            same(actual, explicit, label)
