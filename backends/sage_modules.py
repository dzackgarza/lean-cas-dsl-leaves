"""Published module carriers through Sage FreeModule and quotient-space routines.

The upstream A-lattice Gram matrix is the negative Sage Cartan matrix.
Rank uses FreeModule.rank or quotient vector-space dimension; cardinality
uses FreeModule.cardinality or the Smith invariants of that Gram matrix.
"""
from __future__ import annotations

import json

from engine_python import require_engine

engine = require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_modules", "sage.all"))

from cas_port import serve
from sage.rings.finite_rings.integer_mod_ring import Zmod
from sage.version import version as SAGE_VERSION
from wire import aleph0, finite_cardinal, finite_inventory, named_object, numeral


def receiver(value: object) -> object:
    if isinstance(value, dict) and "receiver" in value:
        return receiver(value["receiver"])
    ctor, args = named_object(value)
    if ctor in {"functorAction", "objectPresentation"} and len(args) == 2:
        return receiver(args[1])
    if ctor in {"valueData", "subobject", "finiteData"} and args:
        return receiver(args[0])
    return value


def ring(value: object):
    ctor, args = named_object(receiver(value))
    if ctor in {"obj.rings.integers", "obj.commutative_rings.integers", "obj.sets.integers"}:
        return engine.ZZ
    if ctor in {"obj.rings.rationals", "obj.commutative_rings.rationals", "obj.sets.rationals", "obj.fields.rationals"}:
        return engine.QQ
    if ctor in {"obj.rings.integers_mod", "obj.commutative_rings.integers_mod", "obj.sets.integers_mod"}:
        return Zmod(numeral(args[0]))
    raise ValueError("no Sage coefficient ring for the selected form %s" % ctor)


def module(value: object):
    ctor, args = named_object(receiver(value))
    if ctor == "obj.modules.regular":
        return engine.FreeModule(ring(args[0]), 1)
    if ctor == "obj.modules.vectors":
        return engine.FreeModule(ring(args[0]), numeral(args[1]))
    if ctor in {"obj.bil_wform.root_lattice_a", "obj.bil_wform.root_lattice_a_dual"}:
        return engine.FreeModule(engine.ZZ, numeral(args[0]))
    if ctor == "obj.integral_lattice.e8":
        return engine.FreeModule(engine.ZZ, 8)
    raise ValueError("no Sage module for the selected form %s" % ctor)


def discriminant_gram(n: int):
    # Translation of the published rootAGram datum, also used by the existing
    # discriminant adapter. Modular Sage need not install the graph package
    # required by its optional CartanMatrix constructor.
    return engine.matrix(engine.ZZ, n, n,
                         lambda i, j: -2 if i == j else (1 if abs(i - j) == 1 else 0))


def rank(value: object) -> dict[str, object]:
    ctor, args = named_object(receiver(value))
    if ctor == "obj.bil_wform.root_lattice_a_discriminant":
        n = numeral(args[0])
        ambient = engine.FreeModule(engine.QQ, n)
        relations = discriminant_gram(n).change_ring(engine.QQ).row_space()
        return finite_cardinal(ambient.quotient(relations).dimension())
    return finite_cardinal(module(value).rank())


def cardinality(value: object) -> dict[str, object]:
    inventory = finite_inventory(value)
    if inventory is not None:
        from sage.sets.finite_enumerated_set import FiniteEnumeratedSet
        points = FiniteEnumeratedSet([json.dumps(p, sort_keys=True) for p in inventory])
        return finite_cardinal(points.cardinality())
    ctor, args = named_object(receiver(value))
    if ctor == "obj.bil_wform.root_lattice_a_discriminant":
        invariants = discriminant_gram(numeral(args[0])).elementary_divisors()
        if any(d == 0 for d in invariants):
            return aleph0()
        return finite_cardinal(engine.prod(abs(d) for d in invariants))
    result = module(value).cardinality()
    return aleph0() if result == engine.Infinity else finite_cardinal(result)


serve("sage", SAGE_VERSION, "0.1.0", {
    "meth.rank": rank,
    "meth.cardinality": cardinality,
})
