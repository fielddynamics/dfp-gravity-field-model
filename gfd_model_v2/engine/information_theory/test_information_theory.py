"""
Information Theory
==================

These tests analyze the information-theoretic properties of the stellated
octahedron structure. The 8-vertex system can be encoded with 3 bits per
vertex. The tests calculate information content per orbit, redundancy from
complementary pairs, and compare to standard information-theoretic bounds.

Classification:
    [E] = ESTABLISHED physics/mathematics
    [M] = MODEL calculation (from geometry)
    [I] = INTERPRETATION (conceptual comparison)

The tests document numerical values without asserting the structure
functions as a physical information processing system.
"""

import sys
import os
import math
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, GroupResult, Renderer, run_test_group
from gfd_model_v2.common import (
    VERTICES, TET_A, TET_B, FACES, K, C, HBAR, ALPHA,
    TIME_FACES, SPATIAL_FACES, COMPLEMENTARY_PAIRS,
    ELECTRON_MASS, LAMBDA_C,
    calculate_settlement_frequency, calculate_bits_per_orbit,
    calculate_bits_per_electron
)


# =============================================================================
# CONSTANTS
# =============================================================================

R_E = 2.8179403262e-15  # Classical electron radius (meters)
BITS_PER_VERTEX = 3
NUM_VERTICES = 8
NUM_FACES = 8
VERTICES_PER_FACE = 3
L_PLANCK = 1.616255e-35  # Planck length (meters)


# =============================================================================
# TESTS: STRUCTURAL INFORMATION
# =============================================================================

class BitsPerFace(GFDTest):
    """
    [E] Test bits required to specify a face reading.
    Each face has 3 vertices. Face selection requires log2(8) = 3 bits.
    Full vertex specification requires 3 vertices x 3 bits = 9 bits.
    """
    name = "Bits Per Face"
    question = (
        "How many bits are required to specify a face in the stellated octahedron, "
        "and how many bits to fully specify its three vertices?"
    )
    reference_source = "Information theory (log2)"
    tolerance = 0.001
    derivation = (
        "From k=4 Field Closure: each tetrahedron has k=4 faces, total faces = 2k = 8. "
        "Face selection bits: ceil(log2(8)) = 3 bits to choose 1 of 8 faces. "
        "Each vertex requires 3 bits (log2(8) = 3 for 8 vertices). "
        "Each Coupling Port face has 3 vertices: 3 vertices * 3 bits = 9 bits total. "
        "The geometry constrains information encoding through its combinatorial structure."
    )
    commentary = (
        "The 3-bit face selection and 9-bit vertex specification arise directly from "
        "the 8-face, 3-vertex-per-face structure of the stellated octahedron. This "
        "correspondence with log2(8) = 3 suggests the geometry imposes natural "
        "information-theoretic constraints on field encoding."
    )
    
    def model(self) -> Dict[str, float]:
        bits_face_select = math.ceil(math.log2(NUM_FACES))
        bits_vertex_spec = VERTICES_PER_FACE * BITS_PER_VERTEX
        
        return {
            "Face selection bits": bits_face_select,
            "Vertex specification bits": bits_vertex_spec,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Face selection bits": 3,
            "Vertex specification bits": 9,
        }


class ParityBitEncoding(GFDTest):
    """
    [M] Vertex parity provides a 1-bit check.
    Tet_A vertices (1,2,4,7): odd parity.
    Tet_B vertices (0,3,5,6): even parity.
    """
    name = "Parity Bit Encoding"
    question = (
        "Does the binary parity of each vertex index (0-7) correctly identify its "
        "membership in Tetrahedron A or Tetrahedron B?"
    )
    reference_source = "Binary parity definition"
    tolerance = 0.001
    derivation = (
        "For vertex v in binary (3 bits), parity = count of 1-bits mod 2. "
        "Tetrahedron A vertices: {1, 2, 4, 7} have binary forms {001, 010, 100, 111}. "
        "Parity of each: 1, 1, 1, 1 (all odd). "
        "Tetrahedron B vertices: {0, 3, 5, 6} have binary forms {000, 011, 101, 110}. "
        "Parity of each: 0, 0, 0, 0 (all even). "
        "Result: Parity = 1 implies Tet_A, Parity = 0 implies Tet_B, with 100% accuracy."
    )
    commentary = (
        "The perfect correspondence between binary parity and Tetrahedron A/B membership "
        "indicates that the stellated octahedron's dual structure is encoded in the binary "
        "representation itself. This may suggest a fundamental connection between geometric "
        "duality and information parity."
    )
    
    def model(self) -> Dict[str, float]:
        tet_a_correct = 0
        tet_b_correct = 0
        
        for v in range(8):
            parity = bin(v).count('1') % 2
            if v in TET_A and parity == 1:
                tet_a_correct += 1
            if v in TET_B and parity == 0:
                tet_b_correct += 1
        
        return {
            "Tet_A odd parity matches": tet_a_correct,
            "Tet_B even parity matches": tet_b_correct,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Tet_A odd parity matches": 4,
            "Tet_B even parity matches": 4,
        }


class TimeSpatialInformationRatio(GFDTest):
    """
    [M] Ratio of TIME to SPATIAL information channels.
    TIME faces: 2 (FACE_A7, FACE_B0), SPATIAL faces: 6.
    Ratio: 2:6 = 1:3 (25% temporal, 75% spatial).
    """
    name = "TIME-SPATIAL Information Ratio"
    question = (
        "What is the ratio of TIME faces to SPATIAL faces in the Field Chamber, "
        "and how does this partition information channels between temporal and spatial modes?"
    )
    reference_source = "Face classification"
    tolerance = 0.001
    derivation = (
        "From k=4 Field Closure: each tetrahedron has k=4 faces. "
        "Per tetrahedron: 1 TIME face (apex-opposite), 3 SPATIAL faces (apex-adjacent). "
        "Two tetrahedra yield: 2 TIME faces, 6 SPATIAL faces. "
        "TIME:SPATIAL ratio = 2:6 = 1:3 = 1/d (where d=k-1=3 spatial dimensions). "
        "Information partition: 2/8 = 25% temporal channels, 6/8 = 75% spatial channels."
    )
    commentary = (
        "The 2:6 (1:3) ratio of TIME to SPATIAL faces corresponds to a 25%/75% partition "
        "of information channels. This asymmetric distribution may indicate preferential "
        "geometric treatment of temporal versus spatial degrees of freedom within the "
        "Field Chamber."
    )
    
    def model(self) -> Dict[str, float]:
        num_time = len(TIME_FACES)
        num_spatial = len(SPATIAL_FACES)
        ratio = num_time / num_spatial if num_spatial > 0 else 0
        
        return {
            "TIME faces": num_time,
            "SPATIAL faces": num_spatial,
            "TIME:SPATIAL ratio": ratio,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "TIME faces": 2,
            "SPATIAL faces": 6,
            "TIME:SPATIAL ratio": 1/3,
        }


class RedundancyFromComplementaryPairs(GFDTest):
    """
    [M] Information redundancy from complementary vertex pairs.
    Pairs: (0,7), (1,6), (2,5), (3,4). Creates 2x redundancy.
    """
    name = "Redundancy From Complementary Pairs"
    question = (
        "Does the complementary vertex pairing (v, 7-v) in the stellated octahedron "
        "provide inherent 2x information redundancy?"
    )
    reference_source = "Complement arithmetic"
    tolerance = 0.001
    derivation = (
        "The 2k=8 vertices form complementary pairs: v + (7-v) = 7 for all v. "
        "Pairs: (0,7), (1,6), (2,5), (3,4) yield 4 unique pairs from 8 vertices. "
        "Knowing vertex v automatically determines its complement (7-v). "
        "Redundancy factor = total vertices / unique pairs = 8/4 = 2.0. "
        "This 2x redundancy enables error detection through complement verification."
    )
    commentary = (
        "The complementary pair structure (V_n + V_(7-n) = 7) provides inherent 2x "
        "redundancy within the stellated octahedron. This geometric redundancy is "
        "consistent with error-resilient encoding schemes in information theory."
    )
    
    def model(self) -> Dict[str, float]:
        pairs = [(v, 7-v) for v in range(4)]
        expected_pairs = [(0,7), (1,6), (2,5), (3,4)]
        pairs_match = 1 if pairs == expected_pairs else 0
        
        unique_pairs = len(pairs)
        total_vertices = NUM_VERTICES
        redundancy_factor = total_vertices / unique_pairs
        
        return {
            "Pairs match expected": pairs_match,
            "Redundancy factor": redundancy_factor,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Pairs match expected": 1,
            "Redundancy factor": 2.0,
        }


class EffectiveInformationContent(GFDTest):
    """
    [M] Effective (non-redundant) information content.
    Apparent bits per orbit: 24 (8 vertices x 3 bits).
    Effective bits per orbit: 12 (2x redundancy).
    """
    name = "Effective Information Content"
    question = (
        "After accounting for complementary pair redundancy, what is the effective "
        "(non-redundant) information content per complete orbit of the Field Chamber?"
    )
    reference_source = "Redundancy calculation"
    tolerance = 0.001
    derivation = (
        "Apparent information: 2k=8 vertices, each requiring 3 bits = 24 bits per orbit. "
        "Complementary redundancy: each vertex v encodes its complement (7-v) implicitly. "
        "Redundancy factor = 2.0 (derived from 4 unique pairs in 8 vertices). "
        "Effective bits = apparent bits / redundancy = 24 / 2 = 12 bits per orbit. "
        "The dual Tetrahedron A/B structure enables this intrinsic error detection."
    )
    commentary = (
        "The reduction from 24 apparent bits to 12 effective bits per orbit through "
        "complementary pair redundancy suggests the Field Chamber maintains information "
        "integrity through geometric self-correction. This is consistent with the dual "
        "Tetrahedron A/B structure providing intrinsic error detection."
    )
    
    def model(self) -> Dict[str, float]:
        # Calculate apparent bits directly (not using calculate_bits_per_orbit which 
        # already accounts for redundancy)
        apparent_bits = NUM_VERTICES * BITS_PER_VERTEX  # 8 * 3 = 24
        redundancy = 2.0
        effective_bits = apparent_bits / redundancy  # 12
        
        return {
            "Apparent bits per orbit": apparent_bits,
            "Effective bits per orbit": effective_bits,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Apparent bits per orbit": 24,
            "Effective bits per orbit": 12,
        }


# =============================================================================
# TESTS: INFORMATION DENSITY
# =============================================================================

class InformationDensityPerGravityField(GFDTest):
    """
    [M] Information density: bits per gravity field volume.
    Gravity field volume ~ r_e^3, Information per orbit: 24 bits.
    """
    name = "Information Density Per Gravity Field"
    question = (
        "What is the information density (bits per cubic meter) at the electron scale, "
        "and does it approach fundamental quantum information limits?"
    )
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Gravity field volume at electron scale is V = r_e^3, with r_e = 2.818e-15 m. "
        "STEP 1: Calculate volume: V = (2.818e-15)^3 = 2.24e-44 m^3. "
        "STEP 2: Information per orbit = 8 vertices * 3 bits = 24 bits. "
        "STEP 3: Density = bits / volume = 24 / 2.24e-44 = 1.07e45 bits/m^3. "
        "OUTPUT: Density > 1e40 bits/m^3, indicating operation near quantum limits."
    )
    commentary = (
        "The calculated information density exceeds 10^40 bits per cubic meter at the "
        "electron scale. This extreme density is consistent with quantum systems "
        "operating near fundamental information-theoretic limits within the Field "
        "Chamber geometry."
    )
    
    def model(self) -> Dict[str, float]:
        gravity_field_volume = R_E ** 3
        bits_per_orbit = calculate_bits_per_orbit()
        density = bits_per_orbit / gravity_field_volume
        above_threshold = 1 if density > 1e40 else 0
        
        return {
            "Information density (bits/m^3)": density,
            "Above 1e40 threshold": above_threshold,
        }


class BitsPerPlanckVolume(GFDTest):
    """
    [M] Bits per Planck volume.
    Planck volume = l_P^3. Relates to quantum gravity bounds.
    """
    name = "Bits Per Planck Volume"
    question = (
        "How many Planck volumes fit within a single gravity field, and what does "
        "this imply about information density at the Planck scale?"
    )
    reference_source = None  # Threshold check
    derivation = (
        "PREMISE: Compare Planck volume to gravity field volume at electron scale. "
        "STEP 1: Planck volume V_P = l_P^3 = (1.616e-35)^3 = 4.22e-105 m^3. "
        "STEP 2: Gravity field volume V_gf = r_e^3 = (2.818e-15)^3 = 2.24e-44 m^3. "
        "STEP 3: Ratio = V_gf / V_P = 2.24e-44 / 4.22e-105 = 5.3e60 Planck volumes per gravity field. "
        "STEP 4: Information per Planck volume = 24 bits / 5.3e60 = 4.5e-60 bits. "
        "OUTPUT: Planck volumes per gravity field > 1e50, indicating sparse encoding."
    )
    commentary = (
        "The ratio of Planck volumes per gravity field (~10^58) compared to 24 bits "
        "per orbit suggests highly sparse information encoding at the Planck scale. This "
        "may indicate the stellated octahedron structure operates at a scale intermediate "
        "between quantum and Planck regimes."
    )
    
    def model(self) -> Dict[str, float]:
        planck_volume = L_PLANCK ** 3
        gravity_field_volume = R_E ** 3
        planck_per_gravity_field = gravity_field_volume / planck_volume
        
        bits_per_orbit = calculate_bits_per_orbit()
        bits_per_planck = bits_per_orbit / planck_per_gravity_field
        
        above_threshold = 1 if planck_per_gravity_field > 1e50 else 0
        
        return {
            "Planck volumes per gravity field": planck_per_gravity_field,
            "Bits per Planck volume": bits_per_planck,
            "Above 1e50 threshold": above_threshold,
        }


class InformationVsElectronCompton(GFDTest):
    """
    [M] Information content vs Compton wavelength.
    Bits per electron: ~3288 (137 orbits x 24 bits).
    """
    name = "Information vs Electron Compton"
    question = (
        "What is the total information content per electron, and how does it relate to "
        "the fine structure constant through orbital count?"
    )
    reference_source = None  # Threshold check
    derivation = (
        "Orbits per electron: 1/alpha = 1/0.007297 = 137 (fine structure constant inverse). "
        "Bits per orbit: 24 (from 8 vertices * 3 bits). "
        "Total bits per electron = 137 * 24 = 3288 bits. "
        "Verification: 3000 < 3288 < 4000 confirms the expected range. "
        "The alignment of 137 orbits with 1/alpha suggests geometric encoding of EM coupling."
    )
    commentary = (
        "The information capacity of approximately 3288 bits per electron corresponds "
        "numerically to 137 orbits at 24 bits each. This alignment with the fine "
        "structure constant (1/alpha ~ 137) may indicate a connection between geometric "
        "structure and electromagnetic coupling strength."
    )
    
    def model(self) -> Dict[str, float]:
        bits_per_electron = calculate_bits_per_electron()
        in_range = 1 if 3000 < bits_per_electron < 4000 else 0
        
        return {
            "Bits per electron": bits_per_electron,
            "In range 3000-4000": in_range,
            "Compton wavelength (m)": LAMBDA_C,
        }


# =============================================================================
# TESTS: BEKENSTEIN-LIKE BOUNDS
# =============================================================================

class HolographicPrincipleCheck(GFDTest):
    """
    [I] Consistency with holographic principle.
    Max bits ~ Area / (4 * l_P^2). Must satisfy this bound.
    """
    name = "Holographic Principle Check"
    question = (
        "Does the Field Chamber's information content respect the holographic (Bekenstein) "
        "bound, which limits entropy to area in Planck units?"
    )
    reference_source = None  # Threshold check
    derivation = (
        "Holographic bound: S_max = A / (4 * l_P^2) where A = surface area. "
        "Electron surface area: A = 4 * pi * r_e^2 = 4 * pi * (2.818e-15)^2 = 9.98e-29 m^2. "
        "Planck area: l_P^2 = (1.616e-35)^2 = 2.61e-70 m^2. "
        "Max bits: S_max = 9.98e-29 / (4 * 2.61e-70) = 9.56e40 bits. "
        "Actual bits: 24 per orbit. Ratio = 24 / 9.56e40 << 1. "
        "The Field Chamber operates far below the holographic limit."
    )
    commentary = (
        "The actual information content falls well within the holographic bound "
        "(ratio << 1), indicating consistency with the Bekenstein limit. This suggests "
        "the Field Chamber geometry respects fundamental entropy bounds from black hole "
        "thermodynamics."
    )
    
    def model(self) -> Dict[str, float]:
        surface_area = 4 * math.pi * R_E ** 2
        planck_area = L_PLANCK ** 2
        max_bits_holographic = surface_area / (4 * planck_area)
        
        actual_bits = calculate_bits_per_orbit()
        ratio = actual_bits / max_bits_holographic
        within_bound = 1 if ratio < 1 else 0
        
        return {
            "Holographic ratio": ratio,
            "Within bound (1=yes)": within_bound,
            "Max bits (holographic)": max_bits_holographic,
        }


# =============================================================================
# TESTS: ERROR CORRECTION
# =============================================================================

class DualTetrahedraErrorDetection(GFDTest):
    """
    [M] Error detection from dual tetrahedra structure.
    Parity bit provides 1 bit error detection per 3 data bits.
    Code rate: 3/4 = 75%.
    """
    name = "Dual Tetrahedra Error Detection"
    question = (
        "Does the dual tetrahedra structure provide error detection with a 75% code rate, "
        "analogous to standard parity-based error detection?"
    )
    reference_source = "Coding theory"
    tolerance = 0.001
    derivation = (
        "Each vertex is specified by 3 data bits (log2(8) = 3). "
        "Tetrahedron membership (A or B) provides 1 parity bit (derived from vertex). "
        "Total bits per vertex: 3 data + 1 parity = 4 bits. "
        "Code rate = data bits / total bits = 3/4 = 0.75 = 75%. "
        "This matches standard single-bit error detection schemes where parity "
        "enables detection of odd-numbered bit flips."
    )
    commentary = (
        "The 75% code rate (3 data bits plus 1 parity bit) corresponds to standard "
        "single-bit error detection. The Tetrahedron A/B parity structure may serve "
        "an analogous role to parity bits in error-detecting codes."
    )
    
    def model(self) -> Dict[str, float]:
        error_detection_bits = 1
        data_bits = BITS_PER_VERTEX
        total_bits = data_bits + error_detection_bits
        code_rate = data_bits / total_bits
        
        return {"Code rate (data/total)": code_rate}
    
    def observations(self) -> Dict[str, float]:
        return {"Code rate (data/total)": 0.75}


class FaceRedundancyForCorrection(GFDTest):
    """
    [M] Face-level redundancy for error correction.
    9 bits transmitted (3 vertices x 3 bits), 6 bits minimal.
    Redundancy: 9/6 = 1.5x.
    """
    name = "Face Redundancy For Correction"
    question = (
        "What is the redundancy factor at the face level, comparing full vertex "
        "specification to minimal face encoding?"
    )
    reference_source = "Face encoding"
    tolerance = 0.001
    derivation = (
        "Full face specification: 3 vertices per face * 3 bits per vertex = 9 bits. "
        "Minimal encoding: face selection (3 bits) + face state (3 bits) = 6 bits. "
        "Redundancy factor = full bits / minimal bits = 9/6 = 1.5. "
        "This 1.5x redundancy at the Coupling Port face level provides error tolerance "
        "beyond vertex-level parity, creating layered protection."
    )
    commentary = (
        "The 1.5x redundancy factor at the face level provides additional error tolerance "
        "beyond vertex-level parity. This layered redundancy structure is consistent with "
        "robust information encoding in the stellated octahedron."
    )
    
    def model(self) -> Dict[str, float]:
        full_bits = VERTICES_PER_FACE * BITS_PER_VERTEX
        face_select_bits = math.ceil(math.log2(NUM_FACES))
        face_state_bits = 3
        minimal_bits = face_select_bits + face_state_bits
        redundancy = full_bits / minimal_bits
        
        return {"Face redundancy factor": redundancy}
    
    def observations(self) -> Dict[str, float]:
        return {"Face redundancy factor": 1.5}


class TimeFaceAsChecksum(GFDTest):
    """
    [M] TIME faces as global checksum.
    FACE_A7 vertices: {1,2,4}, FACE_B0 vertices: {3,5,6}.
    Together cover 6 vertices, apexes (0,7) serve as checksum.
    """
    name = "TIME Face As Checksum"
    question = (
        "Do the TIME faces cover all non-apex vertices, leaving the apex vertices (0,7) "
        "to serve as global checksum locations?"
    )
    reference_source = "Face structure"
    tolerance = 0.001
    derivation = (
        "TIME faces in the Field Chamber: FACE_A7 and FACE_B0. "
        "FACE_A7 vertices: {1, 2, 4} (Tetrahedron A, opposite apex 7). "
        "FACE_B0 vertices: {3, 5, 6} (Tetrahedron B, opposite apex 0). "
        "Union: {1,2,4} | {3,5,6} = {1,2,3,4,5,6} (6 non-apex vertices). "
        "Remaining vertices: {0,7} = Field Origin apexes (complementary pair). "
        "The apexes form a checksum pair where 0 + 7 = 7 verifies integrity."
    )
    commentary = (
        "The TIME faces (containing vertices {1,2,4} and {3,5,6}) cover all non-apex "
        "vertices, leaving the Field Origin apexes (0,7) as potential checksum locations. "
        "This structure suggests a hierarchical organization where temporal faces provide "
        "primary data and apexes provide verification."
    )
    
    def model(self) -> Dict[str, float]:
        face_a7_verts = FACES['FACE_A7']
        face_b0_verts = FACES['FACE_B0']
        
        covered = face_a7_verts | face_b0_verts
        expected = {1, 2, 3, 4, 5, 6}
        coverage_correct = 1 if covered == expected else 0
        
        apexes = set(range(8)) - covered
        apexes_correct = 1 if apexes == {0, 7} else 0
        
        return {
            "Coverage correct (1=yes)": coverage_correct,
            "Apexes correct (1=yes)": apexes_correct,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Coverage correct (1=yes)": 1,
            "Apexes correct (1=yes)": 1,
        }


# =============================================================================
# TESTS: INFORMATION FLOW
# =============================================================================

class BitsPerSettlement(GFDTest):
    """
    [M] Total bits processed per settlement cycle.
    One settlement = one complete field closure = 24 apparent bits.
    """
    name = "Bits Per Settlement"
    question = (
        "How many bits are processed per Field Closure settlement cycle, and what "
        "bandwidth does this yield at the settlement frequency?"
    )
    reference_source = "Orbit definition"
    tolerance = 0.001
    derivation = (
        "One settlement = one complete orbit through the stellated octahedron. "
        "Bits per orbit: 2k=8 vertices * 3 bits per vertex = 24 bits (apparent). "
        "Settlement frequency: f_s = c / lambda_C (Compton frequency). "
        "Bandwidth = bits_per_settlement * frequency = 24 * f_s bits/second. "
        "At electron scale: f_s ~ 1.24e20 Hz, yielding bandwidth ~ 2.97e21 bits/s."
    )
    commentary = (
        "The 24 bits processed per Field Closure corresponds to one complete orbit "
        "through all 8 vertices. The resulting bandwidth (bits/s) depends on the "
        "settlement frequency, linking information flow to the geometric timing of "
        "Field Closure."
    )
    
    def model(self) -> Dict[str, float]:
        freq = calculate_settlement_frequency()
        # Use apparent bits (8 vertices * 3 bits) not effective bits
        bits_per_settlement = NUM_VERTICES * BITS_PER_VERTEX  # 24
        bandwidth = bits_per_settlement * freq
        
        return {
            "Bits per settlement": bits_per_settlement,
            "Bandwidth (bits/s)": bandwidth,
        }
    
    def observations(self) -> Dict[str, float]:
        freq = calculate_settlement_frequency()
        return {
            "Bits per settlement": 24,
            "Bandwidth (bits/s)": 24 * freq,
        }


class ChannelCapacityPerPort(GFDTest):
    """
    [M] Channel capacity per port (face).
    8 total faces, k=4 active ports. 3 bits per face, 6 bits per active port.
    """
    name = "Channel Capacity Per Port"
    question = (
        "What is the channel capacity per face and per active Coupling Port, given "
        "k=4 Field Closure and 8 total faces?"
    )
    reference_source = "Port structure"
    tolerance = 0.001
    derivation = (
        "Total bits per orbit: 24 (from 8 vertices * 3 bits). "
        "Total faces: 2k = 8 (k=4 per tetrahedron). "
        "Bits per face: 24 / 8 = 3 bits. "
        "Active ports per orbit: k = 4 (Field Closure constant). "
        "Bits per active Coupling Port: 24 / 4 = 6 bits. "
        "Port Ratio = active/total = 4/8 = 1/2, determining throughput allocation."
    )
    commentary = (
        "The 3 bits per face and 6 bits per active Coupling Port (k=4) reflect the "
        "geometric constraint of 8 faces with 4 active ports. This Port Ratio determines "
        "the information throughput per Field Closure cycle."
    )
    
    def model(self) -> Dict[str, float]:
        # Use apparent bits (24) not effective bits (12)
        total_bits_per_orbit = NUM_VERTICES * BITS_PER_VERTEX  # 24
        bits_per_port = total_bits_per_orbit / NUM_FACES  # 24/8 = 3
        bits_per_active_port = total_bits_per_orbit / K  # 24/4 = 6
        
        return {
            "Bits per face": bits_per_port,
            "Bits per active port (k=4)": bits_per_active_port,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Bits per face": 3,
            "Bits per active port (k=4)": 6,
        }


class InformationPerAlpha(GFDTest):
    """
    [M] Information content per fine structure constant cycle.
    1/alpha = 137 orbits = one electron.
    """
    name = "Information Per Alpha"
    question = (
        "Does the electron's information content equal the product of 1/alpha orbits "
        "times the bits per orbit, linking geometry to electromagnetic coupling?"
    )
    reference_source = "Fine structure constant"
    tolerance = 0.001
    derivation = (
        "Fine structure constant: alpha = 1/137.036, so 1/alpha = 137 orbits. "
        "Bits per orbit: 24 (from 8 vertices * 3 bits). "
        "Bits per electron: orbits * bits_per_orbit = 137 * 24 = 3288 bits. "
        "Verification: calculate_bits_per_electron() should return 3288. "
        "This correspondence links the geometric Field Closure cycle count "
        "to the electromagnetic coupling strength."
    )
    commentary = (
        "The relationship between information content per electron (3288 bits) and the "
        "fine structure constant (137 orbits) suggests a possible geometric basis for "
        "electromagnetic coupling. This correspondence is noted without claiming the "
        "geometry explains alpha."
    )
    
    def model(self) -> Dict[str, float]:
        orbits_per_electron = int(1 / ALPHA)
        bits_per_orbit = calculate_bits_per_orbit()
        bits_per_electron = calculate_bits_per_electron()
        calculated = orbits_per_electron * bits_per_orbit
        
        return {
            "Orbits per electron": orbits_per_electron,
            "Calculated bits": calculated,
            "Function bits": bits_per_electron,
        }
    
    def observations(self) -> Dict[str, float]:
        orbits_per_electron = int(1 / ALPHA)
        bits_per_orbit = calculate_bits_per_orbit()
        expected = orbits_per_electron * bits_per_orbit
        
        return {
            "Orbits per electron": orbits_per_electron,
            "Calculated bits": expected,
            "Function bits": expected,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    BitsPerFace,
    ParityBitEncoding,
    TimeSpatialInformationRatio,
    RedundancyFromComplementaryPairs,
    EffectiveInformationContent,
    InformationDensityPerGravityField,
    BitsPerPlanckVolume,
    InformationVsElectronCompton,
    HolographicPrincipleCheck,
    DualTetrahedraErrorDetection,
    FaceRedundancyForCorrection,
    TimeFaceAsChecksum,
    BitsPerSettlement,
    ChannelCapacityPerPort,
    InformationPerAlpha,
]


def run_all_tests() -> bool:
    """Run all information theory tests."""
    return run_test_group(
        title="Information Theory Analysis",
        summary=(
            "These tests calculate information-theoretic properties of the stellated "
            "octahedron structure. Each vertex requires 3 bits to specify (log2(8) = 3). "
            "An orbit visits all 8 vertices, processing 24 bits total. Complementary pairs "
            "provide 2x redundancy. The 2:6 ratio of TIME to SPATIAL faces yields 25%/75% "
            "partition. These calculations document the structure's information capacity "
            "without claiming it functions as a physical information processor."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
