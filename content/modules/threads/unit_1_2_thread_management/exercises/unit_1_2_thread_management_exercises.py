"""
Unit 1.2: Thread Management - Exercises
Concept-focused drills testing daemon modes, thread enumeration, naming, and cooperative shutdown.
"""

import threading
import time
from typing import List, Tuple, Optional


# ============================================================================
# Exercise 1: Daemon Thread Configuration
# ============================================================================

def exercise_1_starter(name: str) -> Tuple[bool, str]:
    """
    Instantiate and start a thread with daemon=True and the provided name.
    Wait briefly for it to start, inspect its daemon status and name, and return them.
    
    Objective: Master configuring daemon mode and thread names.
    
    Requirements:
    - Instantiate a threading.Thread targeting a dummy function that sleeps for 0.1s.
    - Set daemon=True and name=name during instantiation.
    - Start the thread.
    - Return a tuple of (thread.daemon, thread.name).
    
    Args:
        name: Name to assign to the thread.
        
    Returns:
        Tuple of (is_daemon, thread_name).
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
    # Test case 1: Standard naming
    daemon_status, thread_name = exercise_1_starter("AuditService")
    assert daemon_status is True, "Thread should be configured as daemon=True"
    assert thread_name == "AuditService", f"Expected 'AuditService', got {thread_name}"
    
    # Test case 2: Secondary worker name
    daemon_status2, thread_name2 = exercise_1_starter("MetricPoller")
    assert daemon_status2 is True
    assert thread_name2 == "MetricPoller"


# ============================================================================
# Exercise 2: Active Thread Filtering by Prefix
# ============================================================================

def exercise_2_starter(prefix: str, count: int) -> List[str]:
    """
    Spawn `count` daemon threads with names formatted as f"{prefix}-{i}".
    Each thread should sleep for 0.2 seconds.
    While they are running, use `threading.enumerate()` to find and return 
    the sorted names of all active threads whose name starts with `prefix`.
    
    Objective: Master runtime thread inspection and filtering via threading.enumerate().
    
    Requirements:
    - Spawn and start `count` daemon threads named f"{prefix}-{i}".
    - Inspect active threads using `threading.enumerate()`.
    - Filter for threads where `t.name.startswith(prefix)`.
    - Return sorted list of matching thread names.
    
    Args:
        prefix: String prefix to filter on.
        count: Number of threads to spawn.
        
    Returns:
        Sorted list of matching thread names.
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
    # Test case 1: 3 workers
    names = exercise_2_starter("WorkerJob", 3)
    assert names == ["WorkerJob-0", "WorkerJob-1", "WorkerJob-2"], f"Got {names}"
    
    # Test case 2: 1 worker
    names2 = exercise_2_starter("SinglePoller", 1)
    assert names2 == ["SinglePoller-0"], f"Got {names2}"
    
    # Test case 3: 0 workers
    names3 = exercise_2_starter("EmptyJob", 0)
    assert names3 == [], f"Got {names3}"


# ============================================================================
# Exercise 3: Cooperative Cancellation with Event
# ============================================================================

def exercise_3_starter(stop_event: threading.Event, result_container: list) -> threading.Thread:
    """
    Start a worker thread that increments an internal counter and sleeps 0.02s per loop,
    checking `stop_event.is_set()` every iteration.
    When `stop_event` is set, the worker stores the final counter value in `result_container`
    and returns. Return the started thread object.
    
    Objective: Implement cooperative thread termination loops using threading.Event.
    
    Requirements:
    - Worker runs: while not stop_event.is_set(): count += 1; stop_event.wait(0.02)
    - Upon exit, worker executes: result_container.append(count)
    - Instantiate, start, and return the Thread instance.
    
    Args:
        stop_event: threading.Event signaling termination.
        result_container: List into which the worker appends its final count upon exit.
        
    Returns:
        The running threading.Thread instance.
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
    event = threading.Event()
    results = []
    
    thread = exercise_3_starter(event, results)
    assert thread.is_alive() is True, "Thread should be running"
    
    # Allow worker to perform several iterations
    time.sleep(0.08)
    
    # Signal cooperative termination
    event.set()
    thread.join(timeout=1.0)
    
    assert thread.is_alive() is False, "Thread should have terminated after stop event"
    assert len(results) == 1, f"Expected 1 recorded count, got {results}"
    assert results[0] >= 2, f"Expected counter >= 2, got {results[0]}"


# ============================================================================
# Exercise 4: Safe Join with Timeout
# ============================================================================

def exercise_4_starter(thread_delay: float, join_timeout: float) -> bool:
    """
    Spawn a worker thread that sleeps for `thread_delay`.
    Attempt to join the thread using `thread.join(timeout=join_timeout)`.
    Return True if the thread terminated within the timeout, or False if it timed out.
    
    Objective: Master timeout handling during thread join synchronization.
    
    Requirements:
    - Spawn a worker thread that sleeps for `thread_delay`.
    - Start the thread.
    - Call `thread.join(timeout=join_timeout)`.
    - If `thread.is_alive()` is False, return True (finished in time).
    - If `thread.is_alive()` is True, return False (timed out).
    
    Args:
        thread_delay: How long the worker sleeps.
        join_timeout: Join timeout in seconds.
        
    Returns:
        Boolean indicating whether thread finished within timeout.
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
    # Test case 1: Fast thread finishes well before timeout
    res1 = exercise_4_starter(thread_delay=0.02, join_timeout=0.2)
    assert res1 is True, "Fast thread should have completed within timeout"
    
    # Test case 2: Slow thread exceeds timeout
    res2 = exercise_4_starter(thread_delay=0.5, join_timeout=0.05)
    assert res2 is False, "Slow thread should have timed out"


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
    print("All Unit 1.2 exercises passed!")
