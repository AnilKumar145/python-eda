# Learning Outcomes: Unit 5.5 - Exceptions and Edge Cases

By the end of this unit, you will be able to:

1. **Verify Expected Exceptions with `pytest.raises`**: Use context managers to assert that specific error types are raised under failure conditions without halting the test suite.
2. **Inspect Exception Metadata**: Use `match="<regex>"` and the `exc_info` variable to validate error messages, custom error code attributes, and parameter payloads.
3. **Apply Boundary Value Analysis (BVA)**: Test extreme points on both sides of clinical partitions (e.g., test input values $x - \epsilon$, $x$, and $x + \epsilon$).
4. **Author Equivalence Partitioning Tests**: Divide input domains into valid and invalid classes, writing representative test cases for each category.
5. **Enforce Zero Silent-Failure Policies**: Ensure application functions raise explicit, informative exceptions rather than returning `None` or failing open.
