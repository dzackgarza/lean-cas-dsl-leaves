#!/usr/bin/env python3
"""Independent endpoint, parameter, packet and owner engineering controls.

No expected mathematical answer is asserted. Numeric data below are self-selected
inputs; checks concern framing, exact retained fields, result kinds and rejection
of malformed or foreign-session packets. No kernel or external test is imported.
"""

import argparse
import os
from pathlib import Path

from cas_port import endpoint_data, map_data, morphism_endpoint
from completion_smoke import Port, fields, identity, invoke, owned, payload, require
from endpoints import EndpointInterfaces
from wire import (Callable, Session, Unsupported, framed_callable, inventory, node,
                  public_data)


ONE = node("obj.sets.fin", 1)
Q = node("obj.sets.rationals")
QR = node("obj.rings.rationals")
QC = node("obj.commutative_rings.rationals")
TRUTH = node("obj.sets.truth_values")


def rational(value):
    return [value, 1]


def reject(call, kind=ValueError):
    try:
        call()
    except kind:
        return
    raise RuntimeError("a malformed or unsupported boundary was accepted")


def protocol_checks():
    class Reader(EndpointInterfaces):
        tag = staticmethod(lambda data: data.get("ctor") if isinstance(data, dict) else None)

        def __init__(self):
            self.session = Session()

    reader = Reader()
    source = node("obj.sets.fin", 2)
    arrow = node("op.rings.add", QR)
    target = endpoint_data(arrow, "source")
    calls = []
    left = reader.session.keep(Callable(source, Q, lambda point: calls.append(("left", point))))
    right = reader.session.keep(Callable(source, Q, lambda point: calls.append(("right", point))))
    actual = framed_callable(node("mediator", left, map_data(source, Q, right)),
                             source, target, reader.session,
                             lambda *args: (_ for _ in ()).throw(Unsupported()),
                             product_factors=reader.product_factors)
    require(actual.source is source and actual.target is target,
            "a mediator replaced its original complete endpoint")
    marker = object()
    actual(marker)
    require(len(calls) == 2 and all(item[1] is marker for item in calls),
            "a mediator discarded the actual generalized-domain input")
    wrapped = map_data(source, target, reader.session.keep(actual))
    same = framed_callable(wrapped, source, target, reader.session, lambda *args: None,
                           product_factors=reader.product_factors)
    require(same is actual, "a typed owned callable was replaced")
    reject(lambda: framed_callable(wrapped, target, source, reader.session, lambda *args: None))
    reject(lambda: framed_callable(target, source, target, reader.session, lambda *args: None))
    for bad in (node("morphismEndpoint", arrow), node("morphismEndpoint", arrow, "source", 0),
                node("morphismEndpoint", arrow, "middle")):
        reject(lambda bad=bad: morphism_endpoint(bad))
        reject(lambda bad=bad: public_data([bad], reader.session))
    finite_endpoint = endpoint_data(node("mor.sets.fin_rev", 2), "source")
    reject(lambda: inventory(finite_endpoint), Unsupported)
    explicit = node("finiteData", finite_endpoint, [0, 1])
    graph = node("finiteGraph", [0, 1], [[0, "first"], [1, "second"]])
    framed_callable(graph, explicit, Q, reader.session, lambda *args: None)
    reject(lambda: framed_callable(graph, finite_endpoint, Q, reader.session, lambda *args: None), Unsupported)
    reject(lambda: framed_callable([[0, "first"]], explicit, Q, reader.session, lambda *args: None))
    reject(lambda: framed_callable([[0, "first"], [0, "second"]], explicit, Q,
                                   reader.session, lambda *args: None))
    foreign = Session().keep(Callable(source, target, lambda point: point))
    reject(lambda: public_data(endpoint_data(foreign, "target"), reader.session), Unsupported)
    reject(lambda: public_data(node("opaqueData", ""), reader.session))
    return 13


def shape_rational(value, label):
    result = payload(value)
    require(isinstance(result, list) and len(result) == 2
            and all(type(item) is int for item in result), label + ": scalar record omitted fields")


def whole(port, label, operation, parameters, arrow=None, source=None, target=None,
          domain=None, argument=None):
    arrow = node(operation, *parameters) if arrow is None else arrow
    source = endpoint_data(arrow, "source") if source is None else source
    target = endpoint_data(arrow, "target") if target is None else target
    domain = source if domain is None else domain
    argument = identity(domain) if argument is None else argument
    result = owned(port.request(label, operation,
                                invoke(operation, parameters, domain, source, target, argument, arrow)))
    return result, source, target


def engine_checks(port):
    op = "op.rings.add"
    full, source, target = whole(port, "ring/unnamed whole endpoints", op, [QR])
    pair = [rational(2), rational(5)]
    shape_rational(port.request("ring/reused actual callable", op,
                                invoke(op, [QR], ONE, source, target, pair, full)), "ring reuse")
    wrapped = map_data(source, target, full)
    shape_rational(port.request("ring/typed reused callable", op,
                                invoke(op, [QR], ONE, source, target, pair, wrapped)), "typed ring reuse")
    port.request("ring/changed owned parameters", op,
                 invoke(op, [node("obj.rings.integers")], ONE, source, target, pair, full), expected="error")
    port.request("ring/changed original endpoint", op,
                 invoke(op, [QR], ONE, endpoint_data(full, "source"), target, pair, full), expected="error")
    port.request("ring/malformed selector", op,
                 invoke(op, [QR], ONE, node("morphismEndpoint", node(op, QR), "other"), target, pair),
                 expected="error")
    port.request("ring/endpoint used as callable", op,
                 invoke(op, [QR], ONE, source, target, pair, source), expected="error")

    power = node("op.rings.pow", QR, 4)
    psource, ptarget = endpoint_data(power, "source"), endpoint_data(power, "target")
    port.request("ring/typed callable omitted parameter", "op.rings.pow",
                 invoke("op.rings.pow", [QR], psource, psource, ptarget, identity(psource),
                        map_data(psource, ptarget, power)), expected="error")
    whole(port, "ring/unary full parameters", "op.rings.pow", [QR, 4])
    port.request("ring/composed callable changed parameter", "op.rings.pow",
                 invoke("op.rings.pow", [QR, 5], psource, psource, ptarget, identity(psource),
                        node("compose", identity(psource), map_data(psource, ptarget, power))),
                 expected="error")
    domain = node("obj.sets.fin", 2)
    left = map_data(domain, Q, [[0, rational(3)], [1, rational(8)]])
    right = map_data(domain, Q, [[0, rational(6)], [1, rational(9)]])
    family, _, _ = whole(port, "ring/mediator keeps actual component endpoints", op, [QR],
                         domain=domain, argument=node("mediator", left, right))
    maps = node("obj.sets.maps", domain, target)
    result = port.request("ring/generalized callable reuse", "mor.sets.equality",
                          invoke("mor.sets.equality", [maps], ONE, node("objectProduct", maps, maps),
                                 TRUTH, [family, family]))
    require(type(payload(result)) is bool, "whole-map observation lost Boolean framing")
    port.request("ring/changed generalized domain", op,
                 invoke(op, [QR], ONE, source, target, pair,
                        map_data(source, target, family)), expected="error")

    finite = node("obj.sets.fin", 3)
    reversal = node("mor.sets.fin_rev", 3)
    endpoint = endpoint_data(reversal, "source")
    finite_target = endpoint_data(reversal, "target")
    graph = node("finiteGraph", [0, 1, 2], [[0, 1], [1, 2], [2, 0]])
    port.request("finite/endpoint has no implicit inventory", "mor.sets.fin_rev",
                 invoke("mor.sets.fin_rev", [3], endpoint, endpoint, finite_target, graph), expected="unsupported")
    inventory = node("finiteData", endpoint, [0, 1, 2])
    whole(port, "finite/supplied exact inventory", "mor.sets.fin_rev", [3],
          source=endpoint, target=finite_target, domain=inventory,
          argument=map_data(inventory, endpoint, graph))
    port.request("finite/omitted graph key", "mor.sets.fin_rev",
                 invoke("mor.sets.fin_rev", [3], inventory, endpoint, finite_target,
                        map_data(inventory, endpoint, [[0, 1], [1, 2]])), expected="error")

    mapping = map_data(finite, finite, reversal)
    image_params = [finite, finite, mapping]
    image_arrow = node("mor.sets.direct_image", *image_params)
    image_source, image_target = endpoint_data(image_arrow, "source"), endpoint_data(image_arrow, "target")
    subset = owned(port.request("image/unnamed endpoints", "mor.sets.direct_image",
                                invoke("mor.sets.direct_image", image_params, ONE,
                                       image_source, image_target, [0, 2])))
    owned(port.request("image/retained subset reuse", "mor.sets.direct_image",
                       invoke("mor.sets.direct_image", image_params, ONE,
                              image_source, image_target, subset)))
    whole(port, "image/whole callable", "mor.sets.direct_image", image_params)
    port.request("image/changed endpoint callable", "mor.sets.direct_image",
                 invoke("mor.sets.direct_image", image_params, ONE, image_source,
                        endpoint_data(node("mor.sets.direct_image", finite, finite, identity(finite)), "target"),
                        [0]), expected="error")

    module = node("obj.modules.regular", QR)
    parameters = [QR, module, module]
    object_id = "obj.sets.module_morphisms"
    application = object_id + "#application"
    hom = node(object_id, *parameters)
    admitted = node("admittedPoint", object_id, parameters, ONE,
                    node("obj.sets.maps", module, module), hom, identity(module, typed=True))
    app, app_source, app_target = whole(port, "hom/whole unnamed application", application, parameters)
    shape_rational(port.request("hom/original admitted callable", application,
                                invoke(application, parameters, ONE, app_source, app_target,
                                       [admitted, rational(7)], app)), "admitted application")
    bad_parameters = [node("obj.rings.integers"), module, module]
    port.request("hom/changed retained scalar selection", application,
                 invoke(application, bad_parameters, ONE, app_source, app_target,
                        [admitted, rational(7)], app), expected="error")

    monoid = node("functorAction", node("fun.rings.multiplicative_monoid"), QR)
    whole(port, "monoid/whole unnamed product", "op.monoids.mul", [monoid])
    group = node("functorAction", node("fun.rings.additive_group"), QR)
    additive = node("functorAction", node("fun.additive_groups.additive_monoid"), group)
    whole(port, "additive/whole unnamed product", "op.additive_monoids.add", [additive])
    cell = node("cellComponent", "cell.additive_groups.carrier", [], group, False)
    whole(port, "additive/retained complete component endpoints",
          "cell.additive_groups.carrier#component", [[], group, False], arrow=cell)

    comparison = "cmp.rational_dual.translation"
    comparison_arrow = node("presentation", comparison, [], False)
    comparison_map, csource, ctarget = whole(port, "comparison/common whole invocation", comparison, [],
                                           arrow=comparison_arrow)
    whole(port, "comparison/reused common callable", comparison, [], arrow=comparison_map,
          source=csource, target=ctarget)
    comparison_map = owned(port.request("comparison/retained presentation invocation", comparison,
                                       node("presentationApply", [], False, csource, ctarget,
                                            identity(csource))))
    port.request("comparison/presentation result changed parameters", comparison,
                 invoke(comparison, [QR], csource, csource, ctarget, identity(csource), comparison_map),
                 expected="error")

    matrix = [[0, [[0, rational(2)]]]]
    parameters = [1, 1, QC, matrix]
    native, native_source, native_target = whole(port, "reindex/retained original whole map",
                                                "mor.modules.rectangular_linear_map", parameters)
    coefficient = node("mor.commutative_rings.integer_coefficients", QC)
    action = node("fun.modules.reindex", coefficient)
    for label, original in (("opaque", native), ("portable", node("mor.modules.rectangular_linear_map", *parameters))):
        whole(port, "reindex/complete " + label + " callable", "fun.modules.reindex", [coefficient],
              arrow=node("map", action, original),
              source=node("functorAction", action, native_source),
              target=node("functorAction", action, native_target))
    return full, source, target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol-only", action="store_true")
    parser.add_argument("--sage-python")
    options = parser.parse_args()
    controls = protocol_checks()
    if options.protocol_only:
        print("protocol boundary groups:", controls)
        return
    environment = dict(os.environ)
    if options.sage_python:
        environment["CAS_SAGE_PYTHON"] = options.sage_python
    backend = Path(__file__).with_name("backend.py")
    with Port(backend, environment) as port:
        full, source, target = engine_checks(port)
        primary_requests = port.requests
    # Open the foreign process only after the original owner has stopped.
    with Port(backend, environment) as port:
        port.request("owner/foreign retained callable", "op.rings.add",
                     invoke("op.rings.add", [QR], ONE, source, target,
                            [rational(2), rational(3)], full), expected="unsupported")
        port.request("owner/foreign token nested in endpoint", "mor.sets.equality",
                     invoke("mor.sets.equality", [Q], ONE,
                            endpoint_data(full, "source"), TRUTH, [rational(2), rational(3)]),
                     expected="unsupported")
        foreign_requests = port.requests
    print("protocol boundary groups:", controls)
    print("primary requests:", primary_requests)
    print("foreign-owner requests:", foreign_requests)
    print("Engineering framing/retention results only; no mathematical acceptance claim.")


if __name__ == "__main__":
    main()
