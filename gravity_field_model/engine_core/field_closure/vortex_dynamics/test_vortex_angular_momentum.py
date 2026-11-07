"""
Vortex Angular Momentum
=======================

This module validates angular momentum properties of the Merkaba vortex.

THE QUESTION:
Does the pi-base-8 traversal carry angular momentum? Can we measure it?

THE APPROACH:
The vortex model says gravity is a rotating field around the Field Origin.
Angular momentum should manifest in the traversal as:
1. A consistent "handedness" (chirality)
2. Cumulative rotation around the origin
3. Conservation of angular momentum through the traversal

KEY INSIGHT:
If vertex coordinates are (-1,-1,-1) to (+1,+1,+1), the traversal traces
a path in 3D space. The cross product of consecutive position vectors
gives angular momentum direction.

Reference: VORTEX_COSMOLOGY_AND_INFORMATION_DOMAINS.md
"""

import math
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8


# =============================================================================
# GEOMETRY CONSTANTS
# =============================================================================

# Vertex coordinates (cube corners)
VERTEX_COORDS = {
    0: (-1, -1, -1),  # 000
    1: (-1, -1, +1),  # 001
    2: (-1, +1, -1),  # 010
    3: (-1, +1, +1),  # 011
    4: (+1, -1, -1),  # 100
    5: (+1, -1, +1),  # 101
    6: (+1, +1, -1),  # 110
    7: (+1, +1, +1),  # 111
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def cross_product(v1, v2):
    """Compute cross product of two 3D vectors."""
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )


def vector_magnitude(v):
    """Compute magnitude of a 3D vector."""
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)


def compute_angular_momentum_per_step(traversal):
    """
    Compute angular momentum contribution from each step.

    L = r x p, where:
    - r is the position vector (vertex coordinates)
    - p is the momentum vector (proportional to velocity = delta_r)

    For discrete steps, L ~ r_i x (r_{i+1} - r_i)
    """
    L_values = []

    for i in range(len(traversal) - 1):
        v1 = traversal[i]['vertex']
        v2 = traversal[i + 1]['vertex']

        r1 = VERTEX_COORDS[v1]
        r2 = VERTEX_COORDS[v2]

        # Velocity vector (change in position)
        delta_r = (r2[0] - r1[0], r2[1] - r1[1], r2[2] - r1[2])

        # Angular momentum: L = r x v
        L = cross_product(r1, delta_r)
        L_values.append(L)

    return L_values


def analyze_angular_momentum(n_digits=10000):
    """Complete angular momentum analysis."""
    traversal = traverse_pi_base8(n_digits)
    L_values = compute_angular_momentum_per_step(traversal)

    # Final cumulative L
    L_cum = (0, 0, 0)
    for L in L_values:
        L_cum = (L_cum[0] + L[0], L_cum[1] + L[1], L_cum[2] + L[2])
    
    L_final_mag = vector_magnitude(L_cum)

    # Mean magnitude per step
    L_mags = [vector_magnitude(L) for L in L_values]
    mean_L_mag = sum(L_mags) / len(L_mags) if L_mags else 0

    # Check for chirality (preferred handedness)
    L_z_values = [L[2] for L in L_values]
    positive_z = sum(1 for Lz in L_z_values if Lz > 0)
    negative_z = sum(1 for Lz in L_z_values if Lz < 0)

    chirality = (positive_z - negative_z) / len(L_z_values) if L_z_values else 0

    return {
        'L_final': L_cum,
        'L_final_magnitude': L_final_mag,
        'mean_L_magnitude': mean_L_mag,
        'total_steps': len(L_values),
        'positive_z': positive_z,
        'negative_z': negative_z,
        'chirality': chirality,
    }


# =============================================================================
# TEST CLASSES
# =============================================================================

class AngularMomentumAccumulation(Test):
    """
    Does the traversal accumulate angular momentum?

    If the vortex model is correct, the traversal should show net rotation
    around the Field Origin (0,0,0).
    """
    name = "Angular Momentum Accumulation"
    question = (
        "Does the Merkaba traversal accumulate angular momentum? "
        "A vortex by definition has rotation. If the pi-base-8 traversal "
        "is a vortex, it should show cumulative angular momentum."
    )
    reference = "Vortex cosmology model"
    level = Standard
    tolerance = 0.20

    commentary = (
        "INTERPRETING ANGULAR MOMENTUM: "
        "Random walk: L ~ sqrt(N) (cancellation). "
        "Coherent vortex: L ~ N (accumulation). "
        "The traversal's angular momentum growth rate indicates "
        "whether the field closure is truly vortex-like. "
        "Key insight: Even if individual steps appear random, the cumulative "
        "angular momentum reveals underlying rotational structure."
    )

    def derivation(self):
        return (
            Derivation()
            .step("ANGULAR MOMENTUM IN THE TRAVERSAL:")
            .step("For each step from vertex v1 to v2:")
            .step("Position: r = coordinates of v1")
            .step("Velocity: v = (coordinates of v2) - (coordinates of v1)")
            .step("Angular momentum: L = r x v (cross product)")
            .step("Cumulative L = sum of all L contributions")
            .conclude("For a vortex, cumulative L should grow with time, indicating net rotation around the origin.")
        )

    def model(self):
        analysis = analyze_angular_momentum(10000)
        L = analysis['L_final']
        magnitude = analysis['L_final_magnitude']
        return (
            Model()
            .add("L_x (final)", L[0])
            .add("L_y (final)", L[1])
            .add("L_z (final)", L[2])
            .add("L magnitude (final)", magnitude)
        .add("log10 |L| (final)", math.log10(magnitude) if magnitude > 0 else -99.0, abs_tol=0.65)
            .add("Below vortex scale (|L| < 0.1 N)", 1 if magnitude < 0.1 * analysis['total_steps'] else 0)
            .add("Total steps", analysis['total_steps'])
        )

    def observations(self):
        # For independent steps L accumulates as a random walk: mean |L| after
        # 10,000 steps is about 234 (mean of 60 random sequences; 99% between
        # 57 and 520). A coherent vortex would instead grow like N, reaching
        # thousands; the flag separates the two. The magnitude is compared on a
    # log scale (234 within a factor of 4.5) because its spread is skewed.
        return (
            Observed()
            .add("log10 |L| (final)", round(math.log10(234), 3))
            .add("Below vortex scale (|L| < 0.1 N)", 1)
        )

class ChiralityMeasurement(Test):
    """
    Does the traversal have a preferred handedness (chirality)?

    A vortex spins either clockwise or counterclockwise. The traversal
    should show preference for one direction.
    """
    name = "Chirality (Handedness) Measurement"
    question = (
        "Does the Merkaba vortex spin clockwise or counterclockwise? "
        "Measure the z-component of angular momentum at each step. "
        "A true vortex has consistent chirality."
    )
    reference = "Vortex cosmology, spinor structure"
    level = Standard
    tolerance = 0.045

    commentary = (
        "CHIRALITY AND SPIN: "
        "If the traversal has consistent chirality, it means "
        "the Merkaba spins in a preferred direction. "
        "Physical implications: Positive chirality = counterclockwise vortex. "
        "Negative chirality = clockwise vortex. Zero chirality = no vortex structure. "
        "Connection to TetA/TetB: The two tetrahedra may have opposite chirality, "
        "giving the hourglass vortex its bi-directional flow."
    )

    def derivation(self):
        return (
            Derivation()
            .step("CHIRALITY MEASUREMENT:")
            .step("For each step, compute L = r x v")
            .step("Look at the z-component (L_z):")
            .step("L_z > 0: counterclockwise (looking down z-axis)")
            .step("L_z < 0: clockwise")
            .step("L_z = 0: radial motion (no rotation)")
            .equation("Chirality = (positive_z - negative_z) / total_steps")
            .conclude("For random motion: chirality ~ 0. For consistent vortex: |chirality| > 0.")
        )

    def model(self):
        analysis = analyze_angular_momentum(10000)
        return (
            Model()
            .add("Positive L_z steps", analysis['positive_z'])
            .add("Negative L_z steps", analysis['negative_z'])
            .add("Chirality", analysis['chirality'], abs_tol=0.02)
            .add("Chirality (%)", abs(analysis['chirality']) * 100)
        )

    def observations(self):
        # No preferred handedness for independent steps: about 2500 positive and
        # 2500 negative L_z steps (99% within 4%), and chirality 0 within 0.02.
        return (
            Observed()
            .add("Positive L_z steps", 2500)
            .add("Negative L_z steps", 2500)
            .add("Chirality", 0.0)
        )

class VortexVsRandomWalk(Test):
    """
    Does the angular momentum grow like a vortex or random walk?

    Vortex: L ~ N (linear growth)
    Random walk: L ~ sqrt(N) (diffusive growth)
    """
    name = "Vortex vs Random Walk Scaling"
    question = (
        "Does the angular momentum grow linearly (vortex) or as sqrt(N) (random)? "
        "This distinguishes coherent rotation from random motion."
    )
    reference = "Statistical mechanics"
    level = Standard
    tolerance = 0.20

    commentary = (
        "INTERPRETING THE SCALING EXPONENT: "
        "Exponent ~ 0.5: Random walk behavior. The traversal has no coherent rotation. "
        "Exponent ~ 1.0: Vortex behavior. The traversal has consistent rotation. "
        "Intermediate values suggest partial coherence: "
        "The traversal may have vortex structure on some scales but randomness on others."
    )

    def derivation(self):
        return (
            Derivation()
            .step("SCALING ANALYSIS:")
            .step("Measure |L| at different N (number of steps):")
            .step("Random walk: |L| ~ sqrt(N), exponent ~ 0.5")
            .step("Coherent vortex: |L| ~ N, exponent ~ 1.0")
            .equation("exponent = log(L2/L1) / log(N2/N1)")
            .conclude("Intermediate exponent (0.5 to 1.0) suggests partial coherence.")
        )

    def model(self):
        # Measure L at different N values
        N_values = [100, 500, 1000, 5000, 10000]
        L_magnitudes = []

        for N in N_values:
            analysis = analyze_angular_momentum(N)
            L_magnitudes.append(analysis['L_final_magnitude'])

        # Fit exponent
        if len(L_magnitudes) >= 2 and L_magnitudes[0] > 0 and L_magnitudes[-1] > 0:
            exponent = math.log(L_magnitudes[-1] / L_magnitudes[0]) / math.log(N_values[-1] / N_values[0])
        else:
            exponent = 0

        return (
            Model()
            .add("N=100 L magnitude", L_magnitudes[0])
            .add("N=10000 L magnitude", L_magnitudes[4])
            .add("Scaling exponent", exponent, abs_tol=0.35)
        )

    def observations(self):
        # Random walk: |L| ~ N^0.5. A vortex: |L| ~ N^1. The exponent here is a
        # two-point estimate (N = 100 and 10,000), which scatters between 0.15
        # and 0.85 for random sequences, so it is checked against 0.5 within
        # 0.35; an exponent near 1 fails.
        return Observed().add("Scaling exponent", 0.5)

# =============================================================================
# RUN ALL TESTS
# =============================================================================

def run_all():
    """Run all vortex angular momentum tests."""
    return run_tests(
        "Vortex Angular Momentum",
        "Tests for angular momentum properties of the Merkaba vortex",
        [
            AngularMomentumAccumulation,
            ChiralityMeasurement,
            VortexVsRandomWalk,
        ]
    )


if __name__ == "__main__":
    run_all()
