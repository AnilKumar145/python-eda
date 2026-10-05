"""
Unit 1.2: Thread Management - Solutions
"""

import threading
import time
from typing import List, Tuple, Optional


def exercise_1_starter(name: str) -> Tuple[bool, str]:
    def dummy():
        time.sleep(0.1)
        
    t = threading.Thread(target=dummy, name=name, daemon=True)
    t.start()
    return (t.daemon, t.name)


def test_exercise_1():
    daemon_status, thread_name = exercise_1_starter("AuditService")
    assert daemon_status is True, "Thread should be configured as daemon=True"
    assert thread_name == "AuditService", f"Expected 'AuditService', got {thread_name}"
    daemon_status2, thread_name2 = exercise_1_starter("MetricPoller")
    assert daemon_status2 is True
    assert thread_name2 == "MetricPoller"


def exercise_2_starter(prefix: str, count: int) -> List[str]:
    def dummy():
        time.sleep(0.2)
        
    threads = []
    for i in range(count):
        t = threading.Thread(target=dummy, name=f"{prefix}-{i}", daemon=True)
        threads.append(t)
        t.start()
        
    matching = [
        t.name for t in threading.enumerate()
        if t.name.startswith(prefix)
    ]
    return sorted(matching)


def test_exercise_2():
    names = exercise_2_starter("WorkerJob", 3)
    assert names == ["WorkerJob-0", "WorkerJob-1", "WorkerJob-2"], f"Got {names}"
    names2 = exercise_2_starter("SinglePoller", 1)
    assert names2 == ["SinglePoller-0"], f"Got {names2}"
    names3 = exercise_2_starter("EmptyJob", 0)
    assert names3 == [], f"Got {names3}"


def exercise_3_starter(stop_event: threading.Event, result_container: list) -> threading.Thread:
    def worker():
        count = 0
        while not stop_event.is_set():
            count += 1
            stop_event.wait(0.02)
        result_container.append(count)
        
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t


def test_exercise_3():
    event = threading.Event()
    results = []
    thread = exercise_3_starter(event, results)
    assert thread.is_alive() is True, "Thread should be running"
    time.sleep(0.08)
    event.set()
    thread.join(timeout=1.0)
    assert thread.is_alive() is False, "Thread should have terminated after stop event"
    assert len(results) == 1, f"Expected 1 recorded count, got {results}"
    assert results[0] >= 2, f"Expected counter >= 2, got {results[0]}"


def exercise_4_starter(thread_delay: float, join_timeout: float) -> bool:
    def worker():
        time.sleep(thread_delay)
        
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout=join_timeout)
    return not t.is_alive()


def test_exercise_4():
    res1 = exercise_4_starter(thread_delay=0.02, join_timeout=0.2)
    assert res1 is True, "Fast thread should have completed within timeout"
    res2 = exercise_4_starter(thread_delay=0.5, join_timeout=0.05)
    assert res2 is False, "Slow thread should have timed out"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All Unit 1.2 solution tests passed!")
