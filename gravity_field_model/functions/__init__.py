"""
Function Registry for Gravity Field Model
=========================================

This module provides a central registry of all @Fn decorated functions
available in the gravity field model. Functions are logically grouped
by domain and easily discoverable.

USAGE:
------
    # Import specific functions
    from gravity_field_model.functions import fn_get_power_output_per_field
    
    # Import all functions from a group
    from gravity_field_model.functions import stellar_mechanics
    
    # Get a list of all available functions
    from gravity_field_model.functions import list_all_functions
    
    # Use in tests via Depends
    from gravity_field_model.framework import Depends
    from gravity_field_model.functions import fn_get_power_output_per_field
    
    class MyTest(Test):
        get_power = Depends(fn_get_power_output_per_field)

WHY THIS EXISTS:
----------------
Functions defined with @Fn are powerful reusable building blocks.
Without a central registry, they are scattered across test files
and hard to discover. This registry:

1. Makes all functions discoverable in one place
2. Groups functions by physics domain
3. Provides quick reference to equations and purposes
4. Encourages reuse and building chains of calculations

ADDING NEW FUNCTIONS:
---------------------
1. Define your function with @Fn in the appropriate test/domain file
2. Import and register it in registry.py under the correct group
3. Re-export it from this __init__.py

See framework/SCIENTIFIC_REASONING_MODULE.md Part 9 for guidance
on when and how to extract functions from tests.
"""

# =============================================================================
# FUNCTION IMPORTS (graduated functions only)
# =============================================================================

from gravity_field_model.functions.registry import (
    # Stellar Mechanics (graduated)
    fn_get_power_output_per_field,
    
    # Atomic Physics (graduated)
    fn_get_element_field_radius,
    
    # Utility functions
    list_all_functions,
    list_functions_by_group,
    get_function_info,
    
    # Graduation API (for pipelines)
    check_graduation,
    assess_function_for_graduation,
    
    # Graduation thresholds
    AUDIT_THRESHOLD,
    CONTRIBUTION_THRESHOLD,
    
    # Group namespaces (for from functions import stellar_mechanics)
    stellar_mechanics,
    atomic_physics,
)

# =============================================================================
# ALL EXPORTS
# =============================================================================

__all__ = [
    # Stellar Mechanics (graduated)
    "fn_get_power_output_per_field",
    
    # Atomic Physics (graduated)
    "fn_get_element_field_radius",
    
    # Discovery utilities
    "list_all_functions",
    "list_functions_by_group",
    "get_function_info",
    
    # Graduation API (for pipelines)
    "check_graduation",
    "assess_function_for_graduation",
    
    # Thresholds
    "AUDIT_THRESHOLD",
    "CONTRIBUTION_THRESHOLD",
    
    # Group namespaces
    "stellar_mechanics",
    "atomic_physics",
]
