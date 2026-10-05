# Lab Level 1 Tasks: ICU Patient Telemetry Watchdog Supervisor

## Task 1: TelemetryWorker Class
**Difficulty**: Easy
**Points**: 10

### Objective
Create a custom `threading.Thread` that polls telemetry until a shared shutdown event is triggered.

### Requirements
- Inherit from `threading.Thread`.
- `__init__(patient_id: str, stop_event: threading.Event)`
  - Call `super().__init__(name=f"Telemetry-{patient_id}", daemon=False)`.
  - Store `patient_id` and `stop_event`.
  - Initialize `self.iterations = 0`.
- In `run()`:
  - Loop while `not self.stop_event.is_set()`:
    - Increment `self.iterations += 1`.
    - Wait on `self.stop_event.wait(0.05)`.

---

## Task 2: Supervisor Active Patient Discovery
**Difficulty**: Easy
**Points**: 10

### Objective
Implement `ICUWatchdogSupervisor.get_active_telemetry_patients()` using `threading.enumerate()`.

### Requirements
- Method signature: `get_active_telemetry_patients(self) -> List[str]`
- Inspect threads returned by `threading.enumerate()`.
- Filter for threads where `t.name.startswith("Telemetry-")` and `t.is_alive()`.
- Extract the `patient_id` (the portion of name after `"Telemetry-"`).
- Return a sorted list of active patient IDs.

---

## Task 3: Graceful Shutdown Orchestrator
**Difficulty**: Easy
**Points**: 10

### Objective
Implement `ICUWatchdogSupervisor.shutdown_all(timeout: float)` to stop and join all workers.

### Requirements
- Set the shared `stop_event.set()`.
- Iterate through all managed workers and call `worker.join(timeout=timeout)`.
- Return a boolean indicating whether all workers terminated successfully (`True` if none are alive, `False` if any timed out).
