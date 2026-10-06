# Unit 3.3: Working with PostgreSQL and Relational Stores

---

## 1. Conceptual Foundation: The Local Notebook vs. The Central Hospital Vault

Imagine how medical data is recorded:

- **The Local Notebook (SQLite)**: A doctor writes prescriptions in a small pocket spiral notebook. It is ultra-portable, requires zero setup, and fits in a lab coat pocket. However, if 50 doctors need to write in the same notebook simultaneously from different surgical theaters, they cannot do it.
- **The Central Hospital Vault (PostgreSQL)**: A secure, climate-controlled institutional record center. Hundreds of nurses, pharmacists, and lab technicians access it over encrypted telephone lines (TCP/IP network connections) at the exact same second. It supports specialized filing formats: raw text, high-resolution radiology metadata (JSONB documents), precise medication dosage measurements (fixed-point Decimals), and universal tracking barcodes (UUIDs).

**PostgreSQL** (often called Postgres) is the world's most advanced open-source object-relational database system, renowned for enterprise reliability, multi-version concurrency control (MVCC), and rich data type extensibility.

---

## 2. PostgreSQL Under-the-Hood: Client-Server & MVCC

Unlike SQLite (which lives inside your Python process as a library), PostgreSQL runs as an independent daemon service (typically on port 5432).

```
+-------------------------------------------------------------+
|                 Python Application (psycopg / psycopg2)     |
+-------------------------------------------------------------+
                              | TCP/IP Network Connection (Port 5432)
                              | Authentication (md5 / scram-sha-256)
                              v
+-------------------------------------------------------------+
|                 PostgreSQL Server (Backend Process)         |
|  +-------------------------------------------------------+  |
|  | Multi-Version Concurrency Control (MVCC) Engine       |  |
|  | - Readers never block writers                         |  |
|  | - Writers never block readers                         |  |
|  +-------------------------------------------------------+  |
|  +-------------------------------------------------------+  |
|  | Shared Buffers | WAL Writer | Background Writer       |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

### Multi-Version Concurrency Control (MVCC)
In traditional databases, if a reporting query is scanning 1,000,000 rows, it locks the table, preventing other users from inserting records.
In PostgreSQL:
- When a row is updated or deleted, PostgreSQL does **not** overwrite the old data in-place.
- Instead, it creates a new version of the row with transaction timestamps (`xmin` and `xmax`).
- Reader queries see a consistent snapshot of the database from the moment their transaction began.
- **Result**: Readers never block writers, and writers never block readers!

---

## 3. Data Type Mapping: Python $\longleftrightarrow$ PostgreSQL

PostgreSQL provides first-class support for advanced types that map seamlessly to Python native objects:

| PostgreSQL Type | Python Type | Use Case & Advantage |
| :--- | :--- | :--- |
| `VARCHAR` / `TEXT` | `str` | Textual data of arbitrary length |
| `INTEGER` / `BIGINT` | `int` | Identifiers, counters, timestamps |
| `NUMERIC` / `DECIMAL` | `decimal.Decimal` | **Financial and medical measurements** (zero floating-point rounding errors!) |
| `BOOLEAN` | `bool` | True / False flags |
| `TIMESTAMP WITH TIME ZONE` | `datetime.datetime` (tz-aware) | UTC audit trails preventing Daylight Saving errors |
| `UUID` | `uuid.UUID` | Universally Unique Identifiers across microservices |
| `JSON` / `JSONB` | `dict` / `list` | Semi-structured data; `JSONB` is indexed via GIN indexes |
| `NULL` | `None` | Represents absence of a value |

---

## 4. Handling SQL `NULL` and Three-Valued Logic

In SQL, `NULL` does not mean zero or empty string; it means **Unknown**.
This leads to SQL **Three-Valued Logic**: `TRUE`, `FALSE`, or `UNKNOWN`.

```sql
-- DANGEROUS / ALWAYS FAILS:
SELECT * FROM patients WHERE discharge_date = NULL; -- Returns 0 rows, always!

-- CORRECT:
SELECT * FROM patients WHERE discharge_date IS NULL;
```

### The `COALESCE` Function
`COALESCE(val1, val2, ...)` returns the first non-null argument. It is the SQL equivalent of Python's `val or default`:
```sql
-- If discharge_date is NULL, display 'STILL ADMITTED'
SELECT patient_name, COALESCE(discharge_date, 'STILL ADMITTED') FROM admissions;
```

---

## 5. Comprehensive Runnable Code Examples

*(Note: To allow running and testing immediately anywhere without requiring a running PostgreSQL server, these examples demonstrate PostgreSQL client configuration, type serialization, and use an engine-agnostic adapter pattern.)*

### Example 1: PostgreSQL DSN & Configuration Builder

```python
from urllib.parse import urlparse
from typing import Dict, Any

class PostgresConfig:
    def __init__(self, host: str = "localhost", port: int = 5432, dbname: str = "hospital",
                 user: str = "postgres", password: str = "", sslmode: str = "prefer"):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.sslmode = sslmode

    def to_dsn(self) -> str:
        """Generate connection URI DSN string."""
        auth = f"{self.user}:{self.password}@" if self.password else f"{self.user}@"
        return f"postgresql://{auth}{self.host}:{self.port}/{self.dbname}?sslmode={self.sslmode}"

    def to_params(self) -> Dict[str, Any]:
        """Generate key-value dictionary for psycopg.connect(**params)."""
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "sslmode": self.sslmode
        }

if __name__ == "__main__":
    cfg = PostgresConfig(host="db.hospital.internal", dbname="clinical_dw", user="svc_ehr", password="secret_token")
    print("DSN Connection String:")
    print(" ", cfg.to_dsn())
```
**Expected Output:**
```
DSN Connection String:
  postgresql://svc_ehr:secret_token@db.hospital.internal:5432/clinical_dw?sslmode=prefer
```

---

### Example 2: Rich Type Serialization (JSONB & Decimal)

```python
import json
from decimal import Decimal
import sqlite3

def demo_rich_types():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Table simulating PostgreSQL JSONB and NUMERIC types
    cursor.execute("""
    CREATE TABLE lab_specimens (
        specimen_id TEXT PRIMARY KEY,
        billing_amount TEXT, -- Stored as string to preserve exact Decimal precision
        metadata_json TEXT   -- Stored as JSON string
    );
    """)

    # Python rich types
    cost = Decimal("145.85")
    metadata = {
        "lab_unit": "Hematology-4",
        "sample_type": "Whole Blood",
        "temperature_celsius": 4.2,
        "flags": ["URGENT", "STAT"]
    }

    cursor.execute(
        "INSERT INTO lab_specimens VALUES (?, ?, ?);",
        ("SPEC-9092", str(cost), json.dumps(metadata))
    )
    conn.commit()

    # Retrieve and deserialize back to rich Python types
    cursor.execute("SELECT specimen_id, billing_amount, metadata_json FROM lab_specimens WHERE specimen_id = ?;", ("SPEC-9092",))
    row = cursor.fetchone()
    
    spec_id = row[0]
    retrieved_cost = Decimal(row[1]) # Restored to Decimal without float drift!
    retrieved_meta = json.loads(row[2]) # Restored to Python dict

    print(f"Specimen: {spec_id}")
    print(f"Exact Cost: ${retrieved_cost} (Type: {type(retrieved_cost).__name__})")
    print(f"Flags from JSON: {retrieved_meta['flags']}")
    conn.close()

if __name__ == "__main__":
    demo_rich_types()
```
**Expected Output:**
```
Specimen: SPEC-9092
Exact Cost: $145.85 (Type: Decimal)
Flags from JSON: ['URGENT', 'STAT']
```

---

### Example 3: NULL-Safe Result Extraction with `COALESCE`

```python
import sqlite3

def demo_null_handling():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE patient_discharges (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        discharge_notes TEXT -- Nullable
    );
    """)

    cursor.executemany("INSERT INTO patient_discharges VALUES (?, ?, ?);", [
        (1, "Alice Morgan", "Discharged in good health. Prescription filled."),
        (2, "Bob Vance", None) # Still in hospital
    ])
    conn.commit()

    # Using SQL COALESCE to provide fallback for NULL
    cursor.execute("""
    SELECT name, COALESCE(discharge_notes, '[PATIENT CURRENTLY ADMITTED]') AS notes
    FROM patient_discharges
    ORDER BY id ASC;
    """)

    for name, notes in cursor.fetchall():
        print(f"Patient: {name:<15} | Status: {notes}")

    conn.close()

if __name__ == "__main__":
    demo_null_handling()
```
**Expected Output:**
```
Patient: Alice Morgan   | Status: Discharged in good health. Prescription filled.
Patient: Bob Vance      | Status: [PATIENT CURRENTLY ADMITTED]
```

---

### Example 4: Resilient Database Adapter (Local / Postgres Compatible)

```python
import sqlite3
from typing import Dict, Any, List, Optional
from contextlib import contextmanager

class ResilientDatabaseAdapter:
    """
    Adapter that executes queries transparently across DB-API 2.0 compliant connections,
    providing row dictionary mappings and safe transaction commits.
    """
    def __init__(self, conn: Any):
        self.conn = conn

    @contextmanager
    def cursor(self):
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    def query_dict(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.cursor() as cur:
            cur.execute(sql, params)
            columns = [desc[0] for desc in cur.description] if cur.description else []
            return [dict(zip(columns, row)) for row in cur.fetchall()]

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    adapter = ResilientDatabaseAdapter(conn)

    with adapter.cursor() as cur:
        cur.execute("CREATE TABLE clinics (id INT, name TEXT);")
        cur.execute("INSERT INTO clinics VALUES (1, 'Downtown Urgent Care');")

    results = adapter.query_dict("SELECT * FROM clinics;")
    print("Dictionary Results:", results)
    conn.close()
```
**Expected Output:**
```
Dictionary Results: [{'id': 1, 'name': 'Downtown Urgent Care'}]
```

---

## 6. Architecture & Implementation Comparison

| Feature | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| **Network Protocol** | None (in-process library call) | TCP/IP Socket (Port 5432, TLS optional) |
| **Semi-Structured Support** | JSON text column via `json_extract()` | Binary `JSONB` with GIN indexed key searches |
| **Numeric Precision** | 64-bit IEEE 754 Floating point | Arbitrary-precision `NUMERIC(precision, scale)` |
| **Concurrency Scale** | 1 writer at a time | Thousands of concurrent writers via MVCC |
| **Python Driver** | Built-in `sqlite3` | `psycopg` (v3) / `psycopg2` |

---

## 7. Real-World Industry Use Cases

### 1. Healthcare: Radiology Imaging Metadata (DICOM)
A CT scan produces hundreds of image slices with variable scanner attributes (gantry tilt, radiation dose, pixel spacing, contrast agent volume). Storing every possible tag in a fixed relational table would require hundreds of nullable columns. PostgreSQL `JSONB` stores the study header as a structured document, allowing radiologists to search for specific scan parameters at index speed.

### 2. eCommerce: Dynamic Product Attributes
An online store sells books, shoes, laptops, and groceries. Each item has radically different attributes (shoes have size/color, laptops have CPU/RAM, books have ISBN/pages). Using PostgreSQL `JSONB` with GIN indexing avoids table-per-category schema explosion.

### 3. Banking: High-Precision Multi-Currency Ledgers
In currency exchange, transactions like €10,000 to ¥1,623,450.28 must be exact to 4 decimal places. Using floating-point arithmetic introduces microscopic rounding errors (e.g. `0.1 + 0.2 = 0.30000000000000004`). PostgreSQL `NUMERIC` paired with Python's `Decimal` guarantees 100% mathematical precision.

---

## 8. Best Practices, Anti-Patterns, and Top 3 Mistakes

### Best Practices:
1. **Always Use `Decimal` for Money and Clinical Dosages**: Never use `float` for financial balances, medication milligrams, or radiation doses.
2. **Use `JSONB` Instead of `JSON` in PostgreSQL**: `JSONB` parses JSON into a decomposed binary format upon storage, enabling fast lookups and indexing.
3. **Always Set `sslmode=require` or `verify-full` in Production**: Protect patient data and database credentials in transit over cloud networks.

### Top 3 Mistakes Developers Make:

#### Mistake 1: Evaluating `NULL` with Equality Operator (`=`)
```sql
-- BROKEN: In SQL, NULL = NULL evaluates to UNKNOWN (falsy)!
SELECT * FROM patient_records WHERE primary_physician = NULL;

-- CORRECT:
SELECT * FROM patient_records WHERE primary_physician IS NULL;
```

#### Mistake 2: Storing Currency as `FLOAT`
```python
# DANGEROUS: Floating-point drift!
balance = 100.10
balance += 0.20 # balance becomes 100.30000000000001!

# CORRECT:
from decimal import Decimal
balance = Decimal("100.10") + Decimal("0.20") # Decimal('100.30')
```

#### Mistake 3: Hardcoding Database Credentials in Source Code
Never write passwords in application source code.
- **Fix**: Load credentials from environment variables or a configuration object:
```python
import os
db_url = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/app")
```
