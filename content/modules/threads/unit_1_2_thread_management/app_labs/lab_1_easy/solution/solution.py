"""
ICU Patient Telemetry Watchdog Supervisor - Solution
"""

import threading
import time
from typing import List, Dict


class TelemetryWorker(threading.Thread):
    def __init__(self, patient_id: str, stop_event: threading.Event):
        super().__init__(name=f"Telemetry-{patient_id}", daemon=False)
        self.patient_id = patient_id
        self.stop_event = stop_event
        self.iterations = 0

    def run(self):
        while not self.stop_event.is_set():
            self.iterations += 1
            self.stop_event.wait(0.05)


class ICUWatchdogSupervisor:
    def __init__(self):
        self.stop_event = threading.Event()
        self.workers: List[TelemetryWorker] = []

    def register_and_start(self, patient_id: str) -> TelemetryWorker:
        worker = TelemetryWorker(patient_id, self.stop_event)
        self.workers.append(worker)
        worker.start()
        return worker

    def get_active_telemetry_patients(self) -> List[str]:
        matching = []
        for t in threading.enumerate():
            if t.name.startswith("Telemetry-") and t.is_alive():
                patient_id = t.name.replace("Telemetry-", "")
                matching.append(patient_id)
        return sorted(matching)

    def shutdown_all(self, timeout: float = 1.0) -> bool:
        self.stop_event.set()
        all_clean = True
        for w in self.workers:
            w.join(timeout=timeout)
            if w.is_alive():
                all_clean = False
        return all_clean
