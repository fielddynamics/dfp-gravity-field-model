# FILENAME: test_time_spatial_face_ratio.py

"""
TIME vs SPATIAL Face Classification in the Stellated Octahedron
===============================================================

The stellated octahedron has 8 triangular faces: 4 on Tetrahedron A and
4 on Tetrahedron B. Each face is classified as either a TIME face or a
SPATIAL face based on its geometric orientation relative to the Field
Origin. TIME faces point inward toward the coupling center (opposite the
apex vertices V7 and V0), while SPATIAL faces point outward. Standard
combinatorics on the defined face sets yields a specific count for each
category. The ratio of TIME faces to total faces (2/8 = 1/4) is load
bearing in GFM: it determines electron spin (S = hbar/2), appears in
the uncertainty principle bound, and encodes the 3+1 decomposition.

GFM OBSERVATION: Exactly 2 of 8 faces are TIME faces and 6 are SPATIAL, giving ratio 1/4.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, FACES, TIME_FACES, SPATIAL_FACES, TET_A, TET_B,
)


class TimeSpatialFaceRatioCrossCheck(Test):
    """
    PHYSICAL CONTEXT:
    In the stellated octahedron, each tetrahedron has 4 triangular faces,
    producing 8 faces total. The GFM framework classifies each face as
    TIME or SPATIAL based on whether it is opposite an apex vertex (V7
    for Tet A, V0 for Tet B). This classification implements the 3+1
    decomposition of spacetime at the level of the fundamental geometric
    structure. Standard physics requires a 3+1 split for Lorentzian
    signature, but does not specify how many geometric elements carry
    the time versus space roles. The GFM stellated octahedron provides
    a concrete realization: 1 TIME face per tetrahedron (2 total) and
    3 SPATIAL faces per tetrahedron (6 total).

    GFM OBSERVATION:
    The TIME_FACES set contains exactly 2 elements and the SPATIAL_FACES
    set contains exactly 6 elements, totaling 8 = 2K faces. The ratio
    TIME/TOTAL = 2/8 = 1/4. This ratio appears in the spin derivation
    S = (2/8) * 2 * hbar = hbar/2 and in the uncertainty principle. The
    face sets are mutually exclusive and jointly exhaustive over FACES.
    Each tetrahedron contributes exactly 1 TIME face and 3 SPATIAL faces,
    reflecting the 3+1 structure per chamber.

    EPISTEMIC STATUS:
    This is a structural cross check validating internal consistency of
    the face classification definitions. The 2/8 ratio is an observation
    about the geometry, not a derivation from first principles.
    """

    name = "TIME vs SPATIAL Face Ratio Cross Check"

    question = (
        "How many of the 8 faces of the stellated octahedron are classified "
        "as TIME faces, and how many as SPATIAL? The spin derivation requires "
        "exactly 2 TIME faces out of 8 total, giving the ratio 1/4 that "
        "produces S = hbar/2. If the face classification were inconsistent "
        "with this count, or if TIME and SPATIAL faces overlapped or failed "
        "to cover all faces, multiple downstream derivations would collapse. "
        "Do the concrete set definitions satisfy all five consistency conditions: "
        "correct TIME count, correct SPATIAL count, mutual exclusivity, joint "
        "exhaustiveness over FACES, and the expected 1/4 ratio?"
    )

    reference = (
        "GFM Paper VI Section 7: Electron spin from TIME face fraction; "
        "GFM Paper VII Section 5.2: Uncertainty principle from same ratio; "
        "Coxeter (1973) Regular Polytopes: stellated octahedron face structure"
    )

    tolerance = 0.01

    level = Level.CRITICAL

    commentary = (
        "This test validates five independent consistency conditions on the "
        "face classification system. The TIME face count (2), SPATIAL face "
        "count (6), their mutual exclusivity (zero overlap), their joint "
        "exhaustiveness (union equals FACES), and the resulting ratio (0.25) "
        "are each checked separately. The ratio 2/8 = 1/4 is not arbitrary: "
        "it encodes the fact that each tetrahedron has 3 spatial faces and "
        "1 temporal face, which is the geometric realization of the 3+1 "
        "spacetime signature. This is an observation about the model's "
        "internal definitions, not a derivation of new physics. Its value "
        "lies in confirming that the face sets imported from the codebase "
        "are mutually consistent and produce the exact ratio on which the "
        "spin and uncertainty principle results depend."
    )

    # Audit scoring
    audit_score = 83
    audit_notes = (
        "Question: 12/15 (asks a concrete quantitative question with clear stakes about downstream derivations collapsing, but reads more like a checklist of five conditions than a mystery hook; leading with the spin connection as tension would sharpen curiosity). Derivation: 12/15 (good logical progression through setup, definitions, and three consistency checks; labels steps clearly as STRUCTURAL SETUP, GFM DEFINITION, and GFM OBSERVATION; but jumps straight into definitions without a physical analogy or intuition building phase; the TENSION step is missing, so the reader never feels the puzzle before seeing the resolution). Commentary: 12/15 (honest epistemic labeling, connects the ratio to spin and uncertainty principle, explains why 1/4 is not arbitrary; but lacks an analogy to make the insight visceral, and does not state implications beyond confirming consistency; restates the five checks rather than delivering a single aha moment). Model: 9/10 (clean summary with 5 key values, good use of binary verdict for coverage check, descriptive names with parenthetical clarification; minor note that the set conversion guards add defensive code that slightly obscures the core logic). Observations: 7/10 (values are mathematically exact and internally justified; Coxeter 1973 cited for stellated octahedron structure; but the TIME/SPATIAL classification itself is a GFM internal definition with no external authoritative source to verify against, which limits independent traceability; the spin and uncertainty references are to GFM papers not external experiments). Constants: 9/10 (K, FACES, TIME_FACES, SPATIAL_FACES, TET_A, TET_B all imported from common; TET_A and TET_B are imported but never used in the model or observations methods, so two unnecessary imports). Accessibility: 13/15 (explains what TIME and SPATIAL faces mean, defines the apex vertex convention, builds from counting to ratio to physical consequence; but assumes familiarity with the spin derivation S = (2/8) * 2 * hbar without explaining where the factor of 2 * hbar comes from, which could lose undergrads; no grounding analogy for why faces point inward versus outward). Header: 9/10 (comprehensive module docstring covering the physical domain, the specific question, explicit GFM OBSERVATION label, honest epistemic status, and the load bearing nature of the ratio; could add a brief note on target audience level)."
    )

    academic_paper = """\
TITLE TIME vs SPATIAL Face Classification in the Stellated Octahedron: Validating the 1/4 Ratio ABSTRACT This investigation checks whether the face classification of the stellated octahedron produces exactly 2 TIME faces and 6 SPATIAL faces out of 8 total. The model validates five consistency conditions. All five hold exactly. The ratio 2/8 = 1/4 is documented as a structural OBSERVATION. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The 3+1 decomposition of spacetime into three spatial dimensions and one temporal dimension is foundational to relativistic physics. The Lorentzian signature requires this split, but general relativity does not specify how geometric substructures carry the temporal versus spatial roles. The GFM stellated octahedron offers a concrete realization. Two interlocking tetrahedra produce 8 triangular faces total, 4 per tetrahedron. Each tetrahedron has one face opposite its apex vertex: FACE_A7 (opposite V7) for Tetrahedron A and FACE_B0 (opposite V0) for Tetrahedron B. These two faces point inward toward the Field Origin and are classified as TIME faces. The remaining 6 faces point outward and are classified as SPATIAL faces. The ratio TIME/TOTAL = 2/8 = 1/4 is not merely a counting exercise. It propagates into multiple GFM results. The electron spin derivation uses S = (2/8) times 2 times hbar = hbar/2. The uncertainty principle bound Delta_x times Delta_p >= hbar/2 traces its factor of 1/2 to the same geometric fraction. If the face classification were inconsistent, if TIME and SPATIAL faces overlapped, failed to cover all faces, or produced the wrong counts, these downstream results would lose their geometric foundation. This test specifically investigates whether the concrete set definitions in the GFM codebase satisfy five independent consistency conditions simultaneously. 2. METHODOLOGY The model imports TIME_FACES, SPATIAL_FACES, and FACES from the GFM common constants module. It computes: (1) the count of TIME faces, (2) the count of SPATIAL faces, (3) the size of the intersection between TIME and SPATIAL sets to check mutual exclusivity, (4) whether the union of TIME and SPATIAL equals the full FACES set to check joint exhaustiveness, and (5) the ratio of TIME faces to total faces. Agreement is defined as exact match on all five quantities with a tolerance of 1 percent. 3. RESULTS Model output: TIME face count: 2.0 SPATIAL face count: 6.0 Overlap count: 0.0 Union covers FACES (1=yes 0=no): 1.0 TIME to TOTAL ratio: 0.25 Expected values: TIME face count: 2.0 SPATIAL face count: 6.0 Overlap count: 0.0 Union covers FACES (1=yes 0=no): 1.0 TIME to TOTAL ratio: 0.25 All five conditions are satisfied exactly. The TIME and SPATIAL face sets partition the full face set without gaps or overlaps. The ratio 2/8 = 0.25 holds precisely. 4. DISCUSSION The result confirms that the GFM face classification system is internally consistent across all five conditions tested. The 2/8 ratio reflects the 3+1 structure at the level of individual tetrahedra: each contributes 3 SPATIAL faces and 1 TIME face, mirroring the 3 spatial plus 1 temporal decomposition of spacetime. EPISTEMIC STATUS: OBSERVATION. The face classification is a GFM definition, not a derivation from first principles. We observe that this definition produces a ratio consistent with the factor 1/2 appearing in spin and uncertainty relations. The test validates internal consistency of definitions, not correspondence with external experiment. This test connects to the complementary pair inversion test, which validated that XOR 7 maps vertices across tetrahedra. Together these tests establish that the stellated octahedron's vertex partition and face classification form a coherent system supporting the 3+1 structure. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that the stellated octahedron is physically realized or that the TIME/SPATIAL distinction has experimental consequences independent of the GFM framework. The classification assumes apex vertices V7 and V0 define the temporal direction, which is itself a GFM postulate. The connection to spin and uncertainty is noted as a pattern, not derived here. Further work should investigate whether the 1/4 ratio produces measurable predictions distinguishable from alternative geometric schemes. 6. CONCLUSION All five consistency conditions for the TIME versus SPATIAL face classification hold exactly. The ratio 2/8 = 1/4 is confirmed as a robust structural property of the stellated octahedron. This merits inclusion as a foundational cross check because three independent GFM results depend on this
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STRUCTURAL SETUP: The stellated octahedron has 2 tetrahedra, "
                "each with K=4 triangular faces, giving 2K=8 faces total."
            )
            .step(
                "GFM DEFINITION: TIME faces are those opposite the apex vertices. "
                "For Tet A, the apex is V7, so FACE_A7 = {V1, V2, V4} is the TIME face. "
                "For Tet B, the apex is V0, so FACE_B0 = {V3, V5, V6} is the TIME face."
            )
            .step(
                "GFM DEFINITION: SPATIAL faces are the remaining 3 faces per tetrahedron, "
                "giving 6 SPATIAL faces total."
            )
            .equation("N_TIME = 2, N_SPATIAL = 6, N_TOTAL = 8 = 2K")
            .step(
                "CONSISTENCY CHECK 1: N_TIME + N_SPATIAL must equal N_TOTAL = 8. "
                "This verifies joint exhaustiveness."
            )
            .step(
                "CONSISTENCY CHECK 2: The intersection of TIME_FACES and SPATIAL_FACES "
                "must be empty. This verifies mutual exclusivity."
            )
            .step(
                "CONSISTENCY CHECK 3: The union of TIME_FACES and SPATIAL_FACES "
                "must equal FACES. This verifies completeness over the defined face set."
            )
            .equation("TIME_RATIO = N_TIME / N_TOTAL = 2 / 8 = 1/4 = 0.25")
            .step(
                "GFM OBSERVATION: This 1/4 ratio propagates into the spin derivation "
                "as S = (2/8) * 2 * hbar = hbar/2, and into the uncertainty principle "
                "as the geometric origin of the factor 1/2 in Delta_x * Delta_p >= hbar/2."
            )
            .conclude(
                "If all five conditions hold (TIME count = 2, SPATIAL count = 6, "
                "zero overlap, full coverage of FACES, ratio = 0.25), the face "
                "classification is internally consistent and supports the downstream "
                "derivations that depend on the 1/4 ratio."
            )
        )

    def model(self) -> Model:
        time_set = set(TIME_FACES) if not isinstance(TIME_FACES, set) else TIME_FACES
        spatial_set = set(SPATIAL_FACES) if not isinstance(SPATIAL_FACES, set) else SPATIAL_FACES
        all_faces = set(FACES) if not isinstance(FACES, set) else FACES

        n_time = float(len(time_set))
        n_spatial = float(len(spatial_set))

        overlap = float(len(time_set & spatial_set))

        union_covers_all = 1.0 if (time_set | spatial_set) == all_faces else 0.0

        total_faces = n_time + n_spatial
        time_ratio = n_time / total_faces if total_faces > 0 else -1.0

        return (
            Model()
            .add("TIME face count", n_time)
            .add("SPATIAL face count", n_spatial)
            .add("Overlap count", overlap)
            .add("Union covers FACES (1=yes 0=no)", union_covers_all)
            .add("TIME to TOTAL ratio", time_ratio)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("TIME face count", 2.0)
            .add("SPATIAL face count", 6.0)
            .add("Overlap count", 0.0)
            .add("Union covers FACES (1=yes 0=no)", 1.0)
            .add("TIME to TOTAL ratio", 0.25)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="TIME vs SPATIAL Face Ratio Cross Check",
        summary="Validates that exactly 2 of 8 faces are TIME faces, confirming the 1/4 ratio used in spin and uncertainty derivations",
        test_classes=[TimeSpatialFaceRatioCrossCheck],
    )
