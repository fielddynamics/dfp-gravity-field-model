# FILENAME: test_historical_time_face_classification.py

"""
TIME Face Classification from Binary Vertex Structure
======================================================

The stellated octahedron has 8 triangular faces: 4 on Tetrahedron A and 4 on
Tetrahedron B. Each face is defined by the 3 vertices it contains, or equivalently,
by the single vertex it omits (the apex opposite that face). Standard geometry
classifies faces by their relationship to the structure's principal axis. In the
GFM framework, 2 of the 8 faces are designated TIME faces and 6 are SPATIAL faces.

The TIME faces are those opposite the binary extrema V0 (000) and V7 (111), the
vertices with popcount 0 and 3 respectively. The SPATIAL faces are opposite the
six vertices with intermediate popcount (1 or 2). This 6:2 partition arises
purely from the combinatorics of the 3 bit binary encoding and the definition
of "extremal" popcount in d=3 dimensions.

GFM OBSERVATION: The TIME face fraction 2/8 = 1/4 appears in the spin formula
S = (2/8) * 2*hbar = hbar/2 and in the uncertainty bound hbar/2.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B,
)
from gravity_field_model.common.geometry_constants import (
    FACES, TIME_FACES, SPATIAL_FACES,
)


class TimeFaceClassificationFromBinary(Test):
    """
    PHYSICAL CONTEXT:
    A tetrahedron in 3D has 4 triangular faces. Two interlocking tetrahedra
    forming a stellated octahedron therefore produce 8 faces total. Each face
    can be uniquely identified by the one vertex of its parent tetrahedron that
    it does NOT contain (the opposite apex). In standard polyhedral geometry,
    faces related to extremal vertices along the principal diagonal have special
    status because they are perpendicular to the axis of maximal spatial extent.

    GFM OBSERVATION:
    The 8 faces partition into 6 SPATIAL and 2 TIME faces. The TIME faces are
    FACE_A7 (opposite V7 = 111, popcount 3) and FACE_B0 (opposite V0 = 000,
    popcount 0). These are the only faces opposite vertices with extremal
    popcount (0 or d). The ratio 2/8 = 1/4 is the same factor that appears
    in the GFM spin derivation S = hbar/2 and the uncertainty principle bound.

    EPISTEMIC STATUS:
    The 6:2 partition is a geometric derivation from binary combinatorics.
    The connection to spin and uncertainty is an observation, not a derivation.
    """

    name = "TIME Face Classification from Binary Structure"

    question = (
        "Why are exactly 2 of the 8 stellated octahedron faces classified as "
        "TIME faces? The answer lies in the binary encoding: in d=3 dimensions, "
        "only 2 of the 8 vertices have extremal popcount (0 ones or 3 ones). "
        "These are V0 = 000 and V7 = 111. The faces opposite these extremal "
        "vertices become the TIME faces, yielding the ratio 2/8 = 1/4 that "
        "appears throughout GFM as the time fraction of the geometry."
    )

    reference = (
        "GFM Textbook Ch.9 Sec.9.4: Face classification and 3+1 structure; "
        "Coxeter (1973) Regular Polytopes: stellated octahedron face geometry"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "In d dimensions, the number of d bit strings with popcount 0 is 1, "
        "and the number with popcount d is 1, giving exactly 2 extremal vertices "
        "out of 2^d total. For d=3 this yields 2 TIME faces out of 8 total faces. "
        "The remaining 6 faces are SPATIAL: their opposite vertices have popcount "
        "1 (three vertices: V1, V2, V4) or popcount 2 (three vertices: V3, V5, V6). "
        "This 6:2 ratio is equivalent to the 3:1 ratio per tetrahedron (3 SPATIAL "
        "faces plus 1 TIME face), which encodes the 3+1 spacetime signature. "
        "The observation that the same fraction 2/8 = 1/4 appears in the spin "
        "formula is noted but is not derived here from first principles."
    )

    # Audit scoring
    audit_score = 83
    audit_notes = (
        "Question: 11/15 (asks 'why' with specific numbers and the 2/8 ratio, but gives away the answer in the question itself rather than building tension; reads more like a summary than a mystery hook). Derivation: 13/15 (excellent progression from geometry to binary encoding to classification; intuition is built before the equations; minor weakness: the 'PHYSICAL SETUP' and 'TENSION' phases could be more distinct, it moves quickly into enumeration). Commentary: 12/15 (solid interpretation connecting 6:2 to 3+1 per tetrahedron, honest about epistemic status, but lacks an analogy for non experts and does not state broader implications beyond spin). Model: 9/10 (clean summary with 8 well chosen quantities; per tetrahedron breakdown adds value; all floats, easy to interpret). Observations: 7/10 (values are correct geometric facts, but 'observed' is slightly misleading for pure combinatorics; Coxeter citation is appropriate but the GFM Textbook Ch.9 is an internal reference not externally verifiable). Constants: 8/10 (K, VERTICES, TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES all imported from common; d=3 is used as a literal which is correct per rules; however FACES, TIME_FACES, SPATIAL_FACES are imported but never directly used in model() computation, which relies on recomputation from scratch instead). Accessibility: 13/15 (undergrads can follow the binary popcount logic; the step from popcount to face classification is clearly explained; 'extremal popcount' is defined in context; PhD readers gain the combinatorial generalization to arbitrary d; slightly dense in the middle enumeration steps). Header: 10/10 (module docstring covers the physical domain, states what is being investigated, clearly labels the GFM observation, explicitly declares epistemic status as observation not derivation, includes the key reference)."
    )

    academic_paper = """\
TITLE The 3+1 Spacetime Signature from Binary Popcount Extremality in the Stellated Octahedron ABSTRACT We investigate why exactly 2 of the 8 faces of the stellated octahedron are classified as TIME faces. Using binary popcount analysis of the vertex encoding, the model recovers the 6:2 spatial to time partition with 0.00% error across all eight quantities. The TIME face fraction 2/8 = 1/4 is documented as an OBSERVATION appearing elsewhere in GFM. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The stellated octahedron, formed by two interpenetrating tetrahedra, has 8 triangular faces. In the Gravity Field Model, these faces serve as coupling ports through which field closure operates. A fundamental question arises: why do exactly 2 of these 8 faces carry the designation TIME, while the remaining 6 are SPATIAL? This 3+1 decomposition per tetrahedron (3 spatial faces plus 1 time face) mirrors the 3+1 signature of spacetime, but does it emerge from the geometry itself or must it be imposed by hand? Standard polyhedral geometry identifies each face of a tetrahedron by the single vertex it omits: the opposite apex. The stellated octahedron's 8 vertices map naturally to 3 bit binary strings (since 8 = 2^3), with vertex indices running from V0 = 000 to V7 = 111. GFM proposes that the TIME faces are those opposite vertices with extremal popcount, meaning vertices whose binary representation contains either all zeros or all ones. This test investigates whether the 6:2 partition follows purely from binary combinatorics in d = 3 dimensions, requiring no additional assumptions. 2. METHODOLOGY The model enumerates all 8 vertices (indices 0 through 7) and computes the popcount (number of 1 bits) for each. Vertices with popcount equal to 0 or equal to d = 3 are classified as extremal. The face opposite each extremal vertex is labeled TIME; all others are labeled SPATIAL. Counts are computed globally (total TIME and SPATIAL faces) and per tetrahedron (using the parity partition: Tet A = {1, 2, 4, 7}, Tet B = {0, 3, 5, 6}). Agreement is defined as exact match (0.00% error) since all quantities are integers derived from combinatorics. Reference values come from the stellated octahedron geometry as documented by Coxeter (1973). 3. RESULTS The model produces eight quantities, all matching exactly: TIME faces total: model 2, observed 2 (0.00% error). SPATIAL faces total: model 6, observed 6 (0.00% error). Total faces: model 8, observed 8 (0.00% error). TIME fraction: model 0.250000, observed 0.250000 (0.00% error). Tet A TIME faces: model 1, observed 1 (0.00% error). Tet A SPATIAL faces: model 3, observed 3 (0.00% error). Tet B TIME faces: model 1, observed 1 (0.00% error). Tet B SPATIAL faces: model 3, observed 3 (0.00% error). The extremal vertices are V0 = 000 (popcount 0, Tet B) and V7 = 111 (popcount 3, Tet A). Each tetrahedron contributes exactly 1 TIME face and 3 SPATIAL faces, producing the 3+1 structure independently in both chambers. 4. DISCUSSION The 6:2 partition is a combinatorial theorem, not a fitted result. In d dimensions, exactly C(d,0) + C(d,d) = 2 vertices have extremal popcount, regardless of d. For d = 3, this yields 2 TIME faces from 8 total, giving the fraction 1/4. The per tetrahedron decomposition of 3 SPATIAL plus 1 TIME is the 3+1 signature that appears throughout relativistic physics. EPISTEMIC STATUS: The partition itself is a DERIVATION from binary combinatorics. The correspondence between the TIME fraction 2/8 = 1/4 and the factor 1/2 in the spin formula S = (2/8) * 2 * hbar = hbar/2 is an OBSERVATION. We do not derive spin from this counting argument. This test bridges the binary vertex encoding tests (which validate labeling) to the physical content of GFM (which uses the face classification for field closure dynamics). 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that spacetime has 3+1 dimensions. The labeling of faces as TIME versus SPATIAL follows a GFM convention tied to the extremal popcount definition. An independent physical criterion for distinguishing face types would strengthen the result. The connection to electron spin remains an observation requiring further investigation. 6. CONCLUSION Binary popcount extremality in d = 3 dimensions uniquely determines the 6:2 face partition of the stellated octahedron,
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: In a stellated octahedron, each of the "
                "8 faces is uniquely identified by the apex vertex opposite to it. "
                "Tet A has 4 faces, each omitting one of {1, 2, 4, 7}. "
                "Tet B has 4 faces, each omitting one of {0, 3, 5, 6}."
            )
            .step(
                "BINARY ENCODING: Each vertex index 0 through 7 is a 3 bit "
                "binary string. The popcount (number of 1 bits) ranges from 0 to 3."
            )
            .step(
                "EXTREMAL POPCOUNT: Vertices with popcount = 0 or popcount = d = 3 "
                "are the binary extrema. For d=3: V0 = 000 (popcount 0) and "
                "V7 = 111 (popcount 3). These are the only two such vertices."
            )
            .equation("N_extremal = C(d,0) + C(d,d) = 1 + 1 = 2")
            .step(
                "FACE CLASSIFICATION: The face opposite an extremal vertex is a "
                "TIME face. FACE_A7 is opposite V7 (extremal, popcount 3). "
                "FACE_B0 is opposite V0 (extremal, popcount 0)."
            )
            .step(
                "COUNT: 2 TIME faces, 8 total faces, so 6 SPATIAL faces. "
                "Per tetrahedron: 1 TIME face + 3 SPATIAL faces = 3+1 structure."
            )
            .equation("TIME_fraction = 2 / 8 = 0.25")
            .step(
                "INTERMEDIATE POPCOUNT: The 6 SPATIAL face apexes have popcount "
                "1 or 2. Popcount 1: V1(001), V2(010), V4(100) in Tet A. "
                "Popcount 2: V3(011), V5(101), V6(110) in Tet B."
            )
            .step(
                "GFM OBSERVATION: The fraction 2/8 = 1/4 is the same factor "
                "that appears in the spin formula S = (2/8)*2*hbar = hbar/2. "
                "This is noted as a geometric correspondence."
            )
            .conclude(
                "The binary encoding in d=3 uniquely determines 2 TIME faces "
                "and 6 SPATIAL faces, producing the 3+1 decomposition per "
                "tetrahedron and the 1/4 time fraction across the full structure."
            )
        )

    def model(self) -> Model:
        # Classify faces by popcount of their opposite apex vertex
        d = 3

        # Count extremal popcount vertices (popcount = 0 or popcount = d)
        extremal_vertices = []
        intermediate_vertices = []
        for v in range(2**d):
            pc = bin(v).count('1')
            if pc == 0 or pc == d:
                extremal_vertices.append(v)
            else:
                intermediate_vertices.append(v)

        n_time_faces = len(extremal_vertices)
        n_spatial_faces = len(intermediate_vertices)
        n_total_faces = n_time_faces + n_spatial_faces
        time_fraction = n_time_faces / n_total_faces

        # Per tetrahedron counts
        # Tet A extremal apexes: those in TET_A with extremal popcount
        tet_a_time = sum(1 for v in extremal_vertices if v in TET_A)
        tet_a_spatial = len(TET_A) - tet_a_time
        tet_b_time = sum(1 for v in extremal_vertices if v in TET_B)
        tet_b_spatial = len(TET_B) - tet_b_time

        return (
            Model()
            .add("TIME faces total", float(n_time_faces))
            .add("SPATIAL faces total", float(n_spatial_faces))
            .add("Total faces", float(n_total_faces))
            .add("TIME fraction", time_fraction)
            .add("Tet A TIME faces", float(tet_a_time))
            .add("Tet A SPATIAL faces", float(tet_a_spatial))
            .add("Tet B TIME faces", float(tet_b_time))
            .add("Tet B SPATIAL faces", float(tet_b_spatial))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("TIME faces total", 2.0)
            .add("SPATIAL faces total", 6.0)
            .add("Total faces", 8.0)
            .add("TIME fraction", 0.25)
            .add("Tet A TIME faces", 1.0)
            .add("Tet A SPATIAL faces", 3.0)
            .add("Tet B TIME faces", 1.0)
            .add("Tet B SPATIAL faces", 3.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="TIME Face Classification from Binary Vertex Structure",
        summary=(
            "Derives the 6 SPATIAL + 2 TIME face partition from binary "
            "popcount extremality in d=3 dimensions"
        ),
        test_classes=[TimeFaceClassificationFromBinary],
    )
