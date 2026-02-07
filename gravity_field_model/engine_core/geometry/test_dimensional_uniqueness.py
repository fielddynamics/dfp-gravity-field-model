# FILENAME: test_dimensional_uniqueness.py

"""
Dimensional Uniqueness of Three Spatial Dimensions
===================================================

The number of spatial dimensions in our universe is three. This is among the
most fundamental observed facts in physics, yet standard physics treats it as
a given rather than explaining it. Ehrenfest (1917) showed that stable orbits
and stable atoms require exactly d=3, but did not explain why nature selects
this value. The GFM framework notes that the tetrahedral closure constant K=4
and spatial dimension d=3 are linked by a unique arithmetic identity:
2(d+1) = 2^d holds only for d=3 among all positive integers. This identity
equates the number of vertices in two tetrahedra (2K = 2(d+1) = 8) with the
number of vertices in a d dimensional cube (2^d = 8), meaning the stellated
octahedron can be inscribed in a cube only in three dimensions.

GFM OBSERVATION: 2(d+1) = 2^d is satisfied uniquely at d=3, linking K=4 to 2^d=8.

This is an OBSERVATION, not a derivation.
"""

import math
from gravity_field_model.framework import Test, Level, Derivation, Model, Observed
from gravity_field_model.common import (
    K,
    VERTICES,
)


class DimensionalUniqueness(Test):
    """
    PHYSICAL CONTEXT:
    Ehrenfest (1917) demonstrated that planetary orbits are unstable for d>3
    and that the hydrogen atom has no bound states for d>3. Tegmark (1997)
    extended this analysis, showing that both gravitational and electrostatic
    problems lack stable solutions unless d=3. Standard physics confirms d=3
    is necessary for a universe with complex structure, but offers no
    mechanism that selects d=3 from all possible integers.

    GFM OBSERVATION:
    The GFM stellated octahedron has 2K = 2(d+1) vertices from its two
    tetrahedra and sits inside a cube with 2^d vertices. The identity
    2(d+1) = 2^d is satisfied only at d=3. No other positive integer
    works. This means K=4 and d=3 are not independent choices but are
    locked together by a single arithmetic constraint. The value d=3
    is the unique fixed point where simplex doubling equals hypercube
    vertex count.

    EPISTEMIC STATUS:
    This is a mathematical observation. The identity 2(d+1) = 2^d at d=3
    is exact and verifiable by enumeration. GFM notes it as structurally
    significant but does not claim to derive the dimensionality of space
    from first principles alone.
    """

    name = "Dimensional Uniqueness d=3"

    question = (
        "Why does the identity 2(d+1) = 2^d hold only for d=3 among all "
        "positive integers? The left side counts vertices in two simplices "
        "(2K where K=d+1), while the right side counts vertices of the "
        "d dimensional cube. Their equality at d=3 means the stellated "
        "octahedron (8 vertices from two tetrahedra) exactly fills the "
        "cube (8 vertices in three dimensions). Does this unique coincidence "
        "explain why our universe has three spatial dimensions?"
    )

    reference = "Ehrenfest (1917); Tegmark (1997); Coxeter, Regular Polytopes (1973)"

    tolerance = 0.001

    level = Level.CRITICAL

    commentary = (
        "The identity 2(d+1) = 2^d is pure arithmetic, verifiable by testing "
        "every positive integer. For d=1: 4 vs 2. For d=2: 6 vs 4. For d=3: "
        "8 vs 8. For d=4: 10 vs 16. The gap widens monotonically for d>3 "
        "because exponential growth dominates linear growth. Standard physics "
        "confirms that d=3 is required for stable orbits and stable atoms. "
        "GFM observes that d=3 is also the unique dimension where two "
        "simplices have the same vertex count as the embedding hypercube. "
        "This is an observation linking K=4 closure geometry to the "
        "dimensionality of space, not a derivation of d=3 from deeper axioms."
    )

    # Audit scoring
    audit_score = 85
    audit_notes = (
        "Question: 13/15 (strong mystery hook with specific numbers and geometric framing, but the final sentence 'Does this unique coincidence explain...' slightly undercuts confidence by framing as coincidence rather than sharpening the stakes). Derivation: 14/15 (excellent progression from standard physics through geometric setup to enumeration to formal proof to GFM observation, intuition is built before math, minor note: could benefit from one everyday analogy such as comparing simplex vs cube growth to a race between a jogger and a sports car). Commentary: 12/15 (clearly states the arithmetic, correctly labels as observation not derivation, connects to bigger picture, but lacks an everyday analogy and does not state implications for what we can now trust or investigate next). Model: 9/10 (clean summary with 5 key values, binary gap metric, uniqueness count is clever, easy to interpret at a glance). Observations: 8/10 (all values are exact mathematical identities so correctness is unambiguous, references listed in the reference field are authoritative, but the observations themselves are mathematical truths rather than experimental data which slightly blurs the observation vs model distinction). Constants: 8/10 (K and VERTICES imported from common as required, d=3 correctly used as literal per project rules, but VERTICES is imported without being used in the code which is a minor compliance issue). Accessibility: 13/15 (an undergraduate with calculus can follow the enumeration and the exponential vs linear argument, the formal proof step is clear, jargon like simplex and hypercube is explained in context, but a concrete analogy for why exponential beats linear would help the broadest audience). Header: 8/10 (module docstring covers the physical domain, states the question clearly, identifies epistemic status as observation, cites key references, but does not explicitly state target audience level or list known limitations of the test)."
    )

    academic_paper = """\
TITLE Dimensional Uniqueness of Three Spatial Dimensions: The Identity 2(d+1) = 2^d at d=3 ABSTRACT We investigate the arithmetic identity 2(d+1) = 2^d, which equates simplex doubling to hypercube vertex count. Enumeration and monotonicity analysis confirm d=3 is the unique positive integer solution. GFM observes this locks the closure constant K=4 to three spatial dimensions. This is an OBSERVATION, not a derivation of dimensionality. 1. INTRODUCTION: THE SCIENTIFIC QUESTION The dimensionality of space is among the deepest open questions in physics. We observe three spatial dimensions, and this fact underpins all known physical law. Ehrenfest (1917) demonstrated that stable planetary orbits exist only for d=3, and Tegmark (1997) extended this result to show that both gravitational and atomic stability require exactly three spatial dimensions. However, neither result explains why nature selects d=3. Standard physics treats dimensionality as an empirical input rather than a consequence of deeper structure. The Gravity Field Model constructs its geometry from two interpenetrating tetrahedra forming a stellated octahedron. Each tetrahedron is a simplex in d dimensions with K = d+1 vertices. Two tetrahedra contribute 2K = 2(d+1) vertices. These vertices are embedded at corners of a d dimensional cube, which has 2^d vertices. For the stellated octahedron to perfectly inscribe in the cube, requiring that every cube vertex is occupied by exactly one tetrahedral vertex, the identity 2(d+1) = 2^d must hold. This test investigates whether d=3 is the unique positive integer satisfying this identity, and what consequences follow for the GFM closure constant K. 2. METHODOLOGY We evaluate both sides of the identity 2(d+1) and 2^d for all positive integers d from 1 through 20. For each value, we compute the gap: the absolute difference between the two sides. We count the total number of solutions where the gap equals zero. We then provide a formal monotonicity argument showing that no solutions exist beyond the tested range. The comparison criterion is exact equality (zero gap), since both sides are integers. We also verify that the solution yields K = d+1 = 4, consistent with the GFM closure constant. 3. RESULTS Model output: 2(d+1) at d=3: 8 2^d at d=3: 8 Gap: 0 (exact match) Unique solutions found in d=1 through 20: 1 K closure constant at solution: 4 Enumeration detail: d=1 gives 4 versus 2 (gap 2). d=2 gives 6 versus 4 (gap 2). d=3 gives 8 versus 8 (gap 0). d=4 gives 10 versus 16 (gap 6). d=5 gives 12 versus 32 (gap 20). The exponential function 2^d grows far faster than the linear function 2(d+1) for all d greater than 3, and both functions fall below equality for d less than 3. The function f(d) = 2^d minus 2(d+1) equals zero at d=3, is negative for d=1 and d=2, and is strictly increasing for d greater than or equal to 4. Therefore d=3 is the unique positive integer solution globally, not merely within the tested range. 4. DISCUSSION The identity 2(d+1) = 2^d at d=3 is a mathematical fact requiring no physical input. Its significance for GFM is that it couples two apparently independent parameters: the closure constant K=4 (vertices per tetrahedron) and the spatial dimension d=3 (hypercube embedding dimension). Rather than being two free choices, K and d are locked by a single constraint. At the solution, 2K = 2^d = 8, which is precisely the vertex count of the GFM stellated octahedron and its embedding cube. EPISTEMIC STATUS: OBSERVATION. GFM does not derive the dimensionality of space from first principles. We observe that the geometric requirement for perfect cube inscription of two simplices is satisfied at exactly d=3 and nowhere else. This correspondence is noted as structurally significant within the GFM framework. 5. LIMITATIONS AND HONESTY STATEMENT This test does not prove that space must have three dimensions. The identity is arithmetic and does not by itself constitute a physical mechanism for dimensional selection. The assumption that the stellated octahedron must inscribe in a cube is a GFM premise, not an independently established physical requirement. Further work is needed to connect this identity to dynamical dimensional selection mechanisms such as those proposed in string theory or causal dynamical triangulations. 6. CONCLUSION The identity 2(d+1) = 2^d has a unique positive integer
    """



    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step(
                "STANDARD PHYSICS: The number of spatial dimensions d=3 is "
                "an empirical fact. Ehrenfest (1917) proved that stable "
                "planetary orbits require d=3. Tegmark (1997) showed both "
                "gravitational and atomic stability require d=3."
            )
            .step(
                "GEOMETRIC SETUP: In GFM, the fundamental structure is the "
                "stellated octahedron: two interpenetrating tetrahedra. Each "
                "tetrahedron is a d simplex with K = d+1 vertices. Two "
                "tetrahedra contribute 2K = 2(d+1) vertices total."
            )
            .step(
                "EMBEDDING: These vertices sit at corners of a d dimensional "
                "cube (hypercube), which has 2^d vertices. For the stellated "
                "octahedron to exactly fill the cube, we need 2(d+1) = 2^d."
            )
            .equation("2(d+1) = 2^d")
            .step(
                "ENUMERATION: Test all positive integers. "
                "d=1: 2(2)=4, 2^1=2, gap=2. "
                "d=2: 2(3)=6, 2^2=4, gap=2. "
                "d=3: 2(4)=8, 2^3=8, gap=0. MATCH. "
                "d=4: 2(5)=10, 2^4=16, gap=6. "
                "d=5: 2(6)=12, 2^5=32, gap=20. "
                "For d>=4, 2^d grows exponentially while 2(d+1) grows linearly, "
                "so no further solutions exist."
            )
            .step(
                "FORMAL PROOF: Define f(d) = 2^d minus 2(d+1). Then f(1)= -2, "
                "f(2)= -2, f(3)=0, f(4)=6. For d>=4, the derivative of 2^d "
                "(which is 2^d * ln(2)) exceeds the derivative of 2(d+1) "
                "(which is 2), so f(d) is strictly increasing for d>=4. "
                "Since f(3)=0 and f is strictly increasing beyond d=3, "
                "there are no solutions for d>3. Combined with f(1)<0 and "
                "f(2)<0, d=3 is the unique positive integer solution."
            )
            .step(
                "GFM OBSERVATION: At d=3, K = d+1 = 4 (the closure constant), "
                "2K = 8 (total vertices of two tetrahedra), and 2^d = 8 "
                "(cube vertices). The stellated octahedron perfectly inscribes "
                "in the cube. This locks the GFM geometry to exactly three "
                "spatial dimensions."
            )
            .conclude(
                "The equation 2(d+1) = 2^d has a unique positive integer "
                "solution at d=3. This is a mathematical fact. GFM observes "
                "that this identity is the reason K=4 and d=3 are not "
                "independent parameters but a single geometric constraint: "
                "two tetrahedra fill a cube only in three dimensions."
            )
        )

    def model(self) -> Model:
        d = 3
        k = d + 1
        simplex_vertices = 2 * k
        cube_vertices = 2 ** d
        gap = abs(simplex_vertices - cube_vertices)

        # Verify uniqueness: count solutions for d in 1..20
        solutions_found = 0.0
        for test_d in range(1, 21):
            if 2 * (test_d + 1) == 2 ** test_d:
                solutions_found += 1.0

        return (
            Model()
            .add("2(d+1) at d=3", float(simplex_vertices))
            .add("2^d at d=3", float(cube_vertices))
            .add("Gap (should be zero)", float(gap))
            .add("Unique solutions in d=1..20", solutions_found)
            .add("K closure constant", float(k))
        )

    def observations(self) -> Observed:
        return (
            Observed()
            .add("2(d+1) at d=3", 8.0)
            .add("2^d at d=3", 8.0)
            .add("Gap (should be zero)", 0.0)
            .add("Unique solutions in d=1..20", 1.0)
            .add("K closure constant", 4.0)
        )


if __name__ == "__main__":
    from gravity_field_model.framework import run_tests
    run_tests(
        title="Dimensional Uniqueness Test",
        summary="Verifies that 2(d+1) = 2^d holds uniquely at d=3, linking K=4 to three spatial dimensions",
        test_classes=[DimensionalUniqueness],
    )
