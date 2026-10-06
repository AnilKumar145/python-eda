# Lab 1 Tasks: Hospital Patient Registry & Encounter Schema

## Task 1: Schema Architecture Initialization
- In `HospitalPatientRegistry.__init__(db_path=":memory:")`:
  - Connect to SQLite database.
  - Enable foreign keys with `PRAGMA foreign_keys = ON;`.
  - Create table `patients`:
    - `patient_id INTEGER PRIMARY KEY`
    - `mrn TEXT NOT NULL UNIQUE` (Medical Record Number)
    - `full_name TEXT NOT NULL`
    - `dob TEXT NOT NULL`
  - Create table `encounters`:
    - `encounter_id INTEGER PRIMARY KEY`
    - `patient_id INTEGER NOT NULL`
    - `encounter_date TEXT NOT NULL`
    - `department TEXT NOT NULL`
    - `diagnosis TEXT NOT NULL`
    - `FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE`
  - Create index `idx_encounters_patient_date` on `encounters(patient_id, encounter_date)`.

## Task 2: Patient Registration & Encounter Logging
- Implement `register_patient(mrn: str, full_name: str, dob: str) -> int`:
  - Inserts patient row and returns generated `patient_id`.
- Implement `log_encounter(patient_id: int, encounter_date: str, department: str, diagnosis: str) -> int`:
  - Inserts encounter row and returns generated `encounter_id`.
  - If `patient_id` violates foreign key, raise `ValueError` or catch `IntegrityError` and raise `ValueError`.

## Task 3: Relational Querying
- Implement `get_patient_encounters(patient_id: int) -> List[Dict[str, Any]]`:
  - Returns list of encounter dictionaries ordered by `encounter_date DESC`.
- Implement `get_patient_summary(mrn: str) -> Optional[Dict[str, Any]]`:
  - Fetches patient details by MRN, or `None` if not found.
