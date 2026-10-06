"""
Verification Tests for Lab 1 Easy: Hospital Patient Registry & Encounter Schema
"""

import pytest

try:
    from solution.solution import HospitalPatientRegistry
except (ImportError, ModuleNotFoundError):
    from starter_code import HospitalPatientRegistry


def test_patient_registration_and_encounters():
    registry = HospitalPatientRegistry(":memory:")

    p_id = registry.register_patient("MRN-1001", "Eleanor Vance", "1985-04-12")
    assert p_id > 0, "Patient ID should be a positive integer"

    e1 = registry.log_encounter(p_id, "2026-03-01", "Emergency", "Acute appendicitis")
    e2 = registry.log_encounter(p_id, "2026-03-05", "Surgery", "Post-op checkup")

    encounters = registry.get_patient_encounters(p_id)
    assert len(encounters) == 2, f"Expected 2 encounters, got {len(encounters)}"
    # Verify order DESC
    assert encounters[0]["encounter_date"] == "2026-03-05"
    assert encounters[1]["encounter_date"] == "2026-03-01"

    summary = registry.get_patient_summary("MRN-1001")
    assert summary is not None
    assert summary["full_name"] == "Eleanor Vance"

    registry.close()


def test_foreign_key_protection_orphan_encounter():
    registry = HospitalPatientRegistry(":memory:")

    with pytest.raises(ValueError) as excinfo:
        registry.log_encounter(99999, "2026-03-02", "ICU", "Non-existent patient encounter")

    assert "Invalid encounter reference" in str(excinfo.value)
    registry.close()


def test_index_creation():
    registry = HospitalPatientRegistry(":memory:")
    cursor = registry.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='encounters';")
    indexes = [row[0] for row in cursor.fetchall()]

    assert "idx_encounters_patient_date" in indexes, "Composite index must be created"
    registry.close()
