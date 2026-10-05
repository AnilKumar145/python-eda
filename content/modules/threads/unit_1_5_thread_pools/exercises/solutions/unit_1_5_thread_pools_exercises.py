"""
Unit 1.5: Thread Pools - Solutions
"""

from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import time
from typing import List, Tuple, Dict, Any, Callable


def exercise_1_starter(values: List[int]) -> List[int]:
    if not values:
        return []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(lambda x: x * 10, v) for v in values]
        return [f.result() for f in futures]


def test_exercise_1():
    assert exercise_1_starter([1, 2, 3, 4]) == [10, 20, 30, 40]
    assert exercise_1_starter([]) == []
    assert exercise_1_starter([-5, 0, 5]) == [-50, 0, 50]


def exercise_2_starter(words: List[str]) -> List[str]:
    if not words:
        return []
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(lambda w: w[::-1], words))


def test_exercise_2():
    assert exercise_2_starter(["python", "threads", "pool"]) == ["nohtyp", "sdaerht", "loop"]
    assert exercise_2_starter([]) == []
    assert exercise_2_starter(["racecar", "madam"]) == ["racecar", "madam"]


def exercise_3_starter(tasks: List[Tuple[str, float]]) -> List[str]:
    def delayed_task(name, delay):
        time.sleep(delay)
        return name
        
    finished = []
    with ThreadPoolExecutor(max_workers=len(tasks) or 1) as executor:
        futures = [executor.submit(delayed_task, name, delay) for name, delay in tasks]
        for fut in as_completed(futures):
            finished.append(fut.result())
    return finished


def test_exercise_3():
    task_list = [("Task-A", 0.05), ("Task-B", 0.10), ("Task-C", 0.01)]
    result = exercise_3_starter(task_list)
    assert result == ["Task-C", "Task-A", "Task-B"], f"Expected ['Task-C', 'Task-A', 'Task-B'], got {result}"


def exercise_4_starter(divisors: List[int]) -> Dict[int, Any]:
    def div_task(d):
        return 100 // d
        
    results = {}
    with ThreadPoolExecutor(max_workers=len(divisors) or 1) as executor:
        future_to_d = {executor.submit(div_task, d): d for d in divisors}
        for fut in as_completed(future_to_d):
            d = future_to_d[fut]
            try:
                results[d] = fut.result()
            except Exception:
                results[d] = "ERROR"
    return results


def test_exercise_4():
    res = exercise_4_starter([10, 0, 5, 2])
    assert res == {10: 10, 0: "ERROR", 5: 20, 2: 50}, f"Got {res}"
    assert exercise_4_starter([20, 25]) == {20: 5, 25: 4}


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All Unit 1.5 solution tests passed!")
