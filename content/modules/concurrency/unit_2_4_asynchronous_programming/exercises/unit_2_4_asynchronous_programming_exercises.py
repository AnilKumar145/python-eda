"""
Unit 2.4: Asynchronous Programming - Exercises
Concept-focused drills testing async/await, asyncio.gather, timeouts, and cancellation.
"""

import asyncio
import time
from typing import List, Tuple, Any, Optional


# ============================================================================
# Exercise 1: Basic Coroutine Invocation
# ============================================================================

async def exercise_1_starter(val: int) -> int:
    """
    Asynchronous function that sleeps for 0.02 seconds using asyncio.sleep(),
    then returns val * 2.
    
    Objective: Master defining and awaiting an async coroutine.
    
    Args:
        val: Integer to double.
        
    Returns:
        Doubled integer.
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
    res1 = asyncio.run(exercise_1_starter(5))
    assert res1 == 10, f"Expected 10, got {res1}"
    
    res2 = asyncio.run(exercise_1_starter(-3))
    assert res2 == -6


# ============================================================================
# Exercise 2: Concurrent Gathering with asyncio.gather()
# ============================================================================

async def exercise_2_starter(numbers: List[int]) -> List[int]:
    """
    For each number in `numbers`, call `exercise_1_starter(num)`.
    Execute all calls concurrently using `asyncio.gather(*coroutines)`.
    Return the list of doubled numbers in the original order.
    
    Objective: Master concurrent batching via asyncio.gather().
    
    Args:
        numbers: List of integers.
        
    Returns:
        List of doubled integers.
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
    t0 = time.perf_counter()
    # 5 tasks each sleeping 0.02s
    # Sequential would take 0.10s. Concurrent should take ~0.02s-0.05s
    res = asyncio.run(exercise_2_starter([1, 2, 3, 4, 5]))
    elapsed = time.perf_counter() - t0
    
    assert res == [2, 4, 6, 8, 10], f"Expected [2, 4, 6, 8, 10], got {res}"
    assert elapsed < 0.08, f"Took {elapsed:.2f}s; tasks were not gathered concurrently!"


# ============================================================================
# Exercise 3: Timeout Enforcement with asyncio.wait_for()
# ============================================================================

async def _delayed_task(delay: float, message: str) -> str:
    await asyncio.sleep(delay)
    return message

async def exercise_3_starter(delay: float, timeout_sec: float) -> str:
    """
    Execute `_delayed_task(delay, 'SUCCESS')` with `asyncio.wait_for()`.
    If the task completes within timeout_sec, return its result ('SUCCESS').
    If asyncio.TimeoutError is raised, catch it and return 'TIMED_OUT'.
    
    Objective: Apply non-blocking timeouts to asynchronous operations.
    
    Args:
        delay: How long the task sleeps.
        timeout_sec: Timeout threshold.
        
    Returns:
        'SUCCESS' or 'TIMED_OUT'
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
    # Test case 1: Finishes within timeout
    res1 = asyncio.run(exercise_3_starter(delay=0.01, timeout_sec=0.10))
    assert res1 == "SUCCESS"
    
    # Test case 2: Exceeds timeout
    res2 = asyncio.run(exercise_3_starter(delay=0.20, timeout_sec=0.02))
    assert res2 == "TIMED_OUT"


# ============================================================================
# Exercise 4: Graceful Task Cancellation
# ============================================================================

async def _long_cancellable_task() -> str:
    try:
        await asyncio.sleep(1.0)
        return "FINISHED"
    except asyncio.CancelledError:
        return "CANCELLED_GRACEFULLY"

async def exercise_4_starter() -> str:
    """
    Spawn `_long_cancellable_task()` using `asyncio.create_task()`.
    Wait 0.02 seconds.
    Cancel the task using `task.cancel()`.
    Await the task result and return the returned status string.
    
    Objective: Understand task cancellation mechanics and CancelledError handling.
    
    Returns:
        'CANCELLED_GRACEFULLY'
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
    res = asyncio.run(exercise_4_starter())
    assert res == "CANCELLED_GRACEFULLY", f"Expected 'CANCELLED_GRACEFULLY', got {res}"


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
    print("All Unit 2.4 exercises passed!")
