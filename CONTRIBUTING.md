# Contributing to lean-cas-dsl-leaves

Each policy has a stable alphanumeric ID checked at commit time.

- **INP001 — Blind to acceptance tests.** Leaves never import, read, or reference `cas-dsl` acceptance `.cas` files or `CasElaborator` source.
- **MTH001 — Zero leaf-authored mathematics.** Every operation ID and input form comes from `lean-categories` via `declared-ports.json` / `extension-ports.json`. Missing mathematics is an upstream `lean-categories` task.
- **ENG001 — Glue over mature engines.** Delegate algorithms to SageMath (`sage.all`), GAP (`libgap`), PARI, Singular, SymPy, or Catlab; do not reimplement standard algebra/combinatorics in Python.
- **ENG002 — Single container engine.** Target `/sage/.venv/bin/python3` in `ghcr.io/dzackgarza/sage:develop` without workspace `.venv` traversal.
- **DAT001 — Consume supplied data.** Build engine values from supplied inventories, inclusions, parameters, and preceding lift outputs rather than recomputing canonical defaults.
- **DAT002 — Fail explicitly on unsupported inputs.** Never substitute a point or heuristic when a generalized domain or unowned opaque handle is unsupported.
- **DOC001 — Present tense rules.** Keep historical rationale in git commit messages rather than progress logs in Markdown.
