"""
TIME Face Completion Rate
=========================

This module tests the completion timing of TIME vs SPATIAL faces.

THE HOURGLASS MODEL:
The Merkaba is an hourglass with:
- 6 SPATIAL faces (the bulbs): point outward into TetA/TetB space
- 2 TIME faces (the neck): point toward the Field Origin

THE PREDICTION:
TIME faces should complete later than SPATIAL faces during traversal,
because they are the "bottleneck" through which angular momentum flows.

Reference: ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md, Paper VI
"""

from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import get_pi_base8
from gravity_field_model.common.geometry_constants import (
    TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES,
    get_faces_for_vertex
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def traverse_and_track_face_completion(n_digits=10000):
    """
    Traverse and track when each face completes.

    A face "completes" when all 3 of its vertices have been visited.
    """
    digits = get_pi_base8(n_digits, include_integer=True)

    # Track which vertices have been seen for each face
    face_reads = {name: set() for name in FACES}
    face_completed_at = {}

    cumsum = 0
    for step, digit in enumerate(digits):
        cumsum += digit
        vertex = cumsum % 8

        # Update face reads
        for fname in get_faces_for_vertex(vertex):
            face_reads[fname].add(vertex)

            # Check if face just completed
            if fname not in face_completed_at and face_reads[fname] == FACES[fname]:
                face_completed_at[fname] = step

    return face_completed_at


def analyze_face_completion_timing(n_digits=10000):
    """
    Analyze completion timing for TIME vs SPATIAL faces.
    """
    completion = traverse_and_track_face_completion(n_digits)

    # Separate TIME and SPATIAL face completion times
    time_completions = [completion.get(f, n_digits) for f in TIME_FACES]
    spatial_completions = [completion.get(f, n_digits) for f in SPATIAL_FACES]

    # Statistics
    time_mean = sum(time_completions) / len(time_completions) if time_completions else 0
    spatial_mean = sum(spatial_completions) / len(spatial_completions) if spatial_completions else 0

    time_min = min(time_completions) if time_completions else 0
    time_max = max(time_completions) if time_completions else 0
    spatial_min = min(spatial_completions) if spatial_completions else 0
    spatial_max = max(spatial_completions) if spatial_completions else 0

    # How much later do TIME faces complete?
    delay_ratio = time_mean / spatial_mean if spatial_mean > 0 else 0

    return {
        'time_completions': time_completions,
        'spatial_completions': spatial_completions,
        'time_mean': time_mean,
        'spatial_mean': spatial_mean,
        'time_min': time_min,
        'time_max': time_max,
        'spatial_min': spatial_min,
        'spatial_max': spatial_max,
        'delay_ratio': delay_ratio,
        'all_faces_complete': len(completion) == 8,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class TimeFaceCompleteLater(Test):
    """
    Do TIME faces complete later than SPATIAL faces?

    The hourglass model predicts TIME faces are the "neck" and should
    complete after the SPATIAL faces (the bulbs).
    """
    name = "TIME Faces Complete Later"
    question = (
        "Do the TIME faces (FACE_A7, FACE_B0) complete later than SPATIAL faces? "
        "The hourglass model says the neck (TIME faces) is the bottleneck "
        "through which angular momentum flows."
    )
    reference = "ELECTRON_HALF_SPIN_HOURGLASS_VORTEX.md"
    level = Critical
    tolerance = 0.20

    commentary = (
        "THE NECK BOTTLENECK: "
        "If TIME faces complete later, it confirms the hourglass model: "
        "The neck is harder to 'fill'. Angular momentum must squeeze through. "
        "This is why spin = what flows through the neck. "
        "Physical interpretation: The TIME faces are the interface between TetA and TetB. "
        "They complete later because crossing between chambers requires going through the Field Origin."
    )

    def derivation(self):
        return (
            Derivation()
            .step("FACE COMPLETION IN THE HOURGLASS:")
            .step("SPATIAL faces (6 total): the bulbs")
            .step("FACE_A1, FACE_A2, FACE_A4 (in TetA), FACE_B3, FACE_B5, FACE_B6 (in TetB)")
            .step("Each contains the apex vertex. Points outward into space.")
            .step("TIME faces (2 total): the neck")
            .step("FACE_A7 = {1, 2, 4} (opposite apex V7)")
            .step("FACE_B0 = {3, 5, 6} (opposite apex V0)")
            .step("Point toward Field Origin.")
            .conclude("Prediction: TIME faces complete later because they exclude the apex vertex, which is visited frequently.")
        )

    def model(self):
        analysis = analyze_face_completion_timing(10000)
        return (
            Model()
            .add("TIME mean completion", analysis['time_mean'])
            .add("SPATIAL mean completion", analysis['spatial_mean'])
            .add("Delay ratio (TIME/SPATIAL)", analysis['delay_ratio'])
            .add("TIME min", analysis['time_min'])
            .add("TIME max", analysis['time_max'])
        )

    def observations(self):
        return (
            Observed()
            .add("Expected delay ratio", 1.2)
            .add("TIME should be > SPATIAL", 1)
        )


class TimeFaceRareVisitation(Test):
    """
    Are TIME face vertices visited less frequently during early traversal?

    The TIME faces are {1,2,4} and {3,5,6}. These exclude the apexes
    V7 and V0. If the traversal explores the bulbs first, TIME face
    vertices might be underrepresented early on.
    """
    name = "TIME Face Vertex Visitation Rate"
    question = (
        "Do TIME face vertices get visited at a different rate than "
        "SPATIAL face vertices? This affects face completion timing."
    )
    reference = "Face structure analysis"
    level = Standard
    tolerance = 0.10

    commentary = (
        "VERTEX VISITATION AND FACE COMPLETION: "
        "If all vertices are visited equally (1/8 each), "
        "then face completion depends on the COMBINATION. "
        "TIME faces need 3 specific vertices: FACE_A7 needs {1, 2, 4}, FACE_B0 needs {3, 5, 6}. "
        "SPATIAL faces can use the apexes: V7 helps complete 3 SPATIAL faces, V0 helps complete 3 SPATIAL faces. "
        "The apexes are 'multi-purpose' vertices, which is why SPATIAL faces complete faster."
    )

    def derivation(self):
        return (
            Derivation()
            .step("VERTEX CLASSIFICATION BY FACE TYPE:")
            .step("TIME faces contain: {1,2,4} and {3,5,6}")
            .step("This is all vertices EXCEPT V0 and V7.")
            .step("SPATIAL faces contain the apexes:")
            .step("V7 is in 3 SPATIAL faces of TetA")
            .step("V0 is in 3 SPATIAL faces of TetB")
            .conclude("All 8 vertices should be visited equally (1/8 each). But TIME face COMPLETION depends on getting 3 specific non-apex vertices together.")
        )

    def model(self):
        digits = get_pi_base8(10000, include_integer=True)

        # Count vertex visits
        vertex_counts = Counter()
        cumsum = 0
        for digit in digits:
            cumsum += digit
            vertex = cumsum % 8
            vertex_counts[vertex] += 1

        total = sum(vertex_counts.values())

        # TIME face vertices (all except 0 and 7)
        time_vertices = [1, 2, 3, 4, 5, 6]
        apex_vertices = [0, 7]

        time_freq = sum(vertex_counts[v] for v in time_vertices) / total
        apex_freq = sum(vertex_counts[v] for v in apex_vertices) / total

        return (
            Model()
            .add("V0 frequency", vertex_counts[0] / total)
            .add("V7 frequency", vertex_counts[7] / total)
            .add("Apex total (V0+V7)", apex_freq)
            .add("Non-apex total", time_freq)
        )

    def observations(self):
        return (
            Observed()
            .add("Expected per vertex", 0.125)
            .add("Expected apex total", 0.25)
            .add("Expected non-apex total", 0.75)
        )


class NeckVsBulbCompletionOrder(Test):
    """
    In what order do faces complete: bulbs first, then neck?

    The hourglass model predicts SPATIAL faces (bulbs) complete before
    TIME faces (neck).
    """
    name = "Neck vs Bulb Completion Order"
    question = (
        "Do the bulbs (SPATIAL faces) complete before the neck (TIME faces)? "
        "Track the completion order of all 8 faces."
    )
    reference = "Hourglass vortex model"
    level = Standard
    tolerance = 0.15

    commentary = (
        "COMPLETION ORDER AND THE HOURGLASS: "
        "If 4+ SPATIAL faces complete before any TIME face, the hourglass model is supported. "
        "Physical meaning: The bulbs fill with 'stuff' first. The neck is the last to complete. "
        "Angular momentum waits to flow through. This is why spin = (2/8) x 2hbar: The 2 TIME faces control the flow rate."
    )

    def derivation(self):
        return (
            Derivation()
            .step("COMPLETION ORDER PREDICTION:")
            .step("If the hourglass model is correct:")
            .step("1. SPATIAL faces complete first (bulbs fill)")
            .step("2. TIME faces complete last (neck fills)")
            .step("Count how many SPATIAL faces complete before TIME faces.")
            .conclude("Expected: most SPATIAL faces complete before most TIME faces.")
        )

    def model(self):
        completion = traverse_and_track_face_completion(10000)

        # Get completion times
        time_times = [(f, completion.get(f, 10000)) for f in TIME_FACES]
        spatial_times = [(f, completion.get(f, 10000)) for f in SPATIAL_FACES]

        # Sort by completion time
        all_sorted = sorted(time_times + spatial_times, key=lambda x: x[1])

        # Count how many SPATIAL complete before first TIME
        first_time = min(t for _, t in time_times)
        spatial_before_time = sum(1 for f, t in spatial_times if t < first_time)

        return (
            Model()
            .add("First TIME completion step", first_time)
            .add("SPATIAL faces before first TIME", spatial_before_time)
        )

    def observations(self):
        return (
            Observed()
            .add("Expected SPATIAL before TIME", 4)
        )


# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all TIME face completion tests."""
    return run_tests(
        "TIME Face Completion",
        "Tests for TIME vs SPATIAL face completion timing in the hourglass model",
        [
            TimeFaceCompleteLater,
            TimeFaceRareVisitation,
            NeckVsBulbCompletionOrder,
        ]
    )


if __name__ == "__main__":
    run_all()
