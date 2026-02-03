#!/usr/bin/env python3
"""
==============================================================================
GFD TEST SUITE RESTRUCTURE - PHASE 1
==============================================================================

Reorganizes engine/system_mechanics/ and related directories into a cleaner
structure with better semantic groupings.

Run from: dfp-gravity-field-model/ (repo root)
Usage: python restructure_phase1.py [--dry-run] [--verbose]

Author: GFD Restructure Script
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

# Verify we're in the right directory
REPO_ROOT_MARKER = "dfp_console.py"
GFD_MODEL_ROOT = "gfd_model_v2"
ENGINE_ROOT = f"{GFD_MODEL_ROOT}/engine"
CALC_ROOT = f"{GFD_MODEL_ROOT}/calculations"

# =============================================================================
# FILE MOVE MAP
# =============================================================================
# Format: (source_dir, filename, dest_dir)
# All paths relative to repo root

MOVE_MAP: List[Tuple[str, str, str]] = [
    # =========================================================================
    # system_mechanics → core_geometry (structural geometry tests)
    # =========================================================================
    # Registered modules
    (f"{ENGINE_ROOT}/system_mechanics", "test_complementary_pairs.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_binary_triad.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_vertex_encoding.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_face_classification.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_tetrahedron_assignment.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_subspace_geometry.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_time_face_geometry.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_port_ratio.py", f"{ENGINE_ROOT}/core_geometry"),
    # Orphans (triad/spin geometry)
    (f"{ENGINE_ROOT}/system_mechanics", "test_spin_binding_conservation.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_spin_direction_analysis.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_triad_stability_simulation.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_triad_stability_rigorous.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_triad_fluid_dynamics.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_triad_falsification_attempts.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_interface_parity_triads.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_closure_geometry.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_binding_hierarchy.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_coupled_rotation.py", f"{ENGINE_ROOT}/core_geometry"),
    # Compression tests (geometry-related)
    (f"{ENGINE_ROOT}/system_mechanics", "test_compression_blocking.py", f"{ENGINE_ROOT}/core_geometry"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_bidirectional_compression.py", f"{ENGINE_ROOT}/core_geometry"),

    # =========================================================================
    # system_mechanics → traversal_engine (pi-driven traversal tests)
    # =========================================================================
    (f"{ENGINE_ROOT}/system_mechanics", "test_closure_cycle.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_bbp_validation.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_bbp_engine.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_face_traversal.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_pi_base8_traversal.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_pi_digits_full.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_orbit_statistics.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_field_closure_runs.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_closure_cycle_triforce.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_enterprise_field_closure.py", f"{ENGINE_ROOT}/traversal_engine"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_parallel_face_traversal.py", f"{ENGINE_ROOT}/traversal_engine"),

    # =========================================================================
    # system_mechanics → timing_analysis (timing/frequency tests)
    # =========================================================================
    (f"{ENGINE_ROOT}/system_mechanics", "test_settlement_frequency.py", f"{ENGINE_ROOT}/timing_analysis"),

    # =========================================================================
    # system_mechanics → information_theory (bits/entropy tests)
    # =========================================================================
    (f"{ENGINE_ROOT}/system_mechanics", "test_information_content.py", f"{ENGINE_ROOT}/information_theory"),

    # =========================================================================
    # system_mechanics → CALC emergent_constants (derived constants)
    # =========================================================================
    (f"{ENGINE_ROOT}/system_mechanics", "test_field_energy.py", f"{CALC_ROOT}/emergent_constants"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_spin_derivation.py", f"{CALC_ROOT}/emergent_constants"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_mond_hexagonal.py", f"{CALC_ROOT}/emergent_constants"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_hubble_electron_mond.py", f"{CALC_ROOT}/emergent_constants"),
    (f"{ENGINE_ROOT}/system_mechanics", "test_sixfold_symmetry.py", f"{CALC_ROOT}/emergent_constants"),

    # =========================================================================
    # theoretical_insights → information_theory
    # =========================================================================
    (f"{ENGINE_ROOT}/theoretical_insights", "test_information_theory.py", f"{ENGINE_ROOT}/information_theory"),

    # =========================================================================
    # theoretical_insights → lattice_foundations
    # =========================================================================
    (f"{ENGINE_ROOT}/theoretical_insights", "test_lattice_fundamentals.py", f"{ENGINE_ROOT}/lattice_foundations"),

    # =========================================================================
    # information_flow → information_theory
    # =========================================================================
    (f"{ENGINE_ROOT}/information_flow", "test_bit_propagation.py", f"{ENGINE_ROOT}/information_theory"),

    # =========================================================================
    # CALC symmetry_operations → ENGINE core_geometry
    # =========================================================================
    (f"{CALC_ROOT}/symmetry_operations", "test_stellated_octahedron_symmetries.py", f"{ENGINE_ROOT}/core_geometry"),
]

# Directories to create (if they don't exist)
NEW_DIRECTORIES = [
    f"{ENGINE_ROOT}/core_geometry",
    f"{ENGINE_ROOT}/traversal_engine",
    f"{ENGINE_ROOT}/information_theory",
    f"{ENGINE_ROOT}/lattice_foundations",
]

# Directories to dissolve (remove if empty after moves)
DISSOLVE_DIRECTORIES = [
    f"{ENGINE_ROOT}/system_mechanics",
    f"{ENGINE_ROOT}/theoretical_insights",
    f"{ENGINE_ROOT}/information_flow",
    f"{CALC_ROOT}/symmetry_operations",
]

# =============================================================================
# UTILITIES
# =============================================================================

class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    DIM = '\033[38;5;245m'
    GREEN = '\033[38;5;46m'
    CYAN = '\033[38;5;51m'
    YELLOW = '\033[38;5;226m'
    RED = '\033[38;5;196m'
    PURPLE = '\033[38;5;129m'


def print_header(text: str):
    """Print a section header."""
    print(f"\n{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")


def print_step(step_num: int, text: str):
    """Print a step header."""
    print(f"\n{Colors.PURPLE}[Step {step_num}] {text}{Colors.RESET}")
    print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")


def print_success(text: str):
    """Print success message."""
    print(f"  {Colors.GREEN}[OK]{Colors.RESET} {text}")


def print_warning(text: str):
    """Print warning message."""
    print(f"  {Colors.YELLOW}[!!]{Colors.RESET} {text}")


def print_error(text: str):
    """Print error message."""
    print(f"  {Colors.RED}[ERR]{Colors.RESET} {text}")


def print_info(text: str):
    """Print info message."""
    print(f"  {Colors.DIM}  ->{Colors.RESET} {text}")


def file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def create_init_py(directory: Path):
    """Create an __init__.py file in the directory."""
    init_file = directory / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""Package initialization."""\n')
        return True
    return False


# =============================================================================
# MAIN RESTRUCTURE LOGIC
# =============================================================================

class Restructurer:
    """Handles the test suite restructuring."""

    def __init__(self, repo_root: Path, dry_run: bool = False, verbose: bool = False):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.verbose = verbose
        self.copy_results: Dict[str, bool] = {}
        self.errors: List[str] = []

    def run(self) -> bool:
        """Execute the full restructuring process."""
        print_header("GFD TEST SUITE RESTRUCTURE - PHASE 1")
        print(f"  Repo root: {self.repo_root}")
        print(f"  Dry run:   {self.dry_run}")
        print(f"  Timestamp: {datetime.now().isoformat()}")

        # Step 1: Preflight checks
        if not self.step1_preflight():
            return False

        # Step 2: Create new directories
        self.step2_create_directories()

        # Step 3: Copy files to new locations
        self.step3_copy_files()

        # Step 4: Verify copies
        if not self.step4_verify_copies():
            print_error("Verification failed. Originals NOT deleted.")
            return False

        # Step 5: Remove verified originals
        self.step5_remove_originals()

        # Step 6: Clean up empty directories
        self.step6_cleanup_directories()

        # Step 7: Final report
        self.step7_final_report()

        return len(self.errors) == 0

    def step1_preflight(self) -> bool:
        """Verify we're in the right place and files exist."""
        print_step(1, "Preflight Checks")

        # Check repo root marker
        marker = self.repo_root / REPO_ROOT_MARKER
        if not marker.exists():
            print_error(f"Not in repo root: {REPO_ROOT_MARKER} not found")
            print_info(f"Run this script from dfp-gravity-field-model/")
            return False
        print_success(f"Found {REPO_ROOT_MARKER} (confirmed repo root)")

        # Check gfd_model_v2 exists
        model_root = self.repo_root / GFD_MODEL_ROOT
        if not model_root.exists():
            print_error(f"Missing: {GFD_MODEL_ROOT}/")
            return False
        print_success(f"Found {GFD_MODEL_ROOT}/")

        # Check system_mechanics exists
        sys_mech = self.repo_root / ENGINE_ROOT / "system_mechanics"
        if not sys_mech.exists():
            print_error(f"Missing: {ENGINE_ROOT}/system_mechanics/")
            return False

        # Count files to move
        files_found = 0
        files_missing = []
        for src_dir, filename, _ in MOVE_MAP:
            src_path = self.repo_root / src_dir / filename
            if src_path.exists():
                files_found += 1
            else:
                files_missing.append(f"{src_dir}/{filename}")

        print_success(f"Found {files_found}/{len(MOVE_MAP)} files to move")

        if files_missing:
            print_warning(f"Missing {len(files_missing)} files:")
            for f in files_missing[:5]:
                print_info(f)
            if len(files_missing) > 5:
                print_info(f"... and {len(files_missing) - 5} more")

        # Scan for unexpected files in system_mechanics
        expected_files = {filename for src_dir, filename, dest_dir in MOVE_MAP 
                          if "system_mechanics" in src_dir}
        actual_files = set()
        for f in sys_mech.glob("test_*.py"):
            actual_files.add(f.name)

        unexpected = actual_files - expected_files
        if unexpected:
            print_warning(f"Found {len(unexpected)} files NOT in move map:")
            for f in sorted(unexpected):
                print_info(f"{Colors.YELLOW}{f}{Colors.RESET}")

        return True

    def step2_create_directories(self):
        """Create new destination directories."""
        print_step(2, "Create New Directories")

        for dir_path in NEW_DIRECTORIES:
            full_path = self.repo_root / dir_path
            if full_path.exists():
                print_info(f"Already exists: {dir_path}/")
            else:
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                    create_init_py(full_path)
                print_success(f"Created: {dir_path}/")

    def step3_copy_files(self):
        """Copy files to new locations (originals remain)."""
        print_step(3, "Copy Files to New Locations")

        copied = 0
        skipped = 0

        for src_dir, filename, dest_dir in MOVE_MAP:
            src_path = self.repo_root / src_dir / filename
            dest_path = self.repo_root / dest_dir / filename

            if not src_path.exists():
                if self.verbose:
                    print_warning(f"Source missing: {src_dir}/{filename}")
                skipped += 1
                continue

            if dest_path.exists():
                print_warning(f"Dest exists, skipping: {dest_dir}/{filename}")
                skipped += 1
                continue

            key = f"{src_dir}/{filename}"

            if not self.dry_run:
                try:
                    # Ensure destination directory exists
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    create_init_py(dest_path.parent)

                    # Copy with metadata preserved
                    shutil.copy2(src_path, dest_path)
                    self.copy_results[key] = True
                    copied += 1
                    if self.verbose:
                        print_success(f"{filename} -> {dest_dir}/")
                except Exception as e:
                    self.copy_results[key] = False
                    self.errors.append(f"Copy failed {key}: {e}")
                    print_error(f"Failed: {filename}: {e}")
            else:
                self.copy_results[key] = True
                copied += 1
                if self.verbose:
                    print_info(f"Would copy: {filename} -> {dest_dir}/")

        print_success(f"Copied {copied} files")
        if skipped:
            print_info(f"Skipped {skipped} files (missing source or dest exists)")

    def step4_verify_copies(self) -> bool:
        """Verify all copied files match their sources."""
        print_step(4, "Verify Copies")

        if self.dry_run:
            print_info("Dry run - skipping verification")
            return True

        verified = 0
        failed = 0

        for src_dir, filename, dest_dir in MOVE_MAP:
            key = f"{src_dir}/{filename}"

            # Skip if copy wasn't attempted
            if key not in self.copy_results or not self.copy_results[key]:
                continue

            src_path = self.repo_root / src_dir / filename
            dest_path = self.repo_root / dest_dir / filename

            if not src_path.exists():
                continue

            if not dest_path.exists():
                print_error(f"Dest missing: {dest_dir}/{filename}")
                self.copy_results[key] = False
                failed += 1
                continue

            # Compare sizes
            if src_path.stat().st_size != dest_path.stat().st_size:
                print_error(f"Size mismatch: {filename}")
                self.copy_results[key] = False
                failed += 1
                continue

            # Compare hashes
            if file_hash(src_path) != file_hash(dest_path):
                print_error(f"Hash mismatch: {filename}")
                self.copy_results[key] = False
                failed += 1
                continue

            verified += 1

        print_success(f"Verified {verified} files")
        if failed:
            print_error(f"Failed verification: {failed} files")

        return failed == 0

    def step5_remove_originals(self):
        """Remove original files that were successfully copied and verified."""
        print_step(5, "Remove Verified Originals")

        if self.dry_run:
            print_info("Dry run - not removing originals")
            return

        removed = 0
        kept = 0

        for src_dir, filename, dest_dir in MOVE_MAP:
            key = f"{src_dir}/{filename}"
            src_path = self.repo_root / src_dir / filename

            if not src_path.exists():
                continue

            if self.copy_results.get(key, False):
                try:
                    src_path.unlink()
                    removed += 1
                    if self.verbose:
                        print_success(f"Removed: {src_dir}/{filename}")
                except Exception as e:
                    print_error(f"Failed to remove {filename}: {e}")
                    kept += 1
            else:
                kept += 1
                if self.verbose:
                    print_warning(f"Kept (not verified): {src_dir}/{filename}")

        print_success(f"Removed {removed} original files")
        if kept:
            print_info(f"Kept {kept} files (not copied/verified)")

    def step6_cleanup_directories(self):
        """Remove directories that are now empty."""
        print_step(6, "Cleanup Empty Directories")

        if self.dry_run:
            print_info("Dry run - not removing directories")
            return

        for dir_path in DISSOLVE_DIRECTORIES:
            full_path = self.repo_root / dir_path

            if not full_path.exists():
                print_info(f"Already gone: {dir_path}/")
                continue

            # Count remaining test files
            remaining = list(full_path.glob("test_*.py"))

            if remaining:
                print_warning(f"Not empty ({len(remaining)} files): {dir_path}/")
                for f in remaining[:3]:
                    print_info(f"  {f.name}")
                if len(remaining) > 3:
                    print_info(f"  ... and {len(remaining) - 3} more")
            else:
                # Remove __pycache__ first
                pycache = full_path / "__pycache__"
                if pycache.exists():
                    shutil.rmtree(pycache)

                # Check if truly empty (except __init__.py)
                remaining_all = [f for f in full_path.iterdir() if f.name != "__init__.py"]

                if not remaining_all:
                    shutil.rmtree(full_path)
                    print_success(f"Removed: {dir_path}/")
                else:
                    print_warning(f"Has non-test files: {dir_path}/")
                    for f in remaining_all:
                        print_info(f"  {f.name}")

    def step7_final_report(self):
        """Print final status and next steps."""
        print_step(7, "Final Report")

        # Count new directory contents
        print(f"\n  {Colors.CYAN}New Directory Structure:{Colors.RESET}")
        for dir_path in NEW_DIRECTORIES:
            full_path = self.repo_root / dir_path
            if full_path.exists():
                count = len(list(full_path.glob("test_*.py")))
                print(f"    {dir_path}/: {count} test files")

        # Check emergent_constants (gained files)
        ec_path = self.repo_root / CALC_ROOT / "emergent_constants"
        if ec_path.exists():
            count = len(list(ec_path.glob("test_*.py")))
            print(f"    {CALC_ROOT}/emergent_constants/: {count} test files")

        # Report any errors
        if self.errors:
            print(f"\n  {Colors.RED}Errors:{Colors.RESET}")
            for err in self.errors:
                print(f"    {err}")

        # Next steps
        print(f"\n  {Colors.YELLOW}NEXT STEPS:{Colors.RESET}")
        print(f"    1. Update CATEGORIES dict in dfp_console.py")
        print(f"    2. Update any import statements in test files")
        print(f"    3. Run: python dfp_console.py (verify all tests pass)")
        print(f"    4. Delete __pycache__ directories if needed")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="GFD Test Suite Restructure - Phase 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python restructure_phase1.py --dry-run    # Preview changes
  python restructure_phase1.py              # Execute restructure
  python restructure_phase1.py --verbose    # Execute with detailed output
        """
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without modifying files")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed progress")

    args = parser.parse_args()

    # Determine repo root (current directory)
    repo_root = Path.cwd()

    # Run restructure
    restructurer = Restructurer(repo_root, dry_run=args.dry_run, verbose=args.verbose)
    success = restructurer.run()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
