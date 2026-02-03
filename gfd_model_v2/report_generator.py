"""
GFD Report Generator
====================

Generates NASA/CERN-style validation reports from GFDTest results.

Reports:
  1. Pre-Flight Check (PFC) — All ENGINE categories → GO/NO-GO decision
  2. Advanced Timing Report (ATR) — timing_analysis_advanced → Science findings

Usage:
    from report_generator import generate_flight_reports

    # Generate both reports
    result = generate_flight_reports()

    # Pre-flight only
    result = generate_flight_reports(preflight_only=True)

    # Custom output directory
    result = generate_flight_reports(output_dir="my_reports")

Output:
    reports/GFD-PFC-{YYYYMMDD}-{HHMMSS}.md  — Pre-Flight Check
    reports/GFD-ATR-{YYYYMMDD}-{HHMMSS}.md  — Advanced Timing Report

The ATR always cross-references its PFC by document ID.
"""

import sys
import os
import io
import platform
import importlib
from datetime import datetime, timezone
from contextlib import redirect_stdout, redirect_stderr

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from base import GFDTest, TestResult, GroupResult


# =============================================================================
# CONFIGURATION
# =============================================================================

# Categories included in the Pre-Flight Check (all ENGINE types)
PREFLIGHT_CATEGORIES = [
    "system_mechanics",
    "timing_analysis",
    "theoretical_insights",
    "information_flow",
    "engine_stress_tests",
]

# Categories included in the Advanced Timing Report
ADVANCED_CATEGORIES = [
    "timing_analysis_advanced",
]

# Severity thresholds
SEVERITY_CRITICAL = 2.0   # error > 2× tolerance
SEVERITY_WARNING = 1.0    # error > 1× tolerance (test failed)
SEVERITY_ADVISORY = 0.5   # error > 50% of tolerance (passed but marginal)


# =============================================================================
# DATA COLLECTION
# =============================================================================

def _get_categories():
    """Import CATEGORIES from dfp_console without triggering interactive mode."""
    # We import just the CATEGORIES dict, not the whole console
    try:
        from dfp_console import CATEGORIES
        return CATEGORIES
    except ImportError:
        print("  [ERROR] Cannot import CATEGORIES from dfp_console.py")
        return {}


def _collect_detailed_results(category_keys, progress_callback=None):
    """
    Run specified categories silently, return full TestResult objects.

    This is the data collection pass for reports. It runs each test class
    and preserves the full TestResult (model values, observations, errors,
    derivations, commentary) rather than just counting pass/fail.

    Args:
        category_keys: List of category keys to run (e.g., ['system_mechanics', ...])
        progress_callback: Optional fn(phase, message) for progress updates

    Returns:
        dict: {
            'category_key': {
                'name': str,
                'type': str,
                'description': str,
                'modules': {
                    'module_path': {
                        'name': str,
                        'tests': [TestResult, ...],
                        'passed': int,
                        'failed': int,
                        'errors': int,
                    }
                },
                'total_passed': int,
                'total_failed': int,
                'total_errors': int,
                'total_tests': int,
            }
        }
    """
    CATEGORIES = _get_categories()
    results = {}

    for cat_key in category_keys:
        if cat_key not in CATEGORIES:
            continue

        cat_info = CATEGORIES[cat_key]

        if progress_callback:
            progress_callback("COLLECT", f"Running {cat_info['name']}...")

        cat_result = {
            'name': cat_info['name'],
            'type': cat_info['type'],
            'description': cat_info['description'],
            'modules': {},
            'total_passed': 0,
            'total_failed': 0,
            'total_errors': 0,
            'total_tests': 0,
        }

        for module_path in cat_info['modules']:
            mod_result = {
                'name': module_path.split('.')[-1].replace('test_', '').replace('_', ' ').title(),
                'tests': [],
                'passed': 0,
                'failed': 0,
                'errors': 0,
            }

            try:
                module = importlib.import_module(module_path)

                if hasattr(module, 'ALL_TESTS'):
                    for test_class in module.ALL_TESTS:
                        try:
                            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                                test = test_class()
                                result = test.run()

                            mod_result['tests'].append(result)
                            if result.passed:
                                mod_result['passed'] += 1
                            else:
                                mod_result['failed'] += 1
                        except Exception as e:
                            mod_result['errors'] += 1

            except Exception as e:
                mod_result['errors'] += 1

            cat_result['modules'][module_path] = mod_result
            cat_result['total_passed'] += mod_result['passed']
            cat_result['total_failed'] += mod_result['failed']
            cat_result['total_errors'] += mod_result['errors']
            cat_result['total_tests'] += (
                mod_result['passed'] + mod_result['failed'] + mod_result['errors']
            )

        results[cat_key] = cat_result

    return results


# =============================================================================
# ANALYSIS HELPERS
# =============================================================================

def _classify_anomaly(error, tolerance):
    """Classify anomaly severity based on error vs tolerance ratio."""
    if error is None:
        return "INFO"
    ratio = error / tolerance if tolerance > 0 else float('inf')
    if ratio > SEVERITY_CRITICAL:
        return "CRITICAL"
    elif ratio > SEVERITY_WARNING:
        return "WARNING"
    elif ratio > SEVERITY_ADVISORY:
        return "ADVISORY"
    return None  # Not anomalous


def _identify_anomalies(results):
    """
    Find all failed tests or tests with error > 50% of tolerance.

    Returns:
        list of dicts: [{
            'id': 'A-1',
            'test_name': str,
            'subsystem': str,
            'error': float or None,
            'tolerance': float,
            'severity': 'CRITICAL' | 'WARNING' | 'ADVISORY' | 'INFO',
        }]
    """
    anomalies = []
    counter = 1

    for cat_key, cat_data in results.items():
        for mod_path, mod_data in cat_data['modules'].items():
            for test_result in mod_data['tests']:
                # Check each comparison within the test
                for item, model, ref, error, passed in test_result.comparisons:
                    severity = _classify_anomaly(error, test_result.tolerance)
                    if severity:
                        anomalies.append({
                            'id': f"A-{counter}",
                            'test_name': f"{test_result.name}: {item}",
                            'subsystem': cat_data['name'],
                            'error': error,
                            'tolerance': test_result.tolerance,
                            'severity': severity,
                        })
                        counter += 1

    return anomalies


def _compute_go_nogo(results):
    """
    Determine GO/NO-GO status.
    NO-GO if any CRITICAL or WARNING anomalies exist.

    Returns:
        tuple: (status_str, is_go)
    """
    anomalies = _identify_anomalies(results)
    blocking = [a for a in anomalies if a['severity'] in ('CRITICAL', 'WARNING')]

    if not blocking:
        return "GO", True
    else:
        return "NO-GO", False


# =============================================================================
# REPORT FORMATTERS
# =============================================================================

def _header_block(title, doc_id):
    """Generate the report header block."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  {title}")
    lines.append(f"  Document: {doc_id}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  CLASSIFICATION:  Internal — GFD Model Validation")
    lines.append(f"  GENERATED:       {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"  FRAMEWORK:       GFD Model V2")
    lines.append(f"  PYTHON:          {platform.python_version()}")
    lines.append(f"  PLATFORM:        {platform.system()} {platform.release()}")
    lines.append("")
    return "\n".join(lines)


def _separator():
    """Horizontal rule."""
    return "-" * 70


def _go_nogo_matrix(results):
    """Build the GO/NO-GO matrix table."""
    lines = []
    lines.append("")
    lines.append("  GO/NO-GO MATRIX")
    lines.append("  " + _separator())
    lines.append("")

    # Table header
    lines.append(f"  {'Subsystem':<32} {'Tests':>7} {'Pass':>7} {'Status':>10}")
    lines.append(f"  {'-'*32} {'-'*7} {'-'*7} {'-'*10}")

    total_tests = 0
    total_passed = 0

    for cat_key, cat_data in results.items():
        t = cat_data['total_tests']
        p = cat_data['total_passed']
        total_tests += t
        total_passed += p

        status = "GO" if cat_data['total_failed'] == 0 and cat_data['total_errors'] == 0 else "NO-GO"
        lines.append(f"  {cat_data['name']:<32} {t:>7} {p:>7} {status:>10}")

    lines.append(f"  {'-'*32} {'-'*7} {'-'*7} {'-'*10}")

    overall_status, _ = _compute_go_nogo(results)
    lines.append(f"  {'TOTAL':<32} {total_tests:>7} {total_passed:>7} {overall_status:>10}")
    lines.append("")

    return "\n".join(lines)


def _detailed_results_section(results):
    """Build the detailed test results tables per subsystem."""
    lines = []
    section_num = 1

    for cat_key, cat_data in results.items():
        p = cat_data['total_passed']
        t = cat_data['total_tests']
        lines.append("")
        lines.append(f"  {section_num}. {cat_data['name'].upper()}  [{p}/{t} PASS]")
        lines.append("  " + "-" * 50)

        for mod_path, mod_data in cat_data['modules'].items():
            if not mod_data['tests']:
                continue

            lines.append("")
            lines.append(f"    Module: {mod_data['name']}")
            lines.append(f"    {'Test':<35} {'Model':>12} {'Observed':>12} {'Error':>8} {'Status':>8}")
            lines.append(f"    {'-'*35} {'-'*12} {'-'*12} {'-'*8} {'-'*8}")

            for test_result in mod_data['tests']:
                for item, model, ref, error, passed in test_result.comparisons:
                    status = "PASS" if passed else "FAIL"
                    model_str = f"{model:.6g}" if model is not None else "--"
                    ref_str = f"{ref:.6g}" if ref is not None else "--"
                    error_str = f"{error:.2%}" if error is not None else "--"

                    # Truncate long test names
                    display_name = f"{test_result.name}: {item}"
                    if len(display_name) > 35:
                        display_name = display_name[:32] + "..."

                    lines.append(
                        f"    {display_name:<35} {model_str:>12} {ref_str:>12} "
                        f"{error_str:>8} {status:>8}"
                    )

        section_num += 1

    return "\n".join(lines)


def _anomaly_log(anomalies):
    """Build the anomaly log section."""
    lines = []
    lines.append("")
    lines.append("  ANOMALY LOG")
    lines.append("  " + _separator())
    lines.append("")

    if not anomalies:
        lines.append("  No anomalies detected.")
    else:
        lines.append(f"  {'ID':<6} {'Test':<30} {'Subsystem':<18} {'Error':>8} {'Severity':>10}")
        lines.append(f"  {'-'*6} {'-'*30} {'-'*18} {'-'*8} {'-'*10}")

        for a in anomalies:
            name = a['test_name'][:30] if len(a['test_name']) > 30 else a['test_name']
            err = f"{a['error']:.2%}" if a['error'] is not None else "--"
            lines.append(
                f"  {a['id']:<6} {name:<30} {a['subsystem']:<18} {err:>8} {a['severity']:>10}"
            )

    lines.append("")
    return "\n".join(lines)


# =============================================================================
# REPORT BUILDERS
# =============================================================================

def _build_preflight_report(results, timestamp):
    """
    Build the Pre-Flight Check markdown report.

    Sections:
        1. Header
        2. Executive Summary (GO/NO-GO, total counts)
        3. GO/NO-GO Matrix (per subsystem)
        4. Detailed Results (per module, per test)
        5. Anomaly Log
        6. Certification

    Args:
        results: Output from _collect_detailed_results()
        timestamp: str, YYYYMMDD-HHMMSS format

    Returns:
        tuple: (report_text, doc_id, is_go)
    """
    doc_id = f"GFD-PFC-{timestamp}"

    total_tests = sum(c['total_tests'] for c in results.values())
    total_passed = sum(c['total_passed'] for c in results.values())
    total_failed = sum(c['total_failed'] for c in results.values())

    overall_status, is_go = _compute_go_nogo(results)
    anomalies = _identify_anomalies(results)

    max_error = 0.0
    for cat_data in results.values():
        for mod_data in cat_data['modules'].values():
            for test_result in mod_data['tests']:
                if test_result.max_error > max_error:
                    max_error = test_result.max_error

    # Build report
    sections = []

    # Header
    sections.append(_header_block("GFD ENGINE PRE-FLIGHT CHECK", doc_id))
    sections.append(_separator())

    # Executive Summary
    sections.append("")
    sections.append("  EXECUTIVE SUMMARY")
    sections.append("  " + _separator())
    sections.append("")
    sections.append(f"  STATUS:      {overall_status}")
    sections.append(f"  TESTS:       {total_passed}/{total_tests} PASSED")
    sections.append(f"  FAILURES:    {total_failed}")
    sections.append(f"  ANOMALIES:   {len(anomalies)}")
    sections.append(f"  MAX ERROR:   {max_error:.4%}")
    sections.append("")

    if is_go:
        sections.append("  DECISION: ALL SUBSYSTEMS GO. ENGINE CLEARED FOR OPERATION.")
    else:
        blocking = [a for a in anomalies if a['severity'] in ('CRITICAL', 'WARNING')]
        sections.append(f"  DECISION: NO-GO. {len(blocking)} blocking anomalies detected.")
    sections.append("")

    # GO/NO-GO Matrix
    sections.append(_separator())
    sections.append(_go_nogo_matrix(results))

    # Detailed Results
    sections.append(_separator())
    sections.append("")
    sections.append("  DETAILED RESULTS BY SUBSYSTEM")
    sections.append("  " + _separator())
    sections.append(_detailed_results_section(results))

    # Anomaly Log
    sections.append(_separator())
    sections.append(_anomaly_log(anomalies))

    # Certification
    sections.append(_separator())
    sections.append("")
    sections.append("  CERTIFICATION")
    sections.append("  " + _separator())
    sections.append("")
    sections.append("  This report was generated automatically by the GFD Engine")
    sections.append("  Pre-Flight Check system. All tests executed against the current")
    sections.append("  codebase with no manual intervention.")
    sections.append("")
    sections.append(f"  Generated:  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    sections.append(f"  Report ID:  {doc_id}")
    sections.append("")
    sections.append(_separator())
    sections.append("  END OF REPORT")
    sections.append(_separator())

    return "\n".join(sections), doc_id, is_go


def _build_advanced_report(results, preflight_doc_id, preflight_is_go, timestamp):
    """
    Build the Advanced Timing Analysis Report.

    Sections:
        1. Header
        2. Executive Summary (with pre-flight cross-reference)
        3. Pre-Flight Reference
        4. Analysis Matrix
        5. Detailed Results
        6. Anomaly Log
        7. Certification

    Args:
        results: Output from _collect_detailed_results() for advanced categories
        preflight_doc_id: str, the PFC document ID for cross-reference
        preflight_is_go: bool, whether pre-flight passed
        timestamp: str, YYYYMMDD-HHMMSS format

    Returns:
        tuple: (report_text, doc_id)
    """
    doc_id = f"GFD-ATR-{timestamp}"

    total_tests = sum(c['total_tests'] for c in results.values())
    total_passed = sum(c['total_passed'] for c in results.values())
    anomalies = _identify_anomalies(results)

    # Build report
    sections = []

    # Header
    sections.append(_header_block("GFD ADVANCED TIMING ANALYSIS REPORT", doc_id))
    sections.append(_separator())

    # Executive Summary
    sections.append("")
    sections.append("  EXECUTIVE SUMMARY")
    sections.append("  " + _separator())
    sections.append("")
    pfc_status = "GO" if preflight_is_go else "NO-GO"
    sections.append(f"  PRE-FLIGHT STATUS:  {pfc_status} ({preflight_doc_id})")
    sections.append(f"  ADVANCED TESTS:     {total_passed}/{total_tests} COMPLETED")
    sections.append(f"  ANOMALIES:          {len(anomalies)}")
    sections.append("")

    if not preflight_is_go:
        sections.append("  WARNING: Pre-flight check did not pass. Advanced results")
        sections.append("  should be interpreted with caution.")
        sections.append("")

    # Analysis Matrix
    sections.append(_separator())
    sections.append("")
    sections.append("  ANALYSIS MATRIX")
    sections.append("  " + _separator())
    sections.append("")
    sections.append(f"  {'Analysis Domain':<32} {'Tests':>7} {'Pass':>7} {'Status':>10}")
    sections.append(f"  {'-'*32} {'-'*7} {'-'*7} {'-'*10}")

    for cat_key, cat_data in results.items():
        t = cat_data['total_tests']
        p = cat_data['total_passed']
        status = "COMPLETE" if p == t else "PARTIAL"
        sections.append(f"  {cat_data['name']:<32} {t:>7} {p:>7} {status:>10}")

    sections.append("")

    # Detailed Results
    sections.append(_separator())
    sections.append("")
    sections.append("  DETAILED RESULTS")
    sections.append("  " + _separator())
    sections.append(_detailed_results_section(results))

    # Anomaly Log
    sections.append(_separator())
    sections.append(_anomaly_log(anomalies))

    # Certification
    sections.append(_separator())
    sections.append("")
    sections.append("  CERTIFICATION")
    sections.append("  " + _separator())
    sections.append("")
    sections.append("  This report was generated automatically by the GFD Advanced")
    sections.append("  Timing Analysis system.")
    sections.append("")
    sections.append(f"  Generated:   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    sections.append(f"  Depends on:  {preflight_doc_id}")
    sections.append(f"  Report ID:   {doc_id}")
    sections.append("")
    sections.append(_separator())
    sections.append("  END OF REPORT")
    sections.append(_separator())

    return "\n".join(sections), doc_id


# =============================================================================
# PUBLIC API
# =============================================================================

def generate_flight_reports(preflight_only=False, output_dir=None, progress_callback=None):
    """
    Main entry point. Generates Pre-Flight Check and (optionally) Advanced
    Timing Report.

    1. Collect detailed results for ENGINE categories
    2. Build + save Pre-Flight Check report
    3. If not preflight_only and advanced categories exist:
       a. Collect detailed results for timing_analysis_advanced
       b. Build + save Advanced Timing Report (references pre-flight)
    4. Print summary to terminal

    Args:
        preflight_only: bool, if True skip advanced report
        output_dir: str, override default reports/ directory
        progress_callback: fn(phase, message) for progress updates

    Returns:
        dict: {
            'preflight_path': str,
            'preflight_status': 'GO' | 'NO-GO',
            'preflight_doc_id': str,
            'advanced_path': str or None,
            'advanced_doc_id': str or None,
            'timestamp': str,
        }
    """
    # Resolve output directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

    os.makedirs(output_dir, exist_ok=True)

    # Timestamp for both reports
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d-%H%M%S")

    # --- Pre-Flight Check ---
    if progress_callback:
        progress_callback("PFC", "Collecting engine test results...")

    preflight_results = _collect_detailed_results(PREFLIGHT_CATEGORIES, progress_callback)

    if progress_callback:
        progress_callback("PFC", "Building Pre-Flight Check report...")

    preflight_text, preflight_doc_id, is_go = _build_preflight_report(
        preflight_results, timestamp
    )

    preflight_path = os.path.join(output_dir, f"{preflight_doc_id}.md")
    with open(preflight_path, 'w') as f:
        f.write(preflight_text)

    if progress_callback:
        status = "GO" if is_go else "NO-GO"
        progress_callback("PFC", f"Pre-Flight Check: {status} → {preflight_path}")

    result = {
        'preflight_path': preflight_path,
        'preflight_status': "GO" if is_go else "NO-GO",
        'preflight_doc_id': preflight_doc_id,
        'advanced_path': None,
        'advanced_doc_id': None,
        'timestamp': timestamp,
    }

    # --- Advanced Timing Report ---
    if not preflight_only:
        CATEGORIES = _get_categories()
        # Only generate if advanced categories are registered
        advanced_cats = [c for c in ADVANCED_CATEGORIES if c in CATEGORIES]

        if advanced_cats:
            if progress_callback:
                progress_callback("ATR", "Collecting advanced timing results...")

            advanced_results = _collect_detailed_results(advanced_cats, progress_callback)

            if progress_callback:
                progress_callback("ATR", "Building Advanced Timing Report...")

            advanced_text, advanced_doc_id = _build_advanced_report(
                advanced_results, preflight_doc_id, is_go, timestamp
            )

            advanced_path = os.path.join(output_dir, f"{advanced_doc_id}.md")
            with open(advanced_path, 'w') as f:
                f.write(advanced_text)

            result['advanced_path'] = advanced_path
            result['advanced_doc_id'] = advanced_doc_id

            if progress_callback:
                progress_callback("ATR", f"Advanced Timing Report → {advanced_path}")
        else:
            if progress_callback:
                progress_callback("ATR", "No advanced timing categories registered yet — skipping.")

    return result


def generate_preflight_only(output_dir=None):
    """Convenience: just the pre-flight check."""
    return generate_flight_reports(preflight_only=True, output_dir=output_dir)


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    """Allow running directly: python report_generator.py [--preflight-only]"""
    preflight_only = "--preflight-only" in sys.argv

    def _cli_progress(phase, message):
        print(f"  [{phase}] {message}")

    print()
    print("  GFD Report Generator")
    print("  " + "=" * 50)
    print()

    result = generate_flight_reports(
        preflight_only=preflight_only,
        progress_callback=_cli_progress
    )

    print()
    print("  " + "=" * 50)
    print(f"  Pre-Flight: {result['preflight_status']}")
    print(f"  Saved:      {result['preflight_path']}")
    if result['advanced_path']:
        print(f"  Saved:      {result['advanced_path']}")
    print()
