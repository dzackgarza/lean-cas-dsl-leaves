#!/usr/bin/env python3
"""Public-port framing and composition checks for structural carrier actions.

Inputs are independently selected published packets. Only reply shape, complete
parameter/endpoint consumption and ownership are asserted. There are no expected
arithmetic answers, equality truths, functor laws or acceptance assertions.
"""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path

from completion_smoke import (ONE, Port, equality_reply, fields, identity, invoke,
                              node, owned, payload, require)


MODULE_ADDITIVE = "fun.modules.additive_group"
TO_GROUPS = "fun.additive_groups.to_groups"
GROUP_MONOID = "fun.groups.monoid"
SEMIGROUP = "fun.monoids.semigroup"
RING_ADD_COMM = "fun.rings.additive_commutative_monoid"
ADD_COMM_MONOID = "fun.additive_commutative_monoids.additive_monoid"
ADD_UNDERLYING = "fun.additive_monoids.underlying"
RING_MULTIPLICATIVE = "fun.rings.multiplicative_monoid"
ASSOCIATIVE = "clf.magmas.associative"
BINARY_OPERATION = "clf.sets.binary_operation"
FUNCTORS = (MODULE_ADDITIVE, TO_GROUPS, GROUP_MONOID, SEMIGROUP,
            RING_ADD_COMM, ADD_COMM_MONOID, ADD_UNDERLYING, RING_MULTIPLICATIVE)


def address(action):
    if action["ctor"] == "classifierForget":
        return "action:" + json.dumps({"classifierForget": action["args"][0]}, separators=(",", ":"))
    return action["ctor"]


def parameters(action):
    return [action] if action["ctor"] == "classifierForget" else action["args"]


def object_request(action, receiver):
    return {"ctor": address(action), "args": parameters(action), "receiver": receiver}


def map_request(action, source, target, original, domain=None, argument=None):
    if domain is None:
        domain, argument = source, identity(source)
    return invoke(address(action) + "#map", parameters(action), domain, source, target,
                  argument, node("map", action, original))


def object_step(port, label, action, receiver):
    return owned(port.request(label, address(action), object_request(action, receiver)))


def chain(port, label, source, target, original, actions, point):
    steps = []
    for index, action in enumerate(actions):
        name = label + "/" + str(index)
        image_source = object_step(port, name + "/source", action, source)
        image_target = object_step(port, name + "/target", action, target)
        supplied = node("typedMap", source, target, original)
        request = map_request(action, image_source, image_target, supplied)
        mapped = owned(port.request(name + "/whole map", address(action) + "#map", request))
        # A generalized arrow lives at its actual source object, including
        # non-Set stages. No terminal set is substituted for that domain.
        continued = owned(port.request(name + "/actual mapped-arrow reuse", address(action) + "#map",
                                        map_request(action, image_target, image_target,
                                                    identity(target, True), image_source, mapped)))
        steps.append({"action": action, "receiver": source, "otherReceiver": target,
                      "source": image_source, "target": image_target, "map": mapped,
                      "request": request, "supplied": supplied})
        source, target, original = image_source, image_target, continued
    equality_reply(port, label + "/final callable interface", source, target, original,
                   node("valueData", original))
    last = steps[-1]
    result = port.request(label + "/final closed point", address(last["action"]) + "#map",
                          map_request(last["action"], source, target, last["supplied"], ONE, point))
    require(isinstance(payload(result), (int, list, dict)), "final point omitted its data representation")
    domain = node("obj.sets.fin", 2)
    family = node("typedMap", domain, source,
                  node("finiteGraph", [0, 1], [[0, point], [1, node("element", source, point)]]))
    returned = owned(port.request(label + "/final generalized point", address(last["action"]) + "#map",
                                  map_request(last["action"], source, target, last["supplied"], domain, family)))
    equality_reply(port, label + "/final generalized interface", domain, target, returned, returned)
    return steps


def consume_structures(port, module_steps, multiplicative_steps, additive_steps, module_point, scalar):
    additive_group = next(step["source"] for step in module_steps if address(step["action"]) == MODULE_ADDITIVE)
    additive_monoid = object_step(port, "existing additive object consumes owned group",
                                  node("fun.additive_groups.additive_monoid"), additive_group)
    operation = "op.additive_monoids.add"
    result = port.request("existing addition on returned group image", operation,
                          invoke(operation, [additive_monoid], ONE,
                                 node("objectProduct", additive_monoid, additive_monoid),
                                 additive_monoid, [module_point, module_point]))
    require(isinstance(payload(result), list), "module addition reply changed its point form")
    group = next(step["source"] for step in module_steps if address(step["action"]) == TO_GROUPS)
    result = port.request("existing inverse on returned group", "op.groups.inverse",
                          invoke("op.groups.inverse", [group], ONE, group, group, module_point))
    require(isinstance(payload(result), list), "group inverse reply changed its point form")
    for label, steps, point in (("module", module_steps, module_point),
                                ("multiplicative", multiplicative_steps, scalar)):
        monoid = next(step["source"] for step in steps
                      if address(step["action"]) in {GROUP_MONOID, RING_MULTIPLICATIVE})
        operation = "op.monoids.mul"
        result = port.request(label + "/existing multiplication on actual image", operation,
                              invoke(operation, [monoid], ONE, node("objectProduct", monoid, monoid),
                                     monoid, [point, point]))
        require(isinstance(payload(result), (int, list, dict)), "multiplication reply lost point data")
        result = port.request(label + "/existing nullary operation on actual image", "op.monoids.one",
                              invoke("op.monoids.one", [monoid], ONE, ONE, monoid, identity(ONE)))
        require(isinstance(payload(result), (int, list, dict)), "unit reply lost point data")
    monoid = next(step["source"] for step in additive_steps if address(step["action"]) == ADD_COMM_MONOID)
    operation = "op.additive_monoids.add"
    port.request("addition consumes returned additive-commutative image", operation,
                 invoke(operation, [monoid], ONE, node("objectProduct", monoid, monoid), monoid,
                        [scalar, scalar]))
    underlying = object_step(port, "old additive monoid to new underlying action", node(ADD_UNDERLYING), additive_monoid)
    mapped = owned(port.request("old additive map to new underlying action", ADD_UNDERLYING + "#map",
                                map_request(node(ADD_UNDERLYING), underlying, underlying,
                                            identity(additive_monoid, True))))
    equality_reply(port, "old additive callable retained", underlying, underlying, mapped, mapped)


def controls(port, steps):
    for step in steps:
        action = step["action"]
        operation = address(action)
        malformed = object_request(action, step["receiver"])
        malformed["args"] = parameters(action) + [node("obj.rings.integers")]
        port.request(operation + "/extra object parameter", operation, malformed, expected="error")
        malformed = deepcopy(step["request"])
        malformed["args"][2]["args"][1]["args"][2] = node("typedMap", step["otherReceiver"],
                                                             step["receiver"], step["map"])
        port.request(operation + "/invalid actual callable interface", operation + "#map", malformed,
                     expected="error")
        malformed = deepcopy(step["request"])
        malformed["args"][4] = step["target"]
        port.request(operation + "/changed original image selection", operation + "#map", malformed,
                     expected="error")
    classifier = next(step for step in steps if step["action"]["ctor"] == "classifierForget")
    operation = address(classifier["action"])
    changed = node("classifierForget", classifier["action"]["args"][0], [node("obj.rings.integers")])
    malformed = deepcopy(classifier["request"])
    malformed["args"][1] = [changed]
    malformed["args"][2]["args"][0] = changed
    port.request("classifier nested parameters retained in both copies", operation + "#map", malformed,
                 expected="error")
    malformed = deepcopy(classifier["request"])
    malformed["args"][2]["args"][0] = node("classifierForget", BINARY_OPERATION, [])
    port.request("classifier map identity mismatch", operation + "#map", malformed, expected="error")
    port.request("unsupported source structure", GROUP_MONOID,
                 object_request(node(GROUP_MONOID), node("obj.groups.cyclic", 7)), expected="unsupported")


def manifest_check(contract):
    manifest = json.loads(Path(__file__).with_name("leaves.json").read_text())
    api = json.loads((contract / "api" / "declared-ports.json").read_text())
    operations = {row["operation"] for row in api["operations"]}
    inputs = {row["input"] for row in api["inputForms"]}
    actions = [node(functor) for functor in FUNCTORS]
    actions += [node("classifierForget", classifier, []) for classifier in (ASSOCIATIVE, BINARY_OPERATION)]
    for action in actions:
        operation = address(action)
        for suffix in ("", "#map"):
            rows = [row for row in manifest["registrations"] if row["operation"] == operation + suffix]
            require(len(rows) == 1 and rows[0]["input"] == operation + "#input",
                    "a structural action registration changed its complete-request input")
            require(operation + suffix in operations and operation + "#input" in inputs,
                    "a structural action registration is absent from the public snapshot")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=os.environ.get("CAS_LEAF_CONTRACT_PATH"))
    parser.add_argument("--engine", default=os.environ.get("CAS_SAGE_PYTHON"))
    arguments = parser.parse_args()
    require(bool(arguments.contract), "the published contract checkout is required")
    contract = Path(arguments.contract).resolve()
    manifest_check(contract)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(contract / "python"))
    if arguments.engine:
        environment["CAS_SAGE_PYTHON"] = arguments.engine
    backend = Path(__file__).with_name("backend.py").resolve()
    classifiers = [node("classifierForget", classifier, []) for classifier in (ASSOCIATIVE, BINARY_OPERATION)]
    module_actions = [node(functor) for functor in (MODULE_ADDITIVE, TO_GROUPS, GROUP_MONOID, SEMIGROUP)] + classifiers
    additive_actions = [node(functor) for functor in (RING_ADD_COMM, ADD_COMM_MONOID, ADD_UNDERLYING)]
    multiplicative_actions = [node(RING_MULTIPLICATIVE), node(SEMIGROUP)] + classifiers
    with Port(backend, environment) as port:
        ring = node("obj.rings.rationals")
        source, target = (node("obj.modules.vectors", ring, n) for n in (3, 2))
        coefficients = [[0, [[0, [2, 1]], [1, [1, 1]], [2, [-3, 1]]]],
                        [1, [[0, [0, 1]], [1, [4, 1]], [2, [1, 1]]]]]
        original = node("mor.modules.rectangular_linear_map", 2, 3, ring, coefficients)
        point = [[0, [3, 5]], [1, [-2, 7]], [2, [4, 9]]]
        module_steps = chain(port, "module carrier", source, target, original,
                             [node("fun.modules.fibre_inclusion", ring)] + module_actions, point)
        kernel = payload(port.request("actual kernel for full carrier composition", "fun.arrows_modules.kernel",
                                      {"ctor": "fun.arrows_modules.kernel", "args": [ring],
                                       "receiver": node("arrow", source, target,
                                                        node("typedMap", source, target, original))}))
        kernel_source, kernel_target, inclusion = fields(kernel, "arrow", 3)
        chain(port, "actual retained kernel carrier", kernel_source, kernel_target, inclusion,
              [node("fun.modules.fibre_inclusion", ring)] + module_actions,
              [[0, [0, 1]], [1, [0, 1]], [2, [0, 1]]])
        scalar = [4, 11]
        additive_steps = chain(port, "ring additive carrier", ring, ring, identity(ring),
                               additive_actions, scalar)
        multiplicative_steps = chain(port, "ring multiplicative carrier", ring, ring, identity(ring),
                                     multiplicative_actions, scalar)
        consume_structures(port, module_steps, multiplicative_steps, additive_steps, point, scalar)
        symbolic_group = node("valueData", node("valueData",
                              node("functorAction", node("fun.rings.additive_group"), ring)))
        group_steps = chain(port, "wrapped ring additive group", symbolic_group, symbolic_group,
                            identity(symbolic_group), [node(TO_GROUPS), node(GROUP_MONOID),
                                                       node(SEMIGROUP)] + classifiers, scalar)
        group_monoid = group_steps[1]["source"]
        carrier = group_steps[-1]["source"]
        domain = node("objectProduct", carrier, carrier)
        multiply = owned(port.request("retained scalar-addition whole callable", "op.monoids.mul",
                                      invoke("op.monoids.mul", [group_monoid], domain, domain,
                                             carrier, identity(domain))))
        equality_reply(port, "retained infinite scalar-addition interface", domain, carrier, multiply, multiply)
        modular = object_step(port, "actual coefficient ring", node("fun.commutative_rings.ring"),
                               node("obj.commutative_rings.integers_mod", 7))
        finite = node("obj.modules.vectors", modular, 1)
        finite_steps = chain(port, "owned finite coefficient", finite, finite, identity(finite),
                             [node("fun.modules.fibre_inclusion", modular)] + module_actions, [[0, 3]])
        result = port.request("finite actual carrier consumption", "meth.cardinality",
                              {"ctor": "meth.cardinality", "args": [node("fun.sets.cardinality")],
                               "receiver": finite_steps[-1]["source"]})
        require(payload(result).get("ctor") == "finite", "finite cardinality reply changed its form")
        last = additive_steps[-1]
        wrapped_source = node("valueData", last["receiver"])
        chain(port, "wrapped additive objects", wrapped_source, wrapped_source,
              identity(wrapped_source), [node(ADD_UNDERLYING)], scalar)
        symbolic_monoid = node("functorAction", node(RING_MULTIPLICATIVE), modular)
        symbolic_semigroup = node("functorAction", node(SEMIGROUP), symbolic_monoid)
        chain(port, "explicit portable semigroup", symbolic_semigroup, symbolic_semigroup,
              identity(symbolic_semigroup), classifiers, 3)
        # Swapping images changes the original receivers in this rectangular
        # module chain; there is no computed arithmetic assertion.
        controls(port, module_steps[1:])
        for action in (node(RING_ADD_COMM), node(ADD_COMM_MONOID), node(ADD_UNDERLYING), node(RING_MULTIPLICATIVE)):
            port.request("missing complete object receiver", address(action), node(address(action), *parameters(action)),
                         expected="error")
        primary_requests = port.requests
    with Port(backend, environment) as foreign:
        foreign.request("closed module additive owner", TO_GROUPS,
                        object_request(node(TO_GROUPS), module_steps[1]["source"]), expected="unsupported")
        foreign.request("closed scalar nested owner", RING_MULTIPLICATIVE,
                        object_request(node(RING_MULTIPLICATIVE), node("valueData", modular)), expected="unsupported")
        foreign.request("closed classifier callable", address(classifiers[-1]) + "#map",
                        module_steps[-1]["request"], expected="unsupported")
        foreign_requests = foreign.requests
    print(json.dumps({"script": Path(__file__).name, "primaryConnectionRequests": primary_requests,
                      "foreignOwnerRequests": foreign_requests, "result": "completed",
                      "boundary": "Public protocol only; no mathematical acceptance claim."}, indent=2))


if __name__ == "__main__":
    main()
