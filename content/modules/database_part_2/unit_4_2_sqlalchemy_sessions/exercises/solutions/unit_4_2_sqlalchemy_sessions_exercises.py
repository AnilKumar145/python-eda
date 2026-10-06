"""
Unit 4.2 Exercises: SQLAlchemy Sessions - Solutions & Test Verification
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


def add_physician(session: Session, name: str, specialty: str) -> int:
    physician = Physician(name=name, specialty=specialty, is_active=True)
    session.add(physician)
    session.commit()
    return physician.id


def query_active_by_specialty(session: Session, specialty: str) -> List[Physician]:
    stmt = (
        select(Physician)
        .where(
            and_(
                Physician.specialty == specialty,
                Physician.is_active == True
            )
        )
        .order_by(Physician.name.asc())
    )
    return list(session.scalars(stmt).all())


def update_physician_status(session: Session, physician_id: int, is_active: bool) -> bool:
    physician = session.get(Physician, physician_id)
    if not physician:
        return False
    physician.is_active = is_active
    session.commit()
    return True


def delete_physician(session: Session, physician_id: int) -> bool:
    physician = session.get(Physician, physician_id)
    if not physician:
        return False
    session.delete(physician)
    session.commit()
    return True


if __name__ == "__main__":
    print("Running Unit 4.2 Solutions Test Suite...")

    engine = create_engine("sqlite:///:memory:", echo=False)
    SessionClinicBase.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    with SessionLocal() as session:
        # Test 1: Add
        doc_id1 = add_physician(session, "Dr. Gregory House", "Diagnostics")
        doc_id2 = add_physician(session, "Dr. Allison Cameron", "Diagnostics")
        doc_id3 = add_physician(session, "Dr. Robert Chase", "Surgery")
        assert doc_id1 > 0 and doc_id2 > 0 and doc_id3 > 0, "Physician IDs must be generated"
        print("Exercise 1 passed: Added 3 physicians.")

        # Test 2: Query
        diagnosticians = query_active_by_specialty(session, "Diagnostics")
        assert len(diagnosticians) == 2, f"Expected 2 diagnosticians, got {len(diagnosticians)}"
        assert diagnosticians[0].name == "Dr. Allison Cameron", "Ordering by name failed"
        print("Exercise 2 passed: Query filtered and ordered correctly.")

        # Test 3: Update
        updated = update_physician_status(session, doc_id1, False)
        assert updated is True, "Update failed"
        active_diagnosticians = query_active_by_specialty(session, "Diagnostics")
        assert len(active_diagnosticians) == 1, "Deactivated physician should not be returned"
        print("Exercise 3 passed: Status update committed.")

        # Test 4: Delete
        deleted = delete_physician(session, doc_id3)
        assert deleted is True, "Delete failed"
        surgeries = query_active_by_specialty(session, "Surgery")
        assert len(surgeries) == 0, "Deleted physician should not exist"
        print("Exercise 4 passed: Deletion verified.")

    print("All Unit 4.2 Exercise Solutions PASSED!")
