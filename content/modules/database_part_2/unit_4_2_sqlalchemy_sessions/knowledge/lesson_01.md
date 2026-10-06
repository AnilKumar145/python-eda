# Lesson 4.2: SQLAlchemy Session Lifecycle, Unit of Work, and Modern Query Execution

---

## 1. Conceptual Foundation

In database programming, issuing individual SQL statements immediately whenever an object attribute changes creates severe overhead and concurrency hazards. If updating a patient's chart requires modifying their address, insurance policy, and primary care provider, sending three separate network updates leaves the database in an inconsistent state if the third update fails.

SQLAlchemy solves this through the **Unit of Work** design pattern, encapsulated by the **`Session`**.

The `Session` acts as an intelligent staging environment:
1. It buffers your Python object modifications in memory.
2. It tracks which objects are new, modified, or marked for deletion.
3. When you call `session.commit()`, the session calculates the minimum, optimized set of SQL DML statements (`INSERT`, `UPDATE`, `DELETE`) and flushes them to the database inside a single atomic transaction.

```
+------------------------------------------------------------------------+
|                      Python Application Code                           |
|       surgeon = Surgeon(name="Dr. Meredith Grey")                      |
|       session.add(surgeon)       # Staged in Session                   |
|       surgery.status = "COMPLETED" # Attribute change tracked          |
+-----------------------------------+------------------------------------+
                                    | session.commit()
                                    v
+------------------------------------------------------------------------+
|                          SQLAlchemy Session                            |
|    - Identity Map: Ensures 1 in-memory instance per database row       |
|    - Dirty Tracking: Detects mutated fields (surgery.status)          |
|    - Flush: Orders INSERTs before UPDATEs, avoiding FK conflicts       |
+-----------------------------------+------------------------------------+
                                    | Emits SQL over DB-API
                                    v
+------------------------------------------------------------------------+
|               BEGIN TRANSACTION;                                       |
|               INSERT INTO surgeons (name) VALUES ('Dr. Grey');         |
|               UPDATE surgeries SET status = 'COMPLETED' WHERE id = 12; |
|               COMMIT;                                                  |
+------------------------------------------------------------------------+
```

---

## 2. Architecture & Internal Mechanics

### The Four States of an Entity Lifecycle
Every ORM object exists in one of four distinct states relative to a `Session`:

```
          [ New Python Object ]
                   |
                   v
            +--------------+
            |  TRANSIENT   |  (Not in session, no primary key)
            +-------+------+
                    | session.add(obj)
                    v
            +--------------+
            |   PENDING    |  (In session, not yet saved to DB)
            +-------+------+
                    | session.flush() / session.commit()
                    v
            +--------------+
            |  PERSISTENT  |  (In session, synchronized with DB row)
            +-------+------+
                    | session.close() / session.expunge()
                    v
            +--------------+
            |   DETACHED   |  (Has primary key, but session is closed)
            +--------------+
```

1. **Transient**: Created via normal constructor (`patient = Patient(name="Alice")`). Has no database identity and is not associated with any session.
2. **Pending**: Registered with the session via `session.add(patient)`. Staged for insertion during the next flush.
3. **Persistent**: Synchronized with an actual database row. Possesses an assigned database primary key.
4. **Detached**: Formerly persistent object whose owning `Session` has been closed or expunged. Its attributes still exist in Python memory, but modifications will not be tracked or committed.

### `session.flush()` vs `session.commit()`
- **`flush()`**: Emits pending SQL DML (`INSERT`, `UPDATE`, `DELETE`) to the database transaction buffer. Database triggers run, autoincrement IDs are populated, but the transaction remains open and uncommitted. Can be rolled back.
- **`commit()`**: Automatically calls `flush()`, commits the underlying database transaction permanently, and marks the session ready for the next transaction.

---

## 3. Real-World Code Implementation & Patterns

### 1. Modern SQLAlchemy 2.0 Select Queries
SQLAlchemy 2.0 replaced legacy `session.query(Model)` with explicit `select()` constructs:

```python
from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

def get_scheduled_surgeries(session: Session, department: str, min_duration_mins: int):
    # Construct declarative SQL select statement
    stmt = (
        select(Surgery)
        .where(
            and_(
                Surgery.department == department,
                Surgery.duration_minutes >= min_duration_mins,
                Surgery.status == "SCHEDULED"
            )
        )
        .order_by(desc(Surgery.scheduled_time))
    )

    # session.scalars() unpacks the 1st column of each tuple result into Model instances
    surgeries = session.scalars(stmt).all()
    return surgeries
```

### 2. Relational Join Queries
```python
def get_surgeries_with_operating_theatre(session: Session, theatre_code: str):
    stmt = (
        select(Surgery)
        .join(OperatingTheatre, Surgery.theatre_id == OperatingTheatre.id)
        .where(OperatingTheatre.code == theatre_code)
        .order_by(Surgery.scheduled_time.asc())
    )
    return session.scalars(stmt).all()
```

### 3. Safe Session Context Management
```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def update_patient_status(patient_id: int, new_status: str):
    # Context manager automatically commits on clean exit, rolls back on exception
    with SessionLocal() as session:
        with session.begin():
            stmt = select(Patient).where(Patient.id == patient_id)
            patient = session.scalars(stmt).first()
            if not patient:
                raise ValueError(f"Patient {patient_id} not found")
            patient.status = new_status
            # commit happens automatically when exiting session.begin()
```

---

## 4. Failure Modes & Edge Cases

| Failure Mode | Symptoms | Resolution |
| :--- | :--- | :--- |
| **`DetachedInstanceError`** | Accessing a lazy relationship on an object after its session has closed. | Configure eager loading (`selectinload`), or access attributes while the session is open, or set `expire_on_commit=False`. |
| **Silent Rollback Discard** | Failing to catch exceptions and leaving dirty objects in session across web requests. | Always scope sessions per-request and close them in `finally` blocks. |
| **`NoResultFound` / `MultipleResultsFound`** | Using `session.scalars(stmt).one()` when query returns 0 or 2+ rows. | Use `.scalar_one_or_none()` when expecting 0 or 1 rows safely. |
| **Forgotten `commit()`** | Inserts succeed in Python code, but database tables remain completely empty! | Ensure `session.commit()` or `with session.begin():` is explicitly invoked. |

---

## 5. Performance & Optimization: Session Identity Map

The session's **Identity Map** functions as an in-memory cache of persistent objects keyed by `(ModelClass, primary_key)`:
```python
# Query 1: Emits SELECT statement across the wire
patient_a = session.get(Patient, 101)

# Query 2: Retrieves existing patient_a directly from memory with ZERO SQL emitted!
patient_b = session.get(Patient, 101)

assert patient_a is patient_b  # Exact same Python object reference!
```
The identity map guarantees that multiple queries for the same primary key in a single transaction never result in conflicting in-memory Python instances.

---

## 6. Industry Best Practices & Production Patterns

1. **Use `expire_on_commit=False` for Web APIs**:
   By default, `commit()` expires all attributes on persistent instances so the next access re-queries the database. Setting `expire_on_commit=False` preserves loaded attributes in memory, allowing you to serialize the object to JSON after the session closes without triggering `DetachedInstanceError`.
2. **Bulk Inserts via `session.add_all()`**:
   Instead of looping with `session.add(obj)`, pass a list of instances to `session.add_all(instances)` to allow SQLAlchemy to batch internal queue operations.
3. **Use `.scalar_one_or_none()` for Unique Lookups**:
   Avoid `.first()` when querying by unique identifiers (e.g., MRN or email); `.scalar_one_or_none()` validates that the database actually contains at most one match.

---

## 7. Healthcare Domain Case Study: Operating Theatre Dispatcher

In emergency surgical departments, scheduling an emergency procedure involves:
1. Finding an open Operating Theatre (e.g. `OT-01`).
2. Booking the surgical slot for the patient.
3. Marking the theatre as occupied.

Using a single `Session`:
- The surgeon and procedure records are created.
- The theatre status is updated to `"IN_USE"`.
- If another thread concurrently reserved `OT-01`, a unique constraint or conflict causes a database rollback, ensuring no patient is ever transferred into an already occupied operating theatre.

---

## 8. Hands-On Verification & Knowledge Check

1. What is the difference between `session.flush()` and `session.commit()`?
2. What causes SQLAlchemy to raise a `DetachedInstanceError`?
3. How does the session's Identity Map prevent duplicate object references in Python memory?
