# Computational leaves of cas-dsl

Untrusted computational backends registered in [`leaves.json`](leaves.json) for [`dzackgarza/cas-dsl`](https://github.com/dzackgarza/cas-dsl) over the generated category interfaces of [`dzackgarza/lean-categories`](https://github.com/dzackgarza/lean-categories) and [`dzackgarza/lean-cas-dsl-leaf-contracts`](https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts).

- **Semantic authority:** `lean-categories` owns every operation ID, input form, and category signature. Leaves ship no Lean and hold zero semantic authority ([`INTENT.md`](INTENT.md)).
- **Protocol:** Each program in [`backends/`](backends/) speaks `cas-computation/2` frames over stdio (`cas_port`).
- **Engines:** Executed inside `ghcr.io/dzackgarza/sage:develop` (`sage-research`) under `/sage/.venv/bin/python3` (`sage.all`, `libgap`, PARI, Singular, SymPy, Julia/Catlab).
- **Boundary enforcement:** Leaves never import `CasElaborator`, `cas_runtime`, or `tests/acceptance`.
