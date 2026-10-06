"""
Lab 1 Easy: Patient Allergy Cross-Reference & Eager Loading Hub
Reference Solution
"""

from typing import List, Optional
from sqlalchemy import Table, Column, Integer, String, ForeignKey, select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload, Session


class AllergyRegistryBase(DeclarativeBase):
    pass


patient_allergy_links = Table(
    "patient_allergy_links",
    AllergyRegistryBase.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    Column("allergy_id", Integer, ForeignKey("allergies.id", ondelete="CASCADE"), primary_key=True),
)


class Allergen(AllergyRegistryBase):
    __tablename__ = "allergies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)

    patients: Mapped[List["Patient"]] = relationship(
        "Patient",
        secondary=patient_allergy_links,
        back_populates="allergies"
    )

    def __repr__(self) -> str:
        return f"<Allergen(id={self.id}, name='{self.name}', category='{self.category}')>"


class Patient(AllergyRegistryBase):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mrn: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    allergies: Mapped[List[Allergen]] = relationship(
        Allergen,
        secondary=patient_allergy_links,
        back_populates="patients"
    )

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, mrn='{self.mrn}', name='{self.name}')>"


class PatientAllergyService:

    def initialize_schema(self, engine) -> None:
        AllergyRegistryBase.metadata.create_all(engine)

    def record_allergen(self, session: Session, name: str, category: str) -> Allergen:
        allergen = Allergen(name=name, category=category)
        session.add(allergen)
        session.commit()
        return allergen

    def register_patient(self, session: Session, mrn: str, name: str) -> Patient:
        patient = Patient(mrn=mrn, name=name)
        session.add(patient)
        session.commit()
        return patient

    def link_allergy(self, session: Session, mrn: str, allergen_name: str) -> bool:
        patient_stmt = select(Patient).where(Patient.mrn == mrn)
        patient = session.scalars(patient_stmt).one_or_none()
        allergen_stmt = select(Allergen).where(Allergen.name == allergen_name)
        allergen = session.scalars(allergen_stmt).one_or_none()

        if not patient or not allergen:
            return False

        if allergen not in patient.allergies:
            patient.allergies.append(allergen)
            session.commit()
        return True

    def get_patient_allergies_eager(self, session: Session, mrn: str) -> List[str]:
        stmt = (
            select(Patient)
            .options(selectinload(Patient.allergies))
            .where(Patient.mrn == mrn)
        )
        patient = session.scalars(stmt).one_or_none()
        if not patient:
            return []
        return sorted([a.name for a in patient.allergies])

    def find_patients_allergic_to(self, session: Session, allergen_name: str) -> List[Patient]:
        stmt = (
            select(Patient)
            .join(patient_allergy_links, Patient.id == patient_allergy_links.c.patient_id)
            .join(Allergen, Allergen.id == patient_allergy_links.c.allergy_id)
            .where(Allergen.name == allergen_name)
            .order_by(Patient.name.asc())
        )
        return list(session.scalars(stmt).all())
