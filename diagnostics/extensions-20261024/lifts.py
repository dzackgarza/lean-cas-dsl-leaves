"""Callable pullbacks for the two publicly declared bilinear-module lifts."""

from sage.all import QQ

from cas_port import lift_factor_input, lift_input, lift_parameters, map_data, typed_map
from engine import Form
from wire import Callable, NativeIdentity, Unsupported, fields, node, same


RESTRICTION = "lift.bilin_module.restrict"
CHANGE_VALUE = "lift.bilin_module.change_value_restriction"


def selected_context(engine, lift_id, action, parameters):
    if lift_id == RESTRICTION:
        expected_action, count = "fun.bilin_module.forget", 2
    elif lift_id == CHANGE_VALUE:
        expected_action, count = "fun.bilin_module.change_value", 4
    else:
        raise Unsupported("the selected lift is outside this specimen")
    if len(parameters) != count:
        raise ValueError("the lift selection omits or adds an explicit declaration parameter")
    actual_parameters = fields(action, expected_action, count)
    same(actual_parameters, parameters, "selected lift action parameters")
    if engine.ring(parameters[0]) is not QQ:
        raise Unsupported("the diagnostic lift implementation requires rational scalars")
    # Read the actual selected value modules and change-of-values callable. They
    # remain separate fields even when two selections have equal carriers.
    source_values = engine.module(parameters[1])
    if lift_id == CHANGE_VALUE:
        target_values = engine.module(parameters[2])
        change = engine.function(parameters[3], parameters[1], parameters[2])
        return source_values, target_values, change
    return source_values, None, None


def original_object(kind, source):
    return fields(source, "arrow", 3)[0] if kind == "liftInput" else source


def check_prefix(action, source, base, outputs):
    if not outputs:
        return
    obj = outputs[0]
    apex = fields(base, base["ctor"], 3)[0]
    changed = node("functorAction", action, obj)
    expected = ((obj, source), (changed, apex), (apex, changed))
    for output, (domain, codomain) in zip(outputs[1:], expected):
        actual_domain, actual_codomain, _ = typed_map(output)
        same(actual_domain, domain, "retained lift-map source")
        same(actual_codomain, codomain, "retained lift-map target")


def field(engine, operation, packet):
    kind, lift_id, action, original_source, base, outputs = lift_input(packet, operation)
    parameters = lift_parameters(packet)
    selected_context(engine, lift_id, action, parameters)
    source = original_object(kind, original_source)
    apex, ambient, inclusion_data = fields(base, base["ctor"], 3)
    inclusion = engine.function(inclusion_data, apex, ambient)
    original = engine.form(source)
    base_module = engine.module(apex)
    check_prefix(action, source, base, outputs)
    port = operation[len(lift_id) + 1:]

    if port == "obj":
        # The whole actual request is retained with the native object, including
        # an original Arrow if one was supplied. No source arrow is synthesized
        # for the explicit-object variant. The pullback keeps K's module data.
        context = {"lift": lift_id, "selection": parameters, "action": action,
                   "sourceKind": kind, "source": original_source, "base": base}
        pulled_back = Form(base_module,
                           lambda x, y: original.pairing(inclusion(x), inclusion(y)),
                           context)
        return engine.session.keep(pulled_back)

    obj = outputs[0]
    # Retain and consume the actual previous object output. We do not replace it
    # by a fresh pullback object, a named sample, or a formal construction.
    actual_object = engine.form(obj)
    changed = node("functorAction", action, obj)
    if port == "hom":
        callable_data = engine.session.keep(Callable(obj, source, inclusion, inclusion.native))
        return map_data(obj, source, callable_data)
    if port == "forward":
        callable_data = engine.session.keep(Callable(changed, apex, lambda point: point,
                                                     NativeIdentity(changed, apex)))
        return map_data(changed, apex, callable_data)
    if port == "backward":
        callable_data = engine.session.keep(Callable(apex, changed, lambda point: point,
                                                     NativeIdentity(apex, changed)))
        return map_data(apex, changed, callable_data)
    raise Unsupported("the requested lift component is not published by this specimen")


def factor(engine, operation, packet):
    lift_id, action, source, base, outputs, g_data, f_data = lift_factor_input(packet, operation)
    parameters = lift_parameters(packet)
    selected_context(engine, lift_id, action, parameters)
    check_prefix(action, source, base, outputs)
    obj = outputs[0]
    engine.form(obj)
    apex, _, _ = fields(base, base["ctor"], 3)
    changed_domain, g_target, _ = typed_map(g_data)
    domain, f_target, _ = typed_map(f_data)
    same(g_target, apex, "universal factor's actual base-map target")
    same(f_target, source, "universal factor's actual cone target")
    g = engine.function(g_data, changed_domain, apex)
    f = engine.function(f_data, domain, source)
    # Both supplied maps and all preceding fields remain retained. The declared
    # factor's underlying action is g; f is a separate input, never an inferred
    # replacement for g. Compatibility proofs stay outside the wire protocol.
    retained = (parameters, action, source, base, outputs, g, f)

    def factor_action(point, context=retained):
        return context[-2](point)

    return map_data(domain, obj, engine.session.keep(Callable(domain, obj, factor_action, g.native)))
