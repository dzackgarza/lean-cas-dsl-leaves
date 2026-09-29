# Computational leaves of lean-cas-dsl

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a realization: it says how presentations of objects
that are already formal in `lean-categories` are computed, in any language, arbitrarily ugly
internally. It contributes zero mathematics.

* **Dependencies.** This package depends on the leaf contract (`lean-cas-dsl-leaf-contracts`) and
  `lean-categories` only. A leaf module imports `CasContract.Leaf`, `lean-categories` (with its
  catalogue), Mathlib and `CasLeaves.*`, and nothing else (`leafImportAllowed`, enforced by
  `register_leaf` and again by `cas-harness`).
* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`, which depends on
  this package; nothing here depends on it or can reach it. A leaf is never written or changed to
  make a test pass: `lean-cas-dsl`'s harness measures the installed leaves and reports gaps.
* **Missing mathematics goes upstream.** If a leaf seems to need a new category, method,
  placement, forwarding or edge, the defect is upstream: formalize it in `lean-categories`,
  release, re-pin, and only then realize it here.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency
  of the contract, the kernel or `lean-categories`, and name the deficiency in the commit.
* **Programs.** A leaf's backend program lives beside it (`CasLeaves/**/<leaf>/*.py`) and is
  located with `Backend.packageFile "cas_leaves" …`; it speaks the contract's port protocol
  (`cas_port`, put on its `PYTHONPATH` by `Backend.connect`). Engines: `CAS_GAP_PYTHON`,
  `CAS_SAGE_PYTHON` (default `.venv/bin/python` of the running workspace).

Build: `lake build`, with the same Lean toolchain and pins as `lean-cas-dsl`.
