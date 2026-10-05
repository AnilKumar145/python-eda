"""
Hospital ER Patient Triage Dispatcher - Starter Code
"""

import threading
import queue
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


# ============================================================================
# Task 1: Prioritized TriageCase
# ============================================================================
@dataclass(order=True)
class TriageCase:
    """Prioritized emergency department patient record."""
    acuity_level: int
    patient_id: str = field(compare=False)
    patient_name: str = field(compare=False)
    condition: str = field(compare=False)
 
 
SENTINEL_CASE = TriageCase(acuity_level=999999, patient_id="__SHUTDOWN__", patient_name="", condition="")


# ============================================================================
# Tasks 2, 3, 4: ERTriageDispatcher
# ============================================================================
class ERTriageDispatcher:
    """Prioritized emergency room intake and physician dispatch coordinator."""
    
    def __init__(self):
        self.queue: queue.PriorityQueue = queue.PriorityQueue()
        self.treated_records: List[Tuple[str, int, str]] = []
        self._lock = threading.Lock()
        self.doctors: List[threading.Thread] = []

    def admit_patient(self, case: TriageCase) -> None:
        """Admit a patient case into the prioritized intake queue."""
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def doctor_worker(self, doc_id: str) -> None:
        """Physician consumer worker loop."""
        # ====================================================================
        # WRITE CODE HERE (Task 3)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def start_doctors(self, count: int) -> None:
        """Launch count physician consumer threads."""
        for i in range(count):
            t = threading.Thread(target=self.doctor_worker, args=(f"Dr-{i}",))
            self.doctors.append(t)
            t.start()

    def drain_and_shutdown(self) -> None:
        """Block until all patients are treated, then cleanly stop doctors."""
        # ====================================================================
        # WRITE CODE HERE (Task 4)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================
