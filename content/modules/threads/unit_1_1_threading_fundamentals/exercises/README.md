# Unit 1.1: Threading Fundamentals - Exercises

## Overview
Concept-focused drills testing the implementation of thread instantiation, argument passing, thread lifecycle verification, and synchronous join coordination.

**Target File**: `unit_1_1_threading_fundamentals_exercises.py`

---

## Exercise List

### Exercise 1: Basic Thread Instantiation and Execution
**Objective**: Create a `threading.Thread` targeting a callable that appends a value to an output list, and wait for its completion using `.join()`.

### Exercise 2: Parameterized Thread Execution
**Objective**: Launch a thread that takes positional and keyword arguments via `args` and `kwargs` and stores the processed product into an external accumulator.

### Exercise 3: Parallel Batch Thread Coordinator
**Objective**: Write a function that accepts a list of payloads, launches a dedicated worker thread for each payload, and blocks until all threads have completed execution.

### Exercise 4: Thread State and Alive Detection
**Objective**: Inspect whether a thread is active before and after calling `.join()` and return its active status lifecycle tuple.
