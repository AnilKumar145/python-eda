# Learning Outcomes: Unit 5.4 - Mocking and Isolation

By the end of this unit, you will be able to:

1. **Understand When and Why to Mock**: Differentiate between state verification and behavior verification, identifying external boundaries (network calls, SMS gateways, payment APIs, hardware) that require mocking.
2. **Utilize Mock and MagicMock**: Configure mock return values (`return_value`), simulated exceptions (`side_effect = TimeoutError`), and verify call counts (`assert_called_once()`).
3. **Master the `patch` Mechanism**: Safely intercept functions, methods, and classes at runtime using `@patch` decorators and `with patch(...)` context managers where the target is imported.
4. **Spy on Real Collaborators**: Track invocations, arguments passed (`assert_called_with(...)`), and call order on system boundaries.
5. **Prevent Over-Mocking Antipatterns**: Avoid brittle tests that mock internal private methods, keeping tests focused on public interfaces and external I/O boundaries.
