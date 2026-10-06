# Application Lab 1: Clinical Lab Test Reference Range & Reagent Harness

## Scenario
You are building an automated quality control (QC) and testing system for a clinical pathology laboratory. Automated chemistry analyzers require consumable reagent cartridges with finite test capacities. You will implement an analyzer simulator and a comprehensive pytest suite featuring reusable fixtures, yield-based cartridge disposal, parameterized reference range matrices, and temporary result log persistence.

## Learning Objectives
- Design lifecycle fixtures with automatic teardown using Python generators (`yield`).
- Test multiple pathology reference ranges using `@pytest.mark.parametrize`.
- Isolate file export and audit logging using pytest's `tmp_path` fixture.
- Inject dependent fixtures (analyzer requiring calibrated reagent cartridge).

## Lab Structure
- `tasks.md`: Detailed specifications for Tasks 1, 2, and 3.
- `starter_code.py`: Starter skeleton containing class stubs and TODO markers.
- `solution/solution.py`: Complete reference implementation.
- `tests.py`: Pytest test suite validating your implementation.

## How to Test
```bash
# Test Reference Solution
pytest content/modules/unit_testing/unit_5_3_fixtures_and_test_data/app_labs/lab_1_easy/tests.py -v
```
