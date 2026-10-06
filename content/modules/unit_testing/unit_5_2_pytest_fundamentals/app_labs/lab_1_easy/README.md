# Application Lab 1: Pediatric Dosage Calculator Test Harness

## Scenario
You are developing safety tests for a pediatric medication calculation service in a children's hospital. Because pediatric dosages depend heavily on body weight and have narrow therapeutic windows, your test suite must enforce strict validation against under-dosing and lethal overdoses.

## Learning Objectives
- Test algorithmic boundary calculations using pytest assertions.
- Group medication-specific tests into structured `Test*` classes.
- Use pytest execution targeting flags (`-k`, `-m`) to test specific drug categories.
- Ensure clear error reporting when calculations encounter negative weights or missing formulations.

## Lab Structure
- `tasks.md`: Detailed specifications for Tasks 1, 2, and 3.
- `starter_code.py`: Starter skeleton containing class stubs and TODO markers.
- `solution/solution.py`: Complete reference implementation.
- `tests.py`: Pytest test suite validating your implementation.

## How to Test
```bash
# Test Reference Solution
pytest content/modules/unit_testing/unit_5_2_pytest_fundamentals/app_labs/lab_1_easy/tests.py -v
```
