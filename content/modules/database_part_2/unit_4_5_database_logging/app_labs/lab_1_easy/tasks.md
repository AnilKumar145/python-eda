# Tasks: ICU Diagnostic Query Profiler & Slow Statement Watchdog

## Task 1: Define Telemetry Model
Define `TelemetryWatchdogRecord` dataclass:
- `statement: str`: Sanitized SQL command string.
- `duration_ms: float`: Execution latency in milliseconds.
- `is_slow: bool`: Flag indicating if latency >= threshold.
- `timestamp_epoch_ms: int`: Epoch timestamp when query finished.

## Task 2: Implement ICUQueryWatchdog
In `ICUQueryWatchdog`:
- `__init__(engine, slow_threshold_ms)`: Initialize watchdog with target engine and threshold.
- `attach_listeners()`: Register `before_cursor_execute` and `after_cursor_execute` hooks to engine.
- `get_recorded_queries()`: Return list of all recorded `TelemetryWatchdogRecord` instances.
- `get_slow_query_count()`: Return count of queries where `is_slow` is True.
- `get_average_duration_ms()`: Return average latency across all recorded queries in milliseconds (0.0 if empty).
