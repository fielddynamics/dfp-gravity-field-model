"""
11. What the two reading rules are, in terms of the labels
==========================================================

Role:     Prepares a derivation of PROOF.md Theorem 5's rules: equivalent forms that may be easier to motivate.
Expected: Passes. A failure means one of the stated identities is false for some trigram.

The weight rule 2b + m + t and the step rule 2t + 1 are written in the lines.
This test checks equivalent forms over all eight trigrams (label v = 4b + 2m + t):

- weight = ceil(v / 2): the label halved, rounded up;
- weight = (number of yang lines) + b: the yang count, with the bottom line counted twice;
- reading through the complement map: weight(complement) = 4 - weight;
- step = 1 + 2 (v mod 2): 3 for odd labels, 1 for even ones;
- along the father's family in rank order, the steps 3, 1, 1, 3 sum to 8.
"""

from math import ceil

from gravity_field_model.framework import *

LINES = {v: ((v >> 2) & 1, (v >> 1) & 1, v & 1) for v in range(8)}


class LineRuleIdentities(Test):
    name = "11. The Reading Rules in Terms of the Labels"
    question = (
        "Can the two reading rules be stated in other, possibly more natural, terms: the "
        "binary label, the yang count, the complement?"
    )
    reference = "PROOF.md Theorem 5"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For each label v = 4b + 2m + t, compute 2b + m + t, ceil(v/2), yang count + b.")
            .step("Compare the weight of each trigram with that of its complement.")
            .step("Compare 2t + 1 with 1 + 2 (v mod 2).")
            .conclude("Count the trigrams on which each identity holds.")
        )

    commentary = (
        "All the identities hold on all eight trigrams. The weight is the label halved and "
        "rounded up, equivalently the number of yang lines with the bottom line counted "
        "twice; complementing a trigram replaces its weight w by 4 - w = K - w. The step is 3 "
        "for an odd label and 1 for an even one: the top line is the label's lowest bit. These "
        "forms are candidates for a derivation (why should the bottom line count twice, why "
        "should the lowest bit set the step?), not a derivation themselves."
    )

    def model(self):
        w = {v: 2 * b + m + t for v, (b, m, t) in LINES.items()}
        return (
            Model()
            .add("Trigrams with weight = ceil(v/2)", sum(1 for v in w if w[v] == ceil(v / 2)))
            .add("Trigrams with weight = yang count + bottom", sum(1 for v, (b, m, t) in LINES.items() if w[v] == b + m + t + b))
            .add("Trigrams with weight(7-v) = 4 - weight(v)", sum(1 for v in w if w[7 - v] == 4 - w[v]))
            .add("Trigrams with 2t+1 = 1 + 2(v mod 2)", sum(1 for v, (b, m, t) in LINES.items() if 2 * t + 1 == 1 + 2 * (v % 2)))
            .add("Steps along Qian, Zhen, Kan, Gen", " ".join(str(2 * LINES[v][2] + 1) for v in (7, 4, 2, 1)))
            .add("Their sum", sum(2 * LINES[v][2] + 1 for v in (7, 4, 2, 1)))
        )

    def observations(self):
        return (
            Observed()
            # ceil((4b + 2m + t)/2) = 2b + m + ceil(t/2) = 2b + m + t for t in {0, 1}.
            .add("Trigrams with weight = ceil(v/2)", 8)
            .add("Trigrams with weight = yang count + bottom", 8)
            # (2(1-b) + (1-m) + (1-t)) = 4 - (2b + m + t).
            .add("Trigrams with weight(7-v) = 4 - weight(v)", 8)
            # t is the lowest bit of v.
            .add("Trigrams with 2t+1 = 1 + 2(v mod 2)", 8)
            .add("Steps along Qian, Zhen, Kan, Gen", "3 1 1 3")
            .add("Their sum", 8)
        )


ALL_TESTS = [LineRuleIdentities]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("11", "Line rule identities.", ALL_TESTS) else 1)
