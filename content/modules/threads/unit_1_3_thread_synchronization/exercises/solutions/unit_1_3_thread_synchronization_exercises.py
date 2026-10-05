"""
Unit 1.3: Thread Synchronization - Solutions
"""

import threading
import time
from typing import List, Optional


class SafeCounter:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0

    def increment(self):
        with self.lock:
            self.value += 1

    def get_value(self) -> int:
        with self.lock:
            return self.value


def test_exercise_1():
    counter = SafeCounter()
    def worker():
        for _ in range(500):
            counter.increment()
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert counter.get_value() == 5000, f"Expected 5000, got {counter.get_value()}"


class ReentrantResource:
    def __init__(self):
        self.lock = threading.RLock()
        self.acc = 0

    def step_one(self, val: int):
        with self.lock:
            self.acc += val

    def step_two(self, val: int, bonus: int) -> int:
        with self.lock:
            self.step_one(val)
            self.acc += bonus
            return self.acc


def test_exercise_2():
    resource = ReentrantResource()
    result = resource.step_two(10, 5)
    assert result == 15, f"Expected 15, got {result}"
    result2 = resource.step_two(20, 10)
    assert result2 == 45, f"Expected 45, got {result2}"


class ThrottledWorkerPool:
    def __init__(self, max_concurrent: int):
        self.semaphore = threading.Semaphore(max_concurrent)
        self.state_lock = threading.Lock()
        self.current_active = 0
        self.peak_concurrent = 0

    def execute_task(self, work_time: float):
        with self.semaphore:
            with self.state_lock:
                self.current_active += 1
                if self.current_active > self.peak_concurrent:
                    self.peak_concurrent = self.current_active
            time.sleep(work_time)
            with self.state_lock:
                self.current_active -= 1


def test_exercise_3():
    pool = ThrottledWorkerPool(max_concurrent=3)
    threads = [threading.Thread(target=pool.execute_task, args=(0.05,)) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert pool.peak_concurrent <= 3, f"Semaphore failed: peak was {pool.peak_concurrent} > 3"
    assert pool.peak_concurrent >= 2, f"Concurrency was too low: peak was {pool.peak_concurrent}"


class SingleItemBuffer:
    def __init__(self):
        self.condition = threading.Condition()
        self.item: Optional[str] = None

    def put(self, item: str):
        with self.condition:
            while self.item is not None:
                self.condition.wait()
            self.item = item
            self.condition.notify()

    def get(self) -> str:
        with self.condition:
            while self.item is None:
                self.condition.wait()
            ret = self.item
            self.item = None
            self.condition.notify()
            return ret


def test_exercise_4():
    buf = SingleItemBuffer()
    consumed = []
    def consumer():
        for _ in range(3):
            val = buf.get()
            consumed.append(val)
    def producer():
        for i in range(3):
            time.sleep(0.02)
            buf.put(f"MSG-{i}")
    c_thread = threading.Thread(target=consumer)
    p_thread = threading.Thread(target=producer)
    c_thread.start()
    p_thread.start()
    p_thread.join()
    c_thread.join()
    assert consumed == ["MSG-0", "MSG-1", "MSG-2"], f"Expected ['MSG-0', 'MSG-1', 'MSG-2'], got {consumed}"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All Unit 1.3 solution tests passed!")
