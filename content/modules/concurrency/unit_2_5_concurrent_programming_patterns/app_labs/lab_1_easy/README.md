---
title: "Fan-Out / Fan-In Diagnostic Telemetry Aggregator"
type: app_lab
module: concurrency
unit: unit_2_5_concurrent_programming_patterns
lab_number: 1
difficulty: easy
use_case: fan_out_fan_in_diagnostics
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - concurrency
    - patterns
  subtopics:
    - fan-out-fan-in
    - worker-pool
    - immutability
    - exception-shielding
---

# Lab Level 1: Fan-Out / Fan-In Diagnostic Telemetry Aggregator
**Module**: Concurrency
**Objective**: Build a robust Fan-Out / Fan-In patient diagnostics aggregator combining EHR records, lab pathology, and bedside telemetry safely.
**Difficulty**: Easy
**Context**: Hospital Clinical Decision Support System

## Generic Information
**Problem Statement**: When an emergency physician assesses a trauma patient, critical clinical data resides across isolated hospital subsystems: Electronic Health Records (EHR), Pathology Laboratory Information System (LIS), and Bedside Cardiac Telemetry. Fetching these three endpoints sequentially delays critical care recommendations. The system must fan-out requests across a bounded worker pool concurrently, shield against upstream subsystem failures without crashing the entire query, and fan-in the results into an immutable composite patient report.
**Goals**:
- Implement a thread pool fan-out dispatcher querying multiple subsystems in parallel.
- Handle partial upstream subsystem errors gracefully (exception shielding).
- Synthesize an immutable composite patient report.
**Data Elements**:
- `patient_id` (str): Unique patient record identifier.
- `ehr_record` (dict): Medical history and allergies.
- `lab_results` (dict): Blood chemistry and troponin levels.
- `telemetry` (dict): Real-time pulse and oxygen saturation.

## Use Case
**Title**: Aggregate Patient Diagnostics via Fan-Out / Fan-In
**Description**: Query three clinical services concurrently for a patient. Even if one service raises a connection error or times out, return the healthy components and an error flag for the degraded service.

### Rules
- Dispatches must execute concurrently using a `ThreadPoolExecutor`.
- All partial subsystem failures must be caught and shielded into an error dictionary (`{"error": str(exc)}`).
- Data returned must be structured in a composite dictionary.

### Test Cases
- Case 1: All three services respond successfully; verify aggregation speedup and data completeness.
- Case 2: One service encounters a database timeout; verify partial result contains the error flag and other services are preserved.

### Success Criteria
- Concurrency speedup verified.
- Fault isolation: individual subsystem failures do not propagate or fail the caller.
- Clean thread shutdown.

## Overview
You will implement `DiagnosticAggregator` in `starter_code.py`.

## Learning Goals
- Apply the Fan-Out / Fan-In pattern using `ThreadPoolExecutor`.
- Implement exception shielding to protect distributed aggregation flows.
- Structure concurrent pipeline code cleanly.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement methods in `starter_code.py`.
3. Run `python tests.py` to verify functionality.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Implement `aggregate_patient_profile(patient_id, services, max_workers)`.
