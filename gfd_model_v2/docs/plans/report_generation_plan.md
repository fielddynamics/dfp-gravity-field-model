# Report Generation Plan — Pre-Flight Check & Advanced Metrics
## Two Reports, Two Purposes, One Flight Plan

---

## The Idea

Every time the flight plan runs, two reports are automatically generated:

```
reports/
├── GFD-PREFLIGHT-20260203-143022.md       ← "Are we GO for launch?"
└── GFD-ADVANCED-TIMING-20260203-143022.md ← "What did the instruments see?"
```

**Report 1: Engine Pre-Flight Check** covers all core systems (not just timing — the
full engine). This is the GO/NO-GO document. If it's not green, nothing else matters.

**Report 2: Advanced Timing Metrics** covers the advanced timing analysis. This is the
science payload. It runs regardless, but results are interpretive rather than blocking.

Both are generated in one pass during `[2] Run All Validation Tests` or via a new
`[6] Generate Flight Reports` menu option.

---

## Architecture: How It Hooks In

### Current Flow
```
dfp_console.py
  └── run_all_tests_quick()
        ├── imports each module
        ├── runs test_class().run() → TestResult
        ├── counts pass/fail
        └── returns results dict (by_category)
              └── display_quick_test_results() → terminal output
```

### New Flow
```
dfp_console.py
  └── run_all_tests_quick()          ← UNCHANGED, still returns results dict
        └── results dict
              ├── display_quick_test_results()   ← existing terminal output
              └── generate_flight_reports()       ← NEW
                    ├── _collect_detailed_results()  ← runs tests again WITH TestResult objects
                    ├── _build_preflight_report()     ← Report 1: markdown
                    ├── _build_advanced_report()      ← Report 2: markdown
                    └── saves to reports/
```

### Key Design Decision: Collect Full TestResults

`run_all_tests_quick()` currently discards `TestResult` objects — it only counts
pass/fail. For reports, we need the full objects (model values, observations,
derivations, commentary, error percentages). So the report generator runs a
**second pass** that collects `TestResult` objects without terminal output.

This keeps `run_all_tests_quick()` unchanged and backward-compatible.

```python
def _collect_detailed_results(category_keys):
    """
    Run specified categories and return full TestResult objects.
    Suppresses terminal output. Returns:
    {
        'category_key': {
            'name': str,
            'type': str,
            'description': str,
            'modules': {
                'module_path': {
                    'group_title': str,
                    'tests': [TestResult, ...],
                    'passed': int,
                    'failed': int,
                }
            }
        }
    }
    """
```

---

## Report 1: Engine Pre-Flight Check

### What It Covers

ALL engine categories — not just timing. This is the full systems check:

| Section | Categories | Purpose |
|---------|-----------|---------|
| **§1 System Mechanics** | `system_mechanics` | Core traversal, vertex encoding, field closure |
| **§2 Timing Analysis** | `timing_analysis` | Settlement frequency, simultaneity, hierarchy, jitter, causality |
| **§3 Theoretical Insights** | `theoretical_insights` | Information theory, lattice fundamentals |
| **§4 Information Flow** | `information_flow` | Bit propagation, entropy |
| **§5 Engine Stress Tests** | `engine_stress_tests` | Determinism, ergodicity, stability |

### Report Structure

```markdown
╔══════════════════════════════════════════════════════════════════════╗
║                    GFD ENGINE PRE-FLIGHT CHECK                      ║
║                    Document: GFD-PFC-20260203-143022                ║
╚══════════════════════════════════════════════════════════════════════╝

CLASSIFICATION:  Internal — GFD Model Validation
GENERATED:       2026-02-03 14:30:22 UTC
FRAMEWORK:       GFD Model V2
ENGINE VERSION:  (git hash if available)
PYTHON:          3.x.x
PLATFORM:        (os info)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        EXECUTIVE SUMMARY

  STATUS:    ██ GO       (or ██ NO-GO)
  TESTS:     187/187 PASSED
  ANOMALIES: 0
  MAX ERROR: 0.003%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§1  SYSTEM OVERVIEW

  The GFD Engine operates on a stellated octahedron (dual Field Chamber)
  with 2k=8 vertices driven by pi base-8 traversal. Settlement frequency:
  1.236×10²⁰ Hz. This report validates all core engine subsystems.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§2  GO/NO-GO MATRIX

  ┌─────────────────────────────┬────────┬───────┬────────────┐
  │ Subsystem                   │ Tests  │ Pass  │ Status     │
  ├─────────────────────────────┼────────┼───────┼────────────┤
  │ System Mechanics            │  85    │ 85    │ ██ GO      │
  │ Timing Analysis (Core)      │  45    │ 45    │ ██ GO      │
  │ Theoretical Insights        │  24    │ 24    │ ██ GO      │
  │ Information Flow            │  12    │ 12    │ ██ GO      │
  │ Engine Stress Tests         │  21    │ 21    │ ██ GO      │
  ├─────────────────────────────┼────────┼───────┼────────────┤
  │ TOTAL                       │ 187    │ 187   │ ██ GO      │
  └─────────────────────────────┴────────┴───────┴────────────┘

  DECISION: ALL SUBSYSTEMS GO. ENGINE CLEARED FOR OPERATION.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§3  CRITICAL PARAMETERS

  ┌──────────────────────────────────┬──────────────────┬───────────┐
  │ Parameter                        │ Value            │ Status    │
  ├──────────────────────────────────┼──────────────────┼───────────┤
  │ Settlement Frequency             │ 1.2356×10²⁰ Hz   │ NOMINAL   │
  │ Settlement Period                │ 8.09×10⁻²¹ s     │ NOMINAL   │
  │ Port Firing Frequency            │ 3.09×10¹⁹ Hz     │ NOMINAL   │
  │ Light Crossing / Step Ratio      │ 3.46             │ NOMINAL   │
  │ Vertex Coverage                  │ 8/8              │ COMPLETE  │
  │ Tetrahedra Balance               │ 50.2%/49.8%      │ NOMINAL   │
  │ Determinism (100-run hash)       │ 0 mismatches     │ VERIFIED  │
  │ Ergodic Convergence σ            │ 0.012            │ NOMINAL   │
  │ Information Preservation         │ 100%             │ VERIFIED  │
  │ Modular Arithmetic Consistency   │ 100%             │ VERIFIED  │
  └──────────────────────────────────┴──────────────────┴───────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§4  DETAILED RESULTS BY SUBSYSTEM

  §4.1  SYSTEM MECHANICS  [85/85 PASS]
  ─────────────────────────────────────

    §4.1.1  Vertex Encoding
    ┌──────────────────────────────┬─────────┬──────────┬────────┬────────┐
    │ Test                         │ Model   │ Observed │ Error  │ Status │
    ├──────────────────────────────┼─────────┼──────────┼────────┼────────┤
    │ Vertices 0-7: Count          │ 8       │ 8        │ 0.00%  │ PASS   │
    │ Vertices 0-7: Correct        │ 1       │ 1        │ 0.00%  │ PASS   │
    │ Binary 3-bit: All valid      │ 8       │ 8        │ 0.00%  │ PASS   │
    │ ...                          │         │          │        │        │
    └──────────────────────────────┴─────────┴──────────┴────────┴────────┘

    (continues for each module...)

  §4.2  TIMING ANALYSIS (CORE)  [45/45 PASS]
  ─────────────────────────────────────────────
    (all core timing modules...)

  §4.3  THEORETICAL INSIGHTS  [24/24 PASS]
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§5  ANOMALY LOG

  No anomalies detected.

  (or, if failures exist:)
  ┌─────┬──────────────────────┬──────────────┬────────┬──────────────┐
  │ #   │ Test                 │ Subsystem    │ Error  │ Severity     │
  ├─────┼──────────────────────┼──────────────┼────────┼──────────────┤
  │ A-1 │ Ergodic Convergence  │ Stress Tests │ 6.2%   │ ADVISORY     │
  │ A-2 │ ...                  │ ...          │ ...    │ ...          │
  └─────┴──────────────────────┴──────────────┴────────┴──────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§6  CERTIFICATION

  This report was generated automatically by the GFD Engine Pre-Flight
  Check system. All tests executed against the current codebase with
  no manual intervention.

  Generated: 2026-02-03 14:30:22 UTC
  Duration:  4.7 seconds
  Report ID: GFD-PFC-20260203-143022

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                          END OF REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Report 2: Advanced Timing Metrics

### What It Covers

Only `timing_analysis_advanced` — the exploratory science:

| Section | Module | Purpose |
|---------|--------|---------|
| **§1 Phase Coherence** | `test_phase_coherence` | Berry phase dynamics |
| **§2 Spectral Analysis** | `test_spectral_analysis` | Frequency domain characterization |
| **§3 Relativistic Timing** | `test_relativistic_timing` | GR, GPS, curved spacetime |
| **§4 Quantum Clock** | `test_quantum_clock` | Metrological characterization |

### Report Structure

```markdown
╔══════════════════════════════════════════════════════════════════════╗
║               GFD ADVANCED TIMING ANALYSIS REPORT                   ║
║               Document: GFD-ATR-20260203-143022                     ║
╚══════════════════════════════════════════════════════════════════════╝

CLASSIFICATION:  Internal — GFD Advanced Analysis
GENERATED:       2026-02-03 14:30:22 UTC
PREREQUISITE:    GFD-PFC-20260203-143022 (Pre-Flight: GO)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        EXECUTIVE SUMMARY

  PRE-FLIGHT STATUS: GO (all core tests passed)
  ADVANCED TESTS:    42/42 COMPLETED
  NEW FINDINGS:      3
  OPEN QUESTIONS:    2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§1  PRE-FLIGHT REFERENCE

  This analysis depends on the core engine being operational.
  Pre-Flight Report: GFD-PFC-20260203-143022
  Pre-Flight Status: ██ GO (187/187 tests passed)

  Core Timing Parameters (from Pre-Flight):
  ┌──────────────────────────────────┬──────────────────┐
  │ Settlement Frequency             │ 1.2356×10²⁰ Hz   │
  │ Timing Jitter (σ_y)             │ 0.043            │
  │ Causal Diameter                  │ 4 steps          │
  │ Nonlocal Fraction                │ 62%              │
  └──────────────────────────────────┴──────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§2  ANALYSIS MATRIX

  ┌─────────────────────────────┬────────┬───────┬──────────────┐
  │ Analysis Domain             │ Tests  │ Pass  │ Findings     │
  ├─────────────────────────────┼────────┼───────┼──────────────┤
  │ Phase Coherence             │  10    │ 10    │ 1 new        │
  │ Spectral Analysis           │  10    │ 10    │ 1 new        │
  │ Relativistic Timing         │  12    │ 12    │ 1 new        │
  │ Quantum Clock Metrology     │  10    │ 10    │ 0            │
  ├─────────────────────────────┼────────┼───────┼──────────────┤
  │ TOTAL                       │  42    │ 42    │ 3 new        │
  └─────────────────────────────┴────────┴───────┴──────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§3  FINDINGS

  FINDING ATR-001: Phase Coherence
  ────────────────────────────────
  Berry phase accumulates coherently over 137 orbits, with total
  phase = 274π ± 0.003. Phase autocorrelation shows no degradation
  up to lag-100, consistent with geometric (non-random) accumulation.

  FINDING ATR-002: Spectral Structure
  ─────────────────────────────────────
  Closure event PSD shows spectral flatness = 0.87 (near white noise)
  but with a marginal peak at the 8th harmonic, consistent with
  base-8 octave structure. Significance: 2.1σ. Requires more digits.

  FINDING ATR-003: GPS Consistency
  ──────────────────────────────────
  Settlement frequency under combined SR+GR GPS correction produces
  a 38.1 μs/day drift, matching the operational GPS correction of
  38.0 μs/day to 0.3%.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§4  DETAILED RESULTS BY DOMAIN

  (same detailed table format as pre-flight...)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§5  OPEN QUESTIONS

  OQ-1: Does the 8th harmonic in the closure PSD persist with
        10,000+ pi digits? (Currently tested with 200.)

  OQ-2: The phase slip at orbit 89 — coincidence with Fibonacci,
        or artifact of digit sequence?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§6  CLOCK METROLOGY SUMMARY

  ┌──────────────────────────────────┬──────────────────┬──────────────┐
  │ Metric                           │ GFD Value        │ Comparison   │
  ├──────────────────────────────────┼──────────────────┼──────────────┤
  │ Q Factor                         │ 2.3×10⁴          │ Cs: 10¹⁰    │
  │ Fractional Instability (1 orbit) │ 4.3×10⁻²         │              │
  │ Fractional Instability (137 orb) │ 3.7×10⁻³         │              │
  │ Timekeeping Capacity             │ 66.7 bits/s      │              │
  │ Settlement / Cesium Ratio        │ 1.344×10¹⁰       │              │
  │ Settlement / Strontium Ratio     │ 2.880×10⁵        │              │
  └──────────────────────────────────┴──────────────────┴──────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§7  CERTIFICATION

  Generated: 2026-02-03 14:30:22 UTC
  Duration:  8.2 seconds
  Depends on: GFD-PFC-20260203-143022
  Report ID: GFD-ATR-20260203-143022

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                          END OF REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Implementation: New File `report_generator.py`

This is a standalone module at the same level as `dfp_console.py` and `base.py`.
It imports from `base.py` and the test modules, but does NOT modify them.

### File Structure

```python
"""
GFD Report Generator
====================

Generates NASA/CERN-style validation reports from GFDTest results.

Reports:
  1. Pre-Flight Check (PFC) — All ENGINE categories → GO/NO-GO
  2. Advanced Timing Report (ATR) — timing_analysis_advanced → Science findings

Usage:
    from report_generator import generate_flight_reports
    generate_flight_reports()                    # Both reports
    generate_flight_reports(preflight_only=True) # Core only
"""
```

### Key Functions

```python
# ─── Data Collection ─────────────────────────────────────────────

def _collect_detailed_results(category_keys: list) -> dict:
    """
    Run specified categories silently, return full TestResult objects.
    This is the second pass — run_all_tests_quick() handles the terminal
    display, this handles the report data.
    """

def _extract_critical_parameters(results: dict) -> list:
    """
    Pull out the key values that go in the Critical Parameters table.
    Searches TestResult objects for specific metric names.
    """

def _identify_anomalies(results: dict) -> list:
    """
    Find all failed tests or tests with error > 50% of tolerance.
    Returns list of anomaly dicts for the Anomaly Log.
    """

def _identify_findings(results: dict) -> list:
    """
    For advanced report: extract notable results where commentary
    indicates a new finding or where observed matches model unusually well.
    """


# ─── Report Builders ─────────────────────────────────────────────

def _build_preflight_report(results: dict, timestamp: str) -> str:
    """
    Build the Pre-Flight Check markdown string.
    Sections: Header, Executive Summary, GO/NO-GO Matrix,
    Critical Parameters, Detailed Results, Anomaly Log, Certification.
    """

def _build_advanced_report(results: dict, preflight_status: dict,
                           timestamp: str) -> str:
    """
    Build the Advanced Timing Report markdown string.
    Sections: Header, Executive Summary (with pre-flight reference),
    Analysis Matrix, Findings, Detailed Results, Open Questions,
    Clock Metrology Summary, Certification.
    """


# ─── Public API ──────────────────────────────────────────────────

def generate_flight_reports(preflight_only=False, output_dir="reports"):
    """
    Main entry point. Generates both reports (or just pre-flight).

    1. Collect detailed results for ENGINE categories
    2. Build + save Pre-Flight Check report
    3. If not preflight_only:
       a. Collect detailed results for timing_analysis_advanced
       b. Build + save Advanced Timing Report (references pre-flight)
    4. Print summary to terminal

    Returns:
        dict with 'preflight_path', 'advanced_path', 'preflight_status'
    """

def generate_preflight_only(output_dir="reports"):
    """Convenience: just the pre-flight check."""
    return generate_flight_reports(preflight_only=True, output_dir=output_dir)
```

---

## Console Integration

### New Menu Option

Add option `[6] Generate Flight Reports` to the main menu:

```python
def show_main_menu():
    menu_1 = _gradient_text("[1] View Model Predictions")
    menu_2 = _gradient_text("[2] Run All Validation Tests")
    menu_3 = _gradient_text("[3] GFD Foundations (Why This Structure)")
    menu_4 = _gradient_text("[4] GFD Definitions")
    menu_5 = _gradient_text("[5] GFD Concepts (How Things Work)")
    menu_6 = _gradient_text("[6] Generate Flight Reports")        # NEW
    menu_q = _gradient_text("[q] Quit")
    ...
```

### Handler

```python
elif choice == '6':
    clear_screen()
    print_banner()
    print()
    print(f"  {_gradient_title('GENERATING FLIGHT REPORTS', C.GRADIENT_CYAN_GREEN)}")
    print_separator()
    print()

    from report_generator import generate_flight_reports

    def report_progress(phase, message):
        print(f"  {C.DIM}[{phase}] {message}{C.RESET}")

    result = generate_flight_reports(progress_callback=report_progress)

    print()
    print_separator("=")
    print(f"  Pre-Flight: {result['preflight_status']}")
    print(f"  Saved: {result['preflight_path']}")
    if result.get('advanced_path'):
        print(f"  Saved: {result['advanced_path']}")
    print_separator("=")

    input("\n  Press Enter to continue...")
```

### Auto-Generate After Run All Tests (Optional)

Could also auto-generate after `[2] Run All Validation Tests`:

```python
elif choice == '2':
    # ... existing run_all_tests_quick() ...
    display_quick_test_results(results)

    # Auto-generate reports
    print()
    print(f"  {C.DIM}Generating flight reports...{C.RESET}")
    from report_generator import generate_flight_reports
    report_result = generate_flight_reports()
    print(f"  {C.DIM}Reports saved to: {report_result['preflight_path']}{C.RESET}")
    if report_result.get('advanced_path'):
        print(f"  {C.DIM}                 {report_result['advanced_path']}{C.RESET}")
```

---

## Report File Naming & Storage

### Directory Structure

```
gfd_model_v2/
├── reports/                              ← NEW directory
│   ├── .gitkeep
│   ├── GFD-PFC-20260203-143022.md       ← Pre-Flight Check
│   ├── GFD-ATR-20260203-143022.md       ← Advanced Timing Report
│   ├── GFD-PFC-20260203-091500.md       ← Previous run
│   └── GFD-ATR-20260203-091500.md       ← Previous run
├── dfp_console.py
├── base.py
├── report_generator.py                   ← NEW file
└── ...
```

### Naming Convention

```
GFD-{TYPE}-{YYYYMMDD}-{HHMMSS}.md

TYPE:
  PFC = Pre-Flight Check
  ATR = Advanced Timing Report
```

### Report Cross-References

The Advanced Timing Report always references its Pre-Flight Check by document ID:

```
PREREQUISITE: GFD-PFC-20260203-143022 (Pre-Flight: GO)
```

This creates an audit trail. You can always find which pre-flight check a given
advanced analysis was based on.

---

## Category Mapping for Each Report

### Pre-Flight Check Includes:

```python
PREFLIGHT_CATEGORIES = [
    "system_mechanics",
    "timing_analysis",
    "theoretical_insights",
    "information_flow",
    "engine_stress_tests",
]
```

These are ALL categories with `'type': 'ENGINE'` in the CATEGORIES dict.
Simple rule: **if it's ENGINE, it's in the pre-flight check.**

### Advanced Timing Report Includes:

```python
ADVANCED_CATEGORIES = [
    "timing_analysis_advanced",
]
```

Just the one new category. Clean and focused.

### Future Extension

If you later add other `_advanced` categories (e.g., `information_flow_advanced`),
they could get their own reports or be folded into a general "Advanced Analysis Report."
The architecture supports both approaches.

---

## Severity Levels

For the Anomaly Log in the Pre-Flight report:

| Level | Condition | Meaning |
|-------|-----------|---------|
| **CRITICAL** | Test failed, error > 2× tolerance | Blocks GO decision |
| **WARNING** | Test failed, error ≤ 2× tolerance | Blocks GO, but marginal |
| **ADVISORY** | Test passed, but error > 50% of tolerance | Worth monitoring |
| **INFO** | Test has no observation (model-only) | Documented, not judged |

GO/NO-GO rule: **Any CRITICAL or WARNING → NO-GO.** Advisory items are noted
but do not block.

---

## Implementation Phases

### Phase A — Foundation (Build with Pre-Flight only)
1. Create `report_generator.py` with `_collect_detailed_results()` and `_build_preflight_report()`
2. Create `reports/` directory
3. Add `[6] Generate Flight Reports` to console menu
4. Test with existing engine categories

### Phase B — Advanced Report
1. Add `_build_advanced_report()` with findings extraction
2. Wire up `timing_analysis_advanced` category
3. Add cross-reference to pre-flight report ID

### Phase C — Polish
1. Auto-generate after `[2] Run All Tests`
2. Add `--report` CLI flag for headless execution
3. Optional: HTML version with embedded charts (spectral plots, etc.)
4. Optional: Report comparison tool (diff two reports to see what changed)

---

## Summary

| Deliverable | File | Purpose |
|-------------|------|---------|
| `report_generator.py` | New module | Generates both report types |
| `reports/` | New directory | Stores timestamped reports |
| `dfp_console.py` changes | Menu option `[6]` | User-facing trigger |
| Pre-Flight Check | `GFD-PFC-*.md` | GO/NO-GO for all ENGINE tests |
| Advanced Timing Report | `GFD-ATR-*.md` | Science findings from advanced timing |

The pre-flight check runs ~187 tests across 5 ENGINE categories.
The advanced report runs ~42 tests across 1 category.
Both save as timestamped markdown with cross-references.
Together they form a complete audit trail for every validation run.
