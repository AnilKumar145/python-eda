"""
Unit 2.5 Exercises: Concurrent Programming Patterns
Implement each exercise function to pass the assertion test suites.
"""

import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Dict, Any


# ---------------------------------------------------------------------------
# Exercise 1: Bounded Producer-Consumer Pipeline
# ---------------------------------------------------------------------------
def run_producer_consumer_pipeline(items: List[int], queue_size: int = 2) -> List[int]:
    """
    Exercise 1:
    Create a bounded queue of size `queue_size`.
    Launch a producer thread that enqueues each integer in `items`, followed by None (poison pill).
    Launch a consumer thread that dequeues items, computes item * 2, and appends to a local processed list.
    When consumer encounters None, it terminates and signals task_done.
    Return the collected processed results.
    """
    # TODO: Implement producer-consumer pipeline with poison pill
    pass


# ---------------------------------------------------------------------------
# Exercise 2: Fan-Out / Fan-In Map-Reduce
# ---------------------------------------------------------------------------
def fan_out_fan_in_sum_squares(batches: List[List[int]], max_workers: int = 3) -> int:
    """
    Exercise 2:
    Fan-Out: Submit each batch in `batches` to a ThreadPoolExecutor to compute the sum of squares of that batch.
    Fan-In: Collect the resulting partial sums and compute the grand total sum.
    """
    # TODO: Implement fan-out fan-in reduction
    pass


# ---------------------------------------------------------------------------
# Exercise 3: Safe Multi-Resource Lock Hierarchy (Deadlock Prevention)
# ---------------------------------------------------------------------------
class ContestedResource:
    def __init__(self, resource_id: int, initial_value: int):
        self.resource_id = resource_id
        self.value = initial_value
        self.lock = threading.Lock()


def safe_transfer(
    source: ContestedResource, 
    target: ContestedResource, 
    amount: int
) -> bool:
    """
    Exercise 3:
    Safely transfer `amount` from `source.value` to `target.value`.
    To guarantee deadlock freedom regardless of invocation argument ordering,
    always acquire locks sorted in ascending order of `resource_id`.
    If source.value >= amount, deduct amount from source and add to target; return True.
    Otherwise return False without changing values.
    """
    # TODO: Implement ordered lock acquisition to prevent circular wait deadlocks
    pass


# ---------------------------------------------------------------------------
# Assertion Verification Tests
# ---------------------------------------------------------------------------
def test_exercise_1():
    res1 = run_producer_consumer_pipeline([1, 2, 3, 4], queue_size=2)
    assert res1 == [2, 4, 6, 8], f"Expected [2, 4, 6, 8], got {res1}"

    res2 = run_producer_consumer_pipeline([], queue_size=1)
    assert res2 == [], f"Expected [], got {res2}"

    res3 = run_producer_consumer_pipeline([10, 20], queue_size=5)
    assert res3 == [20, 40], f"Expected [20, 40], got {res3}"
    print("Exercise 1 passed!")


def test_exercise_2():
    batches = [[1, 2], [3, 4], [5]]
    # (1 + 4) + (9 + 16) + (25) = 5 + 25 + 25 = 55
    res1 = fan_out_fan_in_sum_squares(batches, max_workers=3)
    assert res1 == 55, f"Expected 55, got {res1}"

    res2 = fan_out_fan_in_sum_squares([[]], max_workers=2)
    assert res2 == 0, f"Expected 0, got {res2}"

    res3 = fan_out_fan_in_sum_squares([[10]], max_workers=1)
    assert res3 == 100, f"Expected 100, got {res3}"
    print("Exercise 2 passed!")


def test_exercise_3():
    r1 = ContestedResource(1, 100)
    r2 = ContestedResource(2, 50)

    # Normal order
    assert safe_transfer(r1, r2, 30) is True
    assert r1.value == 70 and r2.value == 80

    # Reversed order (should not deadlock)
    assert safe_transfer(r2, r1, 20) is True
    assert r1.value == 90 and r2.value == 60

    # Insufficient balance
    assert safe_transfer(r2, r1, 100) is False
    assert r1.value == 90 and r2.value == 60
    print("Exercise 3 passed!")


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    print("All Unit 2.5 Exercise tests passed successfully!")
