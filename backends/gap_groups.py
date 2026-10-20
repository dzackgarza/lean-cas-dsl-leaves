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
from wire import aleph0, decision, finite_cardinal, finite_data, finite_graph, finite_inventory, graph_data, named_object, numeral


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
    if ctor in {"subobject", "valueData", "finiteData"}:
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
    if ctor in {"obj.groups.units", "obj.sets.units"}:
        return units(args[0])
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


def native_ring(value: object):
    ctor, args = named_object(receiver(value))
    if ctor in {"obj.rings.integers", "obj.sets.integers"}:
        return libgap.Integers
    if ctor in {"obj.rings.rationals", "obj.sets.rationals"}:
        return libgap.Rationals
    if ctor in {"obj.rings.integers_mod", "obj.sets.integers_mod"}:
        n = numeral(args[0])
        return libgap.Integers if n == 0 else libgap.ZmodnZ(n)
    raise ValueError("no GAP ring lowering for the selected units parameter %s" % ctor)


def units(value: object):
    ctor, args = named_object(value)
    if ctor != "functorAction" or len(args) != 2:
        raise ValueError("units require the selected monoid object, including its actual structural action")
    edge, source = args
    edge_id, edge_parameters = named_object(edge)
    if edge_id == "fun.rings.multiplicative_monoid":
        R = native_ring(source)
        result = libgap.Units(R)
        if bool(libgap.IsGroup(result)):
            return result
        if bool(libgap.IsFinite(result)):
            # GAP returns the integer units as a finite scalar collection.
            # Its native matrix-group constructor supplies a group-map parent;
            # entries remain the original engine-computed units.
            return libgap.Group([libgap.ImmutableMatrix(R, [[u]]) for u in result])
        raise ValueError("the engine's infinite units collection has no native group-map representation")
    if edge_id == "fun.groups.monoid":
        return libgap.Units(group(source))
    raise ValueError("no native units lowering for the selected monoid action %s" % edge_id)


def homomorphism(source: object, target: object, arrow: object):
    G = group(source)
    H = G if source == target else group(target)
    return native_homomorphism(source, target, arrow, G, H)


def native_homomorphism(source: object, target: object, arrow: object, G, H):
    if not bool(libgap.IsGroup(G)) or not bool(libgap.IsGroup(H)):
        raise ValueError("the engine supplied a units collection without a native group-map representation")
    if isinstance(arrow, list) or (isinstance(arrow, dict) and arrow.get("ctor") == "finiteGraph"):
        arrow = graph_data(arrow)
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
    if ctor == "typedMap" and len(args) == 3:
        if args[0] != source or args[1] != target:
            raise ValueError("the typed map endpoints differ from the selected groups")
        return native_homomorphism(source, target, args[2], G, H)
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
        first_endpoints, second_endpoints = endpoints(args[0]), endpoints(args[1])
        if first_endpoints is None and second_endpoints is None:
            raise ValueError("a composite of unlabelled group graphs requires its intermediate chosen group")
        if first_endpoints is not None and second_endpoints is not None and first_endpoints[1] != second_endpoints[0]:
            raise ValueError("the supplied named group arrows disagree at the intermediate group")
        middle = first_endpoints[1] if first_endpoints is not None else second_endpoints[0]
        if middle == source:
            M = G
        elif middle == target:
            M = H
        else:
            M = group(middle)
        f = native_homomorphism(source, middle, args[0], G, M)
        g = native_homomorphism(middle, target, args[1], M, H)
        return libgap.CompositionMapping(g, f)
    raise ValueError("no GAP lowering for the published group arrow %s" % ctor)


def endpoints(arrow: object) -> tuple[object, object] | None:
    """Read endpoints supplied in the published named-map parameters."""
    if isinstance(arrow, list):
        return None
    ctor, args = named_object(arrow)
    if ctor == "typedMap" and len(args) == 3:
        return args[0], args[1]
    if ctor == "finiteGraph":
        return None
    if ctor == "mor.groups.sign":
        return named("obj.groups.symmetric", args[0]), named("obj.groups.cyclic", 2)
    if ctor == "mor.groups.identity":
        return args[0], args[0]
    if ctor == "mor.groups.trivial":
        return args[0], args[1]
    if ctor == "compose" and len(args) == 2:
        first, second = endpoints(args[0]), endpoints(args[1])
        if first is not None and second is not None:
            return first[0], second[1]
    return None


def encoder(descriptor: object, G):
    ctor, args = named_object(receiver(descriptor))
    if ctor == "obj.subgroups.kernel":
        return encoder(args[0], group(args[0]))
    if ctor == "obj.subgroups.alternating":
        return encoder(named("obj.groups.symmetric", args[0]), G)
    if ctor in {"obj.groups.units", "obj.sets.units"}:
        monoid_ctor, monoid_args = named_object(args[0])
        if monoid_ctor == "functorAction" and len(monoid_args) == 2:
            edge_id, _ = named_object(monoid_args[0])
            if edge_id == "fun.rings.multiplicative_monoid":
                def scalar(g):
                    return g[0][0] if bool(libgap.IsMatrix(g)) else g

                return lambda g: [int(libgap.Int(scalar(g))),
                                  int(libgap.Int(scalar(g ** -1)))]
            if edge_id == "fun.groups.monoid":
                encode = encoder(monoid_args[1], group(monoid_args[1]))
                return lambda g: [encode(g), encode(g ** -1)]
        raise ValueError("no point lowering for the selected units presentation")
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
    inventory = finite_inventory(value)
    if inventory is not None:
        points = libgap.Set([json.dumps(p, sort_keys=True) for p in inventory])
        return finite_cardinal(int(points.Size()))
    size = group(value).Size()
    return aleph0() if size == libgap.infinity else finite_cardinal(int(size))


def finiteness(value: object) -> dict[str, object]:
    inventory = finite_inventory(value)
    if inventory is not None:
        points = libgap.Set([json.dumps(p, sort_keys=True) for p in inventory])
        return decision(bool(points.IsFinite()))
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
    actual_map = homomorphism(source, target, arrow)
    G, K = actual_map.Source(), actual_map.Kernel()
    declared = named("obj.subgroups.kernel", source, target, arrow)
    apex = named("functorAction", named("fun.subobjects_groups.domain"), declared)
    if not bool(G.IsFinite()):
        return named("subobject", apex, source, named("subobjectInclusion", declared))
    encode = encoder(source, G)
    inclusion = [[encode(g), encode(g)] for g in K.Elements()]
    inventory = [pair[0] for pair in inclusion]
    return named("subobject", finite_data(apex, inventory), source,
                 finite_graph(inventory, inclusion))


serve("gap", str(libgap.eval("GAPInfo.Version")), "0.1.0", {
    "meth.cardinality": cardinality,
    "prop.is_finite": finiteness,
    "prop.is_abelian": abelianness,
    "prop.is_commutative": abelianness,
    "meth.group_arrow_kernel": kernel,
    "fun.arrows_groups.kernel": kernel,
})
