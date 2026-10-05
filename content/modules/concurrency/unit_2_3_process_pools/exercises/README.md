# Unit 2.3: Process Pools - Exercises

## Overview
Concept-focused drills testing `ProcessPoolExecutor`, batch mapping with chunking, individual future submission, and worker exception isolation across separate CPU worker processes.

**Target File**: `unit_2_3_process_pools_exercises.py`

---

## Exercise List

### Exercise 1: Parallel Factorial Mapping
**Objective**: Use `ProcessPoolExecutor.map()` to calculate the factorial of a list of numbers across multiple CPU worker processes.

### Exercise 2: Chunked Batch Processing
**Objective**: Optimize high-volume task dispatch using the `chunksize` parameter in `executor.map()`.

### Exercise 3: Dynamic Result Streaming with `as_completed()`
**Objective**: Submit compute tasks of varying complexity to a process pool and gather results in completion order.

### Exercise 4: Worker Exception Handling in Process Pools
**Objective**: Isolate and trap exceptions raised within child worker processes without crashing the process pool.
