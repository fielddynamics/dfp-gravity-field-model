"""
19. Hexagrams: crossing the Field Origin is odd Hamming distance
================================================================

Role:     Extends PROOF.md Theorem 1(d): the geometry of the 64 hexagrams.
Expected: Passes. A failure means the Hamming counts or the parity rule differ from those stated.

A hexagram is an ordered pair of trigrams (lower, upper), i.e. an ordered pair
of cube vertices. The number of lines that differ between them is the Hamming
distance h = 0..3, the number of cube edges between the vertices. The research
notes report the distribution 8 / 24 / 24 / 8. This test checks it, explains
it (8 C(3, h)), and adds the geometric reading: a hexagram crosses between the
two tetrahedra exactly when h is odd. So the 32 within-chamber hexagrams have
h = 0 or 2, and the 32 cross-chamber ones h = 1 or 3; h = 3 are the 8 that go
straight through the Field Origin along a body diagonal.
"""

from math import comb

from gravity_field_model.framework import *

TETA = {1, 2, 4, 7}


class HexagramParity(Test):
    name = "19. Hexagrams by Hamming Distance and Chamber"
    question = (
        "How do the 64 hexagrams divide by how many lines change, and how does that relate to "
        "crossing between the two tetrahedra?"
    )
    reference = "PROOF.md Theorem 1(d); research notes (Hamming 8/24/24/8)"
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("For all 64 ordered pairs (a, b), compute h = popcount(a XOR b).")
            .step("Tally by h, and by whether a and b lie in the same tetrahedron.")
            .conclude("Compare with 8 C(3, h) and with the parity rule.")
        )

    commentary = (
        "The distribution is 8 / 24 / 24 / 8 = 8 x C(3, h), as for any complete set of ordered "
        "pairs of cube vertices: it is binomial, not specific to pi or to the walk. Its "
        "geometry is the useful part. Changing an even number of lines keeps a trigram in its "
        "family; changing an odd number moves it to the other. So the 32 cross-chamber "
        "hexagrams are exactly those with one or three changing lines, and the 8 with all "
        "three changing are the body diagonals through the Field Origin, the four Shuo Gua "
        "opposites in both directions."
    )

    def model(self):
        by_h = [0, 0, 0, 0]
        parity_ok = 0
        diag = 0
        for a in range(8):
            for b in range(8):
                h = bin(a ^ b).count("1")
                by_h[h] += 1
                cross = (a in TETA) != (b in TETA)
                parity_ok += cross == (h % 2 == 1)
                diag += h == 3 and a + b == 7
        return (
            Model()
            .add("Hexagrams by changing lines h = 0,1,2,3", " ".join(map(str, by_h)))
            .add("Equals 8 C(3,h) (1=yes)", int(by_h == [8 * comb(3, h) for h in range(4)]))
            .add("Hexagrams where crossing = odd h", parity_ok)
            .add("h = 3 hexagrams that are body diagonals", diag)
        )

    def observations(self):
        return (
            Observed()
            .add("Hexagrams by changing lines h = 0,1,2,3", "8 24 24 8")
            .add("Equals 8 C(3,h) (1=yes)", 1)
            # Each line change flips the yang-count parity.
            .add("Hexagrams where crossing = odd h", 64)
            # a XOR b = 7 means b = 7 - a.
            .add("h = 3 hexagrams that are body diagonals", 8)
        )


ALL_TESTS = [HexagramParity]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("19", "Hexagram parity.", ALL_TESTS) else 1)
