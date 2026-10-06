# Learning Outcomes: Unit 4.5 - Database Logging and Diagnostics

By the end of this unit, you will be able to:

1. **Configure SQLAlchemy Logging Subsystems**: Manage standard Python `logging` loggers (`sqlalchemy.engine`, `sqlalchemy.pool`, `sqlalchemy.dialects`, `sqlalchemy.orm`) with targeted log levels and structured formatters.
2. **Instrument Event Listeners**: Attach listeners to SQLAlchemy `Engine` and `Pool` using `@event.listens_for()` hooks (`before_cursor_execute`, `after_cursor_execute`, `checkout`, `checkin`).
3. **Build Real-Time Query Profilers**: Measure exact millisecond elapsed execution times for database statements, capturing SQL statements and parameter bindings.
4. **Implement Slow Query Alerting**: Configure thresholds (e.g. queries > 50ms) to log structured warnings, identify unindexed table scans, and trigger telemetry alerts.
5. **Monitor Connection Pool Health**: Track pool checkouts, checkins, connection borrowing duration, and detect connection leaks before pool exhaustion occurs.
