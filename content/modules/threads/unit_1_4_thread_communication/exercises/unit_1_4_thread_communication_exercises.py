"""
Unit 1.4: Thread Communication - Exercises
Concept-focused drills testing Queue, PriorityQueue, task_done, and sentinel shutdown.
"""

import threading
import queue
import time
from typing import List, Tuple, Any


# ============================================================================
# Exercise 1: FIFO Message Queue Pipeline
# ============================================================================

def exercise_1_starter(messages: List[str]) -> List[str]:
    """
    Pass a list of strings through a queue.Queue from a producer thread to a consumer thread.
    The producer sends each message followed by None as a sentinel.
    The consumer accumulates messages until encountering None, then returns the list.
    
    Objective: Implement a basic FIFO producer-consumer pipeline with sentinel termination.
    
    Requirements:
    - Instantiate a queue.Queue().
    - In producer: put all items from `messages`, then put None.
    - In consumer: loop getting from queue. If item is None, break; otherwise append to received.
    - Run both threads, join them, and return the received list.
    
    Args:
        messages: List of strings to transmit.
        
    Returns:
        List of strings received in order.
    """
    # ========================================================================
    # WRITE CODE HERE
    # ========================================================================
    pass
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


def test_exercise_1():
    """Test cases for Exercise 1"""
    # Test case 1: Multiple messages
    msgs = ["ALPHA", "BETA", "GAMMA"]
    assert exercise_1_starter(msgs) == ["ALPHA", "BETA", "GAMMA"]
    
    # Test case 2: Empty messages list
    assert exercise_1_starter([]) == []
    
    # Test case 3: Single message
    assert exercise_1_starter(["SOLO"]) == ["SOLO"]


# ============================================================================
# Exercise 2: Task Tracking with task_done() and join()
# ============================================================================

def exercise_2_starter(numbers: List[int]) -> List[int]:
    """
    Process `numbers` by squaring each number across 2 worker threads using queue.Queue.
    Use `queue.join()` to block until all items have been processed with `task_done()`.
    
    Objective: Master task lifecycle coordination using task_done() and queue.join().
    
    Requirements:
    - Instantiate work_queue = queue.Queue().
    - Spawn 2 daemon worker threads that loop:
      - num = work_queue.get()
      - append num * num to a shared results list (protect with lock or pre-allocate)
      - work_queue.task_done()
    - Put all items from `numbers` into work_queue.
    - Call work_queue.join().
    - Return sorted results list.
    
    Args:
        numbers: List of integers to square.
        
    Returns:
        Sorted list of squared integers.
    """
    # ========================================================================
    # WRITE CODE HERE
    # ========================================================================
    pass
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


def test_exercise_2():
    """Test cases for Exercise 2"""
    # Test case 1: Standard list
    nums = [1, 2, 3, 4, 5]
    assert exercise_2_starter(nums) == [1, 4, 9, 16, 25]
    
    # Test case 2: Empty list
    assert exercise_2_starter([]) == []
    
    # Test case 3: Negative numbers
    nums2 = [-3, -2, -1]
    assert exercise_2_starter(nums2) == [1, 4, 9]


# ============================================================================
# Exercise 3: Priority Ordering with PriorityQueue
# ============================================================================

def exercise_3_starter(prioritized_items: List[Tuple[int, str]]) -> List[str]:
    """
    Enqueue tuples of (priority_int, data_str) into a queue.PriorityQueue.
    Dequeue all items and return their data_str values in priority order.
    
    Objective: Understand min-heap ordering in PriorityQueue.
    
    Requirements:
    - Instantiate queue.PriorityQueue().
    - Put all tuples into the priority queue.
    - Dequeue until empty (use q.empty() or loop for len(items)).
    - Return the extracted string items.
    
    Args:
        prioritized_items: List of (priority, name) tuples.
        
    Returns:
        List of names sorted by ascending priority number.
    """
    # ========================================================================
    # WRITE CODE HERE
    # ========================================================================
    pass
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


def test_exercise_3():
    """Test cases for Exercise 3"""
    # Test case 1: Out of order priorities
    items = [(3, "Low"), (1, "Critical"), (2, "Medium")]
    assert exercise_3_starter(items) == ["Critical", "Medium", "Low"]
    
    # Test case 2: Already sorted
    items2 = [(10, "A"), (20, "B")]
    assert exercise_3_starter(items2) == ["A", "B"]
    
    # Test case 3: Empty list
    assert exercise_3_starter([]) == []


# ============================================================================
# Exercise 4: Bounded Queue Backpressure Verification
# ============================================================================

def exercise_4_starter() -> Tuple[bool, bool]:
    """
    Create a queue with maxsize=1.
    Put 1 item into the queue.
    Check if `q.full()` is True.
    Start a background thread that puts a 2nd item (which should block until get is called).
    Wait briefly (0.05s) and verify the 2nd put has NOT finished.
    Call `q.get()`, verify that the 2nd put unblocks and finishes.
    
    Objective: Verify backpressure mechanics and blocking behavior of bounded queues.
    
    Returns:
        Tuple of (was_full_before_get, second_put_completed_after_get)
    """
    # ========================================================================
    # WRITE CODE HERE
    # ========================================================================
    pass
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


def test_exercise_4():
    """Test cases for Exercise 4"""
    was_full, completed_after = exercise_4_starter()
    assert was_full is True, "Queue with maxsize=1 should report full after 1 put"
    assert completed_after is True, "Second put should unblock after get() is invoked"


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
    print("All Unit 1.4 exercises passed!")
