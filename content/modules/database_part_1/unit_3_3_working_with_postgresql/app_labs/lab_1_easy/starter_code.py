"""
Radiology DICOM Study Metadata Store - Starter Code
"""

import sqlite3
import json
from decimal import Decimal
from typing import Dict, Any, List, Optional


class RadiologyStudyStore:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        """Create imaging_studies table and index."""
        # ====================================================================
        # WRITE CODE HERE (Task 1)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def record_study(
        self,
        study_uid: str,
        patient_mrn: str,
        modality: str,
        study_date: str,
        fee: Decimal,
        metadata: Dict[str, Any],
        findings: Optional[str] = None
    ) -> None:
        """Serialize rich types and insert study record."""
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def get_study(self, study_uid: str) -> Optional[Dict[str, Any]]:
        """Fetch study and deserialize fee to Decimal and metadata to dict."""
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def list_studies_by_modality(self, modality: str) -> List[Dict[str, Any]]:
        """Query studies by modality using COALESCE for findings fallback."""
        # ====================================================================
        # WRITE CODE HERE (Task 3)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def close(self) -> None:
        self.conn.close()
