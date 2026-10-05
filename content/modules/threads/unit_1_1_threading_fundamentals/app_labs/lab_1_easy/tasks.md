# Lab Level 1 Tasks: Bedside Monitor Telemetry Ingestion

## Task 1: Simulated Monitor Reading Function
**Difficulty**: Easy
**Points**: 10

### Objective
Create a function that simulates the network latency of polling a hardware monitor and populates an observation payload.

### Requirements
- Function signature: `read_sensor(device_id: str, latency: float, value: float, output_dict: dict) -> None`
- Sleep for `latency` seconds using `time.sleep()`.
- Insert a record into `output_dict[device_id]` formatted as:
  ```python
  {
      "device_id": device_id,
      "value": value,
      "timestamp": time.time()
  }
  ```

---

## Task 2: Concurrent Telemetry Engine
**Difficulty**: Easy
**Points**: 20

### Objective
Implement `TelemetryIngestionEngine.poll_monitors()` to dispatch worker threads for every configured monitor and wait for all to complete.

### Requirements
- Method signature: `poll_monitors(self, monitor_configs: list) -> dict`
- Input `monitor_configs` is a list of tuples: `[(device_id, latency, value), ...]`
- For each monitor:
  - Instantiate a `threading.Thread` targeting `read_sensor`.
  - Pass the tuple items and shared results dictionary via `args`.
  - Assign a descriptive name to the thread: `f"Poller-{device_id}"`.
  - Call `.start()` to initiate execution.
- Maintain a list of all thread objects.
- Iterate over the thread list and call `.join()` on each thread.
- Return the dictionary of aggregated monitor observations.
