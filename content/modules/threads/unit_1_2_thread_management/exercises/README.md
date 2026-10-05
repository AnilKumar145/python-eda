# Unit 1.2: Thread Management - Exercises

## Overview
Concept-focused drills testing daemon thread configuration, runtime thread enumeration, thread naming conventions, and cooperative cancellation patterns.

**Target File**: `unit_1_2_thread_management_exercises.py`

---

## Exercise List

### Exercise 1: Daemon Thread Configuration
**Objective**: Launch a worker thread in daemon mode and verify that its `.daemon` attribute is `True` while running.

### Exercise 2: Active Thread Filtering by Prefix
**Objective**: Use `threading.enumerate()` to inspect the runtime thread list and return the names of all alive threads matching a specified prefix.

### Exercise 3: Cooperative Cancellation with Event
**Objective**: Implement a worker function that loops until a `threading.Event` is set, recording loop count and exiting cleanly.

### Exercise 4: Safe Join with Timeout
**Objective**: Implement a thread join supervisor that attempts to join a worker within a specified timeout, returning whether the thread terminated or timed out.
