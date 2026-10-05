"""
Unit 2.2: Multiprocessing - Exercises
Concept-focused drills testing Process, IPC Queue, Pipe, and isolation.
"""

import multiprocessing
import time
from typing import List, Tuple, Any


# Top-level helper functions for multiprocessing compatibility on Windows (spawn)
def _worker_multiply(val: int, out_q: multiprocessing.Queue):
    out_q.put(val * 10)

def _pipe_echo_worker(conn):
    msg = conn.recv()
    conn.send(f"ECHO_{msg}")
    conn.close()


# ============================================================================
# Exercise 1: Multi-Process Task Dispatch via IPC Queue
# ============================================================================

def exercise_1_starter(values: List[int]) -> List[int]:
    """
    Spawn one multiprocessing.Process per item in `values`.
    Each process multiplies its item by 10 and puts the product into an IPC Queue.
    Collect and return the results.
    
    Objective: Master multiprocessing.Process instantiation and IPC queue communication.
    
    Args:
        values: List of integers.
        
    Returns:
        Sorted list of integer products.
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
    res = exercise_1_starter([1, 2, 3])
    assert res == [10, 20, 30], f"Expected [10, 20, 30], got {res}"
    
    # Test case 2: Empty list
    assert exercise_1_starter([]) == []


# ============================================================================
# Exercise 2: Point-to-Point Two-Way Pipe Communication
# ============================================================================

def exercise_2_starter(message: str) -> str:
    """
    Create a multiprocessing.Pipe().
    Spawn a worker process passing the child connection handle.
    Send `message` across the parent pipe, and return the response received from child.
    
    Objective: Implement bidirectional process communication via Pipe().
    
    Args:
        message: String query.
        
    Returns:
        String response from child process.
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
    res1 = exercise_2_starter("PING")
    assert res1 == "ECHO_PING", f"Expected 'ECHO_PING', got {res1}"
    
    res2 = exercise_2_starter("DATA_PAYLOAD")
    assert res2 == "ECHO_DATA_PAYLOAD"


# ============================================================================
# Exercise 3: Process Lifecycle & Exit Code Inspection
# ============================================================================

def _clean_exit_worker():
    pass

def exercise_3_starter() -> Tuple[bool, int]:
    """
    Spawn and start a worker process that exits cleanly.
    Inspect `p.is_alive()` before joining (may be True or False depending on speed).
    Call `p.join()`.
    Inspect and return `(p.is_alive(), p.exitcode)`.
    
    Objective: Verify process state transitions and exit code inspection.
    
    Returns:
        Tuple of (is_alive_after_join, exitcode).
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
    is_alive, exitcode = exercise_3_starter()
    assert is_alive is False, "Process should be dead after join()"
    assert exitcode == 0, f"Expected clean exit code 0, got {exitcode}"


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
    print("All Unit 2.2 exercises passed!")
