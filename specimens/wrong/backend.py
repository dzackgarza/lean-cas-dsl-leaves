"""Deliberately incorrect cardinal answer; not a mathematical implementation."""
from __future__ import annotations
from cas_port import serve

def answer(value: object) -> dict[str, object]:
    return {"ctor": "aleph0", "args": []}

serve("deliberate-wrong", "none", "0.1.0", {"meth.cardinality": answer})
