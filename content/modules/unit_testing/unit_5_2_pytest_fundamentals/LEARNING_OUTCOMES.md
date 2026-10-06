# Learning Outcomes: Unit 5.2 - pytest Fundamentals

By the end of this unit, you will be able to:

1. **Understand pytest Discovery Rules**: Explain how pytest locates tests across directory trees matching `test_*.py` and `*_test.py`, test classes named `Test*`, and test functions named `test_*()`.
2. **Harness Assertion Rewriting**: Write natural Python `assert` statements without boilerplates, leveraging pytest's AST rewriting to display detailed expression comparisons and diffs upon failure.
3. **Execute Targeted Test Runs**: Command test runs using CLI arguments: `-k <expression>` for keyword filtering, `-m <marker>` for marker tags, `-x` for exit-on-first-failure, and `--maxfail=<N>`.
4. **Configure pytest Behavior**: Author `pytest.ini` and `pyproject.toml` configuration files with default flags, test path declarations, and marker definitions.
5. **Debug Test Failures with Traceback Controls**: Use `--tb=short`, `--tb=native`, `-s` (disable stdout capturing), and `--pdb` to rapidly isolate root causes.
