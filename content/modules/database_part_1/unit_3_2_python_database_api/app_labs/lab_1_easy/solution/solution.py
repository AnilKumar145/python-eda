"""
Clinic Batch Vitals Ingestion & Connection Pool - Reference Solution
"""

import sqlite3
from queue import Queue, Empty
from contextlib import contextmanager
from typing import List, Tuple, Generator, Dict, Any


class ClinicConnectionPool:
    def __init__(self, db_path: str, max_connections: int = 4, uri: bool = False):
        self.db_path = db_path
        self.max_connections = max_connections
        self.pool: Queue[sqlite3.Connection] = Queue(maxsize=max_connections)
        
        for _ in range(max_connections):
            conn = sqlite3.connect(db_path, check_same_thread=False, uri=uri, timeout=10.0)
            conn.execute("PRAGMA busy_timeout = 5000;")
            conn.row_factory = sqlite3.Row
            self.pool.put(conn)

    @contextmanager
    def acquire(self, timeout: float = 1.0):
        try:
            conn = self.pool.get(timeout=timeout)
        except Empty as err:
            raise TimeoutError("Connection pool capacity exhausted") from err
        try:
            yield conn
        finally:
            self.pool.put(conn)

    def close_all(self) -> None:
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            conn.close()


class ClinicTelemetryPipeline:
    def __init__(self, pool: ClinicConnectionPool):
        self.pool = pool
        self._init_schema()

    def _init_schema(self) -> None:
        with self.pool.acquire() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mrn TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                heart_rate INTEGER NOT NULL,
                spo2 REAL NOT NULL
            );
            """)
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_telemetry_mrn_time 
            ON telemetry_readings (mrn, recorded_at);
            """)
            conn.commit()

    def batch_record_vitals(self, records: List[Tuple[str, str, int, float]]) -> int:
        import time
        max_attempts = 5
        for attempt in range(max_attempts):
            with self.pool.acquire() as conn:
                cursor = conn.cursor()
                try:
                    cursor.executemany(
                        """
                        INSERT INTO telemetry_readings (mrn, recorded_at, heart_rate, spo2)
                        VALUES (?, ?, ?, ?);
                        """,
                        records
                    )
                    conn.commit()
                    return len(records)
                except sqlite3.OperationalError as err:
                    conn.rollback()
                    if "locked" in str(err) and attempt < max_attempts - 1:
                        time.sleep(0.05 * (attempt + 1))
                        continue
                    raise
                except Exception:
                    conn.rollback()
                    raise

    def stream_patient_history(self, mrn: str, batch_size: int = 50) -> Generator[List[Dict[str, Any]], None, None]:
        with self.pool.acquire() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    SELECT id, mrn, recorded_at, heart_rate, spo2
                    FROM telemetry_readings
                    WHERE mrn = ?
                    ORDER BY recorded_at DESC;
                    """,
                    (mrn,)
                )
                while True:
                    rows = cursor.fetchmany(batch_size)
                    if not rows:
                        break
                    yield [dict(row) for row in rows]
            finally:
                cursor.close()
