# GFD Test Suite Restructure Plan

**Generated:** 2026-02-03  
**Status:** Ready for execution

---

## Executive Summary

Reorganize the `engine/system_mechanics/` monolith (38 files) into semantically meaningful directories while maintaining all CATEGORIES registrations and import paths.

---

## Current State (Verified from Filesystem)

### engine/system_mechanics/ — 38 FILES TOTAL

**Registered in CATEGORIES (26 files):**
```
test_closure_cycle.py
test_bbp_validation.py
test_face_traversal.py
test_complementary_pairs.py
test_binary_triad.py
test_field_energy.py
test_settlement_frequency.py
test_orbit_statistics.py
test_spin_derivation.py
test_vertex_encoding.py
test_face_classification.py
test_tetrahedron_assignment.py
test_bbp_engine.py
test_information_content.py
test_port_ratio.py
test_pi_base8_traversal.py
test_mond_hexagonal.py
test_sixfold_symmetry.py
test_hubble_electron_mond.py
test_subspace_geometry.py
test_time_face_geometry.py
test_field_closure_runs.py
test_closure_cycle_triforce.py
test_enterprise_field_closure.py
test_parallel_face_traversal.py
test_pi_digits_full.py
```

**Orphan files NOT in CATEGORIES (12 files):**
```
test_spin_binding_conservation.py
test_spin_direction_analysis.py
test_triad_stability_simulation.py
test_triad_stability_rigorous.py
test_triad_fluid_dynamics.py
test_triad_falsification_attempts.py
test_interface_parity_triads.py
test_compression_blocking.py
test_bidirectional_compression.py
test_closure_geometry.py
test_binding_hierarchy.py
test_coupled_rotation.py
```

### Other ENGINE Directories

| Directory | Files | In CATEGORIES |
|-----------|-------|---------------|
| timing_analysis/ | 1 | Yes |
| theoretical_insights/ | 2 | Yes |
| information_flow/ | 1 | Yes |
| engine_stress_tests/ | 1 | Yes |
| engine_crosschecks/ | 2 | **No** |
| timing_analysis_advanced/ | 0 | N/A (empty) |

### CALC symmetry_operations/

| File | Status |
|------|--------|
| test_stellated_octahedron_symmetries.py | Misplaced (is ENGINE work) |

---

## Proposed New Structure

### NEW ENGINE Directories (4 to create)

| Directory | Purpose | File Count |
|-----------|---------|------------|
| `core_geometry/` | Structural geometry, triads, vertices, faces, compression | 21 files (20 from sys_mech + 1 from symmetry_ops) |
| `traversal_engine/` | Pi-driven traversal, BBP algorithm, closure cycles | 11 files |
| `information_theory/` | Bits, entropy, information content | 3 files |
| `lattice_foundations/` | Axioms and fundamental bounds | 1 file |

### Directories to Dissolve (after moves)

| Directory | Reason |
|-----------|--------|
| `system_mechanics/` | All 38 files distributed |
| `theoretical_insights/` | 2 files distributed |
| `information_flow/` | 1 file distributed |
| `symmetry_operations/` (CALC) | 1 file moved to ENGINE |

### Directories UNCHANGED

| Directory | Files |
|-----------|-------|
| `engine_stress_tests/` | 1 |
| `timing_analysis/` | 1 → 2 (gains 1) |
| `engine_crosschecks/` | 2 |

---

## File Move Map (42 moves total)

### system_mechanics → core_geometry (21 files)

**Registered (8):**
- test_complementary_pairs.py
- test_binary_triad.py
- test_vertex_encoding.py
- test_face_classification.py
- test_tetrahedron_assignment.py
- test_subspace_geometry.py
- test_time_face_geometry.py
- test_port_ratio.py

**Orphans (13):**
- test_spin_binding_conservation.py
- test_spin_direction_analysis.py
- test_triad_stability_simulation.py
- test_triad_stability_rigorous.py
- test_triad_fluid_dynamics.py
- test_triad_falsification_attempts.py
- test_interface_parity_triads.py
- test_closure_geometry.py
- test_binding_hierarchy.py
- test_coupled_rotation.py
- test_compression_blocking.py
- test_bidirectional_compression.py

### system_mechanics → traversal_engine (11 files)

- test_closure_cycle.py
- test_bbp_validation.py
- test_bbp_engine.py
- test_face_traversal.py
- test_pi_base8_traversal.py
- test_pi_digits_full.py
- test_orbit_statistics.py
- test_field_closure_runs.py
- test_closure_cycle_triforce.py
- test_enterprise_field_closure.py
- test_parallel_face_traversal.py

### system_mechanics → timing_analysis (1 file)

- test_settlement_frequency.py

### system_mechanics → information_theory (1 file)

- test_information_content.py

### system_mechanics → CALC emergent_constants (5 files)

- test_field_energy.py
- test_spin_derivation.py
- test_mond_hexagonal.py
- test_hubble_electron_mond.py
- test_sixfold_symmetry.py

### theoretical_insights → information_theory (1 file)

- test_information_theory.py

### theoretical_insights → lattice_foundations (1 file)

- test_lattice_fundamentals.py

### information_flow → information_theory (1 file)

- test_bit_propagation.py

### CALC symmetry_operations → ENGINE core_geometry (1 file)

- test_stellated_octahedron_symmetries.py

---

## Execution Plan

### Phase 1: File Restructure (restructure_phase1.py)

```bash
cd dfp-gravity-field-model
python restructure_phase1.py --dry-run    # Preview changes
python restructure_phase1.py              # Execute
```

**Step 1:** Preflight checks
- Verify dfp_console.py exists (repo root confirmation)
- Count files to move vs expected
- Report unexpected files

**Step 2:** Create new directories + `__init__.py`
- core_geometry/
- traversal_engine/
- information_theory/
- lattice_foundations/

**Step 3:** Copy files (shutil.copy2)
- Preserves timestamps
- Originals remain in place

**Step 4:** Verify copies
- File size match
- MD5 hash match
- Report any mismatches

**Step 5:** Remove originals
- Only delete files that passed verification
- Keep any files that failed

**Step 6:** Cleanup empty directories
- Only remove if zero test_*.py files remain
- Remove __pycache__ first
- Report any directories with remaining files

**Step 7:** Final report
- New directory structure with file counts
- Next steps for CATEGORIES update

### Phase 2: Update dfp_console.py CATEGORIES

After Phase 1 completes successfully, update the CATEGORIES dict:

**Remove categories:**
- `system_mechanics` (dissolved)
- `theoretical_insights` (dissolved)
- `information_flow` (dissolved)

**Add new ENGINE categories:**
```python
"core_geometry": {
    "name": "Core Geometry",
    "type": "ENGINE",
    "description": "Structural geometry: triads, vertices, faces, compression, spin binding",
    "modules": [
        "gfd_model_v2.engine.core_geometry.test_complementary_pairs",
        "gfd_model_v2.engine.core_geometry.test_binary_triad",
        # ... (21 total)
    ]
},
"traversal_engine": {
    "name": "Traversal Engine",
    "type": "ENGINE",
    "description": "Pi-driven traversal, BBP algorithm, closure cycles, orbit statistics",
    "modules": [
        "gfd_model_v2.engine.traversal_engine.test_closure_cycle",
        # ... (11 total)
    ]
},
"information_theory": {
    "name": "Information Theory",
    "type": "ENGINE",
    "description": "Bits, entropy, information content, bandwidth",
    "modules": [
        "gfd_model_v2.engine.information_theory.test_information_content",
        "gfd_model_v2.engine.information_theory.test_information_theory",
        "gfd_model_v2.engine.information_theory.test_bit_propagation",
    ]
},
"lattice_foundations": {
    "name": "Lattice Foundations",
    "type": "ENGINE",
    "description": "Axioms and fundamental bounds of the lattice structure",
    "modules": [
        "gfd_model_v2.engine.lattice_foundations.test_lattice_fundamentals",
    ]
},
```

**Update timing_analysis:**
```python
"timing_analysis": {
    "name": "Timing Analysis",
    "type": "ENGINE",
    "description": "Closure simultaneity, Compton-scale timing, settlement frequency",
    "modules": [
        "gfd_model_v2.engine.timing_analysis.test_closure_simultaneity",
        "gfd_model_v2.engine.timing_analysis.test_settlement_frequency",  # NEW
    ]
},
```

**Update emergent_constants (add 5 modules):**
```python
"emergent_constants": {
    "name": "Emergent Constants",
    "type": "CALC",
    "description": "Fundamental parameters derived from geometry",
    "modules": [
        "gfd_model_v2.calculations.emergent_constants.test_emergent_constants",
        "gfd_model_v2.calculations.emergent_constants.test_emergent_constants_extended",
        "gfd_model_v2.calculations.emergent_constants.test_field_energy",        # NEW
        "gfd_model_v2.calculations.emergent_constants.test_spin_derivation",     # NEW
        "gfd_model_v2.calculations.emergent_constants.test_mond_hexagonal",      # NEW
        "gfd_model_v2.calculations.emergent_constants.test_hubble_electron_mond",# NEW
        "gfd_model_v2.calculations.emergent_constants.test_sixfold_symmetry",    # NEW
    ]
},
```

**Remove symmetry_operations category** (file moved to ENGINE core_geometry)

### Phase 3: Update Imports (if needed)

If any test files have relative imports like:
```python
from ..system_mechanics import something
```

These need to be updated to the new paths.

### Phase 4: Validation

```bash
python dfp_console.py
# Select [2] Run All Validation Tests
# Verify all tests pass
```

---

## Risk Mitigation

1. **Copy-then-verify-then-delete:** Files are never moved directly. We copy, verify the copy is identical, then delete the original.

2. **Dry run available:** `--dry-run` flag shows exactly what will happen without modifying anything.

3. **No CATEGORIES changes in Phase 1:** The console will show errors for missing modules until Phase 2 is complete. This is expected.

4. **Rollback:** If needed, the original files can be restored from git history.

---

## Summary

| Metric | Before | After |
|--------|--------|-------|
| ENGINE directories | 7 | 8 |
| system_mechanics/ files | 38 | 0 (dissolved) |
| Largest ENGINE directory | 38 files | 21 files |
| Orphan files | 12 | 0 (all categorized) |
| Total file moves | — | 42 |
