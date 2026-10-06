"""
Test suite for Lab 1 Easy: Inpatient Bed Allocation & Ward Registry
"""

import pytest
from sqlalchemy import create_engine, inspect
from solution.solution import WardRegistryService, Ward, Bed, HospitalBase


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    yield engine
    engine.dispose()


def test_schema_initialization(test_engine):
    service = WardRegistryService()
    service.initialize_schema(test_engine)

    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    assert "wards" in tables, "Table 'wards' must exist"
    assert "beds" in tables, "Table 'beds' must exist"

    ward_cols = {c["name"] for c in inspector.get_columns("wards")}
    assert {"id", "name", "floor", "capacity"}.issubset(ward_cols)


def test_allocate_ward_within_capacity(test_engine):
    service = WardRegistryService()
    service.initialize_schema(test_engine)

    bed_labels = ["ICU-101", "ICU-102", "ICU-103", "ICU-104"]
    ward = service.allocate_ward("Intensive Care", 3, 5, bed_labels)

    assert ward.name == "Intensive Care"
    assert ward.floor == 3
    assert ward.capacity == 5
    assert len(ward.beds) == 4
    assert ward.beds[0].bed_label == "ICU-101"
    assert ward.beds[0].ward is ward
    assert ward.beds[0].is_occupied is False


def test_allocate_ward_exceeding_capacity_raises_error():
    service = WardRegistryService()
    with pytest.raises(ValueError, match="exceeds capacity"):
        service.allocate_ward("Pediatrics", 2, 2, ["PED-1", "PED-2", "PED-3"])
