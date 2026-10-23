#!/usr/bin/env python3
"""Small public-contract-only adapter around Sage/passagemath computations.

This program supplies computational data. It supplies no mathematical declarations,
proofs, certificates, acceptance assertions, or implementation-selected semantics.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile


def node(tag, *args):
    return {"ctor": tag, "args": list(args)}


def fields(value, tag, count=None):
    if not isinstance(value, dict) or value.get("ctor") != tag:
        raise ValueError("expected the public %s envelope" % tag)
    result = value.get("args")
    if not isinstance(result, list) or (count is not None and len(result) != count):
        raise ValueError("incorrect ordered fields for %s" % tag)
    return result


def tag_of(value):
    return value.get("ctor") if isinstance(value, dict) else None


def unbox(value):
    while tag_of(value) == "valueData":
        value, = fields(value, "valueData", 1)
    return value


def natural(value):
    if type(value) is not int or value < 0:
        raise ValueError("expected natural-number data")
    return value


def json_key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def load_public_port(contract_path):
    """Load exactly the helper selected by the host, without kernel imports."""
    root = Path(contract_path).expanduser().resolve(strict=True)
    helper = root / "python" / "cas_port.py"
    spec = importlib.util.spec_from_file_location("diagnostic_public_cas_port", helper)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the configured public Python helper")
    port = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(port)
    finally:
        sys.dont_write_bytecode = previous
    return port


@dataclass
class NativeEntry:
    value: object
    descriptor: object
    domain: object
    source_parent: object = None
    callable: bool = False


@dataclass
class NativeUnitData:
    # These are the supplied computational fields, never unit-membership evidence.
    monoid: object
    value: object
    inverse: object = None


class SageDiagnostic:
    NAME = "sage-v1-diagnostic"
    VERSION = "0.4.0"
    POINT_OPERATIONS = (
        "mor.sets.matrix_rows",
        "mor.sets.matrix_charpoly",
        "obj.sets.matrices#application",
        "mor.sets.polynomial_derivative",
        "mor.sets.polynomial_degree",
        "mor.sets.polynomial_own_evaluation",
        "obj.sets.polynomials#application",
        "op.rings.add",
        "op.rings.mul",
        "op.rings.pow",
        "op.rings.neg",
        "mor.sets.equality",
        "mor.sets.divide",
        "mor.sets.f9_x_constants",
        "mor.sets.f9_y_constants",
        "mor.sets.tuple_empty",
        "mor.sets.tuple_cons",
    )
    F9_OBJECTS = {
        "obj.sets.f9_x": 0,
        "obj.commutative_rings.f9_x": 0,
        "obj.sets.f9_y": 1,
        "obj.commutative_rings.f9_y": 1,
    }
    FORGET_FUNCTORS = (
        "fun.sets.identity",
        "fun.semirings.forget",
        "fun.commutative_rings.ring",
        "fun.rings.multiplicative_monoid",
        "fun.monoids.semigroup",
    )
    FORGET_CLASSIFIERS = ("clf.magmas.associative", "clf.sets.binary_operation", "clf.sets.finite")
    FIN_OBJECTS = ("obj.sets.fin", "obj.finite_sets.fin")
    SEMIRING_OPERATIONS = ("op.semirings.add", "op.semirings.mul", "op.semirings.pow")
    SCALARS = {
        "obj.sets.naturals": "naturals",
        "obj.semirings.naturals": "naturals",
        "obj.sets.integers": "integers",
        "obj.rings.integers": "integers",
        "obj.commutative_rings.integers": "integers",
        "obj.sets.rationals": "rationals",
        "obj.rings.rationals": "rationals",
        "obj.commutative_rings.rationals": "rationals",
        "obj.sets.integers_mod": "residues",
        "obj.rings.integers_mod": "residues",
        "obj.commutative_rings.integers_mod": "residues",
    }

    def __init__(self, port):
        # All mathematical computation below uses these existing engine objects.
        from sage.all import (QQ, ZZ, NN, Zmod, GF, PolynomialRing, MatrixSpace,
                              Family, FiniteEnumeratedSet, cartesian_product,
                              infinity, matrix, vector)
        from sage.sets.disjoint_union_enumerated_sets import DisjointUnionEnumeratedSets
        from sage.version import version
        self.port = port
        self.QQ, self.ZZ, self.NN, self.Zmod = QQ, ZZ, NN, Zmod
        self.Family, self.bottom = Family, -infinity
        self.degrees = DisjointUnionEnumeratedSets(
            [NN, FiniteEnumeratedSet([-infinity])], facade=True, keepkey=False)
        self.GF = GF
        self.PolynomialRing, self.MatrixSpace = PolynomialRing, MatrixSpace
        self.FiniteEnumeratedSet = FiniteEnumeratedSet
        self.cartesian_product, self.matrix, self.vector = cartesian_product, matrix, vector
        self.engine_version = version
        self._owned = {}
        self._session_prefix = secrets.token_hex(16)
        self._sequence = 0
        self._f9 = None

    def operations(self):
        result = {op: (lambda request, op=op: self.apply(op, request))
                  for op in self.POINT_OPERATIONS}
        result["lim.sets.product"] = self.product
        result["cmp.f9.translation"] = self.comparison
        return result

    def f9_presentations(self):
        if self._f9 is None:
            # These are parameters of the independently published presentations,
            # not inferred relations or an engine-selected abstract GF(9).
            # Source: upstream PolynomialPresentation at ee957329414a58759d26e23fa22e8d0a31040fc8.
            base = self.GF(3)
            polynomials = self.PolynomialRing(base, "t")
            t = polynomials.gen()
            first = self.GF(9, "fx", modulus=t ** 2 + 1)
            second = self.GF(9, "fy", modulus=t ** 2 + t + 2)
            forward = first.hom([second.gen() + 2], second)
            backward = second.hom([first.gen() - 2], first)
            self._f9 = (first, second, forward, backward)
        return self._f9

    def native_coerce(self, parent, value):
        if self._f9 is not None and hasattr(value, "parent"):
            actual = value.parent()
            if actual in self._f9[:2] and parent in self._f9[:2] and actual is not parent:
                raise ValueError("distinct F9 presentations require their retained comparison map")
        return parent(value)

    def require_forget_edge(self, edge):
        if any(edge == node(name) for name in self.FORGET_FUNCTORS):
            return
        if any(edge == node("classifierForget", name, []) for name in self.FORGET_CLASSIFIERS):
            return
        raise NotImplementedError("this structural action has no diagnostic adapter")

    def own(self, value, descriptor, domain, *, source_parent=None, callable=False):
        self._sequence += 1
        token = "%s:%d" % (self._session_prefix, self._sequence)
        self._owned[token] = NativeEntry(value, descriptor, domain, source_parent, callable)
        return self.port.opaque_data(token)

    def entry(self, data):
        token, = fields(data, "opaqueData", 1)
        if not isinstance(token, str) or not token:
            raise ValueError("an opaque token must be a nonempty string")
        if token not in self._owned:
            raise ValueError("opaque data are not owned by this live connection")
        return self._owned[token]

    def carrier_descriptor(self, descriptor):
        # Only the explicitly supported published forget actions are lowered.
        # Unknown actions are not erased or guessed from a native carrier.
        if tag_of(descriptor) == "functorAction":
            edge, source = fields(descriptor, "functorAction", 2)
            self.require_forget_edge(edge)
            return self.carrier_descriptor(source)
        if tag_of(descriptor) == "constructionApex":
            operation, diagram, complete_cone = fields(descriptor, "constructionApex", 3)
            actual_apex, _left, _right = self.product_cone(operation, diagram, complete_cone)
            return self.carrier_descriptor(actual_apex)
        return descriptor

    def product_cone(self, operation, diagram, data):
        """Read the returned fields through the explicitly published creation action."""
        if operation != "lim.sets.product":
            raise NotImplementedError("only returned product cones are supported")
        targets = fields(diagram, "pair", 2)
        data = unbox(data)
        if tag_of(data) == "createdCone":
            lift, source_diagram, target_cone = fields(data, "createdCone", 3)
            if lift != "lift.finite_sets.pullbacks":
                raise NotImplementedError("this creation lift has no diagnostic adapter")
            if source_diagram != diagram:
                raise ValueError("a created cone changed its complete source diagram")
            # The published row selects finite-set forgetting. Read its actual
            # target fields; do not manufacture a preferred target-apex spelling.
            for selected in targets:
                self.parent(selected)
            target_cone = unbox(target_cone)
            if tag_of(target_cone) == "createdCone":
                _lift, inner_diagram, _cone = fields(target_cone, "createdCone", 3)
                return self.product_cone(operation, inner_diagram, target_cone)
            data, targets = target_cone, None
        apex, left, right = fields(data, "cone", 3)
        for i, leg in enumerate((left, right)):
            actual_source, actual_target, _callable = self.port.typed_map(unbox(leg))
            if actual_source != apex or (targets is not None and actual_target != targets[i]):
                raise ValueError("a returned product leg changed its complete endpoints")
            self.parent(actual_target)
        return apex, left, right

    def parent(self, descriptor):
        descriptor = self.carrier_descriptor(descriptor)
        tag = tag_of(descriptor)
        args = fields(descriptor, tag)
        kind = self.SCALARS.get(tag)
        if kind == "naturals" and not args:
            return self.NN
        if kind == "integers" and not args:
            return self.ZZ
        if kind == "rationals" and not args:
            return self.QQ
        if kind == "residues" and len(args) == 1:
            return self.Zmod(natural(args[0]))
        if tag in self.F9_OBJECTS and not args:
            return self.f9_presentations()[self.F9_OBJECTS[tag]]
        if tag in self.FIN_OBJECTS and len(args) == 1:
            return self.FiniteEnumeratedSet([self.ZZ(i) for i in range(natural(args[0]))])
        if tag == "obj.sets.degrees" and not args:
            return self.degrees
        if tag == "obj.sets.truth_values" and not args:
            return self.FiniteEnumeratedSet([False, True])
        if tag in ("obj.sets.polynomials", "obj.rings.polynomials") and len(args) == 1:
            return self.PolynomialRing(self.parent(args[0]), "x")
        if tag == "obj.sets.matrices" and len(args) == 2:
            return self.MatrixSpace(self.parent(args[1]), natural(args[0]))
        if tag == "obj.sets.vectors" and len(args) == 2:
            return self.cartesian_product([self.parent(args[0])] * natural(args[1]))
        if tag == "objectProduct" and len(args) == 2:
            return self.cartesian_product([self.parent(args[0]), self.parent(args[1])])
        if tag == "finiteData" and len(args) == 2:
            base = self.parent(args[0])
            return self.FiniteEnumeratedSet([self.native_coerce(base, self.decode(x, args[0]))
                                             for x in args[1]])
        raise NotImplementedError("unsupported selected object descriptor: %s" % tag)

    def graph(self, data, inventory):
        data = unbox(data)
        if tag_of(data) == "finiteGraph":
            actual, data = fields(data, "finiteGraph", 2)
            if sorted(map(json_key, actual)) != sorted(map(json_key, inventory)):
                raise ValueError("graph inventory differs from its supplied domain")
        if not isinstance(data, list):
            raise ValueError("expected a complete finite callable graph")
        expected = [json_key(x) for x in inventory]
        if len(set(expected)) != len(expected):
            raise ValueError("the actual domain inventory contains duplicate points")
        table = {}
        for pair in data:
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError("a graph entry must have a key and value")
            key = json_key(pair[0])
            if key in table:
                raise ValueError("a graph repeats a domain key")
            table[key] = pair[1]
        if set(table) != set(expected):
            raise ValueError("a graph must cover its actual domain exactly once")
        return [table[key] for key in expected]

    def scalar_data(self, value, descriptor):
        descriptor = self.carrier_descriptor(descriptor)
        kind = self.SCALARS.get(tag_of(descriptor))
        if kind == "rationals":
            value = self.QQ(value)
            return [int(value.numerator()), int(value.denominator())]
        if kind in ("naturals", "integers", "residues"):
            return int(self.parent(descriptor)(value))
        raise NotImplementedError("inline scalar output is limited to NN, ZZ, QQ and Z/nZ")

    def decode(self, data, selected, domain=None):
        """Lower supplied point data, retaining wrappers and owned native values."""
        data = unbox(data)
        tag = tag_of(data)
        if selected is not None:
            self.carrier_descriptor(selected)
        if tag == "opaqueData":
            entry = self.entry(data)
            if entry.callable:
                descriptor = self.carrier_descriptor(selected)
                if tag_of(descriptor) == "obj.sets.vectors":
                    coefficient, n = fields(descriptor, "obj.sets.vectors", 2)
                    return self.parent(descriptor)(self.finite_values(data, natural(n), coefficient))
                if tag_of(descriptor) == "obj.sets.matrices":
                    n, coefficient = fields(descriptor, "obj.sets.matrices", 2)
                    return self.matrix_data(data, natural(n), coefficient)
                raise ValueError("callable data were used as an ordinary native point")
            return entry.value
        if tag == "element":
            actual, expression = fields(data, "element", 2)
            self.carrier_descriptor(actual)
            return self.expression(expression, actual, domain)
        if tag == "pointView":
            target, original, original_domain = fields(data, "pointView", 3)
            if domain is not None and original_domain != domain:
                raise ValueError("a point view changed its supplied generalized domain")
            self.carrier_descriptor(target)
            return self.decode(original, target, original_domain)
        if tag == "admittedPoint":
            object_id, parameters, original_domain, original_target, target, original = self.port.admitted_point(data)
            if domain is not None and original_domain != domain:
                raise ValueError("an admitted point changed its supplied generalized domain")
            native = self.decode(original, original_target, original_domain)
            return self.admitted_data(object_id, parameters, target, native)
        if tag == "point":
            arrow, = fields(data, "point", 1)
            return self.point_arrow(arrow, selected, domain)
        if tag in ("compose", "map", "generator", "mor.sets.tuple_empty", "mediator"):
            return self.point_arrow(data, selected, domain)

        selected = self.carrier_descriptor(selected)
        selected_tag = tag_of(selected)
        if selected is None:
            raise NotImplementedError("inline point data need their complete selected object")
        args = fields(selected, selected_tag)
        if selected_tag == "finiteData":
            base, _inventory = fields(selected, "finiteData", 2)
            return self.parent(selected)(self.native_coerce(self.parent(base), self.decode(data, base, domain)))
        if selected_tag == "obj.sets.units":
            monoid, = fields(selected, "obj.sets.units", 1)
            if not isinstance(data, list) or len(data) != 2:
                raise ValueError("a Units record needs its value and inverse data, or an admitted point")
            return NativeUnitData(monoid, self.decode(data[0], monoid, domain),
                                  self.decode(data[1], monoid, domain))
        if selected_tag == "objectProduct":
            left, right = self.pair_data(data)
            return (self.decode(left, args[0], domain), self.decode(right, args[1], domain))
        if selected_tag == "obj.sets.vectors" and len(args) == 2:
            return self.parent(selected)(self.finite_values(data, natural(args[1]), args[0]))
        if selected_tag == "obj.sets.matrices" and len(args) == 2:
            return self.matrix_data(data, natural(args[0]), args[1])
        if selected_tag in ("obj.sets.polynomials", "obj.rings.polynomials") and len(args) == 1:
            return self.polynomial_data(data, args[0])
        if selected_tag == "obj.sets.degrees":
            if tag == "none":
                fields(data, "none", 0)
                return self.bottom
            if tag == "some":
                value, = fields(data, "some", 1)
                return self.NN(natural(value))
            raise ValueError("degree data require the public none/some constructors")
        if selected_tag == "obj.sets.truth_values":
            if type(data) is not bool:
                raise ValueError("a truth observation requires a JSON boolean")
            return data
        if tag == "typedMap":
            return self.point_arrow(data, selected, domain)
        if tag is not None:
            raise NotImplementedError("this public point descriptor has no diagnostic adapter")
        if self.SCALARS.get(selected_tag) == "rationals":
            if not isinstance(data, list) or len(data) != 2 or any(type(x) is not int for x in data):
                raise ValueError("rational data require the two integer record fields")
            if data[1] <= 0:
                raise ValueError("a rational denominator must be strictly positive")
            value = self.QQ(tuple(data))
            if (int(value.numerator()), int(value.denominator())) != tuple(data):
                raise ValueError("a rational record must already be reduced")
            return value
        if type(data) is int:
            if self.SCALARS.get(selected_tag) == "naturals" or selected_tag in self.FIN_OBJECTS:
                natural(data)
            return self.parent(selected)(data)
        raise NotImplementedError("no diagnostic codec for this point representation")

    def admitted_data(self, object_id, parameters, target, native):
        if object_id == "obj.sets.units":
            if len(parameters) != 1 or self.carrier_descriptor(target) != node(object_id, *parameters):
                raise ValueError("an admitted unit must retain its complete selected monoid")
            monoid = parameters[0]
            return NativeUnitData(monoid, self.native_coerce(self.parent(monoid), native))
        return native

    def expression(self, expression, selected, domain=None):
        expression = unbox(expression)
        tag = tag_of(expression)
        if tag not in ("numeral", "generator", "add", "mul", "neg", "operationExpression", "point"):
            # A retained element can contain actual computational data, including
            # a nested token. It is not reconstructed as a numeral or polynomial.
            return self.decode(expression, selected, domain)
        args = fields(expression, tag)
        if tag == "numeral" and len(args) == 1:
            return self.parent(selected)(natural(args[0]))
        if tag == "generator" and not args:
            descriptor = self.carrier_descriptor(selected)
            if tag_of(descriptor) not in ("obj.sets.polynomials", "obj.rings.polynomials", *self.F9_OBJECTS):
                raise NotImplementedError("this selected object has no diagnostic generator adapter")
            return self.parent(descriptor).gen()
        if tag in ("add", "mul") and len(args) == 2:
            a, b = (self.expression(x, selected, domain) for x in args)
            return a + b if tag == "add" else a * b
        if tag == "neg" and len(args) == 1:
            return -self.expression(args[0], selected, domain)
        if tag == "operationExpression":
            operation, parameters, operands = self.port.operation_expression(expression)
            if operation not in ("op.rings.add", "op.rings.mul", "op.rings.pow", "op.rings.neg",
                                 *self.SEMIRING_OPERATIONS):
                raise NotImplementedError("the diagnostic expression adapter supports selected ring and semiring operations")
            expected = 2 if operation in ("op.rings.add", "op.rings.mul", "op.semirings.add", "op.semirings.mul") else 1
            if len(operands) != expected:
                raise ValueError("incorrect operand count for the selected scalar operation")
            values = [self.expression(x, parameters[0]) for x in operands]
            value = values[0] if len(values) == 1 else tuple(values)
            return self.compute(operation, parameters, value)
        if tag == "point" and len(args) == 1:
            return self.point_arrow(args[0], selected, domain)
        raise NotImplementedError("unsupported public arithmetic expression")

    def pair_data(self, data):
        data = unbox(data)
        if tag_of(data) == "mediator":
            return fields(data, "mediator", 2)
        if not isinstance(data, list) or len(data) != 2:
            raise ValueError("a product point requires its two ordered components")
        return data

    def inventory(self, descriptor):
        descriptor = self.carrier_descriptor(descriptor)
        if tag_of(descriptor) in self.FIN_OBJECTS:
            n, = fields(descriptor, tag_of(descriptor), 1)
            return list(range(natural(n)))
        if self.SCALARS.get(tag_of(descriptor)) == "residues":
            modulus, = fields(descriptor, tag_of(descriptor), 1)
            if natural(modulus) == 0:
                raise NotImplementedError("Zmod(0) has no finite callable inventory")
            return [self.scalar_data(value, descriptor) for value in self.parent(descriptor)]
        if tag_of(descriptor) == "objectProduct":
            factors = fields(descriptor, "objectProduct", 2)
            native_factors = [self.FiniteEnumeratedSet([self.decode(key, factor)
                               for key in self.inventory(factor)]) for factor in factors]
            return [self.component_data(value, descriptor, None)
                    for value in self.cartesian_product(native_factors)]
        if tag_of(descriptor) == "finiteData":
            _base, inventory = fields(descriptor, "finiteData", 2)
            if not isinstance(inventory, list):
                raise ValueError("finiteData requires its actual point inventory")
            if len(set(map(json_key, inventory))) != len(inventory):
                raise ValueError("the supplied finite domain repeats a point")
            return inventory
        raise NotImplementedError("this callable needs a supported finite parent or an actual finiteData inventory")

    def finite_values(self, data, n, target):
        """Consume a total finite callable, not a sample or private row codec."""
        data = unbox(data)
        domain = node("obj.sets.fin", n)
        inventory = list(range(n))
        if isinstance(data, list) or tag_of(data) == "finiteGraph":
            return [self.decode(x, target) for x in self.graph(data, inventory)]
        if tag_of(data) == "opaqueData" and not self.entry(data).callable:
            values = list(self.entry(data).value)
            if len(values) != n:
                raise ValueError("owned vector data have the wrong supplied dimension")
            return values
        if tag_of(data) in ("element", "point", "pointView", "admittedPoint"):
            values = list(self.decode(data, node("obj.sets.vectors", target, n)))
            if len(values) != n:
                raise ValueError("vector point data have the wrong supplied dimension")
            return values
        return [self.call_arrow(data, self.ZZ(i), source=domain)
                for i in inventory]

    def matrix_data(self, data, n, coefficient):
        data = unbox(data)
        if tag_of(data) == "opaqueData" and not self.entry(data).callable:
            return self.matrix(self.parent(coefficient), n, n, self.entry(data).value)
        if tag_of(data) in ("element", "point", "pointView", "admittedPoint"):
            return self.matrix(self.parent(coefficient), n, n,
                               self.decode(data, node("obj.sets.matrices", n, coefficient)))
        row_object = node("obj.sets.vectors", coefficient, n)
        rows = self.finite_values(data, n, row_object)
        return self.matrix(self.parent(coefficient), n, n, [list(row) for row in rows])

    def polynomial_data(self, data, coefficient):
        # Polynomial.ofFinsupp and AddMonoidAlgebra.ofCoeff each have one
        # data slot; their public record encoding exposes Finsupp's two slots.
        if not isinstance(data, list) or len(data) != 2 or not isinstance(data[0], list):
            raise NotImplementedError("a polynomial needs owned data, a public expression, or its complete record")
        support, coefficients = data
        support = [natural(i) for i in support]
        if len(set(support)) != len(support):
            raise ValueError("a supplied finite support repeats an index")
        if isinstance(unbox(coefficients), list) or tag_of(unbox(coefficients)) == "finiteGraph":
            raise NotImplementedError("a finite support graph is not a total coefficient function on Nat")
        values = {i: self.native_coerce(self.parent(coefficient),
                                        self.call_arrow(coefficients, self.ZZ(i),
                                                        source=node("obj.sets.naturals")))
                  for i in support}
        return self.parent(node("obj.sets.polynomials", coefficient))(values)

    def algebra_data(self, coefficient, data):
        data = unbox(data)
        # Under R is the public Comma record: Discrete PUnit, right, hom.
        # PUnit has no data fields and Discrete has exactly one.
        if not isinstance(data, list) or len(data) != 3:
            raise NotImplementedError("polynomial application needs the selected algebra's complete Under record")
        unit, target, hom = data
        if unit != []:
            raise ValueError("the Under record's Discrete PUnit field must retain its empty data record")
        self.parent(coefficient)
        self.parent(target)
        if tag_of(unbox(hom)) == "typedMap":
            source, codomain, _callable = self.port.typed_map(unbox(hom))
            if source != coefficient or codomain != target:
                raise ValueError("the selected algebra's coefficient map changed its complete endpoints")
        return target, hom

    def compute(self, operation, parameters, value):
        arities = {
            "mor.sets.matrix_rows": 2, "mor.sets.matrix_charpoly": 2,
            "obj.sets.matrices#application": 2, "obj.sets.polynomials#application": 2,
            "mor.sets.polynomial_derivative": 1, "mor.sets.polynomial_degree": 1,
            "mor.sets.polynomial_own_evaluation": 1, "op.rings.add": 1,
            "op.rings.mul": 1, "op.rings.pow": 2, "op.rings.neg": 1,
            "mor.sets.equality": 1, "mor.sets.divide": 1,
            "mor.sets.f9_x_constants": 0, "mor.sets.f9_y_constants": 0,
            "mor.sets.tuple_empty": 1, "mor.sets.tuple_cons": 2,
            "op.semirings.add": 1, "op.semirings.mul": 1, "op.semirings.pow": 2,
        }
        if operation not in arities:
            raise NotImplementedError("operation has no diagnostic engine wrapper")
        if len(parameters) != arities[operation]:
            raise ValueError("incorrect complete parameters for the selected callable")
        if operation.startswith("op.rings.") or operation in self.SEMIRING_OPERATIONS:
            ring = self.parent(parameters[0])
            if operation in ("op.rings.add", "op.semirings.add"):
                return self.native_coerce(ring, value[0]) + self.native_coerce(ring, value[1])
            if operation in ("op.rings.mul", "op.semirings.mul"):
                return self.native_coerce(ring, value[0]) * self.native_coerce(ring, value[1])
            if operation in ("op.rings.pow", "op.semirings.pow"):
                return self.native_coerce(ring, value) ** natural(parameters[1])
            if operation == "op.rings.neg":
                return -self.native_coerce(ring, value)
        if operation == "mor.sets.equality":
            if tag_of(self.carrier_descriptor(parameters[0])) in self.F9_OBJECTS:
                parent = self.parent(parameters[0])
                value = tuple(self.native_coerce(parent, x) for x in value)
            return bool(value[0] == value[1])
        if operation == "mor.sets.divide":
            parent = self.parent(parameters[0])
            unit = value[1]
            if not isinstance(unit, NativeUnitData) or unit.monoid != parameters[0]:
                raise ValueError("division needs unit data at its supplied selected monoid")
            numerator = self.native_coerce(parent, value[0])
            if unit.inverse is None:
                quotient = numerator / self.native_coerce(parent, unit.value)
            else:
                quotient = numerator * self.native_coerce(parent, unit.inverse)
            return self.native_coerce(parent, quotient)
        if operation in ("mor.sets.f9_x_constants", "mor.sets.f9_y_constants"):
            if parameters:
                raise ValueError("the published F9 coefficient map has no explicit parameters")
            field = self.f9_presentations()[0 if operation.endswith("x_constants") else 1]
            base = self.GF(3)
            return field.coerce_map_from(base)(base(value))
        if operation == "mor.sets.tuple_empty":
            return self.cartesian_product([])(())
        if operation == "mor.sets.tuple_cons":
            selected, dimension = parameters[0], natural(parameters[1])
            parent = self.parent(node("obj.sets.vectors", selected, dimension + 1))
            return parent([value[0], *value[1]])
        if operation == "mor.sets.matrix_rows":
            return self.matrix(self.parent(parameters[1]), natural(parameters[0]),
                               natural(parameters[0]), [list(row) for row in value])
        if operation == "mor.sets.matrix_charpoly":
            return value.charpoly("x")
        if operation == "obj.sets.matrices#application":
            return value[0] * self.vector(self.parent(parameters[1]), value[1])
        if operation == "mor.sets.polynomial_derivative":
            return value.derivative()
        if operation == "mor.sets.polynomial_degree":
            return self.bottom if value.is_zero() else self.NN(value.degree())
        if operation == "mor.sets.polynomial_own_evaluation":
            return value[0](self.parent(parameters[0])(value[1]))
        if operation == "obj.sets.polynomials#application":
            target, hom = self.algebra_data(parameters[0], parameters[1])
            transported = value[0].map_coefficients(
                lambda c: self.call_arrow(hom, c, source=parameters[0], target=target),
                new_base_ring=self.parent(target))
            return transported(self.parent(target)(value[1]))
        raise NotImplementedError("operation has no diagnostic engine wrapper")

    def result_data(self, operation, parameters, value, target, domain):
        if operation == "mor.sets.equality":
            return value
        if operation == "mor.sets.polynomial_degree":
            return node("none") if value == self.bottom else node("some", int(value))
        if operation == "obj.sets.matrices#application":
            return [[i, self.component_data(value[i], parameters[1], domain)]
                    for i in range(natural(parameters[0]))]
        if operation == "mor.sets.polynomial_own_evaluation":
            return self.component_data(value, parameters[0], domain)
        if operation == "obj.sets.polynomials#application":
            coefficient_target, _hom = self.algebra_data(parameters[0], parameters[1])
            return self.component_data(value, coefficient_target, domain)
        if operation in ("mor.sets.tuple_empty", "mor.sets.tuple_cons"):
            return [[i, self.component_data(x, parameters[0], domain)] for i, x in enumerate(value)]
        if operation.startswith("op.rings."):
            descriptor = self.carrier_descriptor(parameters[0])
            if tag_of(descriptor) in self.SCALARS:
                return self.scalar_data(value, parameters[0])
        return self.own(value, target, domain)

    def component_data(self, value, descriptor, domain):
        selected = self.carrier_descriptor(descriptor)
        if tag_of(selected) in self.SCALARS:
            return self.scalar_data(value, descriptor)
        if tag_of(selected) in self.FIN_OBJECTS:
            return int(value)
        if tag_of(selected) == "finiteData":
            base, _inventory = fields(selected, "finiteData", 2)
            return self.component_data(value, base, domain)
        if tag_of(selected) == "obj.sets.degrees":
            return node("none") if value == self.bottom else node("some", int(value))
        if tag_of(selected) == "obj.sets.truth_values":
            return bool(value)
        if tag_of(selected) == "objectProduct":
            left, right = fields(selected, "objectProduct", 2)
            return [self.component_data(value[0], left, domain),
                    self.component_data(value[1], right, domain)]
        if tag_of(selected) == "obj.sets.vectors":
            coefficient, _dimension = fields(selected, "obj.sets.vectors", 2)
            return [[i, self.component_data(x, coefficient, domain)] for i, x in enumerate(value)]
        return self.own(value, descriptor, domain)

    def apply(self, operation, request):
        op, parameters, arrow, domain, source, target, argument = self.port.point_invocation(request, operation)

        def run(native):
            value = self.call_arrow(arrow, native, source=source, target=target)
            return self.result_data(op, parameters, value, target, domain)

        return self.at_domain(domain, source, argument, run)

    def at_domain(self, domain, source, argument, run):
        # A closed input retains the public terminal-source descriptor. Other
        # finite domains keep their actual inventory and supplied action.
        if domain == node("obj.sets.fin", 1):
            result = run(self.decode(argument, source, domain))
            return result if tag_of(result) == "opaqueData" else self.port.value_data(result)
        inventory = self.inventory(domain)
        argument = unbox(argument)
        if isinstance(argument, list) or tag_of(argument) == "finiteGraph":
            native = [self.decode(value, source)
                      for value in self.graph(argument, inventory)]
        else:
            native = [self.call_arrow(argument, self.decode(key, domain), source=domain, target=source)
                      for key in inventory]
        return self.port.value_data(node("finiteGraph", inventory,
                                         [[key, run(value)] for key, value in zip(inventory, native)]))

    def comparison(self, request):
        if tag_of(request) == "presentationApply":
            parameters, inverse, source, target, argument = self.port.presentation_invocation(request)
            native_map = self.f9_comparison(parameters, inverse)
            if self.parent(source) is not native_map.domain() or self.parent(target) is not native_map.codomain():
                raise ValueError("the selected F9 comparison endpoints differ from the request")
            native = native_map(self.native_coerce(native_map.domain(), self.decode(argument, source)))
            return node("element", target, self.field_expression(native))
        _op, parameters, arrow, domain, source, target, argument = self.port.point_invocation(request, "cmp.f9.translation")
        if parameters:
            raise ValueError("the published F9 comparison has no explicit parameters")

        def run(native):
            result = self.call_arrow(arrow, native, source=source, target=target)
            return self.own(result, target, domain)

        return self.at_domain(domain, source, argument, run)

    def f9_comparison(self, parameters, inverse):
        if parameters or type(inverse) is not bool:
            raise ValueError("the F9 presentation arrow requires [] parameters and a Boolean direction")
        return self.f9_presentations()[3 if inverse else 2]

    def field_expression(self, value):
        # Serialize the native polynomial representative using public arithmetic
        # constructors; no private coordinate tuple or engine program crosses.
        expression = node("numeral", 0)
        for coefficient in reversed(value.polynomial().list()):
            expression = node("add", node("mul", expression, node("generator")),
                              node("numeral", int(coefficient)))
        return expression

    def point_arrow(self, arrow, selected=None, domain=None):
        arrow = unbox(arrow)
        tag = tag_of(arrow)
        if tag in ("element", "opaqueData", "pointView", "admittedPoint"):
            return self.decode(arrow, selected, domain)
        if tag == "point":
            inner, = fields(arrow, "point", 1)
            return self.point_arrow(inner, selected, domain)
        if tag == "map":
            edge, inner = fields(arrow, "map", 2)
            self.require_forget_edge(edge)
            return self.point_arrow(inner, selected, domain)
        if tag == "compose":
            first, second = fields(arrow, "compose", 2)
            return self.call_arrow(second, self.point_arrow(first, domain=domain))
        if tag == "mediator":
            first, second = fields(arrow, "mediator", 2)
            return self.point_arrow(first, domain=domain), self.point_arrow(second, domain=domain)
        if tag == "typedMap":
            source, target, _callable = self.port.typed_map(arrow)
            if domain is not None and source != domain:
                raise ValueError("a selected point's callable changed its supplied domain")
            inventory = self.inventory(source)
            if len(inventory) != 1:
                raise NotImplementedError("a nonconstant generalized callable needs its actual application input")
            return self.call_arrow(arrow, self.decode(inventory[0], source), source=source, target=target)
        if tag == "generator":
            object_id, parameters = fields(arrow, "generator", 2)
            if object_id in ("obj.sets.f9_x", "obj.sets.f9_y") and parameters == []:
                return self.parent(node(object_id)).gen()
            if object_id != "obj.sets.polynomials" or len(parameters) != 1:
                raise NotImplementedError("this object has no published diagnostic generator adapter")
            return self.parent(node(object_id, *parameters)).gen()
        if tag == "mor.sets.tuple_empty":
            return self.compute(tag, fields(arrow, tag, 1), None)
        raise NotImplementedError("unsupported closed-point arrow descriptor")

    def call_arrow(self, arrow, value, *, source=None, target=None):
        """Lower only supplied public map data; this adds no dispatch address."""
        arrow = unbox(arrow)
        tag = tag_of(arrow)
        if tag == "typedMap":
            actual_source, actual_target, callable_data = self.port.typed_map(arrow)
            if source is not None and actual_source != source:
                raise ValueError("a typed callable changed its supplied complete source")
            if target is not None and actual_target != target:
                raise ValueError("a typed callable changed its supplied complete target")
            return self.call_arrow(callable_data, value, source=actual_source, target=actual_target)
        if isinstance(arrow, list) or tag == "finiteGraph":
            if source is None or target is None:
                raise NotImplementedError("an unlabelled callable graph needs its complete selected endpoints")
            inventory = self.inventory(source)
            values = self.graph(arrow, inventory)
            native_family = self.Family({self.decode(key, source): self.decode(item, target)
                                         for key, item in zip(inventory, values)})
            return native_family[self.native_coerce(self.parent(source), value)]
        if tag == "opaqueData":
            entry = self.entry(arrow)
            if entry.callable:
                return entry.value(entry.source_parent(value))
            descriptor = self.carrier_descriptor(entry.descriptor)
            if tag_of(descriptor) == "obj.sets.vectors":
                return entry.value[int(self.NN(value))]
            if tag_of(descriptor) == "obj.sets.matrices":
                return entry.value.row(int(self.NN(value)))
            raise ValueError("an ordinary native point was used as a callable")
        if tag == "compose":
            first, second = fields(arrow, "compose", 2)
            # Each typed constituent retains its own intermediate endpoint.
            return self.call_arrow(second, self.call_arrow(first, value, source=source), target=target)
        if tag == "map":
            edge, inner = fields(arrow, "map", 2)
            self.require_forget_edge(edge)
            endpoints = []
            for descriptor in (source, target):
                if tag_of(descriptor) == "functorAction":
                    actual_edge, original = fields(descriptor, "functorAction", 2)
                    self.require_forget_edge(actual_edge)
                    if actual_edge != edge:
                        raise ValueError("a mapped callable changed its supplied structural action")
                    endpoints.append(original)
                else:
                    endpoints.append(None)
            # Unlabelled graphs need these explicitly retained action endpoints;
            # typed/named inner maps carry their own original selected context.
            return self.call_arrow(inner, value, source=endpoints[0], target=endpoints[1])
        if tag == "pointView":
            view, original, original_domain = fields(arrow, "pointView", 3)
            self.carrier_descriptor(view)
            if source is not None and original_domain != source:
                raise ValueError("a point view changed its generalized domain")
            return self.call_arrow(original, value, source=original_domain)
        if tag == "admittedPoint":
            object_id, parameters, original_domain, original_target, admitted, original = self.port.admitted_point(arrow)
            if source is not None and original_domain != source:
                raise ValueError("an admission changed its generalized domain")
            native = self.call_arrow(original, value, source=original_domain, target=original_target)
            return self.admitted_data(object_id, parameters, admitted, native)
        if tag == "presentation":
            comparison, parameters, inverse = fields(arrow, "presentation", 3)
            if comparison != "cmp.f9.translation":
                raise NotImplementedError("this presentation has no diagnostic engine adapter")
            native_map = self.f9_comparison(parameters, inverse)
            return native_map(self.native_coerce(native_map.domain(), value))
        if tag == "identity":
            domain, codomain = fields(arrow, "identity", 2)
            if domain != codomain:
                raise ValueError("an identity arrow must retain equal complete endpoints")
            return self.native_coerce(self.parent(domain), value)
        if tag == "mediator":
            first, second = fields(arrow, "mediator", 2)
            return self.call_arrow(first, value, source=source), self.call_arrow(second, value, source=source)
        if tag == "constructionLeg":
            operation, diagram, complete_cone, index = fields(arrow, "constructionLeg", 4)
            apex, left, right = self.product_cone(operation, diagram, complete_cone)
            if index == node("left"):
                leg = left
            elif index == node("right"):
                leg = right
            else:
                raise ValueError("a product leg uses its public WalkingPair index")
            _source, actual_target, _callable = self.port.typed_map(unbox(leg))
            return self.call_arrow(leg, value, source=apex, target=actual_target)
        if tag == "arrowHom":
            receiver, = fields(arrow, "arrowHom", 1)
            receiver = unbox(receiver)
            if tag_of(receiver) not in ("arrow", "subobject"):
                raise ValueError("arrowHom requires its complete returned Arrow record")
            domain, codomain, stored_map = fields(receiver, tag_of(receiver), 3)
            return self.call_arrow(stored_map, value, source=domain, target=codomain)
        if tag == "objectField":
            object_id, field, parameters = fields(arrow, "objectField", 3)
            if object_id == "obj.sets.polynomials" and field == "constants" and len(parameters) == 1:
                return self.parent(node(object_id, *parameters))(value)
            if object_id == "obj.sets.units" and field == "inclusion" and len(parameters) == 1:
                if not isinstance(value, NativeUnitData) or value.monoid != parameters[0]:
                    raise ValueError("the units inclusion needs the supplied unit data at its selected monoid")
                return self.native_coerce(self.parent(parameters[0]), value.value)
            raise NotImplementedError("unsupported published object field")
        if tag == "incl.sets.fin_integers_mod":
            modulus, = fields(arrow, tag, 1)
            finite = self.parent(node("obj.sets.fin", natural(modulus)))
            return self.Zmod(modulus)(finite(value))
        if tag in ("incl.sets.naturals_integers", "incl.sets.integers_rationals", "incl.sets.naturals_degrees"):
            fields(arrow, tag, 0)
            if tag == "incl.sets.naturals_integers":
                return self.ZZ(self.NN(value))
            if tag == "incl.sets.integers_rationals":
                return self.QQ.coerce_map_from(self.ZZ)(self.ZZ(value))
            return self.degrees(self.NN(value))
        if tag in ("element", "point", "generator", "mor.sets.tuple_empty"):
            if source is not None and len(self.inventory(source)) != 1:
                raise ValueError("a closed point cannot replace a nonconstant generalized map")
            return self.point_arrow(arrow, target, source)
        if tag in self.POINT_OPERATIONS or tag in self.SEMIRING_OPERATIONS:
            return self.compute(tag, fields(arrow, tag), value)
        raise NotImplementedError("unsupported retained callable descriptor")

    def product(self, diagram):
        left, right = fields(diagram, "pair", 2)
        apex = node("objectProduct", left, right)
        native_product = self.parent(apex)
        maps = []
        for i, target in enumerate((left, right)):
            callable_data = self.own(native_product.cartesian_projection(i), target, None,
                                     source_parent=native_product, callable=True)
            maps.append(self.port.map_data(apex, target, callable_data))
        return self.port.value_data(node("cone", apex, *maps))

    def serve(self):
        # Reuse the released frame codec, distinguishing unsupported input shapes
        # from engine failures. The released helper's serve catches both together.
        operations = self.operations()
        self.port.write_frame({"op": "ready", "protocol": 1, "backend": self.NAME,
                               "backend_version": self.engine_version,
                               "adapter_version": self.VERSION,
                               "capabilities": sorted(operations)})
        while True:
            frame = self.port.read_frame()
            if frame is None:
                return
            request_id, operation = frame.get("request_id"), frame.get("op")
            if operation not in operations:
                self.port.write_frame({"request_id": request_id, "status": "unsupported", "op": operation})
                continue
            try:
                if "args" not in frame:
                    raise ValueError("the request omitted its args field")
                result = operations[operation](frame["args"])
                self.port.write_frame({"request_id": request_id, "status": "ok", "value": result})
            except NotImplementedError:
                self.port.write_frame({"request_id": request_id, "status": "unsupported", "op": operation})
            except Exception as exc:
                self.port.write_frame({"request_id": request_id, "status": "error",
                                       "kind": type(exc).__name__, "message": str(exc)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"),
                        help="explicit checkout of the public leaf contract")
    options = parser.parse_args()
    if not options.contract:
        parser.error("set CAS_LEAF_CONTRACT_PATH or pass --contract")
    engine = os.environ.get("CAS_SAGE_PYTHON")
    if engine and os.path.abspath(engine) != os.path.abspath(sys.executable):
        os.execv(engine, [engine, str(Path(__file__).resolve()), *sys.argv[1:]])
    # Sage's ordinary cache must be writable; no host-home mutation is required.
    if "DOT_SAGE" not in os.environ:
        os.environ["DOT_SAGE"] = tempfile.mkdtemp(prefix="cas-v1-sage-")
    adapter = SageDiagnostic(load_public_port(options.contract))
    adapter.serve()


if __name__ == "__main__":
    main()
