"""
Unit 3.3: Working with PostgreSQL and Relational Stores - Exercises (Starter Code)
"""

import sqlite3
import json
from decimal import Decimal
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional, Tuple


# Exercise 1: Connection URI DSN Parser
def parse_postgres_dsn(dsn: str) -> Dict[str, Any]:
    """
    Parse a PostgreSQL DSN (e.g. 'postgresql://user:pass@host:5432/dbname?sslmode=require')
    Return a dictionary with keys: 'user', 'password', 'host', 'port', 'dbname', 'sslmode'.
    Default port to 5432 and sslmode to 'prefer' if missing.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 2: Rich Type Serialization
def store_and_retrieve_specimen(conn: sqlite3.Connection, specimen_id: str, cost: Decimal, metadata: Dict[str, Any]) -> Tuple[Decimal, Dict[str, Any]]:
    """
    1. Table 'specimens' has columns: (specimen_id TEXT PRIMARY KEY, cost_str TEXT, metadata_json TEXT).
    2. Insert the given specimen, serializing cost to str and metadata to JSON string.
    3. Query by specimen_id, parse cost back into Decimal and metadata into dict.
    4. Return tuple (cost, metadata).
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 3: Null-Safe Clinical Record Extractor
def fetch_patients_with_coalesce(conn: sqlite3.Connection) -> List[Tuple[str, str]]:
    """
    Query table 'admissions' (patient_name TEXT, discharge_date TEXT nullable).
    Using SQL COALESCE, return a list of tuples (patient_name, discharge_status)
    where discharge_status is the discharge_date or '[STILL ADMITTED]' if NULL.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 4: Dictionary Mapping Adapter
class DictQueryAdapter:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return rows as a list of dictionaries mapping column name to value.
        """
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================


if __name__ == "__main__":
    print("Run solutions file to verify your exercises.")
