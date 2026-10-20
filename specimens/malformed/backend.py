"""Deliberately malformed result data in an otherwise framed reply."""
from __future__ import annotations
from cas_port import serve

def answer(value: object) -> dict[str, object]:
    return {"ctor": "finite", "args": ["not-a-natural"]}

serve("deliberate-malformed", "none", "0.1.0", {"meth.cardinality": answer})
