"""
Unit 1.1: Threading Fundamentals - Solutions
"""

import threading
import time
from typing import List, Tuple, Any, Callable


# ============================================================================
# Exercise 1: Basic Thread Instantiation and Execution
# ============================================================================

def exercise_1_starter(value: int) -> List[int]:
    result = []
    
    def worker():
        result.append(value)
        
    t = threading.Thread(target=worker)
    t.start()
    t.join()
    return result


def test_exercise_1():
    assert exercise_1_starter(42) == [42], "Failed for value 42"
    assert exercise_1_starter(0) == [0], "Failed for value 0"
    assert exercise_1_starter(-99) == [-99], "Failed for negative integer -99"


# ============================================================================
# Exercise 2: Parameterized Thread Execution
# ============================================================================

def exercise_2_starter(base: int, multiplier: int, tag: str) -> dict:
    out_dict = {}
    
    def worker(b, m, tag=None):
        out_dict[tag] = b * m
        
    t = threading.Thread(target=worker, args=(base, multiplier), kwargs={"tag": tag})
    t.start()
    t.join()
    return out_dict


def test_exercise_2():
    res1 = exercise_2_starter(10, 5, "calc_a")
    assert res1 == {"calc_a": 50}, f"Expected {{'calc_a': 50}}, got {res1}"
    res2 = exercise_2_starter(100, 0, "zero_tag")
    assert res2 == {"zero_tag": 0}, f"Expected {{'zero_tag': 0}}, got {res2}"
    res3 = exercise_2_starter(-4, 7, "neg_tag")
    assert res3 == {"neg_tag": -28}, f"Expected {{'neg_tag': -28}}, got {res3}"


# ============================================================================
# Exercise 3: Parallel Batch Thread Coordinator
# ============================================================================

def exercise_3_starter(items: List[int], transform_fn: Callable[[int], int]) -> List[int]:
    if not items:
        return []
    results = [0] * len(items)
    
    def worker(idx, val):
        results[idx] = transform_fn(val)
        
    threads = []
    for idx, val in enumerate(items):
        t = threading.Thread(target=worker, args=(idx, val))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    return results


def test_exercise_3():
    items1 = [1, 2, 3, 4]
    assert exercise_3_starter(items1, lambda x: x * x) == [1, 4, 9, 16], "Failed squaring"
    assert exercise_3_starter([], lambda x: x + 1) == [], "Failed empty list"
    assert exercise_3_starter([10], lambda x: x * 2) == [20], "Failed single item"


# ============================================================================
# Exercise 4: Thread Lifecycle & Alive Inspection
# ============================================================================

def exercise_4_starter() -> Tuple[bool, bool]:
    def worker():
        time.sleep(0.05)
        
    t = threading.Thread(target=worker)
    t.start()
    alive_during = t.is_alive()
    t.join()
    alive_after = t.is_alive()
    return (alive_during, alive_after)


def test_exercise_4():
    during, after = exercise_4_starter()
    assert during is True, f"Thread should be alive during execution, got {during}"
    assert after is False, f"Thread should be dead after join(), got {after}"
    during2, after2 = exercise_4_starter()
    assert during2 is True and after2 is False, "Repeated lifecycle inspection failed"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All solution tests passed!")
