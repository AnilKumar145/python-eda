# Unit 2.1: Concurrency Fundamentals - Exercises

## Overview
Concept-focused drills testing workload classification (I/O-bound vs CPU-bound), Amdahl's Law theoretical speedup calculations, and selecting concurrency models based on task constraints.

**Target File**: `unit_2_1_concurrency_fundamentals_exercises.py`

---

## Exercise List

### Exercise 1: Workload Characterization Classifier
**Objective**: Analyze task profiles and classify tasks into `"IO_BOUND"` or `"CPU_BOUND"`.

### Exercise 2: Amdahl's Law Speedup Calculator
**Objective**: Implement a function calculating theoretical speedup given the parallelizable fraction $P$ and number of processors $N$.

### Exercise 3: Concurrency Model Selector
**Objective**: Implement an architectural selector that chooses between `"ASYNCIO"`, `"THREADING"`, and `"MULTIPROCESSING"` based on workload type, socket volume, and CPU intensity.

### Exercise 4: Simulating Workload Overlap
**Objective**: Demonstrate how overlapping two independent I/O tasks reduces total elapsed execution time compared to sequential execution.
