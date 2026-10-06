"""
Hospital Patient Registry & Encounter Schema - Starter Code
"""

import sqlite3
from typing import Dict, Any, List, Optional


class HospitalPatientRegistry:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize relational tables and compound index."""
        # ====================================================================
        # WRITE CODE HERE (Task 1)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def register_patient(self, mrn: str, full_name: str, dob: str) -> int:
        """Insert a patient and return generated patient_id."""
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def log_encounter(self, patient_id: int, encounter_date: str, department: str, diagnosis: str) -> int:
        """
        Insert an encounter and return encounter_id.
        Raise ValueError if patient_id violates foreign key constraints.
        """
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def get_patient_encounters(self, patient_id: int) -> List[Dict[str, Any]]:
        """Return all encounters for patient ordered by encounter_date DESC."""
        # ====================================================================
        # WRITE CODE HERE (Task 3)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def get_patient_summary(self, mrn: str) -> Optional[Dict[str, Any]]:
        """Fetch patient record by MRN."""
        # ====================================================================
        # WRITE CODE HERE (Task 3)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def close(self) -> None:
        self.conn.close()
