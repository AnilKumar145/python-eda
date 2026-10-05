"""
Unit 2.6 Exercises: Choosing the Right Concurrency Model
Implement each exercise function to pass the assertion test suites.
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Dict, Any, Callable


# Top-level helper functions for multiprocessing support
def compute_sum_of_squares(n: int) -> int:
    return sum(i * i for i in range(n))


def simulate_io_fetch(delay: float) -> str:
    time.sleep(delay)
    return "io_done"


# ---------------------------------------------------------------------------
# Exercise 1: Workload Router (CPU vs I/O Routing)
# ---------------------------------------------------------------------------
def route_workloads(
    cpu_inputs: List[int],
    io_delays: List[float],
    cpu_pool: ProcessPoolExecutor,
    thread_pool: ThreadPoolExecutor
) -> Dict[str, Any]:
    """
    Exercise 1:
    Execute CPU tasks in parallel using `cpu_pool.map(compute_sum_of_squares, cpu_inputs)`.
    Execute I/O tasks concurrently using `thread_pool.map(simulate_io_fetch, io_delays)`.
    Return a dictionary with:
    {
        "cpu_results": list of int results,
        "io_results": list of str results
    }
    """
    # TODO: Route tasks to their optimal executor and gather results
    pass


# ---------------------------------------------------------------------------
# Exercise 2: Asyncio Blocking Offloader
# ---------------------------------------------------------------------------
async def async_run_blocking(
    blocking_func: Callable[[float], str], 
    arg: float
) -> str:
    """
    Exercise 2:
    Execute a synchronous blocking function from within an async coroutine
    without blocking the running event loop by using loop.run_in_executor(None, ...).
    Return the function result.
    """
    # TODO: Offload blocking function to default ThreadPoolExecutor
    pass


# ---------------------------------------------------------------------------
# Exercise 3: Hybrid Asyncio-Process Pipeline
# ---------------------------------------------------------------------------
async def hybrid_pipeline(
    cpu_numbers: List[int], 
    process_pool: ProcessPoolExecutor
) -> List[int]:
    """
    Exercise 3:
    In an async coroutine, schedule each compute_sum_of_squares call across
    `process_pool` using loop.run_in_executor(process_pool, compute_sum_of_squares, n).
    Gather all futures asynchronously with asyncio.gather().
    Return the list of computed results.
    """
    # TODO: Schedule process pool tasks via asyncio.gather and loop.run_in_executor
    pass


# ---------------------------------------------------------------------------
# Assertion Verification Tests
# ---------------------------------------------------------------------------
def test_exercise_1():
    with ProcessPoolExecutor(max_workers=2) as cpu_pool:
        with ThreadPoolExecutor(max_workers=2) as thread_pool:
            out1 = route_workloads([10, 20], [0.02, 0.02], cpu_pool, thread_pool)
            assert out1["cpu_results"] == [sum(i*i for i in range(10)), sum(i*i for i in range(20))]
            assert out1["io_results"] == ["io_done", "io_done"]

            out2 = route_workloads([], [], cpu_pool, thread_pool)
            assert out2["cpu_results"] == []
            assert out2["io_results"] == []
    print("Exercise 1 passed!")


def test_exercise_2():
    async def _test():
        t0 = time.perf_counter()
        # Run two blocking tasks concurrently via asyncio
        futs = [async_run_blocking(simulate_io_fetch, 0.05) for _ in range(2)]
        results = await asyncio.gather(*futs)
        elapsed = time.perf_counter() - t0
        assert results == ["io_done", "io_done"]
        # Concurrent offloading should take ~0.05-0.09s, not sequential 0.10s+
        assert elapsed < 0.095, f"Took {elapsed:.3f}s; not offloaded concurrently"

    asyncio.run(_test())
    print("Exercise 2 passed!")


def test_exercise_3():
    async def _test():
        with ProcessPoolExecutor(max_workers=2) as pool:
            numbers = [100, 200, 300]
            results = await hybrid_pipeline(numbers, pool)
            expected = [compute_sum_of_squares(n) for n in numbers]
            assert results == expected, f"Expected {expected}, got {results}"

            empty = await hybrid_pipeline([], pool)
            assert empty == []

    asyncio.run(_test())
    print("Exercise 3 passed!")


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    print("All Unit 2.6 Exercise tests passed successfully!")
