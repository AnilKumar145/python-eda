---
title: "Multi-Service Clinical Diagnostics Aggregator"
type: app_lab
module: threads
unit: unit_1_5_thread_pools
lab_number: 1
difficulty: easy
use_case: clinical_diagnostics_aggregator
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - thread-pool-executor
    - as-completed
    - future-objects
    - error-resilience
---

# Lab Level 1: Multi-Service Clinical Diagnostics Aggregator
**Module**: Threads
**Objective**: Build a high-performance clinical diagnostics aggregator using `ThreadPoolExecutor` and `as_completed()`.
**Difficulty**: Easy
**Context**: Hospital Inpatient Patient Portal

## Generic Information
**Problem Statement**: When an attending physician reviews an admitted patient's electronic health record, the dashboard must compile data from multiple disparate hospital systems: Laboratory Chemistry, Radiology PACS, Genomic Sequencing, and Pharmacy Orders. Calling each system sequentially takes over 4 seconds, causing noticeable UI lag. Furthermore, if the Genomic service is down, the entire dashboard must not fail—partial clinical results must still be rendered promptly.
**Goals**:
- Concurrently query multiple clinical microservice endpoints using `ThreadPoolExecutor`.
- Stream results as they arrive using `concurrent.futures.as_completed()`.
- Implement per-service error isolation so one failing or slow service does not crash the aggregator.
**Data Elements**:
- `patient_id` (str): Unique medical record number.
- `service_name` (str): Diagnostic service name ("Lab", "Radiology", "Pharmacy", "Genomics").
- `status` (str): "SUCCESS", "TIMEOUT", or "FAILED".
- `payload` (dict/str): Clinical diagnostic payload.

## Use Case
**Title**: Aggregate Patient Diagnostic Records
**Description**: Dispatch parallel queries to 4 simulated clinical services, aggregate completed findings, handle service timeouts and exceptions gracefully, and return a consolidated patient clinical chart.

### Rules
- Concurrency must be bounded by `max_workers=4`.
- If an endpoint raises an exception or times out, the service record must reflect `"FAILED"` without terminating the remaining queries.
- Completed responses must be gathered using `as_completed()`.

### Test Cases
- Case 1: All 4 services respond normally; total aggregation completes within the duration of the slowest service (~0.4s).
- Case 2: One service throws a simulated network failure; the other 3 services succeed, and the failed service is marked with error details.
- Case 3: Empty service list returns an empty aggregation map immediately.

### Success Criteria
- Total elapsed time is less than half the sum of sequential latencies.
- 100% of queried services are accounted for in the output payload.
- Zero uncaught exceptions terminate the aggregator.

## Overview
You will implement `ClinicalDiagnosticsAggregator`, a production-grade service aggregator using Python's `concurrent.futures` framework.

## Learning Goals
- Use `ThreadPoolExecutor` within a context manager.
- Map futures to service identifiers.
- Handle worker exceptions cleanly via `Future.result()`.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Complete `starter_code.py`.
3. Run `python tests.py` to verify thread pool concurrency and error isolation.
4. Compare with `solution/solution.py`.

## Task Summary
- Task 1: Implement `ClinicalDiagnosticsAggregator.__init__(max_workers)`.
- Task 2: Implement `aggregate_patient_record(patient_id, service_callables)`.
