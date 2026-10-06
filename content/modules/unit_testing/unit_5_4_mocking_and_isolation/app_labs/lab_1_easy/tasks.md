# Lab Tasks: Critical Alert SMS & Pager Notification Gateway

## Task 1: Notification Gateway Dispatcher
Implement `EmergencyAlertDispatcher.dispatch_code_blue(patient_id: int, room: str) -> DispatchResult`:
- Attempt to dispatch alert via `primary_sms_client.send_sms(to=on_call_phone, message=...)`.
- If `primary_sms_client` succeeds, return `DispatchResult(delivered=True, channel="PRIMARY_SMS", attempts=1)`.
- If `primary_sms_client` raises an exception:
  - Fall back to `secondary_pager_client.send_page(pager_id=on_call_pager, text=...)`.
  - If pager succeeds, return `DispatchResult(delivered=True, channel="SECONDARY_PAGER", attempts=2)`.
  - If pager also fails, return `DispatchResult(delivered=False, channel="NONE", attempts=2)`.

## Task 2: Mock Interaction Verification
Author unit tests in `tests.py`:
- `test_primary_sms_success_never_calls_secondary_pager()`: Verifies that when primary SMS succeeds, secondary pager is NOT called (`assert_not_called()`).
- `test_primary_sms_failure_triggers_secondary_pager_fallback()`: Configures `primary_sms_client.send_sms.side_effect = TimeoutError`, verifies fallback is called with exact room argument.
- `test_both_channels_failing_reports_failure()`: Configures both clients to raise exceptions and asserts `delivered == False`.
