"""
Unit 4.1 Exercises: ORM Fundamentals
Student Starter - Implement the declarative models and helper functions below.
"""

from typing import List, Optional, Tuple
from sqlalchemy import String, Integer, ForeignKey, create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Exercise 1: Define DeclarativeBase and Models
class ClinicBase(DeclarativeBase):
    pass


# TODO: Define Department model inheriting from ClinicBase
# Table name: "departments"
# Columns:
#   id: Mapped[int] - primary key, autoincrement
#   name: Mapped[str] - String(100), unique, nullable=False
#   head_physician: Mapped[str] - String(120), nullable=False
# Relationship:
#   staff_members: Mapped[List["StaffMember"]] - relationship to StaffMember,
#                  back_populates="department", cascade="all, delete-orphan"
class Department(ClinicBase):
    __tablename__ = "departments"
    # WRITE CODE HERE
    pass


# TODO: Define StaffMember model inheriting from ClinicBase
# Table name: "staff_members"
# Columns:
#   id: Mapped[int] - primary key, autoincrement
#   department_id: Mapped[int] - ForeignKey("departments.id", ondelete="CASCADE"), nullable=False
#   full_name: Mapped[str] - String(120), nullable=False
#   role: Mapped[str] - String(50), nullable=False
# Relationship:
#   department: Mapped["Department"] - relationship to Department, back_populates="staff_members"
class StaffMember(ClinicBase):
    __tablename__ = "staff_members"
    # WRITE CODE HERE
    pass


# Exercise 2: Schema DDL Generator
def create_schema(engine) -> None:
    """Emit DDL CREATE TABLE statements for ClinicBase models."""
    # TODO: Call create_all on metadata
    pass


# Exercise 3: Inspect Database Tables
def get_existing_tables(engine) -> List[str]:
    """Inspect and return sorted list of table names in the database."""
    # TODO: Use inspect(engine).get_table_names()
    return []


# Exercise 4: Object Relationship Builder
def build_department_with_staff(
    dept_name: str,
    head_physician: str,
    staff_info: List[Tuple[str, str]]
) -> Department:
    """
    Instantiate a Department and append child StaffMember instances to its staff_members list.
    staff_info is a list of (full_name, role) tuples.
    Return the populated Department instance.
    """
    # TODO: Build and return Department object with attached StaffMember objects
    return None


if __name__ == "__main__":
    print("Run the solutions file to test your implementations.")
