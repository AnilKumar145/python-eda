---
title: "Asynchronous ICU Vital Signs Hub"
type: app_lab
module: concurrency
unit: unit_2_4_asynchronous_programming
lab_number: 1
difficulty: easy
use_case: async_icu_vital_hub
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - concurrency
    - asyncio
  subtopics:
    - async-await
    - gather
    - non-blocking-io
    - timeout-handling
---

# Lab Level 1: Asynchronous ICU Vital Signs Hub
**Module**: Concurrency
**Objective**: Build a high-throughput asynchronous patient telemetry gateway using `asyncio.gather()` and `asyncio.wait_for()`.
**Difficulty**: Easy
**Context**: Intensive Care Unit Digital Telemetry Hub

## Generic Information
**Problem Statement**: In a hospital intensive care unit, 100 patient monitors continuously stream high-frequency vital signs (Heart Rate, SPO2, Blood Pressure) over asynchronous TCP connections. An ingestion service using threads would consume excessive system memory and introduce thread-scheduling latency. An asynchronous event-loop architecture allows a single thread to ingest from all 100 monitors concurrently in non-blocking fashion while enforcing strict timeouts on slow sensors.
**Goals**:
- Ingest patient telemetry concurrently across coroutines using `asyncio.gather()`.
- Guard against network dropouts using per-query timeouts with `asyncio.wait_for()`.
- Return a synthesized clinical observation payload.
**Data Elements**:
- `bed_id` (str): Identifier for ICU bed (e.g. "BED-301").
- `telemetry` (dict): Sensor readings dictionary.
- `status` (str): "OK" or "TIMEOUT".

## Use Case
**Title**: Ingest ICU Bedside Vitals Asynchronously
**Description**: Query multiple bedside telemetry endpoints concurrently on the asyncio event loop, capture responses without blocking, and flag uncommunicative monitors.

### Rules
- All networking calls must be non-blocking coroutines using `async` and `await`.
- Individual device queries exceeding the timeout threshold must degrade to `"TIMEOUT"` without failing the remaining batch.

### Test Cases
- Case 1: Ingest from 4 responsive monitors; total batch time must not exceed the longest single monitor delay.
- Case 2: Ingest from a mixed batch containing a stalled monitor; verify the stalled monitor is flagged as `"TIMEOUT"` while healthy monitors succeed.

### Success Criteria
- Concurrency speedup verified (elapsed time << sequential sum).
- 100% of monitors accounted for.
- Zero unhandled exceptions.

## Overview
You will implement `AsyncICUVitalHub`, managing concurrent asynchronous device polling on the Python event loop.

## Learning Goals
- Write async functions using `async def` and `await`.
- Use `asyncio.gather()` with `return_exceptions=True`.
- Apply `asyncio.wait_for()`.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement methods in `starter_code.py`.
3. Run `python tests.py` to verify asynchronous execution.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Implement `poll_bed(bed_id: str, delay: float, vitals: dict, timeout_sec: float)`.
- Task 2: Implement `AsyncICUVitalHub.poll_all_beds(bed_configs, timeout_sec)`.
