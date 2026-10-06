# Lab 1 Tasks: Secure Clinical Prescription Audit Ledger

## Task 1: Schema & Parameterized Queries
- In `PrescriptionAuditLedger`:
  - `_init_schema()`:
    - Create table `consultation_events` (`event_id INTEGER PRIMARY KEY AUTOINCREMENT`, `patient_mrn TEXT NOT NULL`, `doctor_id TEXT NOT NULL`, `notes TEXT NOT NULL`, `created_at TEXT NOT NULL`).
    - Create table `prescriptions` (`rx_id INTEGER PRIMARY KEY AUTOINCREMENT`, `event_id INTEGER NOT NULL`, `drug_name TEXT NOT NULL`, `dosage_mg INTEGER NOT NULL`, `is_narcotic INTEGER NOT NULL`, `FOREIGN KEY (event_id) REFERENCES consultation_events(event_id)`).
  - Implement `search_consultations_by_patient(mrn_query: str) -> List[Dict[str, Any]]`:
    - MUST use parameterized binding `?`.

## Task 2: Savepoint-Guarded Prescription Processing
- Implement `record_consultation_with_prescriptions(patient_mrn: str, doctor_id: str, notes: str, created_at: str, rx_items: List[Tuple[str, int, bool]]) -> Tuple[int, int]`:
  - Step 1: Insert row into `consultation_events` and obtain `event_id`.
  - Step 2: Establish `SAVEPOINT rx_checkpoint;`.
  - Step 3: Iterate `rx_items` (`drug_name`, `dosage_mg`, `is_narcotic`).
    - If `is_narcotic` is True and `dosage_mg > 100`:
      - Rollback to `rx_checkpoint`.
      - Record warning note or mark prescriptions rejected.
      - Release savepoint and commit `consultation_events`.
      - Return `(event_id, 0)` (0 prescriptions added).
    - Else insert into `prescriptions`.
  - Step 4: Release savepoint, commit, and return `(event_id, len(rx_items))`.

## Task 3: Resource Cleanup Context Manager
- Implement `__enter__` and `__exit__` on `PrescriptionAuditLedger` ensuring `self.conn.close()` is called on exit.
