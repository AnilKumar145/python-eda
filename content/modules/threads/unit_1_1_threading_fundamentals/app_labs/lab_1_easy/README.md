---
title: "Bedside Monitor Telemetry Ingestion"
type: app_lab
module: threads
unit: unit_1_1_threading_fundamentals
lab_number: 1
difficulty: easy
use_case: bedside_telemetry_ingestion
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - thread-instantiation
    - thread-coordination
    - non-blocking-io
    - join-synchronization
---

# Lab Level 1: Bedside Monitor Telemetry Ingestion
**Module**: Threads
**Objective**: Build a multi-threaded telemetry ingestion worker for healthcare bedside patient monitors.
**Difficulty**: Easy
**Context**: Healthcare Intensive Care Unit (ICU)

## Generic Information
**Problem Statement**: In an ICU, bedside monitors (Heart Rate, SPO2, Blood Pressure) broadcast telemetry data over network channels. If an ingestion system reads from each bedside monitor sequentially, a slow connection to one monitor blocks the ingestion of all other patients' vital signs, jeopardizing emergency alerts.
**Goals**:
- Concurrently ingest vital sign streams from multiple bedside monitors.
- Maintain independent execution paths so one slow monitor does not delay other monitors.
- Gather all patient telemetry into an aggregated clinic observation batch.
**Data Elements**:
- `device_id` (str): Unique hardware identifier (e.g., "BED-01-ECG").
- `patient_id` (str): Unique patient medical record number.
- `reading_type` (str): Vital category ("heart_rate", "spo2", "blood_pressure").
- `value` (float/str): Clinical sensor reading.
- `timestamp` (float): Epoch seconds of observation.

## Use Case
**Title**: Ingest Bedside Patient Telemetry
**Description**: Spawn dedicated worker threads to fetch sensor observations from multiple bedside monitors simultaneously, verify each monitor responds, and synthesize a unified patient status payload.

### Rules
- Each bedside monitor must be queried via an independent `threading.Thread`.
- The main thread must coordinate and join all worker threads before finalizing the observation report.
- The system must capture simulated network latency without freezing other sensor reads.

### Test Cases
- Case 1: Ingest 3 responsive bedside monitors concurrently, completing within the duration of the slowest single monitor.
- Case 2: Ingest from an empty monitor list returning an empty telemetry map.
- Case 3: Verify that worker threads are cleanly joined and inactive upon task completion.

### Success Criteria
- Total ingestion time is approximately equal to the maximum latency among monitors, not the sum of latencies.
- All telemetry records are accurately mapped into the aggregate result dictionary.
- No dangling or unjoined worker threads remain.

## Overview
This foundational lab focuses on applying `threading.Thread` and `.join()` to an enterprise healthcare ingestion scenario. You will implement the monitor reading logic, dispatch concurrent workers, and aggregate vital sign telemetry.

## Learning Goals
- Instantiate worker threads targeting network reading handlers.
- Pass device configurations and output references via thread arguments.
- Coordinate multiple threads using list tracking and synchronized joins.
- Measure elapsed time to verify concurrent versus sequential performance.

## The Scenario
St. Jude Medical Center operates a telemetry gateway. Every 5 seconds, the central gateway polls bedside monitors in Room 301. Currently, sequential polling takes 4.5 seconds across 3 monitors. You are tasked with migrating the polling gateway to multithreaded execution, reducing round-trip latency to under 2 seconds.

## What You'll Build
You will implement `TelemetryIngestionEngine`, a class that accepts a list of monitor configurations, launches worker threads to poll each monitor, and returns an aggregated telemetry payload.

## How to Use This Lab
1. **Read** this `README.md` for scenario and design rules.
2. **Review** `tasks.md` for task step details.
3. **Open** `starter_code.py` and implement tasks marked with `# WRITE CODE HERE`.
4. **Run** `python tests.py` to validate your solution.
5. **Compare** with `solution/solution.py` upon passing.

## Task Summary
- Task 1: Implement `simulate_monitor_read(device_id, latency, value)`
- Task 2: Implement `TelemetryIngestionEngine.poll_monitors_concurrently(monitors)`
- Task 3: Validate execution time reflects concurrent overlap

## Time Estimate
- Reading & planning: 10 minutes
- Implementation: 45 minutes
- Testing & verification: 15 minutes
- **Total**: ~1-1.5 hours

## Success Criteria
- [ ] All 3 tasks implemented in `starter_code.py`
- [ ] `tests.py` passes 100% of test cases
- [ ] Total batch duration is less than 60% of the sequential sum of delays
