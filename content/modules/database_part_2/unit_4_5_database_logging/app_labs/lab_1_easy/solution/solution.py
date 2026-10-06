"""
Lab 1 Easy: ICU Diagnostic Query Profiler & Slow Statement Watchdog
Reference Solution
"""

import time
from dataclasses import dataclass
from typing import List
from sqlalchemy import Engine, event


@dataclass
class TelemetryWatchdogRecord:
    statement: str
    duration_ms: float
    is_slow: bool
    timestamp_epoch_ms: int


class ICUQueryWatchdog:

    def __init__(self, engine: Engine, slow_threshold_ms: float = 20.0):
        self.engine = engine
        self.slow_threshold_ms = slow_threshold_ms
        self.records: List[TelemetryWatchdogRecord] = []

    def attach_listeners(self) -> None:
        @event.listens_for(self.engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault("watchdog_start", []).append(time.perf_counter())

        @event.listens_for(self.engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            start = conn.info["watchdog_start"].pop()
            elapsed_sec = time.perf_counter() - start
            elapsed_ms = elapsed_sec * 1000.0

            is_slow = elapsed_ms >= self.slow_threshold_ms
            clean_stmt = statement.replace("\n", " ").strip()

            record = TelemetryWatchdogRecord(
                statement=clean_stmt,
                duration_ms=round(elapsed_ms, 3),
                is_slow=is_slow,
                timestamp_epoch_ms=int(time.time() * 1000)
            )
            self.records.append(record)

    def get_recorded_queries(self) -> List[TelemetryWatchdogRecord]:
        return self.records

    def get_slow_query_count(self) -> int:
        return sum(1 for r in self.records if r.is_slow)

    def get_average_duration_ms(self) -> float:
        if not self.records:
            return 0.0
        total = sum(r.duration_ms for r in self.records)
        return round(total / len(self.records), 3)
