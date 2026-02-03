#!/usr/bin/env python3
"""
==============================================================================
DFP VALIDATION CONSOLE
==============================================================================

Enterprise-level command-line interface for running DFP validation tests.

Usage:
    python dfp_console.py              # Launch interactive console

Author: Physics Paper Validation Suite
"""

import os
import sys
import re
import time
import importlib
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# CONFIGURATION
# =============================================================================

VERSION = "2.0.0"
CONSOLE_WIDTH = 78

# Test categories using gfd_model_v2 tests
CATEGORIES = {
    # =========================================================================
    # ENGINE - Core GFD Model
    # =========================================================================
    "system_mechanics": {
        "name": "System Mechanics",
        "type": "ENGINE",
        "description": "Core field closure mechanics, pi traversal, binary encoding, spin derivation",
        "modules": [
            "gfd_model_v2.engine.system_mechanics.test_closure_cycle",
            "gfd_model_v2.engine.system_mechanics.test_bbp_validation",
            "gfd_model_v2.engine.system_mechanics.test_face_traversal",
            "gfd_model_v2.engine.system_mechanics.test_complementary_pairs",
            "gfd_model_v2.engine.system_mechanics.test_binary_triad",
            "gfd_model_v2.engine.system_mechanics.test_field_energy",
            "gfd_model_v2.engine.system_mechanics.test_settlement_frequency",
            "gfd_model_v2.engine.system_mechanics.test_orbit_statistics",
            "gfd_model_v2.engine.system_mechanics.test_spin_derivation",
            "gfd_model_v2.engine.system_mechanics.test_vertex_encoding",
            "gfd_model_v2.engine.system_mechanics.test_face_classification",
            "gfd_model_v2.engine.system_mechanics.test_tetrahedron_assignment",
            "gfd_model_v2.engine.system_mechanics.test_bbp_engine",
            "gfd_model_v2.engine.system_mechanics.test_information_content",
            "gfd_model_v2.engine.system_mechanics.test_port_ratio",
            "gfd_model_v2.engine.system_mechanics.test_pi_base8_traversal",
            "gfd_model_v2.engine.system_mechanics.test_mond_hexagonal",
            "gfd_model_v2.engine.system_mechanics.test_sixfold_symmetry",
            "gfd_model_v2.engine.system_mechanics.test_hubble_electron_mond",
            "gfd_model_v2.engine.system_mechanics.test_subspace_geometry",
            "gfd_model_v2.engine.system_mechanics.test_time_face_geometry",
            "gfd_model_v2.engine.system_mechanics.test_field_closure_runs",
            "gfd_model_v2.engine.system_mechanics.test_closure_cycle_triforce",
            "gfd_model_v2.engine.system_mechanics.test_enterprise_field_closure",
            "gfd_model_v2.engine.system_mechanics.test_parallel_face_traversal",
            "gfd_model_v2.engine.system_mechanics.test_pi_digits_full",
        ]
    },
    "timing_analysis": {
        "name": "Timing Analysis",
        "type": "ENGINE",
        "description": "Closure simultaneity, Compton-scale timing",
        "modules": [
            "gfd_model_v2.engine.timing_analysis.test_closure_simultaneity",
        ]
    },
    "theoretical_insights": {
        "name": "Theoretical Insights",
        "type": "ENGINE",
        "description": "Information theory, lattice fundamentals",
        "modules": [
            "gfd_model_v2.engine.theoretical_insights.test_information_theory",
            "gfd_model_v2.engine.theoretical_insights.test_lattice_fundamentals",
        ]
    },
    "information_flow": {
        "name": "Information Flow",
        "type": "ENGINE",
        "description": "Bit propagation, entropy in field closure",
        "modules": [
            "gfd_model_v2.engine.information_flow.test_bit_propagation",
        ]
    },
    "engine_stress_tests": {
        "name": "Engine Stress Tests",
        "type": "ENGINE",
        "description": "Determinism, ergodicity, boundary conditions, stability",
        "modules": [
            "gfd_model_v2.engine.engine_stress_tests.test_engine_stress",
        ]
    },
    # =========================================================================
    # CALCULATIONS - Predictions from the GFD Model
    # =========================================================================
    "stellar_mechanics": {
        "name": "Stellar Mechanics",
        "type": "CALC",
        "description": "Power output, elements, compression, valence predictions",
        "modules": [
            "gfd_model_v2.calculations.stellar_mechanics.test_power_output",
            "gfd_model_v2.calculations.stellar_mechanics.test_element_k_multiples",
            "gfd_model_v2.calculations.stellar_mechanics.test_molecular_formation",
            "gfd_model_v2.calculations.stellar_mechanics.test_periodic_field_counts",
            "gfd_model_v2.calculations.stellar_mechanics.test_core_compression",
            "gfd_model_v2.calculations.stellar_mechanics.test_subspace_packing",
            "gfd_model_v2.calculations.stellar_mechanics.test_field_origin_geometry",
            "gfd_model_v2.calculations.stellar_mechanics.test_unanswered_questions",
            "gfd_model_v2.calculations.stellar_mechanics.test_valence_predictions",
            "gfd_model_v2.calculations.stellar_mechanics.test_vortex_transit",
        ]
    },
    "particle_physics": {
        "name": "Particle Physics",
        "type": "CALC",
        "description": "Quark derivations, shell structure, particle properties, advanced SM",
        "modules": [
            "gfd_model_v2.calculations.particle_physics.test_quark_derivations",
            "gfd_model_v2.calculations.particle_physics.test_shell_structure",
            "gfd_model_v2.calculations.particle_physics.test_particle_properties",
            "gfd_model_v2.calculations.particle_physics.test_particle_advanced",
        ]
    },
    "historical_systems": {
        "name": "Historical Systems",
        "type": "CALC",
        "description": "Cross-cultural correspondences: I Ching, Gematria, Mitsuuroko, field origin geometry, stargate physics, advanced analysis",
        "modules": [
            "gfd_model_v2.calculations.historical_systems.test_historical_binary_system",
            "gfd_model_v2.calculations.historical_systems.test_hebrew_gematria_correspondence",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_field_origin_geometry",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_geometric_quantum_correspondence",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_quantum_foundations",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_stargate_physics",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_advanced_field_origin",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_kings_chamber",
            "gfd_model_v2.calculations.historical_systems.field_origin_geometry.test_pyramid_coupling",
            "gfd_model_v2.calculations.historical_systems.japanese_mitsuuroko.test_face_sampling_subdivision",
            "gfd_model_v2.calculations.historical_systems.japanese_mitsuuroko.test_japanese_mitsuuroko_correspondence",
        ]
    },
    "entanglement_mechanics": {
        "name": "Entanglement Mechanics",
        "type": "CALC",
        "description": "Quantum entanglement, subspace nonlinearity, advanced correlations",
        "modules": [
            "gfd_model_v2.calculations.entanglement_mechanics.test_entanglement",
            "gfd_model_v2.calculations.entanglement_mechanics.test_subspace_nonlinearity",
            "gfd_model_v2.calculations.entanglement_mechanics.test_entanglement_advanced",
        ]
    },
    "biological_mechanics": {
        "name": "Biological Mechanics",
        "type": "CALC",
        "description": "Iron in hemoglobin, k-alignment in living systems",
        "modules": [
            "gfd_model_v2.calculations.biological_mechanics.test_iron_hemoglobin",
        ]
    },
    "black_holes": {
        "name": "Black Holes",
        "type": "CALC",
        "description": "Event horizons, Hawking radiation, singularities",
        "modules": [
            "gfd_model_v2.calculations.black_holes.test_black_hole_mechanics",
        ]
    },
    "coupling_dynamics": {
        "name": "Coupling Dynamics",
        "type": "CALC",
        "description": "Tetrahedra coupling, interaction dynamics",
        "modules": [
            "gfd_model_v2.calculations.coupling_dynamics.test_tetrahedra_coupling",
        ]
    },
    "quantum_tunneling": {
        "name": "Quantum Tunneling",
        "type": "CALC",
        "description": "Barrier penetration, alpha decay",
        "modules": [
            "gfd_model_v2.calculations.quantum_tunneling.test_tunneling",
        ]
    },
    "symmetry_operations": {
        "name": "Symmetry Operations",
        "type": "CALC",
        "description": "Stellated octahedron symmetries, transformations",
        "modules": [
            "gfd_model_v2.calculations.symmetry_operations.test_stellated_octahedron_symmetries",
        ]
    },
    "cross_checks": {
        "name": "Cross Checks",
        "type": "CALC",
        "description": "Inter-module validation, consistency checks",
        "modules": [
            "gfd_model_v2.calculations.cross_checks.test_cross_checks",
        ]
    },
    "emergent_constants": {
        "name": "Emergent Constants",
        "type": "CALC",
        "description": "Fundamental parameters derived from geometry: α=1/137, m_p/m_e=1836, Bekenstein-Hawking, Tsirelson, π encoding, Flower of Life",
        "modules": [
            "gfd_model_v2.calculations.emergent_constants.test_emergent_constants",
            "gfd_model_v2.calculations.emergent_constants.test_emergent_constants_extended",
        ]
    },
}


# =============================================================================
# DISPLAY UTILITIES
# =============================================================================

# ANSI color codes
class C:
    RESET = '\033[0m'
    DIM = '\033[38;5;245m'
    GREEN = '\033[38;5;46m'
    CYAN = '\033[38;5;51m'
    PURPLE = '\033[38;5;129m'
    YELLOW = '\033[38;5;226m'
    RED = '\033[38;5;196m'
    
    # Red to purple gradient (for test list)
    GRADIENT_RED_PURPLE = [
        '\033[38;5;196m',  # Red
        '\033[38;5;197m',  # Red-pink
        '\033[38;5;198m',  # Pink
        '\033[38;5;199m',  # Pink-magenta
        '\033[38;5;200m',  # Magenta
        '\033[38;5;164m',  # Magenta-purple
        '\033[38;5;128m',  # Purple
        '\033[38;5;93m',   # Deep purple
    ]
    
    # Cyan to green gradient (for category menu)
    GRADIENT_CYAN_GREEN = [
        '\033[38;5;51m',   # Cyan
        '\033[38;5;50m',   # Cyan-teal
        '\033[38;5;49m',   # Teal
        '\033[38;5;48m',   # Teal-green
        '\033[38;5;47m',   # Green-teal
        '\033[38;5;46m',   # Green
        '\033[38;5;82m',   # Light green
        '\033[38;5;118m',  # Yellow-green
    ]
    
    # Diagonal gradient for ASCII logo (smooth purple to green gradient)
    # Using many more colors for smooth transition like the reference
    GRADIENT_LOGO = [
        # Purple shades
        '\033[38;5;129m', '\033[38;5;129m', '\033[38;5;128m', '\033[38;5;128m',
        '\033[38;5;127m', '\033[38;5;127m', '\033[38;5;126m', '\033[38;5;126m',
        # Purple to blue transition
        '\033[38;5;91m', '\033[38;5;91m', '\033[38;5;90m', '\033[38;5;90m',
        '\033[38;5;55m', '\033[38;5;55m', '\033[38;5;54m', '\033[38;5;54m',
        # Blue to cyan transition
        '\033[38;5;33m', '\033[38;5;33m', '\033[38;5;39m', '\033[38;5;39m',
        '\033[38;5;38m', '\033[38;5;38m', '\033[38;5;44m', '\033[38;5;44m',
        # Cyan to teal transition
        '\033[38;5;43m', '\033[38;5;43m', '\033[38;5;49m', '\033[38;5;49m',
        '\033[38;5;48m', '\033[38;5;48m', '\033[38;5;42m', '\033[38;5;42m',
        # Teal to green transition
        '\033[38;5;41m', '\033[38;5;41m', '\033[38;5;47m', '\033[38;5;47m',
        '\033[38;5;46m', '\033[38;5;46m', '\033[38;5;82m', '\033[38;5;82m',
        # Light green
        '\033[38;5;118m', '\033[38;5;118m', '\033[38;5;154m', '\033[38;5;154m',
    ]
    
    # Menu colors to match the purple-green logo gradient
    MENU_TITLE = '\033[38;5;129m'   # Purple
    MENU_LABEL = '\033[38;5;49m'    # Teal
    MENU_VALUE = '\033[38;5;48m'    # Teal-green
    MENU_ITEM = '\033[38;5;46m'     # Green


# ASCII art for DFP logo (circle pattern matching parrot style - all s interior)
DFP_LOGO = [
    "           .-/+oossssoo+/-.",
    "       `:+ssssssssssssssssss+:`",
    "     -+ssssssssssssssssssyyssss+-",
    "   .osssssssssssssssssssssssssssso.",
    "  /sssssssssssssssssssssssssssssssss/",
    " +sssssssssssssssssssssssssssssssssss+",
    "/sssssssssssssssssssssssssssssssssssss/",
    ".ssssssssssssssssssssssssssssssssssssss.",
    "+ssssssssssssssssssssssssssssssssssssss+",
    "osssssssssssssssssssssssssssssssssssssso",
    "osssssssssssssssssssssssssssssssssssssso",
    "+ssssssssssssssssssssssssssssssssssssss+",
    ".ssssssssssssssssssssssssssssssssssssss.",
    "/sssssssssssssssssssssssssssssssssssss/",
    " +sssssssssssssssssssssssssssssssssss+",
    "  /sssssssssssssssssssssssssssssssss/",
    "   .osssssssssssssssssssssssssssso.",
    "     -+ssssssssssssssssssyyssss+-",
    "       `:+ssssssssssssssssss+:`",
    "           .-/+oossssoo+/-.",
]


def _gradient_title(text, colors):
    """Apply gradient coloring to text."""
    if not text:
        return text
    result = []
    for i, char in enumerate(text):
        color_idx = int(i * len(colors) / len(text))
        color_idx = min(color_idx, len(colors) - 1)
        result.append(f"{colors[color_idx]}{char}")
    return ''.join(result) + C.RESET


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def _color_logo_line(line, color):
    """Apply a single color to a logo line."""
    return f"{color}{line}{C.RESET}"


def _interpolate_color(t, start_rgb, end_rgb):
    """Interpolate between two RGB colors. t is 0-1."""
    r = int(start_rgb[0] + t * (end_rgb[0] - start_rgb[0]))
    g = int(start_rgb[1] + t * (end_rgb[1] - start_rgb[1]))
    b = int(start_rgb[2] + t * (end_rgb[2] - start_rgb[2]))
    return (r, g, b)


def _get_gradient_color(t):
    """Get RGB color for position t (0-1) in purple-to-green gradient."""
    # Define color stops with smoother purple-to-blue transition
    stops = [
        (0.0,   (180, 80, 220)),   # Bright purple
        (0.08,  (160, 70, 220)),   # Purple
        (0.16,  (140, 60, 220)),   # Purple-violet
        (0.24,  (110, 50, 210)),   # Violet
        (0.32,  (80, 50, 200)),    # Blue-violet
        (0.40,  (50, 80, 200)),    # Blue
        (0.50,  (50, 130, 200)),   # Cyan-blue
        (0.60,  (50, 170, 190)),   # Cyan
        (0.70,  (50, 195, 165)),   # Teal
        (0.80,  (50, 210, 130)),   # Teal-green
        (0.90,  (50, 218, 100)),   # Green-teal
        (1.0,   (50, 220, 80)),    # Green
    ]
    
    # Find which segment we're in
    for i in range(len(stops) - 1):
        if t <= stops[i + 1][0]:
            # Interpolate within this segment
            seg_start = stops[i][0]
            seg_end = stops[i + 1][0]
            seg_t = (t - seg_start) / (seg_end - seg_start) if seg_end > seg_start else 0
            return _interpolate_color(seg_t, stops[i][1], stops[i + 1][1])
    
    return stops[-1][1]


def _rgb_to_ansi(rgb):
    """Convert RGB tuple to true color ANSI escape code."""
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def _diagonal_gradient_line(line, row, total_rows, total_cols, colors):
    """Apply smooth diagonal gradient using true color (24-bit RGB)."""
    result = []
    max_diag = total_rows + total_cols - 2  # Max diagonal distance
    
    for col, char in enumerate(line):
        if char == ' ':
            result.append(char)
        else:
            # Diagonal position: row + col determines color
            diag_pos = row + col
            t = diag_pos / max_diag if max_diag > 0 else 0
            t = max(0, min(1, t))  # Clamp to 0-1
            
            # Get true color RGB
            rgb = _get_gradient_color(t)
            color_code = _rgb_to_ansi(rgb)
            result.append(f"{color_code}{char}{C.RESET}")
    return ''.join(result)


def _gradient_text(text):
    """Apply purple-to-cyan gradient to text (like STELLAR POWER OUTPUT)."""
    if not text:
        return text
    result = []
    for i, char in enumerate(text):
        t = i / (len(text) - 1) if len(text) > 1 else 0
        # Purple (148, 80, 220) to Cyan (50, 200, 220)
        r = int(148 + t * (50 - 148))
        g = int(80 + t * (200 - 80))
        b = int(220 + t * (220 - 220))
        result.append(f"\033[38;2;{r};{g};{b}m{char}")
    return ''.join(result) + C.RESET


def print_splash():
    """Print the splash screen with ASCII art logo on left, branding on right."""
    print()
    
    # Fixed width for logo column (max logo line length)
    logo_width = max(len(line) for line in DFP_LOGO)
    total_rows = len(DFP_LOGO)
    
    # Gradient title
    title = _gradient_text("GRAVITY FIELD DYNAMICS MODEL v2")
    
    # Branding items to display on the right side (centered vertically)
    branding_lines = [
        "",
        "",
        "",
        "",
        "",
        f"{C.DIM}Distributed Field Processing (DFP){C.RESET}",
        title,
        f"{C.DIM}MIT License{C.RESET}",
        "",
        f"{C.MENU_LABEL}Version:{C.RESET}  {C.MENU_VALUE}{VERSION}{C.RESET}",
        f"{C.MENU_LABEL}Date:{C.RESET}     {C.MENU_VALUE}{datetime.now().strftime('%Y-%m-%d')}{C.RESET}",
        f"{C.MENU_LABEL}Time:{C.RESET}     {C.MENU_VALUE}{datetime.now().strftime('%H:%M:%S')}{C.RESET}",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]
    
    # Print logo with diagonal gradient on left + branding on right
    gradient = C.GRADIENT_LOGO
    for i, logo_line in enumerate(DFP_LOGO):
        # Apply diagonal gradient (top-left to bottom-right)
        colored_logo = _diagonal_gradient_line(logo_line, i, total_rows, logo_width, gradient)
        
        # Pad logo to fixed width
        padding = " " * (logo_width - len(logo_line))
        
        # Branding line (if available)
        branding_line = branding_lines[i] if i < len(branding_lines) else ""
        
        # Print side by side: logo on left, branding on right
        print(f"  {colored_logo}{padding}    {branding_line}")
    
    print()


def print_banner():
    """Print the menu banner without ASCII art logo."""
    print()
    
    # Gradient title
    title = _gradient_text("GRAVITY FIELD DYNAMICS MODEL v2")
    
    # Print branding header
    print(f"  {C.DIM}Distributed Field Processing (DFP){C.RESET}")
    print(f"  {title}")
    print(f"  {C.DIM}MIT License{C.RESET}")
    print()
    
    # Academic description
    desc_lines = [
        "A geometric model of gravitational field closure based on dual tetrahedra",
        "(stellated octahedron). The model derives from four independent textbook",
        "results: ADM constraint structure, tetrad formalism, loop quantum gravity,",
        "and bimetric theory, all converging on k=4 coupling topology.",
        "",
        "Field closure dynamics are encoded by pi digits in base-8, driving traversal",
        "through 8 vertices and 8 faces. The structure yields spin-1/2 from topology:",
        "(2 TIME faces / 8 total) x 2h = h/2. These tests validate the model's",
        "geometric predictions against physical constants and observations.",
    ]
    
    for line in desc_lines:
        print(f"  {C.DIM}{line}{C.RESET}")
    
    print()


def print_separator(char="-"):
    """Print a separator line."""
    print("  " + C.DIM + char * (CONSOLE_WIDTH - 4) + C.RESET)


def print_menu_item(key, description, indent=2):
    """Print a menu item."""
    print(f"{' ' * indent}[{key}] {description}")


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_module(module_path):
    """Run a single test module and return success."""
    try:
        module = importlib.import_module(module_path)
        
        if hasattr(module, 'run_all_tests'):
            return module.run_all_tests()
        else:
            print(f"  [WARN] Module {module_path} has no run_all_tests() function")
            return False
            
    except Exception as e:
        print(f"  [ERROR] {module_path}: {e}")
        return False


def run_all_tests_quick(progress_callback=None):
    """Run all tests and return actual test counts (individual tests, not modules)."""
    import io
    from contextlib import redirect_stdout, redirect_stderr
    
    results_by_category = {}
    total_passed = 0
    total_failed = 0
    total_errors = 0
    
    cat_keys = list(CATEGORIES.keys())
    
    for idx, cat_key in enumerate(cat_keys):
        cat_info = CATEGORIES[cat_key]
        
        # Show progress
        if progress_callback:
            progress_callback(cat_info['name'], idx + 1, len(cat_keys))
        
        cat_passed = 0
        cat_failed = 0
        cat_errors = 0
        
        for module_path in cat_info['modules']:
            try:
                # Import the module
                module = importlib.import_module(module_path)
                
                # Get ALL_TESTS list if it exists
                if hasattr(module, 'ALL_TESTS'):
                    test_classes = module.ALL_TESTS
                    
                    # Run each test class individually
                    for test_class in test_classes:
                        try:
                            # Suppress output
                            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                                test = test_class()
                                result = test.run()
                            
                            if result.passed:
                                cat_passed += 1
                            else:
                                cat_failed += 1
                        except Exception:
                            cat_errors += 1
                else:
                    # Fallback: count module as 1 test
                    if hasattr(module, 'run_all_tests'):
                        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                            result = module.run_all_tests()
                        if result:
                            cat_passed += 1
                        else:
                            cat_failed += 1
                    else:
                        cat_errors += 1
                        
            except Exception:
                cat_errors += 1
        
        results_by_category[cat_key] = {
            'name': cat_info['name'],
            'type': cat_info['type'],
            'passed': cat_passed,
            'failed': cat_failed,
            'errors': cat_errors,
            'total': cat_passed + cat_failed + cat_errors
        }
        
        total_passed += cat_passed
        total_failed += cat_failed
        total_errors += cat_errors
    
    return {
        'by_category': results_by_category,
        'total_passed': total_passed,
        'total_failed': total_failed,
        'total_errors': total_errors,
        'total': total_passed + total_failed + total_errors
    }


def _print_category_line(cat_data):
    """Print a single category result line."""
    cat_total = cat_data['total']
    cat_passed = cat_data['passed']
    cat_failed = cat_data['failed']
    
    # Status indicator
    if cat_failed == 0 and cat_passed > 0:
        status = f"{C.GREEN}PASS{C.RESET}"
        count_color = C.GREEN
    elif cat_passed == 0 and cat_total > 0:
        status = f"{C.RED}FAIL{C.RESET}"
        count_color = C.RED
    elif cat_total == 0:
        status = f"{C.DIM}----{C.RESET}"
        count_color = C.DIM
    else:
        status = f"{C.YELLOW}PART{C.RESET}"
        count_color = C.YELLOW
    
    # Format: [PASS] Category Name                    12/12
    name = cat_data['name']
    
    # Build the line
    prefix = f"    [{status}] {name}"
    suffix = f"{count_color}{cat_passed}/{cat_total}{C.RESET}"
    
    # Calculate padding (account for ANSI codes in prefix)
    visible_prefix = f"    [PASS] {name}"  # Length without ANSI
    padding = 56 - len(visible_prefix)
    
    print(f"{prefix}{' ' * padding}{suffix}")


def display_quick_test_results(results):
    """Display the quick test results with nice formatting, grouped by type."""
    print()
    
    # Title with gradient
    title = _gradient_title("ALL TESTS SUMMARY", C.GRADIENT_CYAN_GREEN)
    print(f"  {title}")
    print_separator()
    
    # Separate results by type
    engine_results = {k: v for k, v in results['by_category'].items() if v['type'] == 'ENGINE'}
    calc_results = {k: v for k, v in results['by_category'].items() if v['type'] == 'CALC'}
    
    # Calculate totals per section
    engine_passed = sum(v['passed'] for v in engine_results.values())
    engine_total = sum(v['total'] for v in engine_results.values())
    calc_passed = sum(v['passed'] for v in calc_results.values())
    calc_total = sum(v['total'] for v in calc_results.values())
    
    # ENGINE section
    print()
    engine_title = _gradient_text("GFD ENGINE")
    engine_count = f"{C.GREEN}{engine_passed}/{engine_total}{C.RESET}" if engine_passed == engine_total else f"{C.YELLOW}{engine_passed}/{engine_total}{C.RESET}"
    print(f"  {engine_title}  {C.DIM}Core field mechanics, traversal, timing{C.RESET}")
    print()
    
    for cat_key, cat_data in engine_results.items():
        _print_category_line(cat_data)
    
    # CALCULATIONS section
    print()
    calc_title = _gradient_text("GFD CALCULATIONS")
    calc_count = f"{C.GREEN}{calc_passed}/{calc_total}{C.RESET}" if calc_passed == calc_total else f"{C.YELLOW}{calc_passed}/{calc_total}{C.RESET}"
    print(f"  {calc_title}  {C.DIM}Predictions from the model{C.RESET}")
    print()
    
    for cat_key, cat_data in calc_results.items():
        _print_category_line(cat_data)
    
    print()
    print_separator("=")
    
    # Total summary
    total = results['total']
    passed = results['total_passed']
    failed = results['total_failed']
    
    if failed == 0:
        result_text = f"{C.GREEN}{passed}/{total} tests passed{C.RESET}"
    else:
        result_text = f"{C.YELLOW}{passed}/{total} passed{C.RESET}, {C.RED}{failed} failed{C.RESET}"
    
    print(f"  {result_text}")
    print_separator("=")


def run_category(category_key):
    """Run all tests in a category."""
    if category_key not in CATEGORIES:
        print(f"  [ERROR] Unknown category: {category_key}")
        return 0, 0
    
    category = CATEGORIES[category_key]
    passed = 0
    total = len(category['modules'])
    
    for module_path in category['modules']:
        if run_module(module_path):
            passed += 1
    
    return passed, total


def run_single_test(category_key, module_path):
    """Run a single test with category context."""
    if category_key not in CATEGORIES:
        print(f"  [ERROR] Unknown category: {category_key}")
        return False
    
    category = CATEGORIES[category_key]
    
    # Show context
    print(f"  Category: {category['name']} [{category['type']}]")
    print(f"  {category['description']}")
    print()
    print_separator()
    print("  (Running individual test from this group)")
    print_separator()
    print()
    
    return run_module(module_path)


# =============================================================================
# INTERACTIVE MENU
# =============================================================================

def show_main_menu():
    """Display the main menu options."""
    menu_1 = _gradient_text("[1] View Model Predictions")
    menu_2 = _gradient_text("[2] Run All Validation Tests")
    menu_3 = _gradient_text("[3] GFD Foundations (Why This Structure)")
    menu_4 = _gradient_text("[4] GFD Definitions")
    menu_5 = _gradient_text("[5] GFD Concepts (How Things Work)")
    menu_q = _gradient_text("[q] Quit")
    
    print(f"  {menu_1}")
    print(f"  {menu_2}")
    print(f"  {menu_3}")
    print(f"  {menu_4}")
    print(f"  {menu_5}")
    print(f"  {menu_q}")
    print()


def _count_tests_in_module(module_path):
    """Count actual GFDTest classes in a module."""
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, 'ALL_TESTS'):
            return len(module.ALL_TESTS)
        return 1  # Fallback: count module as 1 test
    except Exception:
        return 0


def _count_tests_in_category(cat_info):
    """Count total tests in a category (all modules)."""
    total = 0
    for module_path in cat_info['modules']:
        total += _count_tests_in_module(module_path)
    return total


def show_category_menu():
    """Display the category selection menu."""
    # Gradient title (cyan to green)
    print()
    print(f"  {_gradient_title('SELECT TEST CATEGORY', C.GRADIENT_CYAN_GREEN)}")
    print_separator()
    
    # Group by type
    engine_cats = [(k, v) for k, v in CATEGORIES.items() if v['type'] == 'ENGINE']
    calc_cats = [(k, v) for k, v in CATEGORIES.items() if v['type'] == 'CALC']
    
    # ENGINE section with gradient title (same style as Run All Tests)
    print()
    engine_title = _gradient_text("GFD ENGINE")
    print(f"  {engine_title}  {C.DIM}Core field mechanics, traversal, timing{C.RESET}")
    print()
    
    idx = 1
    cat_keys = []
    for key, cat in engine_cats:
        test_count = _count_tests_in_category(cat)
        print(f"    [{idx:2d}] {cat['name']:<25s} {C.DIM}({test_count} tests){C.RESET}")
        cat_keys.append(key)
        idx += 1
    
    # CALCULATIONS section with gradient title (same style as Run All Tests)
    print()
    calc_title = _gradient_text("GFD CALCULATIONS")
    print(f"  {calc_title}  {C.DIM}Predictions from the model{C.RESET}")
    print()
    
    for key, cat in calc_cats:
        test_count = _count_tests_in_category(cat)
        print(f"    [{idx:2d}] {cat['name']:<25s} {C.DIM}({test_count} tests){C.RESET}")
        cat_keys.append(key)
        idx += 1
    
    print()
    print_separator()
    total_tests = sum(_count_tests_in_category(c) for c in CATEGORIES.values())
    print(f"  {C.DIM}Total: {len(CATEGORIES)} categories, {total_tests} tests{C.RESET}")
    print()
    print_menu_item("b", "Back to main menu")
    print()
    
    return cat_keys


# =============================================================================
# DEFINITIONS DISPLAY
# =============================================================================

# Purple gradient for definition titles
GRADIENT_PURPLE = [
    '\033[38;5;129m',  # Purple
    '\033[38;5;128m',  # Purple
    '\033[38;5;127m',  # Purple-violet
    '\033[38;5;126m',  # Violet
    '\033[38;5;91m',   # Blue-violet
    '\033[38;5;90m',   # Blue-violet
    '\033[38;5;55m',   # Deep purple
    '\033[38;5;54m',   # Deep purple
]


def _purple_gradient_text(text):
    """Apply purple gradient to text for definition titles."""
    if not text:
        return text
    result = []
    for i, char in enumerate(text):
        t = i / (len(text) - 1) if len(text) > 1 else 0
        # Purple gradient: (180, 80, 220) -> (100, 50, 180)
        r = int(180 - t * 80)
        g = int(80 - t * 30)
        b = int(220 - t * 40)
        result.append(f"\033[38;2;{r};{g};{b}m{char}")
    return ''.join(result) + C.RESET


def show_definitions_menu():
    """Display the GFD Definitions reference."""
    try:
        from gfd_model_v2.common.gfd_definitions import GFD_DEFINITIONS, get_all_categories
    except ImportError:
        print(f"  {C.RED}Error: Could not load GFD definitions module.{C.RESET}")
        print(f"  {C.DIM}Make sure gfd_model_v2/common/gfd_definitions.py exists.{C.RESET}")
        input("\n  Press any key to return to menu...")
        return
    
    clear_screen()
    print()
    
    # Header
    header = _purple_gradient_text("GRAVITY FIELD DYNAMICS DEFINITIONS")
    print(f"  {header}")
    print(f"  {C.DIM}Reference guide for GFD model terminology{C.RESET}")
    print()
    print("  " + "-" * 70)
    print()
    
    # Get categories and sort them
    categories = get_all_categories()
    category_order = ['Foundation', 'Constants', 'Field Dynamics', 'Architecture', 'Principles', 'Stellar Forge']
    sorted_categories = [c for c in category_order if c in categories]
    # Add any remaining categories not in the order list
    for c in categories:
        if c not in sorted_categories:
            sorted_categories.append(c)
    
    # Display definitions grouped by category
    for category in sorted_categories:
        # Category header with purple gradient
        cat_title = _purple_gradient_text(f"  {category.upper()}")
        print(cat_title)
        print("  " + "-" * 70)
        print()
        
        # Get definitions in this category
        cat_defs = [d for d in GFD_DEFINITIONS if d['category'] == category]
        
        for defn in cat_defs:
            # Definition name with purple gradient
            name_text = _purple_gradient_text(defn['name'])
            print(f"  {name_text}")
            print("  " + "-" * 50)
            
            # Summary in dim
            print(f"  {C.DIM}{defn['summary']}{C.RESET}")
            print()
            
            # Explanation - wrap text nicely
            explanation = defn['explanation']
            # Word wrap at ~70 chars
            words = explanation.split()
            lines = []
            current_line = "  "
            for word in words:
                if len(current_line) + len(word) + 1 <= 72:
                    current_line += word + " "
                else:
                    lines.append(current_line.rstrip())
                    current_line = "  " + word + " "
            if current_line.strip():
                lines.append(current_line.rstrip())
            
            for line in lines:
                print(line)
            
            print()
            print()
        
        print()
    
    # Footer
    print("  " + "=" * 70)
    print(f"  {C.DIM}Total: {len(GFD_DEFINITIONS)} definitions across {len(sorted_categories)} categories{C.RESET}")
    print("  " + "=" * 70)
    print()
    
    # Wait for user input
    input("  Press Enter to return to menu...")


def show_foundations_menu():
    """Display the GFD Foundations (Chain of Logic) reference."""
    try:
        from gfd_model_v2.common.gfd_foundations import GFD_FOUNDATIONS, get_all_sections, get_foundations_by_section
    except ImportError:
        print(f"  {C.RED}Error: Could not load GFD foundations module.{C.RESET}")
        print(f"  {C.DIM}Make sure gfd_model_v2/common/gfd_foundations.py exists.{C.RESET}")
        input("\n  Press any key to return to menu...")
        return
    
    clear_screen()
    print()
    
    # Header
    header = _purple_gradient_text("GRAVITY FIELD DYNAMICS: FOUNDATIONS")
    print(f"  {header}")
    print(f"  {C.DIM}The chain of logic: WHY gravity must have this structure{C.RESET}")
    print()
    print("  " + "-" * 70)
    print()
    
    # Get sections in order
    sections = get_all_sections()
    
    # Display foundations grouped by section
    for section in sections:
        # Section header with purple gradient
        section_title = _purple_gradient_text(f"  {section.upper()}")
        print(section_title)
        print("  " + "-" * 70)
        print()
        
        # Get foundations in this section
        section_foundations = get_foundations_by_section(section)
        
        for foundation in section_foundations:
            # Foundation title with purple gradient and order number
            title_text = _purple_gradient_text(f"{foundation['order']}. {foundation['title']}")
            print(f"  {title_text}")
            print("  " + "-" * 50)
            
            # Content - wrap text nicely and handle newlines
            content = foundation['content']
            paragraphs = content.split('\n\n')
            
            for para in paragraphs:
                # Word wrap at ~70 chars
                words = para.replace('\n', ' ').split()
                lines = []
                current_line = "  "
                for word in words:
                    if len(current_line) + len(word) + 1 <= 72:
                        current_line += word + " "
                    else:
                        lines.append(current_line.rstrip())
                        current_line = "  " + word + " "
                if current_line.strip():
                    lines.append(current_line.rstrip())
                
                for line in lines:
                    print(line)
                print()  # Blank line between paragraphs
            
            print()
        
        print()
    
    # Footer
    print("  " + "=" * 70)
    print(f"  {C.DIM}Total: {len(GFD_FOUNDATIONS)} entries across {len(sections)} sections{C.RESET}")
    print("  " + "=" * 70)
    print()
    
    # Wait for user input
    input("  Press Enter to return to menu...")


def show_concepts_menu():
    """Display the GFD Concepts (How Things Work) reference."""
    try:
        from gfd_model_v2.common.gfd_concepts import GFD_CONCEPTS, get_all_concept_categories
    except ImportError:
        print(f"  {C.RED}Error: Could not load GFD concepts module.{C.RESET}")
        print(f"  {C.DIM}Make sure gfd_model_v2/common/gfd_concepts.py exists.{C.RESET}")
        input("\n  Press any key to return to menu...")
        return
    
    clear_screen()
    print()
    
    # Header
    header = _purple_gradient_text("GRAVITY FIELD DYNAMICS CONCEPTS")
    print(f"  {header}")
    print(f"  {C.DIM}How things work in the GFD model{C.RESET}")
    print()
    print("  " + "-" * 70)
    print()
    
    # Get categories in order
    categories = get_all_concept_categories()
    
    # Display concepts grouped by category
    for category in categories:
        # Category header with purple gradient
        cat_title = _purple_gradient_text(f"  {category.upper()}")
        print(cat_title)
        print("  " + "-" * 70)
        print()
        
        # Get concepts in this category
        cat_concepts = [c for c in GFD_CONCEPTS if c['category'] == category]
        
        for concept in cat_concepts:
            # Concept title with purple gradient
            title_text = _purple_gradient_text(concept['title'])
            print(f"  {title_text}")
            print("  " + "-" * 50)
            
            # Content - wrap text nicely and handle newlines
            content = concept['content']
            paragraphs = content.split('\n\n')
            
            for para in paragraphs:
                # Word wrap at ~70 chars
                words = para.replace('\n', ' ').split()
                lines = []
                current_line = "  "
                for word in words:
                    if len(current_line) + len(word) + 1 <= 72:
                        current_line += word + " "
                    else:
                        lines.append(current_line.rstrip())
                        current_line = "  " + word + " "
                if current_line.strip():
                    lines.append(current_line.rstrip())
                
                for line in lines:
                    print(line)
                print()  # Blank line between paragraphs
            
            print()
        
        print()
    
    # Footer
    print("  " + "=" * 70)
    print(f"  {C.DIM}Total: {len(GFD_CONCEPTS)} concepts across {len(categories)} sections{C.RESET}")
    print("  " + "=" * 70)
    print()
    
    # Wait for user input
    input("  Press Enter to return to menu...")


def show_test_list_menu(category_key):
    """Display the list of tests in a category."""
    category = CATEGORIES[category_key]
    
    # Gradient title (red to purple)
    title = f"{category['name'].upper()} [{category['type']}]"
    print()
    print(f"  {_gradient_title(title, C.GRADIENT_RED_PURPLE)}")
    print_separator()
    print()
    print(f"  {category['description']}")
    print()
    
    # List all test modules with their test counts
    total_tests = 0
    for idx, module_path in enumerate(category['modules'], 1):
        # Extract test name from module path
        test_name = module_path.split('.')[-1].replace('test_', '').replace('_', ' ').title()
        test_count = _count_tests_in_module(module_path)
        total_tests += test_count
        print(f"  [{idx:2d}] {test_name:<30s} {C.DIM}({test_count} tests){C.RESET}")
    
    print()
    print_separator()
    print(f"  {C.DIM}Total: {len(category['modules'])} modules, {total_tests} tests{C.RESET}")
    print()
    print_menu_item("a", "Run ALL tests in this category")
    print_menu_item("b", "Back to categories")
    print()
    print_separator()
    
    return category['modules']


def interactive_mode():
    """Run the interactive console."""
    # Show splash screen on first load
    clear_screen()
    print_splash()
    time.sleep(3)
    
    while True:
        clear_screen()
        print_banner()
        show_main_menu()
        
        prompt = _gradient_text("Enter choice:")
        choice = input(f"  {prompt} ").strip().lower()
        
        if choice == '1':
            # Run by category - LEVEL 2: Category selection
            while True:
                clear_screen()
                print_banner()
                cat_keys = show_category_menu()
                
                prompt = _gradient_text("Enter choice:")
                cat_choice = input(f"  {prompt} ").strip().lower()
                
                if cat_choice == 'b':
                    break
                else:
                    try:
                        idx = int(cat_choice) - 1
                        if 0 <= idx < len(cat_keys):
                            category_key = cat_keys[idx]
                            
                            # LEVEL 3: Test selection within category
                            while True:
                                clear_screen()
                                print_banner()
                                test_modules = show_test_list_menu(category_key)
                                
                                prompt = _gradient_text("Enter choice:")
                                test_choice = input(f"  {prompt} ").strip().lower()
                                
                                if test_choice == 'b':
                                    break
                                elif test_choice == 'a':
                                    # Run all tests in category
                                    clear_screen()
                                    print_banner()
                                    
                                    cat = CATEGORIES[category_key]
                                    print(f"  Running: {cat['name']} [{cat['type']}]")
                                    print(f"  {cat['description']}")
                                    print()
                                    
                                    passed, total = run_category(category_key)
                                    
                                    print()
                                    print_separator("=")
                                    if passed == total:
                                        print(f"  Result: {passed}/{total} tests passed")
                                    else:
                                        print(f"  Result: {passed}/{total} tests passed ({total - passed} failed)")
                                    print_separator("=")
                                    
                                    input("\n  Press Enter to continue...")
                                else:
                                    try:
                                        test_idx = int(test_choice) - 1
                                        if 0 <= test_idx < len(test_modules):
                                            # Run single test
                                            clear_screen()
                                            print_banner()
                                            
                                            module_path = test_modules[test_idx]
                                            success = run_single_test(category_key, module_path)
                                            
                                            print()
                                            print_separator("=")
                                            if success:
                                                print("  Result: PASSED")
                                            else:
                                                print("  Result: FAILED")
                                            print_separator("=")
                                            
                                            input("\n  Press Enter to continue...")
                                    except ValueError:
                                        pass
                    except ValueError:
                        pass
        
        elif choice == '3':
            # Show GFD Foundations (Chain of Logic)
            show_foundations_menu()
        
        elif choice == '4':
            # Show GFD Definitions
            show_definitions_menu()
        
        elif choice == '5':
            # Show GFD Concepts (How Things Work)
            show_concepts_menu()
        
        elif choice == '2':
            # Run all tests quickly
            clear_screen()
            print_banner()
            
            print()
            print(f"  {_gradient_title('RUNNING ALL TESTS', C.GRADIENT_CYAN_GREEN)}")
            print_separator()
            print()
            
            # Progress callback to show which category is running
            def show_progress(cat_name, current, total):
                # Clear line and print progress
                print(f"\r  {C.DIM}[{current}/{total}] Testing: {cat_name}...{C.RESET}".ljust(70), end='', flush=True)
            
            # Run tests with progress
            results = run_all_tests_quick(progress_callback=show_progress)
            
            # Clear progress line
            print("\r" + " " * 70 + "\r", end='')
            
            # Clear and show results
            clear_screen()
            print_banner()
            display_quick_test_results(results)
            
            input("\n  Press Enter to continue...")
                        
        elif choice == 'q':
            clear_screen()
            print("\n  Goodbye!\n")
            break


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    interactive_mode()
    return 0


if __name__ == "__main__":
    sys.exit(main())
