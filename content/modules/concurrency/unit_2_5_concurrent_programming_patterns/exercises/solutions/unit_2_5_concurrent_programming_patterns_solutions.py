"""
Unit 2.5 Exercises: Concurrent Programming Patterns - Solutions
"""

import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Dict, Any


def run_producer_consumer_pipeline(items: List[int], queue_size: int = 2) -> List[int]:
    q: queue.Queue = queue.Queue(maxsize=queue_size)
    processed: List[int] = []

    def producer():
        for item in items:
            q.put(item)
        q.put(None)

    def consumer():
        while True:
            item = q.get()
            if item is None:
                q.task_done()
                break
            processed.append(item * 2)
            q.task_done()

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_cons.start()
    t_prod.start()

    t_prod.join()
    t_cons.join()
    return processed


def _calc_sum_squares(batch: List[int]) -> int:
    return sum(x * x for x in batch)


def fan_out_fan_in_sum_squares(batches: List[List[int]], max_workers: int = 3) -> int:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_calc_sum_squares, b) for b in batches]
        return sum(f.result() for f in futures)


class ContestedResource:
    def __init__(self, resource_id: int, initial_value: int):
        self.resource_id = resource_id
        self.value = initial_value
        self.lock = threading.Lock()


def safe_transfer(
    source: ContestedResource, 
    target: ContestedResource, 
    amount: int
) -> bool:
    first, second = sorted([source, target], key=lambda r: r.resource_id)
    with first.lock:
        with second.lock:
            if source.value >= amount:
                source.value -= amount
                target.value += amount
                return True
            return False


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from unit_2_5_concurrent_programming_patterns_exercises import (
        test_exercise_1,
        test_exercise_2,
        test_exercise_3,
    )
    import unit_2_5_concurrent_programming_patterns_exercises as ex
    ex.run_producer_consumer_pipeline = run_producer_consumer_pipeline
    ex.fan_out_fan_in_sum_squares = fan_out_fan_in_sum_squares
    ex.safe_transfer = safe_transfer
    ex.test_exercise_1()
    ex.test_exercise_2()
    ex.test_exercise_3()
    print("All Unit 2.5 Solutions Verified!")
