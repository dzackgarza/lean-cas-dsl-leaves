"""Exact symbolic coordinate metadata for supported native scalar actions.

Every input coordinate is an independent polynomial generator.  A callback is
evaluated once on that symbolic input, using Sage's polynomial and quotient-ring
arithmetic; no point sampling, interpolation, or fitted polynomial is involved.
The caller retains the selected formal endpoints and all callable owners.  The
contexts here retain its supplied selections without identifying presentations.
"""

from dataclasses import dataclass, field

from sage.all import QQ, PolynomialRing

from wire import Unsupported


def _coordinates(values, count):
    """Read an ordered, complete coordinate tuple."""
    values = tuple(values)
    if len(values) != count:
        raise ValueError("the symbolic coordinate count differs from its model")
    return values


def _polynomial(ring, value):
    try:
        return ring(value)
    except (TypeError, ValueError, ArithmeticError, NotImplementedError) as error:
        raise Unsupported("a symbolic coordinate is not a polynomial in the selected inputs") from error


@dataclass(frozen=True)
class ScalarModel:
    native_ring: object
    kind: str
    _symbolic_rings: dict = field(default_factory=dict, init=False, repr=False, compare=False)

    def __post_init__(self):
        if self.kind not in {"rational", "integer", "dual_x", "dual_y"}:
            raise Unsupported("the selected scalar presentation has no polynomial coordinate model")

    @property
    def dimension(self):
        return 2 if self.kind in {"dual_x", "dual_y"} else 1

    @property
    def signature(self):
        return ("scalar", self.native_ring, self.kind)

    def symbolic_ring(self, ring):
        """Use ``ring`` for coordinate coefficients, retaining the presentation."""
        if self.dimension == 1:
            return ring
        if ring not in self._symbolic_rings:
            polynomials = PolynomialRing(ring, "z")
            generator = polynomials.gen()
            relation = generator ** 2 if self.kind == "dual_x" else (generator + 1) ** 2
            self._symbolic_rings[ring] = polynomials.quotient(relation, "zbar")
        return self._symbolic_rings[ring]

    def decode_symbolic(self, ring, coordinates):
        coordinates = tuple(_polynomial(ring, value)
                            for value in _coordinates(coordinates, self.dimension))
        if self.dimension == 1:
            return coordinates[0]
        symbolic = self.symbolic_ring(ring)
        return symbolic(coordinates[0]) + symbolic(coordinates[1]) * symbolic.gen()

    def encode_symbolic(self, ring, value):
        if self.dimension == 1:
            return (_polynomial(ring, value),)
        symbolic = self.symbolic_ring(ring)
        try:
            lifted = symbolic(value).lift()
        except (TypeError, ValueError, ArithmeticError, NotImplementedError) as error:
            raise Unsupported("the symbolic output is outside its selected quotient presentation") from error
        return tuple(_polynomial(ring, lifted[index]) for index in range(self.dimension))


@dataclass(frozen=True)
class ProductModel:
    left: object
    right: object

    @property
    def dimension(self):
        return self.left.dimension + self.right.dimension

    @property
    def signature(self):
        return ("product", self.left.signature, self.right.signature)

    def decode_symbolic(self, ring, coordinates):
        coordinates = _coordinates(coordinates, self.dimension)
        split = self.left.dimension
        return (self.left.decode_symbolic(ring, coordinates[:split]),
                self.right.decode_symbolic(ring, coordinates[split:]))

    def encode_symbolic(self, ring, value):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("a symbolic product output requires its two selected components")
        return (self.left.encode_symbolic(ring, value[0])
                + self.right.encode_symbolic(ring, value[1]))


@dataclass(frozen=True)
class PolynomialAction:
    source_model: object
    target_model: object
    ring: object
    polynomials: tuple
    context: object

    def __post_init__(self):
        if self.ring.base_ring() != QQ:
            raise Unsupported("polynomial action metadata requires exact rational coefficients")
        if self.ring.ngens() != self.source_model.dimension:
            raise ValueError("the polynomial generators do not match the source coordinates")
        polynomials = _coordinates(self.polynomials, self.target_model.dimension)
        object.__setattr__(self, "polynomials",
                           tuple(_polynomial(self.ring, value) for value in polynomials))

    def then(self, other):
        """Compose in categorical order: this action, followed by ``other``."""
        if not isinstance(other, PolynomialAction):
            raise Unsupported("the following action has no polynomial coordinate metadata")
        if self.target_model.signature != other.source_model.signature:
            raise Unsupported("the polynomial actions have different selected middle models")
        substitution = other.ring.hom(list(self.polynomials), self.ring)
        polynomials = tuple(substitution(value) for value in other.polynomials)
        return PolynomialAction(self.source_model, other.target_model, self.ring, polynomials,
                                {"first": self.context, "second": other.context})

    def equal(self, other):
        """Compare normalized polynomials at matching complete coordinate models."""
        if not isinstance(other, PolynomialAction):
            raise Unsupported("the other action has no polynomial coordinate metadata")
        if (self.source_model.signature != other.source_model.signature
                or self.target_model.signature != other.target_model.signature):
            raise Unsupported("the polynomial actions have different selected endpoint models")
        rebase = other.ring.hom(list(self.ring.gens()), self.ring)
        return all(bool(left == rebase(right))
                   for left, right in zip(self.polynomials, other.polynomials))


def build(source_model, target_model, compute, context):
    """Evaluate ``compute(symbolic_input, coefficient_ring)`` on all generators."""
    ring = PolynomialRing(QQ, source_model.dimension, "c")
    symbolic_input = source_model.decode_symbolic(ring, ring.gens())
    try:
        symbolic_output = compute(symbolic_input, ring)
    except (TypeError, ValueError, ArithmeticError, NotImplementedError) as error:
        raise Unsupported("the selected computation has no symbolic polynomial action") from error
    polynomials = target_model.encode_symbolic(ring, symbolic_output)
    return PolynomialAction(source_model, target_model, ring, polynomials, context)


def identity(source_model, target_model, context):
    if source_model.signature != target_model.signature:
        raise Unsupported("polynomial identity requires matching selected coordinate models")
    return build(source_model, target_model, lambda value, ring: value, context)


def mediator(left, right, context):
    """Pair two actions on the same selected source, retaining both contexts."""
    if not isinstance(left, PolynomialAction) or not isinstance(right, PolynomialAction):
        raise Unsupported("both mediator components need polynomial coordinate metadata")
    if left.source_model.signature != right.source_model.signature:
        raise Unsupported("the polynomial mediator has different selected source models")
    rebase = right.ring.hom(list(left.ring.gens()), left.ring)
    polynomials = left.polynomials + tuple(rebase(value) for value in right.polynomials)
    return PolynomialAction(left.source_model, ProductModel(left.target_model, right.target_model),
                            left.ring, polynomials,
                            {"selection": context, "left": left.context, "right": right.context})
