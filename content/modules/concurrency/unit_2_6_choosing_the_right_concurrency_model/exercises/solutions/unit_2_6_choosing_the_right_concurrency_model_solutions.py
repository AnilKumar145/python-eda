"""
Unit 2.6 Exercises: Choosing the Right Concurrency Model - Solutions
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Dict, Any, Callable


def compute_sum_of_squares(n: int) -> int:
    return sum(i * i for i in range(n))


def simulate_io_fetch(delay: float) -> str:
    time.sleep(delay)
    return "io_done"


def route_workloads(
    cpu_inputs: List[int],
    io_delays: List[float],
    cpu_pool: ProcessPoolExecutor,
    thread_pool: ThreadPoolExecutor
) -> Dict[str, Any]:
    cpu_res = list(cpu_pool.map(compute_sum_of_squares, cpu_inputs))
    io_res = list(thread_pool.map(simulate_io_fetch, io_delays))
    return {
        "cpu_results": cpu_res,
        "io_results": io_res
    }


async def async_run_blocking(
    blocking_func: Callable[[float], str], 
    arg: float
) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, blocking_func, arg)


async def hybrid_pipeline(
    cpu_numbers: List[int], 
    process_pool: ProcessPoolExecutor
) -> List[int]:
    loop = asyncio.get_running_loop()
    tasks = [
        loop.run_in_executor(process_pool, compute_sum_of_squares, n)
        for n in cpu_numbers
    ]
    if not tasks:
        return []
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from unit_2_6_choosing_the_right_concurrency_model_exercises import (
        test_exercise_1,
        test_exercise_2,
        test_exercise_3,
    )
    import unit_2_6_choosing_the_right_concurrency_model_exercises as ex
    ex.route_workloads = route_workloads
    ex.async_run_blocking = async_run_blocking
    ex.hybrid_pipeline = hybrid_pipeline
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    print("All Unit 2.6 Solutions Verified!")
