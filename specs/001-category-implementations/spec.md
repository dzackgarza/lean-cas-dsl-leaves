# Feature Specification: Category implementations — the shared foundation and the spec list

**Feature Branch**: `001-category-implementations` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the
[kernel constitution][KC] v5.0.0; the [contract constitution][RC] and the released contract
feature [`001-released-contract-v2`][CS].

**Input**: what every category implementation of this repository shares — the move to protocol 2
and the generated interface of the released contract `cas-computation/2`, the common engine
bridge and the container interpreter, the survey record format, the logs and timing records, the
public-only test through a protocol peer, the removal or justification of hand-rolled code — and
the list of category specs 002 to 034, one for each category that a computation needs, which
together move the 115 existing registrations of `leaves.json`.

This document is an input of a leaf author (LV14). It names categories and operations of the
catalogue that the contract publishes, engines, this repository's registrations and the IDs of
the tasks that consume the work. It holds no acceptance statement and no expected answer.

## The category specs

Each category whose rows a computation needs has its own Spec Kit feature, `specs/<NNN>-<slug>/`,
numbered from 002. The [feature order](tasks.md#feature-order) of the task list, not the number,
is the sequence: it follows the structural order and starts with Sets (constitution LV13). The
[plan](plan.md#category-specs) lists the 33 specs and the categories that have no spec. Each spec has versioned milestones:

| Version | Rows of the spec |
| --- | --- |
| V1 | the rows that every computation of the spike and every statement of the kernel V1 definition need |
| V2 | the rows that the remaining full-B0 statements of lean-cas-dsl #19 need |
| V3 | the rows that the classified Sage coverage of lean-cas-dsl #20, #21 and #23 adds by the same membership rule, when kernel tasks T140 to T147 produce the classified statements; no spec plans more for V3 |

A row joins the first version of a computed statement that needs it. It belongs to the latest
category, in the structural order, among its catalogue owners and the categories of its declared
parameters; a structural functor or classifier forget belongs to its source (research R16). The
kernel task that consumes a version reads "Implement <Category> Spec V<n>" (the category tasks of
the kernel task list; the plan's table names the ID of each version).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — A leaf author implements one category from the released contract alone (Priority: P1)

A public-only author has a checkout of this repository, the released contract (tag `v2.0.0`),
the catalogue that the contract publishes and the research container. The author loads the
generated interface of one category, surveys the engines for its operations, writes the
category implementation as glue over the chosen engine routines, registers its ports in
`leaves.json`, and runs the tier 1 tests of that category.

**Why this priority**: every computed answer of the programme comes from category
implementations (K:C22, K:C23). An author who needs kernel source, acceptance material or
another provider's private layout cannot work independently (LV14).

**Independent Test**: in a container with only this repository and the contract checkout
mounted, `just setup` and `just test-category sets` run the tier 1 tests of the sets
implementation against the contract's protocol peer, and every file that the run reads is in
this repository, the contract release or the research image.

**Acceptance Scenarios**:

1. **Given** the generated interface, **When** the author calls
   `cas_interfaces.load_interfaces(...).category("cat.sets")`, **Then** the object constructors,
   morphism constructors, operations and functor actions of `cat.sets` are listed, and the
   implementation registers a port for each part, or the survey record names the part as a gap.
2. **Given** a category implementation that needs an operation of another category, **When** it
   asks the kernel by a suspension and the peer resumes with the `noImplementation` slot, **Then**
   the backend receives a `NoImplementation` value and its next reply follows its own control
   logic (LV8).
3. **Given** a request whose input presentation the implementation does not support, **When**
   the backend replies, **Then** the reply is `status:"unsupported"` with the exact `op`, and no
   substitute value is sent (LV11).
4. **Given** a backend whose engine is absent, **When** it starts, **Then** it exits before its
   ready frame (LV21).

---

The researcher's stories are those of the category specs: each version of each spec states the
computations that it makes possible, and its acceptance scenarios state the reply at the
generated layout, the named routine, the retained selected data and the functor endpoints.

### User Story 2 — An assessor replaces this provider with an independent one (Priority: P2)

An assessor removes the registrations of one category implementation of this repository and
installs an independently written provider for the same operations and input forms. The
questions, the kernel and the other implementations stay unchanged, and the acceptance suite
still judges the answers.

**Why this priority**: independent replacement is the evidence that the contract, not this
repository's private layout, carries the interface (K:C12; LV15). The trials follow
functionality (K:C21).

**Independent Test**: a manifest without the sets ports of this repository and with a specimen
package in their place is admitted, and each specimen's failure reaches its distinct stratum
(`specimens/README.md`).

**Acceptance Scenarios**:

1. **Given** the specimen packages migrated to protocol 2, **When** the kernel launches each,
   **Then** `missing` gives no implementation, `wrong` a well-framed wrong answer, `malformed`
   the `malformed` stratum and `unavailable` the `unavailable` stratum.
2. **Given** a consumer category implementation of this repository, **When** a provider of a
   category that it consumes is replaced, **Then** the consumer needs no edit, because it reads
   only the generated result layout (LV9, LV15).

### Edge Cases

| Situation | Required behaviour | Source |
| --- | --- | --- |
| An operation of the generated interface has no engine routine | The leaf implements the known method and cites its reference; only mathematically new work is a gap of the survey record, with its searches, and needs a separately authorized research assignment | LV6, LV7 |
| A result needs a wire form that the contract does not declare | lean-cas-dsl-leaf-contracts T021 declares the form (contract issue #14; FR-033); the workstream of the row finishes that task first, in the contract role, and then registers the row | LV14; RC8 |
| A named object arrives as its descriptor | One lowering table of the category implementation maps it to the engine constructor | LV1 |
| A named object has defining data that no engine constructor builds (a defining polynomial, a Gram matrix) | The implementation reads the data from the unfolded definition that the request carries (K:C22); a request that carries only the name is `status:"unsupported"` and a finding against the contract | LV1; CONTRIBUTING MTH001 |
| An engine returns an unevaluated form | A branch to the second engine that the routine table names, as control logic | LV8, LV11 |
| The SDK reports a reserved constructor in a reply | The SDK raises before writing; the backend sends no frame | contract FR-010 |
| Two backends realize one operation at one input form | The manifest holds one; implementation ambiguity is the kernel's outcome | LV10; RC5 |
| A suspended child has no implementation | The backend receives `NoImplementation(op, input)` and continues | LV8; contract FR-010 |

## Requirements *(mandatory)*

### Functional Requirements — the category specs

- **FR-038 — One spec for each needed category.** Each category with a row in V1 or V2 MUST have
  its Spec Kit feature, at its step of the feature order: its spec states the category, the user
  stories of each version and one requirement for each row with its catalogue ID and its version;
  its plan names, for each row, the engine and routine, the module of this repository, the
  dependent inputs and the inputs before it; its task list has, for each version, the survey
  record, the implementation tasks of its rows, the move of its registrations and the task
  "Spec V<n> complete", which names the kernel task that consumes the version. The
  [plan](plan.md#category-specs) lists the specs; a category with no row in V1 or V2 has no spec
  and is listed there with its reason.
- **FR-039 — Placement of the existing registrations.** Each of the 115 registrations of
  `leaves.json` at `8b181d7` MUST belong to exactly one category spec and one version of it, by
  the rule of research R15, and MUST move there (LV12). The move task of a version trashes each
  v1 program whose last registration it moves (research R4).

### Functional Requirements — the contract, the moves and the engineering defaults

- **FR-026 — Protocol 2 and the generated interface.** Every backend MUST speak
  `cas-computation/2` through the released SDK (`cas_session`, `cas_interfaces`) and build its
  requests and replies from the generated interface: negotiation (contract T004), manifest with
  required `preferredRoutes` (T005), exact references (T006), replies and exports (T007),
  failure strata (T008), deferred programs (T009), suspension with the `noImplementation` slot
  (T010), decision replies (T011), routine observations and SDK logs (T012), method and map
  requests (T013, T015), the category view (T014, T015). The release `v2.0.0` (contract T019)
  is the input of the V1 versions of the category specs; the release `v2.0.1` (contract T020) is
  the delivery dependency and the input of their V2 versions. No v1
  frame and no hand-written wire codec remain (`backends/wire.py` is deleted).
- **FR-027 — Hand-rolled algorithms and lookups.** Each registration whose answer is
  hand-rolled, partly hand-rolled or a lookup in its v1 source MUST be replaced by an engine
  routine, or justified under LV6. The plan of each category spec gives the decision of each of
  its registrations in its table "Registrations that move", and its section "Hand-rolled code"
  names each computation of known mathematics that no surveyed engine provides, with its cited
  reference.
- **FR-028 — Survey record.** Before the implementation tasks of each version of each category
  spec, the survey record of that version MUST exist in the spec's `research.md`, in the row
  format of [research.md](research.md), "Survey record", with the content that LV7 prescribes;
  the commit of the implementation cites it.
- **FR-029 — Logs.** Each backend MUST log to standard error each request (id, operation,
  input form), each engine routine with its elapsed time, each request to the kernel and each
  reply status. Each test run MUST write `tests/logs/<UTC>-<revision>.log` (LV22).
- **FR-030 — Timing records.** Each test and each computation MUST have a record in
  `tests/timing/records.jsonl` with run, revision, environment, input, engine start-up, setup,
  construction and nested work (LV23).
- **FR-031 — One engine installation.** Every backend MUST run under `/sage/.venv/bin/python3`
  of the research container. `backends/engine_python.py`, the variables `CAS_SAGE_PYTHON` and
  `CAS_GAP_PYTHON`, the modular passagemath entrypoints and the workspace interpreter search
  are deleted (LV21).
- **FR-032 — Declared dependencies.** The package MUST declare the contract SDK at its release
  tag and the Julia packages that it uses, with explicit setup outside the ordinary loop;
  `lakefile.toml`, which no kernel branch requires, is deleted (LV16).
- **FR-033 — Contract findings.** The wire forms that `DEFECTS.md` lists as leaf-chosen (a
  non-integral rational or an irrational real in an answer, $\mathbb{N}\cup\{-\infty\}$, a
  Kähler differential, a matrix, an infinite subset given by `span`, the request of a binder,
  the apex of a product with an infinite factor, a closed point in a morphism position) and the
  missing inputs that it lists (the intermediate group of an unlabelled composite, a
  representation of `op.rings.*` in `apply`) are the ten items of lean-cas-dsl-leaf-contracts
  issue #14, which contract task T021 declares before the release `v2.0.0`. A registration that
  needs such a form is not answered with a leaf-chosen encoding; it is registered with the form of
  T021 (LV14).
- **FR-034 — No mathematics in the source.** No backend answers by lookup, writes a defining
  datum that an engine constructor builds, or writes one datum twice (LV1). Each category spec
  names the v1 data that its moves delete, with their source lines at `8b181d7`.
- **FR-035 — Specimens on protocol 2.** The four packages under `specimens/` MUST speak
  protocol 2 and keep their deliberately bad behaviour (LV15).
- **FR-036 — Findings in issues.** The findings of `DEFECTS.md` MUST be recorded in an issue of
  this repository, and `DEFECTS.md` trashed after a semantic comparison (constitution,
  Governance).

### Key Entities

- **Category implementation**: the code of one category against its generated interface; the
  unit of responsibility (LV3).
- **Backend program**: one process that speaks protocol 2 and registers the ports of one category
  implementation (research R3).
- **Category spec**: the Spec Kit feature of one category, with its versions V1, V2 and V3
  (FR-038).
- **Registration**: one `(operation, input, backend)` row of `leaves.json`; a port.
- **Survey record**: the per-category record of engines, decisions and gaps (LV7).
- **Lowering table**: the map from named-object descriptors to engine constructors of one
  category implementation (LV1).
- **Routine table**: the engine routine of each port, published in the plan and in replies.
- **Scenario**: a file of frames that `cas-peer` sends and expects in a tier 1 test.
- **Timing record**, **run log**: the durable outputs of a test run.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For each version of each category spec, its kernel task "Implement <Category> Spec
  V<n>" observes its attainment through the public session of lean-cas-dsl with this repository's
  manifest, with no kernel-side evaluation in any part.
- **SC-002**: All 115 registrations of `leaves.json` at `8b181d7` are in a category
  implementation on protocol 2, and no registration of a v1 backend remains.
- **SC-003**: `git grep -n "engine_python\|CAS_SAGE_PYTHON\|CAS_GAP_PYTHON\|all__sagemath"`
  over `backends/` and `leaves.json` returns nothing.
- **SC-004**: Tier 1 of one category implementation runs in under five minutes in the research
  container after `just setup`, and writes one log and one timing record per test.
- **SC-005**: The registrations classed hand-rolled, partial or lookup in the category plans are
  zero, or each has an LV6 justification in its plan.
- **SC-006**: Each port has a row in the routine table, and each reply of a tier 1 test carries
  a routine observation that names that routine.
- **SC-007**: The tier 1 tests of User Story 1 pass in a container where no lean-cas-dsl
  checkout is mounted.

## Assumptions

- Kernel readiness F and contract `v2.0.0` precede the V1 versions of the category specs (kernel
  specification, clarification of 2026-11-25; contract FR-022). Before F, only FR-033 and FR-036
  run, because they need no contract release.
- The categories, rows, versions and structural order are those of the roadmap record of
  lean-cas-dsl at `0e6ccbd` (research R16); the placement of the registrations follows research
  R15.
- Engine versions are those of the research container on 2026-11-25 (kernel research record
  `engine-survey.md`); the survey record of each version records the versions that it uses.

[KC]: https://github.com/dzackgarza/lean-cas-dsl/blob/main/.specify/memory/constitution.md
[RC]: https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/blob/main/.specify/memory/constitution.md
[CS]: https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/tree/main/specs/001-released-contract-v2
