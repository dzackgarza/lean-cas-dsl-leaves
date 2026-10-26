"""Computational observation of actual data at a complete selected public set.

Sage/Python value equality supplies an untrusted Boolean answer. A result is no
proposition, certificate, comparison of selected structures, or acceptance claim.
"""

import operator

from primitive_actions import Unsupported, fields, inline, record, tag
from point_calls import EQUALITY, MULTIPLY, PointCall, wire


class Equality(PointCall):
    operation = EQUALITY
    result_field = "Observation.callable"

    def __init__(self, session, packet):
        super().__init__(session, packet)
        left, right = self.product_factors(self.source)
        wire.same(left, self.selected, "equality's selected left set")
        wire.same(right, self.selected, "equality's selected right set")
        fields(self.endpoint_view(self.target), "obj.sets.truth_values", 0)

    def unwrapped(self, data, selected):
        data = inline(data)
        while tag(data) == "element":
            owner, expression = fields(data, "element", 2)
            self.check_owner(owner, selected)
            data = inline(expression)
        return data

    def equal(self, left, right, selected):
        view = self.endpoint_view(selected)
        kind = tag(view)
        left, right = self.resolve_value(left, selected), self.resolve_value(right, selected)
        if kind == "objectProduct":
            a, b = self.product_factors(selected)
            l0, l1 = record(self.unwrapped(left, selected), "left product point", 2)
            r0, r1 = record(self.unwrapped(right, selected), "right product point", 2)
            return self.equal(l0, r0, a) and self.equal(l1, r1, b)
        if kind == "obj.sets.truth_values":
            fields(view, kind, 0)
            l, r = self.unwrapped(left, selected), self.unwrapped(right, selected)
            if type(l) is not bool or type(r) is not bool:
                raise ValueError("truth-value points require JSON booleans")
            return operator.eq(l, r)
        if kind == "obj.sets.maps":
            domain, codomain = fields(view, kind, 2)
            f = self.function(self.unwrapped(left, selected), domain, codomain)
            g = self.function(self.unwrapped(right, selected), domain, codomain)
            # Only an actual complete inventory licenses this finite reader.
            # No finite sample or callable identity stands for an infinite map.
            return all(self.equal(f(point), g(point), codomain) for point in self.inventory(domain))
        points = self.point_context(selected)
        return bool(operator.eq(points.read(left), points.read(right)))

    def observe(self, pair):
        pair = inline(pair)
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("equality requires both ordered argument fields")
        left, right = pair
        return bool(self.equal(left, right, self.selected))

    def interpret(self, arrow, source, target):
        if tag(arrow) == EQUALITY:
            self.selection(arrow)
            return wire.Callable(source, target, self.observe)
        if tag(arrow) == MULTIPLY:
            from monoid_multiplication import Multiplication
            actual = Multiplication.at_arrow(self.session, self.packet, arrow, source, target)
            return wire.Callable(source, target, actual.product)
        raise Unsupported("this selected-set callable has no implemented reader")

    def result_data(self, data):
        if type(inline(data)) is not bool:
            raise ValueError("an equality observation requires a JSON boolean")
        return inline(data)
