# Lab Level 1 Tasks: Hospital ER Patient Triage Dispatcher

## Task 1: TriageCase Data Structure
**Difficulty**: Easy
**Points**: 5

### Objective
Create a prioritized dataclass for ER patients.

### Requirements
- Decorate with `@dataclass(order=True)`.
- Fields:
  - `acuity_level: int` (primary sorting key, lower integer = higher urgency).
  - `patient_id: str = field(compare=False)`
  - `patient_name: str = field(compare=False)`
  - `condition: str = field(compare=False)`

---

## Task 2: Admission & Dispatcher Core
**Difficulty**: Easy
**Points**: 10

### Objective
Implement `ERTriageDispatcher.admit_patient(case: TriageCase)`.

### Requirements
- Put the `TriageCase` onto internal `self.queue = queue.PriorityQueue()`.

---

## Task 3: Doctor Consumer Worker
**Difficulty**: Easy
**Points**: 15

### Objective
Implement `doctor_worker(doc_id: str)`.

### Requirements
- Loop pulling `case = self.queue.get()`.
- If `case is None`:
  - Call `self.queue.task_done()`.
  - Break out of loop.
- Otherwise:
  - Append record to `self.treated_records`: `(doc_id, case.acuity_level, case.patient_id)`.
  - Call `self.queue.task_done()`.

---

## Task 4: Coordination & Shutdown
**Difficulty**: Easy
**Points**: 10

### Objective
Implement `start_doctors(num_docs)` and `drain_and_shutdown()`.

### Requirements
- Spawn and start `num_docs` consumer threads running `doctor_worker`.
- In `drain_and_shutdown()`:
  - Call `self.queue.join()` to ensure all patient cases have been processed.
  - Put `None` onto `self.queue` for each active doctor thread.
  - Join all doctor threads.
