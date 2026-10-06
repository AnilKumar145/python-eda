---
title: "pytest Fixtures, Teardown Lifecycles, and Parameterization"
module: "unit_testing"
unit: "unit_5_3_fixtures_and_test_data"
order: 1
type: "knowledge"
difficulty: "intermediate"
tags:
  topics: ["pytest", "fixtures", "parameterize", "tmp_path", "setup-teardown"]
  subtopics: ["dependency-injection", "fixture-scope", "yield-fixtures", "data-factories"]
use_case: "Creating robust test fixtures and parameterized boundary suites for clinical pathology laboratory analyzers."
domain: "Software Quality Engineering"
duration_hours: 1.5
---

# Lesson 5.3: pytest Fixtures, Teardown Lifecycles, and Parameterization

---

## 1. What Are Pytest Fixtures & Why Dependency Injection Wins

In classic xUnit frameworks, sharing setup code across tests requires class inheritance (`setUp()` methods). As test suites grow, this leads to deep, brittle inheritance hierarchies where tests inherit setup they do not need.

`pytest` replaces class inheritance with **Dependency Injection via Fixtures**:
- A fixture is a plain Python function decorated with `@pytest.fixture`.
- Tests declare which fixtures they need simply by naming them as **function parameters**.
- Pytest inspects the test's signature, executes the fixture, and passes its return value into the test.

```
       @pytest.fixture
       def sample_patient():
           return Patient(mrn="MRN-101", name="Sarah Connor")
                      |
                      | pytest injects sample_patient
                      v
       def test_patient_admission(sample_patient):
           assert sample_patient.mrn == "MRN-101"
```

---

## 2. Anatomy of a Fixture & Test Injection

Fixtures provide a clean separation of concerns: tests focus exclusively on *acting* and *asserting*, while fixtures handle *arranging*.

```python
import pytest

@pytest.fixture
def empty_blood_gas_panel():
    """Provides a fresh, uncalibrated laboratory panel."""
    return BloodGasAnalyzer(serial_no="BGA-900", calibrated=False)

def test_initial_analyzer_is_uncalibrated(empty_blood_gas_panel):
    assert empty_blood_gas_panel.is_ready() is False
    assert empty_blood_gas_panel.serial_no == "BGA-900"
```

If multiple tests need `empty_blood_gas_panel`, they all request it. Each test receives its own fresh instance, ensuring zero test contamination.

---

## 3. Fixture Scopes: Performance vs Isolation

By default, a fixture has **`function` scope**—it is created anew for every single test function that requests it.

If a fixture performs expensive initialization (e.g., spinning up an in-memory SQLite schema or parsing a large JSON formulary), re-running it for hundreds of tests slows the suite down. pytest allows configuring the **scope**:

| Scope | Lifetime | Best For |
| :--- | :--- | :--- |
| `scope="function"` *(Default)* | Created and destroyed for **each test**. | Mutable domain models, isolated objects. |
| `scope="class"` | Created once per **test class**. | Class-level test scenarios. |
| `scope="module"` | Created once per **Python file**. | Read-only reference tables, static datasets. |
| `scope="session"` | Created once for the **entire test run**.| Docker testcontainers, heavy database engines. |

```python
@pytest.fixture(scope="module")
def clinical_reference_ranges():
    """Heavy lookup dictionary loaded once per module."""
    return load_loinc_reference_data_from_disk()
```

> **Warning**: Never mutate objects returned by a `module` or `session` scoped fixture! Doing so leaks state between tests, causing order-dependent flakiness.

---

## 4. Setup & Teardown with the `yield` Keyword

Real-world test fixtures frequently manage external resources that must be cleaned up—open file handles, database connections, or background worker threads.

In pytest, you define teardown simply by replacing `return` with **`yield`**:

```python
@pytest.fixture
def active_database_connection():
    # 1. SETUP (Runs BEFORE the test)
    conn = sqlite3.connect(":memory:")
    init_schema(conn)

    yield conn  # The test executes while paused here!

    # 2. TEARDOWN (Guaranteed to run AFTER the test, even if it fails!)
    conn.close()
```

```
[Start Test]
       |
       v
Execute code BEFORE 'yield' (Setup)
       |
       v
Execute Test Function with yielded value
       |
       v
Execute code AFTER 'yield' (Teardown / Cleanup)
       |
       v
[Test Complete]
```

---

## 5. Composing Fixtures (Fixtures Requesting Fixtures)

Fixtures are modular and can request other fixtures, building complex dependency graphs cleanly:

```python
@pytest.fixture
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Requests db_engine fixture automatically!"""
    with Session(db_engine) as session:
        yield session

@pytest.fixture
def admitted_patient(db_session):
    """Requests db_session and inserts test record."""
    patient = Patient(mrn="MRN-777", full_name="John Doe")
    db_session.add(patient)
    db_session.commit()
    return patient

def test_patient_discharge(db_session, admitted_patient):
    admitted_patient.status = "DISCHARGED"
    db_session.commit()
    assert admitted_patient.status == "DISCHARGED"
```

---

## 6. Parameterized Testing with `@pytest.mark.parametrize`

Clinical systems frequently have dozens of boundary cases (e.g., pH ranges: acidic, normal, alkalotic). Writing separate test functions for each boundary duplicates assertion code.

**`@pytest.mark.parametrize`** runs a single test function multiple times across an array of input vectors:

```python
@pytest.mark.parametrize("ph_value, expected_classification", [
    (7.20, "ACIDOSIS"),
    (7.34, "ACIDOSIS"),
    (7.35, "NORMAL"),     # Lower normal bound
    (7.40, "NORMAL"),     # Median physiological
    (7.45, "NORMAL"),     # Upper normal bound
    (7.46, "ALKALOSIS"),  # Boundary trigger
    (7.60, "ALKALOSIS"),
])
def test_arterial_blood_gas_ph_classification(ph_value, expected_classification):
    # This single test executes 7 separate times!
    status = classify_arterial_ph(ph_value)
    assert status == expected_classification
```

In the test runner output, each parameter tuple appears as an independently verifiable test:
```
test_abg.py::test_ph[7.2-ACIDOSIS] PASSED
test_abg.py::test_ph[7.35-NORMAL] PASSED
test_abg.py::test_ph[7.46-ALKALOSIS] PASSED
```

---

## 7. Isolating Filesystem Tests with Built-in `tmp_path`

Tests that create real files on disk risk leaving garbage files behind or stepping on each other during parallel test runs.

pytest provides the built-in **`tmp_path`** fixture. It injects a unique, isolated `pathlib.Path` pointing to a temporary directory created exclusively for that test invocation:

```python
def test_export_lab_results_to_csv(tmp_path):
    # tmp_path is a standard pathlib.Path object
    export_file = tmp_path / "lab_results_export.csv"

    records = [{"test": "Potassium", "value": 4.1}]
    export_to_csv(records, output_path=export_file)

    # Verify file was written
    assert export_file.exists()
    content = export_file.read_text()
    assert "Potassium,4.1" in content
    # Directory is automatically deleted by pytest on cleanup!
```

---

## 8. Enterprise Test Data Factory Patterns & Fixture Anti-Patterns

### Anti-Pattern 1: The Monolithic Fixture
Creating a single giant `setup_everything` fixture that builds 10 wards, 50 doctors, and 200 patients when a test only needs 1 doctor.
- **Fix**: Use small, granular fixtures or factory functions (`create_patient(mrn="...")`).

### Anti-Pattern 2: Hidden Assertions Inside Fixtures
Putting `assert` statements inside fixtures makes it difficult to diagnose whether the test failed or the fixture failed. Keep assertions inside test functions.
