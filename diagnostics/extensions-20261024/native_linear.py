"""Exact native matrix actions on complete selected rational modules.

Only an actual retained Sage matrix creates this representation. The module does
not fit matrices to arbitrary callables or test arbitrary functions on a basis.
"""

from dataclasses import dataclass

from sage.all import QQ, identity_matrix, matrix, vector

from wire import Unsupported


def degree(module):
    if module.native is QQ:
        return 1
    if module.native.base_ring() is not QQ:
        raise Unsupported("this native linear representation requires a rational carrier")
    return int(module.native.degree())


def basis_matrix(module):
    return identity_matrix(QQ, 1) if module.native is QQ else module.native.basis_matrix()


@dataclass(frozen=True)
class LinearAction:
    matrix: object
    source: object
    target: object
    context: object

    def __post_init__(self):
        if self.matrix.base_ring() is not QQ:
            raise Unsupported("only exact rational native matrices are implemented here")
        if self.matrix.ncols() != degree(self.source) or self.matrix.nrows() != degree(self.target):
            raise ValueError("the native matrix dimensions differ from its actual selected modules")

    def __call__(self, point):
        x = self.source.read(point)
        if self.source.native is QQ:
            x = vector(QQ, [x])
        y = self.matrix * x
        if self.target.native is QQ:
            return self.target.write(y[0])
        return self.target.write(self.target.native(y))

    def then(self, other):
        if self.target.native != other.source.native:
            raise Unsupported("the actual native intermediate modules differ")
        return LinearAction(other.matrix * self.matrix, self.source, other.target,
                            {"composition": [self.context, other.context]})

    def equal(self, other):
        if self.source.native != other.source.native or self.target.native != other.target.native:
            return False
        # These are full native matrices, not fitted samples. For an actual
        # subspace domain their difference is restricted to its complete Sage
        # basis by exact matrix algebra; this decides the entire linear action.
        basis = basis_matrix(self.source)
        return bool(((self.matrix - other.matrix) * basis.transpose()).is_zero())

    def kernel(self):
        source_basis = basis_matrix(self.source)
        coordinate_matrix = self.matrix * source_basis.transpose()
        coordinate_kernel = coordinate_matrix.right_kernel()
        ambient_basis = coordinate_kernel.basis_matrix() * source_basis
        ambient = QQ ** degree(self.source)
        return ambient.subspace(ambient_basis.rows())


def identity(source, target, context):
    if source.native != target.native:
        raise Unsupported("identity requires the same actual native module")
    return LinearAction(identity_matrix(QQ, degree(source)), source, target, context)


def zero(source, target, context):
    return LinearAction(matrix(QQ, degree(target), degree(source), 0), source, target, context)
