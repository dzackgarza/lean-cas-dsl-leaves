#!/usr/bin/env python3
"""Public-envelope coverage at existing registrations; no expected math answers."""

import argparse
import json
import os
from pathlib import Path

from completion_smoke import (ONE, TRUTH, Port, fields, identity, invoke, node,
                              owned, payload, require)


def request_object(operation, parameters, receiver):
    return {"ctor": operation, "args": parameters, "receiver": receiver}


def method(operation, functor, parameters, receiver):
    return request_object(operation, [node(functor, *parameters)], receiver)


def boolean(port, label, selected, left, right):
    result = port.request(label, "mor.sets.equality",
                          invoke("mor.sets.equality", [selected], ONE,
                                 node("objectProduct", selected, selected), TRUTH, [left, right]))
    require(type(payload(result)) is bool, "the observation omitted its Boolean response shape")


def rational_shape(reply):
    result = payload(reply)
    require(isinstance(result, list) and len(result) == 2
            and all(type(value) is int for value in result) and result[1] > 0,
            "the rational point omitted its public scalar-record shape")


def finite_shape(reply):
    count, = fields(payload(reply), "finite", 1)
    require(type(count) is int, "the finite observation omitted its integer-shaped field")


def finite_consumers(port):
    selected = node("obj.sets.fin", 2)
    points = [node("element", selected, node("numeral", 0)),
              node("valueData", node("element", selected, node("numeral", 1)))]
    domain = node("finiteData", selected, points)
    operation = "mor.sets.fin_rev"
    actual = owned(port.request("retained finite callable", operation,
                                invoke(operation, [2], domain, domain, selected, identity(domain))))
    values = [port.request("retain actual finite point reply", operation,
                           invoke(operation, [2], ONE, domain, selected, point, actual)) for point in points]
    graph = node("typedMap", domain, selected,
                 node("finiteGraph", points, [[point, value] for point, value in zip(points, values)]))
    maps = node("obj.sets.maps", domain, selected)
    for wrapped in (actual, node("valueData", node("typedMap", domain, selected, actual)),
                    node("compose", identity(domain, typed=True), actual),
                    node("compose", actual, identity(selected, typed=True))):
        boolean(port, "finite observer consumes exact input and returned point frames", maps, wrapped, graph)
    paired = node("mediator", actual, graph)
    boolean(port, "finite observer consumes mixed composed readers",
            node("obj.sets.maps", domain, node("objectProduct", selected, selected)), paired, paired)
    expressions = node("typedMap", domain, selected,
                       node("finiteGraph", points, [[point, point] for point in points]))
    boolean(port, "graph retains complete selected expression outputs", maps, actual, expressions)
    wrong = node("element", node("obj.sets.fin", 3), node("numeral", 0))
    port.request("nested finite point keeps its caller-selected target", "mor.sets.equality",
                 invoke("mor.sets.equality", [selected], ONE,
                        node("objectProduct", selected, selected), TRUTH, [wrong, 0]), expected="error")
    return selected, domain, points


def automorphism_consumers(port, selected, domain, points):
    category = node("category", "cat.sets", [])
    group = owned(port.request("actual construction image", "con.automorphisms",
                               request_object("con.automorphisms", [category], node("coreObject", domain))))
    graph = node("typedMap", domain, domain,
                 node("finiteGraph", points, [[point, point] for point in points]))
    actual = owned(port.request("owned automorphism with complete graph directions", "op.groups.inverse",
                                invoke("op.groups.inverse", [group], ONE, group, group, [graph, graph])))
    for operation in ("mor.sets.automorphism_forward", "mor.sets.automorphism_backward"):
        parameters = [domain, actual]
        port.request("returned direction keeps its graph reader", operation,
                     invoke(operation, parameters, ONE, domain, domain, points[1]))
        whole = owned(port.request("whole returned direction", operation,
                                    invoke(operation, parameters, domain, domain, domain, identity(domain))))
        port.request("reuse actual whole direction", operation,
                     invoke(operation, parameters, ONE, domain, domain, points[0],
                            node("valueData", node("typedMap", domain, domain, whole))))
    functor = node("functor", "fun.sets.identity", [])
    point = node("point", node("typedMap", ONE, group, node("finiteGraph", [0], [[0, actual]])))
    for operation in ("mor.sets.automorphism_evaluation", "mor.sets.automorphism_inverse_evaluation"):
        for datum in (actual, node("element", group, actual), node("valueData", point)):
            port.request("evaluation retains both point frames", operation,
                         invoke(operation, [category, functor, domain], ONE,
                                node("objectProduct", group, domain), domain, [datum, points[1]]))
    native = node("typedMap", domain, selected, node("mor.sets.fin_rev", 2))
    encode = node("typedMap", selected, domain,
                  node("finiteGraph", [0, 1], [[index, point] for index, point in enumerate(points)]))
    complete = node("compose", native, encode)
    mixed = owned(port.request("native construction consumes complete composed directions", "op.groups.inverse",
                               invoke("op.groups.inverse", [group], ONE, group, group, [complete, complete])))
    boolean(port, "finite automorphism observation keeps both readers", group, actual, mixed)
    monoid = node("functorAction", node("fun.groups.monoid"), group)
    unit = owned(port.request("identity retains original inventory packets", "op.monoids.one",
                              invoke("op.monoids.one", [monoid], ONE, ONE, monoid, identity(ONE))))
    product = owned(port.request("native Aut composition keeps original readers", "op.monoids.mul",
                                 invoke("op.monoids.mul", [monoid], ONE,
                                        node("objectProduct", monoid, monoid), monoid, [actual, unit])))
    port.request("consume actual native Aut product", "mor.sets.automorphism_forward",
                 invoke("mor.sets.automorphism_forward", [domain, product], ONE, domain, domain, points[1]))
    action = node("con.automorphisms", category)
    comparison = node("coreIso", domain, domain, complete, complete)
    original = node("typedMap", node("coreObject", domain), node("coreObject", domain), comparison)
    operation = "con.automorphisms#map"
    arrow = node("map", action, original)
    mapped = owned(port.request("construction map consumes actual returned images", operation,
                                invoke(operation, [category], ONE, group, group, actual, arrow)))
    port.request("consume actual mapped automorphism", "mor.sets.automorphism_forward",
                 invoke("mor.sets.automorphism_forward", [domain, mapped], ONE, domain, domain, points[1]))
    whole = owned(port.request("whole construction map at actual returned images", operation,
                               invoke(operation, [category], group, group, group, identity(group), arrow)))
    owned(port.request("reuse actual construction-map callable", operation,
                       invoke(operation, [category], ONE, group, group, actual,
                              node("valueData", node("typedMap", group, group, whole)))))
    port.request("construction map requires original Core endpoint fields", operation,
                 invoke(operation, [category], ONE, group, group, actual,
                        node("map", action, comparison)), expected="error")
    malformed_composite = node("compose", node("typedMap", group, group, node("map", action, comparison)),
                               identity(group))
    port.request("composition preserves inner construction-map framing", operation,
                 invoke(operation, [category], ONE, group, group, actual, malformed_composite), expected="error")
    malformed = node("typedMap", domain, node("coreObject", domain), comparison)
    port.request("construction map retains Core source selection", operation,
                 invoke(operation, [category], ONE, group, group, actual,
                        node("map", action, malformed)), expected="error")
    other = owned(port.request("distinct actual construction receiver", "con.automorphisms",
                               request_object("con.automorphisms", [category], node("coreObject", selected))))
    port.request("construction map retains actual target-image context", operation,
                 invoke(operation, [category], ONE, group, other, actual, arrow), expected="error")
    values = [port.request("actual primitive point result for retained graph", "mor.sets.fin_rev",
                           invoke("mor.sets.fin_rev", [2], ONE, selected, selected, index)) for index in range(2)]
    returned_graph = node("typedMap", selected, selected,
                          node("finiteGraph", [0, 1], [[index, value] for index, value in enumerate(values)]))
    retained = owned(port.request("Aut native indexing consumes actual returned output frames", "op.groups.inverse",
                                  invoke("op.groups.inverse", [other], ONE, other, other,
                                         [returned_graph, returned_graph])))
    port.request("returned Aut direction retains those output frames", "mor.sets.automorphism_forward",
                 invoke("mor.sets.automorphism_forward", [selected, retained], ONE, selected, selected, 0))
    return actual


def method_and_record_frames(port):
    finite = node("obj.sets.fin", 2)
    diagram = node("pair", finite, finite)
    cone = port.request("actual finite product cone", "lim.sets.product", diagram)
    apex = node("constructionApex", "lim.sets.product", diagram, cone)
    for receiver in (apex, node("constructionApex", "lim.sets.product", diagram, node("valueData", cone)),
                     node("constructionField", "lim.sets.product", diagram, cone, 0)):
        finite_shape(port.request("complete method consumes retained object projection", "meth.cardinality",
                                  method("meth.cardinality", "fun.sets.cardinality", [], receiver)))
    ring = owned(port.request("actual selected scalar image", "fun.commutative_rings.ring",
                              request_object("fun.commutative_rings.ring", [], node("obj.commutative_rings.rationals"))))
    module = node("obj.modules.regular", ring)
    original = node("arrow", module, module, identity(module, typed=True))
    hom_id = "obj.sets.module_morphisms"
    for operation in ("meth.kernel", "meth.arrow_ker"):
        result = port.request("complete selected kernel method", operation,
                              method(operation, "fun.arrows_modules.kernel", [ring], node("valueData", original)))
        kernel, target, _ = fields(payload(result), "arrow", 3)
        owned(kernel)
        require(target == module, "the complete Arrow changed its retained target")
        for source, target, actual_map in ((module, module, node("arrowHom", original)),
                                           (kernel, module, node("subobjectInclusion", result))):
            parameters = [ring, source, target]
            hom = node(hom_id, *parameters)
            rational_shape(port.request("consume complete retained Arrow map wrapper", hom_id + "#application",
                                         invoke(hom_id + "#application", parameters, ONE,
                                                node("objectProduct", hom, source), target, [actual_map, [0, 1]])))
        selected = node("subobjectApex", result)
        rational_shape(port.request("consume retained subobject apex", "op.modules.scalar_action",
                                     invoke("op.modules.scalar_action", [ring, selected], ONE,
                                            node("objectProduct", ring, selected), selected, [[2, 3], [0, 1]])))
    for bad in (request_object("meth.cardinality", [], finite),
                method("meth.cardinality", "fun.sets.cardinality", [finite], finite),
                method("meth.cardinality", "fun.arrows_modules.kernel", [ring], finite),
                request_object("meth.cardinality", [node("fun.sets.identity"), node("fun.sets.cardinality")], finite),
                {"ctor": "meth.cardinality", "args": [node("fun.sets.cardinality")]}):
        port.request("complete method framing remains exact", "meth.cardinality", bad, expected="error")
    port.request("kernel method retains explicit scalar selection", "meth.kernel",
                 method("meth.kernel", "fun.arrows_modules.kernel", [], original), expected="error")
    port.request("parameterized method cannot infer parameters from legacy receiver", "meth.kernel", original,
                 expected="error")
    for bad in (node("constrainedPoint", "", ONE, ring, ring, [2, 3]),
                node("constrainedPoint", "", ONE, ring, ring)):
        port.request("constrained-point malformed framing", "op.rings.neg",
                     invoke("op.rings.neg", [ring], ONE, ring, ring, bad), expected="error")
    return apex, ring, original


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"))
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"))
    arguments = parser.parse_args()
    require(bool(arguments.contract), "a published contract checkout is required")
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                       PYTHONPATH=str(Path(arguments.contract).resolve() / "python"))
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    backend = Path(__file__).resolve().with_name("backend.py")
    with Port(backend, environment) as port:
        selected, domain, points = finite_consumers(port)
        actual = automorphism_consumers(port, selected, domain, points)
        apex, ring, original = method_and_record_frames(port)
        requests = port.requests
    with Port(backend, environment) as foreign:
        foreign.request("complete projected record retains supplier ownership", "meth.cardinality",
                        method("meth.cardinality", "fun.sets.cardinality", [], apex), expected="unsupported")
        foreign.request("returned automorphism retains supplier ownership", "mor.sets.automorphism_forward",
                        invoke("mor.sets.automorphism_forward", [domain, actual], ONE, domain, domain, points[1]),
                        expected="unsupported")
        foreign.request("complete method parameter retains supplier ownership", "meth.kernel",
                        method("meth.kernel", "fun.arrows_modules.kernel", [ring], original), expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"requests": requests, "foreignOwnerRequests": foreign_requests,
                      "scope": "public envelope framing, actual selected records, callable readers and ownership only"}))


if __name__ == "__main__":
    main()
