"""
Unit 4.2 Exercises: SQLAlchemy Sessions
Student Starter - Implement each function using modern SQLAlchemy 2.0 Session and select() constructs.
"""

from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, create_engine, select, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker


class SessionClinicBase(DeclarativeBase):
    pass


class Physician(SessionClinicBase):
    __tablename__ = "physicians"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


# Exercise 1: Add Physician
def add_physician(session: Session, name: str, specialty: str) -> int:
    """
    Create a Physician entity, add to session, commit, and return assigned physician.id.
    """
    # TODO: Implement adding and committing physician
    return 0


# Exercise 2: Query Active Physicians by Specialty
def query_active_by_specialty(session: Session, specialty: str) -> List[Physician]:
    """
    Query all active physicians (is_active == True) with matching specialty,
    ordered by name ascending. Return list of Physician entities.
    """
    # TODO: Execute modern select() statement and return session.scalars().all()
    return []


# Exercise 3: Update Status
def update_physician_status(session: Session, physician_id: int, is_active: bool) -> bool:
    """
    Look up physician by id using session.get(). If found, update is_active, commit, and return True.
    If not found, return False.
    """
    # TODO: Fetch, update attribute, and commit
    return False


# Exercise 4: Delete Physician
def delete_physician(session: Session, physician_id: int) -> bool:
    """
    Look up physician by id using session.get(). If found, delete from session, commit, and return True.
    If not found, return False.
    """
    # TODO: Delete entity and commit
    return False


if __name__ == "__main__":
    print("Run the solutions file to test your implementations.")
