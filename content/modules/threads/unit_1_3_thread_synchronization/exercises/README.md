# Unit 1.3: Thread Synchronization - Exercises

## Overview
Concept-focused drills testing mutual exclusion using `threading.Lock`, reentrant locking with `threading.RLock`, and capacity-bounded throttling using `threading.Semaphore`.

**Target File**: `unit_1_3_thread_synchronization_exercises.py`

---

## Exercise List

### Exercise 1: Thread-Safe Atomic Counter with `Lock`
**Objective**: Build a synchronized integer counter class using `threading.Lock` that accurately handles simultaneous increments across 20 concurrent threads without lost updates.

### Exercise 2: Reentrant Nested Locking with `RLock`
**Objective**: Implement a class with a parent and child method that both synchronize on the same `threading.RLock`, verifying that reentrant calls do not self-deadlock.

### Exercise 3: Concurrency Throttling with `Semaphore`
**Objective**: Implement a resource pool manager using `threading.Semaphore` that limits simultaneous worker access to a specified maximum capacity.

### Exercise 4: Conditional Signaling with `Condition`
**Objective**: Coordinate a producer-consumer sequence where a consumer thread waits for an item to become available using a `threading.Condition` object.
