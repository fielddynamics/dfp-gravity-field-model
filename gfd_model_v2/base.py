"""
GFD Model V2 - Test Framework Base
===================================

All tests inherit from GFDTest and return structured data.
The Renderer handles all display.

Usage:
    class MyTest(GFDTest):
        name = "Test Name"
        question = "What are we testing?"
        reference_source = "Source (or None)"
        
        def model(self):
            return {"Metric": calculated_value}
        
        def observations(self):
            return {"Metric": reference_value}  # or None

Validated Function Export:
    @validated_function(
        equation="P(A) = BE(A) × (c / λ_C)",
        description="Power output per gravity field",
        inputs={"A": "int — Mass number"},
        outputs={"watts": "float — Power per field"},
        group="Stellar Power Output",
    )
    def power_per_field(A):
        ...

Dependency Injection:
    class MyDownstreamTest(GFDTest):
        depends_on = ["power_per_field"]
        
        def model(self):
            p = self.fn.power_per_field(56)
            ...
"""

import sys
import os
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple
from abc import ABC, abstractmethod

# Add parent paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# VALIDATED FUNCTION REGISTRY
# =============================================================================

_VALIDATED_REGISTRY = {}  # name -> function object with metadata


class ValidatedFunctionError(Exception):
    """Raised when a validated function contract is violated."""
    pass


def validated_function(*, equation, description, inputs, outputs, group=None):
    """
    Decorate a function as a validated export from a test module.
    
    CONTRACT — all four fields required. Omitting any raises at import time:
        equation:    str  — The mathematical formula
        description: str  — What this computes, in plain English
        inputs:      dict — {param_name: "type — description"}
        outputs:     dict — {output_name: "type — description"}
        group:       str  — (optional) Test group that validates this function
    
    The decorator:
        1. Validates the contract at decoration time (module won't import if incomplete)
        2. Attaches metadata to the function object
        3. Registers the function in the global registry
        4. Returns the function UNCHANGED — zero runtime overhead
    
    Usage:
        @validated_function(
            equation="P(A) = BE(A) × (c / λ_C)",
            description="Power output per gravity field from binding energy",
            inputs={"A": "int — Mass number (gravity field count in Tet B)"},
            outputs={"watts": "float — Power per gravity field in watts"},
            group="Stellar Power Output",
        )
        def power_per_field(A):
            be_mev = get_binding_energy(A)
            be_joules = be_mev * MEV_TO_JOULES
            return be_joules * F_CLOSURE
    """
    # Enforce contract at decoration time — fail fast
    missing = []
    if not equation:     missing.append("equation")
    if not description:  missing.append("description")
    if not inputs:       missing.append("inputs")
    if not outputs:      missing.append("outputs")
    
    if missing:
        raise ValidatedFunctionError(
            f"@validated_function missing required fields: {missing}. "
            f"Every validated function must define: equation, description, inputs, outputs."
        )
    
    def decorator(fn):
        # Attach metadata directly to function object
        fn._vf = True
        fn._vf_equation = equation
        fn._vf_description = description
        fn._vf_inputs = inputs
        fn._vf_outputs = outputs
        fn._vf_group = group
        fn._vf_qualname = fn.__qualname__
        
        # Register globally by function name
        _VALIDATED_REGISTRY[fn.__name__] = fn
        
        return fn  # Return UNCHANGED — no wrapper, no performance cost
    
    return decorator


def get_validated_function(name):
    """Look up a validated function by name. Raises if not found."""
    if name not in _VALIDATED_REGISTRY:
        available = list(_VALIDATED_REGISTRY.keys()) if _VALIDATED_REGISTRY else ["(none registered)"]
        raise ValidatedFunctionError(
            f"No validated function '{name}' registered. Available: {available}"
        )
    return _VALIDATED_REGISTRY[name]


def get_all_validated_functions():
    """Return the full registry for introspection and DAG generation."""
    return dict(_VALIDATED_REGISTRY)


class _FnProxy:
    """
    Proxy that enforces depends_on declarations on test classes.
    
    If a test tries to call self.fn.some_function without declaring
    it in depends_on, the proxy raises a clear error telling you
    exactly what to add.
    """
    def __init__(self, declared):
        object.__setattr__(self, '_declared', set(declared))
        object.__setattr__(self, '_cache', {})
    
    def __getattr__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        
        declared = object.__getattribute__(self, '_declared')
        cache = object.__getattribute__(self, '_cache')
        
        if name not in declared:
            raise ValidatedFunctionError(
                f"Function '{name}' not declared in depends_on. "
                f"Add it to your test class:\n"
                f"    depends_on = {sorted(declared | {name})}"
            )
        
        if name not in cache:
            cache[name] = get_validated_function(name)
        
        return cache[name]


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class TestResult:
    """Structured result from a single test."""
    name: str
    question: str
    model_values: Dict[str, float]
    observations: Optional[Dict[str, float]] = None
    reference_source: Optional[str] = None
    tolerance: float = 0.10
    derivation: Optional[str] = None  # How the model arrives at its values
    commentary: Optional[str] = None  # Academic reflection on the result
    table: Optional[Dict] = None  # Structured table data for display
    dependencies: Optional[List[Dict]] = None  # Resolved dependency metadata
    
    passed: bool = field(init=False)
    comparisons: List[Tuple[str, float, float, Optional[float], bool]] = field(init=False)
    max_error: float = field(init=False)
    pass_rate: float = field(init=False)
    
    def __post_init__(self):
        self.comparisons = []
        
        for item, model_val in self.model_values.items():
            if self.observations and item in self.observations:
                ref_val = self.observations[item]
                if ref_val != 0:
                    error = abs(model_val - ref_val) / abs(ref_val)
                else:
                    error = 0.0 if model_val == 0 else float('inf')
                item_passed = error <= self.tolerance
                self.comparisons.append((item, model_val, ref_val, error, item_passed))
            else:
                self.comparisons.append((item, model_val, None, None, True))
        
        errors = [c[3] for c in self.comparisons if c[3] is not None]
        self.max_error = max(errors) if errors else 0.0
        
        n_passed = sum(1 for c in self.comparisons if c[4])
        self.pass_rate = n_passed / len(self.comparisons) if self.comparisons else 1.0
        
        if self.observations:
            self.passed = self.max_error <= self.tolerance and self.pass_rate >= 0.95
        else:
            self.passed = True


@dataclass
class GroupResult:
    """Structured result from a test group."""
    title: str
    summary: str
    tests: List[TestResult] = field(default_factory=list)
    
    @property
    def passed(self) -> bool:
        return all(t.passed for t in self.tests)
    
    @property
    def pass_count(self) -> int:
        return sum(1 for t in self.tests if t.passed)
    
    @property
    def total_count(self) -> int:
        return len(self.tests)


# =============================================================================
# TEST BASE CLASS
# =============================================================================

class GFDTest(ABC):
    """
    Base class for GFD validation tests.
    
    Subclasses define:
        - name: Test name
        - question: What are we testing?
        - reference_source: Source of observations (or None)
        - tolerance: Acceptable error (default 10%)
        - derivation: How the model arrives at its values (or None)
        - commentary: Academic reflection on the result (or None)
        - table: Structured table data for display (or None)
        - depends_on: List of validated function names this test uses (or None)
        
    And implement:
        - model(): Returns dict of calculated values
        - observations(): Returns dict of reference values (or None)
    
    Dependency Injection:
        If depends_on is set, use self.fn to access validated functions:
        
        class MyTest(GFDTest):
            depends_on = ["power_per_field"]
            
            def model(self):
                p = self.fn.power_per_field(56)
                return {"Power": p}
    
    Table Format:
        table = {
            "title": "Table Title",
            "headers": ["Col1", "Col2", "Col3"],
            "rows": [
                ["row1col1", "row1col2", "row1col3"],
                ["row2col1", "row2col2", "row2col3"],
            ],
            "footer": "Optional footer text"
        }
    """
    name: str = "Unnamed Test"
    question: str = "What are we testing?"
    reference_source: Optional[str] = None
    tolerance: float = 0.10
    derivation: Optional[str] = None  # How the model arrives at its calculated values
    commentary: Optional[str] = None  # Academic reflection on what the result means
    table: Optional[Dict] = None  # Structured table data for display
    depends_on: Optional[List[str]] = None  # Validated functions this test uses
    
    @abstractmethod
    def model(self) -> Dict[str, float]:
        """Return model calculated values."""
        pass
    
    def observations(self) -> Optional[Dict[str, float]]:
        """Return reference observations (or None if no data)."""
        return None
    
    @property
    def fn(self):
        """
        Access validated functions declared in depends_on.
        
        Enforces that you can only call functions you've declared.
        Raises ValidatedFunctionError if you access an undeclared function.
        """
        if not hasattr(self, '_fn_proxy'):
            self._fn_proxy = _FnProxy(self.depends_on or [])
        return self._fn_proxy
    
    def run(self) -> TestResult:
        """Execute test and return structured result."""
        # Resolve dependency metadata for rendering
        dep_meta = None
        if self.depends_on:
            dep_meta = []
            for fn_name in self.depends_on:
                try:
                    fn = get_validated_function(fn_name)
                    dep_meta.append({
                        "name": fn_name,
                        "equation": fn._vf_equation,
                        "group": fn._vf_group,
                        "description": fn._vf_description,
                    })
                except ValidatedFunctionError:
                    dep_meta.append({
                        "name": fn_name,
                        "equation": "NOT REGISTERED",
                        "group": None,
                        "description": "Function not found in registry",
                    })
        
        return TestResult(
            name=self.name,
            question=self.question,
            model_values=self.model(),
            observations=self.observations(),
            reference_source=self.reference_source,
            tolerance=self.tolerance,
            derivation=self.derivation,
            commentary=self.commentary,
            table=self.table,
            dependencies=dep_meta,
        )


# =============================================================================
# RENDERER
# =============================================================================

class C:
    """Colors for terminal output."""
    BLUE = '\033[38;5;39m'
    CYAN = '\033[38;5;44m'
    GREEN = '\033[38;5;46m'
    RED = '\033[38;5;196m'
    YELLOW = '\033[38;5;226m'
    DIM = '\033[38;5;245m'
    RESET = '\033[0m'
    GRADIENT = [
        '\033[38;5;93m', '\033[38;5;99m', '\033[38;5;63m', '\033[38;5;69m',
        '\033[38;5;33m', '\033[38;5;39m', '\033[38;5;44m', '\033[38;5;49m',
    ]


def _color_enabled():
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            return False
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


USE_COLOR = _color_enabled()


def _c(color, text):
    return f"{color}{text}{C.RESET}" if USE_COLOR else text


def _gradient(text):
    if not USE_COLOR:
        return text
    result = []
    colors = C.GRADIENT
    text = text.strip()
    for i, char in enumerate(text):
        if char == ' ':
            result.append(char)
        else:
            color_idx = int(i * len(colors) / len(text.replace(' ', '')))
            color_idx = min(color_idx, len(colors) - 1)
            result.append(f"{colors[color_idx]}{char}")
    return ''.join(result) + C.RESET


def _fmt(v):
    if v is None:
        return "--"
    if abs(v) >= 1e6 or (abs(v) < 0.001 and v != 0):
        return f"{v:.3e}"
    elif v == int(v):
        return f"{int(v)}"
    return f"{v:.6f}"


def _wrap_text(text, width=70, indent="  "):
    words = text.split()
    lines = []
    line = indent
    for word in words:
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = indent + word
        else:
            line = line + " " + word if line != indent else indent + word
    if line.strip():
        lines.append(line)
    return "\n".join(lines)


class Renderer:
    """Renders test results to terminal."""
    
    @staticmethod
    def render_table(table_data: Dict, indent: str = "    "):
        """
        Render a structured table.
        
        Table format:
            {
                "title": "Optional Title",
                "headers": ["Col1", "Col2", ...],
                "rows": [["r1c1", "r1c2", ...], ...],
                "footer": "Optional footer"
            }
        """
        if not table_data:
            return
        
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        title = table_data.get("title")
        footer = table_data.get("footer")
        
        if not headers or not rows:
            return
        
        # Calculate column widths
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Build separator
        sep = indent + "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        
        # Print title if present
        if title:
            print()
            print(_c(C.CYAN, f"{indent}{title}"))
        
        # Print top border
        print(sep)
        
        # Print headers
        header_row = indent + "|"
        for i, h in enumerate(headers):
            header_row += f" {str(h):^{col_widths[i]}} |"
        print(_c(C.DIM, header_row))
        
        # Print header separator
        print(sep)
        
        # Print rows
        for row in rows:
            row_str = indent + "|"
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    cell_str = str(cell)
                    # Right-align numbers, left-align text
                    if isinstance(cell, (int, float)):
                        row_str += f" {cell_str:>{col_widths[i]}} |"
                    else:
                        row_str += f" {cell_str:<{col_widths[i]}} |"
            print(row_str)
        
        # Print bottom border
        print(sep)
        
        # Print footer if present
        if footer:
            print(_c(C.DIM, f"{indent}{footer}"))
        print()
    
    @staticmethod
    def render_group(group: GroupResult):
        print()
        print(f"  {_gradient(group.title.upper())}")
        print(_c(C.DIM, "  " + "-" * 60))
        print()
        print(_wrap_text(group.summary))
        print()
        
        for test in group.tests:
            Renderer.render_test(test)
        
        print(_c(C.DIM, "  " + "-" * 60))
        if group.passed:
            print(_c(C.GREEN, f"  {group.pass_count}/{group.total_count} tests passed"))
        else:
            print(_c(C.RED, f"  {group.pass_count}/{group.total_count} tests passed"))
        print()
    
    @staticmethod
    def render_test(result: TestResult):
        print(_c(C.BLUE, f"  {result.name.upper()}"))
        print(_c(C.DIM, "  " + "-" * 60))
        print()
        
        # Dependencies — show chain before the question
        if result.dependencies:
            print(_c(C.YELLOW, "  Depends On"))
            for dep in result.dependencies:
                src = f" ({dep['group']})" if dep.get('group') else ""
                print(_c(C.DIM, f"    \u2190 {dep['name']}{src}"))
                print(_c(C.DIM, f"      {dep['equation']}"))
            print()
        
        print(f"  {result.question}")
        print()
        
        # Derivation (how the model arrives at its values)
        print(_c(C.CYAN, "  Derivation"))
        if result.derivation:
            print(_wrap_text(result.derivation, width=70, indent="    "))
        else:
            print(_c(C.DIM, "    None"))
        print()
        
        # GFD Model
        print(_c(C.CYAN, "  GFD Model"))
        
        # Table (if present) - shows detailed model predictions
        if result.table:
            Renderer.render_table(result.table, indent="    ")
        for item, val in result.model_values.items():
            print(f"    {item:<35} {_fmt(val):>15}")
        print()
        
        # Observations
        if result.reference_source:
            print(_c(C.CYAN, "  Observations") + _c(C.DIM, f"  ({result.reference_source})"))
            for item, _, ref, _, _ in result.comparisons:
                print(f"    {item:<35} {_fmt(ref):>15}")
        else:
            print(_c(C.CYAN, "  Observations"))
            print(_c(C.DIM, "    None"))
        print()
        
        # Comparison
        if result.reference_source:
            print(_c(C.CYAN, "  Comparison"))
            print(_c(C.DIM, f"    {'Item':<28} {'Model':>12} {'Observed':>12} {'Error':>9}"))
            for item, model, ref, error, passed in result.comparisons:
                status = _c(C.GREEN, "OK") if passed else _c(C.RED, "FAIL")
                error_str = f"{error:.2%}" if error is not None else "--"
                print(f"    {item:<28} {_fmt(model):>12} {_fmt(ref):>12} {error_str:>9}  {status}")
            print()
        
        # Checks
        print(_c(C.CYAN, "  Checks"))
        if result.reference_source:
            s1 = _c(C.GREEN, "OK") if result.max_error <= result.tolerance else _c(C.RED, "!!")
            s2 = _c(C.GREEN, "OK") if result.pass_rate >= 0.95 else _c(C.RED, "!!")
            print(f"    [{s1}] Max error {result.max_error:.2%} <= {result.tolerance:.0%}")
            print(f"    [{s2}] Pass rate {result.pass_rate:.0%} >= 95%")
        else:
            print(_c(C.DIM, "    [--] No observations to compare"))
        print()
        
        # Result
        if result.passed:
            print(_c(C.GREEN, "  PASS"))
        else:
            print(_c(C.RED, "  FAIL"))
            for item, _, _, error, passed in result.comparisons:
                if not passed:
                    print(_c(C.DIM, f"    {item}: {error:.2%} error"))
        print()
        
        # Commentary (academic reflection)
        print(_c(C.CYAN, "  Commentary"))
        if result.commentary:
            print(_wrap_text(result.commentary, width=70, indent="    "))
        else:
            print(_c(C.DIM, "    None"))
        print()


# =============================================================================
# RUNNER HELPER
# =============================================================================

def run_test_group(title: str, summary: str, test_classes: List[type]) -> bool:
    """
    Convenience function to run a group of tests.
    
    Args:
        title: Group title
        summary: Group description
        test_classes: List of GFDTest subclasses
    
    Returns:
        True if all tests passed
    """
    group = GroupResult(title=title, summary=summary)
    
    for test_class in test_classes:
        test = test_class()
        group.tests.append(test.run())
    
    Renderer.render_group(group)
    return group.passed
