---
title: "pytest Architecture, Assertions, and CLI Discovery"
module: "unit_testing"
unit: "unit_5_2_pytest_fundamentals"
order: 1
type: "knowledge"
difficulty: "beginner"
tags:
  topics: ["pytest", "assertions", "test-discovery", "cli-flags", "configuration"]
  subtopics: ["ast-rewriting", "test-runner", "markers", "stdout-capture"]
use_case: "Configuring and commanding automated test suites for pediatric clinical medication calculators."
domain: "Software Quality Engineering"
duration_hours: 1.25
---

# Lesson 5.2: pytest Architecture, Assertions, and CLI Discovery

---

## 1. Why pytest Dominates the Python Testing Ecosystem

Historically, Python developers relied on `unittest`, the built-in testing library modeled after Java's JUnit. While functional, `unittest` requires heavy object-oriented boilerplate:
- Every test file requires subclassing `unittest.TestCase`.
- Assertions require memorizing verbose methods: `self.assertEqual()`, `self.assertTrue()`, `self.assertRaises()`.
- Fixture management relies on rigid `setUp()` and `tearDown()` inheritance hierarchies.

**`pytest`** revolutionized Python testing by introducing a pythonic, lightweight model:
- Write simple functions starting with `test_`.
- Use standard Python `assert` statements.
- Powerful dependency-injected fixtures replace inheritance.
- Massive plugin ecosystem (`pytest-cov`, `pytest-mock`, `pytest-asyncio`).

---

## 2. Automatic Test Discovery Mechanics

When you run `pytest` in your terminal without arguments, pytest performs **automatic test discovery**:

```
[Start directory: Current Working Directory]
       |
       v
Recursively scan all subdirectories (ignoring .git, .pytest_cache)
       |
       v
Collect files matching: test_*.py OR *_test.py
       |
       v
Inside collected files:
  - Collect functions starting with 'test_'
  - Collect classes starting with 'Test' (that do NOT have an __init__ method)
    - Inside 'Test*' classes, collect methods starting with 'test_'
```

```
project_root/
|-- src/
|   `-- dosage.py
`-- tests/
    |-- test_dosage_calculator.py     <-- DISCOVERED (Matches test_*.py)
    |-- clinical_spec_test.py         <-- DISCOVERED (Matches *_test.py)
    `-- helper_fixtures.py            <-- IGNORED (Does not match test pattern)
```

---

## 3. The Power of Assertion Rewriting (AST Introspection)

In standard Python, executing `assert a == b` on failure simply throws `AssertionError` with no additional context.

`pytest` intercepts code during compilation using **Abstract Syntax Tree (AST) Rewriting**. When an assertion fails, pytest evaluates every sub-expression and generates an extraordinarily detailed visual diff:

```python
def test_pediatric_dosage():
    calculated = calculate_dose(weight_kg=12, mg_per_kg=15)
    expected = 185  # Intentionally wrong for illustration

    assert calculated == expected
```

### Visual Output from pytest:
```
    def test_pediatric_dosage():
>       assert calculated == expected
E       AssertionError: assert 180 == 185
E         + 180
E         - 185
```
For nested dictionaries, lists, and strings, pytest displays colored character-by-character diffs, dramatically reducing debugging time!

---

## 4. Test Classes vs Standalone Functions

pytest supports both standalone functions and test classes.

### Standalone Functions (Recommended for 90% of Tests):
```python
def test_zero_weight_dose():
    assert calculate_dose(0, 10) == 0.0

def test_maximum_weight_cap():
    assert calculate_dose(100, 10) == 800.0  # Max ceiling
```

### Test Classes (Ideal for Grouping Scenarios):
Classes can group related tests without needing inheritance from any base class:
```python
class TestParacetamolDosage:
    """Group all tests specific to paracetamol pediatric dosing."""

    def test_infant_weight_band(self):
        assert calculate_paracetamol(5.0) == 75.0

    def test_toddler_weight_band(self):
        assert calculate_paracetamol(14.0) == 210.0
```
> **Warning**: Never define `__init__()` on a test class! Doing so prevents pytest from instantiating it during collection.

---

## 5. Command Line Execution Mastery

Mastering pytest CLI flags allows you to run exactly what you need at light speed:

| Flag | Purpose | Example |
| :--- | :--- | :--- |
| `-v` | **Verbose**: Lists each individual test name and status. | `pytest -v` |
| `-q` | **Quiet**: Minimal output (summary dots only). | `pytest -q` |
| `-s` | **Disable capture**: Prints `print()` output directly to console. | `pytest -s` |
| `-k <expr>` | **Keyword Filter**: Runs tests whose names match the expression. | `pytest -k "dosage and not infant"` |
| `-x` | **Exit immediately**: Stop execution on the very first failure. | `pytest -x` |
| `--maxfail=N`| Stop execution after $N$ failures. | `pytest --maxfail=2` |
| `--lf` | **Last Failed**: Runs only tests that failed in the previous run. | `pytest --lf` |
| `--tb=short` | Display compact single-line failure tracebacks. | `pytest --tb=short` |

### Targeting Specific Files & Methods:
```bash
# Run a single file
pytest tests/test_dosage.py

# Run a single function within a file
pytest tests/test_dosage.py::test_zero_weight_dose

# Run a specific class method
pytest tests/test_dosage.py::TestParacetamolDosage::test_infant_weight_band
```

---

## 6. Marker Fundamentals (`@pytest.mark`)

**Markers** allow you to categorize and decorate tests with metadata tags:

```python
import pytest

@pytest.mark.smoke
def test_critical_heart_rate_monitor():
    assert monitor_status() == "ONLINE"

@pytest.mark.slow
def test_long_running_statistical_aggregate():
    # Simulates heavy analytical crunching
    assert run_full_year_report() is not None
```

### Running Marked Tests:
```bash
# Run only tests marked with 'smoke'
pytest -m smoke

# Run all tests EXCEPT slow ones
pytest -m "not slow"
```

### Built-in Markers:
- `@pytest.mark.skip(reason="...")`: Skips test execution unconditionally.
- `@pytest.mark.skipif(condition, reason="...")`: Skips conditionally (e.g., if OS is Windows).
- `@pytest.mark.xfail`: Marks test as "expected to fail" without breaking the build.

---

## 7. Pytest Configuration: `pytest.ini` vs `pyproject.toml`

Rather than passing flags like `-v --tb=short` manually every time, configure them in `pytest.ini` or modern `pyproject.toml`:

### Modern `pyproject.toml` Configuration:
```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-v --tb=short --strict-markers"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
markers = [
    "smoke: Quick sanity check tests",
    "slow: Tests with duration > 1.0s",
    "integration: Database and API integration tests",
]
```

Using `--strict-markers` prevents typos: if someone marks a test with `@pytest.mark.smkoe` (misspelling), pytest halts with a configuration error instead of silently skipping it!

---

## 8. Troubleshooting Test Failures: Traceback Modes & Standard Output Capture

By default, pytest **captures stdout and stderr**. If you include `print("debugging here")` inside a test that passes, pytest hides the output to keep reports clean.

If the test fails, pytest reveals the captured output under a `--- Captured stdout call ---` banner.

To force `print()` statements to appear live during execution, pass the `-s` flag:
```bash
pytest -s tests/test_dosage.py
```
