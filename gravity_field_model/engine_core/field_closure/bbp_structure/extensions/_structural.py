"""
The space of structurally admissible readings (PROOF.md, Theorem 6).

A reading takes the father's tetrahedron in some order (Qian first, then the
three sons in any order), gives each row a weight that is an affine function
of its lines and a step that is an affine function of its lines, starts at
some position, and places + weight for Qian and - weight for each son at the
running positions. Its conditions are structural only; none mentions pi:

    weights positive, steps positive
    closure: Qian's weight equals the sum of the sons' (weights sum to zero)
    one orbit: the four steps sum to 8
    four distinct slots
    TIME silent: no slot on vertex 0 or 7
    chamber balance: two slots in each tetrahedron
"""

from functools import lru_cache
from itertools import permutations, product

LINES = {"Qian": (1, 1, 1), "Zhen": (1, 0, 0), "Kan": (0, 1, 0), "Gen": (0, 0, 1)}
SONS = ("Zhen", "Kan", "Gen")
TETA = {1, 2, 4, 7}
WEIGHT_COEFFS = range(0, 5)
WEIGHT_CONST = range(-2, 3)
STEP_COEFFS = range(0, 4)
STARTS = range(0, 8)


def admissible(order=None):
    """Yield (order, weight (a,c,d,e), step (al,be,ga,de), start, formula) for every admissible reading."""
    orders = [order] if order else list(permutations(SONS))
    for od in orders:
        rows = [LINES["Qian"]] + [LINES[s] for s in od]
        for a, c, d, e in product(WEIGHT_COEFFS, WEIGHT_COEFFS, WEIGHT_COEFFS, WEIGHT_CONST):
            W = [a * b + c * m + d * t + e for b, m, t in rows]
            if min(W) <= 0 or W[0] != sum(W[1:]):
                continue
            for al, be, ga, de in product(STEP_COEFFS, repeat=4):
                S = [al * b + be * m + ga * t + de for b, m, t in rows]
                if min(S) <= 0 or sum(S) != 8:
                    continue
                for st in STARTS:
                    p, slots = st, []
                    for s_ in S:
                        slots.append(((p - 1) % 8) + 1)
                        p += s_
                    verts = {q % 8 for q in slots}
                    if len(set(slots)) < 4 or verts & {0, 7} or len(verts & TETA) != 2:
                        continue
                    formula = tuple(sorted((sl, W[0] if i == 0 else -W[i]) for i, sl in enumerate(slots)))
                    yield od, (a, c, d, e), (al, be, ga, de), st, formula


@lru_cache(maxsize=None)
def admissible_table():
    """Map formula -> list of readings producing it (all orders)."""
    table = {}
    for od, w, s, st, f in admissible():
        table.setdefault(f, []).append((od, w, s, st))
    return table
