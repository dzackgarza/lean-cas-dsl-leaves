# Contributing to the category implementations

The [constitution](.specify/memory/constitution.md) governs. Each policy below has a stable
identifier, a class of contribution, a defective contribution and its replacement. A new lesson
gets the next free identifier in its category. Identifiers are never reused.

## Inputs and authorship (INP)

**INP001 — The assignment's input list binds (LV14).** Defective: a contract-only assignment
reads catalogue source files of lean-categories because a standing rule permits the catalogue in
general. Replacement: read only the inputs that the assignment names; a missing input is a
finding for its owner, and the work that needs it waits.

**INP002 — No acceptance material in leaf documents (LV2, LV14).** Defective: a findings file of
this repository lists acceptance-specific requirements, kernel source references and harness
observations. Replacement: requirements come from the released contract, the catalogue that it
publishes and the engine resources; the acceptance suite stays in lean-cas-dsl, unseen.

## Mathematics (MTH)

**MTH001 — No mathematical datum in leaf source (LV1).** Defective: the Gram matrix of $A_n$ is a
literal in three programs, the rank of $E_8$ is a literal, and two copies of one computation give
different answers on a zero divisor. Replacement: the request supplies the data through the
published constructors; a datum that the request does not carry is a finding against the
contract or the catalogue.

**MTH002 — Missing mathematics is a lean-categories task (LV1, LV14).** Defective: a leaf author
adds the declaration that its implementation needs, or defines it inside the leaf. Replacement:
a task before its consumer in the task list, with its lean-categories issue; a formalization
author does it.

## Engines (ENG)

**ENG001 — Glue over a mature engine (LV5, LV6).** Defective: the pullback of two finite set maps
is a Python filter over a Cartesian product, and the restriction of a bilinear form is a Python
loop over pairs of points. Replacement: the engine routine that the survey record names; where
the survey shows no engine, a hand-rolled algorithm that cites its mature reference.

**ENG002 — One engine installation (LV21).** Defective: a loader tries a modular passagemath
entrypoint, then `sage.all`, then searches the parent directories for `.venv/bin/python`.
Replacement: the one interpreter of the research container; an absent engine stops the backend
before its ready frame.

## Data (DAT)

**DAT001 — Consume the supplied data (LV4).** Defective: a property of a returned kernel subgroup
recomputes the canonical named kernel in place of the supplied inventory and inclusion.
Replacement: build the engine value from the supplied inclusion images and compute on it.

**DAT002 — No substitute for an unsupported request (LV4, LV11).** Defective: a scalar request at
a non-terminal generalized domain is answered as if the domain were a point. Replacement: the
reply `status:"unsupported"` or `status:"error"`, naming the input that is not supported.

**DAT003 — No leaf-invented encoding (LV14).** Defective: $p/q$ is answered as an
`operationExpression` of `mor.sets.divide`, and a Kähler differential as a point of
`mor.sets.kaehler_from_coordinate`, when the contract declares no such form. Replacement: a
finding against the contract; the request is unsupported until the contract declares the form.

## Category implementations (CAT)

**CAT001 — The category is the unit (LV3).** Defective: one port is registered for each request
form that a test needs, and the list of ports is called the category implementation.
Replacement: the generated interface of the category, implemented in full or with each part that
no engine supplies recorded as a survey gap.

## Tests (TST)

**TST001 — Real process, real peer (LV18).** Defective: the commit tier checks only that
`leaves.json` parses and that the programs compile. Replacement: tier 1 drives each backend
through `cas-peer` scenarios on the real engine and writes its log and timing records.

**TST002 — Engineering checks are not correctness evidence (LV2).** Defective: a report counts
successful replies of a leaf as progress towards acceptance. Replacement: the report names the
behaviour that the check exercised; the kernel's acceptance suite decides correctness.

## Documents (DOC)

**DOC001 — State the present rule.** Defective: a document explains how an earlier form came to
be replaced. Replacement: the document states the present rule and the future work; git history
keeps the earlier form.
