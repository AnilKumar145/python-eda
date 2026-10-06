"""
Lab 1 Easy: Surgical Schedule & Operating Theatre Dispatcher
Student Starter Code
"""

from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey, select, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class SurgicalBase(DeclarativeBase):
    pass


class OperatingTheatre(SurgicalBase):
    __tablename__ = "theatres"
    # TODO: Define id, code (unique String 32), specialty (String 64)
    pass


class SurgicalCase(SurgicalBase):
    __tablename__ = "surgical_cases"
    # TODO: Define id, theatre_id (FK), patient_mrn, lead_surgeon, procedure_name, duration_minutes, status
    pass


class SurgicalDispatchService:

    def initialize_schema(self, engine) -> None:
        # TODO: Initialize tables
        pass

    def register_theatre(self, session: Session, code: str, specialty: str) -> OperatingTheatre:
        # TODO: Register theatre
        pass

    def schedule_case(
        self,
        session: Session,
        theatre_code: str,
        patient_mrn: str,
        lead_surgeon: str,
        procedure_name: str,
        duration_minutes: int
    ) -> int:
        # TODO: Schedule case and commit
        pass

    def update_case_status(self, session: Session, case_id: int, new_status: str) -> bool:
        # TODO: Update case status and commit
        pass

    def get_active_cases_for_theatre(self, session: Session, theatre_code: str) -> List[SurgicalCase]:
        # TODO: Return non-COMPLETED cases using join(OperatingTheatre)
        pass
