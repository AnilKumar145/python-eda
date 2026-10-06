"""
Verification Tests for Lab 1 Easy: Secure Clinical Prescription Audit Ledger
"""

import pytest

try:
    from solution.solution import PrescriptionAuditLedger
except (ImportError, ModuleNotFoundError):
    from starter_code import PrescriptionAuditLedger


def test_sql_injection_defense():
    with PrescriptionAuditLedger(":memory:") as ledger:
        # Register normal consultation
        ledger.record_consultation_with_prescriptions(
            patient_mrn="MRN-001",
            doctor_id="DOC-99",
            notes="Regular cardiology checkup.",
            created_at="2026-03-01",
            rx_items=[("Metoprolol", 50, False)]
        )

        # Attempt SQL injection search attack
        injection_attack = "' OR '1'='1"
        results = ledger.search_consultations_by_patient(injection_attack)

        # Due to parameterization, must return 0 results (attack string treated as literal MRN)
        assert len(results) == 0, "SQL injection leaked unauthorized records!"

        # Legitimate search succeeds
        legit = ledger.search_consultations_by_patient("MRN-001")
        assert len(legit) == 1
        assert legit[0]["patient_mrn"] == "MRN-001"


def test_savepoint_rollback_on_narcotic_overdose():
    with PrescriptionAuditLedger(":memory:") as ledger:
        # Overdose narcotic prescription: Morphine 250mg (> 100mg threshold)
        event_id, accepted_count = ledger.record_consultation_with_prescriptions(
            patient_mrn="MRN-002",
            doctor_id="DOC-55",
            notes="Severe trauma patient.",
            created_at="2026-03-02",
            rx_items=[
                ("Acetaminophen", 500, False),
                ("Morphine", 250, True) # Exceeds limit
            ]
        )

        # Consultation event is preserved
        assert event_id > 0
        # Prescriptions rolled back to savepoint
        assert accepted_count == 0

        # Verify database state
        cursor = ledger.conn.cursor()
        cursor.execute("SELECT count(*) FROM consultation_events;")
        assert cursor.fetchone()[0] == 1, "Consultation record must be preserved"

        cursor.execute("SELECT count(*) FROM prescriptions;")
        assert cursor.fetchone()[0] == 0, "Prescriptions must be rolled back"


def test_valid_prescription_commit():
    with PrescriptionAuditLedger(":memory:") as ledger:
        event_id, accepted_count = ledger.record_consultation_with_prescriptions(
            patient_mrn="MRN-003",
            doctor_id="DOC-77",
            notes="Post-operative knee replacement.",
            created_at="2026-03-03",
            rx_items=[
                ("Cephalexin", 500, False),
                ("Oxycodone", 20, True) # Narcotic <= 100mg: allowed
            ]
        )

        assert event_id > 0
        assert accepted_count == 2

        cursor = ledger.conn.cursor()
        cursor.execute("SELECT count(*) FROM prescriptions WHERE event_id = ?;", (event_id,))
        assert cursor.fetchone()[0] == 2
