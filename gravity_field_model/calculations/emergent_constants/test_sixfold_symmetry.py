"""
Hexagonal Geometry Facts
========================

This module documents geometric facts about hexagonal packing that
underpin the MOND constitutive law derivation.

WHAT THIS MODULE CONTAINS:
Basic geometric facts about hexagonal packing. These are not "emergent
constants" but rather the geometric foundations used in deriving them.

WHAT WAS REMOVED:
- Catalogs of sixfold symmetry in nature (snowflakes, benzene, etc.)
- Saturn's hexagon discussion (interesting but not relevant to derivations)
- Speculative predictions about gravitational lensing
- Anything that observes symmetry but doesn't derive a constant

WHY THESE FACTS MATTER:
The MOND constitutive law C_tiling = 6 * (1/3) * (1/2) = 1 relies on:
- N = 6 neighbors in hexagonal packing
- 120-degree internal angle (vesica piscis)
- Optimal packing efficiency

These geometric facts are verified here for completeness.
"""

import sys
import math

from gravity_field_model.framework import *

# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi


# =============================================================================
# TESTS
# =============================================================================

class HexagonInternalAngle(Test):
    """
    The internal angle of a regular hexagon is 120 degrees.
    
    This matches the vesica piscis coupling angle used in the MOND derivation.
    """
    name = "Hexagon Internal Angle = 120 degrees"
    question = (
        "Does the formula (n-2)*180/n for n=6 yield the hexagon internal "
        "angle of 120 degrees?"
    )
    reference = "Euclidean geometry"
    tolerance = 1e-10
    level = Level.STANDARD
    
    commentary = (
        "THE HEXAGON ANGLE:\n"
        "Regular polygon internal angle = (n-2)*180/n degrees.\n"
        "For hexagon (n=6): (6-2)*180/6 = 4*180/6 = 720/6 = 120 degrees.\n\n"
        "This is the same 120 degrees that appears in the vesica piscis\n"
        "coupling angle (2*pi/3 radians), connecting hexagonal packing\n"
        "geometry to the MOND derivation."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("HEXAGON INTERNAL ANGLE:")
            .step("For regular n-gon: angle = (n-2)*180/n degrees.")
            .step("For hexagon, n = 6.")
            .step("Angle = (6-2)*180/6 = 4*180/6 = 720/6 = 120 degrees.")
            .conclude("Hexagon internal angle = 120 degrees.")
        )
    
    def model(self) -> Model:
        n = 6
        angle = (n - 2) * 180 / n
        return Model().add("Internal angle (degrees)", angle)
    
    def observations(self) -> Observed:
        return Observed().add("Internal angle (degrees)", 120)


class HexagonalPackingEfficiency(Test):
    """
    Hexagonal close packing achieves the maximum density: pi/(3*sqrt(2)) ~ 74%.
    
    This was proven by Hales (2005), confirming the Kepler conjecture.
    """
    name = "Hexagonal Packing Efficiency = 74%"
    question = (
        "Does hexagonal close packing achieve the maximum sphere packing "
        "efficiency of pi/(3*sqrt(2)) ~ 74.05%?"
    )
    reference = "Kepler conjecture (proven 2005)"
    tolerance = 0.001
    level = Level.STANDARD
    
    commentary = (
        "THE KEPLER CONJECTURE:\n"
        "No arrangement of equal spheres can exceed the density of\n"
        "hexagonal close packing (or its stacking variant FCC).\n\n"
        "Packing fraction = pi/(3*sqrt(2)) = 0.7405 = 74.05%.\n\n"
        "This was proven by Thomas Hales in 2005 using computer-assisted\n"
        "verification. It explains why hexagonal symmetry is optimal\n"
        "and appears throughout nature."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("HEXAGONAL PACKING EFFICIENCY:")
            .step("Kepler (1611): proposed this is the densest packing.")
            .step("Hales (2005): proved it using computer verification.")
            .step("Packing fraction = pi/(3*sqrt(2)).")
            .step("Calculate: pi/(3*1.414) = 3.1416/4.243 = 0.7405.")
            .conclude("Maximum packing efficiency = 74.05%.")
        )
    
    def model(self) -> Model:
        efficiency = PI / (3 * math.sqrt(2))
        return Model().add("Packing efficiency", round(efficiency, 4))
    
    def observations(self) -> Observed:
        return Observed().add("Packing efficiency", 0.7405)


class C6SymmetryOrder(Test):
    """
    Hexagonal structures have C6 rotational symmetry.
    
    Rotation by 360/6 = 60 degrees maps the structure onto itself.
    """
    name = "C6 Symmetry: 60-degree Rotation"
    question = (
        "Does hexagonal packing exhibit C6 symmetry with 360/6 = 60 degree "
        "rotational invariance?"
    )
    reference = "Point group theory"
    tolerance = 0.0
    level = Level.STANDARD
    
    commentary = (
        "C6 ROTATIONAL SYMMETRY:\n"
        "A hexagonal structure looks the same after rotation by 60 degrees.\n"
        "It has 6 equivalent orientations (symmetry order = 6).\n\n"
        "This is why hexagonal structures have 6-fold patterns:\n"
        "snowflakes, honeycomb, graphene all exhibit C6 symmetry."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("C6 SYMMETRY:")
            .step("Symmetry order = 6.")
            .step("Rotation angle for self-mapping = 360/6 = 60 degrees.")
            .conclude("C6 symmetry has 60-degree rotational invariance.")
        )
    
    def model(self) -> Model:
        symmetry_order = 6
        rotation_angle = 360 / symmetry_order
        return (
            Model()
            .add("Symmetry order", symmetry_order)
            .add("Rotation angle (deg)", rotation_angle)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Symmetry order", 6)
            .add("Rotation angle (deg)", 60)
        )


class VesicaPiscisAngleMatch(Test):
    """
    The vesica piscis angle (2*pi/3 = 120 degrees) equals the hexagon internal angle.
    
    This is not coincidence. Both arise from the same hexagonal geometry.
    """
    name = "Vesica Piscis Angle = Hexagon Angle = 120 deg"
    question = (
        "Does the vesica piscis coupling angle (2*pi/3 = 120 degrees) equal "
        "the hexagon internal angle (120 degrees)?"
    )
    reference = "Geometric correspondence"
    tolerance = 1e-10
    level = Level.STANDARD
    
    commentary = (
        "THE CONNECTION:\n"
        "When circles are packed hexagonally, their overlaps (vesica piscis)\n"
        "subtend 120 degrees. This is the same as the hexagon internal angle.\n\n"
        "This is not coincidence. The vesica piscis angle and the hexagon\n"
        "angle both arise from the same underlying hexagonal geometry.\n"
        "Both are used in the MOND constitutive law derivation."
    )
    
    def derivation(self) -> Derivation:
        return (
            Derivation()
            .step("ANGLE CORRESPONDENCE:")
            .step("Hexagon internal angle: (6-2)*180/6 = 120 degrees.")
            .step("Vesica piscis angle: 2*pi/3 radians = 2*180/3 = 120 degrees.")
            .step("Both = 120 degrees.")
            .conclude("The angles are identical, both from hexagonal geometry.")
        )
    
    def model(self) -> Model:
        hexagon_angle = (6 - 2) * 180 / 6
        vesica_angle = 2 * PI / 3 * (180 / PI)
        difference = abs(hexagon_angle - vesica_angle)
        
        return (
            Model()
            .add("Hexagon angle (deg)", hexagon_angle)
            .add("Vesica angle (deg)", round(vesica_angle, 4))
            .add("Difference", difference)
        )
    
    def observations(self) -> Observed:
        return (
            Observed()
            .add("Hexagon angle (deg)", 120)
            .add("Vesica angle (deg)", 120.0)
            .add("Difference", 0.0)
        )


# =============================================================================
# TEST COLLECTION
# =============================================================================

ALL_TESTS = [
    HexagonInternalAngle,
    HexagonalPackingEfficiency,
    C6SymmetryOrder,
    VesicaPiscisAngleMatch,
]


def run_all() -> bool:
    """Run all hexagonal geometry tests."""
    return run_tests(
        title="Hexagonal Geometry Facts",
        summary=(
            "This module documents geometric facts about hexagonal packing.\n\n"
            "These facts underpin the MOND constitutive law derivation:\n"
            "- Hexagon internal angle = 120 degrees\n"
            "- Optimal packing efficiency = 74%\n"
            "- C6 symmetry order = 6 (60-degree rotation invariance)\n"
            "- Vesica piscis angle = hexagon angle = 120 degrees\n\n"
            "These are geometric facts, not emergent constants.\n"
            "They provide the foundation for the derivation in test_mond_hexagonal.py."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
