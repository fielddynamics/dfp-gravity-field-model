"""
Neck Flow Ratio
===============

This module validates the 2/8 = 25% transfer ratio through the TIME faces.

THE HOURGLASS EQUATION:
S = (N_TIME / N_total) x L_total = (2/8) x 2hbar = hbar/2

The spin-1/2 emerges from:
- 2 TIME faces out of 8 total faces
- This ratio (25%) determines how much angular momentum flows through the neck

THE QUESTION:
Can we measure this 25% flow ratio in the traversal statistics?

Reference: ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md
"""

from collections import Counter

from gravity_field_model.engine_core.field_closure import geometry_derivation as geo
from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, HBAR
from gravity_field_model.common.geometry_constants import (
    FACES, TIME_FACES, SPATIAL_FACES, get_faces_for_vertex
)


# =============================================================================
# CONSTANTS
# =============================================================================

# The predicted neck flow ratio
NECK_FLOW_RATIO = 2 / 8  # = 0.25 = 25%

# Total angular momentum in spinor cycle
L_TOTAL = 2 * HBAR  # 2hbar

# Predicted spin
S_PREDICTED = NECK_FLOW_RATIO * L_TOTAL  # hbar/2


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def analyze_neck_crossing_rate(n_digits=10000):
    """
    Count how often the traversal crosses through the 'neck' (TIME faces).

    The neck connects TetA and TetB through the Field Origin.
    A 'neck crossing' occurs when we transition between chambers.
    """
    traversal = traverse_pi_base8(n_digits)

    # Count chamber transitions
    total_transitions = 0
    neck_crossings = 0  # A->B or B->A
    bulb_stays = 0  # A->A or B->B

    for i in range(len(traversal) - 1):
        v1 = traversal[i]['vertex']
        v2 = traversal[i + 1]['vertex']

        in_A_1 = v1 in TET_A
        in_A_2 = v2 in TET_A

        total_transitions += 1

        if in_A_1 != in_A_2:
            neck_crossings += 1
        else:
            bulb_stays += 1

    return {
        'total_transitions': total_transitions,
        'neck_crossings': neck_crossings,
        'bulb_stays': bulb_stays,
        'neck_crossing_rate': neck_crossings / total_transitions if total_transitions > 0 else 0,
        'bulb_stay_rate': bulb_stays / total_transitions if total_transitions > 0 else 0,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class NeckCrossingRate(Test):
    """
    How often does the traversal cross through the neck (between chambers)?

    The hourglass model predicts cross-chamber transitions occur ~50% of the time
    (balanced bimetric coupling). But the FLOW through the neck is 25%.
    """
    name = "Neck Crossing Rate"
    question = (
        "How often does the traversal cross from TetA to TetB or vice versa? "
        "This is the rate at which the vortex passes through the neck."
    )
    reference = "Bimetric coupling, hourglass model"
    level = Standard
    tolerance = 0.10

    commentary = (
        "NECK PERMEABILITY: "
        "A ~50% neck crossing rate means the Field Origin is "
        "a freely permeable interface between TetA and TetB. "
        "Why 50% and not 25%? 50% is the TRANSITION rate (how often we cross). "
        "25% is the FLOW rate (how much angular momentum). "
        "The distinction: Crossing is binary (did we cross or not?). "
        "Flow is continuous (how much passes through?). "
        "The 2/8 = 25% applies to ANGULAR MOMENTUM, not transitions."
    )

    def derivation(self):
        return (
            Derivation()
            .step("NECK CROSSING ANALYSIS:")
            .step("A neck crossing = transition between TetA and TetB")
            .step("A bulb stay = transition within TetA or within TetB")
            .step("For balanced bimetric coupling:")
            .step("Each vertex has 4 neighbors: 2 in same chamber, 2 in other")
            .equation("Expected cross-chamber rate ~ 50%")
            .conclude("This measures how 'permeable' the neck is.")
        )

    def model(self):
        analysis = analyze_neck_crossing_rate(10000)
        return (
            Model()
            .add("Total transitions", analysis['total_transitions'])
            .add("Neck crossings", analysis['neck_crossings'], tol=0.03)
            .add("Bulb stays", analysis['bulb_stays'], tol=0.03)
            .add("Neck crossing rate", analysis['neck_crossing_rate'], tol=0.03)
        )

    def observations(self):
        # A transition crosses chambers with probability 1/2: about 5000 of
        # 10,000 (standard deviation 50, i.e. 1%).
        return (
            Observed()
            .add("Neck crossings", 5000)
            .add("Bulb stays", 5000)
            .add("Neck crossing rate", 0.5)
        )

class SpinFromFaceRatio(Test):
    """
    Derive spin from the TIME/total face ratio.

    S = (N_TIME / N_total) x L_total = (2/8) x 2hbar = hbar/2
    """
    name = "Spin From Face Ratio"
    question = (
        "Does the ratio of TIME faces to total faces (2/8) correctly "
        "predict electron spin S = hbar/2? This is the core hourglass equation."
    )
    reference = "Paper VI, ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md"
    level = Critical
    tolerance = 0.001

    commentary = (
        "THE SPIN DERIVATION: "
        "Why this works: 1. The stellated octahedron has 8 faces (fixed by k=4). "
        "2. 2 faces point toward the origin (TIME faces). "
        "3. Spinors carry 2hbar per cycle (720 degree rotation). "
        "4. Spin = what flows through the TIME faces. "
        "NO FREE PARAMETERS: The 2 comes from geometry (one TIME face per tet). "
        "The 8 comes from geometry (k=4 means 2x4 faces). "
        "The 2hbar comes from spinor math (720 degree cycle). "
        "Result: S = (2/8) x 2hbar = hbar/2 EXACTLY."
    )

    def derivation(self):
        return (
            Derivation()
            .step("THE HOURGLASS SPIN EQUATION:")
            .step("Step 1: Count faces")
            .step("Total faces: N_total = 8 (stellated octahedron)")
            .step("TIME faces: N_TIME = 2 (FACE_A7, FACE_B0)")
            .step("Step 2: Compute neck fraction")
            .equation("f_neck = N_TIME / N_total = 2/8 = 0.25")
            .step("Step 3: Total spinor angular momentum")
            .equation("L_total = 2 * hbar (720 degree cycle)")
            .step("Step 4: Spin = what flows through the neck")
            .equation("S = f_neck x L_total = 0.25 x 2*hbar = hbar/2")
            .conclude("Electron spin S = hbar/2 from pure geometry.")
        )

    def model(self):
        # Face counts from the coordinates; total angular momentum 2 hbar is the
        # model's input. The derived spin is compared with the measured hbar/2.
        n_time = len(geo.time_faces())
        n_total = len(geo.tetrahedron_faces())
        f_neck = n_time / n_total
        S_derived = f_neck * 2 * HBAR
        return (
            Model()
            .add("N_TIME faces", n_time)
            .add("N_total faces", n_total)
            .add("f_neck = N_TIME/N_total", f_neck)
            .add("S_derived (J*s)", S_derived)
        )

    def observations(self):
        # Electron spin angular momentum hbar/2, with hbar = h / 2 pi and
        # h = 6.62607015e-34 J s (exact).
        return (
            Observed()
            .add("N_TIME faces", 2)
            .add("N_total faces", 8)
            .add("f_neck = N_TIME/N_total", 0.25)
            .add("S_derived (J*s)", 6.62607015e-34 / (2 * 3.141592653589793) / 2)
        )

class AngularMomentumBudget(Test):
    """
    Verify the full angular momentum budget: TetA bulb + neck + TetB bulb = 2hbar

    The hourglass partition:
    - TetA SPATIAL (3 faces): 3hbar/4
    - TIME neck (2 faces): hbar/2
    - TetB SPATIAL (3 faces): 3hbar/4
    - Total: 3/4 + 1/2 + 3/4 = 2hbar
    """
    name = "Angular Momentum Budget"
    question = (
        "Does the angular momentum partition correctly? "
        "TetA bulb (3/8) + neck (2/8) + TetB bulb (3/8) = 8/8 = 100%"
    )
    reference = "ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md"
    level = Critical
    tolerance = 0.001

    commentary = (
        "THE HOURGLASS BALANCE: "
        "The angular momentum is perfectly balanced: "
        "TetA bulb: 3/4 hbar. Neck (spin): 1/2 hbar. TetB bulb: 3/4 hbar. Total: 2 hbar. "
        "Physical interpretation: 75% stays in the bulbs (local structure). "
        "25% flows through the neck (spin). "
        "The hourglass is symmetric: TetA and TetB each hold the same amount (3/4 hbar), "
        "while the neck carries the shared connection (1/2 hbar = spin)."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ANGULAR MOMENTUM BUDGET:")
            .step("Total angular momentum: L_total = 2*hbar")
            .step("Split by face type:")
            .step("TIME faces (2/8): (2/8) x 2*hbar = hbar/2 (flows through)")
            .step("SPATIAL faces (6/8): (6/8) x 2*hbar = 3*hbar/2 (stays in bulbs)")
            .step("Split by chamber:")
            .step("TetA SPATIAL (3 faces): (3/8) x 2*hbar = 3*hbar/4")
            .step("TIME neck (2 faces): (2/8) x 2*hbar = hbar/2")
            .step("TetB SPATIAL (3 faces): (3/8) x 2*hbar = 3*hbar/4")
            .equation("3*hbar/4 + hbar/2 + 3*hbar/4 = 2*hbar")
            .conclude("Total: 3/4 + 1/2 + 3/4 = 8/4 = 2 (in units of hbar)")
        )

    def model(self):
        # Face counts from the coordinates: 8 faces, 2 of them perpendicular to
        # the 0-7 axis (TIME), 3 spatial faces on each tetrahedron. The total of
        # 2 hbar is the hourglass model's input.
        faces = geo.tetrahedron_faces()
        time = geo.time_faces()
        tets = sorted(geo.regular_tetrahedra(), key=min)
        n_total = len(faces)
        f_time = len(time) / n_total
        f_tetA_spatial = sum(1 for v, f in faces.items() if v not in time and f <= tets[1]) / n_total
        f_tetB_spatial = sum(1 for v, f in faces.items() if v not in time and f <= tets[0]) / n_total
        L_total_hbar = 2.0
        return (
            Model()
            .add("TetA SPATIAL (3/8 x 2hbar)", f_tetA_spatial * L_total_hbar)
            .add("TIME neck (2/8 x 2hbar)", f_time * L_total_hbar)
            .add("TetB SPATIAL (3/8 x 2hbar)", f_tetB_spatial * L_total_hbar)
            .add("Sum (should = 2)", (f_tetA_spatial + f_time + f_tetB_spatial) * L_total_hbar)
        )

    def observations(self):
        # TIME neck = electron spin, hbar/2; the remainder split equally.
        return (
            Observed()
            .add("TetA SPATIAL (3/8 x 2hbar)", 0.75)
            .add("TIME neck (2/8 x 2hbar)", 0.5)
            .add("TetB SPATIAL (3/8 x 2hbar)", 0.75)
            .add("Sum (should = 2)", 2.0)
        )

# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all neck flow ratio tests."""
    return run_tests(
        "Neck Flow Ratio",
        "Tests for the 2/8 = 25% transfer ratio through the TIME faces",
        [
            NeckCrossingRate,
            SpinFromFaceRatio,
            AngularMomentumBudget,
        ]
    )


if __name__ == "__main__":
    run_all()
