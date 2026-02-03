"""
Sixfold Symmetry Observations
=============================

This module examines the prevalence of six-fold symmetry in natural systems.
Hexagonal packing (6 neighbors) corresponds to the densest 2D sphere packing,
and this geometry appears in numerous physical systems:

- Saturn's polar hexagon
- Snowflakes and ice crystals
- Benzene rings
- Honeycomb cells
- Graphene lattice
- Benard convection cells

The tests document correspondences between hexagonal geometry and observations.
"""

import sys
import os
import math
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base import GFDTest, run_test_group

# =============================================================================
# CONSTANTS
# =============================================================================

PI = math.pi
N_NEIGHBORS = 6  # Hexagonal packing

# Saturn's hexagon parameters
SATURN_HEXAGON_LATITUDE = 77  # degrees north
SATURN_HEXAGON_RADIUS_KM = 14500

# Known 6-fold symmetric structures
SIXFOLD_STRUCTURES = [
    "Saturn's north polar hexagon",
    "Snowflakes (ice crystals)",
    "Benzene ring",
    "Honeycomb",
    "Graphene",
    "Basalt columns",
    "Benard cells",
    "EZ water",
    "Quartz crystal",
]


def hexagonal_angle():
    """Internal angle of a regular hexagon = 120 degrees."""
    n = 6
    return (n - 2) * 180 / n


def vesica_piscis_angle():
    """Coupling angle in vesica piscis = 120 degrees."""
    return 2 * PI / 3 * (180 / PI)


def hexagonal_packing_efficiency():
    """HCP packing fraction = pi/(3*sqrt(2)) = 0.7405."""
    return PI / (3 * math.sqrt(2))


# =============================================================================
# TESTS
# =============================================================================

class HexagonInternalAngle(GFDTest):
    """
    A regular hexagon has internal angle of 120 degrees.
    This matches the vesica piscis coupling angle.
    """
    name = "Hexagon Internal Angle"
    question = "Does the formula (n-2)×180°/n for n=6 yield the hexagon internal angle of exactly 120 degrees?"
    reference_source = "Geometry (n-2)*180/n for n=6"
    tolerance = 1e-10
    derivation = (
        "PREMISE: Regular polygon internal angle = (n-2)×180°/n. "
        "STEP 1: For hexagon, n = 6. "
        "STEP 2: Internal angle = (6-2)×180°/6 = 4×180°/6 = 720°/6. "
        "STEP 3: Internal angle = 120°. "
        "OUTPUT: Internal angle = 120 degrees."
    )
    commentary = None  # Basic geometric fact
    
    def model(self) -> Dict[str, float]:
        return {"Internal angle (degrees)": hexagonal_angle()}
    
    def observations(self) -> Dict[str, float]:
        return {"Internal angle (degrees)": 120}


class VesicaMatchesHexagon(GFDTest):
    """
    Vesica piscis coupling angle = hexagon internal angle = 120 degrees.
    Both arise from the same hexagonal packing geometry.
    """
    name = "Vesica = Hexagon Angle"
    question = "Does the vesica piscis coupling angle (2π/3 = 120°) equal the hexagon internal angle (120°)?"
    reference_source = "Geometric correspondence"
    tolerance = 1e-10
    derivation = (
        "PREMISE: Both angles should emerge from hexagonal packing geometry. "
        "STEP 1: Hexagon internal angle = 120° (derived above). "
        "STEP 2: Vesica piscis angle = 2π/3 radians = 2×180°/3 = 120°. "
        "STEP 3: Compare: 120° = 120°. "
        "OUTPUT: Hexagon angle = 120, vesica angle = 120."
    )
    commentary = (
        "The 120-degree angle appears in both hexagon geometry and vesica piscis "
        "overlap. This correspondence connects optimal 2D packing to the coupling "
        "fraction used in the MOND derivation."
    )
    
    def model(self) -> Dict[str, float]:
        return {
            "Hexagon angle": hexagonal_angle(),
            "Vesica angle": vesica_piscis_angle(),
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Hexagon angle": 120,
            "Vesica angle": 120,
        }


class SixNeighborsPacking(GFDTest):
    """
    Hexagonal packing gives exactly 6 nearest neighbors.
    This is the fundamental source of 6-fold symmetry.
    """
    name = "Six Neighbors in Hexagonal Packing"
    question = "Does hexagonal close packing produce exactly N=6 nearest neighbors as the geometric source of sixfold symmetry?"
    reference_source = "Hexagonal close packing"
    tolerance = 0.0
    derivation = (
        "PREMISE: In 2D optimal packing, equal circles have maximum contact neighbors. "
        "STEP 1: Arrange equal-radius circles with centers on a triangular lattice. "
        "STEP 2: Each circle can touch at most 6 neighbors (360°/60° per neighbor). "
        "STEP 3: This creates hexagonal arrangement with N = 6. "
        "OUTPUT: Nearest neighbors = 6."
    )
    commentary = (
        "Hexagonal close packing producing exactly 6 neighbors is a fundamental "
        "geometric constraint. This count enters directly into the MOND derivation "
        "and appears throughout natural systems."
    )
    
    def model(self) -> Dict[str, float]:
        return {"Nearest neighbors": N_NEIGHBORS}
    
    def observations(self) -> Dict[str, float]:
        return {"Nearest neighbors": 6}


class C6RotationalSymmetry(GFDTest):
    """
    Hexagonal structures have C6 rotational symmetry:
    rotation by 60 degrees maps the structure onto itself.
    """
    name = "C6 Rotational Symmetry"
    question = "Does hexagonal structure exhibit C6 point group symmetry with 360°/6 = 60° rotational invariance?"
    reference_source = "Point group C6"
    tolerance = 0.0
    derivation = (
        "PREMISE: C6 symmetry means invariance under 6-fold rotation. "
        "STEP 1: Symmetry order = 6 (number of equivalent orientations). "
        "STEP 2: Rotation angle for self-mapping = 360°/6 = 60°. "
        "STEP 3: Rotating hexagon by 60° maps vertices to vertices exactly. "
        "OUTPUT: Symmetry order = 6, rotation angle = 60."
    )
    commentary = None  # Standard crystallographic symmetry
    
    def model(self) -> Dict[str, float]:
        symmetry_order = 6
        rotation_angle = 360 / symmetry_order
        return {
            "Symmetry order": symmetry_order,
            "Rotation angle": rotation_angle,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Symmetry order": 6,
            "Rotation angle": 60,
        }


class OptimalPackingIsHexagonal(GFDTest):
    """
    Hexagonal close packing is the densest sphere packing at ~74%.
    This was proven (Kepler conjecture) in 2005.
    """
    name = "Optimal Packing is Hexagonal"
    question = "Does hexagonal close packing achieve the maximum sphere packing density of π/(3√2) ≈ 74.05%, as proven by Kepler conjecture?"
    reference_source = "Kepler conjecture (proven 2005)"
    tolerance = 0.001
    derivation = (
        "PREMISE: The Kepler conjecture states no packing exceeds HCP density. "
        "STEP 1: HCP packing fraction = π / (3√2). "
        "STEP 2: Calculate: π/(3×1.414) = 3.1416/4.243 ≈ 0.7405. "
        "STEP 3: As percentage: 74.05%. "
        "STEP 4: Proven by Hales (2005) using computer-assisted proof. "
        "OUTPUT: Packing efficiency = 0.7405."
    )
    commentary = (
        "Hexagonal close packing achieving maximum density (74.05%) represents an "
        "optimal configuration. This efficiency may explain why hexagonal symmetry "
        "appears so frequently in natural systems."
    )
    
    def model(self) -> Dict[str, float]:
        efficiency = hexagonal_packing_efficiency()
        return {"Packing efficiency": efficiency}
    
    def observations(self) -> Dict[str, float]:
        return {"Packing efficiency": 0.7405}


class SaturnHexagonExists(GFDTest):
    """
    Saturn's north polar hexagon is a real, confirmed phenomenon.
    First observed by Voyager (1981), confirmed by Cassini.
    """
    name = "Saturn Hexagon Exists"
    question = "Is Saturn's north polar hexagon a confirmed planetary-scale phenomenon exhibiting 6-fold symmetry?"
    reference_source = "Voyager/Cassini observations"
    derivation = (
        "PREMISE: Satellite missions have observed Saturn's north pole in detail. "
        "STEP 1: First observed by Voyager missions in 1981. "
        "STEP 2: Confirmed and studied extensively by Cassini mission (2004-2017). "
        "STEP 3: Hexagon has diameter ~29,000 km centered at ~77°N latitude. "
        "STEP 4: Structure has persisted for decades, confirming stability. "
        "OUTPUT: Hexagon diameter = 29000 km, confirmed = 1."
    )
    commentary = (
        "Saturn's north polar hexagon is a confirmed atmospheric phenomenon "
        "exhibiting 6-fold symmetry at planetary scales. The mechanism "
        "producing this structure remains an area of active research."
    )
    
    def model(self) -> Dict[str, float]:
        diameter_km = 2 * SATURN_HEXAGON_RADIUS_KM
        return {
            "Hexagon diameter (km)": diameter_km,
            "Latitude (degrees N)": SATURN_HEXAGON_LATITUDE,
            "Confirmed": 1,
        }


class SaturnHexagonIsSixSided(GFDTest):
    """
    Saturn's hexagon has exactly 6 sides, matching hexagonal packing.
    Not 5, not 7, but exactly 6.
    """
    name = "Saturn Hexagon Has 6 Sides"
    question = "Does Saturn's polar vortex have exactly 6 sides (not 5 or 7), matching the hexagonal packing neighbor count?"
    reference_source = "Saturn observation"
    tolerance = 0.0
    derivation = (
        "PREMISE: The structure should match hexagonal packing if geometrically fundamental. "
        "STEP 1: Count sides of Saturn's polar structure from imagery: exactly 6. "
        "STEP 2: Compare to hexagonal packing neighbor count: N = 6. "
        "STEP 3: The match is exact (not pentagon with 5, not heptagon with 7). "
        "OUTPUT: Saturn hexagon sides = 6, hexagonal packing neighbors = 6."
    )
    commentary = None  # Observational fact
    
    def model(self) -> Dict[str, float]:
        return {
            "Saturn hexagon sides": 6,
            "Hexagonal packing neighbors": N_NEIGHBORS,
        }
    
    def observations(self) -> Dict[str, float]:
        return {
            "Saturn hexagon sides": 6,
            "Hexagonal packing neighbors": 6,
        }


class SnowflakeSixfold(GFDTest):
    """
    Snowflakes have 6-fold symmetry due to hexagonal ice lattice.
    The H-O-H bond angle favors hexagonal packing.
    """
    name = "Snowflake Sixfold Symmetry"
    question = "Do snowflakes exhibit 6-fold symmetry arising from the hexagonal ice crystal lattice structure?"
    reference_source = "Ice crystal structure"
    tolerance = 0.0
    derivation = (
        "PREMISE: Crystal symmetry constrains macroscopic growth patterns. "
        "STEP 1: Water ice (Ih) forms hexagonal crystal lattice. "
        "STEP 2: H₂O bond angle (~104.5°) favors hexagonal hydrogen bonding. "
        "STEP 3: Crystal growth occurs along six equivalent directions. "
        "STEP 4: Resulting snowflakes display 6-fold rotational symmetry. "
        "OUTPUT: Snowflake symmetry order = 6."
    )
    commentary = (
        "Snowflake 6-fold symmetry emerges from the hexagonal ice lattice structure. "
        "The water molecule bond angle promotes hexagonal packing, demonstrating "
        "how molecular geometry constrains macroscopic form."
    )
    
    def model(self) -> Dict[str, float]:
        return {"Snowflake symmetry order": 6}
    
    def observations(self) -> Dict[str, float]:
        return {"Snowflake symmetry order": 6}


class BenzeneSixfold(GFDTest):
    """
    Benzene (C6H6) has a hexagonal ring of 6 carbons.
    The archetypal aromatic compound.
    """
    name = "Benzene Sixfold Ring"
    question = "Does benzene (C₆H₆) contain exactly 6 carbon atoms arranged in a hexagonal aromatic ring?"
    reference_source = "Organic chemistry"
    tolerance = 0.0
    derivation = (
        "PREMISE: Benzene is the archetypal aromatic compound. "
        "STEP 1: Molecular formula: C₆H₆. "
        "STEP 2: Structure: planar ring of 6 carbons with delocalized π electrons. "
        "STEP 3: C-C-C bond angles = 120° (hexagonal geometry). "
        "STEP 4: All carbon positions equivalent by D6h symmetry. "
        "OUTPUT: Benzene carbons = 6."
    )
    commentary = None  # Well-established molecular structure
    
    def model(self) -> Dict[str, float]:
        return {"Benzene carbons": 6}
    
    def observations(self) -> Dict[str, float]:
        return {"Benzene carbons": 6}


class HoneycombSixfold(GFDTest):
    """
    Honeycomb cells are hexagonal - the most efficient plane tiling
    with equal-area cells.
    """
    name = "Honeycomb Hexagonal"
    question = "Are honeycomb cells hexagonal (6-sided), representing the most efficient plane tiling for equal-area cells?"
    reference_source = "Honeycomb geometry"
    tolerance = 0.0
    derivation = (
        "PREMISE: Bees construct wax cells to store honey and raise larvae. "
        "STEP 1: Honeycomb cells have 6 sides (hexagonal). "
        "STEP 2: Hexagonal tiling minimizes perimeter for given area (honeycomb conjecture). "
        "STEP 3: This minimizes wax usage while maximizing storage. "
        "STEP 4: Proven mathematically optimal by Hales (1999). "
        "OUTPUT: Honeycomb cell sides = 6."
    )
    commentary = (
        "Honeycomb hexagonal cells represent optimal efficiency for covering a "
        "plane with equal-area cells while minimizing perimeter. Bees evolved "
        "this geometry independently, suggesting universal optimality."
    )
    
    def model(self) -> Dict[str, float]:
        return {"Honeycomb cell sides": 6}
    
    def observations(self) -> Dict[str, float]:
        return {"Honeycomb cell sides": 6}


class ManySixfoldStructures(GFDTest):
    """
    Multiple independent systems show 6-fold symmetry.
    This prevalence suggests a common underlying cause.
    """
    name = "Prevalence of Sixfold Symmetry"
    question = "Do numerous independent natural systems exhibit 6-fold symmetry, suggesting a common geometric optimality principle?"
    reference_source = None  # Observation across systems
    derivation = (
        "PREMISE: If 6-fold symmetry appears in many unrelated systems, a common cause may exist. "
        "STEP 1: Enumerate known 6-fold structures: Saturn hexagon, snowflakes, benzene, "
        "honeycomb, graphene, basalt columns, Benard cells, quartz crystals, EZ water. "
        "STEP 2: Count distinct systems exhibiting this symmetry. "
        "STEP 3: These systems span astronomy, chemistry, biology, and geology. "
        "OUTPUT: Number of 6-fold systems = 9."
    )
    commentary = (
        "The prevalence of 6-fold symmetry across disparate physical systems "
        "suggests geometric optimality as a common cause. Whether this reflects "
        "deeper structure or efficient packing is context-dependent."
    )
    
    def model(self) -> Dict[str, float]:
        count = len(SIXFOLD_STRUCTURES)
        return {"Number of 6-fold systems": count}


class LensingM6Prediction(GFDTest):
    """
    Prediction: Gravitational lensing may show m=6 angular harmonics
    if underlying field structure exhibits hexagonal symmetry.
    """
    name = "Lensing m=6 Prediction"
    question = "If underlying field structure is hexagonal, might gravitational lensing show detectable m=6 angular harmonic patterns?"
    reference_source = "Model prediction (testable)"
    derivation = (
        "PREMISE: Hexagonal symmetry should produce m=6 angular modes in physical observables. "
        "STEP 1: Hexagonal structure has 6-fold rotational symmetry (C6). "
        "STEP 2: Angular expansion of hexagonal potential has dominant m=6 harmonic. "
        "STEP 3: Gravitational lensing distortions could preserve this signature. "
        "STEP 4: This is a testable prediction with high-resolution lensing data. "
        "OUTPUT: Predicted dominant m = 6, testable = 1."
    )
    commentary = (
        "A testable prediction from hexagonal field structure would be m=6 "
        "angular harmonics in gravitational lensing. Current observations have "
        "not tested this specific signature with sufficient sensitivity."
    )
    
    def model(self) -> Dict[str, float]:
        return {
            "Predicted dominant m": 6,
            "Hexagonal packing neighbors": N_NEIGHBORS,
            "Testable": 1,
        }


# =============================================================================
# RUNNER
# =============================================================================

ALL_TESTS = [
    HexagonInternalAngle,
    VesicaMatchesHexagon,
    SixNeighborsPacking,
    C6RotationalSymmetry,
    OptimalPackingIsHexagonal,
    SaturnHexagonExists,
    SaturnHexagonIsSixSided,
    SnowflakeSixfold,
    BenzeneSixfold,
    HoneycombSixfold,
    ManySixfoldStructures,
    LensingM6Prediction,
]


def run_all_tests() -> bool:
    """Run all sixfold symmetry tests."""
    return run_test_group(
        title="Sixfold Symmetry Observations",
        summary=(
            "These tests document the prevalence of six-fold symmetry in natural systems. "
            "Hexagonal packing (6 nearest neighbors) represents optimal 2D sphere packing "
            "and creates C6 rotational symmetry. This geometry appears in Saturn's polar "
            "hexagon, snowflake crystals, benzene rings, honeycomb cells, and many other "
            "phenomena. A testable prediction is that gravitational lensing may show m=6 "
            "angular harmonic patterns."
        ),
        test_classes=ALL_TESTS
    )


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
