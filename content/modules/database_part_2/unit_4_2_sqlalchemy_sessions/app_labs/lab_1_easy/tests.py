"""
Test suite for Lab 1 Easy: Surgical Schedule & Operating Theatre Dispatcher
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution.solution import SurgicalDispatchService, SurgicalCase, OperatingTheatre


@pytest.fixture
def session_fixture():
    engine = create_engine("sqlite:///:memory:", echo=False)
    service = SurgicalDispatchService()
    service.initialize_schema(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    with Session() as session:
        yield service, session
    engine.dispose()


def test_theatre_registration_and_scheduling(session_fixture):
    service, session = session_fixture
    theatre = service.register_theatre(session, "OT-CAR-1", "Cardiovascular")
    assert theatre.id > 0
    assert theatre.code == "OT-CAR-1"

    case_id = service.schedule_case(
        session, "OT-CAR-1", "MRN-303", "Dr. Burke", "Coronary Artery Bypass", 240
    )
    assert case_id > 0

    active_cases = service.get_active_cases_for_theatre(session, "OT-CAR-1")
    assert len(active_cases) == 1
    assert active_cases[0].lead_surgeon == "Dr. Burke"
    assert active_cases[0].status == "SCHEDULED"


def test_status_update_and_active_filtering(session_fixture):
    service, session = session_fixture
    service.register_theatre(session, "OT-NEURO-2", "Neurosurgery")

    case1 = service.schedule_case(session, "OT-NEURO-2", "MRN-404", "Dr. Shepherd", "Craniotomy", 300)
    case2 = service.schedule_case(session, "OT-NEURO-2", "MRN-505", "Dr. Nelson", "Biopsy", 90)

    # Both active initially
    assert len(service.get_active_cases_for_theatre(session, "OT-NEURO-2")) == 2

    # Mark case1 as COMPLETED
    updated = service.update_case_status(session, case1, "COMPLETED")
    assert updated is True

    # Only case2 should remain in active query
    active = service.get_active_cases_for_theatre(session, "OT-NEURO-2")
    assert len(active) == 1
    assert active[0].id == case2


def test_schedule_nonexistent_theatre_raises_error(session_fixture):
    service, session = session_fixture
    with pytest.raises(ValueError, match="not found"):
        service.schedule_case(session, "NONEXISTENT", "MRN-999", "Dr. Nick", "Appendectomy", 60)
