"""Debug specific test failures."""
import sys
import traceback
sys.path.insert(0, '.')

from dfp_console import CATEGORIES

# Categories with failures
failing_cats = ['core_geometry', 'traversal_engine', 'timing_analysis', 
                'information_theory', 'stellar_mechanics', 'emergent_constants']

print("=" * 80)
print("DETAILED FAILURE ANALYSIS")
print("=" * 80)

for cat_name in failing_cats:
    cat_data = CATEGORIES.get(cat_name, {})
    print(f"\n{'='*60}")
    print(f"{cat_name.upper()}")
    print(f"{'='*60}")
    
    for module_path in cat_data.get('modules', []):
        try:
            module = __import__(module_path, fromlist=['ALL_TESTS'])
            if hasattr(module, 'ALL_TESTS'):
                for test_class in module.ALL_TESTS:
                    try:
                        test = test_class()
                        result = test.run()
                        if hasattr(result, 'passed'):
                            passed = result.passed
                        else:
                            passed = result.get('passed', False)
                        
                        if not passed:
                            print(f"\nFAIL: {module_path.split('.')[-1]}.{test_class.__name__}")
                            if hasattr(result, 'error') and result.error:
                                print(f"  Error: {result.error}")
                            elif isinstance(result, dict) and result.get('error'):
                                print(f"  Error: {result.get('error')}")
                            if hasattr(result, 'deviations'):
                                for k, v in result.deviations.items():
                                    print(f"  Deviation: {k} = {v}")
                    except Exception as e:
                        print(f"\nERROR: {module_path.split('.')[-1]}.{test_class.__name__}")
                        print(f"  {type(e).__name__}: {str(e)[:200]}")
        except ImportError as e:
            print(f"\nIMPORT ERROR: {module_path.split('.')[-1]}")
            print(f"  {str(e)[:200]}")
        except Exception as e:
            print(f"\nERROR loading {module_path}: {type(e).__name__}: {str(e)[:100]}")
