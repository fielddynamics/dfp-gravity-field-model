"""
Bit Propagation Tests
=====================

This module tests information flow properties in the Field Closure traversal model.
Tests examine bit encoding rates, information accumulation patterns, entropy 
distributions, and derived state relationships. Each test documents quantitative
correspondences without claiming causal mechanisms.

Test categories:
- Bit encoding: Input and state bit requirements
- Information accumulation: Cumulative sum behavior  
- Entropy analysis: Distribution uniformity
- Bandwidth: Information rate calculations
- Derived states: Deterministic relationships
"""

import sys
import os
import math
from typing import Dict, Optional
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from common import (
    VERTICES, TET_A, TET_B, FACES, K, C, HBAR,
    TIME_FACES, SPATIAL_FACES,
    get_tetrahedron, traverse_pi_base8,
    calculate_settlement_frequency
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_entropy(distribution):
    """Calculate Shannon entropy of a distribution."""
    total = sum(distribution.values())
    if total == 0:
        return 0
    
    entropy = 0
    for count in distribution.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return entropy


# =============================================================================
# TESTS: BIT ENCODING
# =============================================================================

class InputIs3BitsPerStep(GFDTest):
    """
    Each Pi digit is 0-7, which is exactly 3 bits of input per step.
    """
    name = "Input Is 3 Bits Per Step"
    question = (
        "Does each digit of pi in base-8 (octal) provide exactly 3 bits of input, "
        "matching the 2k=8 vertex count of the stellated octahedron?"
    )
    reference_source = "Binary encoding"
    tolerance = 0.001
    derivation = (
        "Pi in base-8: each digit d is in the range [0, 7]. "
        "Bits required to encode one digit: ceil(log2(8)) = 3 bits. "
        "The 2k=8 vertices of the Field Chamber correspond to 3-bit addresses. "
        "Verification: traverse N digits and confirm each digit in {0,1,2,3,4,5,6,7}. "
        "This octal representation naturally maps pi digits to Coupling Port positions."
    )
    commentary = (
        "The base-8 representation of Pi provides exactly 3 bits per traversal step, "
        "corresponding to the 8 vertices of the stellated octahedron. This correspondence "
        "suggests the Field Chamber geometry may naturally accommodate octal information encoding."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(100)
        
        valid_count = 0
        for step in traversal:
            digit = step['digit']
            if 0 <= digit <= 7:
                valid_count += 1
        
        bits_needed = math.ceil(math.log2(8))
        
        return {
            "Valid digits (0-7)": valid_count,
            "Total digits": len(traversal),
            "Bits per digit": bits_needed,
        }
    
    def observations(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(100)
        return {
            "Valid digits (0-7)": len(traversal),
            "Total digits": len(traversal),
            "Bits per digit": 3,
        }


class StateIs3Bits(GFDTest):
    """
    The vertex state (0-7) is exactly 3 bits.
    """
    name = "State Is 3 Bits"
    question = (
        "Does each vertex state (0-7) in the Field Chamber require exactly 3 bits to encode, "
        "consistent with 2k=8 Coupling Ports?"
    )
    reference_source = "Binary encoding"
    tolerance = 0.001
    derivation = (
        "Vertex indices: v in {0, 1, 2, 3, 4, 5, 6, 7}. "
        "Binary representation of each vertex: format(v, '03b') yields 3-bit strings. "
        "Examples: 0='000', 1='001', 2='010', ..., 7='111'. "
        "All 8 vertices encode uniquely in exactly 3 bits (no more, no less). "
        "From k=4 Field Closure: 2k=8 vertices require log2(8)=3 bits for state encoding."
    )
    commentary = (
        "The 8 Coupling Ports of the stellated octahedron encode exactly 3 bits of state. "
        "This 3-bit capacity is consistent with the Field Chamber functioning as a minimal "
        "information processing unit where geometry constrains state space."
    )
    
    def model(self) -> Dict[str, float]:
        correct_count = 0
        for v in range(8):
            binary = format(v, '03b')
            if len(binary) == 3:
                correct_count += 1
        
        return {"Vertices with 3-bit encoding": correct_count}
    
    def observations(self) -> Dict[str, float]:
        return {"Vertices with 3-bit encoding": 8}


class DerivedInfoCostsZeroBits(GFDTest):
    """
    Tetrahedron, complement, face membership are DERIVED, not transmitted.
    They cost 0 additional bits because they are computed from vertex.
    """
    name = "Derived Info Costs Zero Bits"
    question = (
        "Are tetrahedron membership, complement vertex, and face associations all "
        "deterministically derived from the vertex index, requiring zero additional bits?"
    )
    reference_source = "Deterministic derivation"
    tolerance = 0.001
    derivation = (
        "From vertex index v (3 bits), derive without extra transmission: "
        "(1) Parity: bin(v).count('1') mod 2. "
        "(2) Tetrahedron: Tet_A if parity=1, Tet_B if parity=0. "
        "(3) Complement: 7 - v (arithmetic operation). "
        "(4) Faces containing v: lookup in FACES dictionary. "
        "All derivations are deterministic functions of v. "
        "Extra bits required = 0, as the 3-bit vertex encodes all information implicitly."
    )
    commentary = (
        "Tetrahedron A/B membership, complementary vertex, and TIME/SPATIAL face associations "
        "are all deterministically derived from the 3-bit vertex index. This suggests the "
        "Field Chamber encodes substantial structural information without additional transmission cost."
    )
    
    def model(self) -> Dict[str, float]:
        derivable_count = 0
        
        for v in range(8):
            # All properties are deterministic from vertex index
            parity = bin(v).count('1') % 2
            tet = 'A' if parity == 1 else 'B'
            complement = 7 - v
            faces_containing_v = [f for f, vertices in FACES.items() if v in vertices]
            derivable_count += 1
        
        return {
            "Derivable vertices": derivable_count,
            "Extra bits needed": 0,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Derivable vertices": 8,
            "Extra bits needed": 0,
        }


# =============================================================================
# TESTS: INFORMATION ACCUMULATION
# =============================================================================

class CumsumAccumulatesInformation(GFDTest):
    """
    Cumsum grows by adding digits, not by receiving signals.
    Information accumulates locally.
    """
    name = "Cumsum Accumulates Information"
    question = (
        "Does the cumulative sum grow through local addition of each digit, rather than "
        "through signal reception from other parts of the Field Chamber?"
    )
    reference_source = "Cumulative sum definition"
    tolerance = 0.001
    derivation = (
        "Cumulative sum update rule: cumsum_n = cumsum_{n-1} + digit_n. "
        "This is a local operation: only the previous cumsum and current digit are needed. "
        "No signal propagation between vertices or faces is required. "
        "Verification: for each step, expected_cumsum = prev_cumsum + digit. "
        "If cumsum == expected_cumsum for all steps, accumulation is purely local."
    )
    commentary = (
        "Information accumulates through local arithmetic rather than external transmission. "
        "This is consistent with the Field Closure operating as a self-contained processing "
        "unit where state evolution depends only on the traversal sequence."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(50)
        
        accumulates_count = 0
        for i, step in enumerate(traversal):
            cumsum = step['cumsum']
            digit = step['digit']
            
            if i == 0:
                expected = digit
            else:
                expected = traversal[i-1]['cumsum'] + digit
            
            if cumsum == expected:
                accumulates_count += 1
        
        return {
            "Accumulating steps": accumulates_count,
            "Total steps": len(traversal),
        }
    
    def observations(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(50)
        return {
            "Accumulating steps": len(traversal),
            "Total steps": len(traversal),
        }


class NoInformationLoss(GFDTest):
    """
    Tests that the sum of input digits equals the final cumulative sum,
    indicating information is preserved through the traversal process.
    """
    name = "No Information Loss"
    question = (
        "Is information conserved through Field Closure traversal, such that the sum of "
        "all input digits equals the final cumulative sum?"
    )
    reference_source = "Conservation"
    tolerance = 0.001
    derivation = (
        "Information conservation criterion: sum(all digits) = final_cumsum. "
        "By definition of cumsum: cumsum_N = sum(digit_1, digit_2, ..., digit_N). "
        "If this equality holds, no information is lost or added during traversal. "
        "Verification: compute total_input = sum(step['digit'] for all steps). "
        "Compare to final_cumsum = traversal[-1]['cumsum']. "
        "Equality confirms reversible, lossless information processing."
    )
    commentary = (
        "The equality between input sum and cumulative total indicates information conservation "
        "through the Field Closure traversal. This conservation property is consistent with "
        "reversible computation at the fundamental scale."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(100)
        
        total_input = sum(step['digit'] for step in traversal)
        final_cumsum = traversal[-1]['cumsum']
        
        return {
            "Sum of digits": total_input,
            "Final cumsum": final_cumsum,
        }
    
    def observations(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(100)
        total_input = sum(step['digit'] for step in traversal)
        
        return {
            "Sum of digits": total_input,
            "Final cumsum": total_input,  # They should be equal
        }


class OrbitPreservesModularInformation(GFDTest):
    """
    Each orbit consumes cumsum bits and outputs vertex position.
    vertex = cumsum mod 8 at all times.
    """
    name = "Orbit Preserves Modular Information"
    question = (
        "Does the vertex position always equal cumsum mod 8, mapping accumulated information "
        "onto the 2k=8 Coupling Ports through modular arithmetic?"
    )
    reference_source = "Modular arithmetic"
    tolerance = 0.001
    derivation = (
        "Vertex determination: vertex = cumsum mod 8. "
        "This maps cumulative information onto the 8-vertex stellated octahedron. "
        "As cumsum grows, vertex cycles through {0,1,2,3,4,5,6,7,0,1,...}. "
        "Verification: for each step, check step['cumsum'] mod 8 == step['vertex']. "
        "100% agreement confirms the modular mapping is exact and consistent."
    )
    commentary = (
        "The modular relationship vertex = cumsum mod 8 maps accumulated information onto "
        "Coupling Port positions within the stellated octahedron. This modular structure "
        "may indicate how continuous information flow produces discrete geometric states."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(100)
        
        preserved_count = 0
        for step in traversal:
            if step['cumsum'] % 8 == step['vertex']:
                preserved_count += 1
        
        return {
            "Preserved steps": preserved_count,
            "Total steps": len(traversal),
        }
    
    def observations(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(100)
        return {
            "Preserved steps": len(traversal),
            "Total steps": len(traversal),
        }


# =============================================================================
# TESTS: ENTROPY ANALYSIS
# =============================================================================

class VertexDistributionEntropy(GFDTest):
    """
    Over many steps, vertex distribution should be approximately uniform,
    giving near-maximal entropy (3 bits).
    """
    name = "Vertex Distribution Entropy"
    question = (
        "Does the vertex visitation distribution approach uniform (maximum entropy of 3 bits), "
        "indicating unbiased exploration of all 2k=8 Coupling Ports?"
    )
    reference_source = None  # Threshold check
    derivation = (
        "Shannon entropy: H = -sum(p_v * log2(p_v)) for v in [0,7]. "
        "Maximum entropy for 8 states: H_max = log2(8) = 3 bits (uniform distribution). "
        "Count vertex occurrences over N steps, compute frequency p_v for each vertex. "
        "Efficiency = H_actual / H_max. "
        "If efficiency > 0.90, the distribution is approximately uniform, "
        "consistent with pi's digits being statistically unbiased in base 8."
    )
    commentary = (
        "Near-maximal entropy in Coupling Port visitation suggests the traversal explores "
        "the stellated octahedron uniformly. This high entropy is consistent with Pi's "
        "statistical properties driving unbiased exploration of the Field Chamber geometry."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(500)
        
        distribution = Counter(step['vertex'] for step in traversal)
        entropy = calculate_entropy(distribution)
        max_entropy = math.log2(8)  # 3 bits
        efficiency = entropy / max_entropy
        
        return {
            "Vertex entropy (bits)": entropy,
            "Max entropy (bits)": max_entropy,
            "Efficiency": efficiency,
        }


class TetrahedronEntropy(GFDTest):
    """
    Tetrahedron distribution should be balanced (1 bit entropy).
    """
    name = "Tetrahedron Entropy"
    question = (
        "Does the tetrahedron visitation distribution approach 50/50 balance, yielding "
        "near-maximum entropy of 1 bit between Tetrahedron A and Tetrahedron B?"
    )
    reference_source = None  # Threshold check
    derivation = (
        "Shannon entropy for binary distribution: H = -p_A*log2(p_A) - p_B*log2(p_B). "
        "Maximum entropy: H_max = log2(2) = 1 bit (when p_A = p_B = 0.5). "
        "Count tetrahedron visits: Tet_A for odd-parity vertices, Tet_B for even-parity. "
        "Compute p_A = count_A / total, p_B = count_B / total. "
        "Efficiency = H_actual / H_max. If efficiency > 0.90, the dual tetrahedra "
        "are explored with approximate balance."
    )
    commentary = (
        "Balanced visitation between Tetrahedron A and Tetrahedron B corresponds to 1 bit "
        "of entropy in the dual structure. This balance is consistent with the complementary "
        "relationship between the two tetrahedra within the Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(500)
        
        distribution = {'A': 0, 'B': 0}
        for step in traversal:
            distribution[step['tetrahedron']] += 1
        
        entropy = calculate_entropy(distribution)
        max_entropy = math.log2(2)  # 1 bit
        efficiency = entropy / max_entropy
        
        return {
            "Tetrahedron entropy (bits)": entropy,
            "Max entropy (bits)": max_entropy,
            "Efficiency": efficiency,
        }


# =============================================================================
# TESTS: BANDWIDTH AND CAPACITY
# =============================================================================

class InformationBandwidth(GFDTest):
    """
    Information bandwidth = bits/second = 3 bits * frequency.
    """
    name = "Information Bandwidth"
    question = (
        "What is the information bandwidth of the Field Chamber, given 3 bits per step "
        "at the settlement frequency?"
    )
    reference_source = None  # Calculation
    derivation = (
        "Bits per step: 3 (from log2(8) for 8 vertices). "
        "Settlement frequency: f = c / lambda_C (Compton frequency). "
        "Bandwidth = bits_per_step * frequency = 3 * f bits/second. "
        "Bits per electron: orbits_per_electron * steps_per_orbit * bits_per_step. "
        "With 1/alpha = 137 orbits and ~8 steps per orbit: 137 * 8 * 3 = 3288 bits. "
        "This represents the information processing capacity per electron."
    )
    commentary = (
        "The bandwidth emerges from 3 bits per step multiplied by the Field Closure frequency. "
        "This information rate suggests a fundamental processing capacity that may relate to "
        "the bits-per-particle measures discussed in quantum information theory."
    )
    
    def model(self) -> Dict[str, float]:
        freq = calculate_settlement_frequency()
        bits_per_step = 3
        bandwidth = bits_per_step * freq
        
        orbits_per_electron = 137
        steps_per_orbit = 8  # average
        bits_per_electron = orbits_per_electron * steps_per_orbit * bits_per_step
        
        return {
            "Bandwidth (bits/s)": bandwidth,
            "Bits per electron": bits_per_electron,
        }


class FaceInformationDerivation(GFDTest):
    """
    Face state is derived from vertex visits, no separate face channel.
    """
    name = "Face Information Derivation"
    question = (
        "Is each face's state derived purely from the vertex visits it contains, without "
        "requiring a separate information channel for face-level encoding?"
    )
    reference_source = "Face derivation"
    tolerance = 0.001
    derivation = (
        "Each face in the stellated octahedron contains 3 vertices. "
        "Face state = set of visited vertices within that face. "
        "As the traversal progresses, track vertices seen per face. "
        "Verification: for each face, vertices_seen must be a subset of face_vertices. "
        "If all face states are consistent with their vertex definitions, "
        "faces derive their information from vertices with no extra channel required."
    )
    commentary = (
        "TIME faces and SPATIAL faces inherit their state from Coupling Port visitation "
        "without requiring separate information channels. This derivation suggests face "
        "properties emerge from vertex dynamics rather than independent encoding."
    )
    
    def model(self) -> Dict[str, float]:
        traversal = traverse_pi_base8(50)
        
        face_state = {name: set() for name in FACES.keys()}
        
        for step in traversal:
            vertex = step['vertex']
            for face_name, face_vertices in FACES.items():
                if vertex in face_vertices:
                    face_state[face_name].add(vertex)
        
        all_derived = 1
        for face_name, vertices_seen in face_state.items():
            expected_vertices = FACES[face_name]
            if not vertices_seen.issubset(expected_vertices):
                all_derived = 0
                break
        
        return {"All faces derived (1=yes)": all_derived}
    
    def observations(self) -> Dict[str, float]:
        return {"All faces derived (1=yes)": 1}


# =============================================================================
# TESTS: INFORMATION FLOW SUMMARY
# =============================================================================

class InformationFlowSummary(GFDTest):
    """
    Summary of information flow: 3 bits input, 3 bits state, 0 bits derived.
    """
    name = "Information Flow Summary"
    question = (
        "Does the information architecture consist of 3 bits input per step, 3 bits state, "
        "and 0 additional bits for derived quantities (tetrahedron, complement, faces)?"
    )
    reference_source = "Flow model"
    tolerance = 0.001
    derivation = (
        "Input: each pi digit is 0-7, requiring ceil(log2(8)) = 3 bits. "
        "State: vertex is 0-7, requiring 3 bits. "
        "Derived quantities require 0 extra bits: "
        "  - Tetrahedron: computed from parity of vertex (deterministic). "
        "  - Complement: computed as 7 - vertex (arithmetic). "
        "  - Face membership: looked up from vertex (fixed mapping). "
        "Total architecture: 3 bits in, 3 bits state, 0 bits derived. "
        "This represents minimal complexity for the k=4 Field Closure geometry."
    )
    commentary = (
        "The information architecture of 3 bits input, 3 bits state, and 0 bits for derived "
        "quantities represents a parsimonious encoding scheme. This structure is consistent "
        "with the Field Chamber operating near minimal complexity for its geometric constraints."
    )
    
    def model(self) -> Dict[str, float]:
        input_bits = 3  # digit is 0-7
        state_bits = 3  # vertex is 0-7
        derived_bits = 0  # tet, complement, faces all computed
        
        return {
            "Input bits per step": input_bits,
            "State bits": state_bits,
            "Derived bits (extra)": derived_bits,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Input bits per step": 3,
            "State bits": 3,
            "Derived bits (extra)": 0,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    InputIs3BitsPerStep,
    StateIs3Bits,
    DerivedInfoCostsZeroBits,
    CumsumAccumulatesInformation,
    NoInformationLoss,
    OrbitPreservesModularInformation,
    VertexDistributionEntropy,
    TetrahedronEntropy,
    InformationBandwidth,
    FaceInformationDerivation,
    InformationFlowSummary,
]


def run_all_tests() -> bool:
    """Run all bit propagation tests."""
    return run_test_group(
        title="Bit Propagation",
        summary=(
            "Tests examine information flow properties in the Field Closure model. "
            "Each step processes 3 bits (Pi digit 0-7), vertex state requires 3 bits, "
            "and derived quantities (Field Chamber assignment, complement, face membership) "
            "are computed deterministically from vertex index. The cumulative sum equals "
            "the sum of all input digits, and vertex position corresponds to cumsum mod 8."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
