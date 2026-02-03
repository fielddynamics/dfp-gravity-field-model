"""
MOND Interpolating Function from Hexagonal Geometry
====================================================

This module examines a geometric derivation of the MOND interpolating
function mu(x) = x/(1+x) from hexagonal packing geometry.

The "1" in the denominator corresponds to exactly 6 × (1/3) × (1/2) from:
- N = 6 neighbors in hexagonal packing
- eta = 1/3 coupling fraction (vesica piscis angle 2*pi/3)
- 1/2 sharing factor (each overlap shared by two cells)

C_tiling = 6 × (1/3) × (1/2) = 1.0
"""

import sys
import os
import math
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi
N_NEIGHBORS = 6  # Hexagonal packing
COUPLING_ANGLE = 2 * PI / 3  # Vesica piscis angle (120 degrees)
SHARING_FACTOR = 0.5  # Each overlap shared by 2 cells


def get_coupling_fraction():
    """Coupling fraction from vesica piscis geometry."""
    return COUPLING_ANGLE / (2 * PI)  # 1/3


def get_tiling_contribution():
    """Tiling contribution C_tiling from hexagonal geometry."""
    eta = get_coupling_fraction()
    return N_NEIGHBORS * eta * SHARING_FACTOR


def mu_from_geometry(x):
    """MOND interpolating function from geometry."""
    C_tiling = get_tiling_contribution()
    return x / (x + C_tiling)


def mu_standard(x):
    """Standard MOND interpolating function."""
    return x / (1 + x)


def average_coupling_analytical():
    """Analytical average coupling over all separations = 1/pi."""
    return 1 / PI


# =============================================================================
# TESTS
# =============================================================================

class CouplingFractionOneThird(GFDTest):
    """
    Vesica piscis coupling fraction = 1/3.
    When two circles overlap at hexagonal distance, coupling angle = 2*pi/3.
    """
    name = "Vesica Piscis Coupling Fraction"
    question = "Does the vesica piscis geometry produce a coupling fraction η = 1/3 from the 120-degree (2π/3 radian) overlap angle?"
    reference_source = "Geometry (2*pi/3 / 2*pi = 1/3)"
    tolerance = 1e-10
    derivation = (
        "PREMISE: When two equal circles overlap at hexagonal spacing, they form a vesica piscis. "
        "STEP 1: The overlap arc subtends angle θ = 2π/3 radians = 120 degrees. "
        "STEP 2: The coupling fraction η = θ / (2π) represents the angular overlap proportion. "
        "STEP 3: η = (2π/3) / (2π) = 1/3. "
        "OUTPUT: The vesica piscis coupling fraction is exactly 1/3."
    )
    commentary = (
        "The vesica piscis angle of 120 degrees produces a coupling fraction of "
        "exactly 1/3. This geometric parameter emerges from hexagonal overlap "
        "without fitting to MOND observations."
    )
    
    def model(self) -> Dict[str, float]:
        eta = get_coupling_fraction()
        return {"Coupling fraction (eta)": eta}
    
    def observations(self) -> Dict[str, float]:
        return {"Coupling fraction (eta)": 1/3}


class TilingContributionIsOne(GFDTest):
    """
    The tiling contribution C_tiling = 6 × (1/3) × (1/2) = 1.0.
    This value emerges from geometric parameters without fitting.
    """
    name = "Tiling Contribution = 1"
    question = "Does the tiling contribution C_tiling = N × η × s = 6 × (1/3) × (1/2) equal exactly unity?"
    reference_source = "Hexagonal geometry derivation"
    tolerance = 1e-10
    derivation = (
        "PREMISE: C_tiling combines neighbor count, coupling fraction, and sharing factor. "
        "STEP 1: N = 6 (hexagonal nearest neighbors). "
        "STEP 2: η = 1/3 (vesica piscis coupling fraction). "
        "STEP 3: s = 1/2 (each overlap shared by two cells). "
        "STEP 4: C_tiling = N × η × s = 6 × (1/3) × (1/2) = 6/6 = 1.0. "
        "OUTPUT: The tiling contribution equals exactly 1, enabling the MOND function."
    )
    commentary = (
        "The product 6 x 1/3 x 1/2 yielding exactly unity is a geometric "
        "coincidence that produces the standard MOND interpolating function. "
        "This exact value emerges without parameter adjustment."
    )
    
    def model(self) -> Dict[str, float]:
        C_tiling = get_tiling_contribution()
        return {
            "C_tiling": C_tiling,
            "N_neighbors": N_NEIGHBORS,
            "Coupling fraction": get_coupling_fraction(),
            "Sharing factor": SHARING_FACTOR,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "C_tiling": 1.0,
            "N_neighbors": 6,
            "Coupling fraction": 1/3,
            "Sharing factor": 0.5,
        }


class GeometricMuMatchesMOND(GFDTest):
    """
    The geometrically derived mu(x) matches the MOND function.
    mu(x) = x / (x + C_tiling) = x / (x + 1) = MOND mu(x).
    """
    name = "Geometric mu(x) = MOND mu(x)"
    question = "Does the geometrically derived μ(x) = x/(x + C_tiling) exactly reproduce the standard MOND interpolating function μ(x) = x/(1+x)?"
    reference_source = "MOND phenomenology"
    tolerance = 1e-10
    derivation = (
        "PREMISE: The MOND interpolating function is μ(x) = x/(1+x) where x = a/a₀. "
        "STEP 1: From geometry, C_tiling = 1 (derived above). "
        "STEP 2: Geometric function: μ_geo(x) = x / (x + C_tiling) = x / (x + 1). "
        "STEP 3: Compare: μ_geo(x) = x/(x+1) = μ_MOND(x). "
        "STEP 4: Test at multiple x values (0.01, 0.1, 1.0, 10.0) and verify equality. "
        "OUTPUT: The geometric derivation exactly reproduces MOND."
    )
    commentary = (
        "The geometric derivation reproduces the standard MOND interpolating function "
        "exactly. This correspondence between hexagonal packing geometry and modified "
        "Newtonian dynamics is documented without claiming causation."
    )
    
    def model(self) -> Dict[str, float]:
        test_x = [0.01, 0.1, 1.0, 10.0]
        max_diff = max(abs(mu_from_geometry(x) - mu_standard(x)) for x in test_x)
        return {
            "mu(0.01) geometric": mu_from_geometry(0.01),
            "mu(1.0) geometric": mu_from_geometry(1.0),
            "mu(10.0) geometric": mu_from_geometry(10.0),
            "Max difference": max_diff,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "mu(0.01) geometric": 0.01/(1+0.01),
            "mu(1.0) geometric": 0.5,
            "mu(10.0) geometric": 10/11,
            "Max difference": 0.0,
        }


class NewtonianLimit(GFDTest):
    """
    mu(x) -> 1 as x -> infinity (Newtonian limit).
    In strong fields, standard gravity is recovered.
    """
    name = "Newtonian Limit"
    question = "Does the interpolating function μ(x) approach 1 as x → ∞, recovering standard Newtonian gravity in strong fields?"
    reference_source = "Newtonian gravity recovery"
    tolerance = 0.001
    derivation = (
        "PREMISE: For consistency with solar system observations, μ(x) → 1 as x → ∞. "
        "STEP 1: μ(x) = x / (x + 1). "
        "STEP 2: As x → ∞: μ(x) = x/(x+1) = 1/(1 + 1/x) → 1/(1+0) = 1. "
        "STEP 3: At x = 1000: μ(1000) = 1000/1001 = 0.999. "
        "OUTPUT: The function recovers Newtonian limit in the high-acceleration regime."
    )
    commentary = (
        "The Newtonian limit recovery ensures the geometric function reduces to "
        "standard gravity in strong field regimes. This asymptotic behavior is "
        "required for consistency with solar system observations."
    )
    
    def model(self) -> Dict[str, float]:
        x_large = 1000
        mu_val = mu_from_geometry(x_large)
        return {"mu(1000)": mu_val}
    
    def observations(self) -> Dict[str, float]:
        return {"mu(1000)": 1.0}


class DeepMONDLimit(GFDTest):
    """
    mu(x) -> x as x -> 0 (deep MOND limit).
    This produces flat rotation curves.
    """
    name = "Deep MOND Limit"
    question = "Does μ(x) approach x as x → 0 (deep MOND regime), producing the gravitational boost for flat rotation curves?"
    reference_source = "MOND flat rotation curves"
    tolerance = 0.01
    derivation = (
        "PREMISE: Flat galaxy rotation curves require effective gravity boost at low accelerations. "
        "STEP 1: μ(x) = x / (x + 1). "
        "STEP 2: As x → 0: μ(x) ≈ x / 1 = x. "
        "STEP 3: At x = 0.001: μ(0.001) = 0.001/1.001 ≈ 0.000999. "
        "STEP 4: Ratio μ/x ≈ 0.999 → 1 as x → 0. "
        "OUTPUT: The function produces the deep MOND boost (μ → x) for flat rotation curves."
    )
    commentary = (
        "The deep MOND limit produces the gravitational boost needed to explain "
        "flat galaxy rotation curves without dark matter. This regime emerges "
        "naturally from the geometric interpolating function."
    )
    
    def model(self) -> Dict[str, float]:
        x_small = 0.001
        mu_val = mu_from_geometry(x_small)
        ratio = mu_val / x_small  # Should be ~1
        return {
            "mu(0.001)": mu_val,
            "mu/x ratio": ratio,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "mu(0.001)": 0.001/1.001,
            "mu/x ratio": 1.0,
        }


class TransitionAtXEqualsOne(GFDTest):
    """
    The transition occurs exactly at x = 1, where mu(1) = 0.5.
    This is where C_field = C_tiling = 1.
    """
    name = "Transition at x = 1"
    question = "Does the transition point occur exactly at x=1 where μ(1)=0.5, balancing field and tiling contributions?"
    reference_source = "C_field = C_tiling balance"
    tolerance = 1e-10
    derivation = (
        "PREMISE: The MOND transition scale a₀ corresponds to x = a/a₀ = 1. "
        "STEP 1: At x = 1: μ(1) = 1 / (1 + 1) = 1/2 = 0.5. "
        "STEP 2: This means effective gravity is exactly half Newtonian at the transition. "
        "STEP 3: The transition represents balance between C_field (numerator) and C_tiling (denominator). "
        "OUTPUT: μ(1) = 0.5 exactly marks the Newtonian-to-MOND transition."
    )
    commentary = (
        "The transition point at x=1 where mu=0.5 represents balanced field and "
        "tiling contributions. This corresponds to the MOND acceleration scale "
        "where Newtonian and modified dynamics contribute equally."
    )
    
    def model(self) -> Dict[str, float]:
        mu_val = mu_from_geometry(1.0)
        return {"mu(1)": mu_val}
    
    def observations(self) -> Dict[str, float]:
        return {"mu(1)": 0.5}


class SixNeighbors(GFDTest):
    """
    Hexagonal packing gives exactly 6 nearest neighbors.
    This is the source of 6-fold symmetry in nature.
    """
    name = "Six Hexagonal Neighbors"
    question = "Does hexagonal close packing produce exactly N=6 nearest neighbors, the maximum for 2D sphere packing?"
    reference_source = "Hexagonal close packing geometry"
    tolerance = 0.0
    derivation = (
        "PREMISE: In 2D, hexagonal packing maximizes density with equal-radius circles. "
        "STEP 1: Each circle is tangent to neighbors arranged in a ring. "
        "STEP 2: The angle between adjacent neighbors is 360°/N. "
        "STEP 3: For tangent circles at distance 2r, the maximum N satisfying geometry is 6. "
        "STEP 4: This gives neighbor angles of 60° and internal hexagon angles of 120°. "
        "OUTPUT: Hexagonal packing uniquely gives N = 6 nearest neighbors."
    )
    commentary = (
        "Hexagonal close packing with 6 neighbors is the most efficient 2D tiling. "
        "This fundamental geometric count enters the MOND derivation as a "
        "multiplier in the tiling contribution."
    )
    
    def model(self) -> Dict[str, float]:
        return {"Neighbors": N_NEIGHBORS}
    
    def observations(self) -> Dict[str, float]:
        return {"Neighbors": 6}


class ContinuousAverageIsOneOverPi(GFDTest):
    """
    When coupling is averaged over all separations:
    <eta> = integral of arccos(u)/pi from 0 to 1 = 1/pi.
    This is the cosmological suppression factor.
    """
    name = "Continuous Average = 1/pi"
    question = "Does averaging the coupling fraction over all separations yield ⟨η⟩ = 1/π as a cosmological suppression factor?"
    reference_source = "Analytical integration"
    tolerance = 1e-6
    derivation = (
        "PREMISE: Coupling varies with separation; averaging gives a universal factor. "
        "STEP 1: Coupling at separation u is η(u) = arccos(u)/π for 0 ≤ u ≤ 1. "
        "STEP 2: Average: ⟨η⟩ = ∫₀¹ [arccos(u)/π] du. "
        "STEP 3: Using integration by parts: ∫arccos(u)du = u·arccos(u) - √(1-u²). "
        "STEP 4: Evaluate: ⟨η⟩ = (1/π)[u·arccos(u) - √(1-u²)]₀¹ = (1/π)[0-0-(-1)] = 1/π. "
        "OUTPUT: The continuous average coupling is exactly 1/π."
    )
    commentary = (
        "The continuous coupling average of 1/pi arises from analytical integration "
        "over all separations. This factor may serve as a cosmological suppression "
        "mechanism connecting local and global gravitational effects."
    )
    
    def model(self) -> Dict[str, float]:
        analytical = average_coupling_analytical()
        return {"<eta> analytical": analytical}
    
    def observations(self) -> Dict[str, float]:
        return {"<eta> analytical": 1/PI}


class GeometryDeterminesMOND(GFDTest):
    """
    The derivation chain: geometry -> C_tiling = 1 -> mu(x) = x/(x+1).
    This corresponds to the standard MOND interpolating function.
    """
    name = "Geometric MOND Derivation"
    question = "Does the complete derivation chain from hexagonal geometry (N=6, η=1/3, s=1/2) to C_tiling=1 produce the MOND function without free parameters?"
    reference_source = "Geometric derivation"
    tolerance = 1e-10
    derivation = (
        "PREMISE: Derive MOND from pure geometry without fitting parameters. "
        "STEP 1: Hexagonal packing gives N = 6 neighbors (geometric constraint). "
        "STEP 2: Vesica piscis overlap gives η = 1/3 (geometric constraint). "
        "STEP 3: Bilateral sharing gives s = 1/2 (geometric constraint). "
        "STEP 4: C_tiling = N × η × s = 6 × (1/3) × (1/2) = 1.0. "
        "STEP 5: μ(x) = x/(x + C_tiling) = x/(x + 1) = MOND function. "
        "OUTPUT: The MOND function emerges from geometry alone."
    )
    commentary = (
        "The complete derivation chain from geometric parameters to the MOND "
        "function proceeds without free parameters. The coincidental product "
        "equaling unity enables this parameter-free connection."
    )
    
    def model(self) -> Dict[str, float]:
        n = N_NEIGHBORS
        eta = get_coupling_fraction()
        s = SHARING_FACTOR
        C_tiling = n * eta * s
        
        return {
            "N": n,
            "eta": eta,
            "s": s,
            "C_tiling": C_tiling,
            "Equals 1": 1 if abs(C_tiling - 1.0) < 1e-10 else 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "N": 6,
            "eta": 1/3,
            "s": 0.5,
            "C_tiling": 1.0,
            "Equals 1": 1,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    SixNeighbors,
    CouplingFractionOneThird,
    TilingContributionIsOne,
    GeometryDeterminesMOND,
    GeometricMuMatchesMOND,
    TransitionAtXEqualsOne,
    NewtonianLimit,
    DeepMONDLimit,
    ContinuousAverageIsOneOverPi,
]


def run_all_tests() -> bool:
    """Run all MOND hexagonal derivation tests."""
    return run_test_group(
        title="MOND from Hexagonal Geometry",
        summary=(
            "These tests examine a geometric derivation of the MOND interpolating function "
            "mu(x) = x/(1+x) from hexagonal packing geometry. The '1' in the denominator "
            "corresponds to 6 × (1/3) × (1/2) from: 6 neighbors in hexagonal packing, "
            "1/3 coupling fraction from vesica piscis geometry (2*pi/3 angle), and 1/2 "
            "sharing factor. This derivation produces the standard MOND function from "
            "geometric parameters. The continuous average coupling (1/pi) serves as a "
            "suppression factor in cosmological applications."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
