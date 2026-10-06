"""
Lab 1 Easy: ICU Diagnostic Query Profiler & Slow Statement Watchdog
Student Starter Code
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
        # TODO: Implement before_cursor_execute and after_cursor_execute event hooks
        pass

    def get_recorded_queries(self) -> List[TelemetryWatchdogRecord]:
        return self.records

    def get_slow_query_count(self) -> int:
        # TODO: Return count of slow queries
        return 0

    def get_average_duration_ms(self) -> float:
        # TODO: Calculate and return average execution duration in ms
        return 0.0
