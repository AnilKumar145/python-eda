"""
Unit 3.4: Database Security, Transactions, and Best Practices - Solutions & Test Verification
"""

import sqlite3
import time
from typing import List, Tuple, Optional, Callable, Any


# Exercise 1: SQL Injection Remediation
def secure_user_authentication(conn: sqlite3.Connection, username_input: str, password_hash: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE username = ? AND password_hash = ?;",
        (username_input, password_hash)
    )
    row = cursor.fetchone()
    cursor.close()
    return row is not None


# Exercise 2: Safe Dynamic Column Ordering
ALLOWED_SORT_MAP = {
    "name": "full_name",
    "department": "dept",
    "date": "hire_date"
}

def safe_query_staff(conn: sqlite3.Connection, sort_alias: str, order_direction: str = "ASC") -> List[Tuple]:
    if sort_alias not in ALLOWED_SORT_MAP:
        raise ValueError(f"Invalid sort alias: {sort_alias}")

    direction = order_direction.upper()
    if direction not in ("ASC", "DESC"):
        raise ValueError(f"Invalid direction: {order_direction}")

    actual_col = ALLOWED_SORT_MAP[sort_alias]
    sql = f"SELECT staff_id, full_name, dept, hire_date FROM staff ORDER BY {actual_col} {direction};"
    cursor = conn.cursor()
    rows = cursor.execute(sql).fetchall()
    cursor.close()
    return rows


# Exercise 3: Savepoint Partial Rollback
def process_prescription_bundle(conn: sqlite3.Connection, base_rx: Tuple[str, str], optional_addons: List[Tuple[str, str]]) -> int:
    cursor = conn.cursor()
    # 1. Base Rx
    cursor.execute("INSERT INTO prescriptions (rx_id, drug_name) VALUES (?, ?);", base_rx)

    # 2. Savepoint for optional addons
    cursor.execute("SAVEPOINT addons_checkpoint;")
    addon_failed = False
    try:
        for addon in optional_addons:
            cursor.execute("INSERT INTO prescriptions (rx_id, drug_name) VALUES (?, ?);", addon)
    except sqlite3.IntegrityError:
        addon_failed = True
        cursor.execute("ROLLBACK TO SAVEPOINT addons_checkpoint;")

    cursor.execute("RELEASE SAVEPOINT addons_checkpoint;")
    conn.commit()

    # Count total prescriptions
    count = conn.execute("SELECT count(*) FROM prescriptions;").fetchone()[0]
    cursor.close()
    return count


# Exercise 4: Query Retry with Exponential Backoff
def retry_db_call(operation: Callable[[], Any], max_attempts: int = 3, base_delay: float = 0.02) -> Any:
    for attempt in range(max_attempts):
        try:
            return operation()
        except sqlite3.OperationalError as err:
            if "locked" in str(err) and attempt < max_attempts - 1:
                time.sleep(base_delay * (2 ** attempt))
                continue
            raise


if __name__ == "__main__":
    print("Running Unit 3.4 Solutions Test Suite...")

    # Test 1: Secure Auth
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (username TEXT, password_hash TEXT);")
    conn.execute("INSERT INTO users VALUES ('dr_clark', 'hash_pass_123');")
    conn.commit()

    # Valid login
    assert secure_user_authentication(conn, "dr_clark", "hash_pass_123") is True
    # Failed login
    assert secure_user_authentication(conn, "dr_clark", "wrong_hash") is False
    # Injection attempt should fail safely
    assert secure_user_authentication(conn, "' OR '1'='1", "whatever") is False

    # Test 2: Safe Staff Query
    conn.execute("CREATE TABLE staff (staff_id INT, full_name TEXT, dept TEXT, hire_date TEXT);")
    conn.executemany("INSERT INTO staff VALUES (?, ?, ?, ?);", [
        (1, "Bob Jones", "Pediatrics", "2024-01-15"),
        (2, "Alice Smith", "Cardiology", "2023-06-01"),
        (3, "Charlie Day", "Emergency", "2025-09-20")
    ])
    conn.commit()

    rows = safe_query_staff(conn, "name", "ASC")
    assert rows[0][1] == "Alice Smith"

    try:
        safe_query_staff(conn, "invalid_column", "ASC")
        assert False, "Should raise ValueError for invalid column"
    except ValueError:
        pass

    try:
        safe_query_staff(conn, "name", "SLEEP(5)")
        assert False, "Should raise ValueError for invalid direction"
    except ValueError:
        pass

    # Test 3: Savepoint Bundle
    conn.execute("CREATE TABLE prescriptions (rx_id TEXT PRIMARY KEY, drug_name TEXT);")
    conn.commit()

    # Bundle with duplicate addon
    base = ("RX-001", "Amoxicillin")
    addons = [("RX-002", "Ibuprofen"), ("RX-001", "Duplicate Collision")] # Will fail uniqueness
    total = process_prescription_bundle(conn, base, addons)
    assert total == 1, f"Expected only base prescription (1), got {total}"

    # Bundle with valid addons
    base2 = ("RX-010", "Metformin")
    addons2 = [("RX-011", "Lisinopril"), ("RX-012", "Atorvastatin")]
    total2 = process_prescription_bundle(conn, base2, addons2)
    assert total2 == 4, f"Expected 4 total prescriptions, got {total2}"

    # Test 4: Retry DB Call
    tries = [0]
    def flaky_func():
        tries[0] += 1
        if tries[0] < 3:
            raise sqlite3.OperationalError("database is locked")
        return "SUCCESS"

    res = retry_db_call(flaky_func, max_attempts=4)
    assert res == "SUCCESS"
    assert tries[0] == 3

    conn.close()
    print("All Unit 3.4 Exercise Solutions PASSED!")
