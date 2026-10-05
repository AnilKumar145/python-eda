"""
ICU Patient Telemetry Watchdog Supervisor - Starter Code
"""

import threading
import time
from typing import List, Dict


class TelemetryWorker(threading.Thread):
    """Worker thread ingesting telemetry for a single patient."""
    
    def __init__(self, patient_id: str, stop_event: threading.Event):
        # ====================================================================
        # WRITE CODE HERE (Task 1)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def run(self):
        # ====================================================================
        # WRITE CODE HERE (Task 1)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================


class ICUWatchdogSupervisor:
    """Supervisor monitoring telemetry workers and coordinating shutdown."""
    
    def __init__(self):
        self.stop_event = threading.Event()
        self.workers: List[TelemetryWorker] = []

    def register_and_start(self, patient_id: str) -> TelemetryWorker:
        """Register and start a new telemetry worker for a patient."""
        worker = TelemetryWorker(patient_id, self.stop_event)
        self.workers.append(worker)
        worker.start()
        return worker

    def get_active_telemetry_patients(self) -> List[str]:
        """
        Scan all active threads using threading.enumerate() and return
        a sorted list of patient IDs currently being actively polled.
        """
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def shutdown_all(self, timeout: float = 1.0) -> bool:
        """
        Trigger cooperative shutdown and wait for all workers to join.
        Returns True if all workers cleanly terminated within timeout.
        """
        # ====================================================================
        # WRITE CODE HERE (Task 3)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================
