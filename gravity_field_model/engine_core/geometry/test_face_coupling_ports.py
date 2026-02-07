# FILENAME: test_face_coupling_ports.py

"""
Face Coupling Ports: The 3+1 Spatial vs Time Face Structure
============================================================

The stellated octahedron has 8 triangular faces: 4 on each tetrahedron.
Each face is a "coupling port" through which field interactions propagate.
Standard geometry determines these faces from the vertex sets. The key
structural fact is that exactly 2 of the 8 faces are TIME faces (those
opposite the temporal apex vertices V7 and V0), while the remaining 6
are SPATIAL faces. This 2:6 ratio, equivalently 1:3, mirrors the 3+1
decomposition of spacetime. In the GFM framework, this face ratio is
the geometric origin of the factor 1/2 in electron spin (S = hbar/2)
and the uncertainty principle minimum (Delta_x Delta_p >= hbar/2).

GFM OBSERVATION: The fraction 2/8 = 1/4 of time faces produces S = (2/8)*2*hbar = hbar/2.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES,
    HBAR,
)


class FaceCouplingPortStructure(Test):
    """
    PHYSICAL CONTEXT:
    A tetrahedron has exactly 4 triangular faces, each defined by the 3
    vertices opposite the excluded vertex. For two tetrahedra embedded in
    a cube (the stellated octahedron), the total face count is 8. In the
    GFM framework, each face serves as a coupling port for field closure.
    The distinction between spatial and time faces arises from the role of
    apex vertices V7 (111) and V0 (000), which define the temporal axis
    of the structure. Faces opposite these apexes are TIME faces; the
    remaining faces are SPATIAL faces.

    GFM OBSERVATION:
    The face partition is 6 spatial + 2 time = 8 total. The time face
    fraction 2/8 = 1/4 appears in the spin derivation S = (2/8)*2*hbar
    = hbar/2, and in the uncertainty principle bound Delta_x*Delta_p
    >= hbar/2. The ratio 6:2 = 3:1 mirrors the 3+1 spacetime split.

    EPISTEMIC STATUS:
    The face count and spatial/time classification are geometric facts
    (derivations from vertex definitions). The connection to spin and
    the uncertainty principle is an observation: GFM notes the numeric
    correspondence but the logical chain from face ratio to hbar/2
    remains a pattern, not a first principles proof.
    """

    name = "Face Coupling Port Structure: 6 Spatial + 2 Time"

    question = (
        "Why does the stellated octahedron have exactly 6 spatial faces "
        "and 2 time faces? Each tetrahedron has 4 faces, giving 8 total. "
        "The time faces are those opposite the apex vertices V7 and V0 "
        "(the endpoints of the temporal body diagonal). Does the resulting "
        "fraction 2/8 = 1/4 have physical significance, given that "
        "electron spin S = hbar/2 = (2/8) * 2 * hbar?"
    )

    reference = (
        "Coxeter (1973), Regular Polytopes; "
        "GFM Paper VI Section 7 (spin derivation); "
        "GFM Paper VII Section 5.2 (uncertainty principle); "
        "GFM Textbook Chapter 9 Section 9.2 (face definitions)"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "Standard geometry fixes the face count at 4 per tetrahedron, 8 total. "
        "The classification into spatial and time faces follows from identifying "
        "V0 and V7 as temporal apexes: they sit at opposite ends of the body "
        "diagonal (minus1,minus1,minus1) to (plus1,plus1,plus1), the unique axis "
        "connecting the two tetrahedral apex vertices. Faces opposite these apexes "
        "are time faces. This gives 6 spatial + 2 time, a 3:1 ratio matching "
        "the 3+1 spacetime signature. GFM observes that the time face fraction "
        "2/8 = 1/4 appears as the geometric factor converting total angular "
        "momentum (2*hbar) into intrinsic spin (hbar/2). This is an observation "
        "not a derivation: the face ratio is exact, and the numerical match to "
        "spin is exact, but the causal mechanism linking face geometry to angular "
        "momentum filtering requires further development."
    )

    # Audit scoring
    audit_score = 87
    audit_notes = (
        "Question: 13/15 (asks why with specific numbers and connects to spin, but the multi part structure slightly dilutes the central mystery hook; could sharpen by leading with the spin puzzle rather than the face count). Derivation: 13/15 (good intuition first structure, clear progression from geometry to physics, but the L = 2*hbar assumption at step 7 appears without justification; one quantum per tetrahedron needs scaffolding). Commentary: 12/15 (honest about epistemic status, clearly states observation not derivation, good connection to 3+1 spacetime; lacks an analogy for accessibility and does not state broader implications beyond spin). Model: 9/10 (clean summary with 8 well chosen values, binary and ratio outputs, no raw dumps; the spatial_per_tet computation has a dead variable spatial_per_tet that is computed but unused, minor clutter). Observations: 9/10 (all values are geometric facts or CODATA derived via HBAR import; Coxeter and GFM papers cited explicitly; could note that spin = hbar/2 is experimentally measured via Stern Gerlach 1922). Constants: 10/10 (HBAR imported from common, K and geometry constants imported, no hardcoded physics constants, derived constants documented inline). Accessibility: 13/15 (undergrad can follow the face counting and ratio logic, the 3+1 connection is intuitive; the leap to angular momentum filtering assumes familiarity with vortex structure that is not explained, and the term coupling port is used without a simple analogy). Header: 8/10 (module docstring covers the physical domain, states what is tested, clearly marks observation vs derivation, cites references; missing explicit target audience level and could benefit from a sentence on what is NOT covered)."
    )

    academic_paper = """\
TITLE Face Coupling Ports of the Stellated Octahedron: The 6+2 Spatial and Time Face Partition ABSTRACT We investigate the face structure of two interpenetrating tetrahedra inscribed in a cube. The 8 triangular faces partition into 6 spatial and 2 time faces, a ratio determined by vertex parity and the temporal axis. All 8 model quantities match geometric expectations exactly (0.00% error). The time face fraction 2/8 = 1/4 corresponds numerically to the factor producing electron spin S = hbar/2. 1. INTRODUCTION: THE SCIENTIFIC QUESTION Electron spin takes the value hbar/2. The Stern Gerlach experiment (1922) established this as an empirical fact, and the Dirac equation (1928) produces it from relativistic quantum mechanics. Yet neither framework explains why the fraction 1/2 appears. The factor is built into the formalism rather than derived from a deeper structure. The Gravity Field Model constructs spacetime geometry from a stellated octahedron: two regular tetrahedra whose 8 vertices occupy the corners of a cube, partitioned by bit parity into Tet A = {1,2,4,7} and Tet B = {0,3,5,6}. Each tetrahedron has 4 triangular faces, yielding 8 faces total. These faces serve as coupling ports through which field closure propagates. A natural classification arises from the temporal axis. Vertices V0 = (minus1,minus1,minus1) and V7 = (plus1,plus1,plus1) sit at the apex of each tetrahedron and define the unique body diagonal connecting both tips. The faces opposite these apexes, Face_A7 = {1,2,4} and Face_B0 = {3,5,6}, point inward toward the Field Origin. These are the time faces. The remaining 6 faces point outward and are spatial. This test investigates whether the resulting partition is geometrically forced and whether the time face fraction 2/8 = 1/4 corresponds to the spin factor. 2. METHODOLOGY We construct all 8 faces algorithmically from the vertex sets TET_A and TET_B by enumerating the 3 vertex subsets opposite each excluded vertex. We identify time faces as those opposite the apex vertices V7 (in Tet A) and V0 (in Tet B). We compute the time face fraction, the spatial to time ratio, and the spin value S = (N_time/N_total) * 2 * hbar. All quantities are compared against geometric expectations. Agreement criterion: 0.00% error for exact geometric identities. 3. RESULTS All 8 model outputs match observations exactly: Total faces: 8 (expected 8, 0.00% error). Faces per tetrahedron: 4 (expected 4, 0.00% error). Time faces: 2 (expected 2, 0.00% error). Spatial faces: 6 (expected 6, 0.00% error). Time face fraction: 0.250000 (expected 0.25, 0.00% error). Spatial to time ratio: 3.0 (expected 3.0, 0.00% error). Spin from face ratio: 5.273e-35 J s (expected hbar/2 = 5.273e-35 J s, 0.00% error). Spatial faces per tetrahedron: 3.0 (expected 3.0, 0.00% error). The 3:1 spatial to time ratio reproduces per tetrahedron as well: each contributes 3 spatial faces and 1 time face, replicating the d + 1 = 3 + 1 pattern within each chamber independently. 4. DISCUSSION The face partition 6 + 2 = 8 is a geometric theorem, not a parameter choice. Once the temporal axis is identified through the complementary apex pair (V0, V7), the classification follows necessarily. The 3:1 ratio of spatial to time faces matches the 3:1 ratio of spatial to temporal dimensions in 3+1 spacetime exactly. The physically significant observation is that the time face fraction 2/8 = 1/4, applied to a total angular momentum of 2*hbar (one quantum per tetrahedron), yields S = hbar/2. This matches the experimentally measured electron spin. The correspondence is exact, not approximate. We document this as an observation: the face ratio is a geometric fact, and its numerical agreement with the spin factor is exact, but the causal mechanism connecting face geometry to angular momentum filtering requires further development. 5. SCOPE AND ASSUMPTIONS The classification assumes V0 and V7 define the temporal axis, following from their role as tetrahedral apexes and complementary pair endpoints. The assignment L = 2*hbar (one quantum per tetrahedron) is assumed, not derived. Establishing this total angular momentum from first principles would elevate the spin result from observation to derivation. 6. CONCLUSION The stellated octahedron partitions into exactly 6 spatial and 2 time faces, a result forced by vertex parity and the temporal axis. The time face fraction 1/4 matches the spin factor in S
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD GEOMETRY: A tetrahedron with vertices {a,b,c,d} has "
                "4 faces, each formed by omitting one vertex. Face opposite vertex "
                "x consists of the remaining 3 vertices."
            )
            .step(
                "Tet A = {1,2,4,7} has faces: {2,4,7}, {1,4,7}, {1,2,7}, {1,2,4}. "
                "Tet B = {0,3,5,6} has faces: {3,5,6}, {0,5,6}, {0,3,6}, {0,3,5}."
            )
            .equation("N_faces_total = 4 + 4 = 8")
            .step(
                "TEMPORAL AXIS IDENTIFICATION: V0 = (minus1,minus1,minus1) and "
                "V7 = (plus1,plus1,plus1) are the apex vertices of Tet B and Tet A "
                "respectively. They form a complementary pair (0+7=7) and define "
                "the unique body diagonal connecting both tetrahedral tips."
            )
            .step(
                "TIME FACES are those opposite the apex vertices: "
                "Face_A7 = {1,2,4} (opposite V7 in Tet A) and "
                "Face_B0 = {3,5,6} (opposite V0 in Tet B). "
                "All other 6 faces are SPATIAL."
            )
            .equation("N_time = 2, N_spatial = 6, ratio = 6:2 = 3:1")
            .step(
                "GFM OBSERVATION: The time face fraction is 2/8 = 1/4. "
                "If total angular momentum in the vortex structure is L = 2*hbar "
                "(one quantum per tetrahedron), and only the time face fraction "
                "passes through the Field Origin, then S = (2/8)*2*hbar = hbar/2."
            )
            .equation("S = (N_time / N_total) * L_total = (2/8) * 2*hbar = hbar/2")
            .step(
                "CROSS CHECK: The 3:1 ratio of spatial to time faces equals the "
                "3:1 ratio of spatial to temporal dimensions in 3+1 spacetime. "
                "Each tetrahedron contributes 3 spatial faces + 1 time face, "
                "replicating the (d) + (1) = (3) + (1) pattern per chamber."
            )
            .conclude(
                "The face structure is geometrically determined: 6 spatial + 2 time "
                "= 8 total faces. The time fraction 2/8 = 1/4 numerically matches "
                "the factor that converts L = 2*hbar to S = hbar/2. The 3+1 pattern "
                "per tetrahedron (3 spatial faces + 1 time face) mirrors spacetime."
            )
        )

    def model(self) -> Model:
        # Count faces per tetrahedron from vertex sets
        def faces_of_tet(tet_vertices):
            vlist = sorted(tet_vertices)
            faces = []
            for i in range(len(vlist)):
                face = set(vlist[:i] + vlist[i+1:])
                faces.append(face)
            return faces

        faces_a = faces_of_tet(list(TET_A))
        faces_b = faces_of_tet(list(TET_B))
        all_faces = faces_a + faces_b

        n_faces_total = float(len(all_faces))
        n_faces_per_tet = float(len(faces_a))

        # Identify time faces: opposite V7 in Tet A, opposite V0 in Tet B
        # Face opposite V7 in Tet A = Tet A minus {7}
        face_a7 = TET_A - {7}
        face_b0 = TET_B - {0}

        # Count time faces among all computed faces
        n_time = 0.0
        for f in all_faces:
            if f == face_a7 or f == face_b0:
                n_time += 1.0

        n_spatial = n_faces_total - n_time

        # Time face fraction
        time_fraction = n_time / n_faces_total

        # Spatial to time ratio
        spatial_to_time_ratio = n_spatial / n_time

        # Spin computation: S = (n_time / n_total) * 2 * hbar
        spin_computed = time_fraction * 2.0 * HBAR

        # Spatial faces per tetrahedron
        spatial_per_tet = (n_faces_per_tet * n_faces_total - n_time) / 2.0
        # Simpler: each tet has 4 faces, 1 is time, so 3 spatial
        spatial_per_tet_direct = n_faces_per_tet - (n_time / 2.0)

        return (
            Model()
            .add("Total faces", n_faces_total)
            .add("Faces per tetrahedron", n_faces_per_tet)
            .add("Time faces", n_time)
            .add("Spatial faces", n_spatial)
            .add("Time face fraction", time_fraction)
            .add("Spatial to time ratio", spatial_to_time_ratio)
            .add("Spin from face ratio (J s)", spin_computed)
            .add("Spatial faces per tetrahedron", spatial_per_tet_direct)
        )

    def observations(self) -> Observed:
        spin_expected = 0.5 * HBAR

        return (
            Observed()
            .add("Total faces", 8.0)
            .add("Faces per tetrahedron", 4.0)
            .add("Time faces", 2.0)
            .add("Spatial faces", 6.0)
            .add("Time face fraction", 0.25)
            .add("Spatial to time ratio", 3.0)
            .add("Spin from face ratio (J s)", spin_expected)
            .add("Spatial faces per tetrahedron", 3.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Face Coupling Port Structure: 6 Spatial + 2 Time",
        summary="Verifies the 6 spatial / 2 time face partition and its connection to spin = hbar/2",
        test_classes=[FaceCouplingPortStructure],
    )
