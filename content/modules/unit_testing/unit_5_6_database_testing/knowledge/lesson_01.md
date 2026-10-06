---
title: "Database Fixtures, Transaction Rollbacks, and DAO Testing"
module: "unit_testing"
unit: "unit_5_6_database_testing"
order: 1
type: "knowledge"
difficulty: "advanced"
tags:
  topics: ["database-testing", "sqlalchemy", "transaction-rollback", "savepoint", "repository-pattern"]
  subtopics: ["sqlite-memory", "db-fixtures", "crud-tests", "integration-testing"]
use_case: "Building hermetic in-memory database test harnesses for hospital pharmacy formulary repositories."
domain: "Software Quality Engineering"
duration_hours: 1.5
---

# Lesson 5.6: Database Fixtures, Transaction Rollbacks, and DAO Testing

---

## 1. Why Mocks are Insufficient for Database Testing

Many developers attempt to test their database access code by mocking SQLAlchemy or JDBC:
```python
# MOCKING DATABASE CALLS - ANTIPATTERN!
mock_session.execute.return_value.scalars.return_value.all.return_value = [patient]
```

### Why Mocking Databases Fails:
1. **Mocks Don't Speak SQL**: A mock cannot tell you if your SQL query has a syntax error, an invalid column name, or a broken join.
2. **Mocks Ignore Constraints**: A mock will happily let you insert a row with a null primary key, duplicate unique code, or broken foreign key reference.
3. **Mocks Hide ORM Quirks**: Lazy loading errors (`DetachedInstanceError`), session flush traps, and transaction deadlocks only occur when interacting with a **real relational database engine**.

> **Industry Rule**: Never mock your database queries. Test your Data Access Layer against a real database engine!

---

## 2. The Ephemeral Test Database Pattern

To keep test suites running in milliseconds rather than minutes, enterprise test harnesses utilize **In-Memory SQLite** (`sqlite:///:memory:`):
- Requires zero external services or Docker daemon.
- Recreated from scratch in under 5 milliseconds.
- Fully supports ANSI SQL, foreign keys, indexes, and transactions.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

@pytest.fixture(scope="session")
def engine():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()
```

---

## 3. Test Isolation via Automatic Transaction Rollback

Recreating tables (`create_all` and `drop_all`) before every single test function is slow if you have 50 tables.

A far superior pattern is **Transactional Rollback Isolation**:
1. At the start of each test, open a database connection and start a **Transaction**.
2. Run the test inside this transaction (inserting records, mutating rows).
3. On teardown, simply **rollback the transaction**!
4. The database instantly reverts to its clean baseline state without executing a single `DROP TABLE` or `DELETE` statement!

```
+--------------------------------------------------------------------------+
|                  Transactional Rollback Test Lifecycle                   |
+--------------------------------------------------------------------------+
| 1. Engine Created Once (Session Scope)                                   |
|    Tables created once via Base.metadata.create_all(engine)              |
|                                                                          |
| 2. Test A Starts:                                                        |
|    - Begin Transaction                                                   |
|    - Test executes: INSERTS patient 'Alice'                              |
|    - Teardown: ROLLBACK! ('Alice' disappears from DB)                    |
|                                                                          |
| 3. Test B Starts:                                                        |
|    - Database is completely empty and clean!                             |
|    - Zero table drops required! Microsecond speed!                       |
+--------------------------------------------------------------------------+
```

---

## 4. Structuring Pytest Database Fixtures

Here is the production-grade fixture pattern for SQLAlchemy 2.0:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(engine):
    """Provides a transactional session rolled back after every test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

---

## 5. Testing CRUD Operations on SQLAlchemy Models

When testing a model, write assertions for each phase of its lifecycle:

```python
def test_medication_crud_lifecycle(db_session):
    # 1. CREATE
    med = Medication(code="AMOX-500", name="Amoxicillin 500mg", stock_count=50)
    db_session.add(med)
    db_session.commit()
    assert med.id is not None

    # 2. READ
    found = db_session.get(Medication, med.id)
    assert found.code == "AMOX-500"

    # 3. UPDATE
    found.stock_count = 45
    db_session.commit()
    assert db_session.get(Medication, med.id).stock_count == 45

    # 4. DELETE
    db_session.delete(found)
    db_session.commit()
    assert db_session.get(Medication, med.id) is None
```

---

## 6. Testing Repository / DAO (Data Access Object) Patterns

In clean enterprise architecture, controllers never call SQLAlchemy directly; they call a **Repository**:

```python
class MedicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_low_stock(self, threshold: int = 10) -> List[Medication]:
        stmt = select(Medication).where(Medication.stock_count <= threshold).order_by(Medication.stock_count.asc())
        return list(self.session.scalars(stmt).all())
```

### Testing the Repository:
```python
def test_find_low_stock_filters_and_sorts(db_session):
    repo = MedicationRepository(db_session)
    db_session.add_all([
        Medication(code="A", name="Drug A", stock_count=5),
        Medication(code="B", name="Drug B", stock_count=20),
        Medication(code="C", name="Drug C", stock_count=2),
    ])
    db_session.commit()

    low_stock = repo.find_low_stock(threshold=10)
    assert len(low_stock) == 2
    assert [m.code for m in low_stock] == ["C", "A"]  # Ascending order
```

---

## 7. Testing Constraint Violations & Integrity Errors

Ensure your test suite verifies database constraint enforcement:

```python
from sqlalchemy.exc import IntegrityError

def test_duplicate_medication_code_raises_integrity_error(db_session):
    med1 = Medication(code="EPI-01", name="Epinephrine", stock_count=10)
    med2 = Medication(code="EPI-01", name="Epi-Pen Duplicate", stock_count=5)

    db_session.add(med1)
    db_session.commit()

    db_session.add(med2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
```

---

## 8. Test Database Trade-offs: In-Memory SQLite vs Testcontainers Postgres

| Strategy | Speed | Engine Parity | Best Used For |
| :--- | :--- | :--- | :--- |
| **In-Memory SQLite** | **< 5 ms per test** | Partial (Generic ANSI SQL) | 90% of Unit and DAO tests in local dev and CI. |
| **Docker Testcontainers (Postgres)** | ~ 2–5 seconds startup | **100% exact production parity** | Specialized tests using Postgres JSONB, window functions, and migrations. |
