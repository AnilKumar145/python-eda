# Tasks: Inpatient Bed Allocation & Ward Registry

## Task 1: Define `HospitalBase` and Declarative Entities
Subclass `DeclarativeBase` to create `HospitalBase`.

1. **`Ward` entity**:
   - `__tablename__ = "wards"`
   - `id`: `int` primary key, autoincrementing.
   - `name`: `str` (String 80), unique, not nullable.
   - `floor`: `int`, not nullable.
   - `capacity`: `int`, not nullable.
   - `beds`: 1-to-many relationship with `Bed` model, `back_populates="ward"`, `cascade="all, delete-orphan"`.
   - Table constraint: Check constraint `capacity > 0`.

2. **`Bed` entity**:
   - `__tablename__ = "beds"`
   - `id`: `int` primary key, autoincrementing.
   - `bed_label`: `str` (String 32), unique, not nullable.
   - `ward_id`: `int` foreign key referencing `"wards.id"` with `ondelete="CASCADE"`, not nullable.
   - `is_occupied`: `bool`, default `False`, not nullable.
   - `ward`: many-to-1 relationship with `Ward`, `back_populates="beds"`.

## Task 2: Implement Bed Allocation Service
In `WardRegistryService`:
- `initialize_schema(engine)`: Create tables using `HospitalBase.metadata.create_all(engine)`.
- `allocate_ward(name, floor, capacity, bed_labels)`: Create a `Ward` instance and populate it with `Bed` instances corresponding to each label in `bed_labels`. Raise `ValueError` if `len(bed_labels) > capacity`.
