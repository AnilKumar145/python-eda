# Unit 2.2: Multiprocessing - Exercises

## Overview
Concept-focused drills testing `multiprocessing.Process` creation, inter-process communication using `multiprocessing.Queue` and `multiprocessing.Pipe`, and memory isolation verification.

**Target File**: `unit_2_2_multiprocessing_exercises.py`

---

## Exercise List

### Exercise 1: Multi-Process Task Dispatch via IPC Queue
**Objective**: Spawn child processes that perform computations and return results to the parent via `multiprocessing.Queue`.

### Exercise 2: Point-to-Point Two-Way Pipe Communication
**Objective**: Set up bidirectional communication using `multiprocessing.Pipe()`, sending a query to a child process and receiving an acknowledgement.

### Exercise 3: Demonstrating Process Memory Isolation
**Objective**: Verify that mutating a variable inside a child process does not affect the parent process's memory.

### Exercise 4: Process Lifecycle & Exit Code Inspection
**Objective**: Inspect the `.is_alive()` status and `.exitcode` attribute of completed and terminated processes.
