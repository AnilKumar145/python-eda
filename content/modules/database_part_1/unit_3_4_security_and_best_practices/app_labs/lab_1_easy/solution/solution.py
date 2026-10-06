"""
Secure Clinical Prescription Audit Ledger - Reference Solution
"""

import sqlite3
from typing import List, Tuple, Dict, Any, Optional


class PrescriptionAuditLedger:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultation_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_mrn TEXT NOT NULL,
            doctor_id TEXT NOT NULL,
            notes TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            rx_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            drug_name TEXT NOT NULL,
            dosage_mg INTEGER NOT NULL,
            is_narcotic INTEGER NOT NULL,
            FOREIGN KEY (event_id) REFERENCES consultation_events(event_id) ON DELETE CASCADE
        );
        """)
        self.conn.commit()

    def search_consultations_by_patient(self, mrn_query: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT event_id, patient_mrn, doctor_id, notes, created_at
            FROM consultation_events
            WHERE patient_mrn = ?
            ORDER BY created_at DESC;
            """,
            (mrn_query,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def record_consultation_with_prescriptions(
        self,
        patient_mrn: str,
        doctor_id: str,
        notes: str,
        created_at: str,
        rx_items: List[Tuple[str, int, bool]]
    ) -> Tuple[int, int]:
        cursor = self.conn.cursor()

        # Step 1: Insert consultation
        cursor.execute(
            """
            INSERT INTO consultation_events (patient_mrn, doctor_id, notes, created_at)
            VALUES (?, ?, ?, ?);
            """,
            (patient_mrn, doctor_id, notes, created_at)
        )
        event_id = cursor.lastrowid

        # Step 2: Savepoint for prescriptions
        cursor.execute("SAVEPOINT rx_checkpoint;")
        rejected = False

        for drug_name, dosage_mg, is_narcotic in rx_items:
            # Narcotic overdose guard: dosage cannot exceed 100mg
            if is_narcotic and dosage_mg > 100:
                rejected = True
                break

            cursor.execute(
                """
                INSERT INTO prescriptions (event_id, drug_name, dosage_mg, is_narcotic)
                VALUES (?, ?, ?, ?);
                """,
                (event_id, drug_name, dosage_mg, 1 if is_narcotic else 0)
            )

        if rejected:
            cursor.execute("ROLLBACK TO SAVEPOINT rx_checkpoint;")
            cursor.execute("RELEASE SAVEPOINT rx_checkpoint;")
            self.conn.commit()
            return event_id, 0

        cursor.execute("RELEASE SAVEPOINT rx_checkpoint;")
        self.conn.commit()
        return event_id, len(rx_items)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
