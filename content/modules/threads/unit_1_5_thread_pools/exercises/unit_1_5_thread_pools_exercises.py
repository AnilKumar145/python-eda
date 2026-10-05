"""
Unit 1.5: Thread Pools - Exercises
Concept-focused drills testing ThreadPoolExecutor, submit, map, Future, and exception handling.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import time
from typing import List, Tuple, Dict, Any, Callable


# ============================================================================
# Exercise 1: Task Dispatch and Future Resolution
# ============================================================================

def exercise_1_starter(values: List[int]) -> List[int]:
    """
    Use ThreadPoolExecutor(max_workers=3) to multiply each number in values by 10.
    Submit each task using `executor.submit()`.
    Collect all Future objects.
    Resolve their `.result()` calls and return the list of products in the original order.
    
    Objective: Master ThreadPoolExecutor.submit() and Future.result().
    
    Args:
        values: List of integers.
        
    Returns:
        List of integers each multiplied by 10.
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
    # Test case 1: Standard values
    assert exercise_1_starter([1, 2, 3, 4]) == [10, 20, 30, 40]
    
    # Test case 2: Empty list
    assert exercise_1_starter([]) == []
    
    # Test case 3: Negative numbers
    assert exercise_1_starter([-5, 0, 5]) == [-50, 0, 50]


# ============================================================================
# Exercise 2: Parallel Batch Transformation with executor.map()
# ============================================================================

def exercise_2_starter(words: List[str]) -> List[str]:
    """
    Use ThreadPoolExecutor(max_workers=4) and `executor.map()` to reverse each string in words.
    Return the list of reversed strings.
    
    Objective: Master executor.map() for batch parallel transformations.
    
    Args:
        words: List of strings.
        
    Returns:
        List of reversed strings in matching order.
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
    # Test case 1: Standard words
    assert exercise_2_starter(["python", "threads", "pool"]) == ["nohtyp", "sdaerht", "loop"]
    
    # Test case 2: Empty list
    assert exercise_2_starter([]) == []
    
    # Test case 3: Palindromes
    assert exercise_2_starter(["racecar", "madam"]) == ["racecar", "madam"]


# ============================================================================
# Exercise 3: Dynamic Result Streaming with as_completed()
# ============================================================================

def exercise_3_starter(tasks: List[Tuple[str, float]]) -> List[str]:
    """
    Each task is a tuple of (name, delay_seconds).
    Submit all tasks using `executor.submit()`, where each task sleeps for delay_seconds
    and then returns name.
    Use `concurrent.futures.as_completed()` to collect names in the exact order they finish.
    
    Objective: Understand completion-order iteration via as_completed().
    
    Args:
        tasks: List of (name, delay) tuples.
        
    Returns:
        List of names ordered by completion time.
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
    # Task C takes 0.01s, Task A takes 0.05s, Task B takes 0.1s
    task_list = [("Task-A", 0.05), ("Task-B", 0.10), ("Task-C", 0.01)]
    result = exercise_3_starter(task_list)
    # Task C must finish first, then Task A, then Task B
    assert result == ["Task-C", "Task-A", "Task-B"], f"Expected ['Task-C', 'Task-A', 'Task-B'], got {result}"


# ============================================================================
# Exercise 4: Trapping Worker Exceptions
# ============================================================================

def exercise_4_starter(divisors: List[int]) -> Dict[int, Any]:
    """
    Submit tasks calculating 100 // divisor for each divisor in `divisors`.
    If division succeeds, map divisor -> quotient.
    If division raises an exception (e.g. ZeroDivisionError), trap the exception and map divisor -> "ERROR".
    
    Objective: Catch and isolate worker exceptions using Future.result().
    
    Args:
        divisors: List of integer divisors.
        
    Returns:
        Dictionary mapping divisor to result or "ERROR".
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
    # Test case 1: Mixed valid and zero divisors
    res = exercise_4_starter([10, 0, 5, 2])
    assert res == {10: 10, 0: "ERROR", 5: 20, 2: 50}, f"Got {res}"
    
    # Test case 2: All valid
    assert exercise_4_starter([20, 25]) == {20: 5, 25: 4}


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
    print("All Unit 1.5 exercises passed!")
