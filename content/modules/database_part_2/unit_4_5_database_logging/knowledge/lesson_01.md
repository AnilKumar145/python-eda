# Lesson 4.5: SQLAlchemy Logging Architecture, Event Listeners, and Profiling

---

## 1. Conceptual Foundation

When an ORM generates SQL queries under the hood, software engineers often face the **"Black Box Problem"**:
- Which SQL query actually executed across the network?
- How long did the database engine spend evaluating the query?
- Why did a simple patient lookup take 400 milliseconds instead of 2 milliseconds?
- Is an application thread holding an open database connection idle, preventing other threads from acquiring one?

Without observability, database bottlenecks remain invisible until the system suffers an outage.

SQLAlchemy provides a comprehensive diagnostic infrastructure:
1. **Hierarchical Standard Logging**: Built on Python's native `logging` module with separate loggers for queries, connection pools, dialects, and ORM units.
2. **The Event System (`sqlalchemy.event`)**: A high-performance pub/sub hook mechanism that notifies your application before and after every query execution, connection checkout, and transaction boundary.

```
+------------------------------------------------------------------------+
|                          Application Query                             |
|          session.scalars(select(Patient).where(...)).all()             |
+-----------------------------------+------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                    SQLAlchemy Event Interceptor                        |
|   1. before_cursor_execute: Record start timestamp in conn.info        |
|   2. Execute SQL query on physical database connection                 |
|   3. after_cursor_execute: Calculate duration (now - start)            |
|   4. If duration > SLOW_QUERY_THRESHOLD: Log structured warning!       |
+-----------------------------------+------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                 Structured Observability & Metrics Logs                |
|      [WARN] SLOW_QUERY: duration=65ms, sql='SELECT * FROM patients...' |
+------------------------------------------------------------------------+
```

---

## 2. Architecture & Internal Mechanics

### Standard Loggers in SQLAlchemy
SQLAlchemy structures its internal diagnostics under the root `"sqlalchemy"` logger namespace:

| Logger Name | Recommended Level | Description |
| :--- | :--- | :--- |
| `sqlalchemy.engine` | `INFO` / `DEBUG` | Logs SQL statements (`INFO`) and bound parameters + result sets (`DEBUG`). |
| `sqlalchemy.pool` | `INFO` / `DEBUG` | Logs connection checkouts, checkins, pool invalidations, and overflow creation. |
| `sqlalchemy.dialects` | `INFO` | Logs dialect-specific execution, encoding negotiations, and type mapping. |
| `sqlalchemy.orm` | `INFO` | Logs unit-of-work flushes, cascade operations, and identity map resolutions. |

### The `create_engine(..., echo=True)` Flag
Setting `echo=True` on `create_engine` is simply shorthand for:
```python
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
```
Setting `echo="debug"` sets the logger level to `logging.DEBUG` (which includes result row contents).

---

## 3. Real-World Code Implementation & Patterns

### 1. Attaching Execution Profilers via Event Listeners
SQLAlchemy's `Connection.info` dictionary provides a thread-safe scratchpad per connection to pass state between `before` and `after` events:

```python
import time
import logging
from sqlalchemy import create_engine, event, Engine

logger = logging.getLogger("db.performance")

def setup_query_profiler(engine: Engine, slow_threshold_sec: float = 0.05):
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        # Store start timestamp on the connection's info dictionary
        conn.info.setdefault("query_start_time", []).append(time.perf_counter())

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total_time = time.perf_counter() - conn.info["query_start_time"].pop()
        
        # Log slow queries exceeding threshold
        if total_time >= slow_threshold_sec:
            logger.warning(
                "SLOW SQL (%.2fms): %s | Params: %s",
                total_time * 1000,
                statement.replace("\n", " ").strip(),
                parameters
            )
```

### 2. Connection Pool Telemetry Hooks
```python
from sqlalchemy.pool import Pool

def setup_pool_monitoring(engine: Engine):
    @event.listens_for(engine.pool, "checkout")
    def on_checkout(dbapi_conn, connection_record, connection_proxy):
        connection_record.info["checkout_time"] = time.perf_counter()

    @event.listens_for(engine.pool, "checkin")
    def on_checkin(dbapi_conn, connection_record):
        borrowed_duration = time.perf_counter() - connection_record.info.get("checkout_time", time.perf_counter())
        if borrowed_duration > 1.0: # Held for more than 1 second!
            logger.warning("CONNECTION LEAK RISK: Connection held for %.2fs before checkin", borrowed_duration)
```

---

## 4. Failure Modes & Edge Cases

| Failure Mode | Symptoms | Root Cause & Resolution |
| :--- | :--- | :--- |
| **`echo=True` Left in Production** | Disk fills rapidly; CPU spikes; HIPAA/GDPR PHI leaked in logs. | Never use `echo=True` in production. Use targeted event listeners with scrubbed parameters. |
| **Connection Info Stack Desynchronization** | Pop from empty list in `after_cursor_execute`. | Occurs if an exception halts execution between before and after hooks. Use `handle_error` event to clear stack. |
| **Logging High-Cardinality Inserts** | Application throughput drops 80% during batch jobs. | Disable per-row logging during bulk inserts; log batch summary execution times instead. |
| **Unbounded Pool Queue Deadlocks** | All worker threads hang waiting on pool checkout. | Set `pool_timeout=5` and log warnings when `checkedout() == pool_size`. |

---

## 5. Performance & Optimization: Overhead of Profiling

Calling `time.perf_counter()` adds negligible overhead (~20 nanoseconds per query on modern x86/ARM CPUs). 

However:
- Formatting complex SQL strings (`str(statement)`) and pretty-printing JSON parameters is expensive.
- **Optimization Strategy**: Only format and construct logging strings **if** the elapsed time exceeds the slow query threshold! Avoid string formatting in `before_cursor_execute`.

---

## 6. Industry Best Practices & Production Patterns

1. **Parameter Masking (Data Sanitization)**:
   In healthcare and banking systems, parameters often contain Social Security Numbers, MRNs, or passwords. Never log raw parameter dictionaries to disk unredacted.
2. **Emit OpenTelemetry / Prometheus Metrics**:
   Instead of writing plain text logs to stdout, emit a Prometheus histogram (`db_query_duration_seconds.observe(total_time)`) to plot 95th and 99th percentile query latencies on Grafana dashboards.
3. **Handle Errors in `handle_error` Event**:
   Register a listener for `@event.listens_for(engine, "handle_error")` to capture SQL statements and stack traces when exceptions occur.

---

## 7. Healthcare Domain Case Study: ICU Slow Statement Watchdog

An ICU dashboard service suffered intermittent 3-second UI freezes during morning physician rounds. Standard application logs showed normal CPU and memory utilization.

By deploying SQLAlchemy's `before_cursor_execute` / `after_cursor_execute` profiler with a 50ms slow query alert:
1. The profiler immediately flagged a query:
   ```sql
   SELECT * FROM vital_telemetry WHERE patient_id = 450 ORDER BY recorded_at DESC;
   ```
2. Execution time: **2,850ms**!
3. Root cause: The `vital_telemetry` table contained 40 million rows, and the composite index `(patient_id, recorded_at)` had been accidentally dropped during a previous deployment, forcing the engine into a full table scan.
4. Adding the index reduced query latency to **1.2ms**, completely eliminating the UI freeze.

---

## 8. Hands-On Verification & Knowledge Check

1. Why should `echo=True` never be enabled in production healthcare deployments?
2. How does the `conn.info` dictionary enable thread-safe state sharing between `before_cursor_execute` and `after_cursor_execute`?
3. What is the operational distinction between logging query duration and tracking connection pool borrow duration?
