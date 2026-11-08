"""
Exact coordinates of the slot series in seven named constants.

The completeness proof (test_bbp_completeness_proof.py) writes each slot
series S_j as a combination of seven logarithms

    Lambda = (i pi, log 2, log(1+sqrt2), log(2+i), log(2-i), log(sqrt2+i), log(sqrt2-i))

with coefficients in Q(zeta_8), and shows Lambda is independent over the
algebraic numbers (Baker). The seven real constants

    pi, ln 2, ln 3, ln 5, arctan(1/2), sqrt2 ln(1+sqrt2), sqrt2 arctan(1/sqrt2)

are also combinations of Lambda (below, exactly). Solving the exact linear
system gives each S_j as a *rational* combination of the named constants.
"""

from functools import lru_cache

import sympy as sp

from gravity_field_model.engine_core.field_closure.bbp_structure.test_bbp_completeness_proof import (
    slot_coefficients, q_parts,
)

I, S2 = sp.I, sp.sqrt(2)
H = sp.Rational(1, 2)

NAMES = ["pi", "ln 2", "ln 3", "ln 5", "arctan(1/2)", "sqrt2 ln(1+sqrt2)", "sqrt2 arctan(1/sqrt2)"]
SYMPY = [sp.pi, sp.log(2), sp.log(3), sp.log(5), sp.atan(H), S2 * sp.log(1 + S2), S2 * sp.atan(1 / S2)]

# Each named constant over Lambda:
#   pi = -i (i pi); ln 3 = log(sqrt2+i) + log(sqrt2-i) since (sqrt2+i)(sqrt2-i) = 3;
#   ln 5 = log(2+i) + log(2-i); arctan(1/2) = arg(2+i) = (log(2+i) - log(2-i))/(2i);
#   arctan(1/sqrt2) = arg(sqrt2+i) = (log(sqrt2+i) - log(sqrt2-i))/(2i).
NAMED_IN_LAMBDA = [
    [-I, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, -I * H, I * H, 0, 0],
    [0, 0, S2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, -I * H * S2, I * H * S2],
]


def _expand(vec):
    """Seven Q(zeta_8) coefficients -> 28 rational coordinates."""
    return [x for c in vec for x in q_parts(c)]


@lru_cache(maxsize=None)
def named_matrix():
    """28 x 7 rational matrix: column k is named constant k in Lambda coordinates."""
    return sp.Matrix([_expand(v) for v in NAMED_IN_LAMBDA]).T


@lru_cache(maxsize=None)
def slot_in_named():
    """8 x 7 rational matrix: row j-1 gives S_j as a combination of the named constants."""
    N = named_matrix()
    rows = []
    for vec in slot_coefficients():
        b = sp.Matrix(_expand(vec))
        sol, params = N.gauss_jordan_solve(b)
        assert params.shape[0] == 0, "named constants are dependent"
        rows.append([sp.nsimplify(x) for x in sol])
    return sp.Matrix(rows)


def value_vector(weights):
    """Named-constant coordinates of sum_j w_j S_j (weights: {slot: number})."""
    M = slot_in_named()
    v = sp.zeros(1, 7)
    for j, w in weights.items():
        v += sp.Rational(w) * M[j - 1, :]
    return v
