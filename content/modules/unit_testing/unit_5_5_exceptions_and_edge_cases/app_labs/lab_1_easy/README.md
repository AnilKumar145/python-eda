# Application Lab 1: Blood Bank Transfusion Compatibility Guard

## Scenario
You are developing safety software for a hospital regional blood transfusion service. Mismatched blood product transfusions trigger Acute Hemolytic Transfusion Reactions (AHTR), which are frequently fatal. You will build a strict compatibility matching engine and an exhaustive negative test suite verifying exception raising, Rh factor matching, and unphysiological payload rejection.

## Learning Objectives
- Assert custom domain exceptions carrying structured clinical metadata using `pytest.raises`.
- Use regex matching with `match="..."` to verify diagnostic safety warnings.
- Perform boundary value analysis on unit volume, expiration hours, and hematocrit levels.
- Test rejection of edge cases (corrupted blood bag barcodes, empty strings, null values).

## Lab Structure
- `tasks.md`: Detailed specifications for Tasks 1, 2, and 3.
- `starter_code.py`: Starter skeleton containing class stubs and TODO markers.
- `solution/solution.py`: Complete reference implementation.
- `tests.py`: Pytest test suite validating your implementation.

## How to Test
```bash
# Test Reference Solution
pytest content/modules/unit_testing/unit_5_5_exceptions_and_edge_cases/app_labs/lab_1_easy/tests.py -v
```
