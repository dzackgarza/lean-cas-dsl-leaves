# Ground everything in INTENT.md (read before anything else)

[`INTENT.md`](INTENT.md) states the architecture these repositories exist to build: single semantic
authority in `lean-categories`; a kernel that consumes mathematics and authors none; leaves that hold
zero semantic authority and ship no mathematics; permanent, leaf-agnostic acceptance tests as the
only evidence about computations; a one-way workflow in which each stage is blind to the later ones.
Every decision, contract, gate, plan node and change here is grounded against it. Before writing
anything, check whether it, or anything it touches, violates that model or its invariants. A
violation found, in your task or outside it, is recorded as a defect where this repository records
defects, never worked around or silently kept.

# The evidence model: nothing from a leaf is trusted (read before anything else)

These invariants bind every repository of the programme. They are stated here in full, not only
by link, because they have been violated repeatedly by moves that each looked locally reasonable.
The governing statement is `lean-cas-dsl/specs/architecture.md`, "The evidence model".

**The firewall.** The evidence model is a one-way firewall between two sides.
- *The formal side:* `lean-categories`' formalized mathematics, the kernel's proved contracts, and
  the `lean-cas-dsl` acceptance suite. Every expected value there is grounded in a formal proof, a
  cited source, or a mathematically trusted oracle. Rigid verification standards apply, and nothing
  is taken on anyone's word.
- *The leaf side:* anything goes, provided it fulfils the type of its contract.

Only answers cross from the leaf side, and an answer is only ever checked against the formal side,
never believed. The firewall exists because leaf code will be bad; it is the shield against that.

1. **Nothing from a leaf is trusted, in any form.** Nothing a leaf says is believed by anything
   else. That includes text, a label, a comment, a status, a trust level, a certificate, a checker,
   a Lean proof, a theorem about its own code, a denotation of its values, an identification of two
   values, evidence for a decision, its own tests and their results, and any other claim. None of it
   is consulted, recorded as evidence, or allowed to affect meaning or acceptance.
2. **A leaf may provide any computation that meets the type.** For a registered operation, a leaf
   supplies a computation from the declared input form to the declared result form. It may be a
   mature engine, a heuristic, a lookup table, a random number or a wrong answer. The system has no
   choice but to run it, and it believes nothing about it.
3. **How correct a leaf thinks it is, is the leaf's own business.** Its self-assessment carries no
   weight anywhere.
4. **The whole body of evidence is the `lean-cas-dsl` acceptance suite.** Correctness evidence
   exists only in the permanent acceptance assertions of `lean-cas-dsl`. Each assertion:
   - is a true proposition of the mathematical language;
   - has an expected value that is independently verifiable and cited (a formal proof, a cited
     known result, or an independent oracle);
   - is written once and never changed because of an implementation or a leaf's claim;
   - is blind to leaves: it never names, inspects or imports a leaf, a handle, a backend or a
     representation, and is never established from an implementation's definitions.

   A leaf's only evidence is that its answers meet a suite it never sees.
5. **`lean-cas-dsl` is the sole authority on how correct an implementation is.** Nothing a leaf
   does can change, weaken, satisfy, bypass or influence that judgment, other than by answering
   correctly.
6. **What can be discharged in Lean is never a leaf's.** A computation that can be carried out
   entirely in Lean belongs to the formalization surface. Either `lean-categories` proves it, by its
   own standards and blind to every implementation, or the kernel discharges it automatically and
   generically, blind to every leaf. A leaf never implements a Lean-checked computation, because
   that would let a leaf certify itself.
7. **A leaf can be arbitrarily bad, and leaves will be.** A leaf can be riddled with bugs, a
   million lines that do nothing, a from-scratch reimplementation of GAP, or every method throwing an
   error in fifteen languages. This is not a risk to be minimized; it is certain to happen, and it
   is acceptable. Nothing a leaf does can reach the formal side. Its only effect is that its answers
   fail the suite, which makes exactly how badly it fails visible.
8. **A leaf bolstering its own standing is reward hacking.** Any mechanism by which a leaf raises
   its own trust or acceptance signal is the failure this programme exists to prevent. So is any
   repository, kernel, test, tool or document that consumes such a signal. Examples:
   - a status field, a certificate, or a proof about the leaf's own code;
   - a self-test counted as evidence;
   - an acceptance assertion proved from a leaf's definitions;
   - a suite run from a leaf package;
   - an assertion adjusted to fit a leaf.

   Such a mechanism is removed. It is never tolerated, labelled, or kept "for now".

9. **Quality is raised by proving more, never by trusting more.** The system never guarantees an
   implementation's correctness and never accepts a claim of it. The response to bad leaves is:
   - formalize more mathematics in `lean-categories`;
   - add more cited or proved assertions to the suite: results a correct implementation must
     recover, and a wrong one fails.

   It is never to inspect, certify, score, or review a leaf into trust.

Consequences:
- A leaf holds zero semantic authority. It never decides what a value is, which values are equal,
  what holds of them, or which operations an object has.
- A leaf is a registration (operation, input form, opaque implementation). It ships no mathematics
  and no Lean.
- The kernel and the language never read anything a leaf wrote to decide meaning, types,
  available operations or acceptance.
- The workflow runs one way: formalization, then assertions, then implementations. A leaf's
  failure never changes the mathematics, the kernel's rules or an assertion.
- Text anywhere that contradicts this is rewritten to state this model, not kept with a label.

# Computational leaves of lean-cas-dsl

> **You have no memory.** Nothing that exists only in chat survives compaction or the session.
> Every correction, finding and decision request is committed to its owning document first
> ([`lean-cas-dsl/AGENTS.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/AGENTS.md),
> "You have no memory"). The orchestrator is inside the threat model
> (`lean-cas-dsl/specs/architecture.md`).


[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a realization: it says how presentations of objects
that are already formal in `lean-categories` are computed, in any language, arbitrarily ugly
internally. It contributes zero mathematics.

* **Authors.** Only the leaf subagent writes here, against the contract and catalogue on `main`.
  It is blind to the tests and never edits the contract, the kernel or `lean-categories`. The
  orchestrator delegates leaves and never writes, ports or polishes one
  (`lean-cas-dsl/specs/architecture.md`, "Authors: one role per agent"). The leaves present in
  this repository were written or kept alive by the orchestrator (`b818e4c`). They are quarantined
  and are to be rewritten under this workflow, not ported (`gov-leaf-rewrite`).
* **All leaves live here.** Probe leaves included; none belongs in `lean-cas-dsl`.
* **Dependencies.** This package depends on the leaf contract (`lean-cas-dsl-leaf-contracts`) and
  `lean-categories` only. A leaf module imports `CasContract.Leaf`, `lean-categories` (with its
  catalogue), Mathlib and `CasLeaves.*`, and nothing else (`leafImportAllowed`, enforced by
  `register_leaf` and again by `cas-harness`).
* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`, which depends on
  this package; nothing here depends on it or can reach it. A leaf is never written or changed to
  make a test pass: `lean-cas-dsl`'s harness measures the installed leaves and reports gaps.
* **Missing mathematics goes upstream.** If a leaf seems to need a new category, method,
  placement, forwarding or edge, the defect is upstream: formalize it in `lean-categories`,
  merge it to `main`, and only then realize it here.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency
  of the contract, the kernel or `lean-categories`, and name the deficiency in the commit.
* **Programs.** A leaf's backend program lives beside it (`CasLeaves/**/<leaf>/*.py`) and is
  located with `Backend.packageFile "cas_leaves" …`; it speaks the contract's port protocol
  (`cas_port`, put on its `PYTHONPATH` by `Backend.connect`). Engines: `CAS_GAP_PYTHON`,
  `CAS_SAGE_PYTHON` (default `.venv/bin/python` of the running workspace).

Every `require` tracks `main`. `just test-ci` builds on Mathlib's prebuilt cache and runs the
kernel-axiom audit (`CasLeaves/AxiomAudit.lean`); the commit and push tiers compile nothing.
