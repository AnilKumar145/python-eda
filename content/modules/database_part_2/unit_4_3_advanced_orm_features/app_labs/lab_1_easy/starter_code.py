"""
Lab 1 Easy: Patient Allergy Cross-Reference & Eager Loading Hub
Student Starter Code
"""

from typing import List, Optional
from sqlalchemy import Table, Column, Integer, String, ForeignKey, select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload, Session


class AllergyRegistryBase(DeclarativeBase):
    pass


# TODO: Define patient_allergy_links junction Table
patient_allergy_links = Table(
    "patient_allergy_links",
    AllergyRegistryBase.metadata,
    # WRITE CODE HERE
)


# TODO: Define Allergen entity
class Allergen(AllergyRegistryBase):
    __tablename__ = "allergies"
    # WRITE CODE HERE
    pass


# TODO: Define Patient entity
class Patient(AllergyRegistryBase):
    __tablename__ = "patients"
    # WRITE CODE HERE
    pass


class PatientAllergyService:

    def initialize_schema(self, engine) -> None:
        # TODO: Initialize tables
        pass

    def record_allergen(self, session: Session, name: str, category: str) -> Allergen:
        # TODO: Record allergen
        pass

    def register_patient(self, session: Session, mrn: str, name: str) -> Patient:
        # TODO: Register patient
        pass

    def link_allergy(self, session: Session, mrn: str, allergen_name: str) -> bool:
        # TODO: Link allergen to patient
        pass

    def get_patient_allergies_eager(self, session: Session, mrn: str) -> List[str]:
        # TODO: Eager load allergies with selectinload and return list of allergen names
        pass

    def find_patients_allergic_to(self, session: Session, allergen_name: str) -> List[Patient]:
        # TODO: Find patients using join
        pass
