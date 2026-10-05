---
title: "Hospital ER Patient Triage Dispatcher"
type: app_lab
module: threads
unit: unit_1_4_thread_communication
lab_number: 1
difficulty: easy
use_case: hospital_er_triage_dispatcher
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - queue-module
    - priority-queue
    - producer-consumer
    - thread-safe-dispatch
---

# Lab Level 1: Hospital ER Patient Triage Dispatcher
**Module**: Threads
**Objective**: Build a thread-safe Emergency Room triage dispatching engine using `queue.PriorityQueue` and consumer worker threads.
**Difficulty**: Easy
**Context**: Healthcare Hospital Emergency Department

## Generic Information
**Problem Statement**: Hospital Emergency Departments receive patients with varying severity: cardiac arrests, trauma injuries, fractures, and minor fevers. Arriving patients cannot be treated on a strictly first-come-first-served basis; critical cases must preempt less severe conditions immediately. Furthermore, multiple attending ER physicians must pull cases from a centralized, thread-safe dispatch pipeline without race conditions or case duplication.
**Goals**:
- Prioritize incoming patient cases by clinical acuity using `queue.PriorityQueue`.
- Dispatch cases concurrently across multiple doctor consumer threads.
- Ensure all admitted patients are treated before shutting down the triage pipeline using `task_done()` and `join()`.
**Data Elements**:
- `acuity_level` (int): Triage score from 1 (Resuscitation) to 5 (Non-urgent).
- `patient_id` (str): Unique patient medical record number.
- `patient_name` (str): Full patient name.
- `condition` (str): Clinical presenting complaint.

## Use Case
**Title**: Prioritized ER Case Dispatching
**Description**: Triage nurses enqueue arriving patient assessments. A pool of attending physician threads continuously dequeues the highest-acuity waiting patient and renders care.

### Rules
- A patient with Acuity Level 1 must always be dequeued before Acuity Level 2 or higher, regardless of arrival timestamp.
- Each patient must be treated by exactly one physician.
- Pipeline completion must be validated via `queue.join()`.

### Test Cases
- Case 1: Out-of-order admissions are treated in strictly ascending acuity order (Level 1, then Level 2, then Level 3).
- Case 2: Multi-doctor consumers process 10 patients without dropping or duplicating any patient.
- Case 3: Pipeline shutdown is clean and leaves no hung worker threads.

### Success Criteria
- 100% of admitted patients are recorded in the treatment audit log.
- Acuity sorting is strictly maintained.
- Doctors cleanly terminate upon pipeline completion.

## Overview
In this lab, you will implement `ERTriageDispatcher`, which coordinates patient admission producers and physician consumers via `queue.PriorityQueue`.

## Learning Goals
- Use `queue.PriorityQueue` with custom prioritized dataclasses.
- Implement consumer thread worker loops with sentinel shutdowns.
- Track batch completion with `task_done()` and `join()`.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement code in `starter_code.py`.
3. Run `python tests.py` to verify implementation.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Create `@dataclass(order=True)` for `TriageCase`.
- Task 2: Implement `ERTriageDispatcher.admit_patient()`.
- Task 3: Implement `ERTriageDispatcher.doctor_worker()` and `start_physicians()`.
- Task 4: Coordinate pipeline drain and shutdown in `wait_for_completion()`.
