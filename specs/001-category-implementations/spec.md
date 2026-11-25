# Feature Specification: Category implementations for the computational milestones

**Feature Branch**: `001-category-implementations` (work is committed on `main`)
**Created**: 2026-11-25
**Status**: Planned
**Governing text**: [constitution](../../.specify/memory/constitution.md) (LV1–LV25); the
[kernel constitution][KC] v4.0.0; the [contract constitution][RC] and the released contract
feature [`001-released-contract-v2`][CS].

**Input**: the category implementations that the computational milestones of lean-cas-dsl
(kernel tasks T200 to T224) need from this repository, written against the released contract
`cas-computation/2`, with the move of the 115 existing registrations of `leaves.json` into them.

This document is an input of a leaf author (LV14). It names categories and operations of the
catalogue that the contract publishes, engines, this repository's registrations and the IDs of
the tasks that consume the work. It holds no acceptance statement and no expected answer.

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

### User Story 2 — A researcher computes a statement of a milestone and gets the engine's result (Priority: P1)

A researcher writes a statement in lean-cas-dsl whose selected route stays within the
categories implemented through one milestone. The kernel resolves each computation to a
registration of this repository. The backend computes it with the engine routine that the
survey chose and returns the engine's result at the generated result layout, with every
selected datum that the request carried.

**Why this priority**: this is the product. A milestone is vertical: its attainment holds as a
computed result through the public interface of each category on its route (LV13; kernel
FR-042).

**Independent Test**: for each milestone, the kernel task that consumes it (T200 to T224 of
lean-cas-dsl) runs its attainment statements through `CasRuntime.KernelSession` with this
repository's manifest. The kernel's acceptance suite judges the result; this repository does
not hold the statements (LV2).

**Acceptance Scenarios**:

1. **Given** the implementations through a milestone, **When** the kernel sends a request at a
   registered port, **Then** the backend calls the routine that the routine table names, reports
   it in its routine observations, and replies at the generated result layout.
2. **Given** a request that carries selected endpoints, cones, comparisons or earlier outputs,
   **When** the backend replies, **Then** the reply contains those data unchanged where the
   result layout retains them, and no recomputed canonical substitute (LV4).
3. **Given** a functor morphism request with two image endpoints, **When** the backend replies,
   **Then** the arrow has exactly those endpoints (contract FR-018).

---

### User Story 3 — An assessor replaces this provider with an independent one (Priority: P2)

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
| An operation of the generated interface has no engine routine | The survey record names the gap and the searches; a hand-rolled algorithm exists only with a cited mature reference | LV6, LV7 |
| A result needs a wire form that the contract does not declare | No registration answers it; the finding goes to the contract owner (FR-033) | LV14; RC8 |
| A named object arrives as its descriptor | One lowering table of the category implementation maps it to the engine constructor | LV1 |
| An engine returns an unevaluated form | A branch to the second engine that the routine table names, as control logic | LV8, LV11 |
| A request asks for an infinite cardinal other than $\aleph_0$ | `status:"unsupported"`; no engine computes it (survey record, "Cardinals") | LV11 |
| The SDK reports a reserved constructor in a reply | The SDK raises before writing; the backend sends no frame | contract FR-010 |
| Two backends realize one operation at one input form | The manifest holds one; implementation ambiguity is the kernel's outcome | LV10; RC5 |
| A suspended child has no implementation | The backend receives `NoImplementation(op, input)` and continues | LV8; contract FR-010 |

## Requirements *(mandatory)*

### Functional Requirements — the computational milestones

Each requirement FR-001 to FR-025 is one milestone of the kernel plan ("Computational
milestones", lean-cas-dsl `4be2a02`). It names the categories, the engine and its routines from
the engine survey, the registrations of `leaves.json` that move into it, the computations that
the kernel performs today and that move into it, the upstream tasks before it, and the kernel
task that consumes it. Each milestone MUST implement the complete generated interface of its
categories (LV3), less the registrations that a subsequent requirement moves; the attainment
statements of the consuming kernel task are the workload statements that it makes computable,
assessed there (LV2, LV13). The plan gives the files, entry points and tests of each.

- **FR-001 — Sets** (kernel T200). Categories `cat.sets`, `cat.core_sets`, `cat.cardinals`,
  `cat.cardinalities`. Engine: Sage `sage.sets` parents, `Hom` in `Sets()`, `FiniteSetMaps`,
  `cartesian_product` with `cartesian_projection`, `DisjointUnionEnumeratedSets`, `Subsets`,
  `cardinality()`, `is_finite()`, membership in `EnumeratedSets` for $\aleph_0$; Catlab.jl
  `pullback` of `FinFunction`s through juliacall. Moves in 31 registrations: `colim.sets.coproduct`,
  `lim.sets.pullback`, `lim.sets.product` (its projections move in here), `meth.cardinality` ×13,
  `mor.sets.equality`, `mor.sets.fin_rev`, `prop.is_finite` ×13. Moves in from the kernel:
  equality of elements, application and composition of maps, the projections of a product, the
  graph of a map. Upstream: kernel T119, T120, T121, T123, T129, T134. Kernel readiness F and
  contract release `v2.0.0` precede it.
- **FR-002 — Finite sets** (kernel T201). Category `cat.finite_sets`. Engine: Sage
  `FiniteEnumeratedSet`, `Sets().Finite()`, `FiniteSetMaps`, `list()`. Moves in 2:
  `meth.cardinality`, `prop.is_finite` at `obj.finite_sets.fin`. From the kernel: the list of the
  elements of a finite carrier. Upstream: T119, T135. After FR-001.
- **FR-003 — Orders** (kernel T202). Categories `cat.preorders`, `cat.partial_orders`,
  `cat.linear_orders`. Engine: Sage `Poset`, `is_lequal`, `is_less_than`, `is_chain`; GAP
  Digraphs `IsPreorderDigraph` through `libgap` for preorders. An order-preserving map is a set
  map with Sage's comparison. Moves in 0. From the kernel: $<$ and $\le$ on $\mathbb{N}$.
  Upstream: T133. After FR-001.
- **FR-004 — Rings** (kernel T203). Categories `cat.magmas`, `cat.semigroups`, `cat.monoids`,
  `cat.groups`, `cat.additive_magmas`, `cat.additive_semigroups`, `cat.additive_monoids`,
  `cat.additive_commutative_monoids`, `cat.semirings`, `cat.additive_groups`, `cat.rings`.
  Engine: Sage `ZZ`, `QQ`, `Zmod`, ring arithmetic, `gcd`, `is_prime`, `factor`; GAP 4.16.1
  through `libgap`: `SymmetricGroup`, `CyclicGroup`, `Units`, `Size`, `IsAbelian`, `IsFinite`;
  SymPy `integrate` and `limit`, with the Sage symbolic ring where SymPy returns an unevaluated
  form. Moves in 25: `bind.sets.integral`, `bind.sets.limit`, `bind.sets.limit_at_infinity`,
  `meth.cardinality` ×5, `mor.sets.complex_abs`, `mor.sets.complex_bar`, `mor.sets.complex_im`,
  `mor.sets.complex_re`, `mor.sets.nat_prime_factors`, `mor.sets.real_sqrt`, `prop.is_abelian` ×3,
  `prop.is_commutative` ×3, `prop.is_finite` ×5. From the kernel: arithmetic of $\mathbb{N}$,
  $\mathbb{Z}$ and $\mathbb{Z}/n$; gcd and primality; multiplication, unit and inverse of an
  instance. Upstream: T122, T131, T132. After FR-001.
- **FR-005 — Group automorphisms** (kernel T204). Category `cat.core_groups`. Engine: GAP
  `AutomorphismGroup`, `ConjugatorAutomorphism`, `InverseGeneralMapping`. Moves in 0. Upstream:
  T134. After FR-004.
- **FR-006 — Commutative rings** (kernel T205). Categories `cat.commutative_monoids`,
  `cat.commutative_rings`. Engine: Sage `PolynomialRing`, `quo`, ring `hom`, `degree`,
  `derivative`, `factor`, `roots`, `companion_matrix`, `change_ring`, `det`, `trace`, `charpoly`;
  Singular 4.4.1 inside Sage for several variables. Moves in 18: `cmp.f9.translation` ×2,
  `meth.cardinality` ×2, `mor.sets.companion_matrix`, `mor.sets.f9_x_constants` ×2,
  `mor.sets.f9_y_constants` ×2, `mor.sets.mv_total_degree`, `mor.sets.polynomial_degree`,
  `mor.sets.polynomial_derivative`, `mor.sets.polynomial_differential`,
  `mor.sets.polynomial_factors`, `mor.sets.polynomial_map`, `mor.sets.polynomial_roots`,
  `prop.is_finite` ×2. After FR-004.
- **FR-007 — Topological monoids** (kernel T206). Category
  `cat.hausdorff_topological_commutative_monoids`. Engine: Sage `LazyPowerSeriesRing`,
  `coefficient`. Moves in 0. Upstream: T128. After FR-006.
- **FR-008 — Modules** (kernel T207). Categories `cat.modules_r`, `cat.modules_total`. Engine:
  Sage `FreeModule`, `VectorSpace`, scalar action, `cardinality()`. Moves in 2:
  `meth.cardinality` at `obj.modules.regular` and `obj.modules.vectors` (`lim.sets.product` moves
  in FR-001). From the kernel: the scalar action of an instance. After FR-006.
- **FR-009 — Bilinear forms** (kernel T208). Category `cat.bil_wform`. Engine: Sage
  `IntegralLattice`, `dual_lattice`, `discriminant_group`, `invariants`; PARI 2.17.4 `matsnf`
  through `cypari2`. Moves in 10: `colim.bil_w_form.cokernel`, `meth.cardinality` ×3,
  `prop.is_abelian` ×3, `prop.is_commutative` ×3. After FR-008.
- **FR-010 — Fields** (kernel T209). Category `cat.fields`. Engine: Sage `QQ`, `GF`,
  `VectorSpace`, `span`, `right_kernel`, `dimension`. Moves in 1: `mor.sets.span`. After FR-006.
- **FR-011 — Module rank** (kernel T210). Category `cat.core_modules_r`. Engine: Sage `rank()`.
  Moves in 5: `meth.rank` ×5. After FR-008.
- **FR-012 — Module kernels** (kernel T211). Categories `cat.subobjects_sets`,
  `cat.subobjects_modules_r`, `cat.arrows_modules_r`, `cat.core_subobjects_modules_r`. Engine: Sage
  module `hom`, `kernel()`, `submodule`, `dimension`, `__contains__`. Moves in 0. From the kernel:
  membership in a subset. Upstream: T134, T138. After FR-008.
- **FR-013 — Formed modules** (kernel T212). Categories `cat.bilin_module`,
  `cat.arrows_bilin_module`. Engine: Sage `FreeModule(QQ, n, inner_product_matrix=G)`,
  `submodule`, `gram_matrix()`, inclusion `hom`. Moves in 4: `lift.bilin_module.restrict#obj`,
  `#hom`, `#forward`, `#backward`. Upstream: T130, T134. After FR-009.
- **FR-014 — Full B0 in the V1 categories** (kernel T213). Extends FR-001 to FR-013. Engine:
  SymPy 1.14.0 `limit`, `series`, `integrate`, with the Sage symbolic ring (Maxima 5.49.0) where
  SymPy returns an unevaluated form. Moves in 0. Upstream: T124, T125, T128, T136, T137. After
  kernel T105. The cardinal $\aleph_0 \cdot \aleph_0$ waits on kernel owner question Q1.
- **FR-015 — Group kernels** (kernel T214). Categories `cat.arrows_groups`,
  `cat.subobjects_groups`. Engine: GAP `GroupHomomorphismByImages`, `Kernel`,
  `AlternatingGroup`, `SignPerm`, `Size`, `IsAbelian`. Moves in 13: `fun.arrows_groups.kernel`,
  `meth.cardinality` ×3, `meth.group_arrow_kernel`, `prop.is_abelian` ×2, `prop.is_commutative`
  ×3, `prop.is_finite` ×3. Upstream: T134. After kernel T105 and FR-004.
- **FR-016 — Boolean algebras** (kernel T215). Categories `cat.join_semilattices`,
  `cat.meet_semilattices`, `cat.order_lattices`, `cat.bounded_order_lattices`,
  `cat.boolean_algebras`. Engine: Sage `Subsets`, `posets.BooleanLattice`, `LatticePoset` `meet`,
  `join`, `complements`. Moves in 0. Upstream: T133, T136. After FR-003, FR-004.
- **FR-017 — Integral lattices** (kernel T216). Category `cat.integral_lattice`. Engine: Sage
  `IntegralLattice`, `rank`, `cardinality`. Moves in 4: `meth.cardinality`, `meth.rank`,
  `prop.is_abelian`, `prop.is_commutative` at `obj.integral_lattice.e8`. After FR-011, FR-013.
- **FR-018 — Set constructions** (kernel T217). Categories `cat.arrows_sets`, `cat.slice_sets`,
  `cat.coslice_sets`, `cat.endofunctors_sets`, `cat.walking_pair`, `cat.sets.pair_diagrams`,
  `cat.pointed_sets`, `cat.core_pointed_sets`, `cat.countable_sets`, `cat.enumerated_sets`,
  `cat.core_subobjects_sets`, `cat.subsets.point_predicates`, `cat.subsets.subset_predicates`,
  `cat.crystals`. Engine: Sage sets with a base point, `EnumeratedSets`, `crystals`; Catlab.jl
  slices, coslices and diagrams. Moves in 0. Upstream: T134; the crystal structural functor.
  After FR-001, FR-012.
- **FR-019 — Well orders** (kernel T218). Categories `cat.well_ordered_sets`,
  `cat.core_well_ordered_sets`, `cat.enumerated_monotone_sets`, `cat.ordinals`. Engine: SymPy
  `sympy.sets.ordinals` (`Ordinal`, `OmegaPower`); Sage posets for finite well orders. Moves in
  0. Upstream: T133. After FR-003, FR-018.
- **FR-020 — Algebraic structures** (kernel T219). Categories `cat.magmaswithtwooperations`,
  `cat.division_rings`. Engine: Sage `QuaternionAlgebra`; GAP `MagmaByMultiplicationTable`. Moves
  in 0. Upstream: T131. After FR-004.
- **FR-021 — Algebras** (kernel T220). Category `cat.algebras`. Engine: Sage `Algebras(R)`,
  `FreeAlgebra`, `GroupAlgebra`. Moves in 0. After FR-006.
- **FR-022 — Schemes** (kernel T221). Categories `cat.schemes`, `cat.schemes_over`,
  `cat.schemes_over_ring`. Engine: Sage `sage.schemes` (`Spec`, `AffineSpace`,
  `ProjectiveSpace`). Moves in 0. Upstream: T136; the scheme structural functor. After FR-001,
  FR-006.
- **FR-023 — Module constructions** (kernel T222). Categories `cat.module_points`,
  `cat.based_module`, `cat.based_module_indexed`, `cat.coord`, `cat.coord_indexed`,
  `cat.finite_projective_lattice`, `cat.finitelygeneratedmodules`, `cat.finiterankmodules`,
  `cat.free_cover`, `cat.free_cover_indexed`, `cat.freemodules`, `cat.quotients_modules_r`,
  `cat.torsion_free_modules`, `cat.ideals_r`. Engine: Sage `fg_pid` modules and quotient modules;
  Macaulay2 1.24.11 through `sage.interfaces.macaulay2` for modules over polynomial rings. Moves
  in 0. Upstream: T118; the ideal structural functor. After FR-006, FR-008, FR-012.
- **FR-024 — Forms over rings** (kernel T223). Categories `cat.modules_over_rings_ext`,
  `cat.bilin_forms_over_rings`, `cat.quad_forms_over_rings`, `cat.integral_forms`,
  `cat.lattices_over_rings`, `cat.finite_projective_lattices_over_rings`,
  `cat.finite_free_lattices_over_rings`, `cat.unimodular_lattices_over_rings`,
  `cat.integral_lattices`, `cat.even_integral_lattices`, `cat.cusps`. Engine: Sage
  `QuadraticForm`; Hecke 0.39.22 through Oscar 1.8.2 for forms over number fields. Moves in 0.
  Upstream: the refinement, form, module and cusp structural functors. After FR-006, FR-008.
- **FR-025 — Lattices and quadratic modules** (kernel T224). Categories `cat.quad_module`,
  `cat.quad_wform`, `cat.alternating_forms`, `cat.lattice`, `cat.subobjects_bilin_module`,
  `cat.coord_lattice`, `cat.fraction_field_perfect_finite_projective_lattice`,
  `cat.definite_lattice`, `cat.indefinite_lattice`, `cat.even_lattice`, `cat.finite_free_lattice`,
  `cat.unimodular_lattice`. Engine: Sage `IntegralLattice`, `TorsionQuadraticModule`; Hecke
  through Oscar for genus and isometry; PARI `qfauto` for definite lattices. Moves in 0. Upstream:
  the lattice structural functors. After FR-013, FR-017, FR-023.

### Functional Requirements — the contract, the moves and the engineering defaults

- **FR-026 — Protocol 2 and the generated interface.** Every backend MUST speak
  `cas-computation/2` through the released SDK (`cas_session`, `cas_interfaces`) and build its
  requests and replies from the generated interface: negotiation (contract T004), manifest with
  required `preferredRoutes` (T005), exact references (T006), replies and exports (T007),
  failure strata (T008), deferred programs (T009), suspension with the `noImplementation` slot
  (T010), decision replies (T011), routine observations and SDK logs (T012), method and map
  requests (T013, T015), the category view (T014, T015). The release `v2.0.0` (contract T019)
  is the input of FR-001; the release `v2.0.1` (contract T020) is the delivery dependency. No v1
  frame and no hand-written wire codec remain (`backends/wire.py` is deleted).
- **FR-027 — Hand-rolled algorithms and lookups.** Each registration whose answer is
  hand-rolled, partly hand-rolled or a lookup in its v1 source MUST be replaced by an engine
  routine, or justified under LV6: `lim.sets.pullback` (Catlab.jl `pullback`),
  `lift.bilin_module.restrict#obj` (Sage `submodule` and `gram_matrix`), `lim.sets.product`
  (Sage `cartesian_product` with `cartesian_projection`), `meth.cardinality` at `cat.sets` (Sage
  `cardinality()` with the `EnumeratedSets` rule), `colim.bil_w_form.cokernel` and
  `meth.cardinality` at the discriminant (Sage `discriminant_group`), `meth.rank` at the root
  lattices and `obj.integral_lattice.e8` (Sage `rank()`), `lift.bilin_module.restrict#hom`,
  `#forward`, `#backward` (Sage inclusion `hom` and its section), `mor.sets.span` (Sage `span`).
- **FR-028 — Survey record.** Before each of FR-001 to FR-025, the survey record of its
  categories MUST exist in [research.md](research.md), with the content that LV7 prescribes, and
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
  representation of `op.rings.*` in `apply`) MUST go to lean-cas-dsl-leaf-contracts as a
  finding. A registration that needs such a form is not answered with a leaf-chosen encoding;
  it waits for the contract form (LV14).
- **FR-034 — No mathematics in the source.** No backend answers by lookup, writes a defining
  datum that an engine constructor builds, or writes one datum twice (LV1). This removes the
  three Gram matrices of $A_n$, the literal ranks of $A_n$ and $E_8$, the two tables from named
  sets to engine parents and the two countability tables.
- **FR-035 — Specimens on protocol 2.** The four packages under `specimens/` MUST speak
  protocol 2 and keep their deliberately bad behaviour (LV15).
- **FR-036 — Findings in issues.** The findings of `DEFECTS.md` MUST be recorded in an issue of
  this repository, and `DEFECTS.md` trashed after a semantic comparison (constitution,
  Governance).

### Key Entities

- **Category implementation**: the code of one category against its generated interface; the
  unit of responsibility (LV3).
- **Backend program**: one process that speaks protocol 2 and registers ports of one milestone's
  category implementations.
- **Registration**: one `(operation, input, backend)` row of `leaves.json`; a port.
- **Survey record**: the per-category record of engines, decisions and gaps (LV7).
- **Lowering table**: the map from named-object descriptors to engine constructors of one
  category implementation (LV1).
- **Routine table**: the engine routine of each port, published in the plan and in replies.
- **Scenario**: a file of frames that `cas-peer` sends and expects in a tier 1 test.
- **Timing record**, **run log**: the durable outputs of a test run.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For each of FR-001 to FR-025, the consuming kernel task observes its attainment
  through `CasRuntime.KernelSession` with this repository's manifest, with no kernel-side
  evaluation in any part.
- **SC-002**: All 115 registrations of `leaves.json` at `8b181d7` are in a category
  implementation on protocol 2, and no registration of a v1 backend remains.
- **SC-003**: `git grep -n "engine_python\|CAS_SAGE_PYTHON\|CAS_GAP_PYTHON\|all__sagemath"`
  over `backends/` and `leaves.json` returns nothing.
- **SC-004**: Tier 1 of one category implementation runs in under five minutes in the research
  container after `just setup`, and writes one log and one timing record per test.
- **SC-005**: The registrations classed hand-rolled, partial or lookup in FR-027 are zero, or
  each has an LV6 justification in the plan.
- **SC-006**: Each port has a row in the routine table, and each reply of a tier 1 test carries
  a routine observation that names that routine.
- **SC-007**: The tier 1 tests of User Story 1 pass in a container where no lean-cas-dsl
  checkout is mounted.

## Assumptions

- Kernel readiness F and contract `v2.0.0` precede FR-001 (kernel specification, clarification
  of 2026-11-25; contract FR-022). Before F, only FR-033 and FR-036 run, because they need no
  contract release.
- The milestone membership, order and moved registrations are those of the kernel plan at
  `4be2a02`, except `lim.sets.product`, which moves with FR-001 because the projections of a
  product move into FR-001.
- Engine versions are those of the research container on 2026-11-25 (kernel research record
  `engine-survey.md`); the survey record of each milestone records the versions it uses.

[KC]: https://github.com/dzackgarza/lean-cas-dsl/blob/main/.specify/memory/constitution.md
[RC]: https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/blob/main/.specify/memory/constitution.md
[CS]: https://github.com/dzackgarza/lean-cas-dsl-leaf-contracts/tree/main/specs/001-released-contract-v2
