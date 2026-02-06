"""
GFD Model Test Framework
========================

A clean, scientific test framework with dependency injection.

Usage:

    # Define a reusable function
    @Fn(
        equation="P(A) = BE(A) * (c / lambda_C)",
        inputs={"A": "int: Mass number"},
        outputs={"watts": "float: Power per field"},
    )
    def power_per_field(A: int) -> float:
        be_mev = get_binding_energy(A)
        return be_mev * MEV_TO_JOULES * F_CLOSURE


    # Define a test that uses the function
    class PowerOutputTest(Test):
        name = "Power Output Validation"
        question = "Does the power formula match observations?"
        tolerance = 0.05
        
        # Type-safe dependency injection
        power = Depends(power_per_field)
        
        def derivation(self):
            return (
                Derivation()
                .step("Get binding energy BE(A)")
                .equation("P = BE × f_closure")
                .conclude("Power peaks at Fe-56")
            )
        
        def model(self):
            return (
                Model()
                .add("Fe-56 power", self.power(56))
                .add("He-4 power", self.power(4))
            )
        
        def observations(self):
            return (
                Observed()
                .add("Fe-56 power", 1.74e8)
                .add("He-4 power", 1.40e8)
            )
"""

from __future__ import annotations
"""
GFD Model Test Framework
========================

A clean, scientific test framework with dependency injection.

Import everything with:
    from gravity_field_model.framework import *

Or import specific items:
    from gravity_field_model.framework import Fn, Depends, Test, Critical
"""
import sys
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Callable, Any, Tuple, TypeVar, Generic

# Type variable for generic function signature
F = TypeVar('F', bound=Callable)

# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # Function decorator
    "Fn",
    # Dependency injection
    "Depends",
    # Test base class
    "Test",
    # Builders
    "Derivation",
    "Model", 
    "Observed",
    # Test levels
    "Level",
    "Critical",
    "Standard", 
    "Exploratory",
    "Ignore",
    # Results
    "TestResult",
    "GroupResult",
    # Runner
    "run_tests",
    # Registry (for advanced use)
    "FunctionRegistry",
]


# =============================================================================
# TEST CLASSIFICATION
# =============================================================================

class Level(Enum):
    """
    Test criticality levels.
    
    CRITICAL: Mission-critical validation. Must pass for the model to be valid.
              These are foundational proofs that everything else depends on.
              Example: Conservation laws, fundamental constants, core geometry.
    
    STANDARD: Normal validation tests. Important but not foundational.
              Example: Specific predictions, cross-checks, derived values.
    
    EXPLORATORY: Experimental or research tests. May not pass yet.
                 Example: New hypotheses, edge cases, speculative predictions.
    
    IGNORE: Test is not serving a useful purpose and should be skipped.
            Mark tests as IGNORE when they:
            - Dump raw data without insight (data dump anti-pattern)
            - Don't answer a clear question
            - Are redundant with other tests
            - Need significant rework before being useful
            These tests are skipped during normal runs but kept for future improvement.
    """
    CRITICAL = "critical"
    STANDARD = "standard"
    EXPLORATORY = "exploratory"
    IGNORE = "ignore"


# Convenient aliases
Critical = Level.CRITICAL
Standard = Level.STANDARD
Exploratory = Level.EXPLORATORY
Ignore = Level.IGNORE


# =============================================================================
# FUNCTION REGISTRY
# =============================================================================

class FunctionRegistry:
    """Global registry for @Fn decorated functions."""
    
    _functions: Dict[str, Dict[str, Any]] = {}
    
    # Graduation thresholds (same as tests)
    AUDIT_THRESHOLD = 65
    CONTRIBUTION_THRESHOLD = 70
    
    @classmethod
    def register(cls, name: str, fn: Callable, equation: str, 
                 inputs: Dict[str, str], outputs: Dict[str, str],
                 description: str = "",
                 audit_score: Optional[int] = None,
                 audit_notes: Optional[str] = None,
                 contribution_score: Optional[int] = None,
                 contribution_notes: Optional[str] = None):
        cls._functions[name] = {
            'fn': fn,
            'equation': equation,
            'inputs': inputs,
            'outputs': outputs,
            'description': description,
            'audit_score': audit_score,
            'audit_notes': audit_notes,
            'contribution_score': contribution_score,
            'contribution_notes': contribution_notes,
        }
    
    @classmethod
    def get(cls, name: str) -> Callable:
        if name not in cls._functions:
            available = list(cls._functions.keys()) or ['(none)']
            raise KeyError(
                f"Function '{name}' not registered. "
                f"Available: {available}"
            )
        return cls._functions[name]['fn']
    
    @classmethod
    def get_metadata(cls, name: str) -> Optional[Dict]:
        return cls._functions.get(name)
    
    @classmethod
    def all(cls) -> Dict[str, Dict]:
        return dict(cls._functions)
    
    @classmethod
    def is_graduated(cls, name: str) -> bool:
        """Check if a function meets graduation criteria."""
        if name not in cls._functions:
            return False
        meta = cls._functions[name]
        audit = meta.get('audit_score')
        contrib = meta.get('contribution_score')
        if audit is None or contrib is None:
            return False
        return audit >= cls.AUDIT_THRESHOLD and contrib >= cls.CONTRIBUTION_THRESHOLD
    
    @classmethod
    def graduated_functions(cls) -> Dict[str, Dict]:
        """Return only functions that meet graduation criteria."""
        return {
            name: meta for name, meta in cls._functions.items()
            if cls.is_graduated(name)
        }
    
    @classmethod
    def pending_functions(cls) -> Dict[str, Dict]:
        """Return functions that have not yet graduated."""
        return {
            name: meta for name, meta in cls._functions.items()
            if not cls.is_graduated(name)
        }


# =============================================================================
# @Fn DECORATOR
# =============================================================================

def Fn(*, equation: str, inputs: Dict[str, str], outputs: Dict[str, str], 
       description: str = "",
       audit_score: Optional[int] = None,
       audit_notes: Optional[str] = None,
       contribution_score: Optional[int] = None,
       contribution_notes: Optional[str] = None):
    """
    Decorator to register a function as a reusable, documented component.
    
    Usage:
        @Fn(
            equation="P(A) = BE(A) * f_closure",
            inputs={"A": "int: Mass number"},
            outputs={"watts": "float: Power per field"},
            description="Power output per gravity field from binding energy.",
            # Scoring (required for graduation to central registry):
            audit_score=78,
            audit_notes="Clear equation, good docs, validated by CRITICAL test.",
            contribution_score=72,
            contribution_notes="Discovery: 28/40, Precision: 15/20, Cross-Domain: 17/20, Falsifiability: 12/20",
        )
        def power_per_field(A: int) -> float:
            ...
    
    The function is automatically registered and can be injected into tests
    using Depends(power_per_field).
    
    GRADUATION CRITERIA (same as tests):
        - audit_score >= 65 (quality threshold)
        - contribution_score >= 70 (must be "Significant" or higher)
    
    Only graduated functions are included in the central functions/ registry.
    Functions without scores or below threshold remain in their source files
    but are not exposed through gravity_field_model.functions.
    
    SCORING GUIDE:
        audit_score (0-100): How well documented and validated is the function?
        - Equation clarity, input/output docs, description quality
        - Validated by at least one CRITICAL test
        - Constants from common module
        
        contribution_score (0-100): How valuable is this function?
        - Discovery Value (0-40): Does it encapsulate novel calculation?
        - Precision & Rigor (0-20): How reliable?
        - Cross-Domain Impact (0-20): Used across multiple domains?
        - Falsifiability (0-20): Does it make testable predictions?
    """
    def decorator(fn: F) -> F:
        # Attach metadata to function
        fn._fn_registered = True
        fn._fn_equation = equation
        fn._fn_inputs = inputs
        fn._fn_outputs = outputs
        fn._fn_description = description
        fn._fn_audit_score = audit_score
        fn._fn_audit_notes = audit_notes
        fn._fn_contribution_score = contribution_score
        fn._fn_contribution_notes = contribution_notes
        
        # Register in global registry
        FunctionRegistry.register(
            name=fn.__name__,
            fn=fn,
            equation=equation,
            inputs=inputs,
            outputs=outputs,
            description=description,
            audit_score=audit_score,
            audit_notes=audit_notes,
            contribution_score=contribution_score,
            contribution_notes=contribution_notes,
        )
        
        return fn
    
    return decorator


# =============================================================================
# Depends() - DEPENDENCY INJECTION
# =============================================================================

class _Dependency:
    """Descriptor for dependency injection."""
    
    def __init__(self, fn: Callable):
        if not getattr(fn, '_fn_registered', False):
            raise TypeError(
                f"Depends() requires an @Fn decorated function. "
                f"'{fn.__name__}' is not decorated with @Fn."
            )
        self.fn = fn
        self.name = fn.__name__
    
    def __get__(self, obj, objtype=None) -> Callable:
        # Return the actual function
        return self.fn


def Depends(fn: F) -> F:
    """
    Declare a dependency on an @Fn decorated function.
    
    Usage:
        class MyTest(Test):
            power = Depends(power_per_field)
            
            def model(self):
                result = self.power(56)  # Type-safe call
    """
    return _Dependency(fn)  # type: ignore


# =============================================================================
# DERIVATION BUILDER
# =============================================================================

class Derivation:
    """
    Builder for derivation steps.
    
    Usage:
        Derivation()
        .step("First reasoning step")
        .equation("E = mc^2")
        .step("Second reasoning step")
        .conclude("Therefore X equals Y")
    """
    
    def __init__(self):
        self._steps: List[Tuple[str, str]] = []
    
    def step(self, text: str) -> 'Derivation':
        """Add a reasoning step."""
        self._steps.append(('step', text))
        return self
    
    def equation(self, latex: str) -> 'Derivation':
        """Add a mathematical equation."""
        self._steps.append(('equation', latex))
        return self
    
    def conclude(self, text: str) -> 'Derivation':
        """Add the concluding statement."""
        self._steps.append(('conclude', text))
        return self
    
    def to_string(self) -> str:
        """Convert to formatted string."""
        parts = []
        for tag, text in self._steps:
            if tag == 'equation':
                parts.append(f"EQUATION: {text}")
            elif tag == 'conclude':
                parts.append(f"THEREFORE: {text}")
            else:
                parts.append(text)
        return " ".join(parts)
    
    def to_list(self) -> List[Tuple[str, str]]:
        """Return raw steps."""
        return list(self._steps)


# =============================================================================
# MODEL BUILDER
# =============================================================================

@dataclass
class _Metric:
    """Single metric with optional custom tolerance."""
    name: str
    value: float
    tolerance: Optional[float] = None


class Model:
    """
    Builder for model results.
    
    Usage:
        Model()
        .add("Metric A", 123.45)
        .add("Metric B", 67.89, tol=0.05)  # Custom 5% tolerance
        .add_table(title="Results", headers=[...], rows=[...])
    """
    
    def __init__(self):
        self._metrics: List[_Metric] = []
        self._tables: List[Dict] = []
    
    def add(self, name: str, value: float, tol: Optional[float] = None) -> 'Model':
        """
        Add a metric.
        
        Args:
            name: Metric name
            value: Calculated value
            tol: Optional custom tolerance (overrides class default)
        """
        self._metrics.append(_Metric(name, value, tol))
        return self
    
    def add_table(self, data: Dict = None, *, title: str = None, 
                  headers: List[str] = None, rows: List[List] = None,
                  footer: str = None) -> 'Model':
        """
        Add a data table.
        
        Can be called with a dict or keyword arguments:
            .add_table({"title": "...", "headers": [...], "rows": [...]})
            .add_table(title="...", headers=[...], rows=[...])
        """
        if data is not None:
            self._tables.append(data)
        else:
            self._tables.append({
                'title': title,
                'headers': headers,
                'rows': rows,
                'footer': footer,
            })
        return self
    
    def to_dict(self) -> Dict[str, float]:
        """Convert metrics to simple dict (for backward compatibility)."""
        return {m.name: m.value for m in self._metrics}
    
    def get_metrics(self) -> List[_Metric]:
        """Return all metrics with their tolerances."""
        return list(self._metrics)
    
    def get_tables(self) -> List[Dict]:
        """Return all tables."""
        return list(self._tables)


# =============================================================================
# OBSERVED BUILDER
# =============================================================================

class Observed:
    """
    Builder for observed/reference values.
    
    Usage:
        Observed()
        .add("Metric A", 123.0)
        .add("Metric B", 68.0)
        .add_table(title="Reference Data", headers=[...], rows=[...])
    """
    
    def __init__(self):
        self._values: Dict[str, float] = {}
        self._tables: List[Dict] = []
    
    def add(self, name: str, value: float) -> 'Observed':
        """Add an observed value."""
        self._values[name] = value
        return self
    
    def add_table(self, data: Dict = None, *, title: str = None,
                  headers: List[str] = None, rows: List[List] = None,
                  footer: str = None) -> 'Observed':
        """Add a reference data table."""
        if data is not None:
            self._tables.append(data)
        else:
            self._tables.append({
                'title': title,
                'headers': headers,
                'rows': rows,
                'footer': footer,
            })
        return self
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to simple dict."""
        return dict(self._values)
    
    def get_tables(self) -> List[Dict]:
        """Return all tables."""
        return list(self._tables)


# =============================================================================
# TEST RESULT
# =============================================================================

@dataclass
class TestResult:
    """Structured result from a test run."""
    name: str
    question: str
    model_values: Dict[str, float]
    observations: Optional[Dict[str, float]] = None
    reference_source: Optional[str] = None
    tolerance: float = 0.10
    derivation: Optional[str] = None
    commentary: Optional[str] = None
    tables: List[Dict] = field(default_factory=list)
    metric_tolerances: Dict[str, float] = field(default_factory=dict)
    level: Level = Level.STANDARD
    class_name: Optional[str] = None  # The Python class name for CLI runner
    
    # Computed fields
    passed: bool = field(init=False)
    comparisons: List[Tuple[str, float, float, Optional[float], bool]] = field(init=False)
    max_error: float = field(init=False)
    
    def __post_init__(self):
        self.comparisons = []
        
        for name, model_val in self.model_values.items():
            # Get tolerance: metric-specific or default
            tol = self.metric_tolerances.get(name, self.tolerance)
            
            if self.observations and name in self.observations:
                ref_val = self.observations[name]
                if ref_val != 0:
                    error = abs(model_val - ref_val) / abs(ref_val)
                else:
                    error = 0.0 if model_val == 0 else float('inf')
                item_passed = error <= tol
                self.comparisons.append((name, model_val, ref_val, error, item_passed))
            else:
                self.comparisons.append((name, model_val, None, None, True))
        
        errors = [c[3] for c in self.comparisons if c[3] is not None]
        self.max_error = max(errors) if errors else 0.0
        
        if self.observations:
            self.passed = all(c[4] for c in self.comparisons)
        else:
            self.passed = True


# =============================================================================
# TEST BASE CLASS
# =============================================================================

class Test(ABC):
    """
    Base class for scientific tests.
    
    Subclasses define:
        - name: Test name
        - question: What are we testing?
        - tolerance: Default tolerance (default 10%)
        - reference: Source of observations (optional)
        - commentary: Academic reflection (optional)
        - level: Test criticality (Critical, Standard, Exploratory, Ignore)
        - audit_notes: Internal notes for maintainers (optional, not shown in output)
    
    And implement:
        - derivation(): Return Derivation builder
        - model(): Return Model builder
        - observations(): Return Observed builder (optional)
    
    Dependencies are declared as class attributes:
        power = Depends(power_per_field)
    
    Criticality levels:
        level = Critical    # Mission-critical, must pass
        level = Standard    # Normal validation (default)
        level = Exploratory # Experimental, may not pass
        level = Ignore      # Not useful, skip during runs
    
    Audit notes (for Feynman framework compliance):
        audit_notes = "NEEDS WORK: Missing commentary. Reframe question..."
        audit_score = 75  # 0-100 based on TEST_QUALITY_MODULE.md
    
    Scoring (25 points each):
        - Question hooks curiosity (why before what)
        - Derivation builds intuition before math
        - Model output summarizes (not data dump)
        - Commentary delivers insight (not restatement)
    """
    
    name: str = "Unnamed Test"
    question: str = "What are we testing?"
    tolerance: float = 0.10
    reference: Optional[str] = None
    commentary: Optional[str] = None
    level: Level = Level.STANDARD
    
    # Internal notes for maintainers (not shown in test output)
    # Use for Feynman framework audit findings, technical debt, future improvements
    audit_notes: Optional[str] = None
    
    # Feynman framework compliance score (0-100)
    # Based on TEST_QUALITY_MODULE.md criteria:
    #   - Question hooks curiosity (why before what): 25 pts
    #   - Derivation builds intuition before math: 25 pts
    #   - Model output summarizes (not data dump): 25 pts
    #   - Commentary delivers insight (not restatement): 25 pts
    # Score of None means not yet audited
    audit_score: Optional[int] = None
    
    # Scientific Contribution Score (0-100)
    # Measures the VALUE of this test's findings to the overall system
    # Based on CONTRIBUTION_SCORING_MODULE.md criteria:
    #
    # DISCOVERY VALUE (0-40 points):
    #   40: Answers a fundamental unsolved problem in physics
    #   30: Reveals a previously unknown relationship or pattern
    #   20: Confirms a theoretical prediction with new evidence
    #   10: Extends known physics to a new domain
    #   0:  Routine verification of established results
    #
    # PRECISION & RIGOR (0-20 points):
    #   20: Multiple independent confirmations, high precision (<0.1%)
    #   15: Strong confirmation with good precision (<1%)
    #   10: Reasonable confirmation with moderate precision (<5%)
    #   5:  Suggestive but needs more precision
    #   0:  Inconclusive or low precision
    #
    # CROSS-DOMAIN IMPACT (0-20 points):
    #   20: Unifies multiple domains (e.g., GW + particle + cosmology)
    #   15: Connects two previously separate domains
    #   10: Suggests connections worth investigating
    #   5:  Domain-specific insight
    #   0:  No cross-domain relevance
    #
    # FALSIFIABILITY & PREDICTIONS (0-20 points):
    #   20: Makes testable predictions that could be checked experimentally
    #   15: Makes predictions testable with future observations
    #   10: Constrains parameter space meaningfully
    #   5:  Suggests what to look for next
    #   0:  No predictive power
    #
    # Score interpretation:
    #   90-100: Profound (potential paradigm shift)
    #   70-89:  Significant (advances understanding materially)
    #   50-69:  Valuable (solid contribution to the field)
    #   30-49:  Incremental (useful but not groundbreaking)
    #   0-29:   Routine (verification, no new insight)
    #
    # Score of None means not yet assessed
    contribution_score: Optional[int] = None
    
    # Explanation of contribution score
    # Document WHY this test earned its contribution score
    # Example: "Discovery: 30 (new pattern 3/8=d/2^d found), Precision: 15 ..."
    contribution_notes: Optional[str] = None
    
    def derivation(self) -> Derivation:
        """Return derivation steps. Override in subclass."""
        return Derivation()
    
    @abstractmethod
    def model(self) -> Model:
        """Return model calculations. Must override."""
        pass
    
    def observations(self) -> Optional[Observed]:
        """Return observed values. Override if comparing to data."""
        return None
    
    def run(self) -> TestResult:
        """Execute test and return structured result."""
        # Get derivation
        deriv = self.derivation()
        deriv_str = deriv.to_string() if deriv else None
        
        # Get model results
        model_result = self.model()
        model_dict = model_result.to_dict()
        tables = model_result.get_tables()
        
        # Get metric-specific tolerances
        metric_tols = {
            m.name: m.tolerance 
            for m in model_result.get_metrics() 
            if m.tolerance is not None
        }
        
        # Get observations
        obs_result = self.observations()
        obs_dict = obs_result.to_dict() if obs_result else None
        if obs_result:
            tables.extend(obs_result.get_tables())
        
        return TestResult(
            name=self.name,
            question=self.question,
            model_values=model_dict,
            observations=obs_dict,
            reference_source=self.reference,
            tolerance=self.tolerance,
            derivation=deriv_str,
            commentary=self.commentary,
            tables=tables,
            metric_tolerances=metric_tols,
            level=self.level,
            class_name=self.__class__.__name__,
        )


# =============================================================================
# GROUP RESULT
# =============================================================================

@dataclass
class GroupResult:
    """Result from a group of tests."""
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
    
    @property
    def critical_tests(self) -> List[TestResult]:
        return [t for t in self.tests if t.level == Level.CRITICAL]
    
    @property
    def critical_passed(self) -> bool:
        critical = self.critical_tests
        return all(t.passed for t in critical) if critical else True
    
    @property
    def critical_count(self) -> int:
        return len(self.critical_tests)
    
    @property
    def critical_pass_count(self) -> int:
        return sum(1 for t in self.critical_tests if t.passed)


# =============================================================================
# RENDERER
# =============================================================================

class _Colors:
    """Terminal colors."""
    BLUE = '\033[38;5;39m'
    CYAN = '\033[38;5;44m'
    GREEN = '\033[38;5;46m'
    RED = '\033[38;5;196m'
    YELLOW = '\033[38;5;226m'
    DIM = '\033[38;5;245m'
    RESET = '\033[0m'


def _color_enabled():
    if os.environ.get('NO_COLOR'):
        return False
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            return False
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


_USE_COLOR = _color_enabled()


def _c(color: str, text: str) -> str:
    return f"{color}{text}{_Colors.RESET}" if _USE_COLOR else text


def _fmt(v) -> str:
    if v is None:
        return "--"
    if abs(v) >= 1e6 or (abs(v) < 0.001 and v != 0):
        return f"{v:.3e}"
    elif v == int(v):
        return f"{int(v)}"
    return f"{v:.6f}"


def _wrap(text: str, width: int = 70, indent: str = "  ") -> str:
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
    def render_table(table: Dict, indent: str = "    "):
        """Render a data table."""
        if not table:
            return
        
        headers = table.get('headers', [])
        rows = table.get('rows', [])
        title = table.get('title')
        footer = table.get('footer')
        
        if not headers or not rows:
            return
        
        # Column widths
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        
        sep = indent + "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        
        if title:
            print()
            print(_c(_Colors.CYAN, f"{indent}{title}"))
        
        print(sep)
        
        # Headers
        header_row = indent + "|"
        for i, h in enumerate(headers):
            header_row += f" {str(h):^{widths[i]}} |"
        print(_c(_Colors.DIM, header_row))
        print(sep)
        
        # Rows
        for row in rows:
            row_str = indent + "|"
            for i, cell in enumerate(row):
                if i < len(widths):
                    cell_str = str(cell)
                    if isinstance(cell, (int, float)):
                        row_str += f" {cell_str:>{widths[i]}} |"
                    else:
                        row_str += f" {cell_str:<{widths[i]}} |"
            print(row_str)
        
        print(sep)
        
        if footer:
            print(_c(_Colors.DIM, f"{indent}{footer}"))
        print()
    
    @staticmethod
    def render_test(result: TestResult):
        """Render a single test result."""
        # Level badge (always show for UI parsing)
        if result.level == Level.CRITICAL:
            badge = _c(_Colors.RED, "[CRITICAL]")
        elif result.level == Level.EXPLORATORY:
            badge = _c(_Colors.YELLOW, "[EXPLORATORY]")
        elif result.level == Level.IGNORE:
            badge = _c(_Colors.DIM, "[IGNORE]")
        else:
            badge = _c(_Colors.GREEN, "[STANDARD]")
        
        title = f"  {result.name.upper()}  {badge}"
        print(title)
        print(_c(_Colors.DIM, "  " + "-" * 60))
        # Print class name for CLI runner reference
        if result.class_name:
            print(_c(_Colors.DIM, f"  [class: {result.class_name}]"))
        print()
        
        print(f"  {result.question}")
        print()
        
        # Derivation
        print(_c(_Colors.CYAN, "  Derivation"))
        if result.derivation:
            print(_wrap(result.derivation, indent="    "))
        else:
            print(_c(_Colors.DIM, "    (none)"))
        print()
        
        # Model
        print(_c(_Colors.CYAN, "  Model"))
        for name, val in result.model_values.items():
            print(f"    {name:<35} {_fmt(val):>15}")
        print()
        
        # Tables
        for table in result.tables:
            Renderer.render_table(table)
        
        # Observations
        if result.reference_source:
            print(_c(_Colors.CYAN, "  Observations") + 
                  _c(_Colors.DIM, f"  ({result.reference_source})"))
            for name, _, ref, _, _ in result.comparisons:
                if ref is not None:
                    print(f"    {name:<35} {_fmt(ref):>15}")
        else:
            print(_c(_Colors.CYAN, "  Observations"))
            print(_c(_Colors.DIM, "    (none)"))
        print()
        
        # Comparison
        if result.observations:
            print(_c(_Colors.CYAN, "  Comparison"))
            for name, model, ref, error, passed in result.comparisons:
                if ref is not None:
                    status = _c(_Colors.GREEN, "OK") if passed else _c(_Colors.RED, "FAIL")
                    err_str = f"{error:.2%}" if error is not None else "--"
                    print(f"    [{status}] {name}: {err_str} error")
            print()
        
        # Result
        if result.passed:
            print(_c(_Colors.GREEN, "  PASS"))
        else:
            print(_c(_Colors.RED, "  FAIL"))
        print()
        
        # Commentary
        if result.commentary:
            print(_c(_Colors.CYAN, "  Commentary"))
            print(_wrap(result.commentary, indent="    "))
            print()
    
    @staticmethod
    def render_group(group: GroupResult):
        """Render a group of test results."""
        print()
        print(_c(_Colors.CYAN, f"  {group.title.upper()}"))
        print(_c(_Colors.DIM, "  " + "-" * 60))
        print()
        print(_wrap(group.summary))
        print()
        
        for test in group.tests:
            Renderer.render_test(test)
        
        print(_c(_Colors.DIM, "  " + "-" * 60))
        
        # Summary line
        if group.passed:
            print(_c(_Colors.GREEN, f"  {group.pass_count}/{group.total_count} tests passed"))
        else:
            print(_c(_Colors.RED, f"  {group.pass_count}/{group.total_count} tests passed"))
        
        # Critical tests summary (if any)
        if group.critical_count > 0:
            if group.critical_passed:
                print(_c(_Colors.GREEN, f"  {group.critical_pass_count}/{group.critical_count} CRITICAL tests passed"))
            else:
                failed = [t.name for t in group.critical_tests if not t.passed]
                print(_c(_Colors.RED, f"  {group.critical_pass_count}/{group.critical_count} CRITICAL tests passed"))
                print(_c(_Colors.RED, f"  CRITICAL FAILURES: {', '.join(failed)}"))
        
        print()


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_tests(title: str, summary: str, test_classes: List[type], include_ignored: bool = False) -> bool:
    """
    Run a group of tests and render results.
    
    Args:
        title: Group title
        summary: Group description
        test_classes: List of Test subclasses
        include_ignored: If True, run tests marked as IGNORE (default: False)
    
    Returns:
        True if all tests passed
    """
    group = GroupResult(title=title, summary=summary)
    
    ignored_count = 0
    for test_class in test_classes:
        test = test_class()
        # Skip ignored tests unless explicitly requested
        if test.level == Level.IGNORE and not include_ignored:
            ignored_count += 1
            continue
        group.tests.append(test.run())
    
    Renderer.render_group(group)
    
    # Report ignored tests if any
    if ignored_count > 0:
        print(_c(_Colors.DIM, f"  ({ignored_count} tests marked IGNORE, skipped)"))
        print()
    
    return group.passed
