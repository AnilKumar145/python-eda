"""
Unit 2.1: Concurrency Fundamentals - Exercises
Concept-focused drills testing workload classification, Amdahl's Law, and model selection.
"""

from typing import Dict, Any, List


# ============================================================================
# Exercise 1: Workload Characterization Classifier
# ============================================================================

def exercise_1_starter(task_description: str) -> str:
    """
    Classify a workload description into either "IO_BOUND" or "CPU_BOUND".
    
    Keywords for IO_BOUND: "database", "http", "socket", "disk", "network", "download", "query"
    Keywords for CPU_BOUND: "matrix", "crypto", "encryption", "render", "fourier", "compress", "prime"
    
    Objective: Identify the dominant operational bottleneck of computational workloads.
    
    Args:
        task_description: Plain text description of the computational task.
        
    Returns:
        "IO_BOUND" or "CPU_BOUND"
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
    assert exercise_1_starter("Download patient medical records via HTTP REST endpoint") == "IO_BOUND"
    assert exercise_1_starter("Train matrix factorization model for genomic clustering") == "CPU_BOUND"
    assert exercise_1_starter("Compress video stream using HEVC algorithm") == "CPU_BOUND"
    assert exercise_1_starter("Execute SQL query on PostgreSQL database cluster") == "IO_BOUND"


# ============================================================================
# Exercise 2: Amdahl's Law Speedup Calculator
# ============================================================================

def exercise_2_starter(parallel_fraction: float, num_processors: int) -> float:
    """
    Calculate theoretical program speedup using Amdahl's Law:
        Speedup = 1 / ((1 - P) + (P / N))
    
    Objective: Calculate theoretical speedup bounds for parallel architectures.
    
    Args:
        parallel_fraction: Float P between 0.0 and 1.0 representing parallel portion.
        num_processors: Positive integer N representing available cores.
        
    Returns:
        Theoretical speedup factor rounded to 2 decimal places.
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
    # Test case 1: 50% parallel on 2 processors: 1 / (0.5 + 0.5/2) = 1 / 0.75 = 1.33
    assert exercise_2_starter(0.5, 2) == 1.33
    
    # Test case 3: 90% parallel on 8 processors: 1 / (0.1 + 0.9/8) = 1 / 0.2125 = 4.71
    assert exercise_2_starter(0.9, 8) == 4.71
    
    # Test case 4: 0% parallel (purely serial) on 16 processors: speedup must be 1.0
    assert exercise_2_starter(0.0, 16) == 1.0


# ============================================================================
# Exercise 3: Concurrency Model Selector
# ============================================================================

def exercise_3_starter(workload_type: str, socket_volume: int, is_pure_python_cpu: bool) -> str:
    """
    Select the optimal Python concurrency model based on operational parameters.
    
    Rules:
    - If `workload_type == "CPU"` and `is_pure_python_cpu == True`:
      return "MULTIPROCESSING" (bypasses CPython GIL for CPU bound execution).
    - If `workload_type == "IO"` and `socket_volume >= 5000`:
      return "ASYNCIO" (avoids thread stack allocation exhaustion at high volume).
    - If `workload_type == "IO"` and `socket_volume < 5000`:
      return "THREADING" (ideal for moderate I/O with standard synchronous drivers).
      
    Objective: Apply architectural rules to pick the right concurrency tool.
    
    Returns:
        "MULTIPROCESSING", "ASYNCIO", or "THREADING"
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
    assert exercise_3_starter("CPU", socket_volume=0, is_pure_python_cpu=True) == "MULTIPROCESSING"
    assert exercise_3_starter("IO", socket_volume=10000, is_pure_python_cpu=False) == "ASYNCIO"
    assert exercise_3_starter("IO", socket_volume=20, is_pure_python_cpu=False) == "THREADING"


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
    print("All Unit 2.1 exercises passed!")
