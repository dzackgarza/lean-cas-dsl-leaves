#!/usr/bin/env python3
"""Standalone protocol coverage for the five new public generic interfaces.

No mathematical answer is asserted. Complete native results are reused through
their live connection; checks inspect status, framing and ordinary data shapes.
"""

import json
import os
from pathlib import Path

from completion_smoke import (ONE, TRUTH, Port, equality_reply, fields, identity,
                              invoke, node, owned, payload, require)


def admitted(object_id, parameters, source, target, actual):
    selected = node(object_id, *parameters)
    return node("admittedPoint", object_id, parameters, ONE,
                node("obj.sets.maps", source, target), selected, actual)


def whole(port, label, operation, parameters, source, target):
    return owned(port.request(label, operation,
                              invoke(operation, parameters, source, source, target, identity(source))))


def monoid_checks(port):
    group = node("obj.groups.cyclic", 8)
    monoid = node("functorAction", node("fun.groups.monoid"), group)
    pair = node("objectProduct", group, group)
    multiply = whole(port, "monoid/cyclic whole multiplication", "op.monoids.mul", [monoid], pair, group)
    value = payload(port.request("monoid/cyclic multiplication point", "op.monoids.mul",
                                 invoke("op.monoids.mul", [monoid], ONE, pair, group, [3, 6], multiply)))
    require(type(value) is int, "cyclic multiplication did not retain its scalar data shape")
    value = payload(port.request("monoid/cyclic identity point", "op.monoids.one",
                                 invoke("op.monoids.one", [monoid], ONE, ONE, group, 0)))
    require(type(value) is int, "cyclic unit did not retain its scalar data shape")
    equality_reply(port, "monoid/cyclic whole-map equality framing", pair, group, multiply, multiply)

    rationals = node("obj.sets.rationals")
    ring = node("obj.rings.rationals")
    multiplicative = node("functorAction", node("fun.rings.multiplicative_monoid"), ring)
    additive_group = node("functorAction", node("fun.additive_groups.to_groups"),
                          node("functorAction", node("fun.rings.additive_group"), ring))
    additive = node("functorAction", node("fun.groups.monoid"), additive_group)
    pair = node("objectProduct", rationals, rationals)
    products = []
    for label, selected in (("multiplicative", multiplicative), ("additive", additive)):
        products.append(whole(port, "monoid/selected " + label, "op.monoids.mul", [selected], pair, rationals))
        value = payload(port.request("monoid/selected unit " + label, "op.monoids.one",
                                     invoke("op.monoids.one", [selected], ONE, ONE, rationals, 0)))
        require(isinstance(value, list) and len(value) == 2,
                "the selected rational unit omitted its data record")
    equality_reply(port, "monoid/distinct selected structures", pair, rationals, *products)

    receiver = node("obj.sets.fin", 3)
    category = node("category", "cat.sets", [])
    group = owned(port.request("monoid/native Aut object", "con.automorphisms",
                               {"ctor": "con.automorphisms", "args": [category],
                                "receiver": node("coreObject", receiver)}))
    selected = node("functorAction", node("fun.groups.monoid"), group)
    pair = node("objectProduct", group, group)
    actual_unit = owned(port.request("monoid/native Aut unit", "op.monoids.one",
                                     invoke("op.monoids.one", [selected], ONE, ONE, group, 0)))
    first = node("typedMap", receiver, receiver, [[0, 1], [1, 2], [2, 0]])
    second = node("typedMap", receiver, receiver, [[0, 2], [1, 0], [2, 1]])
    product = owned(port.request("monoid/actual Aut directions", "op.monoids.mul",
                                 invoke("op.monoids.mul", [selected], ONE, pair, group,
                                        [[first, second], actual_unit])))
    whole_product = whole(port, "monoid/whole Aut multiplication", "op.monoids.mul", [selected], pair, group)
    equality_reply(port, "monoid/complete finite Aut multiplication domain", pair, group,
                   whole_product, whole_product)
    projected = whole(port, "monoid/project actual product forward", "mor.sets.automorphism_forward",
                      [receiver, product], receiver, receiver)
    equality_reply(port, "monoid/retained product projection", receiver, receiver, projected, projected)


def image_checks(port):
    source, target = node("obj.sets.fin", 4), node("obj.sets.fin", 3)
    source_power = node("obj.sets.power_set", source)
    target_power = node("obj.sets.power_set", target)
    function = node("typedMap", source, target, [[0, 2], [1, 1], [2, 2], [3, 0]])
    parameters = [source, target, function]
    image = owned(port.request("image/actual finite subset", "mor.sets.direct_image",
                               invoke("mor.sets.direct_image", parameters, ONE, source_power,
                                      target_power, [0, 0, 2])))
    equality_source = node("objectProduct", target_power, target_power)
    observed = payload(port.request("image/subset equality framing", "mor.sets.equality",
                                    invoke("mor.sets.equality", [target_power], ONE, equality_source,
                                           TRUTH, [image, [1]])))
    require(type(observed) is bool, "subset equality did not produce Boolean-shaped data")
    all_images = whole(port, "image/whole power-object map", "mor.sets.direct_image", parameters,
                       source_power, target_power)
    equality_reply(port, "image/complete finite power-domain equality", source_power, target_power,
                   all_images, all_images)
    family_domain = node("obj.sets.fin", 2)
    family = node("finiteGraph", [0, 1], [[0, [0, 2]], [1, []]])
    images = owned(port.request("image/generalized subset family", "mor.sets.direct_image",
                                invoke("mor.sets.direct_image", parameters, family_domain,
                                       source_power, target_power, family)))
    equality_reply(port, "image/retained subset-family domain", family_domain, target_power, images, images)

    rationals = node("obj.sets.rationals")
    dual = node("obj.sets.rational_dual_x")
    coefficient_map = whole(port, "image/owned infinite-domain coefficient map",
                            "mor.sets.rational_dual_x_constants", [], rationals, dual)
    q_power, dual_power = node("obj.sets.power_set", rationals), node("obj.sets.power_set", dual)
    owned(port.request("image/finite subset of infinite carrier", "mor.sets.direct_image",
                       invoke("mor.sets.direct_image", [rationals, dual, coefficient_map], ONE,
                              q_power, dual_power, [[-2, 1], [3, 2]])))


def inclusion_observation(port, label, object_id, parameters, source, target, admitted_function, actual):
    selected = node(object_id, *parameters)
    maps = node("obj.sets.maps", source, target)
    point = node("typedMap", ONE, selected, [[0, admitted_function]])
    inclusion = node("typedMap", selected, maps, node("objectField", object_id, "inclusion", parameters))
    included_point = node("point", node("compose", point, inclusion))
    equality_reply(port, label, source, target, included_point, actual)


def morphism_checks(port):
    group = node("obj.groups.cyclic", 7)
    actual = whole(port, "group map/original complete function", "op.groups.inverse", [group], group, group)
    object_id = "obj.sets.group_morphisms"
    parameters = [group, group]
    selected = node(object_id, *parameters)
    admitted_function = admitted(object_id, parameters, group, group, actual)
    application = object_id + "#application"
    application_source = node("objectProduct", selected, group)
    all_applications = whole(port, "group map/whole application", application, parameters,
                             application_source, group)
    value = payload(port.request("group map/reuse whole application", application,
                                 invoke(application, parameters, ONE, application_source, group,
                                        [admitted_function, 4], all_applications)))
    require(type(value) is int, "group application did not retain the point data shape")
    family = node("finiteGraph", list(range(7)), [[point, [admitted_function, point]] for point in range(7)])
    generalized = owned(port.request("group map/generalized admitted application", application,
                                     invoke(application, parameters, group, application_source, group, family)))
    equality_reply(port, "group map/complete generalized result", group, group, generalized, actual)
    family_domain = node("obj.sets.fin", 2)
    original_maps = node("obj.sets.maps", group, group)
    original_family = node("typedMap", family_domain, original_maps,
                           [[0, actual], [1, identity(group)]])
    admitted_family = node("admittedPoint", object_id, parameters, family_domain,
                           original_maps, selected, original_family)
    arguments = node("typedMap", family_domain, group, [[0, 2], [1, 4]])
    family_result = owned(port.request("group map/complete non-singleton admission domain", application,
                                       invoke(application, parameters, family_domain, application_source, group,
                                              node("mediator", admitted_family, arguments))))
    equality_reply(port, "group map/non-singleton admitted result shape", family_domain, group,
                   family_result, family_result)
    inclusion_observation(port, "group map/actual inclusion function", object_id, parameters,
                          group, group, admitted_function, actual)

    ring = node("obj.rings.rationals")
    commutative_ring = node("obj.commutative_rings.rationals")
    source = node("obj.modules.vectors", ring, 2)
    target = node("obj.modules.regular", ring)
    row = [[0, [[0, [5, 2]], [1, [-7, 3]]]]]
    actual = whole(port, "module map/original complete native map", "mor.modules.row_linear_map",
                   [2, commutative_ring, row], source, target)
    object_id = "obj.sets.module_morphisms"
    parameters = [ring, source, target]
    selected = node(object_id, *parameters)
    admitted_function = admitted(object_id, parameters, source, target, actual)
    application = object_id + "#application"
    application_source = node("objectProduct", selected, source)
    all_applications = whole(port, "module map/whole application", application, parameters,
                             application_source, target)
    value = payload(port.request("module map/reuse whole application", application,
                                 invoke(application, parameters, ONE, application_source, target,
                                        [admitted_function, [[0, [2, 1]], [1, [-1, 2]]]], all_applications)))
    require(isinstance(value, list) and len(value) == 2,
            "module application omitted the rational point record")
    inclusion_observation(port, "module map/native inclusion function", object_id, parameters,
                          source, target, admitted_function, actual)


def main():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    backend = Path(__file__).resolve().with_name("backend.py")
    with Port(backend, environment) as port:
        monoid_checks(port)
        image_checks(port)
        morphism_checks(port)
        print(json.dumps({"completedRequests": port.requests,
                          "checks": "public framing, selected structures and live callable reuse only"}))


if __name__ == "__main__":
    main()
