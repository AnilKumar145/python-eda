# Application Lab 1: Critical Alert SMS & Pager Notification Gateway

## Scenario
You are building an emergency notification dispatcher that pages attending physicians and triggers on-call SMS alerts when Intensive Care telemetry detects cardiac arrest. Because tests must never send real SMS messages or hit production telco gateways, you will mock the SMS provider, verify exponential backoff retries, and test error isolation.

## Learning Objectives
- Use `unittest.mock.Mock` to isolate network I/O from unit test suites.
- Verify behavior and interaction contracts using `assert_called_once_with()` and `call_count`.
- Simulate intermittent network failures and gateway timeouts using `side_effect`.
- Test fallback behavior when primary communication gateways fail.

## Lab Structure
- `tasks.md`: Detailed specifications for Tasks 1, 2, and 3.
- `starter_code.py`: Starter skeleton containing class stubs and TODO markers.
- `solution/solution.py`: Complete reference implementation.
- `tests.py`: Pytest test suite validating your implementation.

## How to Test
```bash
# Test Reference Solution
pytest content/modules/unit_testing/unit_5_4_mocking_and_isolation/app_labs/lab_1_easy/tests.py -v
```
