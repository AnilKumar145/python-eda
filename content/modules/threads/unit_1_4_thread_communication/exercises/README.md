# Unit 1.4: Thread Communication - Exercises

## Overview
Concept-focused drills testing FIFO message pipelines with `queue.Queue`, priority-ordered scheduling with `queue.PriorityQueue`, task tracking with `task_done()` and `join()`, and sentinel shutdown protocols.

**Target File**: `unit_1_4_thread_communication_exercises.py`

---

## Exercise List

### Exercise 1: FIFO Message Queue Pipeline
**Objective**: Build a producer-consumer pair that passes items through a `queue.Queue` and uses a sentinel token (`None`) to stop the consumer cleanly.

### Exercise 2: Task Tracking with `task_done()` and `join()`
**Objective**: Enqueue work items into a shared queue processed by background daemon workers, using `queue.join()` to block until all items are completed.

### Exercise 3: Priority Ordering with `PriorityQueue`
**Objective**: Enqueue items with varying integer priorities into a `queue.PriorityQueue` and verify that consumers receive them in strictly ascending priority order.

### Exercise 4: Bounded Queue Backpressure Verification
**Objective**: Configure a bounded queue with `maxsize=2`, verify that attempting to put a 3rd item blocks until an item is retrieved.
