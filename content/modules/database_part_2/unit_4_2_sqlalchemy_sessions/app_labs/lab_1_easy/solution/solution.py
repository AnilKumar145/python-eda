"""
Lab 1 Easy: Surgical Schedule & Operating Theatre Dispatcher
Reference Solution
"""

from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey, select, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class SurgicalBase(DeclarativeBase):
    pass


class OperatingTheatre(SurgicalBase):
    __tablename__ = "theatres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    specialty: Mapped[str] = mapped_column(String(64), nullable=False)

    def __repr__(self) -> str:
        return f"<OperatingTheatre(id={self.id}, code='{self.code}')>"


class SurgicalCase(SurgicalBase):
    __tablename__ = "surgical_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    theatre_id: Mapped[int] = mapped_column(
        ForeignKey("theatres.id", ondelete="CASCADE"), nullable=False
    )
    patient_mrn: Mapped[str] = mapped_column(String(64), nullable=False)
    lead_surgeon: Mapped[str] = mapped_column(String(120), nullable=False)
    procedure_name: Mapped[str] = mapped_column(String(150), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="SCHEDULED", nullable=False)

    def __repr__(self) -> str:
        return f"<SurgicalCase(id={self.id}, mrn='{self.patient_mrn}', status='{self.status}')>"


class SurgicalDispatchService:

    def initialize_schema(self, engine) -> None:
        SurgicalBase.metadata.create_all(engine)

    def register_theatre(self, session: Session, code: str, specialty: str) -> OperatingTheatre:
        theatre = OperatingTheatre(code=code, specialty=specialty)
        session.add(theatre)
        session.commit()
        return theatre

    def schedule_case(
        self,
        session: Session,
        theatre_code: str,
        patient_mrn: str,
        lead_surgeon: str,
        procedure_name: str,
        duration_minutes: int
    ) -> int:
        theatre_stmt = select(OperatingTheatre).where(OperatingTheatre.code == theatre_code)
        theatre = session.scalars(theatre_stmt).one_or_none()
        if not theatre:
            raise ValueError(f"Operating Theatre '{theatre_code}' not found")

        surgical_case = SurgicalCase(
            theatre_id=theatre.id,
            patient_mrn=patient_mrn,
            lead_surgeon=lead_surgeon,
            procedure_name=procedure_name,
            duration_minutes=duration_minutes,
            status="SCHEDULED"
        )
        session.add(surgical_case)
        session.commit()
        return surgical_case.id

    def update_case_status(self, session: Session, case_id: int, new_status: str) -> bool:
        surgical_case = session.get(SurgicalCase, case_id)
        if not surgical_case:
            return False
        surgical_case.status = new_status
        session.commit()
        return True

    def get_active_cases_for_theatre(self, session: Session, theatre_code: str) -> List[SurgicalCase]:
        stmt = (
            select(SurgicalCase)
            .join(OperatingTheatre, SurgicalCase.theatre_id == OperatingTheatre.id)
            .where(
                and_(
                    OperatingTheatre.code == theatre_code,
                    SurgicalCase.status != "COMPLETED"
                )
            )
            .order_by(SurgicalCase.id.asc())
        )
        return list(session.scalars(stmt).all())
