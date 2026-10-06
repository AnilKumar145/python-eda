"""
Unit 5.7 Exercises: Test Coverage and Best Practices (Student Starter)

Follow instructions and complete the TODOs.
"""

from typing import List, Set, Dict
import pytest


def classify_triage_acuity(systolic_bp: int, heart_rate: int, oxygen_sat: int) -> str:
    """
    TODO: Implement triage acuity classification:
    - Validate vitals within physiological limits:
        - 20 <= systolic_bp <= 300 (else ValueError)
        - 20 <= heart_rate <= 300 (else ValueError)
        - 50 <= oxygen_sat <= 100 (else ValueError)
    - Resuscitation ("RED_RESUSCITATION"): systolic_bp < 90 OR heart_rate > 130 OR oxygen_sat < 90
    - Emergent ("ORANGE_EMERGENT"): systolic_bp < 100 OR heart_rate > 110 OR oxygen_sat < 94
    - Urgent ("YELLOW_URGENT"): systolic_bp > 180 OR heart_rate > 100
    - Non-urgent ("GREEN_NON_URGENT"): all normal vitals
    """
    raise NotImplementedError("TODO: Implement classify_triage_acuity")


class AuditLogTrail:
    """
    TODO: Implement AuditLogTrail:
    - __init__: initialize self.entries as empty list
    - record_action(user_id, action, patient_id):
        Validate all 3 fields non-empty strings (raise ValueError if empty).
        Append normalized entry dict: {"user_id": ..., "action": ..., "patient_id": ...}
    - get_actions_for_patient(patient_id): return list of matching entries
    - has_unauthorized_access(patient_id, authorized_users): return True if any access from user not in authorized_users
    """
    def __init__(self):
        self.entries: List[Dict[str, str]] = []

    def record_action(self, user_id: str, action: str, patient_id: str) -> Dict[str, str]:
        raise NotImplementedError("TODO: Implement record_action")

    def get_actions_for_patient(self, patient_id: str) -> List[Dict[str, str]]:
        raise NotImplementedError("TODO: Implement get_actions_for_patient")

    def has_unauthorized_access(self, patient_id: str, authorized_users: Set[str]) -> bool:
        raise NotImplementedError("TODO: Implement has_unauthorized_access")


# =====================================================================
# Branch-Covering Test Suites
# =====================================================================

@pytest.mark.parametrize("bp,hr,o2,err_msg", [
    (10, 80, 98, "Invalid systolic blood pressure"),
    (320, 80, 98, "Invalid systolic blood pressure"),
    (120, 15, 98, "Invalid heart rate"),
    (120, 310, 98, "Invalid heart rate"),
    (120, 80, 45, "Invalid oxygen saturation"),
    (120, 80, 105, "Invalid oxygen saturation"),
])
def test_triage_acuity_invalid_vitals_raises_value_error(bp, hr, o2, err_msg):
    with pytest.raises(ValueError, match=err_msg):
        classify_triage_acuity(bp, hr, o2)


def test_triage_acuity_red_low_bp():
    assert classify_triage_acuity(85, 80, 98) == "RED_RESUSCITATION"


def test_triage_acuity_red_high_hr():
    assert classify_triage_acuity(120, 135, 98) == "RED_RESUSCITATION"


def test_triage_acuity_red_low_o2():
    assert classify_triage_acuity(120, 80, 88) == "RED_RESUSCITATION"


def test_triage_acuity_orange_borderline_bp():
    assert classify_triage_acuity(95, 80, 98) == "ORANGE_EMERGENT"


def test_triage_acuity_orange_borderline_hr():
    assert classify_triage_acuity(120, 115, 98) == "ORANGE_EMERGENT"


def test_triage_acuity_orange_borderline_o2():
    assert classify_triage_acuity(120, 80, 92) == "ORANGE_EMERGENT"


def test_triage_acuity_yellow_hypertensive():
    assert classify_triage_acuity(190, 80, 98) == "YELLOW_URGENT"


def test_triage_acuity_yellow_elevated_hr():
    assert classify_triage_acuity(120, 105, 98) == "YELLOW_URGENT"


def test_triage_acuity_green_normal():
    assert classify_triage_acuity(120, 75, 98) == "GREEN_NON_URGENT"


def test_audit_log_record_and_query():
    audit = AuditLogTrail()
    audit.record_action("dr_smith", "view_chart", "P-100")
    audit.record_action("nurse_joy", "administer_med", "P-100")
    audit.record_action("dr_smith", "view_chart", "P-200")

    p100_entries = audit.get_actions_for_patient("P-100")
    assert len(p100_entries) == 2
    assert p100_entries[0]["action"] == "VIEW_CHART"
    assert p100_entries[1]["action"] == "ADMINISTER_MED"


@pytest.mark.parametrize("uid,action,pid", [
    ("", "VIEW_CHART", "P-100"),
    ("dr_smith", "", "P-100"),
    ("dr_smith", "VIEW_CHART", ""),
])
def test_audit_log_empty_fields_raises_error(uid, action, pid):
    audit = AuditLogTrail()
    with pytest.raises(ValueError, match="All fields are required"):
        audit.record_action(uid, action, pid)


def test_audit_log_unauthorized_access_detected():
    audit = AuditLogTrail()
    audit.record_action("dr_smith", "view_chart", "P-100")
    audit.record_action("unknown_user", "export_records", "P-100")

    authorized = {"dr_smith", "nurse_joy"}
    assert audit.has_unauthorized_access("P-100", authorized) is True


def test_audit_log_all_accesses_authorized():
    audit = AuditLogTrail()
    audit.record_action("dr_smith", "view_chart", "P-100")
    audit.record_action("nurse_joy", "administer_med", "P-100")

    authorized = {"dr_smith", "nurse_joy"}
    assert audit.has_unauthorized_access("P-100", authorized) is False


def test_audit_log_no_records_returns_false_for_unauthorized():
    audit = AuditLogTrail()
    assert audit.has_unauthorized_access("P-999", {"dr_smith"}) is False
