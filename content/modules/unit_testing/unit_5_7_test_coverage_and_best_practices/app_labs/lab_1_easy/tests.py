import importlib.util
import pathlib
import pytest

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_7_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

ClinicalAuditLedger = _sol.ClinicalAuditLedger
AuditRecord = _sol.AuditRecord



@pytest.fixture
def empty_ledger():
    return ClinicalAuditLedger()


@pytest.fixture
def populated_ledger(empty_ledger):
    empty_ledger.append_event("EVT-1", "dr_house", "PAT-10", "READ_EHR", "INFO")
    empty_ledger.append_event("EVT-2", "nurse_jackie", "PAT-10", "OVERRIDE_WARNING", "WARNING")
    empty_ledger.append_event("EVT-3", "unknown_ip", "PAT-10", "EXPORT_PHI", "CRITICAL")
    return empty_ledger


def test_empty_ledger_is_intact(empty_ledger):
    assert empty_ledger.verify_integrity() is True
    summary = empty_ledger.export_summary()
    assert summary["total_events"] == 0
    assert summary["is_intact"] is True


def test_append_event_genesis_hash_chain(empty_ledger):
    rec = empty_ledger.append_event("EVT-1", "dr_house", "PAT-10", "read_ehr", "info")
    assert rec.previous_hash == ClinicalAuditLedger.GENESIS_HASH
    assert rec.current_hash is not None
    assert rec.action == "READ_EHR"
    assert rec.severity == "INFO"
    assert len(empty_ledger.records) == 1


def test_append_second_event_chains_to_previous(empty_ledger):
    rec1 = empty_ledger.append_event("EVT-1", "dr_house", "PAT-10", "READ_EHR", "INFO")
    rec2 = empty_ledger.append_event("EVT-2", "dr_wilson", "PAT-10", "WRITE_PRESCRIPTION", "WARNING")

    assert rec2.previous_hash == rec1.current_hash
    assert empty_ledger.verify_integrity() is True


@pytest.mark.parametrize("eid,actor,pid,action,sev", [
    ("", "dr_house", "PAT-10", "READ_EHR", "INFO"),
    ("EVT-1", "", "PAT-10", "READ_EHR", "INFO"),
    ("EVT-1", "dr_house", "", "READ_EHR", "INFO"),
    ("EVT-1", "dr_house", "PAT-10", "", "INFO"),
    ("EVT-1", "dr_house", "PAT-10", "READ_EHR", ""),
])
def test_append_event_empty_fields_raises_value_error(empty_ledger, eid, actor, pid, action, sev):
    with pytest.raises(ValueError, match="non-empty strings"):
        empty_ledger.append_event(eid, actor, pid, action, sev)


def test_append_event_invalid_severity_raises_value_error(empty_ledger):
    with pytest.raises(ValueError, match="Invalid severity"):
        empty_ledger.append_event("EVT-1", "dr_house", "PAT-10", "READ_EHR", "SUPER_CRITICAL")


def test_verify_integrity_passes_on_valid_ledger(populated_ledger):
    assert populated_ledger.verify_integrity() is True


def test_tamper_detection_modified_action(populated_ledger):
    # Alter second record action without recomputing hash
    populated_ledger.records[1].action = "TAMPERED_ACTION"
    assert populated_ledger.verify_integrity() is False


def test_tamper_detection_broken_previous_hash(populated_ledger):
    # Invalidate previous_hash link
    populated_ledger.records[2].previous_hash = "FORGED_PREVIOUS_HASH"
    assert populated_ledger.verify_integrity() is False


def test_find_critical_breaches(populated_ledger):
    breaches = populated_ledger.find_critical_breaches()
    assert len(breaches) == 1
    assert breaches[0].event_id == "EVT-3"
    assert breaches[0].severity == "CRITICAL"


def test_export_summary(populated_ledger):
    summary = populated_ledger.export_summary()
    assert summary["total_events"] == 3
    assert summary["severity_counts"]["INFO"] == 1
    assert summary["severity_counts"]["WARNING"] == 1
    assert summary["severity_counts"]["CRITICAL"] == 1
    assert summary["is_intact"] is True
