"""
Unit 2.3: Process Pools - Exercises
Concept-focused drills testing ProcessPoolExecutor, map, submit, chunksize, and error handling.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import math
import time
from typing import List, Tuple, Dict, Any


# Top-level helper functions for multiprocessing pickling on Windows
def _worker_factorial(n: int) -> int:
    return math.factorial(n)

def _worker_square(n: int) -> int:
    return n * n

def _worker_delayed_cube(item: Tuple[str, float]) -> str:
    name, delay = item
    time.sleep(delay)
    return name

def _worker_safe_sqrt(n: float) -> float:
    if n < 0:
        raise ValueError(f"Cannot take square root of negative number: {n}")
    return round(math.sqrt(n), 4)


# ============================================================================
# Exercise 1: Parallel Factorial Mapping
# ============================================================================

def exercise_1_starter(numbers: List[int]) -> List[int]:
    """
    Use ProcessPoolExecutor(max_workers=2) and executor.map() to compute
    math.factorial for each integer in `numbers`.
    
    Objective: Apply ProcessPoolExecutor.map() across an iterable.
    
    Args:
        numbers: List of integers (e.g. [3, 4, 5]).
        
    Returns:
        List of factorials in matching order.
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
    res1 = exercise_1_starter([3, 4, 5])
    assert res1 == [6, 24, 120], f"Expected [6, 24, 120], got {res1}"
    
    assert exercise_1_starter([]) == []
    assert exercise_1_starter([0, 1]) == [1, 1]


# ============================================================================
# Exercise 2: Chunked Batch Processing
# ============================================================================

def exercise_2_starter(items: List[int], chunk_size: int) -> List[int]:
    """
    Use ProcessPoolExecutor(max_workers=2) to square all numbers in `items`
    using `executor.map(_worker_square, items, chunksize=chunk_size)`.
    
    Objective: Master chunksize parameter optimization in ProcessPoolExecutor.
    
    Args:
        items: List of numbers.
        chunk_size: Size of chunk batches.
        
    Returns:
        List of squared numbers.
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
    nums = list(range(10))
    res = exercise_2_starter(nums, chunk_size=3)
    assert res == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    assert exercise_2_starter([], chunk_size=5) == []


# ============================================================================
# Exercise 3: Dynamic Result Streaming with as_completed()
# ============================================================================

def exercise_3_starter(tasks: List[Tuple[str, float]]) -> List[str]:
    """
    Submit tasks using `executor.submit(_worker_delayed_cube, task)`.
    Use `concurrent.futures.as_completed()` to collect task names in order of completion.
    
    Objective: Apply as_completed() over ProcessPoolExecutor futures.
    
    Args:
        tasks: List of (name, delay) tuples.
        
    Returns:
        List of names in completion order.
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
    task_list = [("Proc-Slow", 0.08), ("Proc-Fast", 0.01), ("Proc-Med", 0.04)]
    res = exercise_3_starter(task_list)
    assert res == ["Proc-Fast", "Proc-Med", "Proc-Slow"], f"Got {res}"


# ============================================================================
# Exercise 4: Worker Exception Handling in Process Pools
# ============================================================================

def exercise_4_starter(values: List[float]) -> Dict[float, Any]:
    """
    Submit `_worker_safe_sqrt(val)` for each value in `values`.
    If valid, map val -> square_root.
    If ValueError occurs, trap it and map val -> "INVALID".
    
    Objective: Safely catch exceptions raised inside child processes.
    
    Args:
        values: List of numbers (may include negatives).
        
    Returns:
        Dict mapping input value to square root or "INVALID".
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
    res = exercise_4_starter([9.0, -4.0, 16.0, -1.0])
    assert res[9.0] == 3.0
    assert res[-4.0] == "INVALID"
    assert res[16.0] == 4.0
    assert res[-1.0] == "INVALID"


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
    print("All Unit 2.3 exercises passed!")
