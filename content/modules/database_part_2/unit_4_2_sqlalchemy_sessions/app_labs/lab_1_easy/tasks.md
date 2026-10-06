# Tasks: Surgical Schedule & Operating Theatre Dispatcher

## Task 1: Define Declarative Schema
In `SurgicalBase`:
1. `OperatingTheatre`:
   - Table `theatres`: `id` (int PK), `code` (str unique, e.g. "OT-1"), `specialty` (str).
2. `SurgicalCase`:
   - Table `surgical_cases`: `id` (int PK), `theatre_id` (int FK to `theatres.id`), `patient_mrn` (str), `lead_surgeon` (str), `procedure_name` (str), `duration_minutes` (int), `status` (str, default "SCHEDULED").

## Task 2: Implement Surgical Dispatch Service
In `SurgicalDispatchService`:
- `initialize_schema(engine)`: Create tables.
- `register_theatre(session, code, specialty)`: Add theatre and commit.
- `schedule_case(session, theatre_code, mrn, surgeon, procedure, duration_mins)`:
  Find theatre by code. If theatre does not exist, raise `ValueError`. Create and add `SurgicalCase`, commit, and return case id.
- `update_case_status(session, case_id, new_status)`:
  Find case by id. If found, update status and commit. Return True if updated, False otherwise.
- `get_active_cases_for_theatre(session, theatre_code)`:
  Use a relational `join(OperatingTheatre)` query to return all cases for that theatre where status != "COMPLETED", sorted by `SurgicalCase.id` ascending.
