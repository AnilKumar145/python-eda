"""
Unit 1.3: Thread Synchronization - Exercises
Concept-focused drills testing Lock, RLock, Semaphore, and Condition.
"""

import threading
import time
from typing import List, Optional


# ============================================================================
# Exercise 1: Thread-Safe Atomic Counter with Lock
# ============================================================================

class SafeCounter:
    """
    A thread-safe integer counter protected by a threading.Lock.
    
    Objective: Protect shared mutable state against race conditions.
    
    Requirements:
    - Initialize internal value to 0.
    - Instantiate an internal threading.Lock.
    - Implement `increment()`: adds 1 atomically using `with self.lock:`.
    - Implement `get_value()`: returns current value atomically.
    """
    def __init__(self):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def increment(self):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def get_value(self) -> int:
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================


def test_exercise_1():
    """Test cases for Exercise 1"""
    counter = SafeCounter()
    
    def worker():
        for _ in range(500):
            counter.increment()
            
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert counter.get_value() == 5000, f"Expected 5000, got {counter.get_value()} (Race condition detected!)"


# ============================================================================
# Exercise 2: Reentrant Nested Locking with RLock
# ============================================================================

class ReentrantResource:
    """
    A resource requiring nested method calls on the same lock.
    
    Objective: Demonstrate reentrant locking without self-deadlock.
    
    Requirements:
    - Use threading.RLock() as internal lock.
    - `step_one(val)`: acquires rlock, increments internal accumulator by val.
    - `step_two(val, bonus)`: acquires rlock, calls self.step_one(val), then adds bonus.
    - Returns final accumulator.
    """
    def __init__(self):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def step_one(self, val: int):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def step_two(self, val: int, bonus: int) -> int:
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================


def test_exercise_2():
    """Test cases for Exercise 2"""
    resource = ReentrantResource()
    # If standard Lock is used, step_two will hang!
    result = resource.step_two(10, 5)
    assert result == 15, f"Expected 15, got {result}"
    
    result2 = resource.step_two(20, 10)
    assert result2 == 45, f"Expected 45, got {result2}"


# ============================================================================
# Exercise 3: Concurrency Throttling with Semaphore
# ============================================================================

class ThrottledWorkerPool:
    """
    Tracks peak concurrent executions allowed through a Semaphore.
    
    Objective: Restrict simultaneous execution capacity via Semaphore.
    
    Requirements:
    - Initialize with `max_concurrent` capacity using `threading.Semaphore(max_concurrent)`.
    - Track `self.current_active` and `self.peak_concurrent` protected by an internal lock.
    - In `execute_task(work_time)`:
      - Acquire semaphore.
      - Increment current_active; update peak_concurrent = max(peak, current_active).
      - sleep for work_time.
      - Decrement current_active.
      - Release semaphore.
    """
    def __init__(self, max_concurrent: int):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def execute_task(self, work_time: float):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================


def test_exercise_3():
    """Test cases for Exercise 3"""
    pool = ThrottledWorkerPool(max_concurrent=3)
    threads = [threading.Thread(target=pool.execute_task, args=(0.05,)) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert pool.peak_concurrent <= 3, f"Semaphore failed: peak was {pool.peak_concurrent} > 3"
    assert pool.peak_concurrent >= 2, f"Concurrency was too low: peak was {pool.peak_concurrent}"


# ============================================================================
# Exercise 4: Conditional Signaling with Condition
# ============================================================================

class SingleItemBuffer:
    """
    A single-item buffer coordinated by a threading.Condition.
    
    Objective: Coordinate producer and consumer using Condition wait/notify.
    
    Requirements:
    - Instantiate internal threading.Condition().
    - `put(item)`: acquires condition, waits while self.item is not None,
      sets self.item = item, calls notify(), releases condition.
    - `get()`: acquires condition, waits while self.item is None,
      retrieves item, sets self.item = None, calls notify(), returns item.
    """
    def __init__(self):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def put(self, item: str):
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def get(self) -> str:
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================


def test_exercise_4():
    """Test cases for Exercise 4"""
    buf = SingleItemBuffer()
    consumed = []
    
    def consumer():
        for _ in range(3):
            val = buf.get()
            consumed.append(val)
            
    def producer():
        for i in range(3):
            time.sleep(0.02)
            buf.put(f"MSG-{i}")
            
    c_thread = threading.Thread(target=consumer)
    p_thread = threading.Thread(target=producer)
    
    c_thread.start()
    p_thread.start()
    
    p_thread.join()
    c_thread.join()
    
    assert consumed == ["MSG-0", "MSG-1", "MSG-2"], f"Expected ['MSG-0', 'MSG-1', 'MSG-2'], got {consumed}"


# ============================================================================
# Runner
# ============================================================================

if __name__ == "__main__":
    print("Testing Exercise 1...")
    test_exercise_1()
    print("Testing Exercise 2...")
    test_exercise_2()
    print("Testing Exercise 3...")
    test_exercise_3()
    print("Testing Exercise 4...")
    test_exercise_4()
    print("All Unit 1.3 exercises passed!")
