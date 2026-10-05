---
title: "Parallel ECG Arrhythmia Signal Analyzer"
type: app_lab
module: concurrency
unit: unit_2_3_process_pools
lab_number: 1
difficulty: easy
use_case: parallel_ecg_signal_analyzer
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - concurrency
    - multiprocessing
  subtopics:
    - process-pool-executor
    - cpu-parallelism
    - chunksize-optimization
    - signal-processing
---

# Lab Level 1: Parallel ECG Arrhythmia Signal Analyzer
**Module**: Concurrency
**Objective**: Build a multi-core batch ECG telemetry signal processor using `ProcessPoolExecutor`.
**Difficulty**: Easy
**Context**: Clinical Cardiology & Telemetry Analytics

## Generic Information
**Problem Statement**: In a cardiac monitoring ward, 50 patients generate continuous electrocardiogram (ECG) voltage telemetry. Detecting arrhythmia and calculating heart rate variability requires digital signal smoothing and peak detection algorithms across 100,000 samples per recording. Running this computation sequentially takes 45 seconds, delaying clinical alert notifications.
**Goals**:
- Parallelize cardiac signal analysis across physical CPU cores using `ProcessPoolExecutor`.
- Utilize `executor.map()` with optimized chunking to process patient leads concurrently.
- Isolate corrupt or invalid telemetry recordings with error handling.
**Data Elements**:
- `lead_id` (str): Diagnostic lead identifier (e.g. "ECG-PATIENT-101").
- `voltages` (list of float): Raw voltage measurements.
- `peak_voltage` (float): Highest detected R-wave amplitude.
- `avg_voltage` (float): Baseline mean voltage.

## Use Case
**Title**: Batch ECG Signal Processing
**Description**: Dispatch patient ECG lead streams to a process pool executor, compute peak and baseline metrics across multi-core CPU workers, and return a consolidated cardiology report.

### Rules
- Processing must run on `ProcessPoolExecutor`.
- Worker tasks must be defined at the top-level module scope for cross-platform pickle compatibility.
- Corrupted signals (e.g. empty lists) must return a safe fallback without crashing the batch.

### Test Cases
- Case 1: Process 5 patient leads in parallel, verifying peak and average calculations match mathematical expectations.
- Case 2: Handle empty or corrupt voltage arrays cleanly.

### Success Criteria
- Parallel execution across cores completes faster than sequential loops.
- 100% calculation accuracy for all processed leads.
- Clean process pool shutdown.

## Overview
You will implement `ECGSignalProcessor`, leveraging multi-core parallel computing for intensive physiological signal analysis.

## Learning Goals
- Use `ProcessPoolExecutor` for batch mathematical tasks.
- Structure top-level worker functions for process safety.
- Collect and structure parallel task outputs.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement code in `starter_code.py`.
3. Run `python tests.py` to verify multi-core speed and correctness.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Implement top-level `process_lead_signal(lead_data: tuple) -> dict`.
- Task 2: Implement `ECGSignalProcessor.analyze_leads(lead_batch: list) -> list`.
