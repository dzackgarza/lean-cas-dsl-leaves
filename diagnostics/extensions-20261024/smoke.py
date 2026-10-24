#!/usr/bin/env python3
"""Exercise framing and live ownership with self-selected public input packets.

This is a diagnostic smoke run, not a mathematical correctness suite. It contains
no expected mathematical answers and never launches the kernel or Lean.
"""

import json
import os
from pathlib import Path
import subprocess
import sys


def node(tag, *arguments):
    return {"ctor": tag, "args": list(arguments)}


def apply(operation, parameters, domain, source, target, argument):
    return node("apply", operation, parameters, node(operation, *parameters),
                domain, source, target, argument)


def read_frame(stream):
    line = stream.readline()
    if not line or not line[:-1].isdigit():
        raise RuntimeError("the backend did not provide a framed reply")
    length = int(line)
    payload = stream.read(length)
    if len(payload) != length:
        raise RuntimeError("the backend closed inside its framed reply")
    return json.loads(payload)


def main():
    root = Path(__file__).resolve().parent
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    child = subprocess.Popen([sys.executable, str(root / "backend.py")], cwd=root,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=None, env=environment)
    try:
        ready = read_frame(child.stdout)
        if ready.get("op") != "ready" or ready.get("protocol") != 1:
            raise RuntimeError("the public ready announcement is incomplete")
        print(json.dumps({"announcement": ready["backend"], "capabilityCount": len(ready["capabilities"])}))
        request_id = 0

        def invoke(operation, arguments):
            nonlocal request_id
            request_id += 1
            frame = {"request_id": request_id, "op": operation, "args": arguments}
            payload = json.dumps(frame, separators=(",", ":")).encode()
            child.stdin.write(str(len(payload)).encode() + b"\n" + payload)
            child.stdin.flush()
            reply = read_frame(child.stdout)
            if reply.get("request_id") != request_id:
                raise RuntimeError("the backend changed a request identity")
            print(json.dumps({"request": request_id, "operation": operation,
                              "status": reply.get("status"),
                              "envelope": reply.get("value", {}).get("ctor") if isinstance(reply.get("value"), dict) else None}))
            if reply.get("status") != "ok":
                raise RuntimeError(json.dumps(reply))
            return reply["value"]

        one = node("obj.sets.fin", 1)
        q = node("obj.sets.rationals")
        qr = node("obj.rings.rationals")
        qc = node("obj.commutative_rings.rationals")
        x = node("obj.sets.rational_dual_x")
        y = node("obj.sets.rational_dual_y")
        xr = node("functorAction", node("fun.commutative_rings.ring"), node("obj.commutative_rings.rational_dual_x"))
        point = node("element", x, node("add", node("generator"), node("numeral", 7)))
        shifted = invoke("cmp.rational_dual.translation", node("presentationApply", [], False, x, y, point))
        invoke("cmp.rational_dual.translation", node("presentationApply", [], True, y, x, shifted))
        invoke("op.rings.pow", apply("op.rings.pow", [xr, 5], one, x, x, point))
        finite_domain = node("obj.sets.fin", 3)
        family = [[0, point], [1, node("element", x, node("generator"))], [2, node("element", x, node("numeral", 4))]]
        invoke("op.rings.pow", apply("op.rings.pow", [xr, 2], finite_domain, x, x, family))

        rows = [[0, [[0, [2, 3]], [1, [-5, 7]]]],
                [1, [[0, [1, 1]], [1, [4, 9]]]],
                [2, [[0, [0, 1]], [1, [3, 2]]]]]
        v2, v3 = node("obj.modules.vectors", qr, 2), node("obj.modules.vectors", qr, 3)
        invoke("mor.modules.rectangular_linear_map", apply(
            "mor.modules.rectangular_linear_map", [3, 2, qc, rows], one, v2, v3,
            [[0, [11, 5]], [1, [-2, 1]]]))
        matrix_arrow = node("typedMap", v2, v3, node("mor.modules.rectangular_linear_map", 3, 2, qc, rows))
        whole_map = invoke("mor.modules.rectangular_linear_map", apply(
            "mor.modules.rectangular_linear_map", [3, 2, qc, rows], v2, v2, v3,
            node("typedMap", v2, v2, node("identity", v2, v2))))
        linear_maps = node("obj.sets.maps", v2, v3)
        invoke("mor.sets.equality", apply("mor.sets.equality", [linear_maps], one,
               node("objectProduct", linear_maps, linear_maps), node("obj.sets.truth_values"),
               [whole_map, matrix_arrow]))

        lift = "lift.bilin_module.change_value_restriction"
        value_map = node("typedMap", q, q, node("identity", q, q))
        parameters = [q, q, q, value_map]
        action = node("fun.bilin_module.change_value", *parameters)
        source = node("obj.bilin_module.degenerate_plane_target")
        base_apex = node("obj.bilin_module.degenerate_plane")
        ambient = node("functorAction", action, source)
        inclusion = node("typedMap", base_apex, ambient, node("mor.bilin_module.degenerate_plane_map"))
        base = node("subobject", base_apex, ambient, inclusion)
        outputs = []
        for component in ("obj", "hom", "forward", "backward"):
            packet = node("monoLiftInput", lift, action, source, base, outputs[:])
            packet["parameters"] = parameters
            outputs.append(invoke(lift + "#" + component, packet))

        factor = node("liftFactorInput", lift, action, source, base, outputs[:], outputs[2], outputs[1])
        factor["parameters"] = parameters
        invoke(lift + "#factor", factor)
        pairing = "mor.sets.bilin_module_pairing"
        object_data = outputs[0]
        invoke(pairing, apply(pairing, [qc, node("obj.modules.regular", qr), object_data],
                             one, node("objectProduct", object_data, object_data), q,
                             [[[0, [3, 4]], [1, [8, 3]]],
                              [[0, [-1, 2]], [1, [6, 5]]]]))

        restriction = "lift.bilin_module.restrict"
        forget = node("fun.bilin_module.forget", q, q)
        formed_source = node("obj.bilin_module.degenerate_plane")
        formed_target = node("obj.bilin_module.degenerate_plane_target")
        module_source = node("functorAction", forget, formed_source)
        module_target = node("functorAction", forget, formed_target)
        formed_map = node("typedMap", formed_source, formed_target, node("mor.bilin_module.degenerate_plane_map"))
        module_map = node("typedMap", module_source, module_target, node("map", forget, formed_map))
        module_arrow = node("arrow", module_source, module_target, module_map)
        native_kernel_reply = invoke("fun.arrows_modules.kernel",
               {"ctor": "fun.arrows_modules.kernel", "args": [qr], "receiver": module_arrow})
        native_kernel = native_kernel_reply["args"][0]
        restriction_outputs = []
        for component in ("obj", "hom", "forward", "backward"):
            packet = node("monoLiftInput", restriction, forget, formed_source, native_kernel,
                          restriction_outputs[:])
            packet["parameters"] = [q, q]
            restriction_outputs.append(invoke(restriction + "#" + component, packet))
        restricted_image = node("functorAction", forget, restriction_outputs[0])
        restricted_maps = node("obj.sets.maps", restricted_image, restricted_image)
        roundtrip = node("compose", restriction_outputs[2], restriction_outputs[3])
        invoke("mor.sets.equality", apply("mor.sets.equality", [restricted_maps], one,
               node("objectProduct", restricted_maps, restricted_maps), node("obj.sets.truth_values"),
               [roundtrip, node("identity", restricted_image, restricted_image)]))
        factor = node("liftFactorInput", restriction, forget, formed_source, native_kernel,
                      restriction_outputs[:], restriction_outputs[2], restriction_outputs[1])
        factor["parameters"] = [q, q]
        native_factor = invoke(restriction + "#factor", factor)
        factor_maps = node("obj.sets.maps", restriction_outputs[0], restriction_outputs[0])
        invoke("mor.sets.equality", apply("mor.sets.equality", [factor_maps], one,
               node("objectProduct", factor_maps, factor_maps), node("obj.sets.truth_values"),
               [native_factor, node("identity", restriction_outputs[0], restriction_outputs[0])]))

        value_diagram = node("pair", q, q)
        value_product = invoke("lim.sets.product", value_diagram)["args"][0]
        paired_values = value_product["args"][0]
        first_projection = node("typedMap", paired_values, q,
                                node("constructionField", "lim.sets.product", value_diagram, value_product, 1))
        paired_form = node("obj.bilin_module.degenerate_plane_with_dot")
        changed_parameters = [q, paired_values, q, first_projection]
        changed_action = node("fun.bilin_module.change_value", *changed_parameters)
        changed_form = node("functorAction", changed_action, paired_form)
        changed_inclusion = node("typedMap", changed_form, changed_form,
                                 node("identity", changed_form, changed_form))
        changed_base = node("subobject", changed_form, changed_form, changed_inclusion)
        changed_outputs = []
        for component in ("obj", "hom", "forward", "backward"):
            packet = node("monoLiftInput", lift, changed_action, paired_form, changed_base, changed_outputs[:])
            packet["parameters"] = changed_parameters
            changed_outputs.append(invoke(lift + "#" + component, packet))
        invoke(pairing, apply(pairing, [qc, paired_values, changed_outputs[0]], one,
                             node("objectProduct", changed_outputs[0], changed_outputs[0]), paired_values,
                             [[[0, [5, 3]], [1, [-4, 7]]], [[0, [-2, 9]], [1, [1, 4]]]]))
        for operation in ("mor.bilin_module.pulled_back_forward", "mor.bilin_module.pulled_back_backward"):
            parameters = changed_parameters + [paired_form, changed_inclusion]
            comparison_arrow = node(operation, *parameters)
            compare_source = node("morphismEndpoint", comparison_arrow, "source")
            compare_target = node("morphismEndpoint", comparison_arrow, "target")
            invoke(operation, apply(operation, parameters, one, compare_source, compare_target,
                                   [[0, [-3, 5]], [1, [7, 8]]]))

        finite = node("obj.sets.fin", 4)
        subsets = node("obj.sets.two_subsets", finite)
        subset_object = invoke("meth.two_subsets", finite)
        invoke("meth.cardinality", subset_object)
        reverse_order = node("obj.linear_orders.fin_reverse", 4)
        invoke("op.linear_orders.le", apply("op.linear_orders.le", [reverse_order], one,
               node("objectProduct", finite, finite), node("obj.sets.truth_values"), [1, 3]))
        constant_subset = node("typedMap", one, subsets, [[0, [0, 2]]])
        subset_map = node("map", node("fun.core_sets.two_subsets"), node("mor.core_sets.fin_rev", 4))
        subset_point = node("point", node("compose", constant_subset, subset_map))
        invoke("mor.sets.equality", apply("mor.sets.equality", [subsets], one,
               node("objectProduct", subsets, subsets), node("obj.sets.truth_values"),
               [subset_point, [0, 1]]))
        finite_maps = node("obj.sets.maps", finite, finite)
        finite_function = node("typedMap", finite, finite, [[0, 2], [1, 0], [2, 3], [3, 1]])
        composite_function = node("compose", finite_function, node("typedMap", finite, finite, [[0, 3], [1, 2], [2, 1], [3, 0]]))
        invoke("mor.sets.equality", apply("mor.sets.equality", [finite_maps], one,
               node("objectProduct", finite_maps, finite_maps), node("obj.sets.truth_values"),
               [finite_function, composite_function]))

        sets = node("category", "cat.sets", [])
        aut_action = node("con.automorphisms", sets)
        aut_object = node("functorAction", aut_action, node("coreObject", finite))
        invoke("con.automorphisms", {"ctor": "con.automorphisms", "args": [sets], "receiver": node("coreObject", finite)})
        auto = [[[0, 1], [1, 2], [2, 3], [3, 0]], [[0, 3], [1, 0], [2, 1], [3, 2]]]
        comparison = node("coreIso", finite, finite, node("mor.sets.fin_rev", 4), node("mor.sets.fin_rev", 4))
        mapped_auto = invoke("con.automorphisms#map", node("apply", "con.automorphisms#map", [sets],
               node("map", aut_action, comparison), one, aut_object, aut_object, auto))
        invoke("mor.sets.automorphism_evaluation", apply("mor.sets.automorphism_evaluation",
               [sets, node("functor", "fun.sets.identity", []), finite], one,
               node("objectProduct", aut_object, finite), finite, [mapped_auto, 2]))

        groups = node("category", "cat.groups", [])
        quotient = node("obj.groups.cyclic_quotient", 7)
        cyclic = node("obj.groups.cyclic", 7)
        group_action = node("con.automorphisms", groups)
        quotient_aut = node("functorAction", group_action, node("coreObject", quotient))
        cyclic_aut = node("functorAction", group_action, node("coreObject", cyclic))
        invoke("con.automorphisms", {"ctor": "con.automorphisms", "args": [groups], "receiver": node("coreObject", quotient)})
        residue = node("obj.sets.integers_mod", 7)
        monoid = node("functorAction", node("fun.rings.multiplicative_monoid"), node("obj.rings.integers_mod", 7))
        units = node("obj.sets.units", monoid)
        unit_point = node("admittedPoint", "obj.sets.units", [monoid], one, residue, units,
                          node("element", residue, node("numeral", 3)))
        group_auto = invoke("mor.groups.cyclic_quotient_aut_by_unit", apply(
               "mor.groups.cyclic_quotient_aut_by_unit", [7], one, units, quotient_aut, unit_point))
        quotient_comparison = node("coreIso", quotient, cyclic,
               node("presentation", "cmp.groups.cyclic_quotient_residue", [7], False),
               node("presentation", "cmp.groups.cyclic_quotient_residue", [7], True))
        transported_auto = invoke("con.automorphisms#map", node("apply", "con.automorphisms#map", [groups],
               node("map", group_action, quotient_comparison), one, quotient_aut, cyclic_aut, group_auto))
        invoke("mor.groups.automorphism_forward", apply("mor.groups.automorphism_forward",
               [cyclic, transported_auto], one, cyclic, cyclic, 4))

        integer_ring = node("obj.rings.integers")
        scalar_map = node("typedMap", integer_ring, qr,
               node("map", node("fun.commutative_rings.ring"), node("mor.commutative_rings.integer_coefficients", qc)))
        restricted = invoke("fun.modules.reindex", {"ctor": "fun.modules.reindex", "args": [scalar_map], "receiver": v2})
        invoke("op.modules.scalar_action", apply("op.modules.scalar_action", [integer_ring, restricted], one,
               node("objectProduct", node("obj.sets.integers"), restricted), restricted,
               [-3, [[0, [5, 4]], [1, [-7, 3]]]]))
        restricted_image = node("functorAction", node("fun.modules.reindex", scalar_map), v2)
        total_source = node("functorAction", node("fun.modules.fibre_inclusion", integer_ring), restricted_image)
        total_target = node("functorAction", node("fun.modules.fibre_inclusion", qr), v2)
        invoke("fun.modules.reindex#cartesian", node("apply", "fun.modules.reindex#cartesian", [v2, scalar_map],
               node("cartesianMap", "fun.modules.reindex", [scalar_map], v2), one,
               total_source, total_target, [[0, [9, 2]], [1, [-11, 5]]]))

        naturals = node("obj.sets.naturals")
        for coefficient, coefficient_set in [(qc, q), (node("obj.commutative_rings.integers_mod", 7), residue)]:
            series_object = node("obj.sets.power_series", coefficient)
            topology = node("obj.hausdorff_topological_monoids.power_series", coefficient)
            summable = node("obj.sets.summable_families", topology, naturals)
            family = node("mor.sets.successor_power_series_terms", coefficient)
            admitted_family = node("admittedPoint", "obj.sets.summable_families", [topology, naturals],
                                   one, node("obj.sets.maps", naturals, series_object), summable, family)
            summed = invoke("bind.sets.power_series_sum", apply("bind.sets.power_series_sum",
                     [coefficient, naturals], one, summable, series_object, admitted_family))
            invoke("mor.sets.power_series_coefficient", apply("mor.sets.power_series_coefficient",
                   [coefficient], one, node("objectProduct", series_object, naturals), coefficient_set,
                   [summed, 23]))
        print(json.dumps({"completedRequests": request_id, "checks": "framing, startup, selected packet consumption and live opaque reuse only"}))
    finally:
        child.stdin.close()
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            child.terminate()
            child.wait(timeout=10)


if __name__ == "__main__":
    main()
