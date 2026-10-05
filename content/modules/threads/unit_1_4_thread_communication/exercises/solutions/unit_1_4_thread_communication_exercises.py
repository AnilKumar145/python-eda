"""
Unit 1.4: Thread Communication - Solutions
"""

import threading
import queue
import time
from typing import List, Tuple, Any


def exercise_1_starter(messages: List[str]) -> List[str]:
    q = queue.Queue()
    received = []
    
    def producer():
        for m in messages:
            q.put(m)
        q.put(None)
        
    def consumer():
        while True:
            item = q.get()
            if item is None:
                break
            received.append(item)
            
    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start()
    c.start()
    p.join()
    c.join()
    return received


def test_exercise_1():
    assert exercise_1_starter(["ALPHA", "BETA", "GAMMA"]) == ["ALPHA", "BETA", "GAMMA"]
    assert exercise_1_starter([]) == []
    assert exercise_1_starter(["SOLO"]) == ["SOLO"]


def exercise_2_starter(numbers: List[int]) -> List[int]:
    if not numbers:
        return []
    work_queue = queue.Queue()
    results = []
    results_lock = threading.Lock()
    
    def worker():
        while True:
            n = work_queue.get()
            with results_lock:
                results.append(n * n)
            work_queue.task_done()
            
    for _ in range(2):
        threading.Thread(target=worker, daemon=True).start()
        
    for num in numbers:
        work_queue.put(num)
        
    work_queue.join()
    return sorted(results)


def test_exercise_2():
    assert exercise_2_starter([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]
    assert exercise_2_starter([]) == []
    assert exercise_2_starter([-3, -2, -1]) == [1, 4, 9]


def exercise_3_starter(prioritized_items: List[Tuple[int, str]]) -> List[str]:
    pq = queue.PriorityQueue()
    for item in prioritized_items:
        pq.put(item)
        
    out = []
    while not pq.empty():
        priority, val = pq.get()
        out.append(val)
    return out


def test_exercise_3():
    items = [(3, "Low"), (1, "Critical"), (2, "Medium")]
    assert exercise_3_starter(items) == ["Critical", "Medium", "Low"]
    items2 = [(10, "A"), (20, "B")]
    assert exercise_3_starter(items2) == ["A", "B"]
    assert exercise_3_starter([]) == []


def exercise_4_starter() -> Tuple[bool, bool]:
    q = queue.Queue(maxsize=1)
    q.put("First")
    was_full = q.full()
    
    second_put_finished = False
    
    def second_producer():
        nonlocal second_put_finished
        q.put("Second")
        second_put_finished = True
        
    t = threading.Thread(target=second_producer, daemon=True)
    t.start()
    
    time.sleep(0.04)
    # The second put should still be blocked waiting for capacity
    assert second_put_finished is False
    
    # Retrieve the first item, unblocking the second put
    q.get()
    t.join(timeout=0.2)
    
    return (was_full, second_put_finished)


def test_exercise_4():
    was_full, completed_after = exercise_4_starter()
    assert was_full is True
    assert completed_after is True


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All Unit 1.4 solution tests passed!")
