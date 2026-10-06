# Unit 5.7: Test Coverage and Testing Best Practices

---

## Part 1: Clinical & Conceptual Motivation

In healthcare software engineering, untested code is an unmitigated liability. Imagine an electronic chemotherapy administration system that calculates intravenous infusion rates. If an error handling branch that checks for abnormal patient creatinine levels is never executed during automated testing, an undetected bug could cause kidney failure or fatal drug toxicity in a real patient.

Measuring **code coverage** provides visibility into which lines, branches, and execution paths your automated test suite touches, and more importantly, **which paths remain completely untested**.

However, high code coverage alone is not a guarantee of defect-free code:
- **100% statement coverage does not mean zero bugs.** A test might execute every line of code without asserting any return values or without testing boundary conditions.
- **Good testing requires quality assertions, branch coverage, and edge case resilience**, backed by strict automated quality gates.

---

## Part 2: Core Concepts & Definitions

### 1. Statement Coverage (Line Coverage)
The percentage of executable program lines touched at least once by the test suite:
$$\text{Statement Coverage} = \frac{\text{Executed Statements}}{\text{Total Executable Statements}} \times 100\%$$

### 2. Branch Coverage (Decision Coverage)
Evaluates whether every branch of each conditional control structure (both the `True` and `False` directions of every `if` statement) has been exercised:
$$\text{Branch Coverage} = \frac{\text{Executed Decision Branches}}{\text{Total Decision Branches}} \times 100\%$$

> **The Trap of Line Coverage**: Consider an `if` block without an `else`. If a test only exercises the `True` condition, statement coverage may report 100%, but branch coverage will detect that the `False` decision was never verified.

### 3. The Test Pyramid
A sustainable automated testing distribution:
- **Unit Tests (70-80%)**: Fast (milliseconds), isolated, in-memory, testing individual functions and classes.
- **Integration Tests (15-20%)**: Testing database repositories, serialized API endpoints, and component collaborations.
- **End-to-End / Acceptance Tests (5-10%)**: Slow, realistic, testing entire clinical user flows across the full stack.

### 4. Quality Gates (`--cov-fail-under`)
A continuous integration (CI) checkpoint that rejects pull requests if overall repository coverage drops below a mandated threshold (e.g., 90% or 95% in medical informatics).

---

## Part 3: Code Architecture & Implementation Patterns

### Running pytest with Coverage
In Python, coverage is measured using the `pytest-cov` plugin and underlying `coverage.py` engine:

```bash
# Basic coverage report
pytest --cov=src

# Coverage with missing line numbers and branch coverage
pytest --cov=src --cov-report=term-missing --cov-branch

# HTML visual report (generated in htmlcov/index.html)
pytest --cov=src --cov-report=html --cov-branch

# Enforcing a minimum coverage threshold
pytest --cov=src --cov-fail-under=90
```

### Configuring `.coveragerc` or `pyproject.toml`
Enterprise projects define explicit exclusion rules so developers don't write useless tests just to satisfy coverage counters:

```ini
# .coveragerc
[run]
branch = True
source = content/modules

[report]
show_missing = True
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

### The Anatomy of High-Value Unit Tests: AAA Pattern
Always adhere to **Arrange - Act - Assert**:
```python
def test_ventilator_alarm_triggers_on_low_tidal_volume():
    # 1. Arrange: Setup domain objects and state
    monitor = VentilatorMonitor(min_tidal_volume_ml=300)
    
    # 2. Act: Execute the single method under test
    alarm_status = monitor.evaluate_breath(actual_tidal_volume_ml=220)
    
    # 3. Assert: Verify the outcome precisely
    assert alarm_status.is_critical is True
    assert alarm_status.reason == "LOW_TIDAL_VOLUME"
```

---

## Part 4: Common Pitfalls & Anti-Patterns

### 1. "Assertion-Free" Coverage (The False Confidence Trap)
Writing tests that invoke methods purely to increase coverage numbers without asserting behavior:
```python
# ANTI-PATTERN: High coverage, ZERO safety!
def test_calculate_dosage():
    calculate_pediatric_dose(weight_kg=15.0, mg_per_kg=10.0)
    # No assert statement! If the function returns a negative number or None, the test passes!
```
**Fix**: Every test must contain unambiguous, strict assertions verifying both values and state changes.

### 2. Flaky Tests
A test that passes sometimes and fails other times without code changes:
- **Root causes**: Unseeded random numbers (`random.choice`), real system clocks (`datetime.now()`), network dependencies, unisolated database records, or shared module-level state.
- **Fix**: Inject mock clocks, seed random generators, and isolate database state with in-memory engines and transaction rollbacks.

### 3. Testing Implementation Details Instead of Contracts
Asserting private attributes (`_internal_cache`) instead of observable public behaviors. When internal code is refactored, tests break even though the behavior remains correct.

---

## Part 5: Production Patterns & Enterprise Recipes

### Pattern: Coverage-Gated Clinical Audit Logger
In hospital compliance systems, every sensitive action (e.g., viewing an VIP patient's chart, prescribing controlled substances) must be recorded in an immutable audit ledger:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class AuditEntry:
    entry_id: str
    user_id: str
    patient_id: str
    action: str
    timestamp: datetime
    is_sensitive: bool


class ClinicalAuditLogger:
    SENSITIVE_ACTIONS = {"VIEW_PSYCH_NOTES", "PRESCRIBE_OPIOID", "OVERRIDE_DRUG_ALLERGY"}

    def __init__(self):
        self._entries: List[AuditEntry] = []

    def log_event(self, entry_id: str, user_id: str, patient_id: str, action: str) -> AuditEntry:
        if not entry_id or not user_id or not patient_id or not action:
            raise ValueError("All audit log fields must be non-empty strings.")

        is_sensitive = action.strip().upper() in self.SENSITIVE_ACTIONS
        entry = AuditEntry(
            entry_id=entry_id.strip(),
            user_id=user_id.strip(),
            patient_id=patient_id.strip(),
            action=action.strip().upper(),
            timestamp=datetime.now(),
            is_sensitive=is_sensitive
        )
        self._entries.append(entry)
        return entry

    def get_sensitive_events_for_patient(self, patient_id: str) -> List[AuditEntry]:
        target = patient_id.strip()
        return [e for e in self._entries if e.patient_id == target and e.is_sensitive]
```

To achieve 100% branch coverage on this component, tests must cover:
1. Normal non-sensitive event logging.
2. Sensitive action event logging (verifying `is_sensitive=True`).
3. Validation failures for empty fields (exercising the guard clause).
4. Querying sensitive events where matches exist and where no matches exist.

---

## Part 6: Hands-On Walkthrough & Analysis

Let's inspect how to test both branches of a decision:

```python
def classify_triage_acuity(systolic_bp: int, heart_rate: int) -> str:
    if systolic_bp < 90 or heart_rate > 130:
        return "RED_RESUSCITATION"
    elif systolic_bp < 100 or heart_rate > 110:
        return "ORANGE_EMERGENT"
    else:
        return "GREEN_NON_URGENT"
```

To obtain 100% branch coverage:
- Test 1: `systolic_bp < 90` (e.g. 80, 100) -> `RED_RESUSCITATION`
- Test 2: `heart_rate > 130` (e.g. 120, 140) -> `RED_RESUSCITATION`
- Test 3: `systolic_bp < 100` (e.g. 95, 80) -> `ORANGE_EMERGENT`
- Test 4: `heart_rate > 110` (e.g. 115, 120) -> `ORANGE_EMERGENT`
- Test 5: Normal vitals (e.g. 120, 75) -> `GREEN_NON_URGENT`

Missing any of these compound Boolean clauses leaves decision branches un-evaluated.

---

## Part 7: Exercises & Application Lab Preview

- **Exercises (`exercises/`)**:
  - Exercise 1: Build comprehensive branch-covering test suites for clinical dosage boundary checks.
  - Exercise 2: Identify and fix under-tested conditional paths.
  - Exercise 3: Implement an isolated audit trail accumulator and verify branch coverage.
- **Application Lab (`app_labs/lab_1_easy/`)**:
  - Build and thoroughly test a **Clinical Audit Log Quality Gate and Coverage Harness**, validating HIPAA-compliant immutable event logging, tamper detection, and querying with 100% branch coverage.

---

## Part 8: Key Takeaways & Review Checklist

- [ ] Statement coverage measures executed lines; branch coverage measures evaluated decision paths.
- [ ] Strive for high branch coverage on core domain logic, but never sacrifice assertion quality for artificial metrics.
- [ ] Use `--cov-branch` and `--cov-report=term-missing` to spot untested lines and edge cases.
- [ ] Configure exclusions (`pragma: no cover`) for boilerplate and untestable infrastructure scaffolding.
- [ ] Keep tests fast, independent, deterministic, and isolated.
