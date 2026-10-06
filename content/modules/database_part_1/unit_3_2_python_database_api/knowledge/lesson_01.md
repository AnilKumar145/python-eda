# Unit 3.2: Python Database API (DB-API 2.0)

---

## 1. Conceptual Foundation: The Universal Travel Adapter and The Bank Teller

Imagine traveling the world with a laptop. In the United Kingdom, wall sockets have three large rectangular pins; in the United States, two flat prongs; in Europe, two round pins. If your charger only fit UK sockets, you would have to buy a completely new charger for every country.

A **Universal Travel Adapter** provides one standard interface for your laptop while adapting behind the scenes to each country's socket.

- **The Database Babel**: PostgreSQL, MySQL, SQLite, and Oracle are written in C, C++, or Rust, and each has its own proprietary network protocol, binary wire format, and error codes.
- **Python's PEP 249 (DB-API 2.0)**: A universal standard that every Python database driver must follow. Whether you import `sqlite3`, `psycopg2` (PostgreSQL), or `mysql-connector-python`, they all provide the **exact same core methods**:
  - `connect()` $\to$ creates a **Connection**
  - `connection.cursor()` $\to$ creates a **Cursor**
  - `cursor.execute(sql, params)` $\to$ runs a query
  - `cursor.fetchone()`, `cursor.fetchall()`, `cursor.fetchmany()` $\to$ retrieves data
  - `connection.commit()` & `connection.rollback()` $\to$ controls transactions

Once you learn the DB-API standard in Python, you know how to connect to **every major database on earth**.

---

## 2. The PEP 249 Standard Architecture & Under-the-Hood

```
+-------------------------------------------------------------+
|                      Python Application                     |
+-------------------------------------------------------------+
                              | Standard PEP 249 Method Calls
                              v
+-------------------------------------------------------------+
|                     Python DB-API 2.0                       |
|           (Connection, Cursor, Exception Hierarchy)        |
+-------------------------------------------------------------+
          /                   |                    \
         v                    v                     v
+-----------------+  +-----------------+  +-----------------+
| sqlite3 (StdLib)|  | psycopg (Postgres)| | mysql-connector |
+-----------------+  +-----------------+  +-----------------+
         |                    |                     |
         v                    v                     v
   Local Disk File       TCP / Port 5432       TCP / Port 3306
    (SQLite DB)           (PostgreSQL)            (MySQL)
```

### Module Globals (Self-Inspection)
Every compliant driver exposes module attributes defining its capabilities:
- `apilevel`: Driver specification version (usually `'2.0'`).
- `threadsafety`: Thread safety level:
  - `0`: Threads may not share the module.
  - `1`: Threads may share the module, but not connections.
  - `2`: Threads may share the module and connections, but not cursors.
  - `3`: Threads may share the module, connections, and cursors.
- `paramstyle`: Parameter placeholder syntax:
  - `qmark`: `WHERE id = ?` (SQLite)
  - `format`: `WHERE id = %s` (psycopg2 / MySQL)
  - `named`: `WHERE id = :id` (Oracle / SQLAlchemy)

### The Standard Exception Hierarchy
PEP 249 establishes an exception tree so applications can catch database errors portably:

```
StandardError
 └── Warning
 └── Error
      ├── InterfaceError (Driver failed, e.g. dropped socket)
      └── DatabaseError
           ├── DataError (Division by zero, string value too long)
           ├── OperationalError (Database crashed, out of memory, disk full)
           ├── IntegrityError (Unique constraint or Foreign Key violated)
           ├── InternalError (Database backend bug)
           ├── ProgrammingError (Table doesn't exist, SQL syntax error)
           └── NotSupportedError (Feature not implemented by engine)
```

---

## 3. Connection and Cursor Mechanics

### 1. Connection Objects
A **Connection** manages the low-level communication socket, authentication, and transaction boundary with the database engine.
- Opening a network connection is expensive: it involves TCP 3-way handshakes, TLS handshakes, and user authentication.
- Connections maintain **transaction state**. By default, PEP 249 begins a transaction on the first DML statement (`INSERT`, `UPDATE`, `DELETE`).

### 2. Cursor Objects
A **Cursor** manages the query execution context, server-side memory buffer, and row iteration.
- You can create multiple cursors from a single connection.
- A cursor acts as a pointer moving forward through result rows.

---

## 4. Comprehensive Runnable Code Examples

### Example 1: Basic DB-API 2.0 CRUD Workflow with Explicit Commit

```python
import sqlite3

def run_db_api_crud():
    # 1. Connect
    conn = sqlite3.connect(":memory:")
    
    # 2. Allocate Cursor
    cursor = conn.cursor()

    # 3. Execute DDL
    cursor.execute("""
    CREATE TABLE clinic_appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_mrn TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """)

    # 4. Parameterized Insert (qmark style)
    cursor.execute(
        "INSERT INTO clinic_appointments (patient_mrn, doctor_name, status) VALUES (?, ?, ?);",
        ("MRN-501", "Dr. Gregory House", "SCHEDULED")
    )
    
    # Commit transaction to persist changes
    conn.commit()
    print("Inserted appointment with ID:", cursor.lastrowid)

    # 5. Query and Fetch
    cursor.execute("SELECT id, patient_mrn, doctor_name FROM clinic_appointments WHERE status = ?;", ("SCHEDULED",))
    row = cursor.fetchone()
    print("Retrieved Row:", row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_db_api_crud()
```
**Expected Output:**
```
Inserted appointment with ID: 1
Retrieved Row: (1, 'MRN-501', 'Dr. Gregory House')
```

---

### Example 2: Memory-Bounded Result Streaming with `fetchmany()`

When a query matches 500,000 rows, calling `cursor.fetchall()` loads all 500,000 rows into Python RAM at once, causing Out-Of-Memory (OOM) crashes. `fetchmany(batch_size)` streams rows in bounded chunks.

```python
import sqlite3
from typing import Generator, List, Tuple

def stream_audit_logs(batch_size: int = 100) -> Generator[List[Tuple], None, None]:
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, event TEXT);")

    # Seed 550 rows
    records = [(f"AUDIT_EVENT_{i:04d}",) for i in range(550)]
    cursor.executemany("INSERT INTO audit_logs(event) VALUES (?);", records)
    conn.commit()

    cursor.execute("SELECT id, event FROM audit_logs ORDER BY id ASC;")
    
    while True:
        chunk = cursor.fetchmany(batch_size)
        if not chunk:
            break
        yield chunk

    cursor.close()
    conn.close()

if __name__ == "__main__":
    total_processed = 0
    for batch_num, batch in enumerate(stream_audit_logs(batch_size=200), start=1):
        print(f"Batch {batch_num}: Processed {len(batch)} records (First: {batch[0][1]})")
        total_processed += len(batch)
    print(f"Total Streamed Records: {total_processed}")
```
**Expected Output:**
```
Batch 1: Processed 200 records (First: AUDIT_EVENT_0000)
Batch 2: Processed 200 records (First: AUDIT_EVENT_0200)
Batch 3: Processed 150 records (First: AUDIT_EVENT_0400)
Total Streamed Records: 550
```

---

### Example 3: Transaction Context Manager with Automatic Rollback

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def transaction(conn: sqlite3.Connection):
    """Context manager for explicit ACID transactions."""
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as err:
        conn.rollback()
        print(f"[Rollback Triggered] Error: {err}")
        raise
    finally:
        cursor.close()

def demo_transaction_rollback():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE pharmacy_stock (drug_id TEXT PRIMARY KEY, qty INT CHECK(qty >= 0));")
    conn.execute("INSERT INTO pharmacy_stock VALUES ('INSULIN', 10);")
    conn.commit()

    # Attempt an overdraw that triggers a check violation
    try:
        with transaction(conn) as cur:
            cur.execute("UPDATE pharmacy_stock SET qty = qty - 5 WHERE drug_id = 'INSULIN';")
            # This second statement fails check constraint:
            cur.execute("UPDATE pharmacy_stock SET qty = qty - 20 WHERE drug_id = 'INSULIN';")
    except Exception:
        pass # Caught after rollback

    # Verify original stock was preserved (Atomicity)
    cur = conn.cursor()
    cur.execute("SELECT qty FROM pharmacy_stock WHERE drug_id = 'INSULIN';")
    stock = cur.fetchone()[0]
    print("Stock after rolled-back transaction:", stock) # Still 10!
    conn.close()

if __name__ == "__main__":
    demo_transaction_rollback()
```
**Expected Output:**
```
[Rollback Triggered] Error: CHECK constraint failed: qty >= 0
Stock after rolled-back transaction: 10
```

---

### Example 4: Custom Thread-Safe Connection Pool

```python
import sqlite3
import threading
from queue import Queue, Empty
from contextlib import contextmanager

class SQLiteConnectionPool:
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.pool: Queue[sqlite3.Connection] = Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        
        # Pre-populate pool
        for _ in range(max_connections):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.pool.put(conn)

    @contextmanager
    def get_connection(self, timeout: float = 2.0):
        try:
            conn = self.pool.get(timeout=timeout)
        except Empty:
            raise TimeoutError("No available database connections in pool")
        try:
            yield conn
        finally:
            self.pool.put(conn) # Return to pool

    def close_all(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            conn.close()

def demo_connection_pool():
    pool = SQLiteConnectionPool(":memory:", max_connections=3)
    
    # Initialize shared table using one pooled connection
    with pool.get_connection() as conn:
        conn.execute("CREATE TABLE visitors (id INTEGER PRIMARY KEY, visitor_name TEXT);")
        conn.commit()

    def record_visitor(name: str):
        with pool.get_connection() as conn:
            conn.execute("INSERT INTO visitors (visitor_name) VALUES (?);", (name,))
            conn.commit()

    # Run 6 threads concurrently sharing 3 pooled connections
    threads = [threading.Thread(target=record_visitor, args=(f"Visitor-{i}",)) for i in range(6)]
    for t in threads: t.start()
    for t in threads: t.join()

    with pool.get_connection() as conn:
        count = conn.execute("SELECT count(*) FROM visitors;").fetchone()[0]
        print(f"Successfully inserted {count} visitors through connection pool!")

    pool.close_all()

if __name__ == "__main__":
    demo_connection_pool()
```
**Expected Output:**
```
Successfully inserted 6 visitors through connection pool!
```

---

## 5. Architecture & Implementation Comparison

| Model | Resource Overhead | Thread Safety | Latency | Scalability |
| :--- | :--- | :--- | :--- | :--- |
| **New Connection per Query** | Catastrophic (TCP handshake every request) | Safe | High (10-50ms handshake per query) | Low (Engine exhausts connection limits) |
| **Single Shared Connection** | Minimal | **Dangerous** (Race conditions on cursor state) | Low | Fails under concurrency |
| **Connection Pooling** | Controlled & bounded | **Safe** (Each thread borrows 1 connection) | Lowest (Zero handshake latency) | High |

---

## 6. Real-World Industry Use Cases

### 1. Healthcare: Vital Signs Stream Batch Flusher
An ICU telemetry hub receives 10,000 vital sign readings per second from patient bedside monitors. Instead of opening a new database connection for each reading or performing 10,000 separate `INSERT` operations, an ingestion daemon batches readings into groups of 500 and uses `cursor.executemany()` over a pooled connection, reducing database CPU load by 95%.

### 2. eCommerce: Inventory Reservation Transaction
During high-traffic checkout, an order must deduct stock from the warehouse and record an invoice line. If payment verification fails, the connection calls `connection.rollback()`. ACID atomicity guarantees that stock is never deducted without a valid payment record.

### 3. Banking: Inter-Account Balance Transfer
A transfer moves $500 from Alice's account to Bob's account. Both operations must occur within a single transaction boundary. If the server crashes after debiting Alice but before crediting Bob, the database Write-Ahead Log rolls back the debit upon recovery, preventing disappearing funds.

---

## 7. Best Practices, Anti-Patterns, and Top 3 Mistakes

### Best Practices:
1. **Always Use Parameterized Placeholders**: Never concatenate strings or format variables into SQL queries.
2. **Always Close Cursors & Return Connections**: Use `with` blocks or `try-finally` structures to guarantee connections are released back to the pool.
3. **Keep Transactions Short**: Acquire connections and begin transactions only when ready to execute; commit immediately after to release row locks and prevent deadlocks.

### Top 3 Mistakes Developers Make:

#### Mistake 1: Forgetting to Call `conn.commit()`
```python
# WRONG: The insert executes in memory but is never flushed to disk!
cursor.execute("INSERT INTO patients VALUES (1, 'Jane');")
conn.close() # Silent rollback! Jane is lost forever!

# CORRECT:
cursor.execute("INSERT INTO patients VALUES (1, 'Jane');")
conn.commit()
```

#### Mistake 2: Calling `fetchall()` on Unbounded Queries
```python
# DANGEROUS: If orders has 10,000,000 rows, this consumes all server RAM!
cursor.execute("SELECT * FROM orders;")
all_orders = cursor.fetchall()

# CORRECT: Stream with fetchmany or server-side cursor
while chunk := cursor.fetchmany(1000):
    process_chunk(chunk)
```

#### Mistake 3: Sharing a Single Connection Across Multiple Threads in SQLite
By default in Python, SQLite connections verify they are only used in the thread that created them. Passing a single connection into multiple worker threads raises `sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.`
- **Fix**: Use a thread-safe connection pool where each thread borrows its own dedicated connection.
