#!/usr/bin/env python3
"""Independent public callable-form and owner engineering controls.

The numeric inputs are self-selected. Checks concern packet framing, exact
retained endpoints, callable reuse, result shapes and failure classification.
No computed truth, cardinality or other mathematical answer is asserted.
"""

import argparse
import os
from pathlib import Path

from cas_port import endpoint_data, map_data
from completion_smoke import (ONE, TRUTH, Port, equality_reply, fields, identity,
                              invoke, owned, payload, require)
from endpoints import EndpointInterfaces
from wire import (Callable, Session, Unsupported, framed_callable, key, node,
                  power_object_map, public_data)


def power(field, *parameters):
    return node("powerObjectMap", "pow.sets", field, list(parameters))


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
    selected = node("obj.sets.fin", 4)
    other = node("obj.sets.fin", 5)
    terminal = power("terminal", selected)
    predicate = map_data(selected, TRUTH, [[0, True], [1, False], [2, True], [3, False]])
    forms = [power("truth"), terminal, power("member", selected),
             power("transpose", selected, predicate), power("image", selected, selected, identity(selected))]
    for form in forms:
        _, field, parameters = power_object_map(form)
        source, target = reader.power_endpoints(form)
        require(key(reader.endpoint_view(endpoint_data(form, "source"))) == key(source),
                field + ": source selector lost its declared context")
        require(key(reader.endpoint_view(endpoint_data(form, "target"))) == key(target),
                field + ": target selector lost its declared context")
        for side, expected in (("source", source), ("target", target)):
            reader.same_endpoint(endpoint_data(form, side), expected, form, side, field)
            reject(lambda form=form, side=side, expected=expected:
                   reader.same_endpoint(endpoint_data(form, "target" if side == "source" else "source"),
                                        expected, form, side, field))
        reject(lambda form=form, parameters=parameters:
               power_object_map(node("powerObjectMap", "pow.sets", form["args"][1], parameters + [selected])))
    for invalid in (node("powerObjectMap", "pow.sets", "terminal"),
                    node("powerObjectMap", "pow.sets", "terminal", selected),
                    node("powerObjectMap", 4, "truth", []),
                    node("compose", terminal), node("mediator", terminal)):
        reject(lambda invalid=invalid: public_data(invalid, reader.session))
    reject(lambda: power_object_map(node("powerObjectMap", "pow.other", "terminal", [selected])), Unsupported)
    reject(lambda: power_object_map(power("notPublished", selected)), Unsupported)
    mediator = node("mediator", terminal, terminal)
    require(key(reader.endpoint_view(endpoint_data(mediator, "source"))) == key(selected),
            "the mediator changed its shared source")
    reject(lambda: reader.endpoint_view(endpoint_data(node("mediator", terminal,
                                                          power("terminal", other)), "source")))
    events = []
    first = reader.session.keep(Callable(selected, ONE, lambda point: events.append(("first", point)) or point))
    second = reader.session.keep(Callable(ONE, TRUTH, lambda point: events.append(("second", point)) or point))
    composite = node("compose", map_data(selected, ONE, first), map_data(ONE, TRUTH, second))
    actual = framed_callable(composite, selected, TRUTH, reader.session,
                             lambda *args: (_ for _ in ()).throw(Unsupported()))
    marker = object()
    actual(marker)
    require(actual.source is selected and actual.target is TRUTH,
            "composition replaced an actual endpoint descriptor")
    require([name for name, _ in events] == ["first", "second"]
            and all(point is marker for _, point in events),
            "composition discarded an actual callable or its input")
    reject(lambda: framed_callable(node("compose", map_data(selected, ONE, first),
                                         map_data(other, TRUTH, second)), selected, TRUTH,
                                    reader.session, lambda *args: None))
    foreign = Session().keep(Callable(selected, selected, lambda point: point))
    reject(lambda: public_data(endpoint_data(power("image", selected, selected, foreign), "target"),
                               reader.session), Unsupported)
    return len(forms)


def finite_cardinality(port, label, extent):
    value = payload(port.request(label, "meth.cardinality", extent))
    count, = fields(value, "finite", 1)
    require(type(count) is int and count >= 0, label + ": the finite cardinal record is malformed")


def engine_checks(port):
    domain = node("obj.sets.fin", 4)
    target = node("obj.sets.fin", 3)
    target_power = node("obj.sets.power_set", target)
    truth = power("truth")
    terminal = power("terminal", domain)
    for selected in (node("obj.sets.fin", 0), ONE, domain):
        arrow = power("terminal", selected)
        equality_reply(port, "terminal/complete selected domain", selected, ONE,
                       arrow, node("compose", identity(selected), map_data(selected, ONE, arrow)))
    constant = node("compose", terminal, truth)
    equality_reply(port, "truth/terminal composition", domain, TRUTH, constant, constant)

    endpoint_source = endpoint_data(constant, "source")
    supplied_source = node("finiteData", endpoint_source, [0, 1, 2, 3])
    endpoint_target = endpoint_data(constant, "target")
    equality_reply(port, "endpoint/complete composite context", supplied_source, endpoint_target,
                   constant, constant)

    ring = node("obj.rings.rationals")
    rationals = node("obj.sets.rationals")
    monoid = node("functorAction", node("fun.rings.multiplicative_monoid"), ring)
    family = owned(port.request("terminal/actual nullary source comparison", "op.monoids.one",
                                invoke("op.monoids.one", [monoid], domain, ONE, rationals, terminal)))
    equality_reply(port, "terminal/reused owned generalized result", domain, rationals, family, family)

    unnamed = endpoint_data(node("mor.sets.fin_rev", 4), "source")
    owned(port.request("terminal/no source inventory required", "op.monoids.one",
                       invoke("op.monoids.one", [monoid], unnamed, ONE, rationals,
                              power("terminal", unnamed))))

    predicate = map_data(domain, TRUTH, [[0, True], [1, False], [2, False], [3, True]])
    transpose = power("transpose", domain, predicate)
    domain_power = node("obj.sets.power_set", domain)
    transpose_family = node("compose", terminal, transpose)
    member = power("member", domain)
    member_source = node("objectProduct", domain, domain_power)
    membership = node("compose", node("mediator", identity(domain), transpose_family), member)
    equality_reply(port, "member/mediator of a point and retained subset family", domain, TRUTH,
                   membership, map_data(domain, TRUTH, membership))
    equality_reply(port, "member/whole finite product domain", member_source, TRUTH, member, member)
    finite_cardinality(port, "transpose/extent consumer",
                       node("extent", "pow.sets", domain, node("point", transpose)))

    original = map_data(domain, target, [[0, 1], [1, 2], [2, 0], [3, 1]])
    image = power("image", domain, target, original)
    finite_cardinality(port, "image/complete global image extent", node("extent", "pow.sets", target, image))
    finite_cardinality(port, "image/element point wrapper",
                       node("extent", "pow.sets", target,
                            node("element", target_power, node("point", image))))
    reverse = node("mor.sets.fin_rev", 3)
    reverse_owned = owned(port.request("image/retain actual original callable", "mor.sets.fin_rev",
                                       invoke("mor.sets.fin_rev", [3], target, target, target, identity(target))))
    owned_image = power("image", target, target, reverse_owned)
    finite_cardinality(port, "image/owned original callable extent",
                       node("extent", "pow.sets", target, owned_image))
    image_parameters = [target, target, reverse]
    subset = owned(port.request("image/reuse global subset inside direct image", "mor.sets.direct_image",
                                invoke("mor.sets.direct_image", image_parameters, ONE,
                                       target_power, target_power, node("point", image))))
    pair = node("objectProduct", target_power, target_power)
    answer = payload(port.request("image/retained subset equality framing", "mor.sets.equality",
                                  invoke("mor.sets.equality", [target_power], ONE, pair, TRUTH, [subset, subset])))
    require(type(answer) is bool, "the retained subset observation lost Boolean framing")
    finite_cardinality(port, "image/actual owned subset extent",
                       node("extent", "pow.sets", target, subset))

    complete = node("finiteData", endpoint_data(reverse, "source"), [0, 1, 2])
    explicit = map_data(complete, target, [[0, 2], [1, 0], [2, 1]])
    finite_cardinality(port, "image/explicit inventory at an endpoint",
                       node("extent", "pow.sets", target, power("image", complete, target, explicit)))
    bare = endpoint_data(reverse, "source")
    port.request("image/no invented endpoint inventory", "meth.cardinality",
                 node("extent", "pow.sets", target,
                      power("image", bare, target, map_data(bare, target, [[0, 2], [1, 0], [2, 1]]))),
                 expected="unsupported")

    # The following failures concern representation, selection or implementation
    # boundaries. They make no assertion about a computed mathematical answer.
    maps = node("obj.sets.maps", domain, ONE)
    compare_source = node("objectProduct", maps, maps)
    for malformed in (power("terminal"), power("terminal", target), power("truth", domain),
                      map_data(domain, target, terminal)):
        port.request("malformed/power parameter or exact endpoint", "mor.sets.equality",
                     invoke("mor.sets.equality", [maps], ONE, compare_source, TRUTH, [malformed, terminal]),
                     expected="error")
    broken_shared = node("compose", map_data(domain, ONE, terminal), map_data(target, TRUTH, truth))
    broken_maps = node("obj.sets.maps", domain, TRUTH)
    port.request("malformed/composition changes the shared descriptor", "mor.sets.equality",
                 invoke("mor.sets.equality", [broken_maps], ONE,
                        node("objectProduct", broken_maps, broken_maps), TRUTH, [broken_shared, constant]),
                 expected="error")
    broken_predicate = map_data(domain, TRUTH, [[0, True], [1, False], [2, 7], [3, True]])
    port.request("malformed/predicate point data", "meth.cardinality",
                 node("extent", "pow.sets", domain, power("transpose", domain, broken_predicate)), expected="error")
    incomplete = map_data(domain, target, [[0, 1]])
    port.request("malformed/incomplete original graph", "meth.cardinality",
                 node("extent", "pow.sets", target, power("image", domain, target, incomplete)), expected="error")
    for unsupported in (power("notPublished", domain),
                        node("powerObjectMap", "pow.other", "terminal", [domain])):
        port.request("unsupported/unimplemented selected field", "mor.sets.equality",
                     invoke("mor.sets.equality", [maps], ONE, compare_source, TRUTH, [unsupported, terminal]),
                     expected="unsupported")
    naturals = node("obj.sets.naturals")
    port.request("unsupported/infinite global image", "meth.cardinality",
                 node("extent", "pow.sets", naturals, power("image", naturals, naturals, identity(naturals))),
                 expected="unsupported")
    port.request("unsupported/infinite predicate subset", "meth.cardinality",
                 node("extent", "pow.sets", naturals,
                      power("transpose", naturals, node("compose", power("terminal", naturals), truth))),
                 expected="unsupported")
    return subset, reverse_owned, target, target_power


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol-only", action="store_true")
    options = parser.parse_args()
    groups = protocol_checks()
    if options.protocol_only:
        print("published callable-field groups:", groups)
        return
    backend = Path(__file__).with_name("backend.py")
    environment = dict(os.environ)
    with Port(backend, environment) as port:
        subset, original, target, target_power = engine_checks(port)
        primary = port.requests
    with Port(backend, environment) as port:
        port.request("owner/foreign subset in retained extent", "meth.cardinality",
                     node("extent", "pow.sets", target, subset), expected="unsupported")
        port.request("owner/foreign original map in retained image", "meth.cardinality",
                     node("extent", "pow.sets", target, power("image", target, target, original)),
                     expected="unsupported")
        source = endpoint_data(power("image", target, target, original), "target")
        port.request("owner/foreign map nested in a selected endpoint", "mor.sets.equality",
                     invoke("mor.sets.equality", [target_power], ONE,
                            node("objectProduct", source, source), TRUTH, [[], []]), expected="unsupported")
        foreign = port.requests
    print("published callable-field groups:", groups)
    print("primary requests:", primary)
    print("foreign-owner requests:", foreign)
    print("Engineering framing/retention results only; no mathematical acceptance claim.")


if __name__ == "__main__":
    main()
