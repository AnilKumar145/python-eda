# Unit 1.5: Thread Pools - Exercises

## Overview
Concept-focused drills testing `ThreadPoolExecutor`, task dispatching with `submit()` and `map()`, asynchronous completion iteration with `as_completed()`, and worker exception handling.

**Target File**: `unit_1_5_thread_pools_exercises.py`

---

## Exercise List

### Exercise 1: Task Dispatch and Future Resolution
**Objective**: Submit multiple compute jobs using `executor.submit()`, collect the returned `Future` instances, and resolve their return values.

### Exercise 2: Parallel Batch Transformation with `executor.map()`
**Objective**: Use `executor.map()` to apply a transformation across a dataset concurrently and collect the ordered results.

### Exercise 3: Dynamic Result Streaming with `as_completed()`
**Objective**: Submit tasks with varying synthetic execution delays and process them in order of completion using `concurrent.futures.as_completed()`.

### Exercise 4: Trapping Worker Exceptions
**Objective**: Submit a batch of tasks where certain inputs trigger exceptions, catching the exceptions on the main thread via `future.result()` without crashing.
