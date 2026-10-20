# Deliberately bad replacement leaves

Each subdirectory is a standalone replacement package whose `leaves.json` uses
only the published registration and port contracts. These are deliberately bad
implementations, independently chosen from the published `meth.cardinality`
operation and `obj.sets.fin` input form. They contain no tests, mathematical
oracle, proof, trust field, or acceptance inventory.

| Manifest | Behavior |
| --- | --- |
| `missing/leaves.json` | No registrations or backend programs. |
| `wrong/leaves.json` | Replies with the cardinal literal `aleph0` for every request. |
| `malformed/leaves.json` | Replies with `finite` applied to a string instead of a natural number. |
| `unavailable/leaves.json` | Its registered program exits with code 73 before a ready frame. |

Launch backend arguments relative to each manifest directory, with the published
contract's `python` directory on `PYTHONPATH`. No engine is needed. Select one
complete manifest as the replacement leaf package; these are not merged into
the normal `leaves.json`. A revision-qualified repository path identifies each
specimen without letting the specimen choose the mathematical question.

Only deliberately bad computational data or execution failure crosses the port.
The specimen and its local engineering checks establish no correctness or
acceptance result.
