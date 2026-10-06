# Lesson 4.1: SQLAlchemy 2.0 Declarative Modeling and Relational Mapping

---

## 1. Conceptual Foundation

In modern application engineering, developers work with **Object-Oriented Programming (OOP)** languages like Python, representing domain entities through classes, instance attributes, and method behaviors. Relational databases, on the other hand, represent entities as **tables, rows, and mathematical relations**.

This fundamental divide is known as the **Object-Relational Impedance Mismatch**:
- **Identity**: In Python, object identity is memory address (`id(obj)`). In SQL, identity is a primary key value (`id = 42`).
- **Data Types**: Python uses dynamically typed objects, arbitrary-precision integers, and rich composite structures. SQL requires fixed column definitions (`VARCHAR(100)`, `NUMERIC(10,2)`).
- **Relationships**: In Python, relationships are direct memory object references (e.g., `patient.vitals_records.append(record)`). In SQL, relationships are governed by foreign key constraints and join operations across relational tables.

An **Object-Relational Mapper (ORM)** bridges this divide. It translates Python class definitions into database tables, converts rows into instantiated Python objects, and translates object state changes into SQL statements automatically.

```
+------------------------------------------------------------------------+
|                          Python Domain Code                            |
|    ward = Ward(name="ICU East")                                        |
|    bed = Bed(bed_number="ICU-101", ward=ward)                          |
+-----------------------------------+------------------------------------+
                                    | SQLAlchemy ORM Unit of Work
                                    v
+------------------------------------------------------------------------+
|                         SQLAlchemy Core & Dialect                      |
|    INSERT INTO wards (name) VALUES ('ICU East') RETURNING id;          |
|    INSERT INTO beds (bed_number, ward_id) VALUES ('ICU-101', 1);       |
+-----------------------------------+------------------------------------+
                                    | DB-API (sqlite3 / psycopg2)
                                    v
+------------------------------------------------------------------------+
|                         Relational Database Disk                       |
+------------------------------------------------------------------------+
```

---

## 2. Architecture & Internal Mechanics

SQLAlchemy is organized into two distinct layers: **Core** and **ORM**.

```
+------------------------------------------------------------------------+
|                          SQLAlchemy ORM Layer                          |
|         DeclarativeBase, Mapped, Session, relationship()               |
+-----------------------------------+------------------------------------+
                                    | Built on top of
                                    v
+------------------------------------------------------------------------+
|                         SQLAlchemy Core Layer                          |
|         MetaData, Table, Column, select(), insert(), update()          |
+-----------------------------------+------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                            Database Engine                             |
|          Connection Pool (QueuePool) + Dialect (PostgreSQL/SQLite)     |
+-----------------------------------+------------------------------------+
                                    | DB-API 2.0
                                    v
+------------------------------------------------------------------------+
|                          Physical Database RDBMS                       |
+------------------------------------------------------------------------+
```

### SQLAlchemy 2.0 Modern Declarative Syntax
Prior to SQLAlchemy 2.0, models used dynamic `Column()` attributes without static type-checker awareness. SQLAlchemy 2.0 introduced PEP 484 type annotations using `Mapped[...]` and `mapped_column()`:
1. **`DeclarativeBase`**: The root base class from which all ORM entities inherit. It maintains a shared `MetaData` registry containing table catalog information.
2. **`Mapped[T]`**: Type annotation explicitly stating the Python type of the attribute (`int`, `str`, `datetime`, `Optional[str]`).
3. **`mapped_column()`**: Configures SQL-specific schema details, such as column names, foreign keys, constraints, and indices.
4. **`relationship()`**: Declares an in-memory navigational link between related models.

---

## 3. Real-World Code Implementation & Patterns

### 1. Defining Declarative Models in SQLAlchemy 2.0
```python
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    String, Integer, ForeignKey, DateTime, CheckConstraint, func, create_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Ward(Base):
    __tablename__ = "wards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    # 1-to-many relationship with Beds
    beds: Mapped[List["Bed"]] = relationship(
        "Bed", 
        back_populates="ward", 
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("capacity > 0", name="chk_ward_capacity_positive"),
    )

    def __repr__(self) -> str:
        return f"<Ward(id={self.id}, name='{self.name}', capacity={self.capacity})>"


class Bed(Base):
    __tablename__ = "beds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bed_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    ward_id: Mapped[int] = mapped_column(ForeignKey("wards.id", ondelete="CASCADE"), nullable=False)
    is_occupied: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Many-to-1 relationship back to Ward
    ward: Mapped["Ward"] = relationship("Ward", back_populates="beds")

    def __repr__(self) -> str:
        return f"<Bed(id={self.id}, number='{self.bed_number}', occupied={self.is_occupied})>"
```

### 2. Creating Tables Programmatically
```python
# Create an in-memory SQLite engine
engine = create_engine("sqlite:///:memory:", echo=False)

# Emit CREATE TABLE statements for all registered Declarative models
Base.metadata.create_all(engine)
```

---

## 4. Failure Modes & Edge Cases

| Failure Mode | Root Cause | Engineering Solution |
| :--- | :--- | :--- |
| **`back_populates` Mismatch** | Typo in relationship name string causes runtime `ArgumentError`. | Ensure both sides of the relationship point to matching attribute names on the opposing model. |
| **Orphaned Child Records** | Deleting parent without `cascade="all, delete-orphan"` leaves child rows pointing to non-existent parent. | Configure `cascade="all, delete-orphan"` on 1-to-many relationships and `ondelete="CASCADE"` on the foreign key. |
| **Missing Foreign Key in `ForeignKey()`** | Referencing table name instead of `table_name.column` (e.g. `ForeignKey("wards")`). | Always specify target column explicitly: `ForeignKey("wards.id")`. |
| **Mutable Default Argument Pitfall** | Using `default=[]` or `default=datetime.now()` executes once at import time. | Use callable defaults: `default=datetime.utcnow` or database server defaults: `server_default=func.now()`. |

---

## 5. Performance & Optimization: Core vs ORM

| Dimension | SQLAlchemy Core | SQLAlchemy ORM |
| :--- | :--- | :--- |
| **Level of Abstraction** | SQL Expression Language (`Table`, `select()`) | Python Domain Objects & Unit of Work |
| **Throughput** | High throughput (direct tuple mapping) | Moderate throughput (object instantiation overhead) |
| **Use Case** | High-volume batch ingestion, reporting, data pipelines | Domain business logic, web apps, REST APIs |
| **Memory Overhead** | Low (raw dictionaries/tuples) | Higher (managed objects in identity map) |

**Rule of Thumb**: Use ORM for application business workflows where entities maintain business methods and relationships. Fall back to Core expressions for bulk batch ingestion of 100,000+ records.

---

## 6. Industry Best Practices & Production Patterns

1. **Always Use `back_populates` Instead of `backref`**:
   `backref` dynamically synthesizes an attribute on the related model at runtime, hiding it from IDE autocomplete and static type checkers. `back_populates` explicitly defines attributes on both classes, providing full IDE type hinting and safety.
2. **Explicit Nullability**:
   In SQLAlchemy 2.0, `mapped_column()` defaults nullability based on whether the Python type is `Optional[T]` or `T`. Explicitly declaring `nullable=False` or `nullable=True` clarifies intent and avoids schema discrepancies across databases.
3. **Keep `Base.metadata.create_all()` in Tests Only**:
   In production environments, never run `create_all()`. Use database migration tools like **Alembic** to incrementally evolve production schemas.

---

## 7. Healthcare Domain Case Study: Hospital Inpatient Bed Allocation

In emergency hospitals, inpatient bed management is critical. Wards (Intensive Care, Oncology, Pediatric, Surgical) have finite bed capacities. 

When an emergency trauma patient arrives, the triage coordinator requires real-time bed lookup. By modeling `Ward` and `Bed` with proper foreign keys and bidirectional relationships:
1. `ward.beds` immediately yields all physical beds assigned to that ward.
2. Database check constraints (`CheckConstraint("capacity > 0")`) prevent administrators from configuring illegal negative bed spaces.
3. If an entire temporary ward is decommissioned, cascading deletes safely clear bed assignments without corrupting relational integrity.

---

## 8. Hands-On Verification & Knowledge Check

1. What is the fundamental difference between SQLAlchemy Core and SQLAlchemy ORM?
2. Why is `back_populates` strongly preferred over legacy `backref` in modern Python codebases?
3. What is the purpose of `cascade="all, delete-orphan"` in a 1-to-many relationship?
