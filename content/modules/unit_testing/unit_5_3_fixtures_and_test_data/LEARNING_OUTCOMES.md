# Learning Outcomes: Unit 5.3 - Fixtures and Test Data

By the end of this unit, you will be able to:

1. **Leverage Dependency-Injected Fixtures**: Author `@pytest.fixture` functions and inject them into test arguments cleanly without manual instantiation.
2. **Control Fixture Scopes**: Select appropriate scopes (`function`, `class`, `module`, `session`) to balance execution speed with state isolation.
3. **Manage Safe Setup & Teardown**: Implement deterministic teardown logic using Python generators (`yield`) to clean up open files, temporary resources, and memory caches.
4. **Author Parameterized Test Matrices**: Use `@pytest.mark.parametrize` to execute identical assertion logic across dozens of clinical boundary test vectors with minimal duplication.
5. **Isolate Filesystem Operations with `tmp_path`**: Utilize pytest's built-in `tmp_path` fixture to create, read, and delete temporary clinical files without touching the host filesystem.
