"""
Unit 3.1: Database Fundamentals - Solutions & Test Verification
"""

import sqlite3
from typing import List, Tuple, Optional


# Exercise 1: Clinic Schema Builder
def initialize_clinic_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinics (
        clinic_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        city TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INTEGER PRIMARY KEY,
        clinic_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id) ON DELETE CASCADE
    );
    """)
    conn.commit()


# Exercise 2: Filter Patients by Department
def get_patients_by_department(conn: sqlite3.Connection, department: str) -> List[Tuple[int, str]]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT patient_id, full_name FROM patients WHERE department = ? ORDER BY full_name ASC;",
        (department,)
    )
    return cursor.fetchall()


# Exercise 3: Foreign Key Guard
def safe_insert_doctor(conn: sqlite3.Connection, doctor_id: int, clinic_id: int, full_name: str, specialty: str) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO doctors (doctor_id, clinic_id, full_name, specialty) VALUES (?, ?, ?, ?);",
            (doctor_id, clinic_id, full_name, specialty)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False


# Exercise 4: Create Index and Verify Plan
def create_index_and_explain(conn: sqlite3.Connection, table: str, column: str, index_name: str) -> str:
    cursor = conn.cursor()
    cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column});")
    conn.commit()
    cursor.execute(f"EXPLAIN QUERY PLAN SELECT * FROM {table} WHERE {column} = ?;", ("SAMPLE_VALUE",))
    plan = cursor.fetchone()
    return plan[3] # Detail message


if __name__ == "__main__":
    print("Running Unit 3.1 Solutions Test Suite...")

    # Test 1: Schema Initialization
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    initialize_clinic_schema(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "clinics" in tables and "doctors" in tables, "Clinics and doctors tables must exist"

    # Test 2: Filter Patients
    conn.execute("CREATE TABLE patients (patient_id INTEGER PRIMARY KEY, full_name TEXT, department TEXT);")
    conn.executemany("INSERT INTO patients VALUES (?, ?, ?);", [
        (1, "David Miller", "Cardiology"),
        (2, "Alice Smith", "Cardiology"),
        (3, "Bob Vance", "Neurology"),
        (4, "Chloe Jones", "Cardiology")
    ])
    conn.commit()
    cardiology_patients = get_patients_by_department(conn, "Cardiology")
    assert len(cardiology_patients) == 3, f"Expected 3 cardiology patients, got {len(cardiology_patients)}"
    assert cardiology_patients[0][1] == "Alice Smith", "Expected ordering by full_name"

    # Test 3: Foreign Key Guard
    conn.execute("INSERT INTO clinics VALUES (10, 'Central Health', 'Chicago');")
    conn.commit()

    success = safe_insert_doctor(conn, 101, 10, "Dr. Gregory House", "Diagnostics")
    assert success is True, "Valid doctor insert should succeed"

    failure = safe_insert_doctor(conn, 102, 999, "Dr. John Watson", "General") # 999 does not exist
    assert failure is False, "Foreign key violation must return False"

    # Test 4: Index and Plan
    conn.execute("CREATE TABLE records (record_id INTEGER PRIMARY KEY, ssn TEXT, notes TEXT);")
    conn.commit()
    plan_detail = create_index_and_explain(conn, "records", "ssn", "idx_records_ssn")
    assert "INDEX idx_records_ssn" in plan_detail, f"Expected query plan to use index, got {plan_detail}"

    conn.close()
    print("All Unit 3.1 Exercise Solutions PASSED!")
