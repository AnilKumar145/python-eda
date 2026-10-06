"""
Unit 4.1 Exercises: ORM Fundamentals - Solutions & Test Verification
"""

from typing import List, Optional, Tuple
from sqlalchemy import String, Integer, ForeignKey, create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Exercise 1: Define DeclarativeBase and Models
class ClinicBase(DeclarativeBase):
    pass


class Department(ClinicBase):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    head_physician: Mapped[str] = mapped_column(String(120), nullable=False)

    staff_members: Mapped[List["StaffMember"]] = relationship(
        "StaffMember",
        back_populates="department",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Department(id={self.id}, name='{self.name}')>"


class StaffMember(ClinicBase):
    __tablename__ = "staff_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="staff_members"
    )

    def __repr__(self) -> str:
        return f"<StaffMember(id={self.id}, name='{self.full_name}', role='{self.role}')>"


# Exercise 2: Schema DDL Generator
def create_schema(engine) -> None:
    ClinicBase.metadata.create_all(engine)


# Exercise 3: Inspect Database Tables
def get_existing_tables(engine) -> List[str]:
    inspector = inspect(engine)
    return sorted(inspector.get_table_names())


# Exercise 4: Object Relationship Builder
def build_department_with_staff(
    dept_name: str,
    head_physician: str,
    staff_info: List[Tuple[str, str]]
) -> Department:
    dept = Department(name=dept_name, head_physician=head_physician)
    for name, role in staff_info:
        StaffMember(full_name=name, role=role, department=dept)
    return dept


if __name__ == "__main__":
    print("Running Unit 4.1 Solutions Test Suite...")

    # Test 1 & 2: Create Schema
    engine = create_engine("sqlite:///:memory:", echo=False)
    create_schema(engine)

    # Test 3: Table Inspection
    tables = get_existing_tables(engine)
    assert "departments" in tables, f"Expected 'departments' in {tables}"
    assert "staff_members" in tables, f"Expected 'staff_members' in {tables}"
    print("Exercise 1 & 2 & 3 passed: Schema created and tables inspected:", tables)

    # Test 4: Object Relationship Builder
    staff_records = [
        ("Dr. John Watson", "Attending"),
        ("Nurse Clara Barton", "Charge Nurse"),
        ("Mark Davis", "Paramedic")
    ]
    cardio = build_department_with_staff("Cardiology", "Dr. Gregory House", staff_records)
    assert cardio.name == "Cardiology", "Department name mismatch"
    assert len(cardio.staff_members) == 3, f"Expected 3 staff members, got {len(cardio.staff_members)}"
    assert cardio.staff_members[0].full_name == "Dr. John Watson", "First staff name mismatch"
    assert cardio.staff_members[0].department is cardio, "Bidirectional relationship reference failed"
    print("Exercise 4 passed: Object relationship in-memory graph validated.")

    print("All Unit 4.1 Exercise Solutions PASSED!")
