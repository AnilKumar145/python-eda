"""
Verification Tests for Lab 1 Easy: Clinic Batch Vitals Ingestion & Connection Pool
"""

import threading
import pytest

try:
    from solution.solution import ClinicConnectionPool, ClinicTelemetryPipeline
except (ImportError, ModuleNotFoundError):
    from starter_code import ClinicConnectionPool, ClinicTelemetryPipeline


def test_batch_ingestion_and_streaming():
    shared_db = "file:lab32_test?mode=memory&cache=shared"
    pool = ClinicConnectionPool(shared_db, max_connections=3, uri=True)
    pipeline = ClinicTelemetryPipeline(pool)

    # 1. Batch insert 120 records for patient MRN-700
    records = [
        ("MRN-700", f"2026-03-01 10:{i:02d}:00", 70 + (i % 20), 98.0 - (i % 5) * 0.5)
        for i in range(120)
    ]
    inserted = pipeline.batch_record_vitals(records)
    assert inserted == 120, f"Expected 120 inserted, got {inserted}"

    # 2. Stream back with batch_size 50
    chunks = list(pipeline.stream_patient_history("MRN-700", batch_size=50))
    assert len(chunks) == 3, f"Expected 3 chunks (50, 50, 20), got {len(chunks)}"
    assert len(chunks[0]) == 50
    assert len(chunks[1]) == 50
    assert len(chunks[2]) == 20

    # Verify descending ordering
    assert chunks[0][0]["recorded_at"] == "2026-03-01 10:99:00" or chunks[0][0]["recorded_at"] > chunks[0][1]["recorded_at"]

    pool.close_all()


def test_concurrent_pool_usage():
    shared_db = "file:lab32_concurrent?mode=memory&cache=shared"
    pool = ClinicConnectionPool(shared_db, max_connections=4, uri=True)
    pipeline = ClinicTelemetryPipeline(pool)

    # Insert batches concurrently from 4 threads
    def worker(worker_id: int):
        data = [
            (f"MRN-WORKER-{worker_id}", f"2026-03-02 08:00:{i:02d}", 75, 99.0)
            for i in range(25)
        ]
        pipeline.batch_record_vitals(data)

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()

    # Verify total rows = 100
    with pool.acquire() as conn:
        total = conn.execute("SELECT count(*) FROM telemetry_readings;").fetchone()[0]
        assert total == 100, f"Expected 100 total rows across threads, got {total}"

    pool.close_all()
