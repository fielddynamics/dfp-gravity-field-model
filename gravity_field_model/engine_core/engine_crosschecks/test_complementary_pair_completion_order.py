"""
Complementary Pair Completion Order in Pi Base 8 Traversal
==========================================================

The pi base 8 traversal visits vertices of the stellated octahedron in a
deterministic sequence. The 8 vertices form 4 complementary pairs, where
each pair (v, 7 minus v) spans both tetrahedra. The READ process definition
(Chapter 12) claims these pairs complete in a specific order at specific
steps: (3,4) at step 1, (0,7) at step 5, (2,5) at step 11, and (1,6) at
step 15. This is not a statistical claim but a deterministic fact about the
digits of pi in base 8, verifiable by direct computation. The integer part
"3" must be included in the traversal for the first pair to exhibit bimetric
balance (V3 from Tet B, V4 from Tet A, summing to 7).

GFM OBSERVATION: The four pairs complete in an order that encodes the 3+1
structure: the first pair visited is (3,4), whose digits literally spell "3.1".

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K, VERTICES, TET_A, TET_B,
)
from gravity_field_model.engine_core.common.traversal_analyzer import (
    get_analyzer, TraversalAnalyzer,
)


class ComplementaryPairCompletionOrder(Test):
    """
    Verify the exact step at which each complementary pair first has both
    members visited in the pi base 8 traversal.

    PHYSICAL CONTEXT:
    The stellated octahedron has 8 vertices forming 4 complementary pairs:
    (0,7), (1,6), (2,5), (3,4). Each pair connects one vertex from Tet A
    to one from Tet B via the complement operation (v maps to 7 minus v).
    The pair is "complete" when both members have been visited at least once
    in the cumulative traversal. The completion step for each pair is fully
    determined by pi's base 8 expansion including the integer part "3".

    GFM OBSERVATION:
    Chapter 12 of the GFM framework specifies that pair (3,4) completes at
    step 1, pair (0,7) at step 5, pair (2,5) at step 11, and pair (1,6) at
    step 15. The first pair encodes the 3+1 dimensional structure. The last
    pair completes at step 15, which is also when all 8 vertices have been
    visited. The geometric constant k=4 equals the number of complementary
    pairs, and the completion sequence traces the order in which the Field
    Origin coupling activates across the full vertex set.

    EPISTEMIC STATUS:
    This is a deterministic verification against the digits of pi in base 8.
    The step numbers are either exactly correct or exactly wrong. There is
    no statistical tolerance involved. The 3+1 interpretation is an observation.
    """

    name = "Complementary Pair Completion Order"

    question = (
        "Do the four complementary pairs of the stellated octahedron complete "
        "at exactly steps 1, 5, 11, and 15 in the pi base 8 traversal, as "
        "specified by the READ process in Chapter 12? The integer part 3 is "
        "included, making the first vertex V3 (Tet B) and the second V4 "
        "(Tet A), so pair (3,4) completes at step 1 with bimetric balance. "
        "If these step numbers are wrong, the READ process narrative collapses."
    )

    reference = "GFM Chapter 12, READ Process, I Ching pair completion order"

    tolerance = 0.0

    level = Level.CRITICAL

    commentary = (
        "The completion order of complementary pairs is a hard fact about pi "
        "in base 8, not a tunable parameter. Standard mathematics determines "
        "these step numbers uniquely. The observation that the first pair "
        "(3,4) spells the digits '3' and '1' encoding 3+1 spacetime dimensions "
        "is a pattern noted by GFM, not a derivation from first principles. "
        "That all four pairs complete in exactly 15 steps means full vertex "
        "coverage is achieved, and the order in which bimetric coupling "
        "activates across the structure is determined by pi itself. The count "
        "of four pairs equals the closure constant k=4."
    )

    # Audit scoring
    audit_score = 82
    audit_notes = (
        "Question: 12/15 - Stakes are clear and the 'if wrong, narrative collapses' framing is strong, but it leads with technical detail rather than hooking curiosity first. Opening with WHY these pairs matter physically before listing the step numbers would sharpen the mystery. Derivation: 13/15 - Excellent step by step walkthrough with concrete digit sequences. The reader can follow each vertex visit. Minor gap: no intuition building analogy before the procedure starts, and the transition from 'here are the digits' to 'here are the completion steps' could explain WHY vertex 2 takes so long (coupon collector effect). Commentary: 12/15 - Good insight distinguishing hard fact from observation, and the k=4 connection is noted. Missing an analogy to make it vivid, and no implication statement about what we can now trust downstream. The 'spells 3.1' observation deserves more weight. Model: 9/10 - Clean output with 7 well chosen values. The three auxiliary checks (Tet B first, Tet A second, sum equals 7) add real diagnostic value beyond the four step numbers. Observations: 7/10 - Values are deterministic and self documenting (they come from pi), but the reference line cites only 'GFM Chapter 12' without pointing to the specific digit sequence source or the mpmath verification that produces the base 8 expansion. Constants: 9/10 - K, VERTICES, TET_A, TET_B all imported from common. The pair definitions (3,4), (0,7) etc. are hardcoded as literal integers, which is acceptable since these are vertex labels not physical constants, but documenting why they are not imported would be cleaner. Accessibility: 12/15 - A graduate student in physics or math could follow this readily. The step by step digit trace is excellent pedagogy. However, the terms 'bimetric balance', 'Field Origin coupling', and 'I Ching pair' are used without definition for a newcomer. One sentence explaining what complementary pairs physically represent would help undergrads. Header: 8/10 - Module docstring is thorough with clear scope, epistemic status, and the observation disclaimer. Could add target audience level and a brief note on what downstream tests depend on these results."
    )

    academic_paper = """\
COMPLEMENTARY PAIR COMPLETION ORDER IN THE PI BASE 8 TRAVERSAL OF THE STELLATED OCTAHEDRON Exact verification of the four bimetric coupling activation steps AUTHOR GFM Research Agent ABSTRACT The Gravity Field Model traverses the eight vertices of a stellated octahedron using the digits of pi in base 8. These vertices form four complementary pairs, each spanning both tetrahedra. We verify that the four pairs complete at exactly steps 1, 5, 11, and 15, matching the specification in the GFM READ process. All seven diagnostic quantities, including four completion steps and three auxiliary bimetric checks, match their predicted values with 0.00% error. The result is deterministic, not statistical: it follows from the digit sequence of pi and admits no free parameters. The completion order encodes structural information about the 3+1 dimensional signature of spacetime. 1. INTRODUCTION 1.1 The Complementary Pair Structure The stellated octahedron consists of two interpenetrating tetrahedra, designated Tet A (vertices 1, 2, 4, 7) and Tet B (vertices 0, 3, 5, 6). Each vertex v has a complement 7 minus v, obtained by flipping all three bits of the vertex label. This complement always belongs to the opposite tetrahedron, a consequence of parity: the bit sum of v and 7 minus v have opposite evenness. The eight vertices therefore organize into four complementary pairs: (0,7), (1,6), (2,5), and (3,4). Each pair connects one vertex from each tetrahedron through the geometric center, the Field Origin, where the two tetrahedra meet. A natural question arises: when the traversal visits vertices sequentially, in what order do these cross tetrahedral connections first activate? The answer is not adjustable. It is fixed by pi. 1.2 The Traversal Mechanism The GFM field closure engine reads the digits of pi in base 8, including the integer part 3, and maintains a cumulative sum. At each step, the visited vertex equals the cumulative sum modulo 8. This produces a deterministic sequence of vertex visits. A complementary pair is "complete" at the earliest step where both of its members have appeared at least once. The completion steps are therefore exact integers, determined entirely by the mathematical constant pi. 1.3 Structure of This Paper Section 2 traces the traversal through its first 16 steps to identify all four completion events. Section 3 reports the numerical results and auxiliary diagnostics. Section 4 discusses the physical interpretation and epistemic status of the observed patterns. Section 5 states the conclusions. 2. THE TRAVERSAL 2.1 Digit Sequence and Vertex Visits Pi in base 8 is 3.11037552421026... The traversal begins with the integer digit 3. The cumulative sum grows as each digit is added, and the vertex at each step is the cumulative sum modulo 8. The first 16 steps proceed as follows. Step 0 reads digit 3, producing cumulative sum 3 and vertex 3 (Tet B). Step 1 reads digit 1, producing cumulative sum 4 and vertex 4 (Tet A). At this point, both members of pair (3,4) have been visited. The traversal continues through digits 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, ... visiting vertices 5, 5, 0, 7, 4, 1, 3, 7, 1, 2, 2, 4, 2, ... in sequence. 2.2 Pair Completion Events Tracking first appearances, vertex 5 first appears at step 2, vertex 0 at step 4, vertex 7 at step 5, vertex 1 at step 7, vertex 2 at step 11, and vertex 6 at step 15. The four pairs therefore complete in order: pair (3,4) at step 1, pair (0,7) at step 5, pair (2,5) at step 11, and pair (1,6) at step 15. The last pair completion coincides with the first time all eight vertices have been visited, establishing full vertex coverage at step 15. 3. RESULTS 3.1 Completion Step Verification The model computes all four completion steps from the pi base 8 digit sequence and compares against the values specified in the GFM READ process. Pair (3,4) completes at step 1 (predicted 1, error 0.00%). Pair (0,7) completes at step 5 (predicted 5, error 0.00%). Pair (2,5) completes at step 11 (predicted 11, error 0.00%). Pair (1,6) completes at step 15 (predicted 15, error 0.00%). 3.2 Auxiliary Bimetric Diagnostics Three additional checks verify the bimetric structure of the first pair. The first vertex visited (V3) belongs to Tet B (confirmed, 0.00% error). The second vertex visited (V4) belongs to Tet A (confirmed, 0.00% error). The sum of the first two vertices equals 7, confirming they form a valid complementary pair (confirmed, 0.00% error). All seven quantities match exactly. 4. DISCUSSION 4.1 Physical Interpretation The first complementary pair to activate is (3,4), formed by the integer part of pi (digit 3) and the first fractional digit (digit 1). This pair connects V3 in Tet B to V4 in Tet A, establishing cross tetrahedral coupling at the earliest possible moment. The digits that produce this pair, 3 followed by 1, correspond to the 3+1 dimensional signature of spacetime where d = 3 spatial dimensions and k = d + 1 = 4. The second pair to activate, (0,7), connects the two apex vertices, which are the vertices opposite the TIME faces of each tetrahedron. This is the temporal axis of the structure. The total count of four complementary pairs equals the closure constant k = 4. Full vertex coverage at step 15 means the traversal requires 16 total steps (0 through 15) to activate all bimetric connections, and 16 = k squared. 4.2 Epistemic Status The four completion steps are deterministic consequences of pi in base 8. No parameters are adjusted, no fitting is performed, and no approximation is involved. The 3+1 pattern in the first pair and the k = 4 count of pairs are noted as observations. They follow from the same digit sequence but their physical significance is documented, not derived. The gap structure between completion steps (intervals of 4, 6, and 4 steps) resembles the coupon collector problem on 8 items, where later completions require progressively more draws. That vertex 6 is the last to appear,
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD MATHEMATICS: Pi in base 8 is 3.11037552421026... "
                "The traversal includes the integer part. Each digit is added "
                "to a cumulative sum, and the visited vertex is cumsum mod 8."
            )
            .step(
                "Step 0: digit=3, cumsum=3, vertex=3 mod 8=3 (Tet B). "
                "Step 1: digit=1, cumsum=4, vertex=4 mod 8=4 (Tet A). "
                "Both members of pair (3,4) have now been visited. "
                "Note: V3 + V4 = 7, confirming complementarity."
            )
            .step(
                "Continue the traversal. A pair is 'complete' at the step "
                "where the second of its two members is first visited. "
                "Track which vertices have appeared and mark pairs accordingly."
            )
            .equation("pair_complete_step = min(s) such that both v and 7-v visited by step s")
            .step(
                "From the pi base 8 digit sequence (3,1,1,0,3,7,5,5,2,4,2,1,...): "
                "Vertices visited in order: 3,4,5,5,0,7,4,1,3,7,1,2,... "
                "Pair (3,4): both visited by step 1. "
                "Pair (0,7): V0 at step 4, V7 at step 5, complete at step 5. "
                "Pair (2,5): V5 at step 2, V2 at step 11, complete at step 11. "
                "Pair (1,6): V1 at step 7, V6 at step 15, complete at step 15."
            )
            .step(
                "GFM OBSERVATION: The completion order (3,4) then (0,7) then "
                "(2,5) then (1,6) traces the activation of Field Origin coupling "
                "across all four complementary axes. The first pair encodes 3+1. "
                "The second pair (0,7) connects the two apex vertices (the TIME "
                "axis). Four pairs equals k=4."
            )
            .conclude(
                "This test verifies four exact step numbers. Any discrepancy "
                "would invalidate the Chapter 12 READ process specification."
            )
        )

    def model(self) -> Model:
        a = get_analyzer(100)
        steps = a.steps

        visited = set()
        pair_defs = [(3, 4), (0, 7), (2, 5), (1, 6)]
        pair_complete_step = {}

        for idx, s in enumerate(steps):
            visited.add(s.vertex)
            for pv1, pv2 in pair_defs:
                pair_key = f"({pv1},{pv2})"
                if pair_key not in pair_complete_step:
                    if pv1 in visited and pv2 in visited:
                        pair_complete_step[pair_key] = idx

        step_34 = float(pair_complete_step.get("(3,4)", -1))
        step_07 = float(pair_complete_step.get("(0,7)", -1))
        step_25 = float(pair_complete_step.get("(2,5)", -1))
        step_16 = float(pair_complete_step.get("(1,6)", -1))

        first_tet = "A" if steps[0].vertex in TET_A else "B"
        first_vertex_is_tetB = 1.0 if first_tet == "B" else 0.0

        second_tet = "A" if steps[1].vertex in TET_A else "B"
        second_vertex_is_tetA = 1.0 if second_tet == "A" else 0.0

        first_pair_sum = float(steps[0].vertex + steps[1].vertex)

        return (
            Model()
            .add("Pair (3,4) completion step", step_34)
            .add("Pair (0,7) completion step", step_07)
            .add("Pair (2,5) completion step", step_25)
            .add("Pair (1,6) completion step", step_16)
            .add("First vertex in Tet B", first_vertex_is_tetB)
            .add("Second vertex in Tet A", second_vertex_is_tetA)
            .add("First pair vertex sum", first_pair_sum)
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("Pair (3,4) completion step", 1.0)
            .add("Pair (0,7) completion step", 5.0)
            .add("Pair (2,5) completion step", 11.0)
            .add("Pair (1,6) completion step", 15.0)
            .add("First vertex in Tet B", 1.0)
            .add("Second vertex in Tet A", 1.0)
            .add("First pair vertex sum", 7.0)
        )


# ======================================================================
# Runner
# ======================================================================
if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Complementary Pair Completion Order",
        summary="Verify the exact steps at which each I Ching complementary pair first completes in the pi base 8 traversal",
        test_classes=[ComplementaryPairCompletionOrder],
    )
