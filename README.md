# Computational leaves of lean-cas-dsl

[`lean-cas-dsl/specs/architecture.md`](https://github.com/dzackgarza/lean-cas-dsl/blob/main/specs/architecture.md)
owns the separation of concerns. A leaf is a registration: a catalogue operation of
`lean-categories`, an input form, and a backend program that computes the operation's result form.
It contributes no mathematics and ships no Lean. Nothing it says is believed; only its answers are
checked, by `lean-cas-dsl`'s acceptance suite, which this package never sees.

* **`leaves.json`** is the manifest the kernel reads (`CasContract/Registration.lean` of
  `lean-cas-dsl-leaf-contracts`): the backend programs, and for each registration exactly its
  `operation`, `input` form and `backend`. Which registrations are admitted is the kernel's
  decision, against the catalogue.
* **`backends/`** holds the programs. Each speaks the contract's port protocol (`cas_port`, put on
  its `PYTHONPATH` by the kernel) and is glue over an existing engine: it decodes the kernel's
  encoding of the input, calls the engine's routine, and encodes the engine's answer in the result
  form. Each names the engine and routine it calls.
  * `sage_backend.py`: Sage (passagemath), under `CAS_SAGE_PYTHON`;
  * `gap_backend.py`: GAP through Sage's libgap (passagemath-gap), under `CAS_GAP_PYTHON`.

  Both default to `.venv/bin/python` of the running workspace (`backends/engine_python.py`).
* **`lakefile.toml`** only makes this directory a Lake package; it has no targets. `lean-cas-dsl`
  requires no leaf package: it reads a manifest at run time (`CAS_LEAVES`).

* **Blind to the tests.** The permanent acceptance suite lives in `lean-cas-dsl`; nothing here
  depends on it, runs it or can reach it. A leaf is never written or changed to make a test pass:
  `lean-cas-dsl`'s harness measures the installed leaves and reports gaps. A leaf's own tests are
  evidence of nothing.
* **Litmus role.** These leaves also probe the kernel: change one when that exposes a deficiency of
  the contract, the kernel or `lean-categories`, and name the deficiency in the commit.

Missing mathematics or missing forms go upstream to `lean-categories`; a leaf never absorbs them.
