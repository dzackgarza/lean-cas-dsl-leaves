"""Record native engine interfaces used by the bounded adapter, without answer assertions."""
import json
from sage.all__sagemath_modules import FreeModule, matrix
from sage.rings.finite_rings.integer_mod_ring import Zmod
from sage.sets.finite_set_maps import FiniteSetMaps
from sage.version import version

print(json.dumps({"engine": "Sage", "version": version, "scope": "native interface observations only"}))
for modulus in (7, 6):
    scalar = Zmod(modulus)
    module = FreeModule(scalar, 2)
    morphism = module.hom(matrix(scalar, [[2, 1], [0, 0]]), module, side="right")
    record = {"modulus": modulus, "module_class": type(module).__name__,
              "map_class": type(morphism).__name__, "callable": callable(morphism),
              "iteration_interface": type(iter(module)).__name__}
    try:
        kernel = morphism.kernel()
        inclusion = module.coerce_map_from(kernel)
        record.update(kernel_class=type(kernel).__name__, inclusion_class=type(inclusion).__name__,
                      composition_class=type(morphism * inclusion).__name__)
        record["kernel_finiteness_interface"] = bool(kernel.is_finite())
        record["kernel_iterator_interface"] = type(iter(kernel)).__name__
    except Exception as exc:
        record.update(kernel_exception=type(exc).__name__, kernel_message=str(exc))
    print(json.dumps(record))
native = FiniteSetMaps(["domain-a", "domain-b"], ["target-a", "target-b"]).from_dict(
    {"domain-a": "target-b", "domain-b": "target-a"})
print(json.dumps({"finite_map_class": type(native).__name__, "callable": callable(native)}))
