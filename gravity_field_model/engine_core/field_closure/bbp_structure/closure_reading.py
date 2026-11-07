"""
The six-constraint face-reading mechanism of the closure walk
=============================================================

Implements the mechanism of ``research/exploratory/i-ching/
why_pi_formal_derivation.md`` (and ``why_pi_verification.py``), which derives
the BBP series for pi from the face normals of TetA:

1. Rows: the four TetA face normals as sign patterns, the temporal face
   (+,+,+) first, then the spatial faces 4 = (+,-,-), 2 = (-,+,-), 1 = (-,-,+).
2. Columns: one axis vector per spatial axis, + read as D = 3, - as 1:
   x = [3,3,1,1], y = [3,1,3,1], z = [3,1,1,3].
3. Sector positions: running sum of the z vector from offset 1 -> [1,4,5,6].
4. Magnitudes from (x, y) at each reading: (D,D) -> D+1, (D,1) -> D-1,
   (1,D) -> 1, (1,1) -> 1  -> [4,2,1,1].
5. Signs: + for the temporal face, - for the spatial faces.
6. Series: sum_k 16^-k sum_j sign_j mag_j / (8k + position_j).

Every step is parameterised so the tests can apply the symmetries of the
stellated octahedron and the alternatives the derivation says are excluded.
"""

from fractions import Fraction
from itertools import permutations
from typing import Callable, Dict, List, Sequence, Tuple

D = 3
K = D + 1

# TetA face normals keyed by the vertex each face is opposite to (equivalently
# the vertex the normal points to), as signs on (x, y, z).
TETA_NORMALS: Dict[int, Tuple[int, int, int]] = {
    7: (+1, +1, +1),
    4: (+1, -1, -1),
    2: (-1, +1, -1),
    1: (-1, -1, +1),
}
# TetB normals: the complements 7 - v of the TetA ones, i.e. negated signs.
TETB_NORMALS: Dict[int, Tuple[int, int, int]] = {
    7 - v: tuple(-x for x in n) for v, n in TETA_NORMALS.items()
}
PAPER_ORDER = (7, 4, 2, 1)
PAPER_AXES = (0, 1, 2)          # (x, y) give magnitudes, z gives positions


def paper_rule(x: int, y: int) -> int:
    """The magnitude rule of the derivation (as coded in why_pi_verification.py)."""
    if x == D and y == D:
        return D + 1
    if x == D and y == 1:
        return D - 1
    return 1


def symmetric_rule(both_d: int, disagree: int, both_1: int) -> Callable[[int, int], int]:
    """An agreement rule: the value depends only on whether x and y agree."""
    def rule(x: int, y: int) -> int:
        if x == D and y == D:
            return both_d
        if x == 1 and y == 1:
            return both_1
        return disagree
    return rule


def read(order: Sequence[int] = PAPER_ORDER,
         axes: Sequence[int] = PAPER_AXES,
         rule: Callable[[int, int], int] = paper_rule,
         start: int = 1,
         normals: Dict[int, Tuple[int, int, int]] = None,
         complement: bool = False):
    """
    Run the mechanism. Returns (weights by slot 1..8, positions, magnitudes, signs).

    axes[0], axes[1] are the axes read for magnitudes, axes[2] the axis read
    for sector positions.

    complement=True reads TetB through the complement map, as the derivation
    prescribes: its normals are the negated TetA normals, - is read as D and
    + as 1, and the temporal face is the all-minus one (vertex 0, Kun).
    """
    if normals is None:
        normals = TETB_NORMALS if complement else TETA_NORMALS
    rows = [normals[v] for v in order]
    if complement:
        val = lambda s: D if s < 0 else 1
        temporal = lambda r: all(s < 0 for s in r)
    else:
        val = lambda s: D if s > 0 else 1
        temporal = lambda r: all(s > 0 for s in r)
    x = [val(r[axes[0]]) for r in rows]
    y = [val(r[axes[1]]) for r in rows]
    z = [val(r[axes[2]]) for r in rows]
    positions, p = [], start
    for step in z:
        positions.append(p)
        p += step
    mags = [rule(a, b) for a, b in zip(x, y)]
    signs = [1 if temporal(r) else -1 for r in rows]
    weights = {j: Fraction(0) for j in range(1, 9)}
    for pos, m, s in zip(positions, mags, signs):
        slot = ((pos - 1) % 8) + 1          # residue 0 is slot 8
        weights[slot] += Fraction(s * m)
    return weights, positions, mags, signs


def axis_permutation_is_symmetry(perm: Sequence[int]) -> bool:
    """
    True if permuting the coordinates by `perm` maps TetA to itself and fixes
    the TIME apices 0 and 7 (a symmetry of the stellated octahedron that
    preserves the temporal face).
    """
    def label(c):  # coordinates in {-1,+1} -> 3-bit vertex label (x is the high bit)
        return sum((1 if c[i] > 0 else 0) << (2 - i) for i in range(3))
    teta = set(TETA_NORMALS)
    for v, c in TETA_NORMALS.items():
        image = tuple(c[perm[i]] for i in range(3))
        if label(image) not in teta:
            return False
    return label((1, 1, 1)) == 7 and label((-1, -1, -1)) == 0


ALL_AXIS_PERMUTATIONS: List[Tuple[int, int, int]] = list(permutations(range(3)))

# The three sons of the Shuo Gua family, each with one yang (unbroken) line,
# written bottom line first (Wilhelm, The I Ching or Book of Changes, trans.
# Baynes, 1950, Shuo Kua ch. 10): Zhen (Thunder) yang at the bottom, Kan
# (Water) in the middle, Gen (Mountain) at the top. Their vertex labels in
# the model are 4, 2, 1.
SONS_LINES = {"Zhen": (1, 0, 0), "Kan": (0, 1, 0), "Gen": (0, 0, 1)}
SONS_VERTEX = {"Zhen": 4, "Kan": 2, "Gen": 1}


def line_of_axis() -> Dict[int, str]:
    """
    Which trigram line each coordinate axis carries, read off the sons:
    the axis on which a son's normal is + is the line where it is yang.
    """
    names = ("bottom", "middle", "top")
    out = {}
    for son, lines in SONS_LINES.items():
        normal = TETA_NORMALS[SONS_VERTEX[son]]
        axis = next(i for i, s in enumerate(normal) if s > 0)
        out[axis] = names[lines.index(1)]
    return out
