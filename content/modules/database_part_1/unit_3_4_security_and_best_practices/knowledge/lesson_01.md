# Unit 3.4: Database Security, Transactions, and Best Practices

---

## 1. Conceptual Foundation: The Drive-Through Microphone vs. The Sealed Envelope

Imagine a drive-through teller at a high-security bank:

- **The Vulnerable System (String Interpolation / Injection)**: You speak into an open microphone: *"Please deposit $100 into account of John Doe."* But a malicious person shouts: *"John Doe; ALSO TRANSFER ALL VAULT CASH TO ROBBER; --"* If the teller blindly obeys every raw sound coming through the microphone as executable commands, the bank is emptied.
- **The Secure System (Parameterized Protocol / Sealed Envelope)**: The teller has a pre-printed form with rigid slots:
  - Slot 1: Operation (`DEPOSIT`)
  - Slot 2: Amount ($100)
  - Slot 3: Account Holder (`John Doe`)
  If the customer writes `"John Doe; DROP TABLE users;"` in Slot 3, the database treats that entire string **strictly as a literal person's name**. It never executes it as code!

This fundamental separation between **Code (SQL Grammar)** and **Data (Parameters)** is the cornerstone of database security.

---

## 2. The Anatomy of SQL Injection

SQL injection occurs when untrusted user input is concatenated into a SQL statement string before the database parser tokenizes it.

```
Untrusted Input:   ' OR '1'='1' --

Vulnerable Query:  f"SELECT * FROM users WHERE username = '{user_input}' AND pass = '{pass_input}';"
Compiled SQL:      SELECT * FROM users WHERE username = '' OR '1'='1' --' AND pass = '...';
                                                         ^------------^    ^
                                                       Always TRUE!   Comments out password check!
```

Because the database receives the concatenated string as a single text block, the user's quotes break out of the string literal and inject new syntax into the Abstract Syntax Tree (AST).

### The Mathematical Fix: Prepared Statements & Query Parameters
When you use parameterized queries:
1. The database receives the template: `SELECT * FROM users WHERE username = ? AND pass = ?;`
2. The database parses and compiles the query plan **first**.
3. The parameter values are transmitted separately over the wire as raw typed data bytes.
4. **Result**: Even if the input contains quotes, semicolons, or SQL keywords, it is impossible for them to be parsed as SQL syntax.

---

## 3. Safe Dynamic SQL: Parameters vs. Identifiers

There is one critical limitation of parameterized queries:
> **SQL grammar permits parameter placeholders (`?` or `%s`) ONLY for literal values (strings, numbers, dates). You CANNOT use placeholders for SQL identifiers (table names, column names, `ASC`/`DESC`).**

```python
# INVALID SQL SYNTAX - Database engine will throw a syntax error:
cursor.execute("SELECT * FROM ? WHERE ? = ?;", ("patients", "mrn", "MRN-101")) # SYNTAX ERROR!
```

### The Solution: Identifier Whitelisting
To dynamically sort by a column or query a dynamic table safely:
1. Verify the identifier against an explicit **Whitelist**.
2. Reject any input not in the whitelist.

```python
ALLOWED_COLUMNS = {"patient_id", "full_name", "birth_date"}

def search(sort_col: str):
    if sort_col not in ALLOWED_COLUMNS:
        raise ValueError(f"Invalid sort column: {sort_col}")
    # Safe because sort_col is strictly from the verified whitelist
    return f"SELECT * FROM patients ORDER BY {sort_col} ASC;"
```

---

## 4. Advanced Transaction Control: ACID & Savepoints

### The ACID Guarantees:
- **Atomicity**: All statements in a transaction succeed together, or all are rolled back.
- **Consistency**: The database moves from one valid state to another without violating constraints.
- **Isolation**: Concurrent transactions execute without interfering with one another.
- **Durability**: Once committed, changes survive server crashes or power failures.

### Partial Rollbacks with `SAVEPOINT`
In complex multi-step business operations, if step 3 of 5 fails, you may not want to abort steps 1 and 2. A **Savepoint** acts as a checkpoint within a transaction:

```
BEGIN TRANSACTION;
  INSERT INTO patient ... (Step 1)
  SAVEPOINT billing_checkpoint;
    INSERT INTO billing_charge ... (Step 2 - Fails!)
  ROLLBACK TO billing_checkpoint; -- Rolls back ONLY Step 2! Step 1 preserved!
  INSERT INTO fallback_audit ... (Step 2b)
COMMIT;
```

---

## 5. Comprehensive Runnable Code Examples

### Example 1: Demonstrating SQL Injection vs. Parameterized Defense

```python
import sqlite3

def demo_sql_injection():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INT, username TEXT, is_admin INT);")
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?);", [
        (1, "alice", 0),
        (2, "bob", 0),
        (3, "superadmin", 1)
    ])
    conn.commit()

    malicious_input = "' OR '1'='1"

    # 1. VULNERABLE APPROACH (f-string string concatenation)
    vuln_query = f"SELECT username, is_admin FROM users WHERE username = '{malicious_input}';"
    cursor.execute(vuln_query)
    vuln_rows = cursor.fetchall()
    print("[VULNERABLE QUERY] Rows returned (ALL USERS LEAKED!):")
    for row in vuln_rows:
        print("  -", row)

    # 2. SECURE APPROACH (Parameterized query)
    sec_query = "SELECT username, is_admin FROM users WHERE username = ?;"
    cursor.execute(sec_query, (malicious_input,))
    sec_rows = cursor.fetchall()
    print("[SECURE QUERY] Rows returned (SAFELY EMPTY):", sec_rows)

    conn.close()

if __name__ == "__main__":
    demo_sql_injection()
```
**Expected Output:**
```
[VULNERABLE QUERY] Rows returned (ALL USERS LEAKED!):
  - ('alice', 0)
  - ('bob', 0)
  - ('superadmin', 1)
[SECURE QUERY] Rows returned (SAFELY EMPTY): []
```

---

### Example 2: Dynamic Column Sorting via Safe Whitelisting

```python
import sqlite3
from typing import List, Tuple

ALLOWED_SORT_COLUMNS = {
    "name": "full_name",
    "dob": "birth_date",
    "id": "patient_id"
}

def query_patients_safely(conn: sqlite3.Connection, sort_by_alias: str) -> List[Tuple]:
    # Validate against strict whitelist
    if sort_by_alias not in ALLOWED_SORT_COLUMNS:
        raise ValueError(f"Disallowed sort parameter: {sort_by_alias}")
    
    actual_col = ALLOWED_SORT_COLUMNS[sort_by_alias]
    sql = f"SELECT patient_id, full_name, birth_date FROM patients ORDER BY {actual_col} ASC;"
    return conn.execute(sql).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE patients (patient_id INT, full_name TEXT, birth_date TEXT);")
    conn.executemany("INSERT INTO patients VALUES (?, ?, ?);", [
        (102, "Charlie", "1990-01-01"),
        (101, "Alice", "1985-05-12"),
        (103, "Bob", "1995-10-30")
    ])
    conn.commit()

    print("Sorted by Name:", query_patients_safely(conn, "name"))
    
    try:
        query_patients_safely(conn, "id; DROP TABLE patients; --")
    except ValueError as e:
        print("Injection blocked by whitelist:", e)

    conn.close()
```
**Expected Output:**
```
Sorted by Name: [(101, 'Alice', '1985-05-12'), (103, 'Bob', '1995-10-30'), (102, 'Charlie', '1990-01-01')]
Injection blocked by whitelist: Disallowed sort parameter: id; DROP TABLE patients; --
```

---

### Example 3: Nested Transaction Control with Savepoints

```python
import sqlite3

def demo_savepoint_rollback():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE patient_ledger (entry_id INT PRIMARY KEY, description TEXT, amount INT);")
    conn.commit()

    # Outer Transaction
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("INSERT INTO patient_ledger VALUES (1, 'Bed Charge', 500);")

    # Establish Savepoint
    cursor.execute("SAVEPOINT optional_perks;")
    try:
        # Step that fails uniqueness constraint
        cursor.execute("INSERT INTO patient_ledger VALUES (2, 'Cafeteria Meals', 50);")
        cursor.execute("INSERT INTO patient_ledger VALUES (2, 'Duplicate Cafeteria', 50);") # Duplicate primary key!
    except sqlite3.IntegrityError:
        print("[Notice] Optional perks failed. Rolling back to savepoint...")
        cursor.execute("ROLLBACK TO SAVEPOINT optional_perks;")

    # Commit outer transaction
    cursor.execute("RELEASE SAVEPOINT optional_perks;")
    conn.commit()

    # Verify Bed Charge was preserved!
    cursor.execute("SELECT * FROM patient_ledger;")
    rows = cursor.fetchall()
    print("Final Ledger Rows:")
    for r in rows:
        print(" ", r)

    conn.close()

if __name__ == "__main__":
    demo_savepoint_rollback()
```
**Expected Output:**
```
[Notice] Optional perks failed. Rolling back to savepoint...
Final Ledger Rows:
  (1, 'Bed Charge', 500)
```

---

### Example 4: Resilient Query Retry with Exponential Backoff

```python
import time
import sqlite3
from typing import Callable, Any

def execute_with_retry(operation: Callable[[], Any], max_retries: int = 3, base_delay: float = 0.05) -> Any:
    """Executes a database operation with exponential backoff on transient locking errors."""
    for attempt in range(max_retries):
        try:
            return operation()
        except sqlite3.OperationalError as err:
            if "locked" in str(err) and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"[Retry {attempt + 1}] Database busy. Sleeping {delay:.3f}s...")
                time.sleep(delay)
                continue
            raise

if __name__ == "__main__":
    attempts = 0
    def flaky_db_call():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise sqlite3.OperationalError("database is locked")
        return "SUCCESSFUL_WRITE"

    result = execute_with_retry(flaky_db_call)
    print("Result:", result)
```
**Expected Output:**
```
[Retry 1] Database busy. Sleeping 0.050s...
[Retry 2] Database busy. Sleeping 0.100s...
Result: SUCCESSFUL_WRITE
```

---

## 6. Architecture & Implementation Comparison

| Defense Mechanism | Protection Level | Performance | Maintenance Overhead |
| :--- | :--- | :--- | :--- |
| **Parameterized Queries (`?`)** | **100% Immune** against data injection | Ultra-Fast (Reuses compiled query plans) | Standard idiomatic Python |
| **Identifier Whitelisting** | **100% Immune** for dynamic columns | Zero overhead (Dict lookup) | Minimal |
| **Manual Regex / Escaping** | **Flawed & Unsafe** (Attackers bypass filters) | Slow | High (Continuous security vulnerabilities) |

---

## 7. Real-World Industry Use Cases

### 1. Healthcare: HIPAA E-Prescribing Audit Trail
Under HIPAA regulations, altering or tampering with a narcotic prescription audit log carries severe criminal penalties. All electronic prescriptions use strict parameterization with SHA-256 hash chaining. Even if an insider tries to inject SQL through a patient allergies text box, the input is trapped as string data without modifying database permissions.

### 2. eCommerce: Black Friday Coupon Race Conditions
During flash sales, customers attempt to apply the same single-use discount coupon simultaneously from multiple browser tabs. A transaction with `SERIALIZABLE` isolation or explicit row-level locking (`SELECT ... FOR UPDATE`) prevents concurrent double-redemption.

### 3. Banking: Suspicious Activity Account Freeze
When an anti-fraud machine learning model flags a card transaction, a multi-stage transaction freezes the account, logs the telemetry, and creates an audit event. Using savepoints ensures that if an SMS alert notification fails to insert, the vital account freeze is still safely committed.

---

## 8. Best Practices, Anti-Patterns, and Top 3 Mistakes

### Best Practices:
1. **Never Ever Use f-strings for SQL Queries**: Always pass query parameters as a tuple in `cursor.execute(sql, (param,))`.
2. **Always Use `contextlib.closing` or `with` Statements**: Guarantee that cursor and connection handles are returned to the pool even during unhandled exceptions.
3. **Audit Dynamic Identifiers**: Ensure any variable interpolated into SQL is checked against an explicit set of permissible column/table names.

### Top 3 Mistakes Developers Make:

#### Mistake 1: String Formatting with Quotes
```python
# WRONG: Still completely vulnerable to injection!
query = "SELECT * FROM users WHERE email = '%s';" % user_input

# CORRECT:
query = "SELECT * FROM users WHERE email = ?;"
cursor.execute(query, (user_input,))
```

#### Mistake 2: Single-Item Tuple Comma Omission
```python
# MISTAKE: ('Alice') in Python is just the string 'Alice', NOT a tuple!
cursor.execute("SELECT * FROM users WHERE name = ?;", ("Alice")) # Error or char-by-char binding!

# CORRECT: Always include the trailing comma for single-item tuples:
cursor.execute("SELECT * FROM users WHERE name = ?;", ("Alice",))
```

#### Mistake 3: Leaking Database Connections in Exception Handlers
```python
# DANGEROUS: If execute fails, conn.close() is never reached!
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT risky_operation();")
conn.close()

# CORRECT:
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT risky_operation();")
```
