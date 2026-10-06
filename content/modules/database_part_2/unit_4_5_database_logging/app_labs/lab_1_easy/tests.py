"""
Test suite for Lab 1 Easy: ICU Diagnostic Query Profiler & Slow Statement Watchdog
"""

import time
import pytest
from sqlalchemy import create_engine, text
from solution.solution import ICUQueryWatchdog, TelemetryWatchdogRecord


@pytest.fixture
def watchdog_fixture():
    engine = create_engine("sqlite:///:memory:", echo=False)
    watchdog = ICUQueryWatchdog(engine, slow_threshold_ms=10.0)
    watchdog.attach_listeners()
    yield watchdog, engine
    engine.dispose()


def test_watchdog_records_statements(watchdog_fixture):
    watchdog, engine = watchdog_fixture

    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE vitals (id INT, hr INT);"))
        conn.execute(text("INSERT INTO vitals VALUES (1, 80);"))
        conn.execute(text("SELECT * FROM vitals;"))
        conn.commit()

    records = watchdog.get_recorded_queries()
    assert len(records) >= 3, f"Expected at least 3 queries recorded, got {len(records)}"
    statements = [r.statement for r in records]
    assert any("CREATE TABLE vitals" in s for s in statements)
    assert any("INSERT INTO vitals" in s for s in statements)


def test_watchdog_flags_slow_queries(watchdog_fixture):
    watchdog, engine = watchdog_fixture

    with engine.connect() as conn:
        # Fast query
        conn.execute(text("SELECT 1;"))

        # Fast query with threshold = 0.5ms to reliably catch work
        watchdog.slow_threshold_ms = 0.5
        time.sleep(0.002) # Emulate work
        conn.execute(text("SELECT 42;"))
        conn.commit()

    records = watchdog.get_recorded_queries()
    assert len(records) >= 2
    avg_duration = watchdog.get_average_duration_ms()
    assert avg_duration >= 0.0


def test_empty_watchdog_average():
    engine = create_engine("sqlite:///:memory:", echo=False)
    watchdog = ICUQueryWatchdog(engine)
    assert watchdog.get_average_duration_ms() == 0.0
    assert watchdog.get_slow_query_count() == 0
    engine.dispose()
