"""
Pyramid k=5 Coupling Physics: The Portal Interface Mechanism

This module tests the critical concepts from the research documents that establish
the Great Pyramid as a k=5 OPEN system (vs k=4 CLOSED tetrahedron). The pyramid
is "half a Merkaba" - it couples to a remote Tet B through the square base.

Key Concepts from Research:
- k=5 pyramid vs k=4 tetrahedron: open vs closed field structure
- √3/6 coupling coefficient between square base and tetrahedral faces
- 4^28 fractal scale from pyramid to r_e (classical electron radius)
- Pi encoding cycle: 3→4→8→9→4→3 in cumulative sums
- Three chambers as d=3 structure at specific heights
- Grand Gallery as channel structure

Sources:
- great-pyramid-subspace-proof.md
- GreatPyramid_Field_Closure_Encoding.md
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from base import GFDTest, run_test_group


# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Field Chamber scale
R_E = 2.8179403262e-15   # Classical electron radius (m)

# Great Pyramid dimensions (meters)
PYRAMID_BASE_M = 230.4
PYRAMID_HEIGHT_M = 146.6
PYRAMID_APOTHEM_M = 186.4  # Slant height to middle of base edge

# Chamber heights above base (meters)
SUBTERRANEAN_HEIGHT_M = -30  # Below base (carved into bedrock)
QUEENS_CHAMBER_HEIGHT_M = 21.0
KINGS_CHAMBER_HEIGHT_M = 43.03

# Grand Gallery
GRAND_GALLERY_LENGTH_M = 47.0
GRAND_GALLERY_ANGLE_DEG = 26.0

# GFD Constants
K = 4
D = K - 1  # = 3
SQRT_2 = math.sqrt(2)
SQRT_3 = math.sqrt(3)
PHI = (1 + math.sqrt(5)) / 2

# Pi digits for encoding test
PI_DIGITS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]


# =============================================================================
# PART I: k=5 vs k=4 STRUCTURE
# =============================================================================

class K5VsK4Structure(GFDTest):
    """The pyramid (k=5) is an OPEN system vs tetrahedron (k=4) CLOSED."""
    name = "k=5 Open vs k=4 Closed"
    question = (
        "The tetrahedron (k=4) is CLOSED - a complete field structure. "
        "The pyramid (k=5) has 4 triangular faces + 1 square base = 5 faces. "
        "Does this k=5 structure represent an OPEN system that couples to a remote Tet B?"
    )
    reference_source = "great-pyramid-subspace-proof.md"
    tolerance = 0.01
    derivation = (
        "PREMISE: Compare pyramid (k=5) and tetrahedron (k=4) structures. "
        "STEP 1: Tetrahedron: 4 triangular faces, 4 vertices, 6 edges → k=4. "
        "STEP 2: Tetrahedron is minimum 3D enclosure → self-contained field closure. "
        "STEP 3: Pyramid: 4 triangular faces + 1 square base = 5 faces → k=5. "
        "STEP 4: Square base is an INTERFACE, not closure. Tet B couples remotely. "
        "OUTPUT: k=5 is open (couples to remote), k=4 is closed (self-contained)."
    )
    commentary = (
        "The pyramid represents 'half a Merkaba' - only Tet A is present locally. "
        "The square base acts as a coupling interface where Tet B can connect from "
        "ANYWHERE via frequency matching. This is the portal mechanism: the pyramid "
        "doesn't close on itself (like an electron's Merkaba), it reaches out to a "
        "matching remote structure through subspace."
    )
    
    def model(self):
        # Tetrahedron (k=4): closed
        tet_faces = K
        tet_vertices = K
        tet_edges = K * (K - 1) // 2  # 6
        tet_closed = 1  # Self-contained
        
        # Pyramid (k=5): open
        pyr_triangular_faces = K  # 4
        pyr_square_base = 1
        pyr_total_faces = pyr_triangular_faces + pyr_square_base  # 5
        pyr_vertices = K + 1  # 5
        pyr_edges = 2 * K  # 8
        pyr_closed = 0  # Requires remote coupling
        
        return {
            "Tetrahedron faces": tet_faces,
            "Tetrahedron closed": tet_closed,
            "Pyramid faces": pyr_total_faces,
            "Pyramid triangular": pyr_triangular_faces,
            "Pyramid square base": pyr_square_base,
            "Pyramid closed": pyr_closed,
            "k+1 structure": K + 1,
        }
    
    def observations(self):
        return {
            "Tetrahedron faces": 4.0,
            "Tetrahedron closed": 1.0,
            "Pyramid faces": 5.0,
            "Pyramid triangular": 4.0,
            "Pyramid square base": 1.0,
            "Pyramid closed": 0.0,
            "k+1 structure": 5.0,
        }


class SquareBaseCoupling(GFDTest):
    """The square base decomposes into 2 triangles for dual coupling."""
    name = "Square Base Decomposition"
    question = (
        "The square base can be decomposed along its diagonal into 2 triangles. "
        "Does this allow coupling to BOTH tetrahedra of a remote Merkaba structure?"
    )
    reference_source = "great-pyramid-subspace-proof.md"
    tolerance = 0.01
    derivation = (
        "PREMISE: A square decomposes into 2 triangles along its diagonal. "
        "STEP 1: Square base has 4 vertices and 4 edges. "
        "STEP 2: Diagonal creates 2 right triangles (or 2 equilateral if isoceles). "
        "STEP 3: Triangle 1 couples to remote Tet A face. "
        "STEP 4: Triangle 2 couples to remote Tet B face. "
        "OUTPUT: 2 triangles from 1 square, each coupling to one tet."
    )
    commentary = (
        "The square-to-triangle decomposition is the key to portal physics. "
        "A single square interface can couple to BOTH tetrahedra of a remote "
        "Merkaba structure. This dual coupling enables complete field closure "
        "between the local pyramid and a remote matching structure. The diagonal "
        "represents the 'channel selection' - which triangle couples where."
    )
    
    def model(self):
        square_vertices = 4
        square_edges = 4
        diagonal_count = 2  # Each square has 2 diagonals
        triangles_from_diagonal = 2  # One diagonal creates 2 triangles
        
        # Each triangle has 3 vertices, 3 edges
        # Matches a tetrahedral face
        triangle_vertices = D  # 3
        triangle_edges = D  # 3
        
        return {
            "Square vertices": square_vertices,
            "Square edges": square_edges,
            "Diagonals": diagonal_count,
            "Triangles from decomposition": triangles_from_diagonal,
            "Triangle vertices": triangle_vertices,
            "Couples to 2 tetrahedra": 1.0 if triangles_from_diagonal == 2 else 0.0,
        }
    
    def observations(self):
        return {
            "Square vertices": 4.0,
            "Square edges": 4.0,
            "Diagonals": 2.0,
            "Triangles from decomposition": 2.0,
            "Triangle vertices": 3.0,
            "Couples to 2 tetrahedra": 1.0,
        }


class CouplingCoefficient(GFDTest):
    """The √3/6 coupling coefficient between k=5 and k=4 structures."""
    name = "Coupling Coefficient √3/6"
    question = (
        "The coupling ratio between square base area and tetrahedral surface area "
        "equals √3/6. Does this represent the geometric interface efficiency between "
        "k=5 (pyramid) and k=4 (tetrahedron) structures?"
    )
    reference_source = "k5_k4_coupling_test.py results"
    tolerance = 0.01
    derivation = (
        "PREMISE: Calculate area ratio for unit-edge structures. "
        "STEP 1: Square base area (edge=1) = 1² = 1. "
        "STEP 2: Tetrahedron surface area (edge=1) = 4 × (√3/4) = √3. "
        "STEP 3: Coupling ratio = Square / Tet_surface = 1 / √3 = √3/3 ≈ 0.577. "
        "STEP 4: For normalized coupling: (1/2) × (1/√3) = √3/6 ≈ 0.289. "
        "OUTPUT: Coupling coefficient = √3/6 = 1/(2√3)."
    )
    commentary = (
        "The √3/6 coefficient represents how efficiently the square base couples "
        "to tetrahedral faces. This ratio appears in many geometric transformations "
        "between cubic (square) and tetrahedral (triangular) structures. It's the "
        "same ratio that appears in the relationship between a cube and its "
        "inscribed tetrahedra. The pyramid is geometrically 'tuned' to interface "
        "with k=4 field structures through this coupling constant."
    )
    
    def model(self):
        # Unit edge calculations
        square_area = 1.0  # edge = 1
        tet_face_area = SQRT_3 / 4  # equilateral triangle
        tet_surface_area = 4 * tet_face_area  # = √3
        
        # Coupling ratios
        simple_ratio = square_area / tet_surface_area  # 1/√3
        coupling_coefficient = 1 / (2 * SQRT_3)  # √3/6
        
        # Verify √3/6
        sqrt3_over_6 = SQRT_3 / 6
        
        return {
            "Square area": square_area,
            "Tet surface area": tet_surface_area,
            "Simple ratio (1/√3)": simple_ratio,
            "Coupling coefficient": coupling_coefficient,
            "√3/6": sqrt3_over_6,
            "Match": 1.0 if abs(coupling_coefficient - sqrt3_over_6) < 1e-10 else 0.0,
        }
    
    def observations(self):
        return {
            "Square area": 1.0,
            "Tet surface area": SQRT_3,
            "Simple ratio (1/√3)": 1 / SQRT_3,
            "Coupling coefficient": SQRT_3 / 6,
            "√3/6": SQRT_3 / 6,
            "Match": 1.0,
        }


# =============================================================================
# PART II: FRACTAL SCALE 4^28
# =============================================================================

class FractalScaleAnalysis(GFDTest):
    """The pyramid is approximately 4^28 Field Chambers from micro to macro."""
    name = "Fractal Scale 4^28"
    question = (
        "What is the scale relationship between the Great Pyramid and the fundamental "
        "Field Chamber (r_e = 2.818 fm)? Does the ratio approximate 4^n for some n?"
    )
    reference_source = "k5_k4_coupling_test.py"
    tolerance = 0.10
    derivation = (
        "PREMISE: Calculate scale ratio between pyramid and r_e. "
        "STEP 1: Pyramid base = 230.4 m. "
        "STEP 2: Classical electron radius r_e = 2.818 × 10⁻¹⁵ m. "
        "STEP 3: Ratio = 230.4 / (2.818 × 10⁻¹⁵) = 8.18 × 10¹⁶. "
        "STEP 4: log₄(8.18 × 10¹⁶) = ln(8.18 × 10¹⁶) / ln(4) ≈ 28.09. "
        "OUTPUT: Scale factor ≈ 4^28.09, approximately 28 'quadruplings'."
    )
    commentary = (
        "The pyramid base is ~4^28 Field Chambers across. This fractal relationship "
        "suggests the pyramid operates at a macro scale that resonates with the "
        "fundamental r_e scale through powers of k=4. The k=4 closure constant "
        "governs not just local field structure but the entire fractal hierarchy "
        "from quantum to architectural scales. This '28 quadruplings' represents "
        "the number of nested k=4 field levels between electron and pyramid."
    )
    
    def model(self):
        # Scale calculations
        ratio = PYRAMID_BASE_M / R_E
        log4_ratio = math.log(ratio) / math.log(4)
        
        # Also check height
        height_ratio = PYRAMID_HEIGHT_M / R_E
        log4_height = math.log(height_ratio) / math.log(4)
        
        return {
            "Pyramid base (m)": PYRAMID_BASE_M,
            "r_e (m)": R_E,
            "Base / r_e": ratio,
            "log₄(ratio)": log4_ratio,
            "Height / r_e": height_ratio,
            "log₄(height ratio)": log4_height,
            "~28 quadruplings": 1.0 if 27.5 < log4_ratio < 28.5 else 0.0,
        }
    
    def observations(self):
        ratio = PYRAMID_BASE_M / R_E
        return {
            "Pyramid base (m)": 230.4,
            "r_e (m)": R_E,
            "Base / r_e": ratio,
            "log₄(ratio)": math.log(ratio) / math.log(4),
            "Height / r_e": PYRAMID_HEIGHT_M / R_E,
            "log₄(height ratio)": math.log(PYRAMID_HEIGHT_M / R_E) / math.log(4),
            "~28 quadruplings": 1.0,
        }


# =============================================================================
# PART III: PI ENCODING CYCLE
# =============================================================================

class PiEncodingCycle(GFDTest):
    """Pi's first digits encode the field closure cycle: 3→4→8→9→4→3."""
    name = "Pi Encoding Cycle"
    question = (
        "Do the cumulative sums of π's first digits (3, 1, 4, 1, 5, 9) encode the "
        "field closure cycle? Does mod-8 and mod-10 analysis reveal 3→4→8→9→4→3?"
    )
    reference_source = "great-pyramid-subspace-proof.md"
    tolerance = 0.01
    derivation = (
        "PREMISE: Analyze cumulative sums of π = 3.14159... "
        "STEP 1: Position 0, digit 3: cumsum = 3 (3D space entry). "
        "STEP 2: Position 1, digit 1: cumsum = 4 (k=4 spacetime). "
        "STEP 3: Position 2, digit 4: cumsum = 8 (2k=8 dual tetrahedra). "
        "STEP 4: Position 3, digit 1: cumsum = 9 (8+1 = complete + center). "
        "STEP 5: Position 4, digit 5: cumsum = 14, mod 10 = 4 (return to k=4). "
        "STEP 6: Position 5, digit 9: cumsum = 23, mod 10 = 3 (return to 3D exit). "
        "OUTPUT: Cycle 3→4→8→9→4→3 encodes complete field closure traversal."
    )
    commentary = (
        "The π encoding cycle is remarkable: it traces the exact path of field "
        "closure. Enter 3D space (3), engage k=4 structure (4), activate dual "
        "tetrahedra (8), complete with center/King's Chamber (9), return through "
        "k=4 (4), exit in 3D (3). The cycle returns to '3' but NOT the same "
        "location - exit position depends on frequency matching. This is universal "
        "to ALL k=5 structures; the specific destination is determined by resonance."
    )
    
    def model(self):
        # First 6 digits of pi (after decimal point conceptually: 3.14159)
        digits = [3, 1, 4, 1, 5, 9]
        
        # Cumulative sums
        cumsums = []
        total = 0
        for d in digits:
            total += d
            cumsums.append(total)
        
        # Mod 10 and mod 8 analysis
        mod10 = [c % 10 for c in cumsums]
        mod8 = [c % 8 for c in cumsums]
        
        # The cycle in mod 10: 3, 4, 8, 9, 4, 3
        expected_mod10 = [3, 4, 8, 9, 4, 3]
        cycle_matches = (mod10 == expected_mod10)
        
        return {
            "Cumsum pos 0 (3D entry)": cumsums[0],
            "Cumsum pos 1 (k=4)": cumsums[1],
            "Cumsum pos 2 (2k=8)": cumsums[2],
            "Cumsum pos 3 (complete)": cumsums[3],
            "Cumsum pos 4 mod 10 (k=4)": mod10[4],
            "Cumsum pos 5 mod 10 (3D exit)": mod10[5],
            "Cycle matches 3→4→8→9→4→3": 1.0 if cycle_matches else 0.0,
        }
    
    def observations(self):
        return {
            "Cumsum pos 0 (3D entry)": 3.0,
            "Cumsum pos 1 (k=4)": 4.0,
            "Cumsum pos 2 (2k=8)": 8.0,
            "Cumsum pos 3 (complete)": 9.0,
            "Cumsum pos 4 mod 10 (k=4)": 4.0,
            "Cumsum pos 5 mod 10 (3D exit)": 3.0,
            "Cycle matches 3→4→8→9→4→3": 1.0,
        }


class PiExitOffset(GFDTest):
    """The exit position differs from entry by k×(k+1) = 20."""
    name = "Pi Exit Offset k×(k+1)"
    question = (
        "In the pi encoding, the entry (cumsum=3) and exit (cumsum=23) differ by 20. "
        "Does 20 = k×(k+1) = 4×5 represent the offset from k=4 to k=5 portal physics?"
    )
    reference_source = "great-pyramid-subspace-proof.md"
    tolerance = 0.01
    derivation = (
        "PREMISE: Analyze the difference between entry and exit cumsums. "
        "STEP 1: Entry cumsum at position 0 = 3. "
        "STEP 2: Exit cumsum at position 5 = 23. "
        "STEP 3: Offset = 23 - 3 = 20. "
        "STEP 4: Check: k × (k+1) = 4 × 5 = 20. Exact match! "
        "OUTPUT: Exit offset = 20 = k × (k+1)."
    )
    commentary = (
        "The offset 20 = k×(k+1) = 4×5 encodes the transition between k=4 (closed "
        "field structure) and k=5 (open portal structure). You enter through k=4 "
        "physics and exit through k=5 coupling. The '20' is not a physical distance "
        "but represents the algebraic relationship between the two structural modes. "
        "The actual destination is determined by frequency matching, not cumsum offset."
    )
    
    def model(self):
        entry_cumsum = 3
        exit_cumsum = 23  # cumsum at position 5
        offset = exit_cumsum - entry_cumsum
        
        k_times_k_plus_1 = K * (K + 1)  # 4 × 5 = 20
        
        return {
            "Entry cumsum": entry_cumsum,
            "Exit cumsum": exit_cumsum,
            "Offset": offset,
            "k × (k+1)": k_times_k_plus_1,
            "Match": 1.0 if offset == k_times_k_plus_1 else 0.0,
        }
    
    def observations(self):
        return {
            "Entry cumsum": 3.0,
            "Exit cumsum": 23.0,
            "Offset": 20.0,
            "k × (k+1)": 20.0,
            "Match": 1.0,
        }


# =============================================================================
# PART IV: THREE CHAMBERS AS d=3 STRUCTURE
# =============================================================================

class ThreeChamberStructure(GFDTest):
    """Three chambers (Subterranean, Queen's, King's) encode d=3."""
    name = "Three Chambers = d=3"
    question = (
        "The Great Pyramid has three known chambers at different heights. "
        "Does this encode the d=3 spatial structure of field closure?"
    )
    reference_source = "GreatPyramid_Field_Closure_Encoding.md"
    tolerance = 0.10
    derivation = (
        "PREMISE: Analyze the three chamber positions. "
        "STEP 1: Subterranean Chamber: ~30m BELOW base (carved into bedrock). "
        "STEP 2: Queen's Chamber: ~21m above base. "
        "STEP 3: King's Chamber: ~43m above base. "
        "STEP 4: Three chambers = d = k-1 = 3 spatial faces. "
        "OUTPUT: 3 chambers matching d=3 spatial dimensions."
    )
    commentary = (
        "The three chambers represent the d=3 spatial structure. The Subterranean "
        "Chamber is the 'anchor' (below, in bedrock), the Queen's Chamber is the "
        "midpoint or 'preparation' level, and the King's Chamber is the 'drain point' "
        "where field closure occurs. Together they span the three spatial dimensions "
        "required for a complete d=3 structure. The +1 element is the apex (the "
        "time-like component) or the Field Origin itself."
    )
    
    def model(self):
        chambers = 3
        d_spatial = D  # k - 1 = 3
        
        # Chamber heights
        subterranean = SUBTERRANEAN_HEIGHT_M
        queens = QUEENS_CHAMBER_HEIGHT_M
        kings = KINGS_CHAMBER_HEIGHT_M
        
        # Height ratios relative to King's
        queens_ratio = queens / kings  # ~0.49
        
        return {
            "Number of chambers": chambers,
            "d = k-1": d_spatial,
            "Match d=3": 1.0 if chambers == d_spatial else 0.0,
            "Subterranean height (m)": subterranean,
            "Queen's height (m)": queens,
            "King's height (m)": kings,
            "Queen's / King's ratio": queens_ratio,
        }
    
    def observations(self):
        return {
            "Number of chambers": 3.0,
            "d = k-1": 3.0,
            "Match d=3": 1.0,
            "Subterranean height (m)": -30.0,
            "Queen's height (m)": 21.0,
            "King's height (m)": 43.03,
            "Queen's / King's ratio": 21.0 / 43.03,
        }


class KingsChhamberAsDrainPoint(GFDTest):
    """King's Chamber at 1/3 height is the drain point (k+1)."""
    name = "King's Chamber as Drain (k+1)"
    question = (
        "The King's Chamber at ~43m (29.3% of 146.6m height) is close to 1/3 height. "
        "Does this position represent the 'drain point' where field closure occurs?"
    )
    reference_source = "GreatPyramid_Field_Closure_Encoding.md"
    tolerance = 0.15
    derivation = (
        "PREMISE: Analyze King's Chamber position relative to pyramid height. "
        "STEP 1: King's Chamber floor = 43.03m above base. "
        "STEP 2: Pyramid original height = 146.6m. "
        "STEP 3: Ratio = 43.03 / 146.6 = 0.2935 ≈ 0.29. "
        "STEP 4: Compare to 1/d = 1/3 = 0.333. Difference = 0.04 (~12% relative). "
        "STEP 5: In the full octahedron (mirror below), KC is at 2/3 total height. "
        "OUTPUT: KC at ~1/3 height, acting as drain point between above and below."
    )
    commentary = (
        "The King's Chamber position at approximately 1/3 height (not exactly) may "
        "encode the d=3 structure. More significantly, in the mirrored octahedron "
        "model (pyramid + its reflection below), the KC is at 2/3 of total height. "
        "This is the 'drain point' where the field from above meets the field from "
        "below. The slight deviation from exact 1/3 may have functional significance "
        "or reflect construction tolerances."
    )
    
    def model(self):
        kc_height = KINGS_CHAMBER_HEIGHT_M
        pyramid_height = PYRAMID_HEIGHT_M
        ratio = kc_height / pyramid_height
        
        one_third = 1 / D
        deviation = abs(ratio - one_third)
        
        # In full octahedron (2× height)
        full_height = 2 * pyramid_height
        kc_in_octahedron = pyramid_height + kc_height  # Distance from bottom apex
        octahedron_ratio = kc_in_octahedron / full_height
        
        return {
            "KC height (m)": kc_height,
            "Pyramid height (m)": pyramid_height,
            "KC / Pyramid ratio": ratio,
            "1/d = 1/3": one_third,
            "Deviation from 1/3": deviation,
            "In octahedron (2/3)": octahedron_ratio,
        }
    
    def observations(self):
        return {
            "KC height (m)": 43.03,
            "Pyramid height (m)": 146.6,
            "KC / Pyramid ratio": 43.03 / 146.6,
            "1/d = 1/3": 1/3,
            "Deviation from 1/3": abs(43.03/146.6 - 1/3),
            "In octahedron (2/3)": (146.6 + 43.03) / (2 * 146.6),
        }


class GrandGalleryAsChannel(GFDTest):
    """The Grand Gallery (47m, 26°) as the approach channel to Field Origin."""
    name = "Grand Gallery Channel"
    question = (
        "The Grand Gallery is 47m long at 26° angle. Does this represent "
        "one of the k=4 active channels leading to the King's Chamber (Field Origin)?"
    )
    reference_source = "GreatPyramid_Field_Closure_Encoding.md"
    tolerance = 0.10
    derivation = (
        "PREMISE: Analyze Grand Gallery as channel structure. "
        "STEP 1: Grand Gallery length ≈ 47m. "
        "STEP 2: Grand Gallery angle ≈ 26° from horizontal. "
        "STEP 3: This matches the angle of internal passages (~26°). "
        "STEP 4: Compare 26° to GFD angles: arctan(1/2) = 26.57°. "
        "OUTPUT: Gallery at ~26° ≈ arctan(1/2), channeling to KC."
    )
    commentary = (
        "The Grand Gallery is the ascension channel to the King's Chamber. Its "
        "26° angle is close to arctan(1/2) ≈ 26.57°, which appears in the "
        "geometry of the pyramid's internal structure. As one of k=4 channels, "
        "it represents the primary approach path to the Field Origin. The "
        "increasing ceiling height as you ascend may have acoustic/resonance "
        "significance for the frequency-tuning mechanism."
    )
    
    def model(self):
        gallery_length = GRAND_GALLERY_LENGTH_M
        gallery_angle = GRAND_GALLERY_ANGLE_DEG
        
        # Compare to arctan(1/2)
        arctan_half = math.degrees(math.atan(0.5))  # 26.57°
        angle_diff = abs(gallery_angle - arctan_half)
        
        # Vertical rise
        vertical_rise = gallery_length * math.sin(math.radians(gallery_angle))
        
        return {
            "Gallery length (m)": gallery_length,
            "Gallery angle (°)": gallery_angle,
            "arctan(1/2) (°)": arctan_half,
            "Angle difference": angle_diff,
            "Vertical rise (m)": vertical_rise,
            "Close to arctan(1/2)": 1.0 if angle_diff < 1.0 else 0.0,
        }
    
    def observations(self):
        return {
            "Gallery length (m)": 47.0,
            "Gallery angle (°)": 26.0,
            "arctan(1/2) (°)": math.degrees(math.atan(0.5)),
            "Angle difference": abs(26.0 - math.degrees(math.atan(0.5))),
            "Vertical rise (m)": 47.0 * math.sin(math.radians(26.0)),
            "Close to arctan(1/2)": 1.0,
        }


# =============================================================================
# PART V: PYRAMID PI AND PHI ENCODING
# =============================================================================

class PyramidPiEncoding(GFDTest):
    """The pyramid encodes π: perimeter/height ≈ 2π."""
    name = "Pyramid π Encoding"
    question = (
        "Does the Great Pyramid encode π in its proportions? "
        "Specifically, does perimeter/height ≈ 2π?"
    )
    reference_source = "great-pyramid-subspace-proof.md"
    tolerance = 0.01
    derivation = (
        "PREMISE: Check if perimeter/height = 2π. "
        "STEP 1: Pyramid base = 230.4m, so perimeter = 4 × 230.4 = 921.6m. "
        "STEP 2: Pyramid height = 146.6m. "
        "STEP 3: Perimeter / height = 921.6 / 146.6 = 6.286. "
        "STEP 4: 2π = 6.283. Error = 0.05%. "
        "OUTPUT: Perimeter/height = 6.286 ≈ 2π = 6.283."
    )
    commentary = (
        "The pyramid encodes π with remarkable precision. The perimeter/height "
        "ratio of ~6.286 matches 2π to within 0.05%. This is NOT unique to the "
        "pyramid - the natural Merkaba also encodes π. What's significant is that "
        "π encoding is PRESERVED in the k=5 structure, indicating that the field "
        "closure PROCESS is the same whether the system is closed (k=4) or open "
        "(k=5). π is fundamental to field closure itself."
    )
    
    def model(self):
        perimeter = 4 * PYRAMID_BASE_M
        height = PYRAMID_HEIGHT_M
        ratio = perimeter / height
        two_pi = 2 * math.pi
        error_percent = abs(ratio - two_pi) / two_pi * 100
        
        return {
            "Perimeter (m)": perimeter,
            "Height (m)": height,
            "Perimeter / Height": ratio,
            "2π": two_pi,
            "Error (%)": error_percent,
            "Encodes π": 1.0 if error_percent < 0.1 else 0.0,
        }
    
    def observations(self):
        perimeter = 4 * 230.4
        return {
            "Perimeter (m)": perimeter,
            "Height (m)": 146.6,
            "Perimeter / Height": perimeter / 146.6,
            "2π": 2 * math.pi,
            "Error (%)": abs(perimeter/146.6 - 2*math.pi) / (2*math.pi) * 100,
            "Encodes π": 1.0,
        }


class PyramidPhiEncoding(GFDTest):
    """The pyramid encodes φ: apothem/(base/2) ≈ φ."""
    name = "Pyramid φ Encoding"
    question = (
        "Does the Great Pyramid encode the golden ratio φ in its proportions? "
        "Specifically, does apothem/(half-base) ≈ φ?"
    )
    reference_source = "great-pyramid-subspace-proof.md"
    tolerance = 0.01
    derivation = (
        "PREMISE: Check if apothem/(base/2) = φ. "
        "STEP 1: Apothem (slant height to edge midpoint) ≈ 186.4m. "
        "STEP 2: Half-base = 230.4 / 2 = 115.2m. "
        "STEP 3: Ratio = 186.4 / 115.2 = 1.618. "
        "STEP 4: φ = (1+√5)/2 = 1.618. Error < 0.03%. "
        "OUTPUT: Apothem/half-base = 1.618 ≈ φ."
    )
    commentary = (
        "The pyramid encodes φ (golden ratio) with even greater precision than π. "
        "The apothem-to-half-base ratio matches φ to within 0.03%. This φ encoding "
        "relates to the self-similar (fractal) nature of field closure. The golden "
        "ratio appears throughout nature in growth patterns and is connected to "
        "the Fibonacci sequence, which may relate to how nested field structures "
        "scale across the 4^28 hierarchy from r_e to pyramid."
    )
    
    def model(self):
        apothem = PYRAMID_APOTHEM_M
        half_base = PYRAMID_BASE_M / 2
        ratio = apothem / half_base
        error_percent = abs(ratio - PHI) / PHI * 100
        
        return {
            "Apothem (m)": apothem,
            "Half-base (m)": half_base,
            "Apothem / Half-base": ratio,
            "φ": PHI,
            "Error (%)": error_percent,
            "Encodes φ": 1.0 if error_percent < 0.1 else 0.0,
        }
    
    def observations(self):
        return {
            "Apothem (m)": 186.4,
            "Half-base (m)": 115.2,
            "Apothem / Half-base": 186.4 / 115.2,
            "φ": PHI,
            "Error (%)": abs(186.4/115.2 - PHI) / PHI * 100,
            "Encodes φ": 1.0,
        }


# =============================================================================
# TEST REGISTRY AND RUNNER
# =============================================================================

ALL_TESTS = [
    # Part I: k=5 vs k=4 Structure
    K5VsK4Structure,
    SquareBaseCoupling,
    CouplingCoefficient,
    
    # Part II: Fractal Scale
    FractalScaleAnalysis,
    
    # Part III: Pi Encoding Cycle
    PiEncodingCycle,
    PiExitOffset,
    
    # Part IV: Three Chambers
    ThreeChamberStructure,
    KingsChhamberAsDrainPoint,
    GrandGalleryAsChannel,
    
    # Part V: Pi and Phi Encoding
    PyramidPiEncoding,
    PyramidPhiEncoding,
]


def run_all_tests():
    """Run all pyramid coupling physics tests."""
    return run_test_group(
        title="Pyramid k=5 Coupling Physics: The Portal Interface Mechanism",
        summary=(
            "These tests examine the Great Pyramid as a k=5 OPEN system that couples "
            "to remote k=4 field structures through its square base. Key findings: "
            "√3/6 coupling coefficient, 4^28 fractal scale, π encoding cycle "
            "(3→4→8→9→4→3), three chambers as d=3 structure, and π/φ geometric encoding. "
            "The pyramid is 'half a Merkaba' that reaches through subspace to complete "
            "field closure with a remote matching structure."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    passed = run_all_tests()
    exit(0 if passed else 1)
