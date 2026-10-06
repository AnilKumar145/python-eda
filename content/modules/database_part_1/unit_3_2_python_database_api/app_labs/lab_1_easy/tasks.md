# Lab 1 Tasks: Clinic Batch Vitals Ingestion & Connection Pool

## Task 1: Connection Pool Implementation
- Implement class `ClinicConnectionPool`:
  - `__init__(db_path: str, max_connections: int = 4, uri: bool = False)`:
    - Pre-populate a `queue.Queue` with `max_connections` connections (`check_same_thread=False`).
  - `@contextmanager acquire(timeout: float = 1.0)`:
    - Borrow connection from queue; yield it; return it in `finally`.
  - `close_all()`:
    - Drain and close all pooled connections.

## Task 2: Schema Initialization & Batch Ingestion
- In `ClinicTelemetryPipeline`:
  - `init_schema()`:
    - Create table `telemetry_readings` (`id INTEGER PRIMARY KEY AUTOINCREMENT`, `mrn TEXT NOT NULL`, `recorded_at TEXT NOT NULL`, `heart_rate INT`, `spo2 REAL`).
  - `batch_record_vitals(records: List[Tuple[str, str, int, float]]) -> int`:
    - Borrow a connection from the pool.
    - Insert records using `cursor.executemany(...)`.
    - Commit and return number of inserted rows.
    - If error occurs, rollback and re-raise.

## Task 3: Memory-Bounded Result Streaming
- Implement `stream_patient_history(mrn: str, batch_size: int = 50) -> Generator[List[Dict[str, Any]], None, None]`:
  - Borrow a connection from pool.
  - Query readings for `mrn` ordered by `recorded_at DESC`.
  - In a loop, fetch chunks of size `batch_size` with `cursor.fetchmany()`.
  - Convert rows to dictionaries and `yield chunk`.
  - Stop when chunk is empty.
