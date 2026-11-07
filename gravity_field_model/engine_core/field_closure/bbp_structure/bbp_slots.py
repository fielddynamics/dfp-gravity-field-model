"""
BBP slot series and the complete family of base-16, period-8 formulas for pi
============================================================================

Shared functions for the tests in this package. They ask whether the
Bailey-Borwein-Plouffe (BBP) formula

    pi = sum_n 16^-n [ 4/(8n+1) - 2/(8n+4) - 1/(8n+5) - 1/(8n+6) ]

is the stellated-octahedron structure, as the research note
``research/bbp and pi field closure stepping/bbp_field_closure_synthesis.md``
proposes, by testing consequences that could fail.

Notation
--------
Slot j (j = 1..8) is the series

    S_j = sum_{n>=0} 1 / (16^n (8n + j)).

Slot 8 has residue 0 mod 8, so slot j is read as cube vertex j mod 8 (the
3-bit labelling used throughout the model). A *formula* is a rational weight
vector w with sum_j w_j S_j equal to a constant.

Mathematical sources
--------------------
- Bailey, Borwein, Plouffe (1997), Math. Comp. 66, 903-913.
- Adamchik, Wagon (1997), Amer. Math. Monthly 104, 852-855: the one-parameter
  family of base-16 formulas for pi, and the base -4 formula.
- Ferguson, Bailey, Arno (1999), Math. Comp. 68, 351-369: the PSLQ integer
  relation algorithm (mpmath.pslq).

The geometry (tetrahedra, TIME apices) comes from ``geometry_derivation``,
which works from the cube coordinates alone.
"""

from fractions import Fraction
from functools import lru_cache
from typing import Dict, List, Optional, Sequence

from mpmath import mp, mpf, nsum, inf, pslq

from gravity_field_model.engine_core.field_closure import geometry_derivation as geo

# Working precision (decimal digits) and the largest integer coefficient PSLQ
# may use. A relation reported as absent means: none with coefficients up to
# MAX_COEFF exists at this precision.
PRECISION = 100
MAX_COEFF = 10 ** 8

SLOTS = tuple(range(1, 9))

# The published BBP formula, keyed by slot.
BBP_WEIGHTS: Dict[int, Fraction] = {1: Fraction(4), 4: Fraction(-2), 5: Fraction(-1), 6: Fraction(-1)}

# Adamchik-Wagon (1997): for every r,
#   pi = sum_n 16^-n [ (4+8r)/(8n+1) - 8r/(8n+2) - 4r/(8n+3) - (2+8r)/(8n+4)
#                      - (1+2r)/(8n+5) - (1+2r)/(8n+6) + r/(8n+7) ].
# Weights are a_j + r * b_j.
AW_CONSTANT = {1: 4, 2: 0, 3: 0, 4: -2, 5: -1, 6: -1, 7: 0, 8: 0}
AW_PER_R = {1: 8, 2: -8, 3: -4, 4: -8, 5: -2, 6: -2, 7: 1, 8: 0}


def aw_weights(r) -> Dict[int, Fraction]:
    """Weights of the Adamchik-Wagon family member with parameter r (exact)."""
    r = Fraction(r)
    return {j: Fraction(AW_CONSTANT[j]) + r * AW_PER_R[j] for j in SLOTS}


@lru_cache(maxsize=None)
def slot_values(base: int = 16, period: int = 8) -> tuple:
    """S_j for j = 1..period at PRECISION digits."""
    with mp.workdps(PRECISION + 10):
        return tuple(
            nsum(lambda n, j=j: 1 / (mpf(base) ** n * (period * n + j)), [0, inf])
            for j in range(1, period + 1)
        )


def formula_value(weights: Dict[int, Fraction], base: int = 16, period: int = 8):
    """sum_j w_j S_j."""
    vals = slot_values(base, period)
    with mp.workdps(PRECISION + 10):
        return sum(mpf(w.numerator) / w.denominator * vals[j - 1] for j, w in weights.items())


def integer_relation(values: Sequence) -> Optional[List[int]]:
    """PSLQ integer relation among the values, or None if none within MAX_COEFF."""
    with mp.workdps(PRECISION):
        return pslq(list(values), maxcoeff=MAX_COEFF, maxsteps=10 ** 7)


def slot7_free_formula(constant) -> Optional[Dict[int, Fraction]]:
    """
    The formula for `constant` over the slots other than 7, if one exists.

    The only integer relation among the eight slot series is the
    Adamchik-Wagon r-term, whose slot-7 weight is 1, so every constant in their
    span has exactly one formula with w_7 = 0; this returns it.
    """
    basis = [j for j in SLOTS if j != 7]
    vals = slot_values()
    rel = integer_relation([vals[j - 1] for j in basis] + [constant])
    if rel is None or rel[-1] == 0:
        return None
    w = {j: Fraction(-rel[i], rel[-1]) for i, j in enumerate(basis)}
    w[7] = Fraction(0)
    return w


# ---------------------------------------------------------------------------
# Octahedral reading of a formula
# ---------------------------------------------------------------------------

def tetrahedra():
    """The two inscribed tetrahedra, as vertex sets, from cube coordinates."""
    return [set(t) for t in geo.regular_tetrahedra()]


def time_apices() -> set:
    """Vertices on the TIME axis (the body diagonal the model calls time)."""
    return set(geo.time_faces())


def active_vertices(weights: Dict[int, Fraction]) -> set:
    return {j % 8 for j, w in weights.items() if w != 0}


def octahedral_conditions(weights: Dict[int, Fraction]) -> Dict[str, bool]:
    """
    The conditions the research note reads into the BBP formula:
    TIME apices silent, weights summing to zero (closure), four active slots
    (K = 4), and two active slots in each tetrahedron (chamber balance).
    """
    act = active_vertices(weights)
    t1, t2 = tetrahedra()
    return {
        "time_silent": not (act & time_apices()),
        "zero_sum": sum(weights.values()) == 0,
        "four_active": len(act) == 4,
        "chamber_2_2": len(act & t1) == 2 and len(act & t2) == 2,
    }


def is_octahedral(weights: Dict[int, Fraction]) -> bool:
    return all(octahedral_conditions(weights).values())
