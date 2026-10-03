# Ground everything in INTENT.md (read before anything else)

[`INTENT.md`](INTENT.md) states the architecture these repositories exist to build: single semantic
authority in `lean-categories`; a kernel that consumes mathematics and authors none; leaves that hold
zero semantic authority and ship no mathematics; permanent, leaf-agnostic acceptance tests as the
only evidence about computations; a one-way workflow in which each stage is blind to the later ones.
Every decision, contract, gate, plan node and change here is grounded against it. Before writing
anything, check whether it, or anything it touches, violates that model or its invariants. A
violation found, in your task or outside it, is recorded as a defect where this repository records
defects, never worked around or silently kept.

# The evidence model: computation carries no semantic authority

The governing statement is `lean-cas-dsl/specs/architecture.md`, “Fundamental model and
obligation ownership” and “The evidence model”. `lean-categories` verifies and designs the
mathematical API, including its abstract computational obligations. The kernel interprets and
composes that API; the leaf contract publishes concrete invocation and representation protocols.

1. **Registration is a computational claim.** A leaf declares an implementation of an existing
   obligation on supported input representations. Registration, signature, representation and
   protocol checks enable invocation; they do not establish functional correctness.
2. **Declarations and outputs are used as computational claims and data.** The kernel consults
   registrations to dispatch and consumes answers to compute. Neither supplies mathematical
   definitions, laws, semantic placement, method availability or the truth of acceptance assertions.
   A declared comparison can compute the wrong map; a decoded cardinal can be well formed and wrong.
3. **Computational data remain computational.** A result may provide selected parameters,
   inclusions, actions, presentations and callable operations required by the published contract.
   It is not thereby a proved group, isomorphism, limit or colimit. A runtime result or successful
   contract check must never be promoted into a proof of the backend's mathematical correctness.
4. **Complete interfaces need not be eagerly materialized.** Preserve the selected data and
   required operations, including defining maps and forms. Completeness does not require enumerating
   an infinite object, serializing a whole function graph, eagerly computing inherited operations,
   choosing a canonical named object or proving all laws. Callable representations are legitimate
   when provided by the contract; leaves do not invent a replacement protocol locally.
5. **Acceptance is independent.** The permanent `lean-cas-dsl` suite compares observed answers
   with formal proofs, cited results or independent oracles. Assertions preserve the mathematical
   question when implementations change and do not inspect candidate leaves to establish expected
   answers. Passing cases provide evidence about those observations, never universal correctness.
   Leaf self-assessment and internal tests are not independent mathematical acceptance evidence.
6. **Available verified computation belongs to the formal side.** A genuinely checked Lean
   computation or proof may be used within its actual scope. The theoretical possibility of writing
   an algorithm in Lean does not require implementing it there before using an external engine.
7. **Wrong answers remain possible.** Malformed replies may be rejected and unavailable
   implementations may fail to execute. A well-formed wrong answer can pass protocol checks and
   escape current acceptance coverage. These failures must not change the mathematical language,
   weaken its domain or redefine an assertion.
8. **Improve the responsible component.** Formal correctness improves through correct definitions
   and proofs. Computational correctness improves through correct implementations, established
   engines and independent acceptance. A bad backend answer does not automatically require more
   upstream formalization. Independently inadequate mathematical or computational APIs may be
   improved at their owner; backend convenience cannot redefine meaning.
9. **Generic mechanisms belong to the kernel.** Leaves do not reproduce semantic propagation,
   dispatch, construction, transport or result lifting to expose inherited interfaces. The formal
   constructions and selected maps determine those interfaces. Missing generic support is completed
   at its owner, rather than replaced with one forwarding accommodation per leaf.

# Computational leaves of lean-cas-dsl

> **You have no memory.** Nothing that exists only in chat survives compaction or the session.
> Every correction, finding and decision request is committed to its owning document first
> ([`lean-cas-dsl/AGENTS.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/AGENTS.md),
> "You have no memory"). The orchestrator is inside the threat model
> (`lean-cas-dsl/specs/architecture.md`).


> **The model to retain**
>
> `lean-categories` verifies and designs the mathematical API, including its abstract computational obligations. The kernel interprets and composes that API. Leaves declare implementations and supply computations under the published contracts. Acceptance tests their observed answers against independent mathematics.
>
> A verified specification is not a verified backend. Contract conformance is not functional correctness. Computational data may be used without becoming proof. A well-formed wrong answer is possible and must not redefine mathematical meaning.
>
> Interfaces follow formal constructions and selected structural maps, not backend classes or forwarding lists. Selected forms, parameters, inclusions, and actions are data; category membership does not reconstruct them.
>
> Each owner must complete its responsibility and may redesign inadequate implementation means. Existing code, schemas, gates, and assistant-authored plans are not mathematical facts or immutable requirements.
>
> When repairs multiply, inspect the prerequisite generating them. It may be an invented obligation. Removing that obligation is different from weakening the intended product.
>
> Judge progress by functioning required operations, their compositions, and the growth mechanism. Counts, local probes, accurate gap reports, and completed administrative machinery cannot substitute for that judgment.
>
> Preserve corrections and their causal examples in the existing owning documents. Do not assume conversational acknowledgment survives. Recording a settled correction is ordinary maintenance, not another approval transaction.

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf registration names an already formal operation and an
input form, and claims an implementation under the published computational contract. The leaf
supplies computations and required structured data in any language. It contributes zero mathematics
and ships no Lean. The kernel uses its declarations and answers for execution, without treating them
as semantic authority or correctness proofs. Independent acceptance measures observed answers.

**A leaf is glue over existing backends.** This is what a leaf is for, following the precedent of
`sage-categories` (`specs/leaves.md`, "Computation-engine boundary"; `AGENTS.md`, "Leaf categories
and hand-rolled mathematics"):
- **Wire, don't write.** A leaf wires a registered operation to a mature system that already
  computes it: GAP, Sage, Singular, Macaulay2, Julia, SymPy or published research code. Its shape
  is: declared input form, then engine input, then the engine's routine, then the engine result,
  then the declared result form. The leaf owns that translation and the choice of routine, and
  nothing else.
- **No hand-rolled algorithms.** A leaf does not reimplement what an engine provides, and each
  computation names the engine and routine it calls. New algorithmic code is written only when no
  existing system supplies the computation, and the leaf says so with the evidence.
- **No kernel machinery.** Generic dispatch, placement, propagation, composition and refinement
  are the kernel's, done generically. A leaf that finds itself doing any of them has found a gap in
  the kernel or the contract, and reports it upstream (the litmus role below). It is never absorbed
  into the leaf.
- **Engine values stay private.** Engine objects and types live inside the leaf's program; only a
  value of the declared result form crosses the port.

These engineering choices improve implementations; they do not certify them. Internal algorithms,
representations and caches may change within the contract. Independent acceptance remains the
evidence about observed mathematical answers.

The specimen history explains this boundary: `sage-categories` commit `27b3e507` made
Equifier construction decide its defining equation, creating a runtime admission burden;
`96054a58` removed the resulting `certified_structures` escape route. Requiring runtime proofs
for ordinary leaf realizations would recreate that cause. The research placement failures likewise
show why selected structure must be retained instead of recovered from category membership.
Retaining that data does not certify its correctness. The recent B0 reconstruction intervention
repeated the proof burden and generated reconstruction and approval machinery; those proposed
means must be reconsidered rather than reproduced in every leaf.

* **Authors.** Only the leaf subagent writes here, against the contract and catalogue on `main`.
  It is blind to the tests and never edits the contract, the kernel or `lean-categories`. The
  orchestrator delegates leaves and never writes, ports or polishes one
  (`lean-cas-dsl/specs/architecture.md`, "Authors: one role per agent"). The leaves present in
  this repository were written or kept alive by the orchestrator (`b818e4c`). That history explains
  the author-separation concern (`gov-leaf-rewrite`); labels and earlier rewrite plans do not establish
  correctness or make a particular remediation immutable.
* **All leaves live here.** Probe leaves included; none belongs in `lean-cas-dsl`.
* **Dependencies.** This package depends on the leaf contract (`lean-cas-dsl-leaf-contracts`) and
  `lean-categories` only. Every operation a leaf names is a row of `lean-categories`' catalogue.
* **Computational data carry no semantic authority.** Registrations and outputs are consumed
  under the contract. Required selected maps, parameters, forms and callable operations must remain
  available. No registration, result, self-test, status or certificate establishes mathematical laws
  or universal correctness. Ordinary computation does not require a proof of each backend result.
* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`, which depends on
  this package; nothing here depends on it, runs it or can reach it. A leaf is never written or
  changed to make a test pass: `lean-cas-dsl`'s harness measures the installed leaves and reports
  gaps. A leaf may keep whatever internal tests it wants; they are its own business and are
  not independent mathematical acceptance evidence.
* **Missing mathematics goes upstream.** If a leaf seems to need a new category, method,
  placement or semantic edge, the mathematics belongs to `lean-categories`; publish the required
  interface before registering an implementation here. Missing forwarding is generic kernel work,
  not new leaf-owned mathematics. Upstream may improve
  its abstract computational API as well as develop or correct mathematics. Concrete protocol gaps
  belong to the contract; missing generic interpretation belongs to the kernel.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency
  of the contract, the kernel or `lean-categories`, and name the deficiency in the commit.
* **Programs.** A leaf's implementation is a backend program in this repository, in whatever
  language its engine needs; it speaks the contract's port protocol (`cas_port`, put on its
  `PYTHONPATH` by the kernel). Engines: `CAS_GAP_PYTHON`, `CAS_SAGE_PYTHON` (default
  `.venv/bin/python` of the running workspace).

Every `require` tracks `main`. The commit and push tiers compile nothing.

