"""
Hospital Patient Registry & Encounter Schema - Reference Solution
"""

import sqlite3
from typing import Dict, Any, List, Optional


class HospitalPatientRegistry:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mrn TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS encounters (
            encounter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            encounter_date TEXT NOT NULL,
            department TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_encounters_patient_date 
        ON encounters(patient_id, encounter_date);
        """)
        self.conn.commit()

    def register_patient(self, mrn: str, full_name: str, dob: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO patients (mrn, full_name, dob) VALUES (?, ?, ?);",
            (mrn, full_name, dob)
        )
        self.conn.commit()
        return cursor.lastrowid

    def log_encounter(self, patient_id: int, encounter_date: str, department: str, diagnosis: str) -> int:
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO encounters (patient_id, encounter_date, department, diagnosis)
                VALUES (?, ?, ?, ?);
                """,
                (patient_id, encounter_date, department, diagnosis)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as err:
            self.conn.rollback()
            raise ValueError(f"Invalid encounter reference for patient_id {patient_id}: {err}") from err

    def get_patient_encounters(self, patient_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT encounter_id, patient_id, encounter_date, department, diagnosis
            FROM encounters
            WHERE patient_id = ?
            ORDER BY encounter_date DESC;
            """,
            (patient_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_patient_summary(self, mrn: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE mrn = ?;", (mrn,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def close(self) -> None:
        self.conn.close()
