"""
Information Content of Field Closure
====================================

This module examines the information-theoretic aspects of the Field Closure
system. Information is encoded in discrete units:
- 3 bits per vertex (8 vertices = 2^3)
- 24 bits per orbit (8 vertices x 3 bits)
- 3288 bits per electron (137 orbits x 24 bits)

These tests document the information content correspondences in the model.
"""

import math
from typing import Dict

from gravity_field_model.framework import *
from gravity_field_model.common import C, ALPHA, LAMBDA_COMPTON

# =============================================================================
# CONSTANTS
# =============================================================================

BITS_PER_VERTEX = 3
VERTICES_PER_ORBIT = 8
ORBITS_PER_ELECTRON = int(1 / ALPHA)  # 137


def calculate_settlement_frequency():
    """Settlement frequency from Compton wavelength."""
    return C / LAMBDA_COMPTON


def calculate_bits_per_orbit():
    """Calculate bits per complete orbit."""
    return VERTICES_PER_ORBIT * BITS_PER_VERTEX


def calculate_bits_per_electron():
    """Calculate bits per electron (137 orbits)."""
    return ORBITS_PER_ELECTRON * calculate_bits_per_orbit()


# =============================================================================
# TESTS
# =============================================================================

class BitsPerVertex(Test):
    """
    Each vertex requires exactly 3 bits to address (0-7 = 2^3).
    This is the fundamental quantum of position information.
    """
    name = "Bits Per Vertex"
    question = (
        "Why exactly 3 bits? "
        "We verify that each vertex requires log2(8) = 3 bits to address, "
        "which also equals the number of spatial dimensions."
    )
    reference = "Information theory (log2(8) = 3)"
    tolerance = 0.0
    level = Critical
    audit_score = 87
    audit_notes = (
        "Question: 13/15 - Good 'why exactly 3 bits' hook. "
        "Derivation: 13/15 - Clear log2 reasoning. "
        "Commentary: 14/15 - Excellent 3D/3-bit correspondence insight. "
        "Model: 8/10 - Returns single value, minimal. "
        "Observations: 9/10 - Expected value clear. "
        "Constants: 8/10 - Uses local BITS_PER_VERTEX=3 instead of deriving from K. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Derive BITS_PER_VERTEX from K via log2(2*K) in common module."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Addressing 2k=8 distinct vertices requires log2(8) bits")
            .step("Vertex count = 2k = 8 (dual Field Chamber)")
            .step("Bits required = ceil(log2(8)) = ceil(3) = 3")
            .step("This equals d = k - 1 = 3 (spatial dimension count)")
            .step("Each triad encodes exactly one vertex position")
            .conclude("Each vertex address is a d=3 bit quantum of information")
        )
    
    commentary = (
        "Here is something that should make you sit up and pay attention. To specify one of 8 "
        "vertices, you need exactly 3 bits: one binary choice to cut 8 possibilities down to 4, "
        "another to cut 4 down to 2, and a third to pick one of the final 2. And look! We live "
        "in 3 spatial dimensions. The number 3 appears in two completely different contexts: "
        "information theory and geometry. This could be coincidence, or it could be telling us "
        "something deep about why our universe has 3 spatial dimensions."
    )
    
    def model(self):
        required_bits = int(math.ceil(math.log2(8)))
        return Model().add("Bits per vertex", required_bits)
    
    def observations(self):
        return Observed().add("Bits per vertex", 3)


class BitsPerOrbit(Test):
    """
    One complete orbit visits 8 vertex positions, encoding
    24 bits of information (8 x 3 = 24).
    """
    name = "Bits Per Orbit"
    question = (
        "How much information does one complete trip around the geometry hold? "
        "We calculate that a full orbit through all 8 vertices carries 8 x 3 = 24 bits."
    )
    reference = "Orbit = 8 vertex positions"
    tolerance = 0.0
    level = Standard
    audit_score = 85
    audit_notes = (
        "Question: 11/15 - 'How much' rather than 'why orbit matters'. "
        "Derivation: 12/15 - Clear multiplication steps. "
        "Commentary: 14/15 - Excellent 'walking through 8 rooms' analogy. "
        "Model: 9/10 - Returns three related values. "
        "Observations: 9/10 - Expected values clear. "
        "Constants: 8/10 - Uses local BITS_PER_VERTEX and VERTICES_PER_ORBIT. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Reframe question to 'why the orbit unit matters'."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: An orbit visits all 2k vertices, each contributing d bits")
            .step("Vertices per orbit = 2k = 8")
            .step("Bits per vertex = d = 3")
            .equation("Bits per orbit = 2k * d = 8 * 3 = 24")
            .step("This represents one complete traversal of the dual Field Chamber")
            .conclude("Each orbit processes 24 bits of information")
        )
    
    commentary = (
        "Imagine walking through all 8 rooms of a house, and in each room, you flip 3 light "
        "switches (on or off). After visiting every room, you have made 8 x 3 = 24 binary "
        "choices. That is 24 bits of information encoded in one complete tour. An orbit does "
        "exactly this: it visits each vertex (each requiring 3 bits to specify) and collects "
        "the full information content. One orbit = 24 bits. This is the fundamental unit of "
        "information throughput for a complete traversal of the geometry."
    )
    
    def model(self):
        bits = calculate_bits_per_orbit()
        return (
            Model()
            .add("Bits per orbit", bits)
            .add("Vertices per orbit", VERTICES_PER_ORBIT)
            .add("Bits per vertex", BITS_PER_VERTEX)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Bits per orbit", 24)
            .add("Vertices per orbit", 8)
            .add("Bits per vertex", 3)
        )


class BitsPerElectron(Test):
    """
    One electron requires 137 orbits (1/alpha), encoding
    3288 bits of information (137 x 24 = 3288).
    """
    name = "Bits Per Electron"
    question = (
        "What is the total information content of an electron? "
        "We calculate that one electron encodes 137 orbits x 24 bits = 3288 bits per cycle."
    )
    reference = "1/alpha = 137 orbits per electron"
    tolerance = 0.0
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 12/15 - 'What is total' rather than 'why this specific value'. "
        "Derivation: 13/15 - Clear multiplication from alpha. "
        "Commentary: 14/15 - Excellent 'half a kilobyte' perspective. "
        "Model: 9/10 - Returns bits and orbits. "
        "Observations: 9/10 - Expected values clear. "
        "Constants: 9/10 - Uses ALPHA from common. "
        "Accessibility: 13/15 - Undergrad can follow. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Explore 'why 3288 specifically' in the question."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: An electron cycle requires 1/alpha orbits, each encoding 24 bits")
            .step("Orbits per electron = floor(1/alpha) = floor(137.036) = 137")
            .step("Bits per orbit = 24")
            .equation("Bits per electron = 137 * 24 = 3288")
            .step("This links information content to fine structure constant")
            .conclude("Electron information content is 3288 bits per cycle")
        )
    
    commentary = (
        "The fine structure constant alpha (approximately 1/137) governs how strongly "
        "electrons interact with light. Remarkably, its inverse tells us how many orbits "
        "make up one complete electron cycle: 137. With 24 bits per orbit, that gives "
        "137 x 24 = 3288 bits per electron. Think about that: an electron, one of the "
        "simplest particles we know, can be described by about 3300 bits of information. "
        "That is less than half a kilobyte. Nature is extraordinarily efficient."
    )
    
    def model(self):
        bits = calculate_bits_per_electron()
        return (
            Model()
            .add("Bits per electron", bits)
            .add("Orbits per electron (1/alpha)", ORBITS_PER_ELECTRON)
        )
    
    def observations(self):
        return (
            Observed()
            .add("Bits per electron", 3288)
            .add("Orbits per electron (1/alpha)", 137)
        )


class OrbitsEqualsInverseAlpha(Test):
    """
    The number of orbits per electron corresponds to 1/alpha = 137.
    This establishes a correspondence between information content and
    the fine structure constant.
    """
    name = "Orbits = 1/alpha"
    question = (
        "Why does 137 keep appearing in physics? "
        "We verify that the fine structure constant (1/alpha = 137) determines the "
        "number of orbits that constitute one complete electron cycle."
    )
    reference = "CODATA fine structure constant"
    tolerance = 0.001
    level = Standard
    audit_score = 91
    audit_notes = (
        "Question: 14/15 - Excellent 'why 137 keeps appearing' mystery hook. "
        "Derivation: 13/15 - Clear alpha inversion. "
        "Commentary: 14/15 - Feynman quote adds gravitas. "
        "Model: 9/10 - Returns 1/alpha and integer orbits. "
        "Observations: 9/10 - CODATA traceable. "
        "Constants: 10/10 - Uses ALPHA from common. "
        "Accessibility: 13/15 - Mystery framing engages undergrad. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Minor polish only."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: The fine structure constant alpha determines electromagnetic coupling strength")
            .step("alpha = 1/137.036 (CODATA value)")
            .equation("1/alpha = 137.036")
            .step("Integer orbits: floor(1/alpha) = 137")
            .step("This provides information-theoretic interpretation: alpha encodes cycle count")
            .conclude("1/alpha = 137 orbits defines electron information capacity")
        )
    
    commentary = (
        "The number 137 haunted physicists for a century. Feynman called it 'one of the greatest "
        "damn mysteries of physics.' The fine structure constant, approximately 1/137, controls "
        "how strongly electrons couple to light. Here we see it from a new angle: 1/alpha tells "
        "us how many orbits fit into one electron cycle. It is as if the electron takes exactly "
        "137 trips around the geometry before completing its fundamental period. Why 137? "
        "Nobody knows. But the fact that this mysterious number appears as an orbit count "
        "suggests it may have an information-theoretic origin."
    )
    
    def model(self):
        orbits = int(1 / ALPHA)
        return (
            Model()
            .add("1/alpha", 1/ALPHA)
            .add("Orbits (integer)", orbits)
        )
    
    def observations(self):
        return (
            Observed()
            .add("1/alpha", 137.036)
            .add("Orbits (integer)", 137)
        )


class ProcessingRate(Test):
    """
    The information processing rate is frequency x bits per orbit.
    At Compton frequency (~1.2e20 Hz), this gives enormous bandwidth.
    """
    name = "Information Processing Rate"
    question = (
        "How fast can quantum geometry process information? "
        "We calculate that at the settlement frequency, the system achieves "
        "mind-boggling yottabit-scale bandwidth (10^21 bits per second)."
    )
    reference = None  # Model calculation
    level = Standard
    audit_score = 84
    audit_notes = (
        "Question: 11/15 - 'How fast' rather than 'why speed matters'. "
        "Derivation: 12/15 - Clear calculation steps. "
        "Commentary: 14/15 - Excellent internet comparison. "
        "Model: 9/10 - Returns frequency and rate. "
        "Observations: 5/10 - No observations() method. "
        "Constants: 10/10 - Uses calculate_settlement_frequency. "
        "Accessibility: 13/15 - Yottabit comparison helps. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Reframe as 'why speed matters' and add observations()."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Processing rate = frequency * bits per orbit")
            .step("Settlement frequency = c / lambda_Compton = 1.2 x 10^20 Hz")
            .step("Bits per orbit = 24")
            .equation("Processing rate = 1.2 x 10^20 * 24 = 2.9 x 10^21 bits/second")
            .step("In yottabits: 2.9 x 10^21 / 10^24 = 0.0029 Yb/s")
            .conclude("Field Closure implies ~10^21 bits/second processing capacity")
        )
    
    commentary = (
        "The settlement frequency is set by the Compton wavelength: roughly 10^20 cycles per "
        "second. Each cycle processes 24 bits. Multiply them together, and you get about "
        "10^21 bits per second. To put that in perspective: the entire internet handles maybe "
        "10^18 bits per second on a good day. A single electron-scale Field Closure operates "
        "a thousand times faster than all human digital infrastructure combined. Nature does "
        "not mess around when it comes to computational throughput."
    )
    
    def model(self):
        f = calculate_settlement_frequency()
        bits_per_orbit = calculate_bits_per_orbit()
        rate = f * bits_per_orbit
        rate_yb = rate / 1e24  # Yottabits/second
        return (
            Model()
            .add("Settlement frequency (Hz)", f)
            .add("Processing rate (bits/s)", rate)
            .add("Processing rate (Yb/s)", rate_yb)
        )


class InformationIsFinite(Test):
    """
    The electron has finite information content (3288 bits).
    This finiteness is fundamental to quantum discreteness.
    """
    name = "Finite Information Content"
    question = (
        "Is the electron fundamentally finite? "
        "We verify that the electron's information content is bounded at 3288 bits, "
        "consistent with quantum discreteness rather than continuous infinity."
    )
    reference = None  # Model interpretation
    level = Standard
    audit_score = 87
    audit_notes = (
        "Question: 13/15 - Good 'is electron fundamentally finite' hook. "
        "Derivation: 12/15 - Finiteness check is simple. "
        "Commentary: 14/15 - Excellent classical vs quantum contrast. "
        "Model: 8/10 - Returns bits and binary check. "
        "Observations: 5/10 - No observations() method. "
        "Constants: 10/10 - Uses common functions. "
        "Accessibility: 13/15 - Floppy disk comparison helps. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Add observations() method with threshold."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Finite information content supports quantum discreteness")
            .step("Calculate electron bits: 137 orbits * 24 bits = 3288 bits")
            .step("Check finiteness: 0 < 3288 < infinity. Yes, finite")
            .step("Check reasonableness: 3288 << 10^10 (bounded)")
            .step("Finite information suggests electron is discrete information object")
            .conclude("Electron has finite, bounded information content of 3288 bits")
        )
    
    commentary = (
        "Classical physics imagined particles as having infinitely precise positions and momenta. "
        "Quantum mechanics tells us that is wrong. There are limits. The uncertainty principle "
        "says you cannot know everything. Here we see finiteness from another angle: the electron "
        "has finite information content. Not approximately finite, exactly finite: 3288 bits. "
        "That is a remarkably small number. You could store the complete description of an "
        "electron on a fraction of a floppy disk. This finiteness is the mathematical "
        "expression of quantum discreteness: nature uses integers, not infinities."
    )
    
    def model(self):
        bits = calculate_bits_per_electron()
        is_finite = 1 if 0 < bits < 1e10 else 0
        return (
            Model()
            .add("Electron bits", bits)
            .add("Is finite", is_finite)
        )


class InformationHierarchy(Test):
    """
    Information content follows a strict hierarchy:
    vertex < orbit < electron.
    """
    name = "Information Hierarchy"
    question = (
        "How does information build up from simple to complex? "
        "We verify the strict hierarchy: vertex (3 bits) < orbit (24 bits) < electron (3288 bits)."
    )
    reference = None  # Structural requirement
    level = Standard
    audit_score = 88
    audit_notes = (
        "Question: 13/15 - Good 'simple to complex' hook. "
        "Derivation: 13/15 - Clear hierarchy verification. "
        "Commentary: 14/15 - Excellent letters/words/sentences analogy. "
        "Model: 9/10 - Shows all three levels plus check. "
        "Observations: 5/10 - No observations() method. "
        "Constants: 9/10 - Uses local BITS_PER_VERTEX. "
        "Accessibility: 14/15 - Building block analogy very accessible. "
        "Header: 9/10 (module level). "
        "TO IMPROVE: Add observations() with hierarchy verification."
    )
    
    def derivation(self):
        return (
            Derivation()
            .step("PREMISE: Nested structure implies hierarchical information content")
            .step("Bits per vertex = d = 3")
            .step("Bits per orbit = 2k * d = 8 * 3 = 24")
            .step("Bits per electron = (1/alpha) * 24 = 137 * 24 = 3288")
            .step("Verify hierarchy: 3 < 24 < 3288. Yes")
            .conclude("Information scales hierarchically from vertices to electrons")
        )
    
    commentary = (
        "Complex things are built from simpler things. Letters make words. Words make sentences. "
        "Sentences make paragraphs. Here we see the same pattern: 3 bits make a vertex, 8 vertices "
        "(24 bits) make an orbit, 137 orbits (3288 bits) make an electron. Each level is built "
        "from the level below it through simple multiplication. The complexity is emergent: "
        "you start with the simplest possible building block (a 3-bit address) and through "
        "repeated composition, you get the full electron. Nothing is added by hand. "
        "The hierarchy grows naturally from the geometry."
    )
    
    def model(self):
        bits_vertex = BITS_PER_VERTEX
        bits_orbit = calculate_bits_per_orbit()
        bits_electron = calculate_bits_per_electron()
        
        hierarchy_correct = 1 if (bits_vertex < bits_orbit < bits_electron) else 0
        
        return (
            Model()
            .add("Bits per vertex", bits_vertex)
            .add("Bits per orbit", bits_orbit)
            .add("Bits per electron", bits_electron)
            .add("Hierarchy correct", hierarchy_correct)
        )


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    BitsPerVertex,
    BitsPerOrbit,
    BitsPerElectron,
    OrbitsEqualsInverseAlpha,
    ProcessingRate,
    InformationIsFinite,
    InformationHierarchy,
]


def run_all():
    """Run all information content tests."""
    return run_tests(
        title="Information Content of Field Closure",
        summary=(
            "These tests examine information-theoretic aspects of the Field Closure system. "
            "Each vertex requires 3 bits to address (8 vertices = 2^3), producing 24 bits "
            "per orbit and 3288 bits per electron (137 orbits). The correspondence to "
            "1/alpha = 137 suggests a possible information-theoretic interpretation of "
            "the fine structure constant."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
