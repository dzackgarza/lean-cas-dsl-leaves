"""Published finite groups and their kernels, through GAP's native operations.

Routines: SymmetricGroup, CyclicGroup, AlternatingGroup, Size, IsFinite,
IsAbelian, IdentityMapping, GroupHomomorphismByImages, Kernel, Elements,
ListPerm and MinimalGeneratingSet. No group algorithm is implemented here.
"""
from __future__ import annotations

import json

from engine_python import require_engine

require_engine("CAS_GAP_PYTHON", ("sage.all__sagemath_gap", "sage.all"))

from cas_port import serve
from sage.libs.gap.libgap import libgap
from wire import aleph0, decision, finite_cardinal, named_object, numeral


def named(identifier: str, *parameters: object) -> dict[str, object]:
    return {"ctor": identifier, "args": list(parameters)}


def receiver(value: object) -> object:
    """Read retained carrier data; the caller owns its selected formal view."""
    if isinstance(value, dict) and "receiver" in value:
        return receiver(value["receiver"])
    ctor, args = named_object(value)
    if ctor in {"functorAction", "objectPresentation"}:
        if len(args) != 2:
            raise ValueError("incomplete retained object data")
        return receiver(args[1])
    if ctor in {"subobject", "valueData"}:
        if not args:
            raise ValueError("missing computational data")
        return receiver(args[0])
    return value


def group(value: object):
    ctor, args = named_object(receiver(value))
    if ctor in {"obj.groups.symmetric", "obj.sets.permutations"}:
        return libgap.SymmetricGroup(numeral(args[0]))
    if ctor in {"obj.groups.cyclic", "obj.sets.integers_mod"}:
        n = numeral(args[0])
        return libgap.FreeGroup(1) if n == 0 else libgap.CyclicGroup(n)
    if ctor == "obj.subgroups.alternating":
        return libgap.AlternatingGroup(numeral(args[0]))
    if ctor == "obj.subgroups.kernel":
        source, target, arrow = args
        return homomorphism(source, target, arrow).Kernel()
    if ctor in {"obj.bil_wform.root_lattice_a", "obj.bil_wform.root_lattice_a_dual"}:
        return libgap.AbelianGroup([0] * numeral(args[0]))
    if ctor == "obj.integral_lattice.e8":
        return libgap.AbelianGroup([0] * 8)
    if ctor == "obj.bil_wform.root_lattice_a_discriminant":
        n = numeral(args[0])
        # Lower the already published rootAGram datum to GAP's integer matrix.
        gram = [[-2 if i == j else (1 if abs(i - j) == 1 else 0)
                 for j in range(n)] for i in range(n)]
        if n == 0:
            return libgap.AbelianGroup([])
        diagonal = libgap.DiagonalOfMat(libgap.SmithNormalFormIntegerMat(gram))
        return libgap.AbelianGroup([abs(int(d)) for d in diagonal])
    raise ValueError("no GAP group for the published input form %s" % ctor)


def homomorphism(source: object, target: object, arrow: object):
    G, H = group(source), group(target)
    if isinstance(arrow, list):
        encode_source, encode_target = encoder(source, G), encoder(target, H)
        target_points = {json.dumps(encode_target(h), sort_keys=True): h for h in H.Elements()}
        graph = {}
        for pair in arrow:
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError("a group-map graph requires point-image pairs")
            key = json.dumps(pair[0], sort_keys=True)
            if key in graph:
                raise ValueError("a group-map graph repeats a domain point")
            graph[key] = target_points[json.dumps(pair[1], sort_keys=True)]
        if set(graph) != {json.dumps(encode_source(g), sort_keys=True) for g in G.Elements()}:
            raise ValueError("a finite group-map graph must contain every domain point")
        generators = G.GeneratorsOfGroup()
        images = [graph[json.dumps(encode_source(g), sort_keys=True)] for g in generators]
        return libgap.GroupHomomorphismByImages(G, H, generators, images)
    ctor, args = named_object(arrow)
    if ctor == "mor.groups.identity":
        return libgap.IdentityMapping(G)
    if ctor == "mor.groups.trivial":
        generators = G.GeneratorsOfGroup()
        return libgap.GroupHomomorphismByImages(G, H, generators,
                                               [H.One() for _ in generators])
    if ctor == "mor.groups.sign":
        generators = G.GeneratorsOfGroup()
        h = H.MinimalGeneratingSet()[0]
        images = [H.One() if int(g.SignPerm()) == 1 else h for g in generators]
        return libgap.GroupHomomorphismByImages(G, H, generators, images)
    if ctor == "compose" and len(args) == 2:
        # Only endomorphisms can be composed without a separately supplied
        # intermediate descriptor. Do not guess an intermediate chosen group.
        if source != target:
            raise ValueError("a composite group map requires its intermediate endpoint")
        f = homomorphism(source, target, args[0])
        g = homomorphism(source, target, args[1])
        return f * g
    raise ValueError("no GAP lowering for the published group arrow %s" % ctor)


def encoder(descriptor: object, G):
    ctor, args = named_object(receiver(descriptor))
    if ctor == "obj.subgroups.kernel":
        return encoder(args[0], group(args[0]))
    if ctor == "obj.subgroups.alternating":
        return encoder(named("obj.groups.symmetric", args[0]), G)
    if ctor in {"obj.groups.symmetric", "obj.sets.permutations"}:
        n = numeral(args[0])

        def encode(g):
            forward = [int(x) - 1 for x in libgap.ListPerm(g, n)]
            backward = [int(x) - 1 for x in libgap.ListPerm(g ** -1, n)]
            return [[[i, x] for i, x in enumerate(forward)],
                    [[i, x] for i, x in enumerate(backward)]]

        return encode
    if ctor in {"obj.groups.cyclic", "obj.sets.integers_mod"}:
        n = numeral(args[0])
        if n == 0:
            raise ValueError("the infinite cyclic carrier has no complete finite graph")
        if n == 1:
            return lambda g: 0
        generator = G.MinimalGeneratingSet()[0]
        exponents = {str(generator ** i): i for i in range(n)}
        return lambda g: exponents[str(g)]
    raise ValueError("no published finite point encoding for %s" % ctor)


def cardinality(value: object) -> dict[str, object]:
    size = group(value).Size()
    return aleph0() if size == libgap.infinity else finite_cardinal(int(size))


def finiteness(value: object) -> dict[str, object]:
    return decision(bool(group(value).IsFinite()))


def abelianness(value: object) -> dict[str, object]:
    return decision(bool(group(value).IsAbelian()))


def kernel(value: object) -> dict[str, object]:
    if isinstance(value, dict) and "receiver" in value:
        value = value["receiver"]
    ctor, args = named_object(value)
    if ctor != "arrow" or len(args) != 3:
        raise ValueError("a group kernel requires the complete arrow and both endpoints")
    source, target, arrow = args
    G = group(source)
    K = homomorphism(source, target, arrow).Kernel()
    declared = named("obj.subgroups.kernel", source, target, arrow)
    apex = named("functorAction", named("fun.subobjects_groups.domain"), declared)
    if not bool(G.IsFinite()):
        return named("subobject", apex, source, named("subobjectInclusion", declared))
    encode = encoder(source, G)
    inclusion = [[encode(g), encode(g)] for g in K.Elements()]
    return named("subobject", apex, source, inclusion)


serve("gap", str(libgap.eval("GAPInfo.Version")), "0.1.0", {
    "meth.cardinality": cardinality,
    "prop.is_finite": finiteness,
    "prop.is_abelian": abelianness,
    "prop.is_commutative": abelianness,
    "meth.group_arrow_kernel": kernel,
    "fun.arrows_groups.kernel": kernel,
})
