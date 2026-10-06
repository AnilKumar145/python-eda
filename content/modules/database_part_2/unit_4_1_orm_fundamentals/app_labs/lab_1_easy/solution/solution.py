"""
Lab 1 Easy: Inpatient Bed Allocation & Ward Registry
Reference Solution
"""

from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, CheckConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class HospitalBase(DeclarativeBase):
    pass


class Ward(HospitalBase):
    __tablename__ = "wards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    beds: Mapped[List["Bed"]] = relationship(
        "Bed",
        back_populates="ward",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("capacity > 0", name="chk_ward_capacity_positive"),
    )

    def __repr__(self) -> str:
        return f"<Ward(id={self.id}, name='{self.name}', floor={self.floor})>"


class Bed(HospitalBase):
    __tablename__ = "beds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bed_label: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    ward_id: Mapped[int] = mapped_column(
        ForeignKey("wards.id", ondelete="CASCADE"), nullable=False
    )
    is_occupied: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    ward: Mapped["Ward"] = relationship(
        "Ward",
        back_populates="beds"
    )

    def __repr__(self) -> str:
        return f"<Bed(id={self.id}, label='{self.bed_label}', occupied={self.is_occupied})>"


class WardRegistryService:

    def initialize_schema(self, engine) -> None:
        HospitalBase.metadata.create_all(engine)

    def allocate_ward(
        self,
        name: str,
        floor: int,
        capacity: int,
        bed_labels: List[str]
    ) -> Ward:
        if len(bed_labels) > capacity:
            raise ValueError(f"Bed count ({len(bed_labels)}) exceeds capacity ({capacity})")

        ward = Ward(name=name, floor=floor, capacity=capacity)
        for label in bed_labels:
            Bed(bed_label=label, ward=ward, is_occupied=False)
        return ward
