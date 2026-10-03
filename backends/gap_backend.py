"""GAP domain operations on residue sets and released named finite groups/subgroups.

Engine: GAP, through Sage's libgap (passagemath-gap, `sage.all__sagemath_gap`), run under
`$CAS_GAP_PYTHON` or the workspace's `.venv/bin/python` (`engine_python`). The named sets are sent
to GAP domains, and the operation to GAP's own operation on them:

* `obj.sets.integers_mod` at `n`: `ZmodnZ(n)`, and `Integers` at `n = 0` (the catalogue's `ZMod 0`
  is `ℤ`; GAP's `ZmodnZ` takes `n > 0`);
* `obj.sets.integers_mod_power` at `(n, k)`: `FullRowModule(R, k)` over that ring;
* `meth.cardinality`: `Size`, an integer or `infinity`;
* `prop.is_finite`: `IsFinite`.
* Symmetric/cyclic groups and alternating subgroups: `SymmetricGroup`,
  `CyclicGroup` (`FreeGroup(1)` for the infinite cyclic form), `AlternatingGroup`.
* Named kernels: `GroupHomomorphismByImages`, `CompositionMapping`, `Kernel`.
* `prop.is_abelian`: `IsAbelian`.

Speaks the port protocol through the contract's `cas_port` (on `PYTHONPATH`).
"""

import json

from engine_python import require_engine

require_engine("CAS_GAP_PYTHON", "sage.all__sagemath_gap")

from cas_port import serve  # noqa: E402  the leaf contract's reference port
from sage.libs.gap.libgap import libgap  # noqa: E402

from wire import aleph0, constructor, decision, finite_cardinal, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.2.0"
GAP_VERSION = str(libgap.eval("GAPInfo.Version"))


def residue_ring(n):
    n = numeral(n)
    return libgap.Integers if n == 0 else libgap.ZmodnZ(n)


# The GAP domain of each named set, from its numeral parameters.
DOMAINS = {
    "obj.sets.integers_mod": residue_ring,
    "obj.sets.integers_mod_power": lambda n, k: libgap.FullRowModule(residue_ring(n), numeral(k)),
    "obj.sets.permutations": lambda n: libgap.SymmetricGroup(numeral(n)),
    "obj.groups.symmetric": lambda n: libgap.SymmetricGroup(numeral(n)),
    "obj.groups.cyclic": lambda n: (libgap.FreeGroup(1) if numeral(n) == 0
                                    else libgap.CyclicGroup(libgap.IsPermGroup, numeral(n))),
    "obj.subgroups.alternating": lambda n: libgap.AlternatingGroup(numeral(n)),
    "obj.subgroups.kernel": lambda G, H, f: kernel_domain(G, H, f),
}


def domain(value):
    ctor, params = named_object(value)
    if ctor not in DOMAINS:
        raise ValueError("no GAP domain for %s" % ctor)
    return DOMAINS[ctor](*params)


def homomorphism(value):
    """Lower released named group maps to GAP GroupHomomorphismByImages.

    Returns the selected endpoint forms together with the GAP map. Engine map
    composition uses CompositionMapping in its documented right-to-left order.
    """
    ctor, args = named_object(value)
    if ctor == "compose":
        first, second = constructor(value, "compose", 2)
        G, H, f = homomorphism(first)
        H2, K, g = homomorphism(second)
        if H != H2:
            raise ValueError("group map composition changes the selected endpoint")
        return G, K, libgap.CompositionMapping(g, f)
    if ctor == "identity":
        G, H = constructor(value, "identity", 2)
        if G != H:
            raise ValueError("identity changes its selected group endpoint")
        return G, H, libgap.IdentityMapping(domain(G))
    if ctor == "mor.groups.sign":
        n, = constructor(value, ctor, 1)
        G = {"ctor": "obj.groups.symmetric", "args": [numeral(n)]}
        H = {"ctor": "obj.groups.cyclic", "args": [2]}
        source, target = domain(G), domain(H)
        generators = source.GeneratorsOfGroup()
        unit = target.GeneratorsOfGroup()[0]
        images = [unit if int(g.SignPerm()) == -1 else target.One() for g in generators]
    elif ctor == "mor.groups.identity":
        G, = constructor(value, ctor, 1)
        H = G
        source, target = domain(G), domain(H)
        generators = source.GeneratorsOfGroup()
        images = list(generators)
    elif ctor == "mor.groups.trivial":
        G, H = constructor(value, ctor, 2)
        source, target = domain(G), domain(H)
        generators = source.GeneratorsOfGroup()
        images = [target.One() for _ in generators]
    else:
        raise ValueError("no GAP translation for group map %s" % ctor)
    mapping = libgap.GroupHomomorphismByImages(source, target, generators, images)
    if mapping == libgap.fail:
        raise ValueError("GAP could not construct the requested group homomorphism")
    return G, H, mapping


def kernel_domain(G, H, f):
    source, target, mapping = (graph_homomorphism(G, H, f) if isinstance(f, list)
                               else homomorphism(f))
    if G != source or H != target:
        raise ValueError("kernel parameters do not retain the map's selected endpoints")
    return mapping.Kernel()


def encode_point(form, element):
    """Released carrier records: Equiv has two graphs; Multiplicative is an alias.

    GAP acts on the right; inversion translates its permutation multiplication
    to the left composition of the public Equiv.Perm carrier.
    """
    ctor, args = named_object(form)
    if ctor in {"obj.groups.symmetric", "obj.sets.permutations"}:
        n, = args
        forward = libgap.ListPerm(element.Inverse(), numeral(n))
        inverse = libgap.ListPerm(element, numeral(n))
        return [[[i, int(x) - 1] for i, x in enumerate(forward)],
                [[i, int(x) - 1] for i, x in enumerate(inverse)]]
    if ctor == "obj.groups.cyclic":
        n, = args
        if numeral(n) == 0:
            raise ValueError("no finite graph encoding of the infinite cyclic group")
        # CyclicGroup(IsPermGroup,n) uses the regular cycle on 1,...,n.
        return int(libgap.OnPoints(1, element)) - 1
    raise ValueError("no released GAP point translation for %s" % ctor)


def decode_point(form, point):
    ctor, args = named_object(form)
    if ctor in {"obj.groups.symmetric", "obj.sets.permutations"}:
        n, = args
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("a permutation has forward and inverse graph fields")
        inverse = dict(point[1])
        return libgap.PermList([int(inverse[i]) + 1 for i in range(numeral(n))])
    if ctor == "obj.groups.cyclic":
        n, = args
        if isinstance(point, bool) or not isinstance(point, int):
            raise ValueError("a cyclic point is an integer")
        group = domain(form)
        generators = group.GeneratorsOfGroup()
        generator = generators[0] if len(generators) else group.One()
        return generator ** point
    raise ValueError("no released GAP point translation for %s" % ctor)


def graph_homomorphism(G, H, graph):
    if not isinstance(graph, list):
        raise ValueError("expected a finite homomorphism graph")
    source, target = domain(G), domain(H)
    table = {}
    for point, image in graph:
        key = json.dumps(point, sort_keys=True)
        if key in table:
            raise ValueError("homomorphism graph repeats a source point")
        table[key] = decode_point(H, image)
    generators = source.GeneratorsOfGroup()
    images = [table[json.dumps(encode_point(G, g), sort_keys=True)] for g in generators]
    mapping = libgap.GroupHomomorphismByImages(source, target, generators, images)
    if mapping == libgap.fail:
        raise ValueError("GAP rejected the requested homomorphism graph")
    for point, image in graph:
        if mapping.Image(decode_point(G, point)) != decode_point(H, image):
            raise ValueError("graph disagrees with GAP's homomorphism")
    return G, H, mapping


def kernel_presentation(source_form, kernel):
    """Choose an available result form through actual GAP isomorphism computations."""
    if kernel == domain(source_form):
        result = source_form
    elif bool(kernel.IsCyclic()):
        result = {"ctor": "obj.groups.cyclic", "args": [int(kernel.Size())]}
    else:
        raise ValueError("computed kernel needs a result group form not in this release")
    comparison = libgap.IsomorphismGroups(kernel, domain(result))
    if comparison == libgap.fail:
        raise ValueError("GAP found no isomorphism to the selected result presentation")
    return result, comparison, comparison.InverseGeneralMapping()


def op_group_kernel(value):
    f, zero = constructor(value, "parallelPair", 2)
    G, H, second = homomorphism(zero)
    first_G, first_H, first = (graph_homomorphism(G, H, f) if isinstance(f, list)
                              else homomorphism(f))
    if G != first_G or H != first_H:
        raise ValueError("parallel maps change their selected endpoints")
    if not bool(second.ImagesSource().IsTrivial()):
        raise ValueError("this GAP registration computes kernels against a trivial second map")
    kernel = first.Kernel()
    if not bool(kernel.IsFinite()):
        raise ValueError("this kernel result requires finite graph maps")
    apex, hom, inv = kernel_presentation(G, kernel)
    # The independent kernel carrier is a subtype of G; its proof field is omitted.
    forward = [[encode_point(G, x), encode_point(apex, hom.Image(x))]
               for x in kernel.Elements()]
    backward = [[encode_point(apex, y), encode_point(G, inv.Image(y))]
                for y in domain(apex).Elements()]
    return {"ctor": "cone", "args": [apex, backward],
            "presentation": {"hom": forward, "inv": backward}}


def op_cardinality(value):
    # GAP: Size. Both named sets are countable, so GAP's `infinity` is read as aleph0.
    size = domain(value).Size()
    return aleph0() if size == libgap.infinity else finite_cardinal(int(size))


def op_is_finite(value):
    # GAP: IsFinite
    return decision(bool(domain(value).IsFinite()))


def op_is_abelian(value):
    return decision(bool(domain(value).IsAbelian()))


if __name__ == "__main__":
    serve("gap", GAP_VERSION, ADAPTER_VERSION,
          {"meth.cardinality": op_cardinality, "prop.is_finite": op_is_finite,
           "prop.is_abelian": op_is_abelian, "lim.groups.kernel": op_group_kernel})
