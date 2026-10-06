# Unit 3.1: Database Fundamentals and Relational Architecture

---

## 1. Conceptual Foundation: The Hospital Records Department vs. The Loose Paper Pile

Imagine managing patient medical histories for a 500-bed hospital:

- **The Loose Paper Pile (Unstructured / Flat Files)**: Every doctor writes notes on loose sheets of paper and throws them into a giant cardboard box. Finding "Jane Doe's blood pressure from last Tuesday" requires a clerk to pick up every single piece of paper, read it, and put it back until they find the match ($O(N)$ full scan). If two nurses want to write on Jane's chart at the same time, they fight over the paper or create duplicate conflicting notes.
- **The Modern Records Archive (Relational Database - RDBMS)**:
  - **Tables**: Dedicated filing drawers for specific entities (`patients`, `appointments`, `prescriptions`).
  - **Primary Keys**: Every patient has a permanent, unique National Health ID (`patient_id`). No two patients share an ID.
  - **Foreign Keys**: Every prescription links directly to an existing patient ID. If a clerk tries to file a prescription for a non-existent patient, the system rejects it immediately (**Referential Integrity**).
  - **Indexes**: An alphabetized index card drawer sorted by patient surname. Instead of reading 100,000 patient charts, the clerk checks the index card drawer, jumps straight to drawer #4, folder #12 in seconds ($O(\log N)$ lookup).

A **Relational Database Management System (RDBMS)** guarantees that data is **structured**, **consistent**, **searchable**, and **protected against corruption**.

---

## 2. Under-the-Hood: How a Database Stores and Finds Data

A database is not just a file; it is an operating system for data.

```
+-------------------------------------------------------------+
|                 Application (Python DB Client)              |
+-------------------------------------------------------------+
                              | SQL Query: SELECT * FROM ...
                              v
+-------------------------------------------------------------+
|                     Query Optimizer & Parser                |
+-------------------------------------------------------------+
                              | Query Plan (Index Scan)
                              v
+-------------------------------------------------------------+
|              Buffer Pool / Cache Manager (RAM)              |
|              [ Page 1 ]   [ Page 42 ]   [ Page 88 ]         |
+-------------------------------------------------------------+
                              | Reads/Flushes (8KB / 16KB Pages)
                              v
+-------------------------------------------------------------+
|                Storage Engine & Disk Files                  |
|    +-----------------------+     +---------------------+    |
|    | Tablespace (.db / .ibd)|     | Write-Ahead Log(WAL)|    |
|    +-----------------------+     +---------------------+    |
+-------------------------------------------------------------+
```

### 1. Disk Pages & The Buffer Pool
Databases do not read individual rows from the hard disk. Disk reads are organized into fixed-size chunks called **Pages** (typically 4KB in SQLite, 8KB in PostgreSQL, 16KB in MySQL).
- When a query runs, the database loads the entire page containing that row into RAM (**Buffer Pool**).
- Subsequent queries reading adjacent rows on the same page hit RAM with microsecond latency.

### 2. The B-Tree Index: From $O(N)$ to $O(\log N)$
Without an index, finding a patient requires a **Full Table Scan**: scanning every page from start to finish.
A database **Index** is a self-balancing tree structure (typically a **B+ Tree**):

```
                       [ Root Node: 50 ]
                       /               \
            [ Keys < 50 ]             [ Keys >= 50 ]
            /           \             /            \
        [ 10, 25 ]   [ 35, 48 ]   [ 52, 70 ]    [ 85, 99 ]  <-- Leaf Nodes (Pointers to Disk Pages)
```
- In a table with 1,000,000 rows, a full table scan checks 1,000,000 entries.
- A B-Tree index locates the exact row in roughly $\log_2(1,000,000) \approx 20$ page hops!

> **The Trade-Off**: Indexes speed up `SELECT` queries dramatically, but every `INSERT`, `UPDATE`, and `DELETE` must also update the index tree, adding write overhead.

### 3. Write-Ahead Logging (WAL) & Durability
To survive power outages and crashes without losing committed transactions:
1. When a row is inserted, the database writes the change sequentially to an append-only **Write-Ahead Log (WAL)** on disk.
2. Only after the WAL write succeeds does the database confirm the transaction as committed.
3. If the server crashes, the database replays the WAL on restart to restore consistent state.

---

## 3. Core SQL Architecture: DDL & DML

SQL statements fall into two primary categories:

### 1. Data Definition Language (DDL)
Defines the schema structure, constraints, and tables:
- `CREATE TABLE`: Allocates table definition.
- `PRIMARY KEY`: Unique identifier constraint, automatically indexed.
- `FOREIGN KEY ... REFERENCES`: Enforces relational integrity between tables.
- `NOT NULL` & `CHECK`: Enforces data validity at the storage layer.

### 2. Data Manipulation Language (DML)
Interacts with the actual records:
- `INSERT INTO`: Adds new rows.
- `SELECT ... WHERE`: Reads and filters records.
- `UPDATE ... SET`: Modifies existing rows.
- `DELETE FROM`: Removes rows.

---

## 4. Comprehensive Runnable Code Examples

Python includes the `sqlite3` module in its standard library. `sqlite3` provides a full, standard DB-API 2.0 compliant relational database engine that runs locally in-memory or in a file without requiring server installation.

### Example 1: Creating Relational Tables with Primary & Foreign Keys

```python
import sqlite3

def create_hospital_schema():
    conn = sqlite3.connect(":memory:") # In-memory database
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") # Enforce relational constraints

    # 1. Patients Table
    cursor.execute("""
    CREATE TABLE patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mrn TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        blood_type TEXT CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
    );
    """)

    # 2. Vitals Table with Foreign Key
    cursor.execute("""
    CREATE TABLE patient_vitals (
        vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        heart_rate INTEGER NOT NULL,
        systolic_bp INTEGER NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    );
    """)

    print("Hospital schema created successfully with foreign key constraints!")
    return conn

if __name__ == "__main__":
    conn = create_hospital_schema()
    conn.close()
```
**Expected Output:**
```
Hospital schema created successfully with foreign key constraints!
```

---

### Example 2: Inserting and Querying Relational Data

```python
import sqlite3

def populate_and_query():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE patients (
        patient_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        department TEXT NOT NULL
    );
    """)

    # Batch Insert Patients
    patients = [
        (101, "Alice Morgan", "Cardiology"),
        (102, "Bob Vance", "Neurology"),
        (103, "Charlie Hayes", "Cardiology"),
        (104, "Diana Prince", "Orthopedics")
    ]
    cursor.executemany("INSERT INTO patients VALUES (?, ?, ?);", patients)
    conn.commit()

    # Query filtered by department
    cursor.execute("SELECT patient_id, full_name FROM patients WHERE department = ? ORDER BY full_name ASC;", ("Cardiology",))
    rows = cursor.fetchall()

    print("Cardiology Patients:")
    for pid, name in rows:
        print(f" - ID: {pid} | Name: {name}")

    conn.close()

if __name__ == "__main__":
    populate_and_query()
```
**Expected Output:**
```
Cardiology Patients:
 - ID: 101 | Name: Alice Morgan
 - ID: 103 | Name: Charlie Hayes
```

---

### Example 3: Verifying Referential Integrity (Foreign Key Enforcement)

```python
import sqlite3

def test_foreign_key_protection():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("CREATE TABLE wards (ward_id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
    cursor.execute("""
    CREATE TABLE beds (
        bed_id INTEGER PRIMARY KEY,
        ward_id INTEGER NOT NULL,
        FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
    );
    """)

    cursor.execute("INSERT INTO wards VALUES (1, 'Intensive Care Unit');")
    cursor.execute("INSERT INTO beds VALUES (101, 1);") # Valid: ward 1 exists
    conn.commit()

    try:
        # Invalid: ward 99 does NOT exist
        cursor.execute("INSERT INTO beds VALUES (102, 99);")
        conn.commit()
    except sqlite3.IntegrityError as err:
        print(f"Protection Succeeded! Database rejected invalid reference: {err}")

    conn.close()

if __name__ == "__main__":
    test_foreign_key_protection()
```
**Expected Output:**
```
Protection Succeeded! Database rejected invalid reference: FOREIGN KEY constraint failed
```

---

### Example 4: Index Performance and Query Plan Verification

```python
import sqlite3

def verify_query_plan():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE prescriptions (id INTEGER PRIMARY KEY, drug_code TEXT, dosage_mg INT);")

    # Populate 1,000 rows
    records = [(f"DRUG-{i:04d}", 50 + (i % 200)) for i in range(1000)]
    cursor.executemany("INSERT INTO prescriptions(drug_code, dosage_mg) VALUES (?, ?);", records)
    conn.commit()

    # 1. Explain Query without index
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM prescriptions WHERE drug_code = 'DRUG-0450';")
    plan_without_index = cursor.fetchone()
    print("Without Index:", plan_without_index[3]) # SCAN prescriptions

    # 2. Add B-Tree Index
    cursor.execute("CREATE INDEX idx_prescriptions_drug_code ON prescriptions(drug_code);")
    conn.commit()

    # 3. Explain Query with index
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM prescriptions WHERE drug_code = 'DRUG-0450';")
    plan_with_index = cursor.fetchone()
    print("With B-Tree Index:", plan_with_index[3]) # SEARCH using index

    conn.close()

if __name__ == "__main__":
    verify_query_plan()
```
**Expected Output:**
```
Without Index: SCAN prescriptions
With B-Tree Index: SEARCH prescriptions USING INDEX idx_prescriptions_drug_code (drug_code=?)
```

---

## 5. RDBMS Engine Comparison: PostgreSQL vs. SQLite vs. MySQL

| Feature | SQLite | PostgreSQL | MySQL |
| :--- | :--- | :--- | :--- |
| **Architecture** | Serverless / Embedded in-process | Client-Server multi-process | Client-Server multi-threaded |
| **Concurrency Model**| Single-writer database file lock | Multi-Version Concurrency Control (MVCC) | MVCC with InnoDB row locks |
| **Primary Use Case** | Mobile apps, local CLI tools, automated testing | High-concurrency enterprise web applications, complex analytics | High-read web services, e-commerce stores |
| **Data Types** | Dynamic typeless (5 storage classes) | Strict, rich (JSONB, Arrays, UUID, GIS) | Strict static types, JSON |
| **Scale Limit** | Single machine, small write volumes | Terabytes across clustered replicas | Terabytes across read replicas |

---

## 6. Real-World Industry Use Cases

### 1. Healthcare: Master Patient Index (MPI)
A multi-facility hospital network maintains records for 2,000,000 patients. To ensure that medical records from clinics, emergency rooms, and surgical suites map to the same individual without collision, the MPI uses a compound relational model with primary keys, unique national identifiers, and foreign-key enforced clinical encounter tables.

### 2. Pharmacy: Closed-Loop Drug Dispensing
When a physician writes a prescription, the hospital pharmacy system must enforce strict referential validity: the prescription must link to a verified clinician ID, an authorized patient ID, and a valid formulary drug code. If any of those foreign key relations are missing, the prescription cannot be dispensed.

### 3. Banking: Double-Entry Ledger System
In banking accounting, every financial movement requires matching debit and credit rows. Relational constraints guarantee that an account balance update cannot occur unless associated transaction line items exist, ensuring the fundamental accounting equation is never violated.

---

## 7. Best Practices, Anti-Patterns, and Top 3 Mistakes

### Best Practices:
1. **Always Define Explicit Constraints**: Enforce `NOT NULL`, `UNIQUE`, and `CHECK` constraints at the schema level rather than relying solely on Python application validation.
2. **Index Foreign Key Columns**: Databases automatically index Primary Keys, but foreign key columns (e.g., `patient_id` in `vitals`) are **not** indexed by default. Always create an index on foreign key columns to avoid full table scans during `JOIN` queries.
3. **Use Meaningful Data Types**: Store dates as `TIMESTAMP`/`DATE`, numbers as `INTEGER`/`DECIMAL`, and text as `VARCHAR`/`TEXT`.

### Top 3 Mistakes Developers Make:

#### Mistake 1: Relying on `SELECT *` in Production
```sql
-- DANGEROUS: Wastes network bandwidth, breaks if columns change, prevents index-only scans
SELECT * FROM patient_vitals WHERE patient_id = 101;

-- CORRECT: Select only the required columns
SELECT heart_rate, systolic_bp, recorded_at FROM patient_vitals WHERE patient_id = 101;
```

#### Mistake 2: Missing Foreign Key Enforcement in SQLite
By default in SQLite, foreign key constraint checking is **disabled** for backward compatibility!
- **Fix**: Always run `PRAGMA foreign_keys = ON;` immediately after connecting:
```python
conn = sqlite3.connect("hospital.db")
conn.execute("PRAGMA foreign_keys = ON;")
```

#### Mistake 3: Over-Indexing Every Single Column
Adding an index to every column slows down all `INSERT` and `UPDATE` operations and bloats disk storage.
- **Fix**: Index only columns frequently used in `WHERE`, `JOIN ... ON`, and `ORDER BY` clauses with high query selectivity.
