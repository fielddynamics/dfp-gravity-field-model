"""
GFD Test Framework
==================

Drop-in replacement for base.py. All existing tests work unchanged.

New optional properties give each test a complete scientific identity:

    equation          WHAT is being computed
    parameters        FROM WHAT inputs           (use Param for clean specs)
    assumptions       UNDER WHAT premises
    derivation        BY WHAT steps              (original)
    model()           PRODUCING WHAT result      (original)
    units             IN WHAT units
    uncertainty       WITH WHAT confidence
    observations()    COMPARED TO WHAT           (original)
    test_type         AS WHAT kind of test        (D/P/C/S/E)
    prediction_target TESTABLE AGAINST WHAT
    commentary        MEANING WHAT               (original)

Quick start:

    class MyTest(GFDTest):
        name = "MOND Scale"
        question = "Does k=4 predict a₀?"
        test_type = TestType.PREDICTION
        equation = "a₀ = k² · G · mₑ / rₑ²"
        parameters = {
            "k": Param(4, source="simplex theorem", fixed=True),
            "G": Param(6.674e-11, "m³/(kg·s²)", "CODATA 2018", unc=1.5e-15),
        }

        def model(self):
            return {"a₀": 1.23e-10}

        def observations(self):
            return {"a₀": 1.2e-10}
"""

__all__ = [
    "Param", "TestType", "Rating", "TestResult", "GroupResult",
    "GFDTest", "Renderer", "run_test_group",
]

import sys
import os
import traceback
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple, Any
from abc import ABC, abstractmethod

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# PARAM — Clean parameter specification
# =============================================================================

@dataclass
class Param:
    """
    A named input to a test equation.

    Usage:
        Param(4, source="simplex theorem", fixed=True)
        Param(6.674e-11, "m³/(kg·s²)", "CODATA 2018", unc=1.5e-15)
    """
    value: Any
    unit: str = ""
    source: str = ""
    unc: Optional[float] = None
    fixed: bool = False


# =============================================================================
# TEST TYPE — Five constants, nothing more
# =============================================================================

class TestType:
    """What kind of question does this test answer?"""
    DERIVATION  = "derivation"     # [D] Math chain correct?
    PREDICTION  = "prediction"     # [P] Matches real data?
    CONSISTENCY = "consistency"    # [C] Internally coherent?
    SENSITIVITY = "sensitivity"   # [S] Robust to parameters?
    EXPLORATION = "exploration"   # [E] Record what emerges.

    ALL = {DERIVATION, PREDICTION, CONSISTENCY, SENSITIVITY, EXPLORATION}


# =============================================================================
# RATING — How critical is this test to the system?
# =============================================================================

class Rating:
    """
    Test importance to the framework.

    Use this to tell contributors which tests are load-bearing walls
    and which are exploratory scaffolding.

        Rating.CRITICAL   — Core system validation. If this fails, the
                            framework is broken. Do not modify without
                            understanding the full derivation chain.

        Rating.STANDARD   — Important validation. Expected to pass in
                            a healthy system. Default for all tests.

        Rating.RESEARCH   — Active investigation. Results are informative
                            but not yet definitive. Safe to experiment with.

    Integer-valued so you can filter:
        run_test_group(..., min_rating=Rating.CRITICAL)
    """
    RESEARCH  = 1    # ★       Exploratory / under investigation
    STANDARD  = 2    # ★★      Expected to pass (default)
    CRITICAL  = 3    # ★★★     Core framework — must pass

    _LABELS = {1: "RESEARCH", 2: "STANDARD", 3: "CRITICAL"}
    _STARS  = {1: "★", 2: "★★", 3: "★★★"}

    @classmethod
    def label(cls, level: int) -> str:
        return cls._LABELS.get(level, f"UNKNOWN({level})")

    @classmethod
    def stars(cls, level: int) -> str:
        return cls._STARS.get(level, "?")


# =============================================================================
# TEST RESULT
# =============================================================================

@dataclass
class TestResult:
    """Structured output from a single test run."""

    # --- Core (original) ---
    name: str
    question: str
    model_values: Dict[str, float]
    observations: Optional[Dict[str, float]] = None
    reference_source: Optional[str] = None
    tolerance: float = 0.10
    derivation: Optional[str] = None
    commentary: Optional[str] = None
    table: Optional[Dict] = None

    # --- Enhanced (all optional) ---
    equation: Optional[str] = None
    test_type: str = TestType.CONSISTENCY
    parameters: Optional[Dict[str, Any]] = None
    assumptions: Optional[List[str]] = None
    prediction_target: Optional[str] = None
    units: Optional[Dict[str, str]] = None
    uncertainty: Optional[Dict[str, float]] = None
    error_message: Optional[str] = None
    rating: int = Rating.STANDARD

    # --- Computed ---
    passed: bool = field(init=False)
    comparisons: List[Tuple[str, float, float, Optional[float], bool]] = field(init=False)
    max_error: float = field(init=False)
    pass_rate: float = field(init=False)

    def __post_init__(self):
        # If model() crashed, mark failed with no comparisons
        if self.error_message:
            self.comparisons = []
            self.max_error = float('inf')
            self.pass_rate = 0.0
            self.passed = False
            return

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

    @property
    def is_exploration(self) -> bool:
        return self.test_type == TestType.EXPLORATION

    @property
    def rating_label(self) -> str:
        return Rating.label(self.rating)

    @property
    def rating_stars(self) -> str:
        return Rating.stars(self.rating)

    @property
    def one_liner(self) -> str:
        """Single-line summary: '[P] ★★★ MOND Scale — PASS'"""
        badge = _TYPE_SHORT.get(self.test_type, "?")
        stars = Rating.stars(self.rating)
        if self.error_message:
            return f"[{badge}] {stars} {self.name}: ERROR — {self.error_message[:60]}"
        if self.is_exploration:
            vals = ", ".join(f"{k}={_fmt(v)}" for k, v in list(self.model_values.items())[:3])
            return f"[{badge}] {stars} {self.name}: {vals} — RECORDED"
        verdict = "PASS" if self.passed else f"FAIL ({self.max_error:.1%})"
        return f"[{badge}] {stars} {self.name} — {verdict}"

    def to_dict(self) -> Dict[str, Any]:
        """Flat dict for JSON export, logging, or database storage."""
        d: Dict[str, Any] = {
            "name": self.name,
            "type": self.test_type,
            "rating": self.rating,
            "rating_label": Rating.label(self.rating),
            "passed": self.passed,
            "max_error": self.max_error,
        }
        if self.equation:
            d["equation"] = self.equation
        if self.error_message:
            d["error"] = self.error_message
        for key, val in self.model_values.items():
            d[f"result.{key}"] = val
            if self.units and key in self.units:
                d[f"unit.{key}"] = self.units[key]
            if self.uncertainty and key in self.uncertainty:
                d[f"unc.{key}"] = self.uncertainty[key]
        return d


# =============================================================================
# GROUP RESULT
# =============================================================================

@dataclass
class GroupResult:
    """Structured output from a batch of tests."""
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
    def type_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for t in self.tests:
            counts[t.test_type] = counts.get(t.test_type, 0) + 1
        return counts

    @property
    def max_rating(self) -> int:
        """Highest rating in the group — the group is as critical as its most critical test."""
        if not self.tests:
            return Rating.STANDARD
        return max(t.rating for t in self.tests)

    @property
    def rating_counts(self) -> Dict[int, int]:
        """Count tests by rating level."""
        counts: Dict[int, int] = {}
        for t in self.tests:
            counts[t.rating] = counts.get(t.rating, 0) + 1
        return counts


# =============================================================================
# TEST BASE CLASS
# =============================================================================

class GFDTest(ABC):
    """
    Base class for all GFD validation tests.

    REQUIRED:
        name            str     Test name
        question        str     What are we testing?
        model()         →       Dict[str, float]

    ORIGINAL (optional):
        reference_source    Source of observations
        tolerance           Acceptable relative error (default 10%)
        derivation          Step-by-step derivation chain
        commentary          What the result means
        table               Structured table for display
        observations()  →   Dict[str, float] or None

    ENHANCED (optional, all default to None):
        equation            Symbolic formula being tested
        test_type           TestType.PREDICTION / .DERIVATION / etc.
        parameters          Dict of Param objects (inputs to the equation)
        assumptions         List of premises this test depends on
        prediction_target   What real-world data could validate/falsify this
        units               Dict mapping output keys to physical units
        uncertainty         Dict mapping output keys to ±σ values
    """

    # --- Original ---
    name: str = "Unnamed Test"
    question: str = "What are we testing?"
    reference_source: Optional[str] = None
    tolerance: float = 0.10
    derivation: Optional[str] = None
    commentary: Optional[str] = None
    table: Optional[Dict] = None

    # --- Enhanced ---
    equation: Optional[str] = None
    test_type: str = TestType.CONSISTENCY
    parameters: Optional[Dict[str, Any]] = None
    assumptions: Optional[List[str]] = None
    prediction_target: Optional[str] = None
    units: Optional[Dict[str, str]] = None
    uncertainty: Optional[Dict[str, float]] = None
    rating: int = Rating.STANDARD

    @abstractmethod
    def model(self) -> Dict[str, float]:
        """Compute and return model values."""
        pass

    def observations(self) -> Optional[Dict[str, float]]:
        """Return reference observations, or None."""
        return None

    def run(self) -> TestResult:
        """Execute test. Catches exceptions so the suite never crashes."""
        error_msg = None
        model_values: Dict[str, float] = {}
        obs = None

        try:
            model_values = self.model()
        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            model_values = {}

        if error_msg is None:
            try:
                obs = self.observations()
            except Exception as e:
                error_msg = f"observations() — {type(e).__name__}: {e}"
                obs = None

        return TestResult(
            name=self.name,
            question=self.question,
            model_values=model_values,
            observations=obs,
            reference_source=self.reference_source,
            tolerance=self.tolerance,
            derivation=self.derivation,
            commentary=self.commentary,
            table=self.table,
            equation=self.equation,
            test_type=self.test_type,
            parameters=self.parameters,
            assumptions=self.assumptions,
            prediction_target=self.prediction_target,
            units=self.units,
            uncertainty=self.uncertainty,
            error_message=error_msg,
            rating=self.rating,
        )


# =============================================================================
# TERMINAL HELPERS
# =============================================================================

class C:
    """ANSI color codes."""
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    DIM     = '\033[2m'
    BOLD    = '\033[1m'
    RESET   = '\033[0m'

def _c(color: str, text: str) -> str:
    return f"{color}{text}{C.RESET}"

def _fmt(val) -> str:
    if val is None:
        return "--"
    if isinstance(val, float):
        if abs(val) >= 1000 or (abs(val) < 0.01 and val != 0):
            return f"{val:.6e}"
        return f"{val:.6f}"
    return str(val)

def _wrap(text: str, width: int = 70, indent: str = "    ") -> str:
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = indent
        for word in words:
            if len(current) + len(word) + 1 <= width + len(indent):
                current += word + " "
            else:
                lines.append(current.rstrip())
                current = indent + word + " "
        if current.strip():
            lines.append(current.rstrip())
    return '\n'.join(lines)

_PURPLE = ['\033[38;5;93m', '\033[38;5;135m', '\033[38;5;171m', '\033[38;5;177m']

def _gradient(text: str) -> str:
    return ''.join(f"{_PURPLE[i % 4]}{ch}" for i, ch in enumerate(text)) + C.RESET

_TYPE_SHORT = {
    "derivation": "D", "prediction": "P", "consistency": "C",
    "sensitivity": "S", "exploration": "E",
}
_TYPE_COLOR = {
    "derivation": C.CYAN, "prediction": C.GREEN, "consistency": C.BLUE,
    "sensitivity": C.YELLOW, "exploration": C.MAGENTA,
}

def _badge(test_type: str) -> str:
    color = _TYPE_COLOR.get(test_type, C.DIM)
    short = _TYPE_SHORT.get(test_type, "?")
    return _c(color, f"[{short}]")

_RATING_COLOR = {
    Rating.CRITICAL: C.RED,
    Rating.STANDARD: C.DIM,
    Rating.RESEARCH: C.DIM,
}

def _rating_badge(rating: int) -> str:
    """Colored rating badge: ★★★ CRITICAL, ★★, ★"""
    color = _RATING_COLOR.get(rating, C.DIM)
    stars = Rating.stars(rating)
    if rating == Rating.CRITICAL:
        return _c(color, f"{stars} CRITICAL")
    elif rating == Rating.RESEARCH:
        return _c(color, f"{stars} RESEARCH")
    return ""  # STANDARD = default, don't clutter


# =============================================================================
# RENDERER — Modular section-based rendering
# =============================================================================

def _render_header(r: TestResult):
    line = f"  {_badge(r.test_type)} {_c(C.BLUE, r.name.upper())}"
    rb = _rating_badge(r.rating)
    if rb:
        line += f"  {rb}"
    print(line)
    print(_c(C.DIM, "  " + "-" * 60))
    print()
    print(f"  {r.question}")
    print()

def _render_specification(r: TestResult):
    """Equation, parameters, assumptions — the test's scientific identity."""
    if r.equation:
        print(_c(C.CYAN, "  Equation"))
        print(f"    {_c(C.BOLD, r.equation)}")
        print()

    if r.parameters:
        print(_c(C.CYAN, "  Parameters"))
        for pname, p in r.parameters.items():
            if isinstance(p, Param):
                line = f"    {pname:<20} = {_fmt(p.value)}"
                if p.unc is not None:
                    line += f" ± {_fmt(p.unc)}"
                if p.unit:
                    line += f"  {p.unit}"
                if p.source:
                    line += _c(C.DIM, f"  ({p.source})")
                print(line)
            elif isinstance(p, dict):
                # Backward compat: old-style nested dicts
                val = p.get("value", "?")
                line = f"    {pname:<20} = {_fmt(val)}"
                if p.get("uncertainty"):
                    line += f" ± {_fmt(p['uncertainty'])}"
                if p.get("unit"):
                    line += f"  {p['unit']}"
                if p.get("source"):
                    line += _c(C.DIM, f"  ({p['source']})")
                print(line)
            else:
                # Plain value
                print(f"    {pname:<20} = {_fmt(p)}")
        print()

    if r.assumptions:
        print(_c(C.CYAN, "  Assumes"))
        for i, a in enumerate(r.assumptions, 1):
            print(f"    {i}. {a}")
        print()

def _render_derivation(r: TestResult):
    print(_c(C.CYAN, "  Derivation"))
    if r.derivation:
        print(_wrap(r.derivation))
    else:
        print(_c(C.DIM, "    None"))
    print()

def _render_results(r: TestResult):
    """Model values, observations, comparison table."""

    # Error state
    if r.error_message:
        print(_c(C.RED, "  ERROR"))
        print(f"    {r.error_message}")
        print()
        return

    # Model
    print(_c(C.CYAN, "  GFD Model"))
    if r.table:
        Renderer.render_table(r.table, indent="    ")
    for item, val in r.model_values.items():
        suffix = ""
        if r.uncertainty and item in r.uncertainty:
            suffix += _c(C.DIM, f" ± {_fmt(r.uncertainty[item])}")
        if r.units and item in r.units:
            suffix += _c(C.DIM, f"  {r.units[item]}")
        print(f"    {item:<35} {_fmt(val):>15}{suffix}")
    print()

    # Observations
    if r.reference_source:
        print(_c(C.CYAN, "  Observations") + _c(C.DIM, f"  ({r.reference_source})"))
        for item, _, ref, _, _ in r.comparisons:
            unit = ""
            if r.units and item in r.units:
                unit = _c(C.DIM, f"  {r.units[item]}")
            print(f"    {item:<35} {_fmt(ref):>15}{unit}")
    else:
        print(_c(C.CYAN, "  Observations"))
        print(_c(C.DIM, "    None"))
    print()

    # Comparison
    if r.reference_source:
        print(_c(C.CYAN, "  Comparison"))
        print(_c(C.DIM, f"    {'Item':<28} {'Model':>12} {'Observed':>12} {'Error':>9}"))
        for item, model_v, ref, error, passed in r.comparisons:
            status = _c(C.GREEN, "OK") if passed else _c(C.RED, "FAIL")
            err_str = f"{error:.2%}" if error is not None else "--"
            print(f"    {item:<28} {_fmt(model_v):>12} {_fmt(ref):>12} {err_str:>9}  {status}")
        print()

def _render_verdict(r: TestResult):
    # Checks
    print(_c(C.CYAN, "  Checks"))
    if r.error_message:
        print(_c(C.RED, "    [!!] model() raised an exception"))
    elif r.is_exploration:
        print(_c(C.MAGENTA, "    [E] Exploration — result recorded, no pass/fail"))
    elif r.reference_source:
        s1 = _c(C.GREEN, "OK") if r.max_error <= r.tolerance else _c(C.RED, "!!")
        s2 = _c(C.GREEN, "OK") if r.pass_rate >= 0.95 else _c(C.RED, "!!")
        print(f"    [{s1}] Max error {r.max_error:.2%} <= {r.tolerance:.0%}")
        print(f"    [{s2}] Pass rate {r.pass_rate:.0%} >= 95%")
    else:
        print(_c(C.DIM, "    [--] No observations to compare"))
    print()

    # Verdict
    if r.error_message:
        print(_c(C.RED, "  ERROR"))
    elif r.is_exploration:
        print(_c(C.MAGENTA, "  RECORDED"))
    elif r.passed:
        print(_c(C.GREEN, "  PASS"))
    else:
        print(_c(C.RED, "  FAIL"))
        for item, _, _, error, passed in r.comparisons:
            if not passed:
                print(_c(C.DIM, f"    {item}: {error:.2%} error"))
    print()

def _render_context(r: TestResult):
    """Prediction target and commentary."""
    if r.prediction_target:
        print(_c(C.CYAN, "  Testable Against"))
        print(_wrap(r.prediction_target))
        print()

    print(_c(C.CYAN, "  Commentary"))
    if r.commentary:
        print(_wrap(r.commentary))
    else:
        print(_c(C.DIM, "    None"))
    print()


class Renderer:
    """Renders test results to terminal."""

    @staticmethod
    def render_table(table_data: Dict, indent: str = "    "):
        title = table_data.get("title", "")
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        footer = table_data.get("footer", "")

        if title:
            print(f"{indent}{_c(C.BOLD, title)}")
        if not headers or not rows:
            return

        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))

        sep = indent + "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        print(sep)

        hdr = indent + "|"
        for i, h in enumerate(headers):
            hdr += f" {str(h):<{widths[i]}} |"
        print(_c(C.BOLD, hdr))
        print(sep)

        for row in rows:
            line = indent + "|"
            for i, cell in enumerate(row):
                if i < len(widths):
                    s = str(cell)
                    if isinstance(cell, (int, float)):
                        line += f" {s:>{widths[i]}} |"
                    else:
                        line += f" {s:<{widths[i]}} |"
            print(line)
        print(sep)

        if footer:
            print(_c(C.DIM, f"{indent}{footer}"))
        print()

    @staticmethod
    def render_test(result: TestResult):
        _render_header(result)
        _render_specification(result)
        _render_derivation(result)
        _render_results(result)
        _render_verdict(result)
        _render_context(result)

    @staticmethod
    def render_group(group: GroupResult):
        print()
        # Group header with rating
        header = f"  {_gradient(group.title.upper())}"
        grb = _rating_badge(group.max_rating)
        if grb:
            header += f"  {grb}"
        print(header)
        print(_c(C.DIM, "  " + "-" * 60))
        print()
        print(_wrap(group.summary))
        print()

        # Type breakdown (only shown when tests use non-default types)
        counts = group.type_counts
        if any(t != TestType.CONSISTENCY for t in counts):
            parts = [f"{_badge(t)} {n}" for t, n in sorted(counts.items())]
            print(_c(C.DIM, "  Tests: ") + "  ".join(parts))
            print()

        # Rating breakdown (only shown when tests use non-default ratings)
        rcounts = group.rating_counts
        if any(r != Rating.STANDARD for r in rcounts):
            rparts = []
            for level in [Rating.CRITICAL, Rating.STANDARD, Rating.RESEARCH]:
                if level in rcounts:
                    rparts.append(f"{Rating.stars(level)} {Rating.label(level)}: {rcounts[level]}")
            print(_c(C.DIM, "  Ratings: ") + _c(C.DIM, "  ").join(rparts))
            print()

        for test in group.tests:
            Renderer.render_test(test)

        print(_c(C.DIM, "  " + "-" * 60))
        color = C.GREEN if group.passed else C.RED
        print(_c(color, f"  {group.pass_count}/{group.total_count} tests passed"))
        print()


# =============================================================================
# RUNNER
# =============================================================================

def run_test_group(title: str, summary: str, test_classes: List[type],
                   min_rating: int = 0) -> bool:
    """
    Run a group of tests, render results, return True if all passed.

    Args:
        min_rating: Only run tests with rating >= this value.
                    0 = run everything (default).
                    Rating.CRITICAL = only critical tests.
    """
    group = GroupResult(title=title, summary=summary)
    for cls in test_classes:
        test = cls()
        if test.rating >= min_rating:
            group.tests.append(test.run())
    Renderer.render_group(group)
    return group.passed
