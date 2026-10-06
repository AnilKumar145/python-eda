# Lab 1 Tasks: Radiology DICOM Study Metadata Store

## Task 1: Schema Initialization
- In `RadiologyStudyStore.__init__(db_path=":memory:")`:
  - Connect to SQLite database.
  - Create table `imaging_studies`:
    - `study_uid TEXT PRIMARY KEY` (Unique DICOM Study UID)
    - `patient_mrn TEXT NOT NULL`
    - `modality TEXT NOT NULL` (e.g. "CT", "MRI", "XR")
    - `study_date TEXT NOT NULL`
    - `fee_amount TEXT NOT NULL` (Stored as string representation of Decimal)
    - `dicom_metadata TEXT NOT NULL` (Stored as JSON string)
    - `findings TEXT` (Nullable clinical findings report)
  - Create index on `imaging_studies(patient_mrn, modality)`.

## Task 2: Study Ingestion & Retrieval
- Implement `record_study(study_uid: str, patient_mrn: str, modality: str, study_date: str, fee: Decimal, metadata: Dict[str, Any], findings: Optional[str] = None) -> None`:
  - Serialize `fee` as string and `metadata` as JSON.
  - Insert record into `imaging_studies`.
- Implement `get_study(study_uid: str) -> Optional[Dict[str, Any]]`:
  - Query study by UID.
  - Return dictionary with deserialized `fee: Decimal`, `metadata: dict`, and `findings: Optional[str]`.

## Task 3: Modality Search & Null-Safe Reporting
- Implement `list_studies_by_modality(modality: str) -> List[Dict[str, Any]]`:
  - Query all studies for the modality ordered by `study_date DESC`.
  - Use SQL `COALESCE(findings, '[PENDING RADIOLOGIST REVIEW]')` to provide the report status.
  - Return formatted list of dicts.
