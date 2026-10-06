"""
Unit 4.5 Exercises: Database Logging and Diagnostics - Solutions & Test Verification
"""

import time
from typing import Dict, List, Any
from sqlalchemy import create_engine, Engine, text, event


class QueryMetricsCollector:

    def __init__(self):
        self.query_count: int = 0
        self.total_duration_sec: float = 0.0
        self.slow_queries: List[Dict[str, Any]] = []


def attach_query_profiler(
    engine: Engine,
    collector: QueryMetricsCollector,
    slow_threshold_sec: float = 0.005
) -> None:
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start", []).append(time.perf_counter())

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        start_time = conn.info["query_start"].pop()
        duration = time.perf_counter() - start_time

        collector.query_count += 1
        collector.total_duration_sec += duration

        if duration >= slow_threshold_sec:
            collector.slow_queries.append({
                "statement": statement,
                "duration": duration,
                "parameters": parameters
            })


def attach_pool_monitor(engine: Engine, stats: Dict[str, int]) -> None:
    @event.listens_for(engine.pool, "checkout")
    def on_checkout(dbapi_conn, connection_record, connection_proxy):
        stats["checkouts"] += 1

    @event.listens_for(engine.pool, "checkin")
    def on_checkin(dbapi_conn, connection_record):
        stats["checkins"] += 1


if __name__ == "__main__":
    print("Running Unit 4.5 Solutions Test Suite...")

    engine = create_engine("sqlite:///:memory:", echo=False)
    collector = QueryMetricsCollector()
    pool_stats = {"checkouts": 0, "checkins": 0}

    attach_query_profiler(engine, collector, slow_threshold_sec=0.002)
    attach_pool_monitor(engine, pool_stats)

    with engine.connect() as conn:
        # Fast query
        conn.execute(text("CREATE TABLE metrics (id INT, val TEXT);"))
        conn.execute(text("INSERT INTO metrics VALUES (1, 'Alpha');"))

        # Simulated slow query
        conn.execute(text("SELECT * FROM metrics WHERE id = 1;"))
        time.sleep(0.005) # Emulate work
        conn.commit()

    # Test 1: Query Count & Duration
    assert collector.query_count >= 3, f"Expected at least 3 queries, got {collector.query_count}"
    assert collector.total_duration_sec > 0.0, "Total duration must be positive"
    print(f"Exercise 1 passed: Collected {collector.query_count} queries in {collector.total_duration_sec*1000:.2f}ms.")

    # Test 2: Pool Checkouts/Checkins
    assert pool_stats["checkouts"] >= 1, "Expected at least 1 checkout"
    assert pool_stats["checkins"] >= 1, "Expected at least 1 checkin"
    print(f"Exercise 2 passed: Pool telemetry captured {pool_stats['checkouts']} checkouts.")

    print("All Unit 4.5 Exercise Solutions PASSED!")
