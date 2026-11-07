"""
Does the pi walk visit the vertices in the I Ching's order?
===========================================================

The Shuo Gua family sequence, read chamber by chamber, is the order that
makes the face reading give the BBP series (test_iching_visit_order.py):
TetA 7, 4, 2, 1 and TetB 0, 3, 5, 6. If the I Ching documents the field
closure walk itself, the walk driven by pi (start at 3, add each base-8
digit, vertex = running sum mod 8) should visit each tetrahedron's
vertices for the first time in that order.

The order is compared cyclically from the apex (Qian 7, Kun 0), as the
reading is. For a uniformly random digit sequence each chamber's cyclic
first-visit order matches with probability 1/6 (one of the 3! orders of the
three non-apex vertices).
"""

import random

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL
from gravity_field_model.engine_core.field_closure import geometry_derivation as geo

TETA_ORDER = [7, 4, 2, 1]
TETB_ORDER = [0, 3, 5, 6]
N_RANDOM = 20000
SEED = 10


def first_visits(digits):
    cum, order = 0, []
    for d in digits:
        cum += d
        v = cum % 8
        if v not in order:
            order.append(v)
            if len(order) == 8:
                break
    return order


def cyclic_from(order, chamber, apex):
    sub = [v for v in order if v in chamber]
    i = sub.index(apex)
    return sub[i:] + sub[:i]


class PiWalkVisitOrder(Test):
    name = "Pi Walk First-Visit Order vs the Shuo Gua Order"
    question = (
        "Does the walk driven by the digits of pi visit the vertices of each tetrahedron in "
        "the Shuo Gua family order, the order the BBP reading needs?"
    )
    reference = "Walk: closure_walk_proof_iching.py; order: Shuo Kua ch. 10 (Wilhelm/Baynes 1950)"
    tolerance = 0.0
    level = Level.EXPLORATORY

    def derivation(self):
        return (
            Derivation()
            .step("Run the walk on 3 followed by the base-8 digits of pi; record the order of first visits.")
            .step("Restrict to each tetrahedron and rotate to start at its apex (7 or 0).")
            .step("Compare with 7, 4, 2, 1 and 0, 3, 5, 6.")
            .step("Estimate the chance of a match for random digit sequences.")
            .conclude("A match in both chambers would support the walk following the I Ching's order.")
        )

    commentary = (
        "The pi walk first visits 3, 4, 5, 0, 7, 1, 2, 6. Read from the apex, TetA comes in the "
        "order 7, 1, 2, 4 and TetB in 0, 6, 3, 5; neither is the Shuo Gua order, so the "
        "prediction fails in both chambers. Random digit sequences match in each chamber about "
        "one time in six. The I Ching's family order is the order in which the face reading "
        "must take the vertices to produce the BBP series; it is not the order in which pi's "
        "digits walk through them. The BBP connection sits in the reading, not in the walk."
    )

    def model(self):
        teta, tetb = None, None
        for t in geo.regular_tetrahedra():
            if 7 in t:
                teta = set(t)
            else:
                tetb = set(t)
        order = first_visits([3] + list(PI_BASE8_FRACTIONAL))
        a = cyclic_from(order, teta, 7)
        b = cyclic_from(order, tetb, 0)
        rng = random.Random(SEED)
        hits_a = hits_b = 0
        for _ in range(N_RANDOM):
            o = first_visits([3] + [rng.randrange(8) for _ in range(400)])
            if len(o) < 8:
                continue
            hits_a += cyclic_from(o, teta, 7) == TETA_ORDER
            hits_b += cyclic_from(o, tetb, 0) == TETB_ORDER
        return (
            Model()
            .add("Pi first-visit order (info)", " ".join(map(str, order)))
            .add("Pi TetA order from apex (info)", " ".join(map(str, a)))
            .add("Pi TetB order from apex (info)", " ".join(map(str, b)))
            .add("Pi walk visits TetA in Shuo Gua order (1=yes)", int(a == TETA_ORDER))
            .add("Pi walk visits TetB in Shuo Gua order (1=yes)", int(b == TETB_ORDER))
            .add("Random TetA match rate", hits_a / N_RANDOM)
            .add("Random TetB match rate", hits_b / N_RANDOM)
        )

    def observations(self):
        return (
            Observed()
            # Prediction of the claim that the walk follows the I Ching's order.
            .add("Pi walk visits TetA in Shuo Gua order (1=yes)", 1)
            .add("Pi walk visits TetB in Shuo Gua order (1=yes)", 1)
            # One of 3! orders of the three non-apex vertices.
            .add("Random TetA match rate", 1 / 6, abs_tol=0.01)
            .add("Random TetB match rate", 1 / 6, abs_tol=0.01)
        )


ALL_TESTS = [PiWalkVisitOrder]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Pi walk visit order", "Does the pi walk follow the I Ching order?", ALL_TESTS) else 1)
