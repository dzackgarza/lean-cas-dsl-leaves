"""Sage Smith-form realization of the registered A_n discriminant cokernel via elementary divisors."""
from engine_python import require_engine
require_engine('CAS_SAGE_PYTHON', 'sage.all')
from cas_port import serve
from sage.all import ZZ, matrix
from sage.version import version as SAGE_VERSION
from wire import finite_cardinal, named_object, numeral
ADAPTER_VERSION = '0.1.0'
SOURCE = 'obj.bil_wform.root_lattice_a'
DUAL = 'obj.bil_wform.root_lattice_a_dual'
DISCRIMINANT = 'obj.bil_wform.root_lattice_a_discriminant'
INCLUSION = 'mor.bil_wform.root_lattice_a_to_dual'
PROJECTION = 'mor.bil_wform.root_lattice_a_to_discriminant'

def named(identifier, n):
    return {'ctor': identifier, 'args': [n]}

def parameter(value, identifier):
    ctor, args = named_object(value)
    if ctor != identifier or len(args) != 1:
        raise ValueError('expected %s at one parameter' % identifier)
    return numeral(args[0])

def smith_order(n):
    # Matrix from upstream rootAGram = negative simple-root dot product.
    gram = matrix(ZZ, n, n, lambda i, j: -2 if i == j else (1 if abs(i-j) == 1 else 0))
    order = ZZ(1)
    for d in gram.elementary_divisors():
        if d == 0:
            raise ValueError('infinite cokernel')
        order *= abs(d)
    return int(order)

def cokernel(value):
    ctor, args = named_object(value)
    if ctor != 'parallelPair' or len(args) != 2:
        raise ValueError('expected parallelPair of inclusion and zero')
    n = parameter(args[0], INCLUSION)
    zero, endpoints = named_object(args[1])
    if zero != 'zero' or endpoints != [named(SOURCE,n),named(DUAL,n)]:
        raise ValueError('expected zero A_n -> A_n dual')
    smith_order(n)
    return {'ctor':'cocone','args':[named(DISCRIMINANT,n),named(PROJECTION,n)]}

def cardinality(value):
    return finite_cardinal(smith_order(parameter(value,DISCRIMINANT)))

serve('sage', SAGE_VERSION, ADAPTER_VERSION,
      {'colim.bil_w_form.cokernel':cokernel,'meth.cardinality':cardinality})
