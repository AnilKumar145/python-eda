# Application Lab 1: Emergency Triage Patient Scoring Test Suite

## Scenario
You are building an automated testing framework for an Emergency Department Triage System. Clinical guidelines require accurate risk stratification based on adult physiological parameters. You will implement the triage scoring algorithm and author an isolated test harness applying the Arrange-Act-Assert (AAA) pattern.

## Learning Objectives
- Implement clinical boundary algorithms with strict input validation.
- Author isolated unit tests using the AAA (Arrange, Act, Assert) structure.
- Write assertions covering critical boundary cases (e.g. hypoxic vs normal oxygen saturation).
- Validate exception throwing on invalid or missing clinical inputs.

## Lab Structure
- `tasks.md`: Detailed specifications for Tasks 1, 2, and 3.
- `starter_code.py`: Starter skeleton containing class stubs and TODO markers.
- `solution/solution.py`: Complete reference implementation.
- `tests.py`: Pytest test suite validating your implementation.

## How to Test
```bash
# Test Reference Solution
pytest content/modules/unit_testing/unit_5_1_testing_fundamentals/app_labs/lab_1_easy/tests.py -v
```
