"""
Unit 2.1: Concurrency Fundamentals - Solutions
"""

from typing import Dict, Any, List


def exercise_1_starter(task_description: str) -> str:
    desc = task_description.lower()
    cpu_keywords = ["matrix", "crypto", "encryption", "render", "fourier", "compress", "prime"]
    for kw in cpu_keywords:
        if kw in desc:
            return "CPU_BOUND"
    return "IO_BOUND"


def test_exercise_1():
    assert exercise_1_starter("Download patient medical records via HTTP REST endpoint") == "IO_BOUND"
    assert exercise_1_starter("Train matrix factorization model for genomic clustering") == "CPU_BOUND"
    assert exercise_1_starter("Compress video stream using HEVC algorithm") == "CPU_BOUND"
    assert exercise_1_starter("Execute SQL query on PostgreSQL database cluster") == "IO_BOUND"


def exercise_2_starter(parallel_fraction: float, num_processors: int) -> float:
    p = parallel_fraction
    n = num_processors
    speedup = 1.0 / ((1.0 - p) + (p / n))
    return round(speedup, 2)


def test_exercise_2():
    assert exercise_2_starter(0.5, 2) == 1.33
    assert exercise_2_starter(0.9, 8) == 4.71
    assert exercise_2_starter(0.0, 16) == 1.0


def exercise_3_starter(workload_type: str, socket_volume: int, is_pure_python_cpu: bool) -> str:
    if workload_type == "CPU" and is_pure_python_cpu:
        return "MULTIPROCESSING"
    if workload_type == "IO" and socket_volume >= 5000:
        return "ASYNCIO"
    return "THREADING"


def test_exercise_3():
    assert exercise_3_starter("CPU", socket_volume=0, is_pure_python_cpu=True) == "MULTIPROCESSING"
    assert exercise_3_starter("IO", socket_volume=10000, is_pure_python_cpu=False) == "ASYNCIO"
    assert exercise_3_starter("IO", socket_volume=20, is_pure_python_cpu=False) == "THREADING"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    print("All Unit 2.1 solution tests passed!")
