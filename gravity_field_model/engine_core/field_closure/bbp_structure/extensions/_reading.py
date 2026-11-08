"""Shared helpers for the trigram-line reading (PROOF.md, Theorem 5)."""

from fractions import Fraction

from mpmath import mp, mpf, pi

from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_slots import formula_value

LINES_BY_LABEL = {v: ((v >> 2) & 1, (v >> 1) & 1, v & 1) for v in range(8)}   # bottom, middle, top
NAME = {7: "Qian", 4: "Zhen", 2: "Kan", 1: "Gen", 0: "Kun", 3: "Xun", 5: "Li", 6: "Dui"}


def read_rows(labels, complement=False, weight=lambda b, m, t: 2 * b + m + t,
              step=lambda b, m, t: 2 * t + 1, start=1):
    """Weights by slot for rows `labels` (apex first): + apex, - others."""
    w, p = {}, start
    for k, v in enumerate(labels):
        b, m, t = LINES_BY_LABEL[v]
        if complement:
            b, m, t = 1 - b, 1 - m, 1 - t
        slot = ((p - 1) % 8) + 1
        w[slot] = w.get(slot, 0) + (1 if k == 0 else -1) * weight(b, m, t)
        p += step(b, m, t)
    return {j: Fraction(x) for j, x in w.items() if x != 0}


def is_pi(weights, digits=60):
    with mp.workdps(digits + 10):
        return bool(abs(formula_value(weights) - pi) < mpf(10) ** -digits)
