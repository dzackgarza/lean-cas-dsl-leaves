# lean-cas-dsl-leaves Constitution

This repository holds the computational category implementations of the lean-cas-dsl
programme: the manifest `leaves.json`, the backend programs under `backends/` and the
deliberately bad replacement packages under `specimens/` (`README.md`). A category
implementation computes the operations that the formal mathematics of lean-categories
specifies, through the released contract of lean-cas-dsl-leaf-contracts.

The [kernel constitution][K] (lean-cas-dsl, v4.0.1) governs the whole programme. The
[contract constitution][RC] governs the released interface that a leaf implements. This file
states the obligations of those two constitutions that bind a leaf, and the rules of this
repository's own governing documents (`AGENTS.md`, `README.md`, `INTENT.md`). Article
identifiers `LV1` to `LV25` are stable. A kernel article is cited as `K:C<n>`, a contract
article as `RC<n>`, a requirement of the kernel feature as `kernel FR-0nn` and a requirement of
the contract feature as `contract FR-0nn`.

## Core Principles

### LV1. A leaf contributes no mathematics and ships no Lean

A leaf MUST NOT define a category, an operation, a law, a domain, a result type, a membership,
an inheritance, a value identity or a correctness criterion. All mathematics is formalized in
lean-categories (K:C1, K:C2; kernel FR-012, FR-013). A leaf ships no Lean code (K: policy
"Mathematical and leaf-code separation"; `AGENTS.md`).

- A leaf MUST NOT answer by lookup: a rank, a cardinality or another result written in the
  source in place of an engine computation.
- A named object that arrives as its descriptor is lowered to the engine constructor that
  builds it, in one lowering table of its category implementation. A leaf source MUST NOT
  write a defining datum (a Gram matrix, a defining polynomial) that an engine constructor
  builds, and MUST NOT write one datum in two places. Where the kernel unfolds a definition
  into published constructors and literals, the leaf computes from those (K:C22).
- A leaf that needs a declaration which lean-categories does not have has found an upstream
  gap. The gap is a lean-categories task (LV14); the leaf does not supply the mathematics.

### LV2. Nothing a leaf returns is believed

A registration claims that a backend computes an accepted operation at an admitted input form.
A reply is a computational claim. The kernel's acceptance suite is the only evidence about the
correctness of an answer (K:C2, K:C9, K:C10; K: policies "Computational evidence" and
"Independent harness"; `AGENTS.md`, "The evidence model").

- A leaf MUST NOT supply a proof, certificate, checker, denotation, status, trust level,
  identification of values or decision evidence. Nothing reads such a thing from a leaf.
- Nothing in this repository contains, names, imports or runs the acceptance suite. A test of
  this repository is an engineering check of the behaviour that it exercises; it is not
  evidence of a correct answer (LV18).

### LV3. The unit of work is the complete generated category interface

The released contract generates, for each category, its object constructors, morphism
constructors, operations at their actual domains, immediate functor object and morphism actions,
and the dependent parameters, choices, maps and comparisons of each request and result (RC3;
contract FR-014). A category implementation of this repository MUST implement that interface
for its category, with complete dependent results and their later uses (K:C23; RC2).

- A registration is an invocation port. A list of ports does not deliver a category
  implementation (K:C23; RC2).
- Constructors of objects are distinct from constructors of categories (contract FR-014).
- Each operation that the required workload assigns MUST execute (K:C23; kernel FR-033). An
  operation of the interface for which no engine routine and no known method exists is
  mathematically new work (LV6). The survey record names it as a gap with its searches (LV7); it
  is not implemented here without a separately authorized research assignment, and it is not
  omitted without that record.
- A category implementation is complete when each part of its generated interface is
  implemented or recorded as such a gap.

### LV4. Selected data stay selected

A request carries the selected construction: its endpoints, cones, cocones, comparisons,
parameters, captures and the outputs of earlier fields (K:C23). A leaf MUST compute from those
data.

- A leaf MUST NOT recognize an apex expression, search for a matching endpoint, recompute a named
  construction in place of supplied data, or substitute a canonical representative, a nearby
  presentation, an identity for a nonidentity map or a default value (K:C5, K:C23).
- Each reply MUST retain every selected structure, parameter, defining map, comparison, callable
  field and permitted choice of its generated result layout (`README.md`; K:C5, K:C8).
- A functor object action supplies its computed data to a public constructor of the target
  category. A functor morphism action returns an arrow at the two image endpoints that the
  request supplies (K:C23; contract FR-018).
- An inherited method request carries the receiver, one descriptor for each residual action and
  the method functor. The leaf realizes that composite and no other (K:C23; contract FR-017).

### LV5. A leaf is glue over mature engines

A category implementation connects mature existing computation: SageMath, GAP, Julia with Oscar,
Macaulay2, Singular, PARI, SymPy, python-flint or published research code (K:C23; K: policy
"Established computational implementations"; kernel FR-042). Its shape is: decode the request at
its generated layout, build the engine input, call the engine routine, encode the engine result
at the generated result layout.

- A leaf MUST NOT hand-roll an algorithm that an engine supplies.
- Each computation MUST name the engine and the routine that it calls, in the routine table of
  the feature specification and in the routine observations of its replies (contract FR-013;
  K:C15).
- A leaf MUST NOT rewrite an engine (kernel tasks T200 to T224, common definition).

### LV6. Known mathematics with no engine is implemented with its reference

A leaf computes an operation itself only where the survey record (LV7) shows that no surveyed
engine or research implementation provides it. Where the computation is known mathematics, the
leaf implements the known method and cites its reference: a published algorithm, a reference
implementation or a formalization (for example Mathlib's cardinal arithmetic,
`Mathlib.SetTheory.Cardinal.Arithmetic`, for the arithmetic of finite cardinals and $\aleph_0$).
This is ordinary leaf work. The feature specification names the survey row, the reference and the
requirement that assigns the computation (K: policy "Established computational implementations",
v4.0.1; K:C17).

- New algorithm work is mathematically new work: nontrivial mathematics for which no method
  exists anywhere. Only it needs a separately authorized research assignment, and no task of this
  repository supplies that authorization (K: same policy).

- A hand-rolled algorithm of an existing registration is removed when an engine supplies the
  computation, or justified by this rule (LV12).
- The control logic of an operation (branches on intermediate answers, recursion, composition of
  engine calls) is glue, not a hand-rolled algorithm (K:C22).

### LV7. A survey of engines precedes each category implementation

Before a category is implemented, its author surveys the engines and libraries that can supply
the operations of that category. The survey is open-ended (K:C17, K:C23). The survey record MUST
give, for each inspected source: its name, version or revision, the responsibility that it
supplies, the decision (use, fallback, reject) and the reasons. It MUST give each gap with the
searches made. The record is kept in the research record of the feature (`specs/*/research.md`)
and cited in the commit that adds the implementation. An unsuccessful search is not evidence that
no engine exists (K:C17).

### LV8. A leaf owns its control logic and may ask the kernel

A leaf owns all control logic of its implementation (K:C22). For each operation that it uses, a
leaf MAY:

- call an engine routine internally;
- call the code of another category implementation of this repository directly, as a declared
  software dependency (LV16);
- ask the kernel through the released contract, by a deferred program or by an adaptive
  suspension (RC4; contract FR-009, FR-010).

When it asks the kernel, it receives the result or the no-implementation outcome that names the
missing operation and input form, and it continues under its own control logic. A leaf MUST NOT
write the reserved constructor `noImplementation` (contract FR-010).

### LV9. Engine values stay private

Engine objects and types live inside the backend process. Only a value at the generated result
layout crosses the port. A provider-local callable crosses only as an export token with its
ordered captures (RC1; contract FR-006, FR-007; `AGENTS.md`).

### LV10. The kernel owns selection, dispatch, propagation and admission

The kernel owns source interpretation, the selection of meaning, domain and structures,
placement, propagation along structural functors, refinement by formal classifiers, realization
selection and dispatch, composition of published operations, admission, retention and scoped
ownership (K:C22, K:C23). A leaf MUST NOT recreate or bypass any of them.

- `leaves.json` holds no priority, order or cost. Zero, one or several eligible registrations give
  the no-implementation outcome, the call or implementation ambiguity (RC5; kernel FR-028).
- A declared preferred route of a registration names a surviving admitted binding and asserts no
  agreement between bindings (K:C6; RC6; `README.md`).

### LV11. Failure is explicit and stays stratified

A leaf reports each failure by its contract status (RC7; contract FR-011, FR-012):

- an input presentation outside the implementation: `status:"unsupported"` with the exact `op`;
- an engine failure: `status:"error"` with `kind` and `message`;
- a decision (a predicate or a property) that the engine cannot establish: the decision packet
  `none` (contract FR-012);
- an absent engine: the backend exits before its ready frame, and the kernel reports
  `unavailable`.

A leaf MUST NOT retry, switch to another engine after a failure, substitute a default or
declare semantic invalidity or ambiguity (K:C13; RC7). A branch on an observable intermediate
answer of an engine, for example an unevaluated integral that a second engine then computes,
is control logic (LV8) and names both routines.

### LV12. Existing registrations move into category implementations

The registrations of `leaves.json` move into the category implementations of their owner
categories (K:C23: computation outside a category implementation moves into one; kernel plan,
"Computational milestones"). A public-only leaf author performs each move (LV14).

- A routine moves with its registration when the survey of its category keeps it.
- A routine is replaced only when the survey shows that it is wrong for its operation: a
  hand-rolled algorithm where an engine supplies the computation, a routine of a different
  operation, or a mathematical datum held in the source (LV1, LV6).
- Each moved registration migrates to protocol 2 and to the generated interface (contract
  FR-001 to FR-018).

### LV13. Category implementations follow the structural order

A category implementation follows the implementations of the categories that its structural
functors and classifier forgets reach. The work starts with `cat.sets` and then proceeds in
independent directions (K:C23; kernel FR-042). The work is grouped into the computational
milestones of the kernel plan. Each milestone is vertical: its attainment holds as a computed
result through the public interface of each category on its route. A milestone does not end the
obligation of LV3 for its categories. Each task of this repository names the kernel task that it
serves.

- Implementation starts after kernel readiness F, against the contract release `v2.0.0`.
  Delivery uses the release `v2.0.1` on `main` (kernel specification, clarification of
  2026-11-25; contract FR-022).
- The kernel's acceptance suite assesses the attainment of a milestone. This repository holds no
  copy of its statements or expected answers (LV2, LV14).

### LV14. A public-only author needs nothing else

A leaf author receives the released contract (its `api/` documents, generated interface and
SDK), the accepted catalogue that the contract publishes, and backend resources: engine
documentation, engine source and the engines of the research container. A leaf author MUST NOT
receive kernel source, internal handoffs, the acceptance corpus, expected answers or prior
outcomes (K: "Independent authorship and permitted inputs"; RC9; kernel FR-015).

- The documents of this repository are inputs of a leaf author. They MUST contain only permitted
  inputs. A task names a kernel task by its identifier, to state which kernel work it serves; the
  text of that kernel task is not an input and is not copied here.
- A missing mathematical declaration is a lean-categories task. The task list names it before its
  consumer, with its issue, and a formalization author does it. The leaf author of the consumer
  does not formalize what its code implements (K: authorship rule; kernel specification,
  clarifications of 2026-11-07 and 2026-11-25).
- A missing contract form is a finding against the contract and goes to its owner. A leaf MUST
  NOT invent a wire encoding (RC1, RC8).
- A leaf that exposes a deficiency of the contract, the kernel or lean-categories names it in its
  commit (`AGENTS.md`, "Litmus role").

### LV15. An independent provider can replace this one

An independent provider can replace a category implementation of this repository through the
released contract and the same catalogue, with no change to the kernel, the contract, an existing
consumer or the acceptance questions (K:C12; K: "Independent extension evidence"; RC11).

- A result crosses only at its generated result layout; no consumer needs a private
  representation of this repository (LV9).
- The packages under `specimens/` are deliberately bad replacement packages. They use only the
  published registration and port contracts (`specimens/README.md`).

### LV16. Dependencies are declared and local

The package declares its software dependencies: the SDK of the released contract at its release
tag, and the engines of the research container (K:C23; K:C24, "Dependency locality"; contract
plan, disagreement D16).

- A category implementation imports only the engines and code that its algorithms use.
- A test of one category implementation runs without the backends of unrelated categories.
- Setup and dependency refresh are explicit commands outside the ordinary loop (K:C24).

## Engineering Defaults

### LV17. Test tiers

Tier 1 is the smallest set of tests that establishes the specified behaviour of the backends
through the happy paths and the branches that matter. Its total run time is seconds or minutes;
a slow tier 1 is a defect, repaired when it is found. Higher tiers add the long tail: examples,
permutations, edge cases and unusual combinations (K:C24).

### LV18. Test design

A test starts a real backend process of this repository under the engine of the research
container and drives it with the contract's protocol peer `cas-peer` over the length-framed pipes
(RC13; contract FR-020). The test sends requests that the generated interface builds. It checks
externally observable behaviour: negotiation, the reply at the generated result layout, the
retention of the selected data that the request supplied, the named engine routine, the
continuation after a no-implementation slot, and the stratum of an unsupported input.

- A test does not assert a mathematical answer. Correctness of answers belongs to the kernel's
  acceptance suite (LV2).
- No mock, fake engine, in-memory connection or direct handler call replaces the process, the
  engine or the framed connection. A test does not supply the behaviour that it checks (K:C19,
  K:C24).

### LV19. Contribution lessons

`CONTRIBUTING.md` records lessons from past mistakes as policies with stable alphanumeric
identifiers, grouped by category. Each policy covers a general class of contribution and, where
possible, shows a defective contribution beside its replacement (K:C24).

### LV20. Feedback cadence

Feedback loops of ten minutes or more are minimized. The commit-time check and the focused test
of the changed backend are the primary loop. Long runs (all backends against all scenarios, a
survey refresh) are for milestones: a batch of work, a push or a release (K:C24).

### LV21. Platform scope

The one platform is the research container, image `ghcr.io/dzackgarza/sage:develop`
(`AGENTS.md`, shared math container). Its engines are the SageMath library at
`/sage/.venv/bin/python3`, GAP through Sage `libgap`, Julia with Oscar through `juliacall`,
Macaulay2, Singular, PARI, SymPy and python-flint; the survey record names their versions.

- A backend runs under that one interpreter. It does not search for another interpreter, try a
  second package layout or select an engine at run time.
- Another platform or engine installation is added only on explicit request (K:C24).

### LV22. Logging

Each backend writes detailed logs to standard error, the diagnostic channel of the protocol
(contract FR-001, FR-023): for each request its id, operation and input form; each engine routine
that it calls, with its elapsed time; each request that it sends to the kernel; and the reply
status. Each test run writes a durable log under `tests/logs/`, kept in the repository (K:C24).

### LV23. Timing history

Each test and each computation has a timing record that includes setup (engine start-up),
fixtures, construction and nested work. Each record carries its run, revision, environment and
input. A test run appends its records to `tests/timing/records.jsonl`, kept in the repository
(K:C24; kernel FR-043).

### LV24. Timing triage

Optimization is selected from a triage table of measured costs: operation, cost per call,
multiplying factors, aggregate cost, priority, proposed remedy and remaining measured cost. The
aggregate is the cost per call times the calls, examples, fixtures, repetitions and other actual
multipliers. Optimization follows functionality (K:C21, K:C24).

### LV25. Construction cost

Construction of a mathematical object is close to instant. An object constructor request
computes no field that no request has demanded; a lazy field is an export that computes when it
is invoked (K:C7, K:C8, K:C24; contract FR-007). Only an explicit eager flag that the interface
declares requests eager computation. Engine start-up happens once for each backend process,
before its ready frame; timing triage applies when it dominates a computation.

## Ownership and Inputs

| Owner | Owns |
| --- | --- |
| lean-categories | All mathematics and the catalogue |
| lean-cas-dsl-leaf-contracts | Manifest shape, port protocol, failure strata, SDK, generated `api/` interface, protocol peer |
| lean-cas-dsl | Selection, preparation, dispatch, admission, retention; the acceptance suite; the computational milestones and their attainment |
| This repository | Category implementations: `leaves.json`, `backends/`, their tests, logs and timing records, the survey records, `specimens/` |

Changes here are leaf work (K: authorship roles). A leaf never changes the contract, the kernel or
lean-categories to fit itself (`AGENTS.md`, "Authors").

## Governance

This constitution governs the documents of this repository. Where `AGENTS.md`, `README.md`,
`CONTRIBUTING.md`, `DEFECTS.md`, `specimens/README.md` or a feature document conflicts with it,
the subordinate document is corrected. `INTENT.md` records the design discussion that grounds the
architecture; where a passage of it conflicts with this constitution, this constitution governs.
Where this constitution conflicts with the kernel constitution, the kernel constitution governs
and this file is corrected. The released contract governs the interface that a leaf implements.

An amendment identifies the article, the old and the new obligation and its source; it updates
this file, its version and its amendment date in the same change, and it reconciles the affected
documents. Versions are major for incompatible changes to an obligation, minor for additions,
patch for editorial corrections. Article identifiers are never renumbered.

Work order is the task list of the active feature under `specs/`. Its unchecked tasks are executed
in document order; the first unchecked task is active. A wait on an unavailable input blocks only
the task that needs it, and the work continues with the next task whose inputs are present
(K:C16, K:C21). A change of order is a committed edit of the task list that states its reason.

Work records, diagnostics and evidence go to the owning GitHub issue, not to a repository file
(K: "Authority and scope"). The checklist of the computational milestones is lean-cas-dsl#93.

**Version**: 2.0.0 | **Ratified**: 2026-11-25 | **Last Amended**: 2026-11-25

[K]: https://github.com/dzackgarza/lean-cas-dsl/blob/main/.specify/memory/constitution.md
[RC]: https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/blob/main/.specify/memory/constitution.md
