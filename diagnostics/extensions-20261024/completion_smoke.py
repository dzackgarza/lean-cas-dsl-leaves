#!/usr/bin/env python3
"""Standalone framed-port checks of shape, invocation, and live ownership.

Inputs are self-selected public packets.  No computed mathematical value is
asserted, including the truth of an equality reply.  This script imports no
kernel, acceptance suite, engine internals, or expected-answer fixture.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from smoke import node, read_frame


class EngineeringFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise EngineeringFailure(message)


def fields(value, tag, count):
    require(isinstance(value, dict) and value.get("ctor") == tag,
            "expected the %s output envelope" % tag)
    result = value.get("args")
    require(isinstance(result, list) and len(result) == count,
            "%s has an incompatible output shape" % tag)
    return result


def payload(value):
    while isinstance(value, dict) and value.get("ctor") == "valueData":
        value, = fields(value, "valueData", 1)
    return value


def owned(value):
    value = payload(value)
    token, = fields(value, "opaqueData", 1)
    require(isinstance(token, str) and bool(token), "an owned result requires a token")
    return value


def invoke(operation, parameters, domain, source, target, argument, arrow=None):
    if arrow is None:
        arrow = node(operation, *parameters)
    return node("apply", operation, parameters, arrow, domain, source, target, argument)


def identity(selected, typed=False):
    result = node("identity", selected, selected)
    return node("typedMap", selected, selected, result) if typed else result


def comparison(parameters, inverse, source, target, argument):
    return node("presentationApply", parameters, inverse, source, target, argument)


class Port:
    def __init__(self, backend, environment):
        self.backend = backend
        self.environment = environment
        self.process = None
        self.requests = 0

    def __enter__(self):
        self.process = subprocess.Popen(
            [sys.executable, str(self.backend)], cwd=self.backend.parent,
            env=self.environment, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        ready = read_frame(self.process.stdout)
        require(isinstance(ready, dict) and ready.get("op") == "ready",
                "the backend omitted its ready frame")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.process is None:
            return
        self.process.stdin.close()
        try:
            self.process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)
        self.process.stdout.close()

    def request(self, label, operation, argument, expected="ok"):
        self.requests += 1
        packet = {"request_id": self.requests, "op": operation, "args": argument}
        encoded = json.dumps(packet, separators=(",", ":")).encode("utf-8")
        self.process.stdin.write(str(len(encoded)).encode("ascii") + b"\n" + encoded)
        self.process.stdin.flush()
        reply = read_frame(self.process.stdout)
        require(isinstance(reply, dict), label + ": reply is not a JSON object")
        require(reply.get("request_id") == self.requests, label + ": request identity changed")
        if reply.get("status") != expected:
            detail = {key: reply[key] for key in ("status", "op", "kind", "message") if key in reply}
            raise EngineeringFailure(label + ": " + json.dumps(detail, sort_keys=True))
        if expected == "unsupported":
            require(reply.get("op") == operation, label + ": unsupported reply changed operation")
            return None
        if expected == "error":
            require(isinstance(reply.get("kind"), str) and isinstance(reply.get("message"), str),
                    label + ": error reply omitted its diagnostic fields")
            return None
        require("value" in reply, label + ": successful reply omitted its value")
        value = reply["value"]
        require(isinstance(value, dict) and value.get("ctor") in {"valueData", "opaqueData"},
                label + ": successful reply has no public result envelope")
        fields(value, value["ctor"], 1)
        return value


ONE = node("obj.sets.fin", 1)
TRUTH = node("obj.sets.truth_values")


def equality_reply(port, label, domain, codomain, left, right):
    maps = node("obj.sets.maps", domain, codomain)
    source = node("objectProduct", maps, maps)
    value = port.request(label, "mor.sets.equality",
                         invoke("mor.sets.equality", [maps], ONE, source, TRUTH, [left, right]))
    require(type(payload(value)) is bool, label + ": equality reply is not Boolean")


def whole_comparison(port, label, operation, parameters, source, target, inverse=False, typed=False):
    return owned(port.request(label, operation,
                              comparison(parameters, inverse, source, target, identity(source, typed))))


def finite_checks(port, dimension, typed):
    selected = node("obj.sets.fin", dimension)
    label = "finite/%s/%s" % (dimension, "typed" if typed else "bare")
    reversal = owned(port.request(label + "/whole morphism", "mor.sets.fin_rev",
                                  invoke("mor.sets.fin_rev", [dimension], selected, selected, selected,
                                         identity(selected, typed))))
    forward = whole_comparison(port, label + "/whole comparison", "cmp.sets.fin_reversal",
                               [dimension], selected, selected, typed=typed)
    backward = whole_comparison(port, label + "/whole inverse comparison", "cmp.sets.fin_reversal",
                                [dimension], selected, selected, inverse=True, typed=typed)
    for suffix, actual in (("bare owned", forward), ("wrapped owned", node("valueData", forward))):
        owned(port.request(label + "/chain " + suffix, "cmp.sets.fin_reversal",
                           comparison([dimension], True, selected, selected, actual)))
    composite = node("compose", forward, backward)
    owned(port.request(label + "/bare opaque composition", "mor.sets.fin_rev",
                       invoke("mor.sets.fin_rev", [dimension], selected, selected, selected, composite)))
    inventory = list(range(dimension))
    graph = node("finiteGraph", inventory, [[point, point] for point in inventory])
    owned(port.request(label + "/wrapped finite graph", "mor.sets.fin_rev",
                       invoke("mor.sets.fin_rev", [dimension], selected, selected, selected,
                              node("valueData", graph))))
    equality_reply(port, label + "/equality framing", selected, selected, reversal, composite)


def dual_and_polynomial_checks(port):
    operation = "cmp.rational_dual.translation"
    source_ring = node("obj.commutative_rings.rational_dual_x")
    target_ring = node("obj.commutative_rings.rational_dual_y")
    forward_ring = whole_comparison(port, "dual/whole ring comparison", operation, [],
                                    source_ring, target_ring, typed=True)
    backward_ring = whole_comparison(port, "dual/whole inverse ring comparison", operation, [],
                                     target_ring, source_ring, inverse=True)
    owned(port.request("dual/owned ring comparison chain", operation,
                       comparison([], True, target_ring, source_ring, forward_ring)))
    equality_reply(port, "dual/bare ring opaque composition", source_ring, source_ring,
                   node("compose", forward_ring, backward_ring), identity(source_ring))

    source = node("obj.sets.rational_dual_x")
    target = node("obj.sets.rational_dual_y")
    forward = whole_comparison(port, "dual/whole selected set view", operation, [], source, target)
    backward = whole_comparison(port, "dual/whole inverse selected set view", operation, [],
                                target, source, inverse=True, typed=True)
    rationals = node("obj.sets.rationals")
    coefficients = owned(port.request("dual/whole rational coefficients", "mor.sets.rational_dual_x_constants",
                                     invoke("mor.sets.rational_dual_x_constants", [], rationals, rationals,
                                            source, identity(rationals, True))))
    transported = owned(port.request("dual/comparison on owned coefficient map", operation,
                                     comparison([], False, source, target, coefficients)))
    target_coefficients = owned(port.request("dual/whole target coefficients", "mor.sets.rational_dual_y_constants",
                                            invoke("mor.sets.rational_dual_y_constants", [], rationals,
                                                   rationals, target, identity(rationals))))
    equality_reply(port, "dual/coefficient map equality framing", rationals, target,
                   transported, target_coefficients)

    ring_selection = node("functorAction", node("fun.commutative_rings.ring"), source_ring)
    for name in ("add", "mul", "pow", "neg"):
        identifier = "op.rings." + name
        parameters = [ring_selection, 3] if name == "pow" else [ring_selection]
        domain = node("objectProduct", source, source) if name in {"add", "mul"} else source
        actual = owned(port.request("polynomial/whole " + name, identifier,
                                    invoke(identifier, parameters, domain, domain, source,
                                           identity(domain, True))))
        carried = node("compose", node("compose", actual, forward), backward)
        equality_reply(port, "polynomial/" + name + " comparison composition", domain, source,
                       actual, carried)

    diagram = node("pair", source, source)
    cone = payload(port.request("polynomial/source product", "lim.sets.product", diagram))
    apex, first, second = fields(cone, "cone", 3)
    fields(first, "typedMap", 3)
    fields(second, "typedMap", 3)
    selected_first = node("constructionField", "lim.sets.product", diagram, cone, 1)
    selected_second = node("constructionField", "lim.sets.product", diagram, cone, 2)
    carried_first = node("compose", selected_first, forward)
    carried_second = node("compose", selected_second, forward)
    equality_reply(port, "polynomial/actual projection composition", apex, source, selected_first,
                   node("compose", carried_first, backward))
    mediator = node("mediator", carried_first, carried_second)
    target_product = node("objectProduct", target, target)
    equality_reply(port, "polynomial/mediator composition", apex, target_product, mediator, mediator)
    target_cone = payload(port.request("polynomial/target product", "lim.sets.product",
                                      node("pair", target, target)))
    _, target_first, _ = fields(target_cone, "cone", 3)
    equality_reply(port, "polynomial/mediator then actual projection", apex, target,
                   node("compose", mediator, target_first), carried_first)


def series_checks(port):
    coefficient = node("obj.commutative_rings.rationals")
    index = node("obj.sets.naturals")
    series = node("obj.sets.power_series", coefficient)
    family = owned(port.request("series/whole family", "mor.sets.successor_power_series_terms",
                                invoke("mor.sets.successor_power_series_terms", [coefficient], index,
                                       index, series, identity(index, True))))
    maps = node("obj.sets.maps", index, series)
    topological = node("obj.hausdorff_topological_monoids.power_series", coefficient)
    admitted = node("obj.sets.summable_families", topological, index)
    for label, actual in (("bare", family), ("wrapped", node("valueData", family))):
        argument = node("admittedPoint", "obj.sets.summable_families", [topological, index],
                        ONE, maps, admitted, actual)
        total = owned(port.request("series/owned family binder " + label, "bind.sets.power_series_sum",
                                   invoke("bind.sets.power_series_sum", [coefficient, index], ONE,
                                          admitted, series, argument)))
        value = payload(port.request("series/coefficient shape " + label, "mor.sets.power_series_coefficient",
                                     invoke("mor.sets.power_series_coefficient", [coefficient], ONE,
                                            node("objectProduct", series, index), node("obj.sets.rationals"),
                                            [total, 2])))
        require(isinstance(value, list) and len(value) == 2 and all(type(item) is int for item in value),
                "series/coefficient observation did not retain the rational record shape")


def aut_wrapper_checks(port):
    category = node("category", "cat.sets", [])
    receiver = node("obj.sets.fin", 3)
    request = {"ctor": "con.automorphisms", "args": [category], "receiver": node("coreObject", receiver)}
    group = owned(port.request("Aut/owned group", "con.automorphisms", request))
    selected = group
    views = [("owned group", selected)]
    for label, action in (
            ("monoid", node("fun.groups.monoid")),
            ("semigroup", node("fun.monoids.semigroup")),
            ("associativity classifier", node("classifierForget", "clf.magmas.associative", [])),
            ("binary-operation classifier", node("classifierForget", "clf.sets.binary_operation", []))):
        selected = node("functorAction", action, selected)
        views.append((label, selected))
    for label, selected in views:
        value = payload(port.request("Aut/cardinality shape under " + label, "meth.cardinality", selected))
        count, = fields(value, "finite", 1)
        require(type(count) is int, "Aut/cardinality did not produce the finite-count record")
    inverse = owned(port.request("Aut/whole inverse", "op.groups.inverse",
                                 invoke("op.groups.inverse", [group], group, group, group, identity(group))))
    equality_reply(port, "Aut/whole inverse equality framing", group, group, inverse, inverse)


def named_aut_checks(port, groups):
    if groups:
        modulus = 5
        source = node("obj.groups.cyclic_quotient", modulus)
        target = node("obj.groups.cyclic", modulus)
        comparison_id, parameters = "cmp.groups.cyclic_quotient_residue", [modulus]
        operation = "fun.core_groups.automorphisms"
    else:
        source = target = node("obj.sets.fin", 3)
        comparison_id, parameters = "cmp.sets.fin_reversal", [3]
        operation = "fun.core_sets.automorphisms"
    label = "named Aut/" + ("Groups" if groups else "Sets")
    forward = whole_comparison(port, label + "/actual forward", comparison_id, parameters, source, target)
    backward = whole_comparison(port, label + "/actual backward", comparison_id, parameters,
                                target, source, inverse=True, typed=True)
    core_comparison = node("coreIso", source, target, forward, backward)
    action = node(operation)
    source_image = node("functorAction", action, node("coreObject", source))
    target_image = node("functorAction", action, node("coreObject", target))
    arrow = node("map", action, core_comparison)
    actual_automorphism = [identity(source), identity(source)] if groups else [forward, backward]
    owned(port.request(label + "/map point", operation,
                       invoke(operation, [], ONE, source_image, target_image, actual_automorphism, arrow)))
    whole = owned(port.request(label + "/whole map", operation,
                               invoke(operation, [], source_image, source_image, target_image,
                                      identity(source_image, True), arrow)))
    equality_reply(port, label + "/whole-map equality framing", source_image, target_image, whole, whole)
    if not groups:
        inner = node("fun.sets.identity")
        mapped_source = node("functorAction", inner, source)
        mapped_target = node("functorAction", inner, target)
        comparison_action = node("constructorMap", "ctor.core", inner)
        mapped_comparison = node("map", comparison_action, core_comparison)
        mapped_image_source = node("functorAction", action, node("coreObject", mapped_source))
        mapped_image_target = node("functorAction", action, node("coreObject", mapped_target))
        mapped_forward = node("map", inner, node("typedMap", source, target, forward))
        mapped_backward = node("map", inner, node("typedMap", target, source, backward))
        owned(port.request(label + "/retained core constructor action", operation,
                           invoke(operation, [], ONE, mapped_image_source, mapped_image_target,
                                  [mapped_forward, mapped_backward], node("map", action, mapped_comparison))))


def category_descriptor_checks(port):
    category = node("category", "cat.sets", [])
    receiver = node("coreObject", node("coreObject", node("obj.sets.fin", 3)))
    for label, selected, expected in (
            ("well-formed unsupported", node("constructedCategory", "ctor.core", [category]), "unsupported"),
            ("missing constructor argument", node("constructedCategory", "ctor.core", []), "error")):
        argument = {"ctor": "con.automorphisms", "args": [selected], "receiver": receiver}
        port.request("category/" + label, "con.automorphisms", argument, expected=expected)


def foreign_owner_check(port):
    selected = node("obj.sets.fin", 4)
    value = owned(port.request("ownership/original whole map", "mor.sets.fin_rev",
                               invoke("mor.sets.fin_rev", [4], selected, selected, selected, identity(selected))))
    with Port(port.backend, port.environment) as foreign:
        foreign.request("ownership/foreign session reuse", "mor.sets.fin_rev",
                        invoke("mor.sets.fin_rev", [4], selected, selected, selected, value),
                        expected="unsupported")


def cartesian_check(port):
    forget = node("fun.commutative_rings.ring")
    integers = node("obj.commutative_rings.integers")
    rationals = node("obj.commutative_rings.rationals")
    source_ring = node("functorAction", forget, integers)
    target_ring = node("functorAction", forget, rationals)
    base_map = node("map", forget, node("mor.commutative_rings.integer_coefficients", rationals))
    receiver = node("obj.modules.regular", target_ring)
    restricted = node("functorAction", node("fun.modules.reindex", base_map), receiver)
    source = node("functorAction", node("fun.modules.fibre_inclusion", source_ring), restricted)
    target = node("functorAction", node("fun.modules.fibre_inclusion", target_ring), receiver)
    arrow = node("cartesianMap", "fun.modules.reindex", [base_map], receiver)
    operation = "fun.modules.reindex#cartesian"
    owned(port.request("cartesian/nested selected parameters", operation,
                       invoke(operation, [[base_map], receiver], source, source, target,
                              identity(source, True), arrow)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"),
                        help="public contract checkout containing python/cas_port.py")
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"),
                        help="Sage-compatible Python executable for the backend")
    arguments = parser.parse_args()
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    if arguments.contract:
        public_python = str(Path(arguments.contract).resolve() / "python")
        environment["PYTHONPATH"] = public_python + os.pathsep + environment.get("PYTHONPATH", "")
    backend = Path(__file__).resolve().with_name("backend.py")
    exceptions = []
    completed = 0
    with Port(backend, environment) as port:
        checks = [("finite/%s/%s" % (dimension, mode),
                   lambda dimension=dimension, typed=typed: finite_checks(port, dimension, typed))
                  for dimension in (0, 1, 4) for mode, typed in (("bare", False), ("typed", True))]
        checks.extend([
            ("dual and polynomial actions", lambda: dual_and_polynomial_checks(port)),
            ("owned series family", lambda: series_checks(port)),
            ("owned Aut structural views", lambda: aut_wrapper_checks(port)),
            ("named Sets Aut action", lambda: named_aut_checks(port, False)),
            ("named Groups Aut action", lambda: named_aut_checks(port, True)),
            ("category descriptor statuses", lambda: category_descriptor_checks(port)),
            ("foreign-session ownership", lambda: foreign_owner_check(port)),
            ("cartesian parameter framing", lambda: cartesian_check(port)),
        ])
        for label, check in checks:
            try:
                check()
                completed += 1
            except Exception as error:
                exceptions.append({"check": label, "kind": type(error).__name__, "message": str(error)})
        summary = {"engineering_groups_completed": completed, "engineering_groups_requested": len(checks),
                   "primary_connection_requests": port.requests, "engineering_exceptions": exceptions}
    print(json.dumps(summary, indent=2, sort_keys=True))
    return bool(exceptions)


if __name__ == "__main__":
    sys.exit(main())
