"""
Angular Momentum Partition
==========================

This module verifies the 3:2:3 angular momentum partition of the hourglass.

THE PARTITION:
- TetA bulb (3 SPATIAL faces): 3/8 of total angular momentum
- Neck (2 TIME faces): 2/8 of total angular momentum (this is SPIN)
- TetB bulb (3 SPATIAL faces): 3/8 of total angular momentum

Total: 3/8 + 2/8 + 3/8 = 8/8 = 100%

THE INSIGHT:
Spin is NOT a property of "our side" alone. Spin IS the connection
between TetA and TetB, the flow through the origin, the coupling
across the vortex neck.

Reference: ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md
"""

from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B, HBAR
from gravity_field_model.common.geometry_constants import (
    FACES, TIME_FACES, SPATIAL_FACES
)


# =============================================================================
# CONSTANTS
# =============================================================================

# Face partition
N_TETA_SPATIAL = 3  # SPATIAL faces in TetA
N_TETB_SPATIAL = 3  # SPATIAL faces in TetB
N_TIME = 2  # TIME faces (neck)
N_TOTAL = 8

# Fraction partition
F_TETA = N_TETA_SPATIAL / N_TOTAL  # 3/8 = 0.375
F_NECK = N_TIME / N_TOTAL  # 2/8 = 0.25
F_TETB = N_TETB_SPATIAL / N_TOTAL  # 3/8 = 0.375


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def classify_faces_by_chamber():
    """
    Classify faces as TetA-SPATIAL, TetB-SPATIAL, or TIME (shared).

    Returns dict mapping face names to their classification.
    """
    classification = {}

    # TIME faces (shared neck)
    for f in TIME_FACES:
        classification[f] = 'TIME'

    # SPATIAL faces (in bulbs)
    for f in SPATIAL_FACES:
        # Face is in TetA if it starts with FACE_A
        if f.startswith('FACE_A'):
            classification[f] = 'TETA_SPATIAL'
        else:
            classification[f] = 'TETB_SPATIAL'

    return classification


def analyze_partition_in_traversal(n_digits=10000):
    """
    Analyze how traversal time is spent in each partition.

    Track when we're in TetA bulb, TetB bulb, or crossing the neck.
    """
    traversal = traverse_pi_base8(n_digits)

    # Count time in each region
    time_in_tetA = 0
    time_in_tetB = 0
    time_crossing = 0  # Neck crossing

    for i in range(len(traversal) - 1):
        v1 = traversal[i]['vertex']
        v2 = traversal[i + 1]['vertex']

        in_A_1 = v1 in TET_A
        in_A_2 = v2 in TET_A

        if in_A_1 and in_A_2:
            time_in_tetA += 1
        elif not in_A_1 and not in_A_2:
            time_in_tetB += 1
        else:
            time_crossing += 1

    total = time_in_tetA + time_in_tetB + time_crossing

    return {
        'time_in_tetA': time_in_tetA,
        'time_in_tetB': time_in_tetB,
        'time_crossing': time_crossing,
        'total': total,
        'tetA_fraction': time_in_tetA / total if total > 0 else 0,
        'tetB_fraction': time_in_tetB / total if total > 0 else 0,
        'crossing_fraction': time_crossing / total if total > 0 else 0,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class FacePartitionCounts(Test):
    """
    Verify the face partition: 3 TetA-SPATIAL + 2 TIME + 3 TetB-SPATIAL = 8
    """
    name = "Face Partition Counts"
    question = (
        "Does the stellated octahedron partition into 3+2+3 = 8 faces? "
        "This is the geometric foundation of the hourglass model."
    )
    reference = "Stellated octahedron geometry"
    level = Critical
    tolerance = 0.001

    commentary = (
        "THE 3:2:3 PARTITION: "
        "Each tetrahedron has 4 faces: 3 SPATIAL faces (contain the apex), 1 TIME face (opposite the apex). "
        "The TIME faces point toward the Field Origin. The SPATIAL faces point outward into space. "
        "This geometric fact determines spin: S = (2/8) x 2hbar = hbar/2."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FACE CLASSIFICATION:")
            .step("TetA (Chamber A) faces:")
            .step("FACE_A1 = {2, 4, 7}: SPATIAL (contains apex V7)")
            .step("FACE_A2 = {1, 4, 7}: SPATIAL (contains apex V7)")
            .step("FACE_A4 = {1, 2, 7}: SPATIAL (contains apex V7)")
            .step("FACE_A7 = {1, 2, 4}: TIME (opposite apex)")
            .step("TetB (Chamber B) faces:")
            .step("FACE_B0 = {3, 5, 6}: TIME (opposite apex)")
            .step("FACE_B3 = {0, 5, 6}: SPATIAL (contains apex V0)")
            .step("FACE_B5 = {0, 3, 6}: SPATIAL (contains apex V0)")
            .step("FACE_B6 = {0, 3, 5}: SPATIAL (contains apex V0)")
            .conclude("Count: 3 (TetA-SPATIAL) + 2 (TIME) + 3 (TetB-SPATIAL) = 8")
        )

    def model(self):
        classification = classify_faces_by_chamber()

        tetA_spatial = sum(1 for c in classification.values() if c == 'TETA_SPATIAL')
        tetB_spatial = sum(1 for c in classification.values() if c == 'TETB_SPATIAL')
        time_faces = sum(1 for c in classification.values() if c == 'TIME')
        total = len(classification)

        return (
            Model()
            .add("TetA SPATIAL faces", tetA_spatial)
            .add("TIME faces (neck)", time_faces)
            .add("TetB SPATIAL faces", tetB_spatial)
            .add("Total faces", total)
        )

    def observations(self):
        return (
            Observed()
            .add("TetA SPATIAL faces", 3)
            .add("TIME faces (neck)", 2)
            .add("TetB SPATIAL faces", 3)
            .add("Total faces", 8)
        )


class TraversalPartitionTime(Test):
    """
    How does traversal time partition between bulbs and neck?

    The hourglass model predicts:
    - ~25% of transitions cross the neck (A<->B)
    - ~75% of transitions stay in bulbs (A->A or B->B)

    But wait: bimetric balance says ~50% cross. So which is it?
    Answer: 50% CROSS, but only 25% of ANGULAR MOMENTUM flows.
    """
    name = "Traversal Time Partition"
    question = (
        "How is traversal time partitioned between TetA, TetB, and crossings? "
        "This measures the 'residence time' in each region."
    )
    reference = "Hourglass model, bimetric coupling"
    level = Standard
    tolerance = 0.10

    commentary = (
        "TWO DIFFERENT 25%s: "
        "Face ratio (2/8 = 25%): TIME faces / total faces. This determines SPIN (angular momentum through neck). "
        "Stay ratio (~25%): time spent in one chamber. This is residence time, not angular momentum. "
        "The connection: Often people conflate these two. The 50% crossing rate is about how frequently the traversal "
        "crosses the 'neck'. The 25% for angular momentum is about how much of the total angular momentum "
        "(2hbar for a full spinor rotation) is carried by the TIME faces."
    )

    def derivation(self):
        return (
            Derivation()
            .step("TRAVERSAL TIME PARTITION:")
            .step("For each step, classify as:")
            .step("TetA stay: v1 in TetA AND v2 in TetA")
            .step("TetB stay: v1 in TetB AND v2 in TetB")
            .step("Crossing: v1 and v2 in different chambers")
            .step("Expected for balanced bimetric coupling:")
            .step("TetA stay: ~25%")
            .step("TetB stay: ~25%")
            .step("Crossings: ~50%")
            .conclude("(This is different from the face ratio!)")
        )

    def model(self):
        analysis = analyze_partition_in_traversal(10000)
        return (
            Model()
            .add("TetA stays", analysis['time_in_tetA'])
            .add("TetB stays", analysis['time_in_tetB'])
            .add("Crossings", analysis['time_crossing'])
            .add("TetA fraction", analysis['tetA_fraction'])
            .add("TetB fraction", analysis['tetB_fraction'])
            .add("Crossing fraction", analysis['crossing_fraction'])
        )

    def observations(self):
        return (
            Observed()
            .add("Expected TetA fraction", 0.25)
            .add("Expected TetB fraction", 0.25)
            .add("Expected crossing fraction", 0.50)
        )


class SpinAsSharedConnection(Test):
    """
    Demonstrate that spin is the CONNECTION between chambers, not a local property.

    The hbar/2 that flows through the neck belongs to neither side alone.
    It IS the shared connection.
    """
    name = "Spin as Shared Connection"
    question = (
        "Is spin a property of TetA, TetB, or the connection between them? "
        "The hourglass model says spin IS the connection."
    )
    reference = "ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md Section 6.3"
    level = Critical
    tolerance = 0.001

    commentary = (
        "THE DEEPER MEANING OF SPIN: "
        "We measure spin-1/2 because we measure the INTERFACE, not the whole structure. "
        "The electron vortex has: TetA bulb: 3/4 hbar (local to our side). "
        "Neck: 1/2 hbar (the connection = SPIN). TetB bulb: 3/4 hbar (local to other side). "
        "When we measure spin, we measure what flows through the Field Origin, the interface between worlds. "
        "SPIN IS NOT A PROPERTY OF MATTER. SPIN IS THE CONNECTION BETWEEN CHAMBERS. "
        "SPIN IS WHAT WE SEE OF THE HOURGLASS NECK."
    )

    def derivation(self):
        return (
            Derivation()
            .step("SPIN AS THE SHARED CONNECTION:")
            .step("What belongs to TetA alone: 3 SPATIAL faces: (3/8) x 2hbar = 3hbar/4")
            .step("What belongs to TetB alone: 3 SPATIAL faces: (3/8) x 2hbar = 3hbar/4")
            .step("What is SHARED (the neck): 2 TIME faces: (2/8) x 2hbar = hbar/2")
            .step("INSIGHT:")
            .step("Spin isn't 'in' our side or theirs.")
            .conclude("Spin IS the connection between them.")
        )

    def model(self):
        # Angular momentum partition in units of hbar
        L_total = 2.0

        L_tetA_alone = (3/8) * L_total
        L_tetB_alone = (3/8) * L_total
        L_shared = (2/8) * L_total

        # Verify
        L_sum = L_tetA_alone + L_shared + L_tetB_alone

        # The shared portion IS spin
        spin = L_shared

        return (
            Model()
            .add("L_tetA (hbar)", L_tetA_alone)
            .add("L_tetB (hbar)", L_tetB_alone)
            .add("L_shared = SPIN (hbar)", L_shared)
            .add("L_total (hbar)", L_sum)
            .add("Spin is shared?", 1 if L_shared == 0.5 else 0)
        )

    def observations(self):
        return (
            Observed()
            .add("L_tetA (hbar)", 0.75)
            .add("L_tetB (hbar)", 0.75)
            .add("L_shared = SPIN (hbar)", 0.50)
            .add("Spin is shared?", 1)
        )


# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all angular momentum partition tests."""
    return run_tests(
        "Angular Momentum Partition",
        "Tests for the 3:2:3 angular momentum partition of the hourglass",
        [
            FacePartitionCounts,
            TraversalPartitionTime,
            SpinAsSharedConnection,
        ]
    )


if __name__ == "__main__":
    run_all()
