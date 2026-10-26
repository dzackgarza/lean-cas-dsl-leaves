# Complete scalar carrier endpoints

An independent public-contract audit found that `check_element_target` recognized
the exact selected scalar structure and its named set representation, but rejected
a `typedMap` target containing an already supported registered carrier-action
chain rooted in that same exact selected structure. This is a computational
reader gap: the public input grammar retains the actual selected endpoints.

The repair in `endpoints.py` checks the supplied chain with the existing
`carrier_action` reader, including its full parameter framing, and requires the
unchanged selected structure at the chain's root. It uses neither equality of
Sage parents nor reconstruction of a canonical set descriptor to accept that
case. A `morphismEndpoint` is read from its actual retained field. No request
endpoint, expression, operand, output field, action selection or registration is
rewritten. Unknown actions and different selected structures stay outside this
newly handled case.

The public sources are `api/wire-examples.md` sections "Complete expression
inputs and returned-data reuse" and "Scalars and registered point expressions",
the existing registered-functor and classifier-forget framing, and the supplied
pure generated declarations. In particular the inspected declarations include
`ringsMultiplicative`, `ringsAdditive`, `additiveGroupsMonoid`,
`additiveMonoidsUnderlying`, `monoidsSemigroup`, and the classifier metadata for
`clf.magmas.associative` and `clf.sets.binary_operation`. Their complete source
and target signatures fix the selected interfaces independently of this reader.
The export provenance is recorded in the separate primitive-action specimen's
README; the development producer is not labelled a final integrated export.

`carrier_point_protocol_checks.py` is a newly authored, local reader check. It
exercises both existing additive and multiplicative carrier chains, closed and
generalized point data, unchanged inline and owned operands, retained domains and
endpoints, foreign-session rejection, and refusal to identify distinct selections
sharing the same native parent. These are framing and data-retention checks. No
mathematical scalar answer or law is asserted, and no kernel, acceptance suite,
fixed question or runtime acceptance outcome was inspected or run.

Run it under an installed Sage/PassageMath interpreter with the public contract's
`python` directory on `PYTHONPATH`. This repair is separately committed from the
two new primitive registrations and changes no existing manifest.
