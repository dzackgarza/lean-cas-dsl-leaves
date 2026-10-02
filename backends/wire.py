"""The kernel's structural wire encoding, as the backends read and write it.

An input is a named object of the catalogue at its parameters,
`{"ctor": <object id>, "args": [<parameters>]}`, numeral parameters as JSON numbers. An answer is a
value of the operation's result form, a constructor application `{"ctor": <constructor>,
"args": [...]}` with the constructor spelled by its short name in the form's Lean type:

* `meth.cardinality` lands in `Card`, whose literal form `lit.cardinals` has the type
  `CardinalLiteral` with constructors `finite (n : ℕ)` and `aleph0`;
* a property is decided as `Option Bool`: `some true`, `some false`, or `none`.
"""


def named_object(value):
    """The object id and the parameters of an input."""
    if (not isinstance(value, dict) or not isinstance(value.get("ctor"), str)
            or not isinstance(value.get("args"), list)):
        raise ValueError("not a named object: %r" % (value,))
    return value["ctor"], value["args"]


def constructor(value, name, arity):
    """Read an explicit constructor application from the released structural wire."""
    ctor, args = named_object(value)
    if ctor != name or len(args) != arity:
        raise ValueError("expected %s with %d arguments: %r" % (name, arity, value))
    return args


def numeral(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("not a numeral parameter: %r" % (value,))
    return value


def finite_cardinal(n):
    return {"ctor": "finite", "args": [int(n)]}


def aleph0():
    return {"ctor": "aleph0", "args": []}


def decision(answer):
    """`answer` is True, False or None (undecided)."""
    if answer is None:
        return {"ctor": "none", "args": []}
    return {"ctor": "some", "args": [{"ctor": "true" if answer else "false", "args": []}]}
