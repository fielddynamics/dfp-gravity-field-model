#!/usr/bin/env python
"""
GFD Model Test Runner
=====================

Run individual tests or test files easily.

Usage:
    python -m gfd_model_v2.run_test TestClassName
    python -m gfd_model_v2.run_test TestClassName --from file_path.py
    python -m gfd_model_v2.run_test --list                    # List all available tests
    python -m gfd_model_v2.run_test --list valence            # Search tests by name

Examples:
    python -m gfd_model_v2.run_test CarbonTetravalence
    python -m gfd_model_v2.run_test BohrRadiusIdentity
    python -m gfd_model_v2.run_test --list carbon
"""

import sys
import os
import argparse
import importlib.util
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gfd_model_v2.framework import run_tests, Test


def discover_tests(calculations_dir: Path) -> dict:
    """Discover all test classes in the calculations directory."""
    tests = {}
    
    for py_file in calculations_dir.rglob("test_*.py"):
        rel_path = py_file.relative_to(PROJECT_ROOT)
        module_path = str(rel_path).replace(os.sep, ".").replace(".py", "")
        
        try:
            spec = importlib.util.spec_from_file_location(module_path, py_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_path] = module
            spec.loader.exec_module(module)
            
            # Find all Test subclasses in the module
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, Test) and 
                    obj is not Test and
                    hasattr(obj, 'name')):
                    tests[name] = {
                        'class': obj,
                        'file': str(rel_path),
                        'display_name': getattr(obj, 'name', name),
                        'level': getattr(obj, 'level', None),
                    }
        except Exception as e:
            # Skip files that fail to import
            pass
    
    return tests


def list_tests(tests: dict, search: str = None):
    """Print available tests, optionally filtered by search term."""
    print("\nAvailable Tests")
    print("=" * 60)
    
    # Group by file
    by_file = {}
    for name, info in tests.items():
        file = info['file']
        if file not in by_file:
            by_file[file] = []
        by_file[file].append((name, info))
    
    count = 0
    for file in sorted(by_file.keys()):
        file_tests = by_file[file]
        
        # Filter if search term provided
        if search:
            file_tests = [(n, i) for n, i in file_tests 
                         if search.lower() in n.lower() or 
                            search.lower() in i['display_name'].lower()]
        
        if not file_tests:
            continue
            
        print(f"\n{file}")
        print("-" * 60)
        
        for name, info in sorted(file_tests, key=lambda x: x[0]):
            level = info['level']
            level_str = f"[{level.name}]" if level else ""
            print(f"  {name:40} {level_str}")
            count += 1
    
    print(f"\n{count} tests found")
    print("\nRun a test with:")
    print("  python -m gfd_model_v2.run_test <TestClassName>")


def run_single_test(test_class, test_name: str):
    """Run a single test class."""
    display_name = getattr(test_class, 'name', test_name)
    
    return run_tests(
        title=display_name,
        summary=f"Running individual test: {test_name}",
        test_classes=[test_class]
    )


def main():
    parser = argparse.ArgumentParser(
        description="GFD Model Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m gfd_model_v2.run_test CarbonTetravalence
  python -m gfd_model_v2.run_test BohrRadiusIdentity
  python -m gfd_model_v2.run_test --list
  python -m gfd_model_v2.run_test --list carbon
        """
    )
    
    parser.add_argument(
        "test_name",
        nargs="?",
        help="Name of the test class to run (e.g., CarbonTetravalence)"
    )
    
    parser.add_argument(
        "--list", "-l",
        nargs="?",
        const="",
        metavar="SEARCH",
        help="List available tests, optionally filtered by search term"
    )
    
    args = parser.parse_args()
    
    # Discover all tests from multiple directories
    tests = {}
    for subdir in ["calculations", "engine_core"]:
        search_dir = PROJECT_ROOT / "gfd_model_v2" / subdir
        if search_dir.exists():
            tests.update(discover_tests(search_dir))
    
    # List mode
    if args.list is not None:
        list_tests(tests, args.list if args.list else None)
        return 0
    
    # Run mode - need a test name
    if not args.test_name:
        parser.print_help()
        return 1
    
    # Find the test
    if args.test_name not in tests:
        # Try case-insensitive match
        matches = [n for n in tests if n.lower() == args.test_name.lower()]
        if matches:
            args.test_name = matches[0]
        else:
            # Try partial match
            matches = [n for n in tests if args.test_name.lower() in n.lower()]
            if len(matches) == 1:
                args.test_name = matches[0]
            elif len(matches) > 1:
                print(f"Multiple tests match '{args.test_name}':")
                for m in matches:
                    print(f"  {m}")
                return 1
            else:
                print(f"Test '{args.test_name}' not found.")
                print(f"Use --list to see available tests.")
                return 1
    
    test_info = tests[args.test_name]
    print(f"Running: {args.test_name}")
    print(f"From: {test_info['file']}")
    print()
    
    success = run_single_test(test_info['class'], args.test_name)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
