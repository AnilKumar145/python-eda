"""
Unit 3.4: Database Security, Transactions, and Best Practices - Exercises (Starter Code)
"""

import sqlite3
import time
from typing import List, Tuple, Optional, Callable, Any


# Exercise 1: SQL Injection Remediation
def secure_user_authentication(conn: sqlite3.Connection, username_input: str, password_hash: str) -> bool:
    """
    Given username_input and password_hash, query 'users' table (username TEXT, password_hash TEXT).
    Return True if user exists with matching password_hash, False otherwise.
    MUST use parameterized query. Absolutely no f-strings or string formatting!
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 2: Safe Dynamic Column Ordering
ALLOWED_SORT_MAP = {
    "name": "full_name",
    "department": "dept",
    "date": "hire_date"
}

def safe_query_staff(conn: sqlite3.Connection, sort_alias: str, order_direction: str = "ASC") -> List[Tuple]:
    """
    Query table 'staff' (staff_id INT, full_name TEXT, dept TEXT, hire_date TEXT).
    1. Validate sort_alias against ALLOWED_SORT_MAP. If invalid, raise ValueError.
    2. Validate order_direction is strictly 'ASC' or 'DESC'. If invalid, raise ValueError.
    3. Return rows sorted by mapped column and direction.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 3: Savepoint Partial Rollback
def process_prescription_bundle(conn: sqlite3.Connection, base_rx: Tuple[str, str], optional_addons: List[Tuple[str, str]]) -> int:
    """
    Table 'prescriptions' (rx_id TEXT PRIMARY KEY, drug_name TEXT).
    1. Start transaction and insert base_rx (rx_id, drug_name). This MUST succeed.
    2. Create SAVEPOINT 'addons_checkpoint'.
    3. Iterate optional_addons and attempt to insert each.
    4. If ANY optional addon fails an integrity constraint, rollback to 'addons_checkpoint' and release savepoint.
    5. Commit transaction.
    6. Return total number of prescriptions successfully committed.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE
    # ====================================================================


# Exercise 4: Query Retry with Exponential Backoff
def retry_db_call(operation: Callable[[], Any], max_attempts: int = 3, base_delay: float = 0.02) -> Any:
    """
    Execute operation. If sqlite3.OperationalError occurs and indicates 'locked',
    sleep base_delay * (2 ** attempt) and retry. Re-raise if max_attempts reached.
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
