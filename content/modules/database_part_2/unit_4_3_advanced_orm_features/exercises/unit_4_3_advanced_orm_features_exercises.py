"""
Unit 4.3 Exercises: Advanced ORM Features
Student Starter - Implement many-to-many relationships, hybrid properties, and eager loading.
"""

from typing import List, Optional
from sqlalchemy import Table, Column, Integer, String, ForeignKey, select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload, Session
from sqlalchemy.ext.hybrid import hybrid_property


class AdvancedClinicBase(DeclarativeBase):
    pass


# TODO: Define secondary association table 'doctor_certifications'
# Columns:
#   doctor_id: Integer, ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True
#   certification_id: Integer, ForeignKey("certifications.id", ondelete="CASCADE"), primary_key=True
doctor_certifications = Table(
    "doctor_certifications",
    AdvancedClinicBase.metadata,
    # WRITE CODE HERE
)


# TODO: Define Certification entity
class Certification(AdvancedClinicBase):
    __tablename__ = "certifications"
    # Columns: id (int PK), name (String 80 unique)
    # Relationship: doctors (secondary=doctor_certifications, back_populates="certifications")
    pass


# TODO: Define Doctor entity with hybrid_property full_name
class Doctor(AdvancedClinicBase):
    __tablename__ = "doctors"
    # Columns: id (int PK), first_name (str), last_name (str)
    # Relationship: certifications (secondary=doctor_certifications, back_populates="doctors")
    # Hybrid property: full_name (Python getter and SQL expression)
    pass


# Exercise 2: Assign Certification
def assign_certification(session: Session, doctor: Doctor, cert: Certification) -> None:
    """Link certification to doctor and commit."""
    # TODO: Implement assignment
    pass


# Exercise 3: Query Doctor by Hybrid Name
def find_doctor_by_full_name(session: Session, target_name: str) -> Optional[Doctor]:
    """Query Doctor where Doctor.full_name matches target_name."""
    # TODO: Execute select(Doctor).where(Doctor.full_name == target_name)
    return None


# Exercise 4: Eager Loading Query
def get_all_doctors_eager(session: Session) -> List[Doctor]:
    """Return all doctors with their certifications eager-loaded via selectinload."""
    # TODO: Execute select(Doctor).options(selectinload(Doctor.certifications))
    return []


if __name__ == "__main__":
    print("Run the solutions file to test your implementations.")
