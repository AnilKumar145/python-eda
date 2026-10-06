# Lab Tasks: Clinical Audit Log Quality Gate and Coverage Harness

## Task 1: Declare the Audit Record Data Model
Create dataclass `AuditRecord`:
- `event_id`: str
- `actor_id`: str
- `patient_id`: str
- `action`: str
- `severity`: str ("INFO", "WARNING", "CRITICAL")
- `previous_hash`: str
- `current_hash`: str

## Task 2: Implement Cryptographic Hashing & Ledger Methods
Implement `ClinicalAuditLedger`:
- `__init__()`: Initializes empty `records: List[AuditRecord]`.
- `compute_hash(event_id, actor_id, patient_id, action, severity, previous_hash) -> str`: Produces deterministic SHA-256 hex digest of the string concatenated with `|`.
- `append_event(event_id, actor_id, patient_id, action, severity) -> AuditRecord`:
  - Validates non-empty fields (raises `ValueError`).
  - Validates severity is one of `{"INFO", "WARNING", "CRITICAL"}` (raises `ValueError`).
  - Sets `previous_hash` to `"GENESIS_HASH"` if first entry, otherwise previous record's `current_hash`.
  - Computes `current_hash` and appends `AuditRecord`.
- `verify_integrity() -> bool`:
  - Iterates over records and verifies `current_hash` matches freshly recomputed hash.
  - Verifies `previous_hash` points to preceding record's `current_hash`.
  - Returns `True` if untampered; `False` if any hash mismatch is found.
- `find_critical_breaches() -> List[AuditRecord]`:
  - Returns records where `severity == "CRITICAL"`.
- `export_summary() -> Dict[str, Any]`:
  - Returns summary dictionary with counts of `INFO`, `WARNING`, `CRITICAL`, `total_events`, and `is_intact` boolean.

## Task 3: Author 100% Branch Coverage Test Suite
In `tests.py`, implement tests that verify:
1. Normal event addition and hash chaining.
2. Field validation exceptions (empty string for any field).
3. Invalid severity exception.
4. Tampering detection (modifying record action or hash breaks verification).
5. Critical breach filtering.
6. Summary export metrics.
