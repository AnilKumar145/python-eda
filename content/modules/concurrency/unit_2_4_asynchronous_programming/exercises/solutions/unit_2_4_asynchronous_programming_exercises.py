"""
Unit 2.4: Asynchronous Programming - Solutions
"""

import asyncio
import time
from typing import List, Tuple, Any, Optional


async def exercise_1_starter(val: int) -> int:
    await asyncio.sleep(0.02)
    return val * 2


def test_exercise_1():
    res1 = asyncio.run(exercise_1_starter(5))
    assert res1 == 10, f"Expected 10, got {res1}"
    res2 = asyncio.run(exercise_1_starter(-3))
    assert res2 == -6


async def exercise_2_starter(numbers: List[int]) -> List[int]:
    coroutines = [exercise_1_starter(n) for n in numbers]
    return await asyncio.gather(*coroutines)


def test_exercise_2():
    t0 = time.perf_counter()
    res = asyncio.run(exercise_2_starter([1, 2, 3, 4, 5]))
    elapsed = time.perf_counter() - t0
    assert res == [2, 4, 6, 8, 10], f"Expected [2, 4, 6, 8, 10], got {res}"
    assert elapsed < 0.08, f"Took {elapsed:.2f}s; tasks were not gathered concurrently!"


async def _delayed_task(delay: float, message: str) -> str:
    await asyncio.sleep(delay)
    return message


async def exercise_3_starter(delay: float, timeout_sec: float) -> str:
    try:
        return await asyncio.wait_for(_delayed_task(delay, "SUCCESS"), timeout=timeout_sec)
    except asyncio.TimeoutError:
        return "TIMED_OUT"


def test_exercise_3():
    res1 = asyncio.run(exercise_3_starter(delay=0.01, timeout_sec=0.10))
    assert res1 == "SUCCESS"
    res2 = asyncio.run(exercise_3_starter(delay=0.20, timeout_sec=0.02))
    assert res2 == "TIMED_OUT"


async def _long_cancellable_task() -> str:
    try:
        await asyncio.sleep(1.0)
        return "FINISHED"
    except asyncio.CancelledError:
        return "CANCELLED_GRACEFULLY"


async def exercise_4_starter() -> str:
    task = asyncio.create_task(_long_cancellable_task())
    await asyncio.sleep(0.02)
    task.cancel()
    return await task


def test_exercise_4():
    res = asyncio.run(exercise_4_starter())
    assert res == "CANCELLED_GRACEFULLY", f"Expected 'CANCELLED_GRACEFULLY', got {res}"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All Unit 2.4 solution tests passed!")
