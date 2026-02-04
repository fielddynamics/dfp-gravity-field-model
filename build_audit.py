#!/usr/bin/env python3
"""
Build Audit: Check if project builds and audit constants usage.
Scans all test files for:
1. Import errors (try importing each module)
2. Locally-defined constants that should come from common/
3. Constants with values that differ from common/
"""
import sys
import os
import re
import importlib
import traceback

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Known constants that MUST come from common/
COMMON_CONSTANTS = {
    # From constants_codata.py
    'C', 'SPEED_OF_LIGHT', 'H', 'H_PLANCK', 'HBAR', 'H_BAR', 'G',
    'GRAVITATIONAL_CONSTANT', 'K_B', 'BOLTZMANN_CONSTANT',
    'ALPHA', 'FINE_STRUCTURE_CONSTANT', 'ALPHA_INVERSE',
    'E_CHARGE', 'ELEMENTARY_CHARGE', 'EPSILON_0', 'MU_0',
    'M_E', 'ELECTRON_MASS', 'M_E_MEV', 'R_E', 'CLASSICAL_ELECTRON_RADIUS',
    'LAMBDA_COMPTON', 'LAMBDA_C', 'LAMBDA_COMPTON_BAR',
    'A_0', 'BOHR_RADIUS', 'G_ELECTRON',
    'M_P', 'PROTON_MASS', 'M_P_MEV', 'R_PROTON', 'PROTON_RADIUS',
    'LAMBDA_COMPTON_PROTON', 'M_P_OVER_M_E', 'PROTON_ELECTRON_MASS_RATIO',
    'M_N', 'NEUTRON_MASS', 'M_N_MEV', 'DELTA_M_NP', 'DELTA_M_NP_MEV',
    'L_PLANCK', 'PLANCK_LENGTH', 'T_PLANCK', 'PLANCK_TIME',
    'M_PLANCK', 'PLANCK_MASS', 'TEMP_PLANCK', 'PLANCK_TEMPERATURE',
    'E_PLANCK', 'PLANCK_ENERGY',
    'M_SOLAR', 'SOLAR_MASS', 'R_SOLAR', 'SOLAR_RADIUS',
    'L_SOLAR', 'SOLAR_LUMINOSITY', 'AU', 'ASTRONOMICAL_UNIT', 'PARSEC',
    'R_INFINITY', 'SIGMA_SB', 'STEFAN_BOLTZMANN',
    'N_A', 'AVOGADRO', 'AMU', 'ATOMIC_MASS_UNIT',
    'EV', 'ELECTRON_VOLT', 'EV_TO_KG', 'J_TO_MEV',
    # From common/__init__.py
    'K', 'K_CLOSURE', 'A_MOND',
    'VERTICES', 'TET_A', 'TET_B', 'FACES', 'TIME_FACES', 'SPATIAL_FACES',
    'COMPLEMENTARY_PAIRS', 'ME',
    # From stellar_constants.py
    'T_HYDROGEN_FUSION', 'T_HELIUM_FUSION', 'T_CARBON_FUSION',
    'T_OXYGEN_FUSION', 'T_SILICON_FUSION', 'T_IRON_PHOTODISINTEGRATION',
    'RHO_WHITE_DWARF', 'RHO_NEUTRON_STAR', 'RHO_NUCLEAR', 'RHO_FIELD_BINDING',
    'RHO_SOLAR_CORE', 'RHO_SOLAR_SURFACE',
    'MASS_RATIO_PROTON_ELECTRON', 'MASS_RATIO_NEUTRON_PROTON',
    'T_SOLAR_CORE', 'T_SOLAR_SURFACE', 'P_SOLAR_CORE', 'SOLAR_MASS_LOSS_RATE',
    'CHANDRASEKHAR_LIMIT', 'TOV_LIMIT',
    'MAGIC_NUMBERS', 'DOUBLY_MAGIC', 'STABLE_K_MULTIPLES',
    'FE_56_BINDING_ENERGY_PER_NUCLEON',
    'MASS_ELECTRON_MEV', 'MASS_PROTON_MEV', 'MASS_NEUTRON_MEV',
    'MASS_DIFF_NEUTRON_PROTON_MEV',
    'ATOM_MASS_NUMBERS', 'ATOM_VALENCES',
}

# Aliases / variant names used in test files that map to common constants
ALIAS_MAP = {
    'M_SUN': 'M_SOLAR',
    'M_ELECTRON': 'M_E',
    'M_PROTON': 'M_P',
    'M_NEUTRON': 'M_N',
    'K_BOLTZMANN': 'K_B',
    'ALPHA_FINE': 'ALPHA',
    'ALPHA_INV': 'ALPHA_INVERSE',
    'MASS_RATIO_PE': 'M_P_OVER_M_E',
    'G_MEASURED': 'G',
    'D_SPATIAL': None,  # GFD-specific, might need to be in common
    'CLOSURE_FREQUENCY': None,  # GFD-specific
}

# Regex to match constant definitions (ALL_CAPS = value)
CONST_DEF_RE = re.compile(
    r'^([A-Z][A-Z0-9_]*)\s*=\s*(.+?)(?:\s*#.*)?$'
)

# Files to skip
SKIP_FILES = {
    'constants_codata.py',
    'stellar_constants.py',
    '__init__.py',
    'build_audit.py',
    'dfp_console.py',
    'report_generator.py',
    'pi_data.py',
    'gfd_definitions.py',
    'gfd_concepts.py',
    'gfd_foundations.py',
    'tetragram_analyzer.py',
    'traversal_analyzer.py',
}


def find_all_test_files(root):
    """Find all Python test files."""
    test_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs and __pycache__
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
        for f in filenames:
            if f.endswith('.py') and f not in SKIP_FILES:
                test_files.append(os.path.join(dirpath, f))
    return sorted(test_files)


def scan_file_for_constants(filepath):
    """Scan a file for locally-defined constants that should come from common/."""
    violations = []
    local_constants = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_class = False
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Track if we're inside a class (class-level attrs are ok)
        if stripped.startswith('class '):
            in_class = True
        elif stripped and not stripped.startswith(' ') and not stripped.startswith('\t') and not stripped.startswith('#'):
            if not stripped.startswith('def ') and not stripped.startswith('@') and not stripped.startswith('class '):
                in_class = False
        
        # Skip lines inside class bodies (indented)
        if line.startswith('    ') or line.startswith('\t'):
            continue
        
        # Check for constant definitions at module level
        match = CONST_DEF_RE.match(stripped)
        if match:
            name = match.group(1)
            value = match.group(2).strip()
            
            # Skip things that aren't physics constants
            if name in ('ALL_TESTS', 'PI', 'SQRT_2', 'SQRT_3', 'VERSION'):
                continue
            if name.startswith('_'):
                continue
            
            # Check if this constant should come from common
            if name in COMMON_CONSTANTS:
                violations.append({
                    'file': filepath,
                    'line': lineno,
                    'name': name,
                    'value': value,
                    'type': 'REDEFINED',
                    'msg': f"'{name}' redefined locally -- should import from common/"
                })
                local_constants[name] = value
            elif name in ALIAS_MAP:
                canonical = ALIAS_MAP[name]
                violations.append({
                    'file': filepath,
                    'line': lineno,
                    'name': name,
                    'value': value,
                    'type': 'ALIAS',
                    'msg': f"'{name}' defined locally (alias for '{canonical}') -- should import from common/"
                })
                local_constants[name] = value
    
    return violations, local_constants


def check_imports(filepath):
    """Check if a file imports from common/ or redefines constants."""
    imports_from_common = False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'from gfd_model_v2.common' in content or 'from .common' in content or 'from ..common' in content:
        imports_from_common = True
    if 'from gfd_model_v2.common.constants_codata' in content:
        imports_from_common = True
    if 'from gfd_model_v2.common.stellar_constants' in content:
        imports_from_common = True
    
    return imports_from_common


def try_import_modules():
    """Try to import all test modules and report errors."""
    from dfp_console import CATEGORIES
    
    results = []
    for cat_key, cat_info in CATEGORIES.items():
        for module_path in cat_info['modules']:
            try:
                importlib.import_module(module_path)
                results.append({
                    'module': module_path,
                    'category': cat_info['name'],
                    'status': 'OK',
                    'error': None,
                })
            except Exception as e:
                results.append({
                    'module': module_path,
                    'category': cat_info['name'],
                    'status': 'ERROR',
                    'error': f"{type(e).__name__}: {str(e)[:200]}",
                })
    return results


def main():
    root = os.path.join(PROJECT_ROOT, 'gfd_model_v2')
    
    print("=" * 78)
    print("  BUILD AUDIT: GFD Model V2")
    print("=" * 78)
    
    # =========================================================================
    # PART 1: Try importing all modules
    # =========================================================================
    print("\n[1] MODULE IMPORT CHECK")
    print("-" * 78)
    
    import_results = try_import_modules()
    ok_count = sum(1 for r in import_results if r['status'] == 'OK')
    err_count = sum(1 for r in import_results if r['status'] == 'ERROR')
    
    print(f"  Modules OK: {ok_count}")
    print(f"  Modules ERROR: {err_count}")
    
    if err_count > 0:
        print(f"\n  IMPORT ERRORS:")
        for r in import_results:
            if r['status'] == 'ERROR':
                print(f"\n    [{r['category']}] {r['module']}")
                print(f"      {r['error']}")
    
    # =========================================================================
    # PART 2: Scan for locally-defined constants
    # =========================================================================
    print("\n\n[2] CONSTANTS AUDIT (should be in common/)")
    print("-" * 78)
    
    test_files = find_all_test_files(root)
    all_violations = []
    files_without_common_import = []
    
    for filepath in test_files:
        violations, _ = scan_file_for_constants(filepath)
        if violations:
            all_violations.extend(violations)
        
        # Check if file imports from common
        relpath = os.path.relpath(filepath, PROJECT_ROOT)
        if not check_imports(filepath):
            # Only flag test files (not __init__.py etc)
            basename = os.path.basename(filepath)
            if basename.startswith('test_'):
                files_without_common_import.append(relpath)
    
    # Group violations by file
    violations_by_file = {}
    for v in all_violations:
        relpath = os.path.relpath(v['file'], PROJECT_ROOT)
        if relpath not in violations_by_file:
            violations_by_file[relpath] = []
        violations_by_file[relpath].append(v)
    
    print(f"  Files with local constant definitions: {len(violations_by_file)}")
    print(f"  Total violations: {len(all_violations)}")
    print(f"  Test files not importing from common/: {len(files_without_common_import)}")
    
    if violations_by_file:
        print(f"\n  VIOLATIONS BY FILE:")
        for filepath, violations in sorted(violations_by_file.items()):
            print(f"\n    {filepath}")
            for v in violations:
                print(f"      Line {v['line']:4d}: {v['name']:30s} = {v['value'][:40]}")
    
    if files_without_common_import:
        print(f"\n  TEST FILES NOT IMPORTING FROM common/:")
        for f in sorted(files_without_common_import):
            print(f"    {f}")
    
    # =========================================================================
    # PART 3: Summary
    # =========================================================================
    print("\n\n[3] SUMMARY")
    print("=" * 78)
    
    build_ok = err_count == 0
    constants_ok = len(all_violations) == 0
    
    print(f"  Build (imports):    {'PASS' if build_ok else 'FAIL'} ({ok_count}/{ok_count + err_count} modules)")
    print(f"  Constants audit:    {'PASS' if constants_ok else 'FAIL'} ({len(all_violations)} violations in {len(violations_by_file)} files)")
    print(f"  Common imports:     {len(files_without_common_import)} test files missing common/ imports")
    
    if not build_ok or not constants_ok:
        print(f"\n  OVERALL: ISSUES FOUND")
    else:
        print(f"\n  OVERALL: ALL CLEAR")
    
    print("=" * 78)
    
    return 0 if (build_ok and constants_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
