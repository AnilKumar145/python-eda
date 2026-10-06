"""
Unit 5.6 Exercises: Database Testing (Student Starter)

Follow the instructions and replace TODOs with working code.
"""

from typing import List, Optional
import pytest
from sqlalchemy import create_engine, String, Integer, Float, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import IntegrityError


# Database Models
class Base(DeclarativeBase):
    pass


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)


# Repository
class MedicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, name: str, stock: int, unit_price: float) -> Medication:
        """
        TODO: Create Medication instance, add to self.session, commit, and return instance.
        """
        raise NotImplementedError("TODO: Implement MedicationRepository.add")

    def get_by_id(self, med_id: int) -> Optional[Medication]:
        """
        TODO: Query Medication by primary key med_id using session.get.
        """
        raise NotImplementedError("TODO: Implement MedicationRepository.get_by_id")

    def find_low_stock(self, threshold: int) -> List[Medication]:
        """
        TODO: Query medications where stock <= threshold, ordered by stock ascending.
        """
        raise NotImplementedError("TODO: Implement MedicationRepository.find_low_stock")

    def update_stock(self, med_id: int, quantity_delta: int) -> Medication:
        """
        TODO: Find medication by id. If not found, raise ValueError.
        Calculate new stock. If new stock < 0, raise ValueError("Insufficient stock...").
        Update stock, commit, and return updated medication.
        """
        raise NotImplementedError("TODO: Implement MedicationRepository.update_stock")


# Fixtures
@pytest.fixture(scope="function")
def db_session():
    """
    TODO: Create in-memory SQLite engine: sqlite:///:memory:
    Create all tables via Base.metadata.create_all(engine)
    Yield a Session(engine)
    Drop all tables via Base.metadata.drop_all(engine) and dispose engine on teardown.
    """
    raise NotImplementedError("TODO: Implement db_session fixture")


@pytest.fixture
def repo(db_session):
    return MedicationRepository(db_session)


# Test Suite
def test_add_and_retrieve_medication(repo):
    med = repo.add("Amoxicillin 500mg", stock=150, unit_price=12.50)
    assert med.id is not None
    assert med.name == "Amoxicillin 500mg"

    fetched = repo.get_by_id(med.id)
    assert fetched is not None
    assert fetched.name == "Amoxicillin 500mg"
    assert fetched.stock == 150
    assert fetched.unit_price == 12.50


def test_duplicate_medication_name_raises_integrity_error(repo):
    repo.add("Paracetamol 650mg", stock=200, unit_price=5.0)
    with pytest.raises(IntegrityError):
        repo.add("Paracetamol 650mg", stock=50, unit_price=5.0)


def test_find_low_stock_filters_correctly(repo):
    repo.add("Insulin Glargine", stock=8, unit_price=45.0)
    repo.add("Atorvastatin 20mg", stock=45, unit_price=15.0)
    repo.add("Epinephrine 1mg", stock=4, unit_price=60.0)
    repo.add("Metformin 500mg", stock=120, unit_price=8.0)

    low_stock = repo.find_low_stock(threshold=10)
    names = [m.name for m in low_stock]

    assert len(low_stock) == 2
    assert "Epinephrine 1mg" in names
    assert "Insulin Glargine" in names
    assert low_stock[0].stock <= low_stock[1].stock


def test_update_stock_reduces_inventory(repo):
    med = repo.add("Azithromycin 250mg", stock=80, unit_price=22.0)
    updated = repo.update_stock(med.id, quantity_delta=-25)
    assert updated.stock == 55

    re_fetched = repo.get_by_id(med.id)
    assert re_fetched.stock == 55


def test_update_stock_insufficient_raises_error(repo):
    med = repo.add("Morphine 10mg/mL", stock=5, unit_price=35.0)
    with pytest.raises(ValueError, match="Insufficient stock"):
        repo.update_stock(med.id, quantity_delta=-10)

    assert repo.get_by_id(med.id).stock == 5


def test_database_isolation_between_tests(repo):
    all_meds = repo.find_low_stock(threshold=1000)
    assert len(all_meds) == 0
