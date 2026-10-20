"""Sage Permutation realization of the named Fin reversal morphism."""

from engine_python import require_engine

require_engine("CAS_SAGE_PYTHON", ("sage.all__sagemath_combinat", "sage.all"))

from cas_port import point_invocation, serve, value_data  # noqa: E402
from sage.combinat.permutation import Permutation  # noqa: E402
from sage.version import version as SAGE_VERSION  # noqa: E402
from wire import finite_graph, graph_data, named_object, numeral  # noqa: E402

ADAPTER_VERSION = "0.1.0"


def permutation(value):
    ctor, args = named_object(value)
    if ctor == "compose" and len(args) == 2:
        return permutation(args[0]).right_action_product(permutation(args[1]))
    if ctor != "mor.sets.fin_rev" or len(args) != 1:
        raise ValueError("expected mor.sets.fin_rev with one parameter")
    n = numeral(args[0])
    return Permutation(list(range(n, 0, -1)))


def op_fin_rev(value):
    ctor, args = named_object(value)
    if ctor == "apply":
        operation, parameters, arrow, domain, source, target, data = point_invocation(
            value, "mor.sets.fin_rev")
        p = permutation(arrow)
        if isinstance(data, dict) and data.get("ctor") == "valueData":
            data = data["args"][0]
        if isinstance(data, dict) and data.get("ctor") == "element":
            point_source, arithmetic = data["args"]
            if point_source != source or arithmetic.get("ctor") != "numeral":
                raise ValueError("expected a numeral point at the selected finite source")
            data = arithmetic["args"][0]
        if isinstance(data, list) or (isinstance(data, dict) and data.get("ctor") in {"finiteGraph", "typedMap"}):
            graph = graph_data(data)
            return value_data(finite_graph([x for x, _ in graph],
                                          [[x, int(p(numeral(y) + 1)) - 1] for x, y in graph]))
        if domain not in ({"ctor": "obj.sets.fin", "args": [1]},
                          {"ctor": "obj.sets.terminal", "args": []}):
            raise ValueError("a non-closed reversal invocation requires its actual callable data")
        return value_data(int(p(numeral(data) + 1)) - 1)
    p = permutation(value)
    n = len(p)
    return finite_graph(list(range(n)), [[i, int(p(i + 1)) - 1] for i in range(n)])


serve("sage", SAGE_VERSION, ADAPTER_VERSION, {"mor.sets.fin_rev": op_fin_rev})
