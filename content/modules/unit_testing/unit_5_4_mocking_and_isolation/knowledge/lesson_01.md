---
title: "Test Isolation with Mock, MagicMock, and Patch"
module: "unit_testing"
unit: "unit_5_4_mocking_and_isolation"
order: 1
type: "knowledge"
difficulty: "intermediate"
tags:
  topics: ["mocking", "unittest-mock", "patch", "magicmock", "side-effect"]
  subtopics: ["test-doubles", "behavior-verification", "where-to-patch", "pytest-mock"]
use_case: "Isolating emergency SMS and pager notification systems from real external telco networks in clinical test suites."
domain: "Software Quality Engineering"
duration_hours: 1.5
---

# Lesson 5.4: Test Isolation with Mock, MagicMock, and Patch

---

## 1. Why Mocking is Required & The Test Double Taxonomy

When testing business logic in modern applications, classes depend on external collaborators:
- A payment gateway (Stripe API)
- A clinical SMS/Pager gateway (Twilio)
- A third-party radiology imaging server (PACS)
- A production database

If your unit tests call the real Twilio API:
1. Tests fail if your internet connection drops.
2. Tests cost money for every SMS sent!
3. Doctors receive false alarm pagers at 2:00 AM during continuous integration runs!
4. Tests take 800 milliseconds per network call instead of 2 milliseconds.

### Gerard Meszaros' Test Double Taxonomy:
```
+--------------------------------------------------------------------------+
|                               TEST DOUBLES                               |
+--------------------------------------------------------------------------+
| 1. Dummy: Passed around but never actually used (e.g., filler parameter).|
| 2. Stub : Provides pre-canned answers to calls (hardcoded return value). |
| 3. Spy  : Records how it was called (tracks call count, arguments).     |
| 4. Mock : Programmed with expectations; verifies calls occurred.         |
| 5. Fake : Working implementation with a shortcut (e.g., in-memory SQLite)|
+--------------------------------------------------------------------------+
```

---

## 2. `unittest.mock.Mock` vs `MagicMock`

Python's standard library provides `unittest.mock`:

```python
from unittest.mock import Mock, MagicMock

# Standard Mock
m = Mock()
m.some_method()  # Works! Dynamically creates attributes on the fly

# MagicMock: A subclass of Mock that implements Python "dunder" magic methods
mm = MagicMock()
len(mm)          # Implements __len__ -> returns 0 by default
str(mm)          # Implements __str__
iter(mm)         # Implements __iter__
```

> **Rule of Thumb**: Use `MagicMock` by default whenever the object will be passed to functions that call `len()`, iterate (`for x in obj:`), or use context managers (`with obj:`).

---

## 3. Configuring Behaviors: `return_value` vs `side_effect`

A mock can be programmed to return fixed data or simulate catastrophic errors:

### Setting a Static `return_value`:
```python
sms_client = Mock()
sms_client.send_sms.return_value = {"status": "DELIVERED", "id": "MSG-99"}

res = sms_client.send_sms(to="+15550199", text="Code Blue in ICU")
assert res["status"] == "DELIVERED"
```

### Simulating Errors with `side_effect`:
Assigning an exception class or instance to `side_effect` raises the exception when invoked:
```python
# Simulates gateway timeout
sms_client.send_sms.side_effect = TimeoutError("Connection to SMS Gateway timed out")

try:
    sms_client.send_sms(to="+15550199", text="Test")
except TimeoutError:
    print("Caught simulated network failure!")
```

### Dynamic Responses with Callables:
You can assign a function or list of return values to `side_effect`:
```python
# Sequential responses on successive calls:
sms_client.send_sms.side_effect = [
    ConnectionError("Attempt 1 failed"),
    {"status": "DELIVERED"}  # Attempt 2 succeeds
]
```

---

## 4. The Golden Rule of Patching: "Where an Object is Looked Up"

The most frequent bug developers encounter with `@patch` is patching the wrong module path.

### The Rule:
> **"Patch an object where it is used (looked up), NOT where it is originally declared!"**

Suppose module `alerts.py` imports `send_sms` from `gateway.py`:
```python
# src/alerts.py
from src.gateway import send_sms

def dispatch_code_blue(room):
    send_sms("Code Blue in " + room)
```

### The Correct vs Wrong Patch:
```python
# WRONG: gateway.send_sms has already been imported into alerts.py!
@patch("src.gateway.send_sms")  # Alerts.py still points to the old reference!

# CORRECT: Patch the reference as looked up inside alerts.py!
@patch("src.alerts.send_sms")
def test_dispatch(mock_send):
    dispatch_code_blue("OR-3")
    mock_send.assert_called_once_with("Code Blue in OR-3")
```

---

## 5. Patching Styles: Decorator vs Context Manager

### Style A: Function Decorator
Best for an entire test function:
```python
from unittest.mock import patch

@patch("src.alerts.send_sms")
def test_alert_decorator(mock_send):
    mock_send.return_value = True
    dispatch_code_blue("Ward-B")
    mock_send.assert_called_once()
```

### Style B: Context Manager
Best when you only want the mock active for a specific line of code:
```python
def test_alert_context_manager():
    with patch("src.alerts.send_sms") as mock_send:
        mock_send.return_value = True
        dispatch_code_blue("Ward-B")
        mock_send.assert_called_once()
    # Here, original send_sms is automatically restored!
```

---

## 6. Asserting Interactions: Spying on Collaborators

Mocks record every call made to them, allowing comprehensive behavior verification:

```python
mock_logger = Mock()

mock_logger.log_incident("INC-101", severity="CRITICAL")

# 1. Verify call occurred exactly once
mock_logger.log_incident.assert_called_once()

# 2. Verify exact arguments passed
mock_logger.log_incident.assert_called_once_with("INC-101", severity="CRITICAL")

# 3. Verify call count
assert mock_logger.log_incident.call_count == 1

# 4. Verify mock was NOT called
mock_logger.delete_log.assert_not_called()
```

---

## 7. Mocking Network APIs & HTTP Clients

When code uses `requests.get` or `httpx.get`:

```python
import requests

def fetch_patient_allergies(patient_id):
    resp = requests.get(f"https://ehr.hospital.org/api/allergies/{patient_id}")
    if resp.status_code == 200:
        return resp.json()
    raise RuntimeError("API Error")

# Test with mock:
@patch("requests.get")
def test_fetch_allergies_success(mock_get):
    # Configure mock response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"allergen": "PENICILLIN", "severity": "SEVERE"}]
    mock_get.return_value = mock_response

    results = fetch_patient_allergies(101)
    assert len(results) == 1
    assert results[0]["allergen"] == "PENICILLIN"
```

---

## 8. Over-Mocking Pitfalls: Fragile Tests & Mock Drift

### Pitfall 1: Mocking Everything (Testing Nothing)
If you mock the repository, the service, the validator, and the serializer, you are simply testing that mock A called mock B. A complete rewrite of internal code might break the test even though the feature still works!
- **Rule**: Mock **only** external I/O boundaries (HTTP, DB, Hardware). Let real domain models and calculation classes interact normally.

### Pitfall 2: Mock Drift
A third-party API changes its response schema from `{"status": "ok"}` to `{"state": "SUCCESS"}`. Your mock still returns `{"status": "ok"}`, so your unit tests pass, but your production app crashes!
- **Fix**: Supplement mocked unit tests with contract or integration tests.
