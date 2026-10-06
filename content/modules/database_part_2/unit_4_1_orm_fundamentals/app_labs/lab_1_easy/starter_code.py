"""
Lab 1 Easy: Inpatient Bed Allocation & Ward Registry
Student Starter Code
"""

from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, CheckConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class HospitalBase(DeclarativeBase):
    pass


# TODO: Define Ward entity
class Ward(HospitalBase):
    __tablename__ = "wards"
    # WRITE CODE HERE
    pass


# TODO: Define Bed entity
class Bed(HospitalBase):
    __tablename__ = "beds"
    # WRITE CODE HERE
    pass


class WardRegistryService:

    def initialize_schema(self, engine) -> None:
        """Create tables for HospitalBase."""
        # TODO: Implement schema creation
        pass

    def allocate_ward(
        self,
        name: str,
        floor: int,
        capacity: int,
        bed_labels: List[str]
    ) -> Ward:
        """
        Create a Ward instance and populate it with Bed instances.
        Raise ValueError if len(bed_labels) > capacity.
        """
        # TODO: Implement ward allocation with beds
        pass
