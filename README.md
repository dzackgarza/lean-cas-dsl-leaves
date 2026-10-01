# Computational leaves of lean-cas-dsl

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a registration: it names an operation already formal in
`lean-categories` and an input form, and supplies an opaque implementation computing the
operation's declared result form, in any language, arbitrarily ugly internally. It contributes
zero mathematics and ships no Lean. A leaf lives on the leaf side of the firewall, where anything
goes that meets the type of its contract: the system runs it and believes nothing about it. Only
its answers cross, and they are checked against the formal side, `lean-cas-dsl`'s acceptance suite,
never believed.

* **Dependencies.** This package depends on the leaf contract (`lean-cas-dsl-leaf-contracts`) and
  `lean-categories` only. Every operation a leaf names is a row of `lean-categories`' catalogue.
* **Nothing a leaf says is believed.** A leaf supplies no proof, denotation, identification of
  values, decision evidence, status, trust level, certificate or checker, and nothing reads such a
  thing from it.
* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`, which depends on
  this package; nothing here depends on it, runs it or can reach it. A leaf is never written or
  changed to make a test pass: `lean-cas-dsl`'s harness measures the installed leaves and reports
  gaps. A leaf's own tests are evidence of nothing.
* **Missing mathematics goes upstream.** If a leaf seems to need a new category, method,
  placement, forwarding or edge, the defect is upstream: formalize it in `lean-categories`,
  merge it to `main`, and only then register an implementation here.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency
  of the contract, the kernel or `lean-categories`, and name the deficiency in the commit.
* **Programs.** A leaf's implementation is a backend program in this repository, in whatever
  language its engine needs; it speaks the contract's port protocol (`cas_port`, put on its
  `PYTHONPATH` by `Backend.connect`). Engines: `CAS_GAP_PYTHON`, `CAS_SAGE_PYTHON` (default
  `.venv/bin/python` of the running workspace).

Every `require` tracks `main`. The commit and push tiers compile nothing.

The leaves' code does not yet have this form; its replacement is tracked by the plan node
`gov-leaf-authority` in `lean-cas-dsl/specs/computational-core-plan.md`.
