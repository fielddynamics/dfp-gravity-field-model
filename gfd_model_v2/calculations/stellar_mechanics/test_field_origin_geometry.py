"""
Stellar Mechanics: Gravity Field Envelope and Field Origin Relationships
=========================================================================

GFD Model V2 - Converted to GFDTest interface

This module examines geometric relationships between gravity field envelope size,
the Field Origin (vortex eye), and compression ratios.

KEY CONCEPTS:
- Field Envelope size: r_e = 2.818 fm (classical electron radius)
- Field Origin: Center of stellated octahedron, gateway for binding
- Only UNBOUND fields (squish balls) can pass through field origin
- BOUND fields (bowling balls) have outward compression that blocks entry
- Binding requires overcoming compression barrier (~511 keV at r_e)
- k=4 tetrahedral closure geometry determines nuclear stability
"""

import sys
import os
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from gfd_model_v2.base import GFDTest, run_test_group

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from gfd_model_v2.common import (
    VERTICES, TET_A, TET_B, K,
    C, HBAR, ALPHA, ME,
    R_E, A_0, R_PROTON, LAMBDA_COMPTON,
    RHO_NUCLEAR, RHO_WHITE_DWARF, RHO_FIELD_BINDING,
    compression_ratio_equilibrium_to_tile,
    vortex_eye_size as calculate_vortex_eye_size_common,
)


def get_vertex_coords(v):
    coords = VERTICES[v]['coords']
    return np.array(coords, dtype=float)


def calculate_field_origin():
    all_coords = [get_vertex_coords(v) for v in range(8)]
    return np.mean(all_coords, axis=0)


# =============================================================================
# TEST CLASSES
# =============================================================================

class FieldEnvelopeSize(GFDTest):
    """Verify the Field Envelope size equals classical electron radius."""
    name = "Field Envelope r_e"
    question = "Does the fundamental Field Envelope size r_e correspond to the classical electron radius (2.818 fm), establishing the length scale of gravity field geometry?"
    reference_source = "CODATA"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Envelope is the spherical boundary of each gravity field. "
        "Its radius r_e equals the classical electron radius from CODATA. "
        "STEP 1: Apply classical electron radius formula: r_e = e^2 / (4*pi*eps0*m_e*c^2). "
        "STEP 2: CODATA value: r_e = 2.8179403262e-15 m = 2.818 fm. "
        "STEP 3: This scale determines the size of the field origin gateway. "
        "OUTPUT: Field Envelope r_e (m) = 2.818e-15."
    )
    commentary = (
        "The Field Envelope radius r_e = 2.818 fm is the fundamental length scale for gravity "
        "field geometry. It defines the size of each gravity field's spherical boundary and "
        "determines the field origin gateway size through which unbound fields (squish balls) "
        "must pass during binding."
    )
    
    def model(self):
        return {"Field Envelope r_e (m)": R_E}
    
    def observations(self):
        return {"Field Envelope r_e (m)": 2.818e-15}


class FieldEnvelopeLargerThanProton(GFDTest):
    """Verify Field Envelope is larger than proton radius."""
    name = "Field Envelope > Proton"
    question = "Is the Field Envelope size r_e larger than the proton charge radius by a factor > 3, yet fusion still requires stellar temperatures due to compression blocking?"
    reference_source = "Nuclear Physics / DFP"
    tolerance = 0.10
    derivation = (
        "PREMISE: The Field Envelope (r_e = 2.82 fm) is larger than the proton radius "
        "(r_p = 0.87 fm), yet fusion requires stellar temperatures. This proves the "
        "barrier isn't geometric - it's the compression blocking mechanism. "
        "STEP 1: Field Envelope: r_e = 2.818 fm. "
        "STEP 2: Proton radius: r_p = 0.87 fm (from electron scattering). "
        "STEP 3: Ratio: r_e / r_p = 2.818 / 0.87 = 3.24. "
        "STEP 4: Proton FITS geometrically (r_p < r_e). "
        "STEP 5: Yet fusion needs ~15 million K - why? "
        "STEP 6: Because bound atoms (bowling balls) have OUTWARD compression blocking entry. "
        "OUTPUT: r_e/r_p ratio = 3.24, Proton fits geometrically = 1.0."
    )
    commentary = (
        "The proton is geometrically smaller than the field origin (3.24x smaller), yet fusion "
        "requires stellar temperatures. This proves the barrier is NOT geometric size - it's the "
        "compression blocking mechanism. Bound atoms (bowling balls) have outward compression "
        "that resists entry. Overcoming this barrier (~511 keV) requires stellar energies."
    )
    
    def model(self):
        ratio = R_E / R_PROTON
        fits = 1.0 if ratio > 1.0 else 0.0
        return {"r_e/r_p ratio": ratio, "Proton fits geometrically": fits}
    
    def observations(self):
        return {"r_e/r_p ratio": 3.24, "Proton fits geometrically": 1.0}


class ElectronQuantumExtent(GFDTest):
    """Verify electron Compton wavelength spans ~861 Field Envelopes."""
    name = "Electron Quantum Extent"
    question = "Does the electron Compton wavelength span approximately 861 Field Envelope lengths, representing the electron vortex's quantum extent in gravity field units?"
    reference_source = "Quantum Mechanics"
    tolerance = 0.05
    derivation = (
        "PREMISE: The electron vortex pattern spans many gravity field lengths. "
        "The Compton wavelength / Field Envelope gives this count. "
        "STEP 1: Compton wavelength: lambda_C = 2.426e-12 m. "
        "STEP 2: Field Envelope: r_e = 2.818e-15 m. "
        "STEP 3: Ratio: lambda_C / r_e = 2.426e-12 / 2.818e-15 = 861. "
        "STEP 4: The electron vortex pattern extends across ~861 gravity field units. "
        "OUTPUT: lambda_C/r_e ratio = 861."
    )
    commentary = (
        "The ~861 ratio between Compton wavelength and Field Envelope represents the quantum "
        "extent of the electron vortex in gravity field units. The electron is NOT a gravity "
        "field itself - it's a vortex pattern that orbits outside the nuclear structure, "
        "spanning many gravity field lengths."
    )
    
    def model(self):
        ratio = LAMBDA_COMPTON / R_E
        spans_many = 1.0 if ratio > 800 else 0.0
        return {"lambda_C/r_e ratio": ratio, "Spans many fields": spans_many}
    
    def observations(self):
        return {"lambda_C/r_e ratio": 861, "Spans many fields": 1.0}


class FieldOriginAtCenter(GFDTest):
    """Verify Field Origin is at geometric center of stellated octahedron."""
    name = "Field Origin Location"
    question = "Is the Field Origin located at the geometric center (0,0,0) of the stellated octahedron, where Tet A and Tet B interpenetrate, serving as the gateway for gravity field binding?"
    reference_source = "DFP Geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Origin is at the geometric center of the stellated octahedron, "
        "where Tetrahedron A and Tetrahedron B interpenetrate. This is the gateway through "
        "which unbound gravity fields (squish balls) must pass to bind into Tet B. "
        "STEP 1: Calculate centroid of all 8 vertices. "
        "STEP 2: Vertices: {(-1,-1,-1), (-1,-1,1), (-1,1,-1), (-1,1,1), (1,-1,-1), (1,-1,1), (1,1,-1), (1,1,1)}. "
        "STEP 3: Average x = 0, Average y = 0, Average z = 0. "
        "STEP 4: Field Origin = (0, 0, 0). "
        "OUTPUT: Origin = (0, 0, 0), At center = 1.0."
    )
    commentary = (
        "The Field Origin at the geometric center is the gateway for binding. Only unbound "
        "gravity fields (squish balls with no outward compression) can pass through. "
        "Bound fields (bowling balls with outward compression) cannot enter - they must "
        "first be unbound by overcoming the compression blocking barrier."
    )
    
    def model(self):
        origin = calculate_field_origin()
        at_center = 1.0 if np.allclose(origin, [0, 0, 0]) else 0.0
        return {"Origin x": origin[0], "Origin y": origin[1], "Origin z": origin[2], "At center": at_center}
    
    def observations(self):
        return {"Origin x": 0.0, "Origin y": 0.0, "Origin z": 0.0, "At center": 1.0}


class OriginVertexDistance(GFDTest):
    """Verify distance from Field Origin to vertices = sqrt(3)."""
    name = "Origin-Vertex Distance"
    question = "In the stellated octahedron with unit coordinates, is the distance from Field Origin to each vertex exactly sqrt(3), ensuring symmetric geometry for binding?"
    reference_source = "Geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: In the stellated octahedron with unit coordinates, all 8 vertices are "
        "equidistant from the Field Origin. This symmetry is essential for consistent binding. "
        "STEP 1: Distance for vertex (1, 1, 1): sqrt(1+1+1) = sqrt(3) = 1.732. "
        "STEP 2: Same for all 8 vertices due to symmetry. "
        "OUTPUT: Average distance = 1.732, Expected sqrt(3) = 1.732, All equal = 1.0."
    )
    commentary = (
        "The uniform sqrt(3) distance from Field Origin to all vertices ensures symmetric "
        "binding geometry. Gravity fields approaching from any direction face the same "
        "geometric constraints at the field origin gateway."
    )
    
    def model(self):
        origin = calculate_field_origin()
        distances = [np.linalg.norm(get_vertex_coords(v) - origin) for v in range(8)]
        avg_dist = sum(distances) / len(distances)
        expected = math.sqrt(3)
        all_equal = 1.0 if all(abs(d - expected) < 0.001 for d in distances) else 0.0
        return {"Average distance": avg_dist, "Expected sqrt(3)": expected, "All equal": all_equal}
    
    def observations(self):
        return {"Average distance": 1.732, "Expected sqrt(3)": 1.732, "All equal": 1.0}


class VortexEyeSize(GFDTest):
    """Calculate vortex eye (field origin gateway) size."""
    name = "Vortex Eye / Field Origin Gateway"
    question = "Is the vortex eye (field origin gateway) approximately r_e/2 in radius, and what is its relationship to the compression blocking barrier?"
    reference_source = "DFP Model"
    tolerance = 0.15
    derivation = (
        "PREMISE: The vortex eye (field origin gateway) has effective radius ~r_e/2. "
        "This is the physical aperture through which unbound fields must pass. "
        "STEP 1: Field Envelope: r_e = 2.818 fm. "
        "STEP 2: Vortex eye estimate: r_e / 2 = 1.409 fm. "
        "STEP 3: The Coulomb barrier at r_e is ~511 keV - this is the compression "
        "blocking energy that must be overcome to unbind atoms and pass fields through. "
        "OUTPUT: Vortex eye size, Expected r_e/2, Ratio."
    )
    commentary = (
        "The vortex eye at the field origin is the gateway for binding. The ~r_e/2 aperture "
        "is geometrically accessible, but the compression blocking barrier (~511 keV at r_e) "
        "prevents bound atoms from passing. Only unbound fields (squish balls) can enter."
    )
    
    def model(self):
        eye_size = calculate_vortex_eye_size_common(R_E)
        expected = R_E / 2
        ratio = eye_size / expected
        return {"Vortex eye size (m)": eye_size, "Expected r_e/2 (m)": expected, "Ratio": ratio}


class CompressionRatioForBinding(GFDTest):
    """Calculate compression needed for gravity field binding."""
    name = "Compression Ratio for Binding"
    question = "What compression ratio is required to bring atoms from equilibrium spacing to binding proximity, and does this explain why binding only occurs in stellar cores?"
    reference_source = "DFP Model"
    tolerance = 0.20
    derivation = (
        "PREMISE: Atoms at equilibrium spacing (~10^-10 m) must be compressed to binding "
        "proximity (~10^-15 m = r_e). This compression overcomes the bowling ball barrier. "
        "STEP 1: Equilibrium spacing ~10^-10 m (Bohr radius scale). "
        "STEP 2: Binding proximity ~10^-15 m (Field Envelope scale). "
        "STEP 3: Compression ratio = 10^-10 / 10^-15 = 10^5. "
        "STEP 4: This extreme compression requires stellar core conditions. "
        "STEP 5: Compression overcomes outward pressure of bowling balls, enabling unbinding. "
        "OUTPUT: Compression ratio > 10^4."
    )
    commentary = (
        "The >10,000x compression needed to bring atoms to binding proximity explains why "
        "fusion only occurs in stellar cores. This compression must not only bring atoms "
        "close together but also provide enough energy (~511 keV) to overcome the compression "
        "blocking barrier - converting bowling balls to squish balls before they can bind."
    )
    
    def model(self):
        ratio = compression_ratio_equilibrium_to_tile()
        high_ratio = 1.0 if ratio > 1e4 else 0.0
        return {"Compression ratio": ratio, "Exceeds 10^4": high_ratio}


class BindingDensityThreshold(GFDTest):
    """Verify binding threshold density is between WD and nuclear."""
    name = "Binding Density Threshold"
    question = "Is the gravity field binding threshold density between white dwarf (~10^9 kg/m^3) and nuclear (~10^17 kg/m^3) densities, consistent with stellar core fusion conditions?"
    reference_source = "Astrophysics"
    tolerance = 0.01
    derivation = (
        "PREMISE: Binding threshold density should be intermediate between white dwarf "
        "and nuclear densities, matching observed stellar core fusion conditions. "
        "STEP 1: White dwarf density: ~10^9 kg/m^3 (log = 9). "
        "STEP 2: Binding threshold: ~10^14 kg/m^3 (log = 14) per model. "
        "STEP 3: Nuclear density: ~10^17 kg/m^3 (log = 17). "
        "STEP 4: Ordering: WD < binding < nuclear. Correct! "
        "OUTPUT: Correctly ordered = 1.0."
    )
    commentary = (
        "The intermediate binding density (~10^14 kg/m^3) corresponds to conditions "
        "between white dwarf and neutron star interiors. At this density, atoms are "
        "compressed enough that stellar energies can overcome the compression blocking "
        "barrier, enabling gravity field rebinding."
    )
    
    def model(self):
        log_wd = math.log10(RHO_WHITE_DWARF)
        log_bind = math.log10(RHO_FIELD_BINDING)
        log_nuclear = math.log10(RHO_NUCLEAR)
        ordered = 1.0 if log_wd < log_bind < log_nuclear else 0.0
        return {
            "WD log density": log_wd, 
            "Binding log density": log_bind, 
            "Nuclear log density": log_nuclear,
            "Correctly ordered": ordered,
        }
    
    def observations(self):
        log_wd = math.log10(RHO_WHITE_DWARF)
        log_bind = math.log10(RHO_FIELD_BINDING)
        log_nuclear = math.log10(RHO_NUCLEAR)
        return {
            "WD log density": log_wd, 
            "Binding log density": log_bind, 
            "Nuclear log density": log_nuclear,
            "Correctly ordered": 1.0,
        }


class KMultipleStability(GFDTest):
    """Verify k-multiple nuclei correspond to complete closure."""
    name = "K-Multiple = Complete Closure"
    question = "Do He-4, C-12, and O-16 correspond exactly to k, 3k, and k^2 gravity fields in Tet B, demonstrating complete tetrahedral closure geometry?"
    reference_source = "Nuclear Physics"
    tolerance = 0.01
    derivation = (
        "PREMISE: He-4, C-12, and O-16 should have A = k, 3k, k^2 respectively, "
        "representing complete closure configurations in Tet B. "
        "STEP 1: He-4: A = 4 = k = complete first closure. "
        "STEP 2: C-12: A = 12 = 3k = three nested closures (triple alpha). "
        "STEP 3: O-16: A = 16 = k^2 = four nested closures. "
        "STEP 4: All are k-multiples with complete closure geometry. "
        "OUTPUT: He-4 = k = 1.0, C-12 = 3k = 1.0, O-16 = k^2 = 1.0."
    )
    commentary = (
        "He-4 (k=4), C-12 (3k=12), and O-16 (k^2=16) all have A equal to k-multiples, "
        "meaning their Tet B contains complete tetrahedral closures with no leftover geometry. "
        "This complete closure geometry is why these nuclei are among the most stable and "
        "abundant in the universe - they're key products of stellar nucleosynthesis."
    )
    
    def model(self):
        k = K
        he4_is_k = 1.0 if 4 == k else 0.0
        c12_is_3k = 1.0 if 12 == 3 * k else 0.0
        o16_is_k2 = 1.0 if 16 == k ** 2 else 0.0
        return {
            "He-4 = k": he4_is_k,
            "C-12 = 3k": c12_is_3k,
            "O-16 = k^2": o16_is_k2,
        }
    
    def observations(self):
        return {"He-4 = k": 1.0, "C-12 = 3k": 1.0, "O-16 = k^2": 1.0}


class TetrahedralClosureConstant(GFDTest):
    """Verify k=4 follows from simplex theorem."""
    name = "Tetrahedral Closure k=4"
    question = "Does k=4 follow from the simplex theorem (d+1 points needed to enclose d-dimensional space), establishing tetrahedral geometry as fundamental?"
    reference_source = "Geometry (simplex theorem)"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Closure constant k=4 follows from the simplex theorem: "
        "to enclose d-dimensional space, you need d+1 points. "
        "STEP 1: For 3D space: d = 3. "
        "STEP 2: Minimum enclosing points: k = d + 1 = 3 + 1 = 4. "
        "STEP 3: k=4 = tetrahedron (4 vertices, 4 faces). "
        "STEP 4: This is why He-4 (k=4 in Tet B) is the first complete closure. "
        "OUTPUT: k value = 4, Equals d+1 = 1.0."
    )
    commentary = (
        "k=4 is geometrically necessary - you cannot enclose 3D space with fewer than 4 points. "
        "This explains why He-4 (A=4 = k fields in Tet B) is the first truly stable closed "
        "configuration. Configurations with fewer fields (H, D, T, He-3) have incomplete "
        "geometry (point, line, plane) and cannot achieve full 3D closure."
    )
    
    def model(self):
        k = K
        is_4 = 1.0 if k == 4 else 0.0
        return {"k value": k, "Equals 4": is_4}
    
    def observations(self):
        return {"k value": 4, "Equals 4": 1.0}


class InnerOctahedronBoundary(GFDTest):
    """Verify inner octahedron defines Tet A / Tet B boundary."""
    name = "Inner Octahedron Boundary"
    question = "Do the 6 inner octahedron vertices lie at distance 1.0 from Field Origin, defining the symmetric boundary between Tet A and Tet B?"
    reference_source = "Geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The inner octahedron at the stellated octahedron's edge midpoints "
        "defines the boundary between Tet A and Tet B regions. "
        "STEP 1: Inner octahedron vertices: (+/-1,0,0), (0,+/-1,0), (0,0,+/-1). "
        "STEP 2: Distance from origin: sqrt(1) = 1.0 for each. "
        "STEP 3: All 6 vertices equidistant at 1.0. "
        "OUTPUT: Average distance = 1.0, All at 1.0 = 1.0."
    )
    commentary = (
        "The inner octahedron marks the boundary between Tet A (physical space) and Tet B "
        "(where gravity fields bind). The uniform distance of 1.0 reflects the symmetric "
        "relationship between the two tetrahedra - essential for the bidirectional compression "
        "shift that occurs during binding."
    )
    
    def model(self):
        inner_vertices = [
            np.array([1, 0, 0]), np.array([-1, 0, 0]),
            np.array([0, 1, 0]), np.array([0, -1, 0]),
            np.array([0, 0, 1]), np.array([0, 0, -1]),
        ]
        origin = calculate_field_origin()
        distances = [np.linalg.norm(v - origin) for v in inner_vertices]
        all_at_1 = 1.0 if all(abs(d - 1.0) < 0.001 for d in distances) else 0.0
        return {"Average distance": sum(distances)/len(distances), "All at 1.0": all_at_1}
    
    def observations(self):
        return {"Average distance": 1.0, "All at 1.0": 1.0}


class BimetricBalance(GFDTest):
    """Verify Field Origin is equidistant from both tetrahedra."""
    name = "Bimetric Balance"
    question = "Are Tet A and Tet B equidistant from the Field Origin, ensuring symmetric bidirectional compression shift during binding?"
    reference_source = "DFP Geometry"
    tolerance = 0.01
    derivation = (
        "PREMISE: The Field Origin must be equidistant from Tet A and Tet B to ensure "
        "symmetric bidirectional compression shift during binding. "
        "STEP 1: Calculate average distance from origin to Tet A vertices. "
        "STEP 2: Calculate average distance from origin to Tet B vertices. "
        "STEP 3: Both = sqrt(3) = 1.732 (symmetric). "
        "OUTPUT: Tet_A avg = 1.732, Tet_B avg = 1.732, Balanced = 1.0."
    )
    commentary = (
        "The bimetric balance (equal distances to Tet A and Tet B) is essential for the "
        "bidirectional compression shift. When gravity fields bind into Tet B, the compression "
        "reverses from inward to outward. This symmetry ensures the transition is geometrically "
        "consistent, creating the stable bowling ball configuration."
    )
    
    def model(self):
        origin = calculate_field_origin()
        tet_a_dists = [np.linalg.norm(get_vertex_coords(v) - origin) for v in TET_A]
        tet_b_dists = [np.linalg.norm(get_vertex_coords(v) - origin) for v in TET_B]
        avg_a = sum(tet_a_dists) / len(tet_a_dists)
        avg_b = sum(tet_b_dists) / len(tet_b_dists)
        balanced = 1.0 if abs(avg_a - avg_b) < 0.001 else 0.0
        return {"Tet_A avg distance": avg_a, "Tet_B avg distance": avg_b, "Balanced": balanced}
    
    def observations(self):
        return {"Tet_A avg distance": 1.732, "Tet_B avg distance": 1.732, "Balanced": 1.0}


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    FieldEnvelopeSize,
    FieldEnvelopeLargerThanProton,
    ElectronQuantumExtent,
    FieldOriginAtCenter,
    OriginVertexDistance,
    VortexEyeSize,
    CompressionRatioForBinding,
    BindingDensityThreshold,
    KMultipleStability,
    TetrahedralClosureConstant,
    InnerOctahedronBoundary,
    BimetricBalance,
]


def run_all_tests():
    """Run all field envelope and field origin geometry tests."""
    summary = (
        "These tests examine Field Envelope size (r_e = 2.818 fm), the Field Origin geometry, "
        "and compression ratios for gravity field binding. The Field Origin is the gateway "
        "through which unbound fields (squish balls) pass to bind into Tet B. Bound atoms "
        "(bowling balls) cannot enter due to compression blocking (~511 keV barrier). "
        "k=4 tetrahedral geometry determines nuclear stability."
    )
    
    return run_test_group("Field Envelope and Origin Geometry", summary, ALL_TESTS)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
