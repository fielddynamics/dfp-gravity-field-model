# FILENAME: test_face_vertex_chamber_consistency.py

"""
Face Vertex Chamber Consistency Across the Stellated Octahedron
===============================================================

The stellated octahedron (Merkaba) is built from two interlocking tetrahedra,
TET_A and TET_B, each with 4 triangular faces. These faces serve as Coupling
Ports in the GFM framework: the interfaces through which gravitational field
closure operates. For the coupling port mechanism to be self consistent, every
face of TET_A must contain only TET_A vertices, and every face of TET_B must
contain only TET_B vertices. This is a cross check between two independent
definitions in the codebase: the FACES dictionary (which lists vertex triples)
and the TET_A/TET_B sets (which partition the 8 vertices by parity). Standard
combinatorics on the cube confirms that any triangle connecting three vertices
of the same parity class forms a face of one of the two embedded tetrahedra.

GFM OBSERVATION: All 8 faces have vertices exclusively from their parent tetrahedron.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES,
)


class FaceVertexChamberConsistency(Test):
    """
    PHYSICAL CONTEXT:
    In the stellated octahedron, each tetrahedron has 4 triangular faces
    that act as Coupling Ports for field closure. The face definitions
    (stored in the FACES dictionary) list three vertices per face. The
    tetrahedron membership definitions (TET_A and TET_B) assign each of
    the 8 vertices to one chamber based on binary popcount parity. These
    two definitions originate from different aspects of the geometry:
    FACES from the triangular decomposition of each tetrahedron, and
    TET_A/TET_B from the parity partition of the cube. For the model to
    be internally consistent, every vertex in a TET_A face must belong
    to TET_A, and every vertex in a TET_B face must belong to TET_B.
    A single violation would mean a Coupling Port straddles both chambers,
    breaking the clean separation that the bimetric coupling topology
    requires. This test also verifies the 3+1 split: 6 SPATIAL faces
    and 2 TIME faces, which underpins the spin derivation (S = hbar/2)
    and the uncertainty principle factor. The face count of 8 total
    equals 2K for K=4, and the TIME face fraction 2/8 = 1/4 appears
    in multiple GFM results.

    GFM OBSERVATION:
    All 8 faces (4 per tetrahedron) contain vertices exclusively from
    their parent chamber. The face count splits as 6 SPATIAL + 2 TIME,
    giving a TIME fraction of 2/8. Zero faces have mixed chamber membership.

    EPISTEMIC STATUS:
    This is a structural cross check between two independent definitions
    in the GFM codebase. It validates internal consistency, not external
    physics. The result follows from combinatorics once parity based
    membership is assumed. It is an observation, not a derivation.
    """

    name = "Face Vertex Chamber Consistency"

    question = (
        "Do all 8 Coupling Port faces of the stellated octahedron contain "
        "vertices exclusively from their parent tetrahedron? The FACES "
        "dictionary and the TET_A/TET_B sets are defined independently. "
        "If any face contained a vertex from the wrong chamber, that "
        "Coupling Port would bridge both metric sectors simultaneously, "
        "violating the clean bimetric separation. How many of the 8 faces "
        "pass this membership check, and does the SPATIAL/TIME split yield "
        "exactly 6 and 2?"
    )

    reference = (
        "Coxeter (1973), Regular Polytopes: vertex partition of the cube "
        "into two tetrahedra; GFM framework FACES and TET_A/TET_B definitions"
    )

    tolerance = 0.01

    level = Level.STANDARD

    commentary = (
        "This test bridges vertex level and face level structural validation. "
        "The partition tests confirmed TET_A and TET_B are disjoint and "
        "exhaustive. The complementary pair test confirmed XOR 7 crosses "
        "chambers. This test now checks the next layer: that faces, which "
        "are the actual coupling interfaces in the traversal algorithm, "
        "respect the chamber boundary established by vertex parity. The "
        "additional check on the 6 SPATIAL + 2 TIME decomposition validates "
        "the face classification that feeds into the spin derivation "
        "(S = 2/8 * 2*hbar = hbar/2) and the G formula numerator "
        "(17 = 16 face face couplings + 1). This is an observation about "
        "internal consistency of definitions, not a derivation of new physics."
    )

    # Audit scoring
    audit_score = 82
    audit_notes = (
        "Question: 12/15 (clearly states the cross check and physical stakes of a violation, but leads with the mechanism rather than a mystery hook; opening with the consequence, what breaks if a face straddles chambers, before describing the check would sharpen curiosity). Derivation: 11/15 (logical progression from combinatorics through definitions to the cross check, includes a concrete example with FACE_A1, but lacks the PHYSICAL SETUP then TENSION then INSIGHT arc; jumps into definitions without first painting the intuitive picture of why faces must be pure, and no analogy is offered to ground the abstraction). Commentary: 12/15 (good connection to prior tests forming a validation chain, explicitly links the 6/2 split to spin and the G formula numerator, honest epistemic labeling, but restates the test structure more than delivering an aha moment; missing an analogy or implication statement about what we can now trust). Model: 9/10 (clean set of 6 summary values, good mix of counts and a ratio, all floats, easy to interpret at a glance; the only minor note is that 6 values is toward the upper end for a purely structural check). Observations: 7/10 (all expected values are mathematically justified from the geometry, Coxeter citation is appropriate, but the observed values are entirely internal definitions rather than externally traceable measurements, which is inherent to the test type but limits traceability; no CODATA or experimental source applies here). Constants: 9/10 (K, TET_A, TET_B, FACES, TIME_FACES, SPATIAL_FACES all imported from common; the literal 8 appears in the observations but equals 2*K which is documented; minor note that the number 3 for vertex count per face is implicit rather than derived from an imported constant, though importing it would be overkill). Accessibility: 12/15 (graduate level accessible, explains popcount parity, builds logically from vertex to face level, connects to downstream results like spin; but assumes familiarity with bimetric gravity and coupling ports without grounding analogies, and terms like Coupling Port and chamber boundary are used before being motivated for a newcomer). Header: 10/10 (comprehensive module docstring covering the physical domain, the specific cross check being performed, explicit GFM OBSERVATION label, honest epistemic status, clear scope connecting FACES to TET_A/TET_B, and notes the standard combinatorics basis)."
    )

    academic_paper = """\
TITLE Face Vertex Chamber Consistency: Cross Checking Coupling Port Membership Against Tetrahedron Partition in the Stellated Octahedron ABSTRACT This investigation checks whether all 8 triangular faces of the stellated octahedron contain vertices exclusively from their parent tetrahedron. The model finds 8 consistent faces, 0 violations, and a SPATIAL/TIME split of 6/2. This is documented as a structural OBSERVATION confirming internal consistency. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The stellated octahedron consists of two interlocking regular tetrahedra whose 8 vertices occupy the corners of a cube. In the GFM framework, each tetrahedron represents one sector of a bimetric gravitational structure, and the triangular faces serve as Coupling Ports: the interfaces through which field closure operates. Prior structural tests have validated that the vertex sets TET_A and TET_B form a disjoint, exhaustive partition of the 8 vertices based on binary popcount parity, and that complementary pairs under XOR 7 always cross between chambers. However, vertex level consistency does not automatically guarantee face level consistency. The FACES dictionary, which assigns three vertices to each of the 8 triangular faces, is defined independently from the TET_A and TET_B membership sets. If any face contained vertices from both tetrahedra, that Coupling Port would straddle the two metric sectors, breaking the clean bimetric separation the framework requires. Standard combinatorics on the cube predicts that triangles connecting three vertices of the same parity class must form faces of one embedded tetrahedron. This test verifies that prediction against the concrete definitions in the codebase. It also checks the classification of faces into 6 SPATIAL and 2 TIME faces, a split that feeds into the spin derivation (S = hbar/2) and the G formula numerator (17 = 16 face to face couplings + 1). 2. METHODOLOGY The model iterates over all 8 entries in the FACES dictionary. For each face, it tests whether all three vertices belong to TET_A or all three belong to TET_B. Faces satisfying this condition are counted as consistent. Faces with mixed membership are counted as violations. Separately, the model counts the elements of TIME_FACES and SPATIAL_FACES and computes the TIME face fraction as the ratio of TIME faces to total faces. Agreement is defined as 8 consistent faces, 0 violations, 6 SPATIAL faces, 2 TIME faces, and a TIME fraction of 0.25, with tolerance of 1 percent. 3. RESULTS Model output: Consistent faces: 8.0 Violation faces: 0.0 Spatial face count: 6.0 Time face count: 2.0 Total face count: 8.0 Time face fraction: 0.25 Expected values: Consistent faces: 8.0 Violation faces: 0.0 Spatial face count: 6.0 Time face count: 2.0 Total face count: 8.0 Time face fraction: 0.25 All six quantities match exactly. Every face contains vertices exclusively from its parent tetrahedron. The SPATIAL/TIME decomposition yields 6 and 2 respectively, summing to 8 = 2K for K = 4. 4. DISCUSSION The result confirms that the face level geometry is fully consistent with the vertex level partition. No Coupling Port straddles both metric sectors. This means the traversal algorithm, which tracks face completion by accumulating vertex visits, can unambiguously assign each face completion event to one tetrahedron. The 6/2 SPATIAL/TIME split is particularly significant downstream. The TIME face fraction 2/8 = 1/4 appears in the spin derivation, where only the fraction of angular momentum passing through TIME faces constitutes intrinsic spin: S = (2/8) times 2 hbar = hbar/2. The same ratio appears in the uncertainty principle bound. The total face count of 8 = 2K connects to the 16 face to face coupling channels (8 times 8 divided by 4 for symmetry) that, together with the Field Origin, produce the factor 17 in the gravitational constant formula. EPISTEMIC STATUS: OBSERVATION. This is a structural cross check between independently defined data structures. The result follows from combinatorics once parity based membership is assumed. We observe consistency rather than deriving new physics. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that the stellated octahedron is physically realized or that bimetric gravity is correct. It validates internal consistency of definitions, not correspondence with experiment. The FACES and TET sets could both be wrong in a way that preserves mutual consistency. The downstream significance of the 6/2 split depends on the spin and G derivations being independently
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD COMBINATORICS: A cube with vertices labeled 0 through 7 "
                "in 3 bit binary admits exactly two embedded regular tetrahedra, "
                "one at odd parity vertices and one at even parity vertices."
            )
            .step(
                "GFM DEFINITION: TET_A = {1, 2, 4, 7} (odd popcount), "
                "TET_B = {0, 3, 5, 6} (even popcount). Each tetrahedron has "
                "4 triangular faces, for 8 faces total."
            )
            .step(
                "GFM DEFINITION: The FACES dictionary maps face labels to "
                "sets of 3 vertices. For example, FACE_A1 = {2, 4, 7} contains "
                "only TET_A vertices (popcount 1, 1, 3: all odd)."
            )
            .step(
                "CROSS CHECK: For each of the 8 faces, test whether all 3 "
                "vertices belong to the same tetrahedron. Count consistent "
                "faces and violations independently."
            )
            .equation(
                "consistent_faces + violation_faces = 8 = total faces = 2*K"
            )
            .step(
                "FACE CLASSIFICATION CHECK: TIME_FACES should contain exactly "
                "2 faces (FACE_A7 and FACE_B0). SPATIAL_FACES should contain "
                "exactly 6 faces. Together they sum to 8."
            )
            .equation("SPATIAL_FACES + TIME_FACES = 6 + 2 = 8 = 2*K")
            .step(
                "The TIME face fraction 2/8 = 1/4 is the geometric ratio that "
                "appears in the spin derivation and the uncertainty principle."
            )
            .conclude(
                "If all 8 faces pass the membership check with 0 violations, "
                "and the SPATIAL/TIME split is exactly 6/2, the face level "
                "structure is confirmed as internally consistent with the "
                "vertex level partition."
            )
        )

    def model(self) -> Model:
        consistent_count = 0
        violation_count = 0

        for face_label, face_vertices in FACES.items():
            all_in_a = all(v in TET_A for v in face_vertices)
            all_in_b = all(v in TET_B for v in face_vertices)
            if all_in_a or all_in_b:
                consistent_count += 1
            else:
                violation_count += 1

        num_time = len(TIME_FACES)
        num_spatial = len(SPATIAL_FACES)
        total_faces = len(FACES)

        time_fraction = num_time / total_faces if total_faces > 0 else 0.0

        return (
            Model()
            .add("Consistent faces", float(consistent_count))
            .add("Violation faces", float(violation_count))
            .add("Spatial face count", float(num_spatial))
            .add("Time face count", float(num_time))
            .add("Total face count", float(total_faces))
            .add("Time face fraction", time_fraction)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Consistent faces", 8.0)
            .add("Violation faces", 0.0)
            .add("Spatial face count", 6.0)
            .add("Time face count", 2.0)
            .add("Total face count", 8.0)
            .add("Time face fraction", 0.25)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Face Vertex Chamber Consistency",
        summary="Verifies that all 8 Coupling Port faces contain vertices exclusively from their parent tetrahedron and that the SPATIAL/TIME split is 6/2",
        test_classes=[FaceVertexChamberConsistency],
    )
