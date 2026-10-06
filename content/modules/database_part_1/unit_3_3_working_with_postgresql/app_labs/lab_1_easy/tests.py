"""
Verification Tests for Lab 1 Easy: Radiology DICOM Study Metadata Store
"""

from decimal import Decimal
import pytest

try:
    from solution.solution import RadiologyStudyStore
except (ImportError, ModuleNotFoundError):
    from starter_code import RadiologyStudyStore


def test_study_ingestion_and_rich_types():
    store = RadiologyStudyStore(":memory:")

    meta = {
        "institution": "St. Jude Hospital",
        "scanner_model": "Siemens SOMATOM Force",
        "slice_thickness_mm": 0.6,
        "kvp": 120
    }
    fee = Decimal("485.50")

    store.record_study(
        study_uid="1.2.840.113619.2.55.1",
        patient_mrn="MRN-8801",
        modality="CT",
        study_date="2026-03-01 14:30:00",
        fee=fee,
        metadata=meta,
        findings="Mild atelectasis in right lower lobe."
    )

    study = store.get_study("1.2.840.113619.2.55.1")
    assert study is not None
    assert study["patient_mrn"] == "MRN-8801"
    assert study["fee_amount"] == fee
    assert isinstance(study["fee_amount"], Decimal)
    assert study["dicom_metadata"]["kvp"] == 120
    assert study["findings"] == "Mild atelectasis in right lower lobe."

    store.close()


def test_null_findings_coalesce_fallback():
    store = RadiologyStudyStore(":memory:")

    meta = {"institution": "General Hospital", "field_strength_tesla": 3.0}
    fee = Decimal("850.00")

    # Ingest study with NULL findings (in progress)
    store.record_study(
        study_uid="1.2.840.113619.2.55.2",
        patient_mrn="MRN-8802",
        modality="MRI",
        study_date="2026-03-02 09:15:00",
        fee=fee,
        metadata=meta,
        findings=None
    )

    studies = store.list_studies_by_modality("MRI")
    assert len(studies) == 1
    assert studies[0]["findings_status"] == "[PENDING RADIOLOGIST REVIEW]"
    assert studies[0]["fee_amount"] == fee

    store.close()
