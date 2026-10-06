# Learning Outcomes: Unit 5.7 - Test Coverage & Testing Best Practices

By completing this unit, students will be able to:

1. **Quantify Code Coverage with pytest-cov**:
   - Run test suites with `--cov` and `--cov-branch` to measure statement and decision branch coverage.
   - Generate terminal summaries and detailed HTML coverage reports.

2. **Differentiate Statement vs Branch vs Path Coverage**:
   - Understand why 100% statement coverage can still miss critical un-evaluated Boolean branches and failure paths.
   - Design tests that exercise every decision path (`if`, `elif`, `else`, guard clauses).

3. **Configure Enterprise Coverage Rules**:
   - Configure `.coveragerc` or `pyproject.toml` to exclude defensive scaffolding, `__repr__`, abstract methods, and test fixtures.
   - Enforce fail-under thresholds (e.g., `--cov-fail-under=90`) as CI/CD quality gates.

4. **Apply Modern Testing Architecture & Best Practices**:
   - Balance the Testing Pyramid (Unit > Integration > End-to-End).
   - Prevent and eliminate test flakiness, order dependency, and shared mutable state.
   - Write clear Arrange-Act-Assert tests that serve as living clinical specifications.
