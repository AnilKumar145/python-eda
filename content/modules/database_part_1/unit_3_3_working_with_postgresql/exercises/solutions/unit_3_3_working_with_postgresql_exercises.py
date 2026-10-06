"""
Unit 3.3: Working with PostgreSQL and Relational Stores - Solutions & Test Verification
"""

import sqlite3
import json
from decimal import Decimal
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List, Optional, Tuple


# Exercise 1: Connection URI DSN Parser
def parse_postgres_dsn(dsn: str) -> Dict[str, Any]:
    parsed = urlparse(dsn)
    qs = parse_qs(parsed.query)
    sslmode = qs.get("sslmode", ["prefer"])[0]

    return {
        "user": parsed.username or "",
        "password": parsed.password or "",
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "dbname": parsed.path.lstrip("/"),
        "sslmode": sslmode
    }


# Exercise 2: Rich Type Serialization
def store_and_retrieve_specimen(conn: sqlite3.Connection, specimen_id: str, cost: Decimal, metadata: Dict[str, Any]) -> Tuple[Decimal, Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS specimens (
        specimen_id TEXT PRIMARY KEY,
        cost_str TEXT,
        metadata_json TEXT
    );
    """)
    cursor.execute(
        "INSERT OR REPLACE INTO specimens (specimen_id, cost_str, metadata_json) VALUES (?, ?, ?);",
        (specimen_id, str(cost), json.dumps(metadata))
    )
    conn.commit()

    cursor.execute("SELECT cost_str, metadata_json FROM specimens WHERE specimen_id = ?;", (specimen_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        raise ValueError("Specimen not found")

    retrieved_cost = Decimal(row[0])
    retrieved_metadata = json.loads(row[1])
    return retrieved_cost, retrieved_metadata


# Exercise 3: Null-Safe Clinical Record Extractor
def fetch_patients_with_coalesce(conn: sqlite3.Connection) -> List[Tuple[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
    SELECT patient_name, COALESCE(discharge_date, '[STILL ADMITTED]')
    FROM admissions
    ORDER BY patient_name ASC;
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows


# Exercise 4: Dictionary Mapping Adapter
class DictQueryAdapter:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        finally:
            cursor.close()


if __name__ == "__main__":
    print("Running Unit 3.3 Solutions Test Suite...")

    # Test 1: DSN Parser
    uri = "postgresql://dr_house:vicodin99@db.hospital.org:5432/radiology_db?sslmode=require"
    parsed = parse_postgres_dsn(uri)
    assert parsed["user"] == "dr_house"
    assert parsed["password"] == "vicodin99"
    assert parsed["host"] == "db.hospital.org"
    assert parsed["port"] == 5432
    assert parsed["dbname"] == "radiology_db"
    assert parsed["sslmode"] == "require"

    # Test 2: Rich Types
    conn = sqlite3.connect(":memory:")
    cost = Decimal("249.99")
    meta = {"modality": "MRI", "slice_count": 420, "contrast": True}
    r_cost, r_meta = store_and_retrieve_specimen(conn, "SCAN-001", cost, meta)
    assert r_cost == cost
    assert isinstance(r_cost, Decimal)
    assert r_meta == meta

    # Test 3: Null-Safe Coalesce
    conn.execute("CREATE TABLE admissions (patient_name TEXT, discharge_date TEXT);")
    conn.executemany("INSERT INTO admissions VALUES (?, ?);", [
        ("Alice", "2026-03-01"),
        ("Bob", None),
        ("Charlie", "2026-03-02")
    ])
    conn.commit()

    admissions = fetch_patients_with_coalesce(conn)
    assert len(admissions) == 3
    # Bob should have '[STILL ADMITTED]'
    bob_record = next(r for r in admissions if r[0] == "Bob")
    assert bob_record[1] == "[STILL ADMITTED]"

    # Test 4: DictQueryAdapter
    adapter = DictQueryAdapter(conn)
    results = adapter.query("SELECT patient_name, discharge_date FROM admissions WHERE patient_name = ?;", ("Alice",))
    assert len(results) == 1
    assert results[0]["patient_name"] == "Alice"
    assert results[0]["discharge_date"] == "2026-03-01"

    conn.close()
    print("All Unit 3.3 Exercise Solutions PASSED!")
