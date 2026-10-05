"""
Unit 2.2: Multiprocessing - Solutions
"""

import multiprocessing
import time
from typing import List, Tuple, Any


def _worker_multiply(val: int, out_q: multiprocessing.Queue):
    out_q.put(val * 10)

def _pipe_echo_worker(conn):
    msg = conn.recv()
    conn.send(f"ECHO_{msg}")
    conn.close()

def _clean_exit_worker():
    pass


def exercise_1_starter(values: List[int]) -> List[int]:
    if not values:
        return []
    out_q = multiprocessing.Queue()
    processes = []
    for v in values:
        p = multiprocessing.Process(target=_worker_multiply, args=(v, out_q))
        processes.append(p)
        p.start()
        
    results = [out_q.get() for _ in values]
    for p in processes:
        p.join()
    return sorted(results)


def test_exercise_1():
    res = exercise_1_starter([1, 2, 3])
    assert res == [10, 20, 30], f"Expected [10, 20, 30], got {res}"
    assert exercise_1_starter([]) == []


def exercise_2_starter(message: str) -> str:
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=_pipe_echo_worker, args=(child_conn,))
    p.start()
    parent_conn.send(message)
    resp = parent_conn.recv()
    parent_conn.close()
    p.join()
    return resp


def test_exercise_2():
    res1 = exercise_2_starter("PING")
    assert res1 == "ECHO_PING", f"Expected 'ECHO_PING', got {res1}"
    res2 = exercise_2_starter("DATA_PAYLOAD")
    assert res2 == "ECHO_DATA_PAYLOAD"


def exercise_3_starter() -> Tuple[bool, int]:
    p = multiprocessing.Process(target=_clean_exit_worker)
    p.start()
    p.join()
    return (p.is_alive(), p.exitcode)


def test_exercise_3():
    is_alive, exitcode = exercise_3_starter()
    assert is_alive is False, "Process should be dead after join()"
    assert exitcode == 0, f"Expected clean exit code 0, got {exitcode}"


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    print("All Unit 2.2 solution tests passed!")
