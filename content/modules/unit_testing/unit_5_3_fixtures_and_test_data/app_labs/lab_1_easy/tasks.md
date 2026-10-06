# Lab Tasks: Clinical Lab Test Reference Range & Reagent Harness

## Task 1: Pathology Analyzer Implementation
Implement `ChemistryAnalyzer.run_test(test_code: str, value: float) -> TestResult`:
- Check that the installed cartridge is not depleted (`remaining_tests > 0`). If depleted, raise `RuntimeError("Cartridge depleted")`.
- Decrement `cartridge.remaining_tests` by 1.
- Evaluate `value` against reference range:
  - If `value < low_bound`: flag is `"LOW"`
  - If `value > high_bound`: flag is `"HIGH"`
  - Otherwise: flag is `"NORMAL"`
- Return `TestResult(test_code=test_code, value=value, flag=flag, remaining_reagent=cartridge.remaining_tests)`.

## Task 2: Reusable Fixtures with Teardown
Implement fixtures in `tests.py`:
- `reagent_cartridge`: Yields a cartridge with 5 tests remaining; upon teardown, sets `cartridge.is_unlocked = False` and registers disposal.
- `calibrated_analyzer`: Injects `reagent_cartridge` and returns an initialized `ChemistryAnalyzer`.

## Task 3: Parameterized Assertion Suite & File Logging
- Write a `@pytest.mark.parametrize` suite covering normal, low, and high values across multiple test panels (e.g. Glucose, Sodium, Potassium).
- Use `tmp_path` to export run results to an audit JSON file and assert file integrity.
