# Lab Level 1 Tasks: Multi-Service Clinical Diagnostics Aggregator

## Task 1: Engine Initialization
**Difficulty**: Easy
**Points**: 5

### Objective
Initialize `ClinicalDiagnosticsAggregator` with a configurable `max_workers` thread pool size.

### Requirements
- Store `self.max_workers = max_workers` (default 4).

---

## Task 2: Parallel Diagnostic Aggregation
**Difficulty**: Easy
**Points**: 25

### Objective
Implement `aggregate_patient_record(patient_id: str, service_queries: dict) -> dict`.

### Requirements
- `service_queries` is a dict mapping `service_name: str -> callable(patient_id) -> dict`.
- Use `with ThreadPoolExecutor(max_workers=self.max_workers) as executor:`
- Submit each callable: `executor.submit(func, patient_id)`.
- Maintain a dictionary mapping each `Future` to its `service_name`.
- Iterate through futures using `concurrent.futures.as_completed(future_map)`.
- For each future:
  - If `future.result()` succeeds:
    - Set `results[service_name] = {"status": "SUCCESS", "data": future.result()}`.
  - If `future.result()` raises an Exception `exc`:
    - Set `results[service_name] = {"status": "FAILED", "error": str(exc)}`.
- Return the consolidated `results` dictionary.
