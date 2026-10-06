"""
Unit 4.3 Exercises: Advanced ORM Features - Solutions & Test Verification
"""

from typing import List, Optional
from sqlalchemy import Table, Column, Integer, String, ForeignKey, select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload, Session, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property


class AdvancedClinicBase(DeclarativeBase):
    pass


doctor_certifications = Table(
    "doctor_certifications",
    AdvancedClinicBase.metadata,
    Column("doctor_id", Integer, ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True),
    Column("certification_id", Integer, ForeignKey("certifications.id", ondelete="CASCADE"), primary_key=True),
)


class Certification(AdvancedClinicBase):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    doctors: Mapped[List["Doctor"]] = relationship(
        "Doctor",
        secondary=doctor_certifications,
        back_populates="certifications"
    )

    def __repr__(self) -> str:
        return f"<Certification(id={self.id}, name='{self.name}')>"


class Doctor(AdvancedClinicBase):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)

    certifications: Mapped[List[Certification]] = relationship(
        Certification,
        secondary=doctor_certifications,
        back_populates="doctors"
    )

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    def full_name(cls):
        return cls.first_name + " " + cls.last_name

    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, name='{self.full_name}')>"


def assign_certification(session: Session, doctor: Doctor, cert: Certification) -> None:
    if cert not in doctor.certifications:
        doctor.certifications.append(cert)
    session.commit()


def find_doctor_by_full_name(session: Session, target_name: str) -> Optional[Doctor]:
    stmt = select(Doctor).where(Doctor.full_name == target_name)
    return session.scalars(stmt).one_or_none()


def get_all_doctors_eager(session: Session) -> List[Doctor]:
    stmt = select(Doctor).options(selectinload(Doctor.certifications)).order_by(Doctor.id.asc())
    return list(session.scalars(stmt).all())


if __name__ == "__main__":
    print("Running Unit 4.3 Solutions Test Suite...")

    engine = create_engine("sqlite:///:memory:", echo=False)
    AdvancedClinicBase.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    with SessionLocal() as session:
        # Create doctors and certs
        doc1 = Doctor(first_name="Gregory", last_name="House")
        doc2 = Doctor(first_name="James", last_name="Wilson")
        cert1 = Certification(name="Board Certified Nephrology")
        cert2 = Certification(name="Board Certified Oncology")
        cert3 = Certification(name="Infectious Disease Specialist")

        session.add_all([doc1, doc2, cert1, cert2, cert3])
        session.commit()

        # Test 1: Assign Certifications
        assign_certification(session, doc1, cert1)
        assign_certification(session, doc1, cert3)
        assign_certification(session, doc2, cert2)

        assert len(doc1.certifications) == 2, "Expected 2 certs for Dr. House"
        assert len(doc2.certifications) == 1, "Expected 1 cert for Dr. Wilson"
        print("Exercise 1 passed: Many-to-many relationship assigned and committed.")

        # Test 2: Hybrid Property Lookup
        found_doc = find_doctor_by_full_name(session, "Gregory House")
        assert found_doc is not None, "Doctor not found via hybrid property"
        assert found_doc.id == doc1.id, "Found incorrect doctor"
        print("Exercise 2 passed: Hybrid property SQL filter expression verified.")

        # Test 3: Eager Loading
        all_docs = get_all_doctors_eager(session)
        assert len(all_docs) == 2, "Expected 2 doctors"
        assert len(all_docs[0].certifications) == 2, "Eager certifications not populated"
        print("Exercise 3 passed: Eager loading via selectinload verified.")

    print("All Unit 4.3 Exercise Solutions PASSED!")
