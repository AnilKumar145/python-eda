"""
Radiology DICOM Study Metadata Store - Reference Solution
"""

import sqlite3
import json
from decimal import Decimal
from typing import Dict, Any, List, Optional


class RadiologyStudyStore:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS imaging_studies (
            study_uid TEXT PRIMARY KEY,
            patient_mrn TEXT NOT NULL,
            modality TEXT NOT NULL,
            study_date TEXT NOT NULL,
            fee_amount TEXT NOT NULL,
            dicom_metadata TEXT NOT NULL,
            findings TEXT
        );
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_imaging_patient_modality
        ON imaging_studies (patient_mrn, modality);
        """)
        self.conn.commit()

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
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO imaging_studies 
            (study_uid, patient_mrn, modality, study_date, fee_amount, dicom_metadata, findings)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (study_uid, patient_mrn, modality, study_date, str(fee), json.dumps(metadata), findings)
        )
        self.conn.commit()

    def get_study(self, study_uid: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM imaging_studies WHERE study_uid = ?;", (study_uid,))
        row = cursor.fetchone()
        if not row:
            return None

        d = dict(row)
        d["fee_amount"] = Decimal(d["fee_amount"])
        d["dicom_metadata"] = json.loads(d["dicom_metadata"])
        return d

    def list_studies_by_modality(self, modality: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT study_uid, patient_mrn, modality, study_date, fee_amount,
                   COALESCE(findings, '[PENDING RADIOLOGIST REVIEW]') AS findings_status,
                   dicom_metadata
            FROM imaging_studies
            WHERE modality = ?
            ORDER BY study_date DESC;
            """,
            (modality,)
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["fee_amount"] = Decimal(d["fee_amount"])
            d["dicom_metadata"] = json.loads(d["dicom_metadata"])
            results.append(d)
        return results

    def close(self) -> None:
        self.conn.close()
