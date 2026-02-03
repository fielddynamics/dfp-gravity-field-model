"""Quick test runner."""
import sys
sys.path.insert(0, '.')
from dfp_console import run_all_tests_quick
results = run_all_tests_quick()
print(f"\nResults:")
print(f"  Passed: {results['total_passed']}/{results['total']}")
print(f"  Failed: {results['total_failed']}")
print(f"  Errors: {results['total_errors']}")
print(f"\nBy category:")
for cat, data in results['by_category'].items():
    passed = data.get('passed', 0)
    total = data.get('total', 0)
    failed = data.get('failed', 0)
    errors = data.get('errors', 0)
    status = "PASS" if failed == 0 and errors == 0 else "FAIL"
    print(f"  [{status}] {cat}: {passed}/{total}")
