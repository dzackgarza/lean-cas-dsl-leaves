"""Consume the published power-object callable fields inside existing requests.

The terminal and truth fields use their public declared point representations.
Membership, finite images and finite predicate subsets reuse the existing exact
Sage-set readers and complete native inventories. No operation is registered here.
"""

from wire import Callable, node, power_object_map


class PowerObjectInterfaces:
    def interpret_arrow(self, arrow, source, target):
        if self.tag(arrow) != "powerObjectMap":
            return super().interpret_arrow(arrow, source, target)
        _, field, parameters = power_object_map(arrow)
        expected_source, expected_target = self.power_endpoints(arrow)
        self.same_endpoint(source, expected_source, arrow, "source", "power-map source")
        self.same_endpoint(target, expected_target, arrow, "target", "power-map target")
        context = {"arrow": arrow, "source": source, "target": target}
        if field == "terminal":
            # This is the actual declared Fin(1)-valued map. It does not replace
            # another terminal comparison or manufacture a graph inventory.
            actual_target = self.endpoint_view(target) if self.tag(target) == "morphismEndpoint" else target
            selected_target = actual_target if self.tag(actual_target) == "finiteData" else expected_target
            points = self.finite_object(selected_target).points
            if len(points) != 1:
                raise ValueError("the supplied terminal target has no single computational point")
            point, = points
            self.finite_ordinal(point, 1)
            return Callable(source, target, lambda _, retained=(context, point): retained[1])
        if field == "truth":
            def truth(point, retained=context):
                self.finite_ordinal(point, 1)
                return True
            return Callable(source, target, truth)
        if field == "member":
            ambient, = parameters
            def member(pair, retained=context):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("membership requires the actual point and subset")
                subset = self.finite_subset(pair[1], ambient, retained)
                return bool(self.subset_key(pair[0], ambient) in subset.native)
            return Callable(source, target, member)
        if field == "image":
            original_source, ambient, original_map = parameters
            actual = self.function(original_map, original_source, ambient)
            points = self.finite_object(original_source).points
            context.update({"original": actual, "inventory": points})
            def subset(point, retained=context):
                self.finite_ordinal(point, 1)
                image = self.finite_subset([retained["original"].at_point(
                                                value, lambda data, selected: self.point(data, selected, None))
                                            for value in retained["inventory"]], ambient, retained)
                return self.session.keep(image)
            return Callable(source, target, subset)
        ambient, original_predicate = parameters
        predicate = self.function(original_predicate, ambient, node("obj.sets.truth_values"))
        points = self.finite_object(ambient).points
        context.update({"original": predicate, "inventory": points})
        def subset(point, retained=context):
            self.finite_ordinal(point, 1)
            selected = []
            for value in retained["inventory"]:
                answer = retained["original"].at_point(
                    value, lambda data, selected: self.point(data, selected, None))
                if type(answer) is not bool:
                    raise ValueError("the actual predicate result is not Boolean point data")
                if answer:
                    selected.append(value)
            return self.session.keep(self.finite_subset(selected, ambient, retained))
        return Callable(source, target, subset)
