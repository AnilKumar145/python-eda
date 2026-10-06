"""
Unit 3.2: Python Database API (DB-API 2.0) - Solutions & Test Verification
"""

import sqlite3
from typing import List, Tuple, Generator
from queue import Queue, Empty
from contextlib import contextmanager


# Exercise 1: Fast Batch Ingestion
def batch_insert_medications(conn: sqlite3.Connection, records: List[Tuple[str, str, int]]) -> int:
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO medications (drug_code, drug_name, stock_units) VALUES (?, ?, ?);",
        records
    )
    conn.commit()
    cursor.close()
    return len(records)


# Exercise 2: Chunked Result Streamer
def stream_query_batches(conn: sqlite3.Connection, query: str, batch_size: int) -> Generator[List[Tuple], None, None]:
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        while True:
            chunk = cursor.fetchmany(batch_size)
            if not chunk:
                break
            yield chunk
    finally:
        cursor.close()


# Exercise 3: Atomic Multi-Table Transfer with Rollback
def atomic_transfer_inventory(conn: sqlite3.Connection, from_depot: str, to_depot: str, drug: str, qty: int) -> bool:
    cursor = conn.cursor()
    try:
        # Step 1: Deduct from source
        cursor.execute(
            "UPDATE depot_inventory SET quantity = quantity - ? WHERE depot_name = ? AND drug_name = ?;",
            (qty, from_depot, drug)
        )
        if cursor.rowcount == 0:
            raise ValueError(f"No stock row found for depot {from_depot}")

        # Step 2: Add to destination
        cursor.execute(
            "UPDATE depot_inventory SET quantity = quantity + ? WHERE depot_name = ? AND drug_name = ?;",
            (qty, to_depot, drug)
        )
        if cursor.rowcount == 0:
            # Insert if destination doesn't exist yet
            cursor.execute(
                "INSERT INTO depot_inventory (depot_name, drug_name, quantity) VALUES (?, ?, ?);",
                (to_depot, drug, qty)
            )

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cursor.close()


# Exercise 4: Simple Connection Pool
class MiniConnectionPool:
    def __init__(self, db_path: str, size: int = 3, uri: bool = False):
        self.db_path = db_path
        self.size = size
        self.pool: Queue[sqlite3.Connection] = Queue(maxsize=size)
        for _ in range(size):
            conn = sqlite3.connect(db_path, check_same_thread=False, uri=uri)
            self.pool.put(conn)

    @contextmanager
    def acquire(self, timeout: float = 1.0):
        try:
            conn = self.pool.get(timeout=timeout)
        except Empty as err:
            raise TimeoutError("Connection pool exhausted") from err
        try:
            yield conn
        finally:
            self.pool.put(conn)

    def close(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            conn.close()


if __name__ == "__main__":
    print("Running Unit 3.2 Solutions Test Suite...")

    # Test 1: Batch Insert
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE medications (drug_code TEXT, drug_name TEXT, stock_units INT);")
    drugs = [
        ("AMX-500", "Amoxicillin 500mg", 100),
        ("IBU-200", "Ibuprofen 200mg", 250),
        ("MET-500", "Metformin 500mg", 180)
    ]
    inserted = batch_insert_medications(conn, drugs)
    assert inserted == 3, f"Expected 3 inserted, got {inserted}"
    assert conn.execute("SELECT count(*) FROM medications;").fetchone()[0] == 3

    # Test 2: Streamer
    # Insert 100 rows into a temp table
    conn.execute("CREATE TABLE stream_data (val INT);")
    conn.executemany("INSERT INTO stream_data VALUES (?);", [(i,) for i in range(25)])
    conn.commit()

    chunks = list(stream_query_batches(conn, "SELECT val FROM stream_data ORDER BY val;", batch_size=10))
    assert len(chunks) == 3, f"Expected 3 chunks (10, 10, 5), got {len(chunks)}"
    assert len(chunks[0]) == 10
    assert len(chunks[2]) == 5

    # Test 3: Atomic Transfer with Rollback
    conn.execute("""
    CREATE TABLE depot_inventory (
        depot_name TEXT,
        drug_name TEXT,
        quantity INT CHECK(quantity >= 0),
        PRIMARY KEY(depot_name, drug_name)
    );
    """)
    conn.execute("INSERT INTO depot_inventory VALUES ('North', 'Aspirin', 50);")
    conn.execute("INSERT INTO depot_inventory VALUES ('South', 'Aspirin', 20);")
    conn.commit()

    # Valid transfer: 15 units
    success = atomic_transfer_inventory(conn, "North", "South", "Aspirin", 15)
    assert success is True
    assert conn.execute("SELECT quantity FROM depot_inventory WHERE depot_name = 'North';").fetchone()[0] == 35
    assert conn.execute("SELECT quantity FROM depot_inventory WHERE depot_name = 'South';").fetchone()[0] == 35

    # Invalid transfer: 100 units (exceeds 35 in North, triggers CHECK constraint)
    failed = atomic_transfer_inventory(conn, "North", "South", "Aspirin", 100)
    assert failed is False
    # Verify rollback: values untouched!
    assert conn.execute("SELECT quantity FROM depot_inventory WHERE depot_name = 'North';").fetchone()[0] == 35
    assert conn.execute("SELECT quantity FROM depot_inventory WHERE depot_name = 'South';").fetchone()[0] == 35

    # Test 4: Pool with shared cache
    shared_db = "file:unit32_pool?mode=memory&cache=shared"
    pool = MiniConnectionPool(shared_db, size=2, uri=True)
    with pool.acquire() as c1:
        c1.execute("CREATE TABLE ping (id INT);")
        c1.commit()

    with pool.acquire() as c2:
        c2.execute("INSERT INTO ping VALUES (1);")
        c2.commit()

    with pool.acquire() as c3:
        assert c3.execute("SELECT count(*) FROM ping;").fetchone()[0] == 1

    pool.close()
    conn.close()

    print("All Unit 3.2 Exercise Solutions PASSED!")
