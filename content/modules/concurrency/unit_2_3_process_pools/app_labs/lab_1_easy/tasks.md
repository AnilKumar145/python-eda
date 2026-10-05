# Lab Level 1 Tasks: Parallel ECG Arrhythmia Signal Analyzer

## Task 1: Top-Level Signal Worker
**Difficulty**: Easy
**Points**: 10

### Objective
Implement `process_lead_signal(lead_data: tuple) -> dict`.

### Requirements
- Input is a tuple: `(lead_id: str, voltages: list)`.
- If `not voltages`:
  - Return `{"lead_id": lead_id, "status": "EMPTY", "peak": 0.0, "mean": 0.0}`.
- Otherwise:
  - Compute `peak = round(max(voltages), 2)`.
  - Compute `mean = round(sum(voltages) / len(voltages), 2)`.
  - Return `{"lead_id": lead_id, "status": "SUCCESS", "peak": peak, "mean": mean}`.

---

## Task 2: Process Pool Analyzer Engine
**Difficulty**: Easy
**Points**: 20

### Objective
Implement `ECGSignalProcessor.analyze_leads(lead_batch: list) -> list`.

### Requirements
- Use `with ProcessPoolExecutor(max_workers=self.max_workers) as executor:`
- Execute `list(executor.map(process_lead_signal, lead_batch))`
- Return the list of metric dictionaries.
