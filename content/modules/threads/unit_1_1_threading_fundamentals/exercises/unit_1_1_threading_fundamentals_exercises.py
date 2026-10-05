"""
Unit 1.1: Threading Fundamentals - Exercises
Concept-focused drills testing thread creation, parameter binding, lifecycle, and joining.
"""

import threading
import time
from typing import List, Tuple, Any, Callable


# ============================================================================
# Exercise 1: Basic Thread Instantiation and Execution
# ============================================================================

def exercise_1_starter(value: int) -> List[int]:
    """
    Launch a thread that appends `value` to a shared list and wait for it to finish.
    
    Objective: Master basic threading.Thread instantiation, start, and join.
    
    Requirements:
    - Instantiate a threading.Thread targeting a worker function.
    - Start the thread using .start().
    - Join the thread using .join() to ensure execution completes before returning.
    - Return the resulting list containing [value].
    
    Args:
        value: Integer to append.
        
    Returns:
        List containing the single integer.
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
    # Test case 1: Standard positive integer
    assert exercise_1_starter(42) == [42], "Failed for value 42"
    
    # Test case 2: Zero
    assert exercise_1_starter(0) == [0], "Failed for value 0"
    
    # Test case 3: Negative integer
    assert exercise_1_starter(-99) == [-99], "Failed for negative integer -99"


# ============================================================================
# Exercise 2: Parameterized Thread Execution
# ============================================================================

def exercise_2_starter(base: int, multiplier: int, tag: str) -> dict:
    """
    Launch a thread passing positional args (base, multiplier) and keyword arg (tag=tag)
    to calculate base * multiplier and store the result in a dictionary.
    
    Objective: Master passing `args` and `kwargs` into threading.Thread.
    
    Requirements:
    - Pass base and multiplier via `args` tuple.
    - Pass tag via `kwargs` dictionary.
    - Worker function should compute: base * multiplier and set out_dict[tag] = product.
    - Wait for thread with .join() before returning out_dict.
    
    Args:
        base: Number to multiply.
        multiplier: Multiplier factor.
        tag: Key in the output dictionary.
        
    Returns:
        Dictionary mapping tag -> product.
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
    # Test case 1: Standard multiplication
    res1 = exercise_2_starter(10, 5, "calc_a")
    assert res1 == {"calc_a": 50}, f"Expected {{'calc_a': 50}}, got {res1}"
    
    # Test case 2: Multiplication by zero
    res2 = exercise_2_starter(100, 0, "zero_tag")
    assert res2 == {"zero_tag": 0}, f"Expected {{'zero_tag': 0}}, got {res2}"
    
    # Test case 3: Negative factors
    res3 = exercise_2_starter(-4, 7, "neg_tag")
    assert res3 == {"neg_tag": -28}, f"Expected {{'neg_tag': -28}}, got {res3}"


# ============================================================================
# Exercise 3: Parallel Batch Thread Coordinator
# ============================================================================

def exercise_3_starter(items: List[int], transform_fn: Callable[[int], int]) -> List[int]:
    """
    Transform each item in `items` in a separate worker thread and return the transformed items.
    
    Objective: Coordinate multiple concurrent threads and join all before completion.
    
    Requirements:
    - Create a pre-allocated results list of the same length as items.
    - Spawn one threading.Thread per item.
    - Each thread executes transform_fn(items[i]) and stores the output at index i of results.
    - Start all threads, then join all threads.
    - Return the populated results list.
    
    Args:
        items: List of numbers to transform.
        transform_fn: Unary function to apply to each item.
        
    Returns:
        List of transformed numbers in the original order.
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
    # Test case 1: Square numbers
    items1 = [1, 2, 3, 4]
    assert exercise_3_starter(items1, lambda x: x * x) == [1, 4, 9, 16], "Failed squaring"
    
    # Test case 2: Empty list
    assert exercise_3_starter([], lambda x: x + 1) == [], "Failed empty list"
    
    # Test case 3: Single item
    assert exercise_3_starter([10], lambda x: x * 2) == [20], "Failed single item"


# ============================================================================
# Exercise 4: Thread Lifecycle & Alive Inspection
# ============================================================================

def exercise_4_starter() -> Tuple[bool, bool]:
    """
    Launch a worker thread that sleeps briefly (e.g. 0.05s).
    Inspect and capture its `is_alive()` status while running, and after `join()`.
    
    Objective: Understand thread state transitions and `.is_alive()` behavior.
    
    Requirements:
    - Instantiate and start a worker thread that sleeps for 0.05 seconds.
    - Capture `alive_during = thread.is_alive()`.
    - Call `thread.join()`.
    - Capture `alive_after = thread.is_alive()`.
    - Return tuple `(alive_during, alive_after)`.
    
    Returns:
        Tuple of two booleans: (True, False)
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
    # Test case 1: Valid lifecycle state verification
    during, after = exercise_4_starter()
    assert during is True, f"Thread should be alive during execution, got {during}"
    assert after is False, f"Thread should be dead after join(), got {after}"
    
    # Test case 2: Consistency check on repeated invocation
    during2, after2 = exercise_4_starter()
    assert during2 is True and after2 is False, "Repeated lifecycle inspection failed"


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
    print("All exercises passed successfully!")
