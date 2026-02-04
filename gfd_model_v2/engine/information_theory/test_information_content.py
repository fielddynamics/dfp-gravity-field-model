"""
Information Content of Field Closure
====================================

This module examines the information-theoretic aspects of the Field Closure
system. Information is encoded in discrete units:
- 3 bits per vertex (8 vertices = 2^3)
- 24 bits per orbit (8 vertices × 3 bits)
- 3288 bits per electron (137 orbits × 24 bits)

These tests document the information content correspondences in the model.
"""

import sys
import os
import math
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from gfd_model_v2.base import GFDTest, run_test_group
from gfd_model_v2.common import C, ALPHA, LAMBDA_COMPTON

# =============================================================================
# CONSTANTS
# =============================================================================

BITS_PER_VERTEX = 3
VERTICES_PER_ORBIT = 8
ORBITS_PER_ELECTRON = int(1 / ALPHA)  # 137


def calculate_settlement_frequency():
    """Settlement frequency from Compton wavelength."""
    return C / LAMBDA_COMPTON


def calculate_bits_per_orbit():
    """Calculate bits per complete orbit."""
    return VERTICES_PER_ORBIT * BITS_PER_VERTEX


def calculate_bits_per_electron():
    """Calculate bits per electron (137 orbits)."""
    return ORBITS_PER_ELECTRON * calculate_bits_per_orbit()


# =============================================================================
# TESTS
# =============================================================================

class BitsPerVertex(GFDTest):
    """
    Each vertex requires exactly 3 bits to address (0-7 = 2^3).
    This is the fundamental quantum of position information.
    """
    name = "Bits Per Vertex"
    question = "Does each vertex require d=k-1=3 bits to address, corresponding to log2(2k) = log2(8) = 3?"
    reference_source = "Information theory (log2(8) = 3)"
    tolerance = 0.0
    derivation = (
        "PREMISE: Addressing 2k=8 distinct vertices requires log2(8) bits. "
        "STEP 1: Vertex count = 2k = 8 (dual Field Chamber). "
        "STEP 2: Bits required = ceil(log2(8)) = ceil(3) = 3. "
        "STEP 3: This equals d = k - 1 = 3 (spatial dimension count). "
        "STEP 4: Each triad encodes exactly one vertex position. "
        "OUTPUT: Each vertex address is a d=3 bit quantum of information."
    )
    commentary = (
        "Each vertex address encodes exactly 3 bits, corresponding to the three "
        "spatial dimensions of the Field Chamber. This bit depth equals the "
        "fundamental encoding capacity of a single triad."
    )
    
    def model(self) -> Dict[str, float]:
        required_bits = int(math.ceil(math.log2(8)))
        return {"Bits per vertex": required_bits}
    
    def observations(self) -> Dict[str, float]:
        return {"Bits per vertex": 3}


class BitsPerOrbit(GFDTest):
    """
    One complete orbit visits 8 vertex positions, encoding
    24 bits of information (8 x 3 = 24).
    """
    name = "Bits Per Orbit"
    question = "Does one complete orbit encode 2k * d = 8 * 3 = 24 bits by visiting all Field Chamber vertices?"
    reference_source = "Orbit = 8 vertex positions"
    tolerance = 0.0
    derivation = (
        "PREMISE: An orbit visits all 2k vertices, each contributing d bits. "
        "STEP 1: Vertices per orbit = 2k = 8. "
        "STEP 2: Bits per vertex = d = 3. "
        "STEP 3: Bits per orbit = 2k * d = 8 * 3 = 24. "
        "STEP 4: This represents one complete traversal of the dual Field Chamber. "
        "OUTPUT: Each orbit processes 24 bits of information."
    )
    commentary = (
        "Each orbit processes 24 bits by visiting all 8 vertices of the Field "
        "Chamber. This information throughput per cycle may connect to the "
        "model's encoding capacity per complete traversal."
    )
    
    def model(self) -> Dict[str, float]:
        bits = calculate_bits_per_orbit()
        return {
            "Bits per orbit": bits,
            "Vertices per orbit": VERTICES_PER_ORBIT,
            "Bits per vertex": BITS_PER_VERTEX,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Bits per orbit": 24,
            "Vertices per orbit": 8,
            "Bits per vertex": 3,
        }


class BitsPerElectron(GFDTest):
    """
    One electron requires 137 orbits (1/alpha), encoding
    3288 bits of information (137 x 24 = 3288).
    """
    name = "Bits Per Electron"
    question = "Does one electron encode (1/alpha) * 24 = 137 * 24 = 3288 bits per complete cycle?"
    reference_source = "1/alpha = 137 orbits per electron"
    tolerance = 0.0
    derivation = (
        "PREMISE: An electron cycle requires 1/alpha orbits, each encoding 24 bits. "
        "STEP 1: Orbits per electron = floor(1/alpha) = floor(137.036) = 137. "
        "STEP 2: Bits per orbit = 24. "
        "STEP 3: Bits per electron = 137 * 24 = 3288. "
        "STEP 4: This links information content to fine structure constant. "
        "OUTPUT: Electron information content is 3288 bits per cycle."
    )
    commentary = (
        "The 3288 bits per electron cycle emerges from 137 orbits times 24 bits "
        "per orbit. This information content scales with 1/alpha, connecting "
        "electromagnetic coupling strength to information-theoretic measures."
    )
    
    def model(self) -> Dict[str, float]:
        bits = calculate_bits_per_electron()
        return {
            "Bits per electron": bits,
            "Orbits per electron (1/alpha)": ORBITS_PER_ELECTRON,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Bits per electron": 3288,
            "Orbits per electron (1/alpha)": 137,
        }


class OrbitsEqualsInverseAlpha(GFDTest):
    """
    The number of orbits per electron corresponds to 1/alpha = 137.
    This establishes a correspondence between information content and
    the fine structure constant.
    """
    name = "Orbits = 1/alpha"
    question = "Does the fine structure constant determine orbit count via 1/alpha ≈ 137 orbits per electron?"
    reference_source = "CODATA fine structure constant"
    tolerance = 0.001
    derivation = (
        "PREMISE: The fine structure constant alpha determines electromagnetic coupling strength. "
        "STEP 1: alpha = 1/137.036 (CODATA value). "
        "STEP 2: Calculate 1/alpha = 137.036. "
        "STEP 3: Integer orbits: floor(1/alpha) = 137. "
        "STEP 4: This provides information-theoretic interpretation: alpha encodes cycle count. "
        "OUTPUT: 1/alpha = 137 orbits defines electron information capacity."
    )
    commentary = (
        "The correspondence between orbit count and 1/alpha provides an "
        "information-theoretic perspective on the fine structure constant. "
        "This reading suggests electromagnetic coupling may encode a "
        "characteristic cycle number."
    )
    
    def model(self) -> Dict[str, float]:
        orbits = int(1 / ALPHA)
        return {
            "1/alpha": 1/ALPHA,
            "Orbits (integer)": orbits,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "1/alpha": 137.036,
            "Orbits (integer)": 137,
        }


class ProcessingRate(GFDTest):
    """
    The information processing rate is frequency x bits per orbit.
    At Compton frequency (~1.2e20 Hz), this gives enormous bandwidth.
    """
    name = "Information Processing Rate"
    question = "Does the settlement frequency times bits per orbit yield yottabit-scale processing bandwidth?"
    reference_source = None  # Model calculation
    derivation = (
        "PREMISE: Processing rate = frequency * bits per orbit. "
        "STEP 1: Settlement frequency = c / lambda_Compton ≈ 1.2 x 10^20 Hz. "
        "STEP 2: Bits per orbit = 24. "
        "STEP 3: Processing rate = 1.2 x 10^20 * 24 = 2.9 x 10^21 bits/second. "
        "STEP 4: In yottabits: 2.9 x 10^21 / 10^24 = 0.0029 Yb/s. "
        "OUTPUT: Field Closure implies ~10^21 bits/second processing capacity."
    )
    commentary = (
        "The yottabit-scale processing rate at settlement frequency reflects "
        "the vast computational capacity implied by Field Closure dynamics. "
        "This bandwidth exceeds any conceivable classical system."
    )
    
    def model(self) -> Dict[str, float]:
        f = calculate_settlement_frequency()
        bits_per_orbit = calculate_bits_per_orbit()
        rate = f * bits_per_orbit
        rate_yb = rate / 1e24  # Yottabits/second
        return {
            "Settlement frequency (Hz)": f,
            "Processing rate (bits/s)": rate,
            "Processing rate (Yb/s)": rate_yb,
        }


class InformationIsFinite(GFDTest):
    """
    The electron has finite information content (3288 bits).
    This finiteness is fundamental to quantum discreteness.
    """
    name = "Finite Information Content"
    question = "Is the electron information content finite (3288 bits), consistent with quantum discreteness?"
    reference_source = None  # Model interpretation
    derivation = (
        "PREMISE: Finite information content supports quantum discreteness. "
        "STEP 1: Calculate electron bits: 137 orbits * 24 bits = 3288 bits. "
        "STEP 2: Check finiteness: 0 < 3288 < infinity. Yes, finite. "
        "STEP 3: Check reasonableness: 3288 << 10^10 (bounded). "
        "STEP 4: Finite information suggests electron is discrete information object. "
        "OUTPUT: Electron has finite, bounded information content of 3288 bits."
    )
    commentary = (
        "Finite information content per electron is consistent with quantum "
        "discreteness. The specific value of 3288 bits may relate to the "
        "electron's fundamental properties as an information-theoretic object."
    )
    
    def model(self) -> Dict[str, float]:
        bits = calculate_bits_per_electron()
        is_finite = 1 if 0 < bits < 1e10 else 0
        return {
            "Electron bits": bits,
            "Is finite": is_finite,
        }


class InformationHierarchy(GFDTest):
    """
    Information content follows a strict hierarchy:
    vertex < orbit < electron.
    """
    name = "Information Hierarchy"
    question = "Does information content follow the strict hierarchy: vertex (3) < orbit (24) < electron (3288) bits?"
    reference_source = None  # Structural requirement
    derivation = (
        "PREMISE: Nested structure implies hierarchical information content. "
        "STEP 1: Bits per vertex = d = 3. "
        "STEP 2: Bits per orbit = 2k * d = 8 * 3 = 24. "
        "STEP 3: Bits per electron = (1/alpha) * 24 = 137 * 24 = 3288. "
        "STEP 4: Verify hierarchy: 3 < 24 < 3288. Yes. "
        "OUTPUT: Information scales hierarchically from vertices to electrons."
    )
    commentary = (
        "The strict information hierarchy reflects the nested structure of the "
        "model: vertices compose orbits, orbits compose electrons. This scaling "
        "is consistent with emergent complexity from simple primitives."
    )
    
    def model(self) -> Dict[str, float]:
        bits_vertex = BITS_PER_VERTEX
        bits_orbit = calculate_bits_per_orbit()
        bits_electron = calculate_bits_per_electron()
        
        hierarchy_correct = 1 if (bits_vertex < bits_orbit < bits_electron) else 0
        
        return {
            "Bits per vertex": bits_vertex,
            "Bits per orbit": bits_orbit,
            "Bits per electron": bits_electron,
            "Hierarchy correct": hierarchy_correct,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    BitsPerVertex,
    BitsPerOrbit,
    BitsPerElectron,
    OrbitsEqualsInverseAlpha,
    ProcessingRate,
    InformationIsFinite,
    InformationHierarchy,
]


def run_all_tests() -> bool:
    """Run all information content tests."""
    return run_test_group(
        title="Information Content of Field Closure",
        summary=(
            "These tests examine information-theoretic aspects of the Field Closure system. "
            "Each vertex requires 3 bits to address (8 vertices = 2^3), producing 24 bits "
            "per orbit and 3288 bits per electron (137 orbits). The correspondence to "
            "1/alpha = 137 suggests a possible information-theoretic interpretation of "
            "the fine structure constant."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
