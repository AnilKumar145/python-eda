"""
Test suite for Lab 1 Easy: Patient Allergy Cross-Reference & Eager Loading Hub
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution.solution import PatientAllergyService, Patient, Allergen


@pytest.fixture
def session_fixture():
    engine = create_engine("sqlite:///:memory:", echo=False)
    service = PatientAllergyService()
    service.initialize_schema(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    with Session() as session:
        yield service, session
    engine.dispose()


def test_allergy_registration_and_linking(session_fixture):
    service, session = session_fixture
    service.record_allergen(session, "Penicillin", "DRUG")
    service.record_allergen(session, "Peanuts", "FOOD")
    service.record_allergen(session, "Latex", "ENVIRONMENTAL")

    service.register_patient(session, "MRN-100", "Alice Smith")
    service.register_patient(session, "MRN-200", "Bob Jones")

    linked1 = service.link_allergy(session, "MRN-100", "Penicillin")
    linked2 = service.link_allergy(session, "MRN-100", "Latex")
    linked3 = service.link_allergy(session, "MRN-200", "Penicillin")
    assert linked1 and linked2 and linked3

    # Verify eager loading of patient allergies
    alice_allergies = service.get_patient_allergies_eager(session, "MRN-100")
    assert len(alice_allergies) == 2
    assert "Latex" in alice_allergies
    assert "Penicillin" in alice_allergies


def test_find_patients_by_allergen(session_fixture):
    service, session = session_fixture
    service.record_allergen(session, "Aspirin", "DRUG")
    service.register_patient(session, "MRN-301", "Charlie Brown")
    service.register_patient(session, "MRN-302", "David Miller")
    service.register_patient(session, "MRN-303", "Eve Adams")

    service.link_allergy(session, "MRN-301", "Aspirin")
    service.link_allergy(session, "MRN-303", "Aspirin")

    aspirin_patients = service.find_patients_allergic_to(session, "Aspirin")
    assert len(aspirin_patients) == 2
    names = [p.name for p in aspirin_patients]
    assert names == ["Charlie Brown", "Eve Adams"]  # Sorted alphabetically


def test_link_allergy_invalid_patient_or_allergen(session_fixture):
    service, session = session_fixture
    service.record_allergen(session, "Sulfa", "DRUG")
    service.register_patient(session, "MRN-500", "Fiona Gallagher")

    assert service.link_allergy(session, "MRN-INVALID", "Sulfa") is False
    assert service.link_allergy(session, "MRN-500", "NONEXISTENT") is False
