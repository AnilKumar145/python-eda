---
title: "Exception Validation, Boundary Values, and Negative Testing"
module: "unit_testing"
unit: "unit_5_5_exceptions_and_edge_cases"
order: 1
type: "knowledge"
difficulty: "intermediate"
tags:
  topics: ["exceptions", "pytest-raises", "boundary-value-analysis", "edge-cases", "negative-testing"]
  subtopics: ["match-regex", "equivalence-partitioning", "fail-fast", "custom-exceptions"]
use_case: "Enforcing absolute safety invariants in blood transfusion ABO compatibility matching algorithms."
domain: "Software Quality Engineering"
duration_hours: 1.25
---

# Lesson 5.5: Exception Validation, Boundary Values, and Negative Testing

---

## 1. The Critical Role of Negative & Exception Testing

Junior developers often write tests that exclusively test the "Happy Path"—valid inputs that succeed predictably. 

In clinical software, **the unhappy path is where patient harm occurs**. If an incompatible blood type is entered (e.g. transfusing Type A red blood cells into a Type B patient), the system must **immediately fail fast**, raise an exception, and block the transfusion order.

```
+--------------------------------------------------------------------------+
|                     Happy Path vs Negative Testing                       |
+--------------------------------------------------------------------------+
| Happy Path: Does the system work when given perfect inputs?              |
| Unhappy Path: Does the system safely reject invalid, dangerous inputs?    |
+--------------------------------------------------------------------------+
```

A robust test suite devotes at least 50% of its test cases to **negative testing** and **boundary verification**.

---

## 2. Exception Assertions with `pytest.raises`

In pytest, you test that a function raises an expected exception using the `pytest.raises` context manager:

```python
import pytest

def test_negative_blood_volume_raises_value_error():
    # If calculate_transfusion_units() raises ValueError -> Test PASSES
    # If it returns normally WITHOUT raising -> Test FAILS
    with pytest.raises(ValueError):
        calculate_transfusion_units(volume_ml=-250)
```

If the code inside the `with` block raises any *other* exception (e.g., `TypeError`), the test fails, highlighting that the wrong exception type was thrown.

---

## 3. Validating Error Messages with the `match` Regex

Asserting only the exception class (`ValueError`) is insufficient if a function can raise `ValueError` for ten different reasons.

The `match` parameter accepts a regular expression (or exact substring) to ensure the error message contains the expected diagnostic explanation:

```python
def test_invalid_blood_group_error_message():
    with pytest.raises(ValueError, match=r"Invalid ABO blood group: 'XYZ'"):
        validate_abo_group("XYZ")
```

If the code raises `ValueError("System error")`, pytest fails the assertion because the message text does not match the regex pattern.

---

## 4. Inspecting Custom Exception Attributes via `exc_info`

Enterprise systems often define custom exception classes carrying structured error codes, affected patient identifiers, and timestamps:

```python
class IncompatibleTransfusionError(Exception):
    def __init__(self, donor_abo: str, recipient_abo: str, risk_level: str):
        super().__init__(f"Incompatible: Donor {donor_abo} to Recipient {recipient_abo}")
        self.donor_abo = donor_abo
        self.recipient_abo = recipient_abo
        self.risk_level = risk_level
```

You can capture the exception instance using `as exc_info` and assert directly against its custom attributes:

```python
def test_transfusion_incompatibility_attributes():
    with pytest.raises(IncompatibleTransfusionError) as exc_info:
        verify_transfusion_compatibility(donor="A", recipient="B")

    # Access the captured exception instance via exc_info.value
    err = exc_info.value
    assert err.donor_abo == "A"
    assert err.recipient_abo == "B"
    assert err.risk_level == "ACUTE_HEMOLYTIC_REACTION"
```

---

## 5. Equivalence Partitioning (EP) Foundations

Testing every possible number is computationally impossible. **Equivalence Partitioning** divides the input domain into groups of values that should be processed the exact same way.

Suppose patient age determines pediatric dosing categories:
- **Partition 1 (Invalid)**: Age $< 0$
- **Partition 2 (Neonate)**: $0 \le \text{Age} \le 28 \text{ days}$
- **Partition 3 (Pediatric)**: $29 \text{ days} \le \text{Age} < 18 \text{ years}$
- **Partition 4 (Adult)**: $\text{Age} \ge 18 \text{ years}$

Instead of testing all 365 days of a year, you test **one representative value** from each partition (e.g. -1, 14 days, 5 years, 35 years).

---

## 6. Boundary Value Analysis (BVA): The 3-Point Boundary Technique

Bugs congregate at the **edges** of partitions (off-by-one errors with `<` vs `<=`).

For any boundary threshold $X$, test:
1. **Just below**: $X - 1$
2. **Exactly on**: $X$
3. **Just above**: $X + 1$

```
                   Invalid | Valid
                     ... 88, 89 | 90, 91 ...
                            ^    ^
                            |    |
           Boundary Just Below  Boundary Exactly On
```

### Example: Critical Hypoxia Threshold ($90\%$ SpO2)
```python
@pytest.mark.parametrize("spo2, expected_alert", [
    (89, True),   # Just below threshold: MUST ALERT
    (90, False),  # Exactly on threshold: NO ALERT
    (91, False),  # Just above threshold: NO ALERT
])
def test_hypoxia_boundary_conditions(spo2, expected_alert):
    assert check_hypoxia_alert(spo2) == expected_alert
```

---

## 7. Testing Corner Cases: None, Empty Strings, Zero, Overflow

Real-world inputs frequently contain corrupted or empty inputs:
- `None` (missing database fields or uninitialized pointers)
- Empty strings `""` or whitespace-only `"   "`
- Zero `0` (divide-by-zero vulnerabilities in concentration math)
- Extreme floating point values (`float('inf')`, `float('nan')`)
- Special Unicode characters (accented patient names, emojis)

```python
@pytest.mark.parametrize("bad_name", [None, "", "   ", "\t\n"])
def test_patient_name_validation_rejects_empty_inputs(bad_name):
    with pytest.raises(ValueError, match="Patient name cannot be blank"):
        PatientRecord(full_name=bad_name)
```

---

## 8. Fail-Fast vs Fail-Safe Architecture in Medical Systems

In general software, systems sometimes "fail soft" (e.g., returning default recommendations when an API fails).

In **clinical medical systems**, silent defaults can be lethal:
- If a patient's allergy profile is unavailable, the system must **NOT** assume zero allergies.
- It must fail fast with an unhandled clinical alert lock, forcing manual physician review.
