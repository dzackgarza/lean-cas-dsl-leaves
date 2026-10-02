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
                                    else libgap.CyclicGroup(numeral(n))),
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
    source, target, mapping = homomorphism(f)
    if G != source or H != target:
        raise ValueError("kernel parameters do not retain the map's selected endpoints")
    return mapping.Kernel()


def op_cardinality(value):
    # GAP: Size. Both named sets are countable, so GAP's `infinity` is read as aleph0.
    size = domain(value).Size()
    return aleph0() if size == libgap.infinity else finite_cardinal(int(size))


def op_is_finite(value):
    # GAP: IsFinite
    return decision(bool(domain(value).IsFinite()))


def op_is_abelian(value):
    return decision(bool(domain(value).IsAbelian()))


serve("gap", GAP_VERSION, ADAPTER_VERSION,
      {"meth.cardinality": op_cardinality, "prop.is_finite": op_is_finite,
       "prop.is_abelian": op_is_abelian})
