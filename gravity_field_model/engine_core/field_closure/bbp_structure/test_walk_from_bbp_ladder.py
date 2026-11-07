"""
The closure walk driven by the BBP ladder alone
===============================================

Role:     Supporting finding: the closure walk can be driven by the BBP formula alone.
Expected: Passes. A failure means the ladder-driven walk differs from the stored-digit walk.

Every digit the I Ching closure walk uses can be taken from the BBP ladder
(bbp_ladder.py), each from its own rung, with no stored digits and no
arbitrary-precision library. This test drives the walk that way and checks
that it is the same walk: same vertices, closure of all 64 hexagrams at step
332 (the value reported by closure_walk_proof_iching.py).

It also records how the walk uses the ladder. The ladder gives each digit
independently; the walk's position is the running sum of all digits so far,
mod 8. So a change at one rung moves every later position, and the walk
climbs the rungs in order.
"""

from gravity_field_model.framework import *
from gravity_field_model.common.pi_data import PI_BASE8_FRACTIONAL
from gravity_field_model.engine_core.field_closure.bbp_structure.bbp_ladder import octal_digits_from_ladder

N_DIGITS = 400


def walk(digits):
    cum, verts = 0, []
    for d in digits:
        cum += d
        verts.append(cum % 8)
    return verts


def closure_step(verts):
    seen = set()
    for i in range(1, len(verts)):
        seen.add((verts[i - 1], verts[i]))
        if len(seen) == 64:
            return i
    return None


class WalkFromBBPLadder(Test):
    name = "Closure Walk Driven by the BBP Ladder"
    question = (
        "Can the I Ching closure walk be driven by the BBP formula alone, taking each base-8 "
        "digit from its own rung, and is it then the same walk?"
    )
    reference = (
        "Walk: research/exploratory/i-ching/closure_walk_proof_iching.py (closure at step 332); "
        "ladder: Bailey, Borwein, Plouffe (1997)"
    )
    tolerance = 0.0
    level = Level.STANDARD

    def derivation(self):
        return (
            Derivation()
            .step("Take base-8 digits 1..400 of pi, each from its own BBP rung.")
            .step("Prepend the integer part 3 and run the walk: vertex = running sum mod 8.")
            .step("Compare with the walk on the stored mpmath digits; find the 64-hexagram closure step.")
            .step("Change only digit 1 and count how many later positions move.")
            .conclude("The ladder supplies the digits independently; the walk accumulates them in order.")
        )

    commentary = (
        "Driven by the BBP formula alone, the walk is identical to the walk on the stored "
        "digits and closes all 64 hexagrams at step 332. Pi's trigram stream, and the walk it "
        "drives, are therefore fixed by the four BBP slots: the walk is deterministic and "
        "reproducible from the formula. The ladder and the walk use pi in two ways. The "
        "ladder reaches any digit directly. The walk adds the digits up, so its position at "
        "step n depends on every digit before it: changing one rung moves every later "
        "vertex. No shortcut is known that gives the walk's position at step n from rung n "
        "alone; the walk climbs the ladder one rung at a time."
    )

    def model(self):
        ladder = octal_digits_from_ladder(N_DIGITS)
        v_ladder = walk([3] + ladder)
        v_stored = walk([3] + list(PI_BASE8_FRACTIONAL[:N_DIGITS]))
        changed = list(ladder)
        changed[0] = (changed[0] + 1) % 8
        v_changed = walk([3] + changed)
        moved = sum(1 for a, b in zip(v_ladder[1:], v_changed[1:]) if a != b) / N_DIGITS
        only_rung_n = sum(1 for i in range(1, N_DIGITS + 1) if v_ladder[i] == ladder[i - 1] % 8) / N_DIGITS
        return (
            Model()
            .add("Ladder digits equal stored digits (1=yes)", int(ladder == list(PI_BASE8_FRACTIONAL[:N_DIGITS])))
            .add("Walk vertices identical (1=yes)", int(v_ladder == v_stored))
            .add("64-hexagram closure step (ladder-driven)", closure_step(v_ladder))
            .add("Later positions moved by changing digit 1 (fraction)", moved)
            .add("Steps where the vertex equals that rung's digit (info)", round(only_rung_n, 3))
        )

    def observations(self):
        return (
            Observed()
            .add("Ladder digits equal stored digits (1=yes)", 1)
            .add("Walk vertices identical (1=yes)", 1)
            # Reported by closure_walk_proof_iching.py from mpmath digits.
            .add("64-hexagram closure step (ladder-driven)", 332)
            # Running sum: every later partial sum shifts by the same nonzero amount mod 8.
            .add("Later positions moved by changing digit 1 (fraction)", 1.0, abs_tol=0.0)
        )


ALL_TESTS = [WalkFromBBPLadder]

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_tests("Walk from BBP ladder", "The closure walk driven by the BBP formula alone.", ALL_TESTS) else 1)
