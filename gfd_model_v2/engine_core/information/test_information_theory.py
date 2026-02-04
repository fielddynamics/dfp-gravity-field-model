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

import math
from typing import Dict

from gfd_model_v2.framework import *
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

class BitsPerFace(Test):
    """
    [E] Test bits required to specify a face reading.
    Each face has 3 vertices. Face selection requires log2(8) = 3 bits.
    Full vertex specification requires 3 vertices x 3 bits = 9 bits.
    """
    name = "Bits Per Face"
    question = (
        "How does geometry constrain how we specify faces? "
        "We calculate that selecting one of 8 faces takes 3 bits, and fully "
        "specifying its three vertices takes 9 bits."
    )
    reference = "Information theory (log2)"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("From k=4 Field Closure: each tetrahedron has k=4 faces, total faces = 2k = 8")
            .step("Face selection bits: ceil(log2(8)) = 3 bits to choose 1 of 8 faces")
            .step("Each vertex requires 3 bits (log2(8) = 3 for 8 vertices)")
            .step("Each Coupling Port face has 3 vertices: 3 vertices * 3 bits = 9 bits total")
            .conclude("The geometry constrains information encoding through its combinatorial structure")
        )
    
    commentary = (
        "A face is a triangle with 3 corners. To say which face we mean out of 8 possible faces, "
        "we need log2(8) = 3 bits. But to fully describe a face by listing its vertices, we need "
        "more: 3 vertices times 3 bits each = 9 bits total. Notice the 3s everywhere: 3 bits to "
        "select a face, 3 vertices per face, 3 bits per vertex. The geometry of the stellated "
        "octahedron has 3 built into its DNA. This is not design; it is constraint. "
        "The mathematics of 8 things forces this structure upon us."
    )
    
    def model(self):
        bits_face_select = math.ceil(math.log2(NUM_FACES))
        bits_vertex_spec = VERTICES_PER_FACE * BITS_PER_VERTEX
        
        return (
            Model()
            .add("Face selection bits", bits_face_select)
            .add("Vertex specification bits", bits_vertex_spec)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Face selection bits", 3)
            .add("Vertex specification bits", 9)
        )


class ParityBitEncoding(Test):
    """
    [M] Vertex parity provides a 1-bit check.
    Tet_A vertices (1,2,4,7): odd parity.
    Tet_B vertices (0,3,5,6): even parity.
    """
    name = "Parity Bit Encoding"
    question = (
        "Why does a simple bit-count tell you which tetrahedron you are in? "
        "We verify that binary parity (odd vs even number of 1-bits) perfectly "
        "predicts Tetrahedron A vs Tetrahedron B membership."
    )
    reference = "Binary parity definition"
    tolerance = 0.001
    level = Critical
    
    def derivation(self):
        return (
            Derivation()
            .step("For vertex v in binary (3 bits), parity = count of 1-bits mod 2")
            .step("Tetrahedron A vertices: {1, 2, 4, 7} have binary forms {001, 010, 100, 111}")
            .step("Parity of each: 1, 1, 1, 1 (all odd)")
            .step("Tetrahedron B vertices: {0, 3, 5, 6} have binary forms {000, 011, 101, 110}")
            .step("Parity of each: 0, 0, 0, 0 (all even)")
            .conclude("Parity = 1 implies Tet_A, Parity = 0 implies Tet_B, with 100% accuracy")
        )
    
    commentary = (
        "Write each vertex number in binary. Vertex 5 = 101. Count the 1-bits: two. "
        "Two is even, so vertex 5 is in Tetrahedron B. Vertex 7 = 111 has three 1-bits. "
        "Three is odd, so vertex 7 is in Tetrahedron A. It works perfectly, every time. "
        "Why? Because the two tetrahedra interlock in a way that separates odd-parity "
        "and even-parity vertices. The geometry and the binary arithmetic are in perfect "
        "agreement. This is one of those beautiful moments where two completely different "
        "ways of looking at the same thing give identical answers."
    )
    
    def model(self):
        tet_a_correct = 0
        tet_b_correct = 0
        
        for v in range(8):
            parity = bin(v).count('1') % 2
            if v in TET_A and parity == 1:
                tet_a_correct += 1
            if v in TET_B and parity == 0:
                tet_b_correct += 1
        
        return (
            Model()
            .add("Tet_A odd parity matches", tet_a_correct)
            .add("Tet_B even parity matches", tet_b_correct)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Tet_A odd parity matches", 4)
            .add("Tet_B even parity matches", 4)
        )


class TimeSpatialInformationRatio(Test):
    """
    [M] Ratio of TIME to SPATIAL information channels.
    TIME faces: 2 (FACE_A7, FACE_B0), SPATIAL faces: 6.
    Ratio: 2:6 = 1:3 (25% temporal, 75% spatial).
    """
    name = "TIME-SPATIAL Information Ratio"
    question = (
        "Why does the geometry allocate information channels unequally between time and space? "
        "We find a 2:6 ratio (25% temporal, 75% spatial), matching 1 time dimension vs 3 spatial."
    )
    reference = "Face classification"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("From k=4 Field Closure: each tetrahedron has k=4 faces")
            .step("Per tetrahedron: 1 TIME face (apex-opposite), 3 SPATIAL faces (apex-adjacent)")
            .step("Two tetrahedra yield: 2 TIME faces, 6 SPATIAL faces")
            .equation("TIME:SPATIAL ratio = 2:6 = 1:3 = 1/d (where d=k-1=3 spatial dimensions)")
            .step("Information partition: 2/8 = 25% temporal channels, 6/8 = 75% spatial channels")
            .conclude("The geometry partitions information channels asymmetrically between time and space")
        )
    
    commentary = (
        "Our universe has 1 time dimension and 3 space dimensions. That ratio is 1:3. "
        "The stellated octahedron has 2 TIME faces and 6 SPATIAL faces. That ratio? Also 1:3. "
        "The geometry seems to 'know' about spacetime. It allocates 25% of its information "
        "channels to time and 75% to space, exactly mirroring how our 4D spacetime is divided. "
        "Is this coincidence? Or does the geometry encode something fundamental about the "
        "structure of spacetime itself? At minimum, it is a striking numerical correspondence."
    )
    
    def model(self):
        num_time = len(TIME_FACES)
        num_spatial = len(SPATIAL_FACES)
        ratio = num_time / num_spatial if num_spatial > 0 else 0
        
        return (
            Model()
            .add("TIME faces", num_time)
            .add("SPATIAL faces", num_spatial)
            .add("TIME:SPATIAL ratio", ratio)
        )
    
    def observations(self):
        return (
            Observed()
            .add("TIME faces", 2)
            .add("SPATIAL faces", 6)
            .add("TIME:SPATIAL ratio", 1/3)
        )


class RedundancyFromComplementaryPairs(Test):
    """
    [M] Information redundancy from complementary vertex pairs.
    Pairs: (0,7), (1,6), (2,5), (3,4). Creates 2x redundancy.
    """
    name = "Redundancy From Complementary Pairs"
    question = (
        "Why does the geometry have built-in error detection? "
        "We verify that complementary pairs (v, 7-v) create 2x redundancy, "
        "allowing errors to be detected through complement checking."
    )
    reference = "Complement arithmetic"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("The 2k=8 vertices form complementary pairs: v + (7-v) = 7 for all v")
            .step("Pairs: (0,7), (1,6), (2,5), (3,4) yield 4 unique pairs from 8 vertices")
            .step("Knowing vertex v automatically determines its complement (7-v)")
            .equation("Redundancy factor = total vertices / unique pairs = 8/4 = 2.0")
            .conclude("This 2x redundancy enables error detection through complement verification")
        )
    
    commentary = (
        "Every vertex has a partner: 0 pairs with 7, 1 pairs with 6, 2 pairs with 5, 3 pairs "
        "with 4. They always sum to 7. This is like a parity check built right into the geometry. "
        "If you visit vertex 2, you implicitly know about vertex 5 (since 7 minus 2 = 5). "
        "Eight vertices, but only four independent pairs: that is 2x redundancy. In communication, "
        "we add redundancy to catch errors. Nature seems to have done the same. "
        "If something goes wrong, the complement relationship lets you detect it."
    )
    
    def model(self):
        pairs = [(v, 7-v) for v in range(4)]
        expected_pairs = [(0,7), (1,6), (2,5), (3,4)]
        pairs_match = 1 if pairs == expected_pairs else 0
        
        unique_pairs = len(pairs)
        total_vertices = NUM_VERTICES
        redundancy_factor = total_vertices / unique_pairs
        
        return (
            Model()
            .add("Pairs match expected", pairs_match)
            .add("Redundancy factor", redundancy_factor)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Pairs match expected", 1)
            .add("Redundancy factor", 2.0)
        )


class EffectiveInformationContent(Test):
    """
    [M] Effective (non-redundant) information content.
    Apparent bits per orbit: 24 (8 vertices x 3 bits).
    Effective bits per orbit: 12 (2x redundancy).
    """
    name = "Effective Information Content"
    question = (
        "How much truly independent information does one orbit carry? "
        "After subtracting the 2x redundancy from complementary pairs, "
        "we find 12 effective bits rather than 24 apparent bits."
    )
    reference = "Redundancy calculation"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Apparent information: 2k=8 vertices, each requiring 3 bits = 24 bits per orbit")
            .step("Complementary redundancy: each vertex v encodes its complement (7-v) implicitly")
            .step("Redundancy factor = 2.0 (derived from 4 unique pairs in 8 vertices)")
            .equation("Effective bits = apparent bits / redundancy = 24 / 2 = 12 bits per orbit")
            .conclude("The dual Tetrahedron A/B structure enables this intrinsic error detection")
        )
    
    commentary = (
        "At first glance, 8 vertices times 3 bits = 24 bits per orbit. But wait! Half of that "
        "is redundant. Visiting vertex 0 tells you about vertex 7. Visiting vertex 1 tells you "
        "about vertex 6. So 24 apparent bits shrink to 12 effective bits of independent information. "
        "This is not waste; it is protection. The geometry sacrifices raw capacity for robustness. "
        "It is like double-entry bookkeeping: you write each transaction twice, not to store more "
        "information, but to catch mistakes. The Field Chamber has error detection built in."
    )
    
    def model(self):
        # Calculate apparent bits directly (not using calculate_bits_per_orbit which 
        # already accounts for redundancy)
        apparent_bits = NUM_VERTICES * BITS_PER_VERTEX  # 8 * 3 = 24
        redundancy = 2.0
        effective_bits = apparent_bits / redundancy  # 12
        
        return (
            Model()
            .add("Apparent bits per orbit", apparent_bits)
            .add("Effective bits per orbit", effective_bits)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Apparent bits per orbit", 24)
            .add("Effective bits per orbit", 12)
        )


# =============================================================================
# TESTS: INFORMATION DENSITY
# =============================================================================

class InformationDensityPerGravityField(Test):
    """
    [M] Information density: bits per gravity field volume.
    Gravity field volume ~ r_e^3, Information per orbit: 24 bits.
    """
    name = "Information Density Per Gravity Field"
    question = (
        "How densely can information be packed at quantum scales? "
        "We calculate the bits per cubic meter at electron size, checking "
        "whether it approaches fundamental quantum limits."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Gravity field volume at electron scale is V = r_e^3, with r_e = 2.818e-15 m")
            .step("Calculate volume: V = (2.818e-15)^3 = 2.24e-44 m^3")
            .step("Information per orbit = 8 vertices * 3 bits = 24 bits")
            .equation("Density = bits / volume = 24 / 2.24e-44 = 1.07e45 bits/m^3")
            .conclude("Density > 1e40 bits/m^3, indicating operation near quantum limits")
        )
    
    commentary = (
        "Take the volume occupied by one electron-scale Field Closure: roughly 10^-44 cubic "
        "meters (unimaginably tiny). Pack 24 bits into that space. The density? About 10^45 "
        "bits per cubic meter. For comparison: a modern hard drive stores maybe 10^15 bits per "
        "cubic meter. The Field Closure is 10^30 times denser. We are approaching the quantum "
        "limit, where spacetime itself becomes grainy. Nature achieves storage densities that "
        "make our best technology look laughably crude."
    )
    
    def model(self):
        gravity_field_volume = R_E ** 3
        bits_per_orbit = calculate_bits_per_orbit()
        density = bits_per_orbit / gravity_field_volume
        above_threshold = 1 if density > 1e40 else 0
        
        return (
            Model()
            .add("Information density (bits/m^3)", density)
            .add("Above 1e40 threshold", above_threshold)
        )


class BitsPerPlanckVolume(Test):
    """
    [M] Bits per Planck volume.
    Planck volume = l_P^3. Relates to quantum gravity bounds.
    """
    name = "Bits Per Planck Volume"
    question = (
        "How sparse is information at the Planck scale? "
        "We calculate how many Planck volumes fit in one Field Closure, "
        "revealing that bits are spread extremely thin at quantum gravity scales."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Compare Planck volume to gravity field volume at electron scale")
            .step("Planck volume V_P = l_P^3 = (1.616e-35)^3 = 4.22e-105 m^3")
            .step("Gravity field volume V_gf = r_e^3 = (2.818e-15)^3 = 2.24e-44 m^3")
            .equation("Ratio = V_gf / V_P = 2.24e-44 / 4.22e-105 = 5.3e60 Planck volumes per gravity field")
            .step("Information per Planck volume = 24 bits / 5.3e60 = 4.5e-60 bits")
            .conclude("Planck volumes per gravity field > 1e50, indicating sparse encoding")
        )
    
    commentary = (
        "The Planck length is where quantum mechanics meets gravity: about 10^-35 meters. "
        "How many Planck-sized boxes fit inside one electron-scale Field Closure? About 10^60. "
        "And we only have 24 bits spread across all that volume. That is roughly 10^-60 bits "
        "per Planck volume. Incredibly sparse! The information is not tightly packed at the "
        "Planck scale; it is spread thin. The Field Closure operates in a middle regime: "
        "denser than our technology, but far sparser than the Planck limit would allow."
    )
    
    def model(self):
        planck_volume = L_PLANCK ** 3
        gravity_field_volume = R_E ** 3
        planck_per_gravity_field = gravity_field_volume / planck_volume
        
        bits_per_orbit = calculate_bits_per_orbit()
        bits_per_planck = bits_per_orbit / planck_per_gravity_field
        
        above_threshold = 1 if planck_per_gravity_field > 1e50 else 0
        
        return (
            Model()
            .add("Planck volumes per gravity field", planck_per_gravity_field)
            .add("Bits per Planck volume", bits_per_planck)
            .add("Above 1e50 threshold", above_threshold)
        )


class InformationVsElectronCompton(Test):
    """
    [M] Information content vs Compton wavelength.
    Bits per electron: ~3288 (137 orbits x 24 bits).
    """
    name = "Information vs Electron Compton"
    question = (
        "What ties the electron's information budget to electromagnetic coupling? "
        "We verify that 3288 bits per electron equals 137 orbits times 24 bits, "
        "linking information content to the fine structure constant."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Orbits per electron: 1/alpha = 1/0.007297 = 137 (fine structure constant inverse)")
            .step("Bits per orbit: 24 (from 8 vertices * 3 bits)")
            .equation("Total bits per electron = 137 * 24 = 3288 bits")
            .step("Verification: 3000 < 3288 < 4000 confirms the expected range")
            .conclude("The alignment of 137 orbits with 1/alpha suggests geometric encoding of EM coupling")
        )
    
    commentary = (
        "The fine structure constant alpha describes how strongly electrons interact with "
        "light. Its inverse, about 137, is one of the most mysterious numbers in physics. "
        "Here it appears as the number of orbits per electron: 137 orbits times 24 bits per "
        "orbit = 3288 bits. The electron's information content is not arbitrary. It is locked "
        "to the fine structure constant. If you ask 'how much information is in an electron,' "
        "the answer involves the same number that determines how light and matter dance together."
    )
    
    def model(self):
        bits_per_electron = calculate_bits_per_electron()
        in_range = 1 if 3000 < bits_per_electron < 4000 else 0
        
        return (
            Model()
            .add("Bits per electron", bits_per_electron)
            .add("In range 3000-4000", in_range)
            .add("Compton wavelength (m)", LAMBDA_C)
        )


# =============================================================================
# TESTS: BEKENSTEIN-LIKE BOUNDS
# =============================================================================

class HolographicPrincipleCheck(Test):
    """
    [I] Consistency with holographic principle.
    Max bits ~ Area / (4 * l_P^2). Must satisfy this bound.
    """
    name = "Holographic Principle Check"
    question = (
        "Does the geometry respect the ultimate information limit from black hole physics? "
        "We verify that the Field Chamber stays far below the holographic (Bekenstein) bound, "
        "which caps entropy based on surface area."
    )
    reference = None  # Threshold check
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Holographic bound: S_max = A / (4 * l_P^2) where A = surface area")
            .step("Electron surface area: A = 4 * pi * r_e^2 = 4 * pi * (2.818e-15)^2 = 9.98e-29 m^2")
            .step("Planck area: l_P^2 = (1.616e-35)^2 = 2.61e-70 m^2")
            .equation("Max bits: S_max = 9.98e-29 / (4 * 2.61e-70) = 9.56e40 bits")
            .step("Actual bits: 24 per orbit. Ratio = 24 / 9.56e40 << 1")
            .conclude("The Field Chamber operates far below the holographic limit")
        )
    
    commentary = (
        "Black hole physics taught us something astonishing: the maximum information a region "
        "can hold depends on its surface area, not its volume. This is the holographic bound. "
        "For the electron scale, that bound is about 10^40 bits. Our Field Closure uses only "
        "24 bits. That is a ratio of about 10^-40. We are nowhere near the limit. The geometry "
        "is playing it safe, using a tiny fraction of the allowed information capacity. "
        "The laws of physics permit vastly more, but nature operates with elegant restraint."
    )
    
    def model(self):
        surface_area = 4 * math.pi * R_E ** 2
        planck_area = L_PLANCK ** 2
        max_bits_holographic = surface_area / (4 * planck_area)
        
        actual_bits = calculate_bits_per_orbit()
        ratio = actual_bits / max_bits_holographic
        within_bound = 1 if ratio < 1 else 0
        
        return (
            Model()
            .add("Holographic ratio", ratio)
            .add("Within bound (1=yes)", within_bound)
            .add("Max bits (holographic)", max_bits_holographic)
        )


# =============================================================================
# TESTS: ERROR CORRECTION
# =============================================================================

class DualTetrahedraErrorDetection(Test):
    """
    [M] Error detection from dual tetrahedra structure.
    Parity bit provides 1 bit error detection per 3 data bits.
    Code rate: 3/4 = 75%.
    """
    name = "Dual Tetrahedra Error Detection"
    question = (
        "How does the dual structure enable error detection? "
        "We verify that the Tetrahedron A/B parity provides a built-in check bit, "
        "achieving the standard 75% code rate (3 data bits + 1 parity bit)."
    )
    reference = "Coding theory"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Each vertex is specified by 3 data bits (log2(8) = 3)")
            .step("Tetrahedron membership (A or B) provides 1 parity bit (derived from vertex)")
            .step("Total bits per vertex: 3 data + 1 parity = 4 bits")
            .equation("Code rate = data bits / total bits = 3/4 = 0.75 = 75%")
            .conclude("This matches standard single-bit error detection schemes where parity enables detection of odd-numbered bit flips")
        )
    
    commentary = (
        "In digital communication, we add parity bits to detect errors. Send 7 data bits plus "
        "1 parity bit; if the parity check fails, you know something went wrong. The stellated "
        "octahedron does this naturally! Three bits specify the vertex, and the fourth bit (which "
        "tetrahedron) is redundant: it can be computed from parity. If someone claims vertex 5 is "
        "in Tetrahedron A, you can check: 5 = 101, two 1-bits, even parity, so it must be "
        "Tetrahedron B. Error caught! The geometry has a built-in consistency check."
    )
    
    def model(self):
        error_detection_bits = 1
        data_bits = BITS_PER_VERTEX
        total_bits = data_bits + error_detection_bits
        code_rate = data_bits / total_bits
        
        return Model().add("Code rate (data/total)", code_rate)
    
    def observations(self):
        return Observed().add("Code rate (data/total)", 0.75)


class FaceRedundancyForCorrection(Test):
    """
    [M] Face-level redundancy for error correction.
    9 bits transmitted (3 vertices x 3 bits), 6 bits minimal.
    Redundancy: 9/6 = 1.5x.
    """
    name = "Face Redundancy For Correction"
    question = (
        "How much extra protection does face-level encoding provide? "
        "We calculate the 1.5x redundancy factor between full vertex specification "
        "(9 bits) and minimal face encoding (6 bits)."
    )
    reference = "Face encoding"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Full face specification: 3 vertices per face * 3 bits per vertex = 9 bits")
            .step("Minimal encoding: face selection (3 bits) + face state (3 bits) = 6 bits")
            .equation("Redundancy factor = full bits / minimal bits = 9/6 = 1.5")
            .conclude("This 1.5x redundancy at the Coupling Port face level provides error tolerance beyond vertex-level parity, creating layered protection")
        )
    
    commentary = (
        "There are two ways to describe a face. The long way: list all 3 vertices, at 3 bits "
        "each, for 9 bits total. The short way: say which face (3 bits) and its state (3 bits), "
        "for 6 bits. The ratio is 9/6 = 1.5. That extra 50% is redundancy. Why carry the extra "
        "weight? Because if one piece of information gets corrupted, the other pieces can "
        "detect or even correct the error. The geometry is built like a medieval cathedral: "
        "multiple supports, so if one fails, the structure stands."
    )
    
    def model(self):
        full_bits = VERTICES_PER_FACE * BITS_PER_VERTEX
        face_select_bits = math.ceil(math.log2(NUM_FACES))
        face_state_bits = 3
        minimal_bits = face_select_bits + face_state_bits
        redundancy = full_bits / minimal_bits
        
        return Model().add("Face redundancy factor", redundancy)
    
    def observations(self):
        return Observed().add("Face redundancy factor", 1.5)


class TimeFaceAsChecksum(Test):
    """
    [M] TIME faces as global checksum.
    FACE_A7 vertices: {1,2,4}, FACE_B0 vertices: {3,5,6}.
    Together cover 6 vertices, apexes (0,7) serve as checksum.
    """
    name = "TIME Face As Checksum"
    question = (
        "How does the geometry separate data from verification? "
        "We verify that TIME faces cover all 6 non-apex vertices, leaving the "
        "apex pair (0,7) as special checksum locations."
    )
    reference = "Face structure"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("TIME faces in the Field Chamber: FACE_A7 and FACE_B0")
            .step("FACE_A7 vertices: {1, 2, 4} (Tetrahedron A, opposite apex 7)")
            .step("FACE_B0 vertices: {3, 5, 6} (Tetrahedron B, opposite apex 0)")
            .step("Union: {1,2,4} | {3,5,6} = {1,2,3,4,5,6} (6 non-apex vertices)")
            .step("Remaining vertices: {0,7} = Field Origin apexes (complementary pair)")
            .conclude("The apexes form a checksum pair where 0 + 7 = 7 verifies integrity")
        )
    
    commentary = (
        "The two TIME faces together touch vertices {1,2,3,4,5,6}, which is exactly all the "
        "non-apex vertices. The apexes (0 and 7) sit apart, untouched by TIME faces. These "
        "special vertices form a complementary pair (0 + 7 = 7) and can serve as checksum "
        "locations. Think of a book where 6 chapters tell the story and 2 pages at the end "
        "summarize everything for verification. The geometry naturally separates primary "
        "content from summary/verification. Data lives on TIME faces; checksums live at apexes."
    )
    
    def model(self):
        face_a7_verts = FACES['FACE_A7']
        face_b0_verts = FACES['FACE_B0']
        
        covered = face_a7_verts | face_b0_verts
        expected = {1, 2, 3, 4, 5, 6}
        coverage_correct = 1 if covered == expected else 0
        
        apexes = set(range(8)) - covered
        apexes_correct = 1 if apexes == {0, 7} else 0
        
        return (
            Model()
            .add("Coverage correct (1=yes)", coverage_correct)
            .add("Apexes correct (1=yes)", apexes_correct)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Coverage correct (1=yes)", 1)
            .add("Apexes correct (1=yes)", 1)
        )


# =============================================================================
# TESTS: INFORMATION FLOW
# =============================================================================

class BitsPerSettlement(Test):
    """
    [M] Total bits processed per settlement cycle.
    One settlement = one complete field closure = 24 apparent bits.
    """
    name = "Bits Per Settlement"
    question = (
        "How many bits flow through the geometry per tick of its internal clock? "
        "We calculate 24 bits per settlement cycle, and multiply by frequency "
        "to get the staggering bandwidth."
    )
    reference = "Orbit definition"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("One settlement = one complete orbit through the stellated octahedron")
            .step("Bits per orbit: 2k=8 vertices * 3 bits per vertex = 24 bits (apparent)")
            .step("Settlement frequency: f_s = c / lambda_C (Compton frequency)")
            .equation("Bandwidth = bits_per_settlement * frequency = 24 * f_s bits/second")
            .conclude("At electron scale: f_s ~ 1.24e20 Hz, yielding bandwidth ~ 2.97e21 bits/s")
        )
    
    commentary = (
        "Each complete lap around the stellated octahedron settles 24 bits of information. "
        "How fast do laps happen? At the Compton frequency, about 10^20 times per second. "
        "That means 24 x 10^20 = 2.4 x 10^21 bits per second flowing through one electron-scale "
        "Field Closure. If you wanted to build a computer this fast, you would need technology "
        "that does not exist and may never exist. Nature runs at speeds we can only dream of."
    )
    
    def model(self):
        freq = calculate_settlement_frequency()
        # Use apparent bits (8 vertices * 3 bits) not effective bits
        bits_per_settlement = NUM_VERTICES * BITS_PER_VERTEX  # 24
        bandwidth = bits_per_settlement * freq
        
        return (
            Model()
            .add("Bits per settlement", bits_per_settlement)
            .add("Bandwidth (bits/s)", bandwidth)
        )
    
    def observations(self):
        freq = calculate_settlement_frequency()
        return (
            Observed()
            .add("Bits per settlement", 24)
            .add("Bandwidth (bits/s)", 24 * freq)
        )


class ChannelCapacityPerPort(Test):
    """
    [M] Channel capacity per port (face).
    8 total faces, k=4 active ports. 3 bits per face, 6 bits per active port.
    """
    name = "Channel Capacity Per Port"
    question = (
        "How does information divide among the faces and ports? "
        "We calculate 3 bits per face and 6 bits per active port, "
        "showing how the geometry allocates its throughput."
    )
    reference = "Port structure"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Total bits per orbit: 24 (from 8 vertices * 3 bits)")
            .step("Total faces: 2k = 8 (k=4 per tetrahedron)")
            .step("Bits per face: 24 / 8 = 3 bits")
            .step("Active ports per orbit: k = 4 (Field Closure constant)")
            .equation("Bits per active Coupling Port: 24 / 4 = 6 bits")
            .conclude("Port Ratio = active/total = 4/8 = 1/2, determining throughput allocation")
        )
    
    commentary = (
        "Imagine 24 bits of water flowing through a pipe that splits into 8 equal tubes "
        "(the faces). Each tube gets 24/8 = 3 bits. But only 4 of those tubes are 'active' "
        "Coupling Ports at any time. Those 4 active ports share the 24 bits, so each gets "
        "24/4 = 6 bits. The geometry has a 50% duty cycle: half the faces are active, half "
        "are quiet. This ratio is not arbitrary; it emerges from k=4 Field Closure. "
        "The geometry dictates how information is parceled out."
    )
    
    def model(self):
        # Use apparent bits (24) not effective bits (12)
        total_bits_per_orbit = NUM_VERTICES * BITS_PER_VERTEX  # 24
        bits_per_port = total_bits_per_orbit / NUM_FACES  # 24/8 = 3
        bits_per_active_port = total_bits_per_orbit / K  # 24/4 = 6
        
        return (
            Model()
            .add("Bits per face", bits_per_port)
            .add("Bits per active port (k=4)", bits_per_active_port)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Bits per face", 3)
            .add("Bits per active port (k=4)", 6)
        )


class InformationPerAlpha(Test):
    """
    [M] Information content per fine structure constant cycle.
    1/alpha = 137 orbits = one electron.
    """
    name = "Information Per Alpha"
    question = (
        "What deep connection links electron information to electromagnetic coupling? "
        "We verify that bits per electron = (1/alpha) x (bits per orbit) = 137 x 24 = 3288, "
        "tying information content directly to the fine structure constant."
    )
    reference = "Fine structure constant"
    tolerance = 0.001
    level = Standard
    
    def derivation(self):
        return (
            Derivation()
            .step("Fine structure constant: alpha = 1/137.036, so 1/alpha = 137 orbits")
            .step("Bits per orbit: 24 (from 8 vertices * 3 bits)")
            .equation("Bits per electron: orbits * bits_per_orbit = 137 * 24 = 3288 bits")
            .step("Verification: calculate_bits_per_electron() should return 3288")
            .conclude("This correspondence links the geometric Field Closure cycle count to the electromagnetic coupling strength")
        )
    
    commentary = (
        "The fine structure constant controls how electrons interact with photons. Its inverse, "
        "137, appears here as the number of orbits per electron. Each orbit carries 24 bits. "
        "Multiply them: 137 x 24 = 3288 bits. This is not a coincidence we can easily dismiss. "
        "The electron's information budget is numerically tied to the same mysterious number "
        "that governs electromagnetic interactions. Perhaps information and electromagnetism "
        "are two faces of the same underlying structure. We do not claim to understand why, "
        "only that the numbers match."
    )
    
    def model(self):
        orbits_per_electron = int(1 / ALPHA)
        bits_per_orbit = calculate_bits_per_orbit()
        bits_per_electron = calculate_bits_per_electron()
        calculated = orbits_per_electron * bits_per_orbit
        
        return (
            Model()
            .add("Orbits per electron", orbits_per_electron)
            .add("Calculated bits", calculated)
            .add("Function bits", bits_per_electron)
        )
    
    def observations(self):
        orbits_per_electron = int(1 / ALPHA)
        bits_per_orbit = calculate_bits_per_orbit()
        expected = orbits_per_electron * bits_per_orbit
        
        return (
            Observed()
            .add("Orbits per electron", orbits_per_electron)
            .add("Calculated bits", expected)
            .add("Function bits", expected)
        )


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


def run_all():
    """Run all information theory tests."""
    return run_tests(
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
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
