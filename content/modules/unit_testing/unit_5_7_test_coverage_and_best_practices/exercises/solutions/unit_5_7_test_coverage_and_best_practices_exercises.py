"""
Unit 5.7 Exercises: Test Coverage and Best Practices (Reference Solutions)
"""

from typing import List, Set, Dict
import pytest


def classify_triage_acuity(systolic_bp: int, heart_rate: int, oxygen_sat: int) -> str:
    """
    Classifies emergency patient acuity based on vital signs.
    """
    if not (20 <= systolic_bp <= 300):
        raise ValueError(f"Invalid systolic blood pressure: {systolic_bp}")
    if not (20 <= heart_rate <= 300):
        raise ValueError(f"Invalid heart rate: {heart_rate}")
    if not (50 <= oxygen_sat <= 100):
        raise ValueError(f"Invalid oxygen saturation: {oxygen_sat}")

    if systolic_bp < 90 or heart_rate > 130 or oxygen_sat < 90:
        return "RED_RESUSCITATION"
    elif systolic_bp < 100 or heart_rate > 110 or oxygen_sat < 94:
        return "ORANGE_EMERGENT"
    elif systolic_bp > 180 or heart_rate > 100:
        return "YELLOW_URGENT"
    else:
        return "GREEN_NON_URGENT"


class AuditLogTrail:
    """
    In-memory audit log accumulator for clinical compliance tracking.
    """
    def __init__(self):
        self.entries: List[Dict[str, str]] = []

    def record_action(self, user_id: str, action: str, patient_id: str) -> Dict[str, str]:
        if not user_id or not action or not patient_id:
            raise ValueError("All fields are required and must be non-empty.")
        entry = {
            "user_id": user_id.strip(),
            "action": action.strip().upper(),
            "patient_id": patient_id.strip()
        }
        self.entries.append(entry)
        return entry

    def get_actions_for_patient(self, patient_id: str) -> List[Dict[str, str]]:
        pid = patient_id.strip()
        return [e for e in self.entries if e["patient_id"] == pid]

    def has_unauthorized_access(self, patient_id: str, authorized_users: Set[str]) -> bool:
        patient_entries = self.get_actions_for_patient(patient_id)
        for entry in patient_entries:
            if entry["user_id"] not in authorized_users:
                return True
        return False


# =====================================================================
# Branch-Covering Test Suites
# =====================================================================

# Physiological Range Validation
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


# Red Resuscitation compound branches
def test_triage_acuity_red_low_bp():
    assert classify_triage_acuity(85, 80, 98) == "RED_RESUSCITATION"


def test_triage_acuity_red_high_hr():
    assert classify_triage_acuity(120, 135, 98) == "RED_RESUSCITATION"


def test_triage_acuity_red_low_o2():
    assert classify_triage_acuity(120, 80, 88) == "RED_RESUSCITATION"


# Orange Emergent compound branches
def test_triage_acuity_orange_borderline_bp():
    assert classify_triage_acuity(95, 80, 98) == "ORANGE_EMERGENT"


def test_triage_acuity_orange_borderline_hr():
    assert classify_triage_acuity(120, 115, 98) == "ORANGE_EMERGENT"


def test_triage_acuity_orange_borderline_o2():
    assert classify_triage_acuity(120, 80, 92) == "ORANGE_EMERGENT"


# Yellow Urgent compound branches
def test_triage_acuity_yellow_hypertensive():
    assert classify_triage_acuity(190, 80, 98) == "YELLOW_URGENT"


def test_triage_acuity_yellow_elevated_hr():
    assert classify_triage_acuity(120, 105, 98) == "YELLOW_URGENT"


# Green Non-Urgent
def test_triage_acuity_green_normal():
    assert classify_triage_acuity(120, 75, 98) == "GREEN_NON_URGENT"


# Audit Log Tests
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
