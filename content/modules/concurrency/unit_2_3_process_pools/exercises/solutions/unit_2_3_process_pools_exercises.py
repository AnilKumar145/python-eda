"""
Unit 2.3: Process Pools - Solutions
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import math
import time
from typing import List, Tuple, Dict, Any


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


def exercise_1_starter(numbers: List[int]) -> List[int]:
    if not numbers:
        return []
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(_worker_factorial, numbers))


def test_exercise_1():
    res1 = exercise_1_starter([3, 4, 5])
    assert res1 == [6, 24, 120], f"Expected [6, 24, 120], got {res1}"
    assert exercise_1_starter([]) == []
    assert exercise_1_starter([0, 1]) == [1, 1]


def exercise_2_starter(items: List[int], chunk_size: int) -> List[int]:
    if not items:
        return []
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(_worker_square, items, chunksize=chunk_size))


def test_exercise_2():
    nums = list(range(10))
    res = exercise_2_starter(nums, chunk_size=3)
    assert res == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    assert exercise_2_starter([], chunk_size=5) == []


def exercise_3_starter(tasks: List[Tuple[str, float]]) -> List[str]:
    with ProcessPoolExecutor(max_workers=len(tasks) or 1) as executor:
        futures = [executor.submit(_worker_delayed_cube, t) for t in tasks]
        return [f.result() for f in as_completed(futures)]


def test_exercise_3():
    task_list = [("Proc-Slow", 0.08), ("Proc-Fast", 0.01), ("Proc-Med", 0.04)]
    res = exercise_3_starter(task_list)
    assert res == ["Proc-Fast", "Proc-Med", "Proc-Slow"], f"Got {res}"


def exercise_4_starter(values: List[float]) -> Dict[float, Any]:
    results = {}
    with ProcessPoolExecutor(max_workers=len(values) or 1) as executor:
        future_map = {executor.submit(_worker_safe_sqrt, v): v for v in values}
        for fut in as_completed(future_map):
            v = future_map[fut]
            try:
                results[v] = fut.result()
            except Exception:
                results[v] = "INVALID"
    return results


def test_exercise_4():
    res = exercise_4_starter([9.0, -4.0, 16.0, -1.0])
    assert res[9.0] == 3.0
    assert res[-4.0] == "INVALID"
    assert res[16.0] == 4.0
    assert res[-1.0] == "INVALID"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All Unit 2.3 solution tests passed!")
