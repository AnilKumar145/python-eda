# Unit 2.4: Asynchronous Programming - Exercises

## Overview
Concept-focused drills testing asynchronous coroutine creation with `async`/`await`, concurrent execution with `asyncio.gather()`, timeout control with `asyncio.wait_for()`, and task cancellation handling.

**Target File**: `unit_2_4_asynchronous_programming_exercises.py`

---

## Exercise List

### Exercise 1: Basic Coroutine Invocation
**Objective**: Define and await an asynchronous multiplier function using `asyncio.sleep()`.

### Exercise 2: Concurrent Gathering with `asyncio.gather()`
**Objective**: Execute multiple asynchronous tasks concurrently and verify that total execution time reflects concurrent overlapping.

### Exercise 3: Timeout Enforcement with `asyncio.wait_for()`
**Objective**: Wrap an asynchronous coroutine in `asyncio.wait_for()`, catching `asyncio.TimeoutError` when simulated delay exceeds the configured timeout threshold.

### Exercise 4: Graceful Task Cancellation
**Objective**: Cancel a running `asyncio.Task` using `task.cancel()` and handle `asyncio.CancelledError` cleanly.
