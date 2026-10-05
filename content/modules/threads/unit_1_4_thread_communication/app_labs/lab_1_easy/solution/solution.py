"""
Hospital ER Patient Triage Dispatcher - Solution
"""

import threading
import queue
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass(order=True)
class TriageCase:
    acuity_level: int
    patient_id: str = field(compare=False)
    patient_name: str = field(compare=False)
    condition: str = field(compare=False)


SENTINEL_CASE = TriageCase(acuity_level=999999, patient_id="__SHUTDOWN__", patient_name="", condition="")


class ERTriageDispatcher:
    def __init__(self):
        self.queue: queue.PriorityQueue = queue.PriorityQueue()
        self.treated_records: List[Tuple[str, int, str]] = []
        self._lock = threading.Lock()
        self.doctors: List[threading.Thread] = []

    def admit_patient(self, case: TriageCase) -> None:
        self.queue.put(case)

    def doctor_worker(self, doc_id: str) -> None:
        while True:
            case = self.queue.get()
            if case.patient_id == "__SHUTDOWN__":
                self.queue.task_done()
                break
            with self._lock:
                self.treated_records.append((doc_id, case.acuity_level, case.patient_id))
            self.queue.task_done()

    def start_doctors(self, count: int) -> None:
        for i in range(count):
            t = threading.Thread(target=self.doctor_worker, args=(f"Dr-{i}",))
            self.doctors.append(t)
            t.start()

    def drain_and_shutdown(self) -> None:
        self.queue.join()
        for _ in self.doctors:
            self.queue.put(SENTINEL_CASE)
        for doc in self.doctors:
            doc.join()

