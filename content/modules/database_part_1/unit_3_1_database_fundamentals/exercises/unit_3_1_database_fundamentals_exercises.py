"""
Unit 3.1: Database Fundamentals - Exercises (Starter Code)
"""

import sqlite3
from typing import List, Tuple, Optional


# Exercise 1: Clinic Schema Builder
def initialize_clinic_schema(conn: sqlite3.Connection) -> None:
    """
    Enforce foreign keys and create two tables:
    1. 'clinics' (
           clinic_id INTEGER PRIMARY KEY,
           name TEXT NOT NULL UNIQUE,
           city TEXT NOT NULL
       )
    2. 'doctors' (
           doctor_id INTEGER PRIMARY KEY,
           clinic_id INTEGER NOT NULL,
           full_name TEXT NOT NULL,
           specialty TEXT NOT NULL,
           FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id) ON DELETE CASCADE
       )
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 2: Filter Patients by Department
def get_patients_by_department(conn: sqlite3.Connection, department: str) -> List[Tuple[int, str]]:
    """
    Query the 'patients' table for patient_id and full_name where department matches the parameter,
    ordered by full_name ascending. Return a list of tuples.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 3: Foreign Key Guard
def safe_insert_doctor(conn: sqlite3.Connection, doctor_id: int, clinic_id: int, full_name: str, specialty: str) -> bool:
    """
    Insert a doctor row into 'doctors'.
    If the clinic_id violates foreign key constraints (or fails any integrity constraint),
    catch sqlite3.IntegrityError, rollback the transaction, and return False.
    Otherwise commit and return True.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 4: Create Index and Verify Plan
def create_index_and_explain(conn: sqlite3.Connection, table: str, column: str, index_name: str) -> str:
    """
    1. Create an index named index_name on table(column).
    2. Execute 'EXPLAIN QUERY PLAN SELECT * FROM {table} WHERE {column} = ?' with a sample string.
    3. Return the query plan detail string (4th column of explanation tuple).
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


if __name__ == "__main__":
    print("Run the solutions file to test your implementations.")
