# Lab 1 Tasks: Fan-Out / Fan-In Diagnostic Telemetry Aggregator

Follow these instructions to implement the aggregator in `starter_code.py`.

---

### Task 1: Implement `DiagnosticAggregator.aggregate_patient_profile(patient_id, services, max_workers=3)`
1. Receive `services`: a dictionary mapping service names to callable query functions (e.g. `{"ehr": fn_ehr, "labs": fn_labs, "telemetry": fn_telemetry}`).
2. Inside `aggregate_patient_profile`:
   - Initialize a `ThreadPoolExecutor(max_workers=max_workers)`.
   - **Fan-Out**: Submit each service function call (`func(patient_id)`) to the executor. Map each future back to its service name.
   - **Fan-In & Exception Shielding**: Iterate over the completed futures (or dictionary items).
   - If a future raises an exception, catch it and set the service result to `{"error": str(exc), "status": "FAILED"}`.
   - If a future succeeds, record `{"data": result, "status": "SUCCESS"}`.
3. Return the composite profile:
   ```python
   {
       "patient_id": patient_id,
       "services": { ... }
   }
   ```
