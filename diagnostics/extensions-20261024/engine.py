"""A deliberately narrow Sage implementation of published extension declarations.

The only mathematical formulas below are documented in the independently supplied
declaration export. Sage supplies exact quotient-ring and linear algebra operations.
Wire readers retain the original complete object, action and presentation data.
"""

from dataclasses import dataclass

from sage.all import QQ, ZZ, PolynomialRing, matrix, vector

from cas_port import (
    admitted_point, constrained_point, construction_field, map_data,
    object_field, operation_expression, point_invocation,
    presentation_invocation, typed_map,
)
from wire import (Callable, NativeComposition, NativeIdentity, NativeMediator, Session, Unsupported,
                  fields, framed_callable, inventory, key, node, same)
from native_linear import LinearAction
from native_polynomial import (PolynomialAction, ProductModel, ScalarModel,
                               build as polynomial_action,
                               identity as polynomial_identity,
                               mediator as polynomial_mediator)


Q = node("obj.sets.rationals")
Z = node("obj.sets.integers")


@dataclass(frozen=True)
class Scalar:
    selected: object
    value: object


@dataclass(frozen=True)
class Module:
    """Native module structure, with its complete selected point representation."""

    native: object
    read: object
    write: object

    def zero(self):
        return self.write(self.native.zero())

    def add(self, x, y):
        return self.write(self.read(x) + self.read(y))

    def negate(self, x):
        return self.write(-self.read(x))

    def scale(self, a, x):
        return self.write(a * self.read(x))


@dataclass(frozen=True)
class Form:
    module: Module
    pairing: object
    context: object


class Engine:
    comparison = "cmp.rational_dual.translation"
    ring_operations = {"op.rings.add", "op.rings.mul", "op.rings.pow", "op.rings.neg"}
    rational_ids = {"obj.sets.rationals", "obj.rings.rationals", "obj.commutative_rings.rationals"}
    integer_ids = {"obj.sets.integers", "obj.rings.integers", "obj.commutative_rings.integers"}
    dual_x_ids = {"obj.sets.rational_dual_x", "obj.commutative_rings.rational_dual_x"}
    dual_y_ids = {"obj.sets.rational_dual_y", "obj.commutative_rings.rational_dual_y"}
    # These declared actions preserve underlying point and arrow data. This is an
    # explicit supported set, not a rule based on matching endpoint carriers.
    carrier_actions = {
        "fun.sets.identity", "fun.commutative_rings.ring",
        "fun.rings.additive_group", "fun.rings.multiplicative_monoid",
        "fun.additive_groups.to_groups",
        "fun.groups.monoid", "fun.monoids.semigroup",
        "fun.additive_monoids.underlying", "fun.modules.fibre_inclusion",
        "fun.modules.additive_group", "fun.modules.underlying",
        "fun.bilin_module.forget", "fun.bilin_module.change_value",
        "fun.linear_orders.forget",
    }

    def carrier_action(self, action):
        """Read only the explicitly supported published carrier actions."""
        tag = self.tag(action)
        if tag in self.carrier_actions:
            counts = {"fun.modules.fibre_inclusion": 1,
                      "fun.bilin_module.forget": 2,
                      "fun.bilin_module.change_value": 4}
            fields(action, tag, counts.get(tag, 0))
            return True
        if tag == "classifierForget":
            classifier, parameters = fields(action, tag, 2)
            if classifier in {"clf.sets.finite", "clf.magmas.associative",
                              "clf.sets.binary_operation"}:
                same(parameters, [], "classifier-forget declaration parameters")
                return True
        return False

    def __init__(self):
        self.session = Session()
        polynomial_x = PolynomialRing(QQ, "x")
        polynomial_y = PolynomialRing(QQ, "y")
        self.dual_x = polynomial_x.quotient(polynomial_x.gen() ** 2, "xbar")
        self.dual_y = polynomial_y.quotient((polynomial_y.gen() + 1) ** 2, "ybar")
        self.forward = self.dual_x.hom([self.dual_y.gen() + 1], self.dual_y)
        self.backward = self.dual_y.hom([self.dual_x.gen() - 1], self.dual_x)

    @staticmethod
    def tag(data):
        return data.get("ctor") if isinstance(data, dict) else None

    def ring(self, selected):
        tag = self.tag(selected)
        if tag in self.rational_ids | self.integer_ids | self.dual_x_ids | self.dual_y_ids:
            fields(selected, tag, 0)
            if tag in self.rational_ids:
                return QQ
            if tag in self.integer_ids:
                return ZZ
            return self.dual_x if tag in self.dual_x_ids else self.dual_y
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            if self.carrier_action(action):
                return self.ring(receiver)
        if tag == "morphismEndpoint":
            arrow, side = fields(selected, tag, 2)
            if self.tag(arrow) in {"mor.sets.rational_dual_x_constants", "mor.sets.rational_dual_y_constants"}:
                fields(arrow, self.tag(arrow), 0)
                if side == "source":
                    return QQ
                if side == "target":
                    return self.dual_x if self.tag(arrow).endswith("_x_constants") else self.dual_y
        raise Unsupported("this exact selected ring is outside the diagnostic implementation")

    def polynomial_model(self, selected):
        """Native coordinate models for the explicit supported scalar objects."""
        tag = self.tag(selected)
        if tag == "objectProduct":
            left, right = fields(selected, tag, 2)
            return ProductModel(self.polynomial_model(left), self.polynomial_model(right))
        if tag == "obj.modules.regular":
            coefficient, = fields(selected, tag, 1)
            return self.polynomial_model(coefficient)
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            if self.carrier_action(action):
                return self.polynomial_model(receiver)
        native = self.ring(selected)
        if native is QQ:
            kind = "rational"
        elif native is ZZ:
            kind = "integer"
        elif native is self.dual_x:
            kind = "dual_x"
        elif native is self.dual_y:
            kind = "dual_y"
        else:
            raise Unsupported("this scalar carrier has no implemented exact polynomial coordinate model")
        return ScalarModel(native, kind)

    def native_polynomial(self, data):
        if isinstance(data, PolynomialAction):
            return data
        if isinstance(data, NativeIdentity):
            return polynomial_identity(self.polynomial_model(data.source),
                                       self.polynomial_model(data.target),
                                       {"source": data.source, "target": data.target})
        if isinstance(data, NativeComposition):
            return self.native_polynomial(data.first).then(self.native_polynomial(data.second))
        if isinstance(data, NativeMediator):
            return polynomial_mediator(self.native_polynomial(data.left),
                                       self.native_polynomial(data.right),
                                       {"source": data.source, "target": data.target})
        if isinstance(data, LinearAction):
            context = data.context
            if isinstance(context, dict) and "source" in context and "target" in context:
                source_model = self.polynomial_model(context["source"])
                target_model = self.polynomial_model(context["target"])
            elif data.source.native is QQ and data.target.native is QQ:
                source_model = target_model = ScalarModel(QQ, "rational")
            else:
                raise Unsupported("this native matrix has no retained scalar polynomial endpoints")
            if (source_model.dimension != data.matrix.ncols()
                    or target_model.dimension != data.matrix.nrows()):
                raise Unsupported("the exact matrix and polynomial coordinate dimensions differ")
            def compute(value, coefficients):
                coordinates = source_model.encode_symbolic(coefficients, value)
                image = data.matrix * vector(coefficients, coordinates)
                return target_model.decode_symbolic(coefficients, image)
            return polynomial_action(source_model, target_model, compute,
                                     {"nativeMatrix": data, "selection": context})
        raise Unsupported("this callable has no complete native polynomial representation")

    @staticmethod
    def natural(data, label):
        if type(data) is not int or data < 0:
            raise ValueError(label + " requires a natural number")
        return data

    def scalar(self, data, selected, domain=None):
        parent = self.ring(selected)
        tag = self.tag(data)
        if tag == "valueData":
            return self.scalar(fields(data, tag, 1)[0], selected, domain)
        if tag == "opaqueData":
            native = self.session.get(data)
            if not isinstance(native, Scalar) or self.ring(native.selected) is not parent:
                raise ValueError("owned scalar has a different selected presentation")
            return native.value
        if tag == "element":
            original, expression = fields(data, tag, 2)
            if self.ring(original) is not parent:
                raise ValueError("point data uses a different selected ring presentation")
            return self.expression(expression, original, domain)
        if tag in {"point", "compose", "mediator", "typedMap", "pointView", "admittedPoint", "constrainedPoint"}:
            point = self.point(data, selected, domain)
            if key(point) == key(data):
                raise Unsupported("the scalar point has no supported computational data")
            return self.scalar(point, selected, domain)
        if parent is QQ:
            if not isinstance(data, list) or len(data) != 2:
                raise ValueError("a rational scalar requires its reduced two-field record")
            numerator, denominator = data
            if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
                raise ValueError("a rational record has invalid integer fields")
            if ZZ(numerator).gcd(denominator) != 1:
                raise ValueError("a rational record is not reduced")
            return QQ(numerator) / QQ(denominator)
        if parent is ZZ and type(data) is int:
            return ZZ(data)
        raise Unsupported("this scalar needs a published expression or an owned native value")

    def expression(self, expression, selected, domain=None):
        tag = self.tag(expression)
        parent = self.ring(selected)
        if tag == "numeral":
            n, = fields(expression, tag, 1)
            return parent(self.natural(n, "a numeral"))
        if tag == "generator":
            arguments = fields(expression, tag)
            if arguments or parent not in (self.dual_x, self.dual_y):
                raise Unsupported("this named generator is not implemented")
            return parent.gen()
        if tag in {"add", "mul"}:
            left, right = fields(expression, tag, 2)
            a = self.expression(left, selected, domain)
            b = self.expression(right, selected, domain)
            return a + b if tag == "add" else a * b
        if tag == "neg":
            return -self.expression(fields(expression, tag, 1)[0], selected, domain)
        if tag == "operationExpression":
            operation, parameters, operands = operation_expression(expression)
            if operation not in self.ring_operations or not parameters:
                raise Unsupported("this scalar operation expression is not implemented")
            operation_parent = self.ring(parameters[0])
            if operation_parent is not parent:
                raise ValueError("an operation expression changes the selected ring")
            values = [self.expression(value, selected, domain) for value in operands]
            return self.ring_operation(operation, parameters, values)
        if tag == "point":
            return self.scalar(self.point(expression, selected, domain), selected, domain)
        return self.scalar(expression, selected, domain)

    def encode_scalar(self, value, selected):
        parent = self.ring(selected)
        value = parent(value)
        if parent is QQ:
            return [int(value.numerator()), int(value.denominator())]
        if parent is ZZ:
            return int(value)
        return self.session.keep(Scalar(selected, value))

    def ring_operation(self, operation, parameters, values):
        expected_parameters = 2 if operation == "op.rings.pow" else 1
        if len(parameters) != expected_parameters:
            raise ValueError("the ring operation omits or adds a declaration parameter")
        self.ring(parameters[0])
        arity = 2 if operation in {"op.rings.add", "op.rings.mul"} else 1
        if len(values) != arity:
            raise ValueError("the ring operation has a different operand count")
        if operation == "op.rings.add":
            return values[0] + values[1]
        if operation == "op.rings.mul":
            return values[0] * values[1]
        if operation == "op.rings.neg":
            return -values[0]
        return values[0] ** self.natural(parameters[1], "the selected exponent")

    def finite_function_values(self, data, count):
        source = node("obj.sets.fin", self.natural(count, "the selected dimension"))
        if self.tag(data) == "valueData":
            data = fields(data, "valueData", 1)[0]
        if self.tag(data) == "element":
            selected, expression = fields(data, "element", 2)
            data = self.point(node("point", expression), selected, None)
        if self.tag(data) == "typedMap":
            actual_source, actual_target, body = typed_map(data)
            same(actual_source, source, "finite callable index object")
            call = self.function(body, actual_source, actual_target)
        elif self.tag(data) == "opaqueData":
            call = self.session.get(data)
            if not isinstance(call, Callable):
                raise Unsupported("the owned value is not an indexed callable")
            same(call.source, source, "owned finite callable index object")
        else:
            # The result type is independently fixed by the enclosing matrix or
            # vector declaration; this helper only checks the complete index set.
            from wire import graph_callable
            call = graph_callable(data, source, None)
        return [call(i) for i in range(count)]

    def read_vector(self, data, dimension, coefficient=Q):
        return vector(self.ring(coefficient), [
            self.scalar(value, coefficient)
            for value in self.finite_function_values(data, dimension)
        ])

    def write_vector(self, value, coefficient=Q):
        return [[i, self.encode_scalar(entry, coefficient)] for i, entry in enumerate(value)]

    def read_matrix(self, data, rows, columns, coefficient):
        row_data = self.finite_function_values(data, rows)
        values = [self.scalar(entry, coefficient) for row in row_data
                  for entry in self.finite_function_values(row, columns)]
        return matrix(self.ring(coefficient), rows, columns, values)

    def vector_module(self, dimension, coefficient=Q):
        dimension = self.natural(dimension, "the selected vector dimension")
        return Module(self.ring(coefficient) ** dimension,
                      lambda data: self.read_vector(data, dimension, coefficient),
                      lambda data: self.write_vector(data, coefficient))

    def regular_module(self, coefficient=Q):
        if self.ring(coefficient) is not QQ:
            raise Unsupported("this regular module has no implemented native representation")
        return Module(QQ, lambda data: self.scalar(data, coefficient),
                      lambda data: self.encode_scalar(data, coefficient))

    def module(self, selected):
        tag = self.tag(selected)
        if tag == "opaqueData":
            native = self.session.get(selected)
            if isinstance(native, Form):
                return native.module
            if isinstance(native, Module):
                return native
            raise Unsupported("the owned object has no implemented module structure")
        if tag == "obj.modules.vectors":
            coefficient, dimension = fields(selected, tag, 2)
            return self.vector_module(dimension, coefficient)
        if tag == "obj.sets.vectors":
            coefficient, dimension = fields(selected, tag, 2)
            return self.vector_module(dimension, coefficient)
        if tag == "obj.modules.regular":
            coefficient, = fields(selected, tag, 1)
            return self.regular_module(coefficient)
        if tag in self.rational_ids:
            fields(selected, tag, 0)
            return self.regular_module(selected)
        if tag == "objectProduct":
            left, right = fields(selected, tag, 2)
            left_module, right_module = self.module(left), self.module(right)
            if left_module.native is not QQ or right_module.native is not QQ:
                raise Unsupported("only the supplied product of two regular rational modules is implemented")
            def read(data):
                if not isinstance(data, list) or len(data) != 2:
                    raise ValueError("a product-module point requires both ordered components")
                return vector(QQ, [left_module.read(data[0]), right_module.read(data[1])])
            return Module(QQ ** 2, read, lambda data: [left_module.write(data[0]), right_module.write(data[1])])
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            action_tag = self.tag(action)
            if action_tag in {"fun.bilin_module.forget", "fun.bilin_module.change_value"}:
                self.carrier_action(action)
                return self.form(receiver).module
            if self.carrier_action(action):
                return self.module(receiver)
        if tag == "morphismEndpoint":
            arrow, side = fields(selected, tag, 2)
            if side not in {"source", "target"}:
                raise ValueError("a morphism endpoint has an invalid selector")
            atag = self.tag(arrow)
            if atag == "mor.modules.rectangular_linear_map":
                rows, columns, ring, _ = fields(arrow, atag, 4)
                return self.vector_module(columns if side == "source" else rows, ring)
            if atag == "mor.modules.row_linear_map":
                columns, ring, _ = fields(arrow, atag, 3)
                return self.vector_module(columns, ring) if side == "source" else self.regular_module(ring)
            return self.form(selected).module
        if tag == "subobjectApex":
            return self.module(self.arrow_record(fields(selected, tag, 1)[0])[0])
        if tag in {"constructionField", "constructionApex"}:
            return self.module(self.project_field(selected))
        if tag and tag.startswith("obj.bilin_module."):
            return self.form(selected).module
        raise Unsupported("this complete selected module has no implemented native representation")

    def form_from_grams(self, grams, context):
        gram_matrices = tuple(matrix(QQ, data) for data in grams)
        module = self.vector_module(gram_matrices[0].nrows())
        def pairing(left, right):
            x, y = module.read(left), module.read(right)
            values = [self.encode_scalar(x * gram * y, Q) for gram in gram_matrices]
            return values[0] if len(values) == 1 else values
        return Form(module, pairing, context)

    def form(self, selected):
        tag = self.tag(selected)
        if tag == "opaqueData":
            native = self.session.get(selected)
            if not isinstance(native, Form):
                raise ValueError("the owned object is not a complete formed module")
            return native
        grams = {
            "obj.bilin_module.rational_diagonal_2_3": ([[2, 0], [0, 3]],),
            "obj.bilin_module.degenerate_plane": ([[2, 2], [2, 2]],),
            "obj.bilin_module.degenerate_plane_target": ([[2, 0], [0, 5]],),
            "obj.bilin_module.degenerate_plane_with_dot": ([[2, 2], [2, 2]], [[1, 0], [0, 1]]),
        }
        if tag in grams:
            fields(selected, tag, 0)
            return self.form_from_grams(grams[tag], selected)
        if tag == "functorAction":
            action, receiver = fields(selected, tag, 2)
            if self.tag(action) == "fun.bilin_module.change_value":
                scalar, source_values, target_values, value_map = fields(action, self.tag(action), 4)
                if self.ring(scalar) is not QQ:
                    raise Unsupported("this diagnostic formed module requires rational scalars")
                original = self.form(receiver)
                change = self.function(value_map, source_values, target_values)
                return Form(original.module, lambda x, y: change(original.pairing(x, y)), selected)
        if tag == "morphismEndpoint":
            arrow, side = fields(selected, tag, 2)
            atag = self.tag(arrow)
            if side not in {"source", "target"}:
                raise ValueError("a morphism endpoint has an invalid selector")
            if atag == "mor.bilin_module.degenerate_plane_map":
                fields(arrow, atag, 0)
                return self.form_from_grams(([[2, 2], [2, 2]],) if side == "source"
                                           else ([[2, 0], [0, 5]],), selected)
            if atag == "mor.bilin_module.degenerate_plane_cone":
                fields(arrow, atag, 0)
                return self.form_from_grams(([[0, 0], [0, 0]],) if side == "source"
                                           else ([[2, 2], [2, 2]],), selected)
            if atag == "mor.bilin_module.degenerate_plane_paired_cone":
                fields(arrow, atag, 0)
                return self.form_from_grams(([[0, 0], [0, 0]], [[18, -12], [-12, 8]])
                                           if side == "source" else
                                           ([[2, 2], [2, 2]], [[1, 0], [0, 1]]), selected)
        if tag == "subobjectApex":
            return self.form(self.arrow_record(fields(selected, tag, 1)[0])[0])
        raise Unsupported("this exact formed object is outside the diagnostic implementation")

    def arrow_record(self, data):
        tag = self.tag(data)
        if tag == "valueData":
            return self.arrow_record(fields(data, tag, 1)[0])
        if tag in {"arrow", "subobject"}:
            return fields(data, tag, 3)
        if tag == "objectPresentation":
            _, actual = fields(data, tag, 2)
            return self.arrow_record(actual)
        if tag == "liftedSubobject":
            _, _, route, steps = fields(data, tag, 4)
            if not steps or len(route) != len(steps):
                raise ValueError("the completed lift omits its actual component data")
            step = steps[0]
            lift_id, action, source, base, outputs = fields(step, "liftStep", 5)
            if lift_id != route[0] or not isinstance(step.get("parameters"), list) or len(outputs) != 4:
                raise ValueError("the completed lift changes its selected step context")
            source_object = fields(source, "arrow", 3)[0]
            return [outputs[0], source_object, outputs[1]]
        raise Unsupported("no complete returned Arrow record is supplied")

    def project_field(self, data):
        tag = self.tag(data)
        if tag == "constructionApex":
            limit, diagram, packet = fields(data, tag, 3)
            index = 0
        elif tag == "constructionLeg":
            limit, diagram, packet, leg = fields(data, tag, 4)
            if limit != "lim.sets.product":
                raise Unsupported("this diagram-leg indexing has no native constructor adapter")
            if type(leg) is not int or leg not in (0, 1):
                raise ValueError("the selected binary-product leg has an invalid diagram index")
            fields(diagram, "pair", 2)
            index = leg + 1
        else:
            limit, diagram, packet, index = construction_field(data)
        if self.tag(packet) == "valueData":
            packet = fields(packet, "valueData", 1)[0]
        while self.tag(packet) == "createdCone":
            lift, actual_diagram, packet = fields(packet, "createdCone", 3)
            same(actual_diagram, diagram, "created construction's retained source diagram")
            if lift != "lift.finite_sets.pullbacks":
                raise Unsupported("this selected creation action is outside the specimen")
        tag = self.tag(packet)
        if tag not in {"cone", "cocone"}:
            raise ValueError("a construction projection requires the complete returned packet")
        ports = fields(packet, tag)
        if index >= len(ports):
            raise ValueError("the returned construction omits the selected data port")
        return ports[index]

    def closed_domain(self, domain):
        return self.tag(domain) == "obj.sets.fin" and fields(domain, "obj.sets.fin", 1) == [1]

    def point(self, data, target, domain):
        tag = self.tag(data)
        if self.tag(target) == "obj.sets.maps" and tag in {"typedMap", "compose", "mediator"}:
            # This is a complete function-valued point, not a point arrow from
            # the generalized domain into the function object.
            return data
        if isinstance(data, list) and self.tag(target) == "objectProduct":
            left_target, right_target = fields(target, "objectProduct", 2)
            if len(data) != 2:
                raise ValueError("a product point omits an ordered component")
            return [self.point(data[0], left_target, domain),
                    self.point(data[1], right_target, domain)]
        if tag == "valueData":
            return self.point(fields(data, tag, 1)[0], target, domain)
        if tag == "pointView":
            actual_target, original, original_domain = fields(data, tag, 3)
            same(actual_target, target, "point-view target")
            if domain is not None:
                same(original_domain, domain, "point-view domain")
            original_target, _ = fields(original, "element", 2)
            return self.point(original, original_target, original_domain)
        if tag == "admittedPoint":
            _, _, original_domain, original_target, admitted, original = admitted_point(data)
            same(admitted, target, "admitted target")
            if domain is not None:
                same(original_domain, domain, "admitted point domain")
            return self.point(original, original_target, original_domain)
        if tag == "constrainedPoint":
            _, original_domain, original_target, constrained, original = constrained_point(data)
            same(constrained, target, "constrained target")
            if domain is not None:
                same(original_domain, domain, "constrained point domain")
            return self.point(original, original_target, original_domain)
        if tag == "element":
            selected, expression = fields(data, tag, 2)
            if self.tag(expression) == "point":
                return self.point(expression, selected, domain)
            return self.encode_scalar(self.expression(expression, selected, domain), selected)
        if tag == "point":
            arrow, = fields(data, tag, 1)
            if domain is None or not self.closed_domain(domain):
                raise Unsupported("a closed point needs its supplied terminal domain")
            return self.function(arrow, domain, target)(inventory(domain)[0])
        if tag == "mediator":
            left, right = fields(data, tag, 2)
            left_target, right_target = fields(target, "objectProduct", 2)
            return [self.point(left, left_target, domain), self.point(right, right_target, domain)]
        if tag in {"compose", "typedMap"}:
            if domain is None or not self.closed_domain(domain):
                raise Unsupported("a point arrow needs its actual generalized domain")
            return self.function(data, domain, target)(inventory(domain)[0])
        return data

    def function(self, data, source, target):
        return framed_callable(data, source, target, self.session, self.interpret_arrow)

    def intermediate(self, arrow, fallback=None):
        tag = self.tag(arrow)
        if tag == "valueData":
            return self.intermediate(fields(arrow, tag, 1)[0], fallback)
        if tag == "opaqueData":
            actual = self.session.get(arrow)
            if not isinstance(actual, Callable):
                raise ValueError("the owned composition datum is not a callable")
            return actual.target
        if tag == "typedMap":
            return typed_map(arrow)[1]
        if tag == "identity":
            return fields(arrow, tag, 2)[1]
        if tag == "element":
            return fields(arrow, tag, 2)[0]
        if tag == "point":
            return self.intermediate(fields(arrow, tag, 1)[0], fallback)
        if tag == "compose":
            return self.intermediate(fields(arrow, tag, 2)[1], fallback)
        if tag == "presentation":
            comparison, parameters, inverse = fields(arrow, tag, 3)
            if comparison == self.comparison and parameters == [] and type(inverse) is bool:
                return node("obj.sets.rational_dual_x" if inverse else "obj.sets.rational_dual_y")
        if tag == "generator":
            object_id, parameters = fields(arrow, tag, 2)
            if object_id in self.dual_x_ids | self.dual_y_ids:
                return node(object_id, *parameters)
        if tag in {"mor.sets.rational_dual_x_constants", "mor.sets.rational_dual_y_constants"}:
            return node("obj.sets.rational_dual_x" if tag.endswith("_x_constants") else "obj.sets.rational_dual_y")
        if tag in {"arrowHom", "subobjectInclusion"}:
            return self.arrow_record(fields(arrow, tag, 1)[0])[1]
        if tag in {"constructionField", "constructionLeg"}:
            port = self.project_field(arrow)
            if self.tag(port) == "typedMap":
                return typed_map(port)[1]
        if fallback is not None:
            return fallback
        raise Unsupported("the composition needs the supplied typed intermediate endpoint")

    def callable_domain(self, data):
        """Read a retained domain; do not infer it from a sampled point or carrier."""
        tag = self.tag(data)
        if tag == "valueData":
            return self.callable_domain(fields(data, tag, 1)[0])
        if tag == "typedMap":
            return typed_map(data)[0]
        if tag == "identity":
            source, target = fields(data, tag, 2)
            same(source, target, "identity endpoints")
            return source
        if tag == "opaqueData":
            actual = self.session.get(data)
            return actual.source if isinstance(actual, Callable) else None
        if tag == "compose":
            return self.callable_domain(fields(data, tag, 2)[0])
        if tag == "point":
            return self.callable_domain(fields(data, tag, 1)[0])
        return None

    def callable_argument(self, argument, domain, source):
        """Distinguish an explicit generalized arrow from a closed scalar value.

        In particular, identity(X, X) remains a whole-domain request when X is
        Fin(1). A function-valued point has its own different endpoint fields.
        """
        tag = self.tag(argument)
        if tag == "valueData":
            return self.callable_argument(fields(argument, tag, 1)[0], domain, source)
        if tag in {"typedMap", "identity"}:
            actual_source, actual_target = (typed_map(argument)[:2] if tag == "typedMap"
                                            else fields(argument, tag, 2))
            return key(actual_source) == key(domain) and key(actual_target) == key(source)
        if tag == "opaqueData":
            actual = self.session.get(argument)
            return (isinstance(actual, Callable) and key(actual.source) == key(domain)
                    and key(actual.target) == key(source))
        if tag in {"compose", "point"}:
            actual_domain = self.callable_domain(argument)
            if actual_domain is not None:
                return (key(actual_domain) == key(domain)
                        and key(self.intermediate(argument)) == key(source))
        return tag == "finiteGraph" and self.tag(source) != "obj.sets.maps"

    def postcompose(self, original, action):
        same(original.target, action.source, "actual callable composition endpoint")
        native = (NativeComposition(original.native, action.native)
                  if original.native is not None and action.native is not None else None)
        return Callable(original.source, action.target,
                        lambda point: action(original(point)), native)

    def apply_comparison(self, action, argument):
        domain = self.callable_domain(argument)
        if domain is None:
            return action(argument)
        original = self.function(argument, domain, action.source)
        return self.session.keep(self.postcompose(original, action))

    def interpret_arrow(self, arrow, source, target):
        tag = self.tag(arrow)
        if tag == "compose":
            first, second = fields(arrow, tag, 2)
            middle = self.intermediate(first)
            f, g = self.function(first, source, middle), self.function(second, middle, target)
            native = NativeComposition(f.native, g.native) if f.native is not None and g.native is not None else None
            return Callable(source, target, lambda value: g(f(value)), native)
        if tag == "element":
            if not self.closed_domain(source):
                raise Unsupported("a closed element cannot replace a generalized-domain callable")
            return Callable(source, target, lambda _: self.point(arrow, target, source))
        if tag == "point":
            return self.function(fields(arrow, tag, 1)[0], source, target)
        if tag == "presentation":
            comparison, parameters, inverse = fields(arrow, tag, 3)
            if comparison != self.comparison:
                raise Unsupported("this registered comparison is outside the specimen")
            return self.comparison_callable(parameters, inverse, source, target)
        if tag == "map":
            action, original = fields(arrow, tag, 2)
            if not self.carrier_action(action):
                raise Unsupported("this selected functor map is outside the specimen")
            original_domain = self.callable_domain(original)
            if original_domain is not None:
                old_source, old_target = original_domain, self.intermediate(original)
            elif self.tag(original) == "typedMap":
                old_source, old_target, _ = typed_map(original)
            elif self.tag(original) == "opaqueData":
                retained = self.session.get(original)
                if not isinstance(retained, Callable):
                    raise ValueError("the mapped owned datum is not a callable")
                old_source, old_target = retained.source, retained.target
            elif self.tag(source) == "functorAction" and self.tag(target) == "functorAction":
                source_action, old_source = fields(source, "functorAction", 2)
                target_action, old_target = fields(target, "functorAction", 2)
                same(source_action, action, "mapped source action")
                same(target_action, action, "mapped target action")
            else:
                # Preserve a named declared comparison's actual action while
                # interpreting its selected structural view at the supplied ends.
                old_source, old_target = source, target
            original_callable = self.function(original, old_source, old_target)
            return Callable(source, target, original_callable, original_callable.native)
        if tag in {"arrowHom", "subobjectInclusion"}:
            receiver, = fields(arrow, tag, 1)
            actual_source, actual_target, actual_map = self.arrow_record(receiver)
            actual = self.function(actual_map, actual_source, actual_target)
            return Callable(source, target, actual, actual.native)
        if tag in {"constructionField", "constructionLeg"}:
            actual_map = self.project_field(arrow)
            actual_source, actual_target, _ = typed_map(actual_map)
            actual = self.function(actual_map, actual_source, actual_target)
            return Callable(source, target, actual, actual.native)
        if tag == "generator":
            object_id, parameters = fields(arrow, tag, 2)
            selected = node(object_id, *parameters)
            parent = self.ring(selected)
            if parent not in (self.dual_x, self.dual_y) or parameters:
                raise Unsupported("the selected generator is outside the specimen")
            if self.ring(target) is not parent:
                raise ValueError("the named generator has a different target presentation")
            return Callable(source, target, lambda _: self.encode_scalar(parent.gen(), target))
        if tag == "objectField":
            object_id, field, parameters = object_field(arrow)
            if object_id in self.dual_x_ids | self.dual_y_ids and field in {"presentation", "inversePresentation"}:
                if parameters:
                    raise ValueError("the fixed dual-number object has no parameters")
                expected = self.dual_x if object_id in self.dual_x_ids else self.dual_y
                if self.ring(source) is not expected or self.ring(target) is not expected:
                    raise ValueError("the selected carrier identification changes presentation")
                return Callable(source, target, lambda value: value, NativeIdentity(source, target))
            raise Unsupported("this published object field is outside the specimen")
        if tag in self.ring_operations:
            parameters = fields(arrow, tag)
            native = None
            try:
                source_model, target_model = self.polynomial_model(source), self.polynomial_model(target)
            except Unsupported:
                pass
            else:
                def symbolic(value, coefficients):
                    values = list(value) if tag in {"op.rings.add", "op.rings.mul"} else [value]
                    return self.ring_operation(tag, parameters, values)
                native = polynomial_action(source_model, target_model, symbolic,
                                           {"arrow": arrow, "source": source, "target": target})
            def compute(value):
                if tag in {"op.rings.add", "op.rings.mul"}:
                    values = self.point(value, source, None)
                    if not isinstance(values, list) or len(values) != 2:
                        raise ValueError("a binary ring operation requires both operands")
                else:
                    values = [value]
                scalars = [self.scalar(x, parameters[0]) for x in values]
                return self.encode_scalar(self.ring_operation(tag, parameters, scalars), target)
            return Callable(source, target, compute, native)
        if tag in {"mor.sets.rational_dual_x_constants", "mor.sets.rational_dual_y_constants"}:
            fields(arrow, tag, 0)
            expected = self.dual_x if tag.endswith("_x_constants") else self.dual_y
            if self.ring(target) is not expected or self.ring(source) is not QQ:
                raise ValueError("the coefficient map has different selected endpoints")
            target_model = self.polynomial_model(target)
            native = polynomial_action(self.polynomial_model(source), target_model,
                                       lambda value, coefficients: target_model.symbolic_ring(coefficients)(value),
                                       {"arrow": arrow, "source": source, "target": target})
            return Callable(source, target, lambda value: self.encode_scalar(expected(self.scalar(value, source)), target), native)
        if tag in {"mor.modules.rectangular_linear_map", "mor.modules.row_linear_map"}:
            if tag == "mor.modules.rectangular_linear_map":
                rows, columns, coefficient, data = fields(arrow, tag, 4)
            else:
                columns, coefficient, data = fields(arrow, tag, 3)
                rows = 1
            native_matrix = self.read_matrix(data, rows, columns, coefficient)
            if native_matrix.base_ring() is QQ:
                source_module = self.module(source)
                target_module = self.module(target)
                native = LinearAction(native_matrix, source_module, target_module,
                                      {"arrow": arrow, "source": source, "target": target,
                                       "coefficient": coefficient})
                return Callable(source, target, native, native)
            def compute(value):
                image = native_matrix * self.read_vector(value, columns, coefficient)
                return self.encode_scalar(image[0], coefficient) if tag == "mor.modules.row_linear_map" else self.write_vector(image, coefficient)
            return Callable(source, target, compute)
        if tag in {"mor.bilin_module.degenerate_plane_map", "mor.bilin_module.degenerate_plane_cone", "mor.bilin_module.degenerate_plane_paired_cone"}:
            fields(arrow, tag, 0)
            native_matrix = matrix(QQ, [[1, 1], [0, 0]] if tag.endswith("_map") else [[3, -2], [-3, 2]])
            native = LinearAction(native_matrix, self.module(source), self.module(target),
                                  {"arrow": arrow, "source": source, "target": target})
            return Callable(source, target, native, native)
        if tag == "mor.sets.bilin_module_pairing":
            scalar, values, selected = fields(arrow, tag, 3)
            if self.ring(scalar) is not QQ:
                raise Unsupported("this selected pairing is not over rational scalars")
            form = self.form(selected)
            def compute(value):
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError("a pairing requires both actual vector points")
                return form.pairing(value[0], value[1])
            return Callable(source, target, compute)
        if tag == "mor.sets.equality":
            selected, = fields(arrow, tag, 1)
            def compute(value):
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError("equality requires both actual supplied points")
                return self.equal(value[0], value[1], selected)
            return Callable(source, target, compute)
        raise Unsupported("this complete declared callable is outside the specimen")

    def comparison_callable(self, parameters, inverse, source, target):
        if parameters != [] or type(inverse) is not bool:
            raise ValueError("the fixed comparison requires empty parameters and Boolean orientation")
        source_parent, target_parent = (self.dual_y, self.dual_x) if inverse else (self.dual_x, self.dual_y)
        if self.ring(source) is not source_parent or self.ring(target) is not target_parent:
            raise ValueError("the comparison changes its selected presentation endpoints")
        native = self.backward if inverse else self.forward
        target_model = self.polynomial_model(target)
        def symbolic(value, coefficients):
            image = target_model.symbolic_ring(coefficients)
            generator_image = image.gen() - 1 if inverse else image.gen() + 1
            return value.parent().hom([generator_image], image)(value)
        representation = polynomial_action(self.polynomial_model(source), target_model, symbolic,
                                            {"comparison": self.comparison, "parameters": parameters,
                                             "inverse": inverse, "source": source, "target": target,
                                             "nativeHomomorphism": native})
        return Callable(source, target, lambda value: self.encode_scalar(native(self.scalar(value, source)), target), representation)

    def equal(self, left, right, selected):
        try:
            self.ring(selected)
        except Unsupported:
            pass
        else:
            return bool(self.scalar(left, selected) == self.scalar(right, selected))
        if self.tag(selected) == "objectProduct":
            first, second = fields(selected, "objectProduct", 2)
            if not isinstance(left, list) or not isinstance(right, list) or len(left) != 2 or len(right) != 2:
                raise ValueError("a product comparison omits a component")
            return self.equal(left[0], right[0], first) and self.equal(left[1], right[1], second)
        native_module = self.module(selected)
        return bool(native_module.read(left) == native_module.read(right))

    def point_application(self, operation, packet):
        _, parameters, arrow, domain, source, target, argument = point_invocation(packet, operation)
        if self.tag(arrow) == operation:
            same(fields(arrow, operation), parameters, "callable declaration parameters")
        action = self.function(arrow, source, target)
        if self.closed_domain(domain) and not self.callable_argument(argument, domain, source):
            return action(self.point(argument, source, domain))
        original = self.function(argument, domain, source)
        # A returned callable is the actual composite on the complete original
        # domain. Keeping it owned preserves native metadata and dependencies,
        # including finite and singleton domains, without materializing samples.
        return self.session.keep(self.postcompose(original, action))

    def presentation_application(self, packet):
        parameters, inverse, source, target, argument = presentation_invocation(packet)
        action = self.comparison_callable(parameters, inverse, source, target)
        return self.apply_comparison(action, argument)
