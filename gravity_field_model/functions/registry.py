"""
Central Function Registry
=========================

ONLY GRADUATED FUNCTIONS are included here.

Graduation criteria (same as tests):
- audit_score >= 65 (quality threshold)
- contribution_score >= 70 (must be "Significant" or higher)

Functions that don't meet these criteria remain in their source files
but are NOT exposed through this central registry.

DISCOVERING FUNCTIONS:
----------------------
    from gravity_field_model.functions import list_all_functions
    list_all_functions()  # Prints all graduated functions
    
    from gravity_field_model.functions import list_functions_by_group
    list_functions_by_group("stellar_mechanics")  # Functions in a group

USING FUNCTIONS:
----------------
    from gravity_field_model.functions import fn_get_power_output_per_field
    power = fn_get_power_output_per_field(56)  # Fe-56 power output

ADDING NEW FUNCTIONS:
---------------------
1. Define your @Fn function in the appropriate domain file WITH SCORES
2. Ensure audit_score >= 65 and contribution_score >= 70
3. Add import and registration to the appropriate GROUP below
4. Add to __all__ and the group namespace class

See framework/FUNCTION_REGISTRY_GUIDE.md for full documentation.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

# Import the framework's FunctionRegistry to check graduation status
from gravity_field_model.framework import FunctionRegistry


# =============================================================================
# GRADUATION THRESHOLDS
# =============================================================================

AUDIT_THRESHOLD = 65
CONTRIBUTION_THRESHOLD = 70


# =============================================================================
# FUNCTION CATALOG (metadata for discovery)
# =============================================================================

@dataclass
class FunctionEntry:
    """Metadata for a registered function."""
    name: str
    group: str
    equation: str
    description: str
    source_file: str
    function: Callable
    audit_score: Optional[int]
    contribution_score: Optional[int]
    
    @property
    def is_graduated(self) -> bool:
        """Check if function meets graduation criteria."""
        if self.audit_score is None or self.contribution_score is None:
            return False
        return (self.audit_score >= AUDIT_THRESHOLD and 
                self.contribution_score >= CONTRIBUTION_THRESHOLD)


# The catalog is populated as functions are imported
FUNCTION_CATALOG: Dict[str, FunctionEntry] = {}


def register_function(
    func: Callable,
    group: str,
    equation: str,
    description: str,
    source_file: str
) -> Callable:
    """
    Register a function in the catalog.
    
    Only functions that meet graduation criteria will be accessible.
    Scores are read from the function's @Fn decorator metadata.
    """
    # Get scores from the function's metadata (set by @Fn decorator)
    audit_score = getattr(func, '_fn_audit_score', None)
    contribution_score = getattr(func, '_fn_contribution_score', None)
    
    entry = FunctionEntry(
        name=func.__name__,
        group=group,
        equation=equation,
        description=description,
        source_file=source_file,
        function=func,
        audit_score=audit_score,
        contribution_score=contribution_score,
    )
    
    # Only add to catalog if graduated
    if entry.is_graduated:
        FUNCTION_CATALOG[func.__name__] = entry
    else:
        # Log warning about non-graduated function
        status = []
        if audit_score is None:
            status.append("audit_score: None")
        elif audit_score < AUDIT_THRESHOLD:
            status.append(f"audit_score: {audit_score} < {AUDIT_THRESHOLD}")
        if contribution_score is None:
            status.append("contribution_score: None")
        elif contribution_score < CONTRIBUTION_THRESHOLD:
            status.append(f"contribution_score: {contribution_score} < {CONTRIBUTION_THRESHOLD}")
        
        import warnings
        warnings.warn(
            f"Function '{func.__name__}' not graduated to central registry. "
            f"Status: {', '.join(status)}. "
            f"Function remains available at source location.",
            UserWarning
        )
    
    return func


# =============================================================================
# GROUP 1: STELLAR MECHANICS
# =============================================================================
# Functions related to stellar physics, nuclear binding, power output

# Import the actual function from its source
from gravity_field_model.examples.example_power_output import fn_get_power_output_per_field

# Register with metadata (scores are read from @Fn decorator)
register_function(
    fn_get_power_output_per_field,
    group="stellar_mechanics",
    equation="P(A) = BE(A) * (c / lambda_C)",
    description="Power output per gravity field from binding energy. Peaks at Fe-56.",
    source_file="examples/example_power_output.py",
)


# =============================================================================
# GROUP 2: ATOMIC PHYSICS
# =============================================================================
# Functions related to atomic structure, radii, valence

# Import the actual function from its source
from gravity_field_model.calculations.stellar_mechanics.test_valence_predictions import (
    fn_get_element_field_radius
)

# Register with metadata (scores are read from @Fn decorator)
register_function(
    fn_get_element_field_radius,
    group="atomic_physics",
    equation="r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [1 - (k/pi^2)*mu(Z/56)]",
    description="Empirical atomic radius prediction (fitted formula, ~13% accuracy).",
    source_file="calculations/stellar_mechanics/test_valence_predictions.py",
)


# =============================================================================
# GROUP 3: BLACK HOLES (placeholder for future functions)
# =============================================================================
# Functions related to black hole physics, horizons, Hawking radiation

# Example of what will be added (once graduated):
# from gravity_field_model.calculations.black_holes.test_black_hole_mechanics import (
#     fn_get_isco_radius,
#     fn_calc_hawking_temperature,
# )


# =============================================================================
# GROUP 4: GRAVITATIONAL WAVES (placeholder for future functions)
# =============================================================================
# Functions related to GW physics, chirp mass, strain

# Example of what will be added (once graduated):
# from gravity_field_model.calculations.field_theory.test_gw_geometric_coefficients import (
#     fn_calc_chirp_mass,
#     fn_calc_gw_frequency,
# )


# =============================================================================
# GROUP 5: FIELD CLOSURE (placeholder for future functions)
# =============================================================================
# Functions related to pi encoding, closure cycles, field origin

# Example of what will be added (once graduated):
# from gravity_field_model.engine_core.field_closure.test_closure_cycle import (
#     fn_calc_closure_steps,
#     fn_get_pi_digit_at_position,
# )


# =============================================================================
# GROUP NAMESPACE CLASSES
# =============================================================================
# These allow: from gravity_field_model.functions import stellar_mechanics
# Then: stellar_mechanics.fn_get_power_output_per_field(56)

class StellarMechanicsNamespace:
    """Namespace for stellar mechanics functions (graduated only)."""
    fn_get_power_output_per_field = fn_get_power_output_per_field
    
    @staticmethod
    def list_functions() -> List[str]:
        """List all graduated functions in this group."""
        return [name for name, entry in FUNCTION_CATALOG.items() 
                if entry.group == "stellar_mechanics"]


class AtomicPhysicsNamespace:
    """Namespace for atomic physics functions (graduated only)."""
    fn_get_element_field_radius = fn_get_element_field_radius
    
    @staticmethod
    def list_functions() -> List[str]:
        """List all graduated functions in this group."""
        return [name for name, entry in FUNCTION_CATALOG.items() 
                if entry.group == "atomic_physics"]


# Create namespace instances
stellar_mechanics = StellarMechanicsNamespace()
atomic_physics = AtomicPhysicsNamespace()


# =============================================================================
# DISCOVERY UTILITIES
# =============================================================================

def list_all_functions(show_scores: bool = True) -> None:
    """Print all GRADUATED functions grouped by domain."""
    print("\n" + "=" * 78)
    print("GRAVITY FIELD MODEL - FUNCTION REGISTRY (GRADUATED FUNCTIONS ONLY)")
    print("=" * 78)
    print(f"\nGraduation Criteria: audit_score >= {AUDIT_THRESHOLD}, "
          f"contribution_score >= {CONTRIBUTION_THRESHOLD}")
    
    # Group by domain
    groups: Dict[str, List[FunctionEntry]] = {}
    for entry in FUNCTION_CATALOG.values():
        if entry.group not in groups:
            groups[entry.group] = []
        groups[entry.group].append(entry)
    
    for group_name, entries in sorted(groups.items()):
        print(f"\n### {group_name.upper().replace('_', ' ')} ###\n")
        for entry in sorted(entries, key=lambda e: e.name):
            print(f"  {entry.name}")
            print(f"    Equation: {entry.equation}")
            print(f"    Purpose:  {entry.description}")
            print(f"    Source:   {entry.source_file}")
            if show_scores:
                print(f"    Scores:   audit={entry.audit_score}, "
                      f"contribution={entry.contribution_score} [GRADUATED]")
            print()
    
    print("=" * 78)
    print(f"Total graduated functions: {len(FUNCTION_CATALOG)}")
    print("=" * 78 + "\n")


def list_functions_by_group(group: str) -> List[str]:
    """Get list of graduated function names in a specific group."""
    return [name for name, entry in FUNCTION_CATALOG.items() 
            if entry.group == group]


def get_function_info(name: str) -> Optional[FunctionEntry]:
    """Get metadata for a specific graduated function."""
    return FUNCTION_CATALOG.get(name)


def get_all_groups() -> List[str]:
    """Get list of all function groups with graduated functions."""
    return list(set(entry.group for entry in FUNCTION_CATALOG.values()))


def check_graduation(func: Callable) -> Dict[str, Any]:
    """
    Check if a function meets graduation criteria.
    
    This is the SINGLE SOURCE OF TRUTH for function graduation.
    Other modules (START_RESEARCH_MODULE, SCIENTIFIC_REASONING_MODULE)
    should call this function to assess function graduation status.
    
    Usage in pipelines:
        from gravity_field_model.functions import check_graduation
        
        result = check_graduation(my_function)
        if result['graduated']:
            # Add to central registry
        else:
            print(f"Not graduated: {result['issues']}")
    
    Returns dict with graduation status and details.
    """
    audit = getattr(func, '_fn_audit_score', None)
    contrib = getattr(func, '_fn_contribution_score', None)
    
    result = {
        'name': func.__name__,
        'audit_score': audit,
        'contribution_score': contrib,
        'audit_threshold': AUDIT_THRESHOLD,
        'contribution_threshold': CONTRIBUTION_THRESHOLD,
        'audit_passed': audit is not None and audit >= AUDIT_THRESHOLD,
        'contribution_passed': contrib is not None and contrib >= CONTRIBUTION_THRESHOLD,
        'graduated': False,
        'issues': [],
        'recommendation': '',
    }
    
    if audit is None:
        result['issues'].append("audit_score not set")
    elif audit < AUDIT_THRESHOLD:
        result['issues'].append(f"audit_score {audit} < {AUDIT_THRESHOLD}")
    
    if contrib is None:
        result['issues'].append("contribution_score not set")
    elif contrib < CONTRIBUTION_THRESHOLD:
        result['issues'].append(f"contribution_score {contrib} < {CONTRIBUTION_THRESHOLD}")
    
    result['graduated'] = result['audit_passed'] and result['contribution_passed']
    
    # Provide recommendation
    if result['graduated']:
        result['recommendation'] = "GRADUATED: Add to central registry"
    elif audit is None or contrib is None:
        result['recommendation'] = "PENDING: Add scores to @Fn decorator"
    elif not result['audit_passed']:
        result['recommendation'] = "IMPROVE QUALITY: Better docs, validation, or constants"
    elif not result['contribution_passed']:
        if contrib >= 50:
            result['recommendation'] = "CLOSE: Increase value (currently 'Valuable', need 'Significant')"
        else:
            result['recommendation'] = "RECONSIDER: Low contribution value, may not be worth graduating"
    
    return result


def assess_function_for_graduation(func: Callable, verbose: bool = True) -> bool:
    """
    Assess a function for graduation and optionally print details.
    
    This is the pipeline-friendly API for checking graduation.
    
    Usage in START_RESEARCH_MODULE or SCIENTIFIC_REASONING_MODULE pipelines:
        from gravity_field_model.functions import assess_function_for_graduation
        
        if assess_function_for_graduation(my_function):
            # Proceed to add to registry
        else:
            # Keep in sandbox / source file
    
    Args:
        func: The @Fn decorated function to assess
        verbose: If True, print assessment details
    
    Returns:
        True if function meets graduation criteria, False otherwise
    """
    result = check_graduation(func)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"FUNCTION GRADUATION ASSESSMENT: {result['name']}")
        print(f"{'='*60}")
        print(f"  audit_score:        {result['audit_score']} (threshold: {AUDIT_THRESHOLD})")
        print(f"  contribution_score: {result['contribution_score']} (threshold: {CONTRIBUTION_THRESHOLD})")
        print(f"  audit_passed:       {result['audit_passed']}")
        print(f"  contribution_passed: {result['contribution_passed']}")
        print(f"  {'='*56}")
        if result['graduated']:
            print(f"  STATUS: GRADUATED - Ready for central registry")
        else:
            print(f"  STATUS: NOT GRADUATED")
            print(f"  Issues: {', '.join(result['issues'])}")
            print(f"  Recommendation: {result['recommendation']}")
        print(f"{'='*60}\n")
    
    return result['graduated']


# =============================================================================
# QUICK REFERENCE (printed when module is run directly)
# =============================================================================

QUICK_REFERENCE = """
================================================================================
FUNCTION REGISTRY - GRADUATED FUNCTIONS ONLY
================================================================================

Graduation Criteria:
  - audit_score >= 65 (quality threshold)
  - contribution_score >= 70 (must be "Significant" or higher)

Only functions meeting BOTH criteria are available in this registry.
Functions without scores or below threshold remain in their source files.

--------------------------------------------------------------------------------
STELLAR MECHANICS:
  fn_get_power_output_per_field(mass_number: int) -> float
    # P(A) = BE(A) * (c / lambda_C)
    # Power output per gravity field from binding energy. Peaks at Fe-56.
    # Scores: audit=82, contribution=75 [GRADUATED]

ATOMIC PHYSICS:
  fn_get_element_field_radius(symbol: str) -> float
    # r = (84/137) * a_bohr * n^2 * sqrt(A) / Z * [1 - (k/pi^2)*mu(Z/56)]
    # Empirical atomic radius prediction (fitted formula, ~13% accuracy).
    # Scores: audit=78, contribution=71 [GRADUATED]

--------------------------------------------------------------------------------
USAGE:
  from gravity_field_model.functions import fn_get_power_output_per_field
  power = fn_get_power_output_per_field(56)  # Fe-56
  
  # In tests:
  from gravity_field_model.framework import Depends
  from gravity_field_model.functions import fn_get_power_output_per_field
  
  class MyTest(Test):
      get_power = Depends(fn_get_power_output_per_field)

--------------------------------------------------------------------------------
DISCOVERY:
  from gravity_field_model.functions import list_all_functions
  list_all_functions()  # Print all graduated functions

  from gravity_field_model.functions import check_graduation
  check_graduation(my_function)  # Check if a function can graduate

================================================================================
"""


if __name__ == "__main__":
    print(QUICK_REFERENCE)
    list_all_functions()
