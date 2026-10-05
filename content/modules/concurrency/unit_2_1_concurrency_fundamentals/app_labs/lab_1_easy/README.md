---
title: "Clinical Workload Router and Profiler"
type: app_lab
module: concurrency
unit: unit_2_1_concurrency_fundamentals
lab_number: 1
difficulty: easy
use_case: clinical_workload_router
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - concurrency
    - multiprocessing
    - asyncio
  subtopics:
    - workload-classification
    - concurrency-routing
    - performance-profiling
---

# Lab Level 1: Clinical Workload Router and Profiler
**Module**: Concurrency
**Objective**: Build a clinical request router that profiles incoming healthcare jobs (I/O vs CPU) and routes them to appropriate concurrency executors.
**Difficulty**: Easy
**Context**: Healthcare Enterprise Service Gateway

## Generic Information
**Problem Statement**: A central hospital gateway receives incoming jobs ranging from I/O-bound operations (e.g. fetching patient demographic records from a database) to heavy CPU-bound computations (e.g. computing genomic risk scores and image Fourier transformations). If CPU-heavy tasks are routed to the I/O thread pool, CPython's GIL blocks the threads, causing network timeouts for patient lookup requests.
**Goals**:
- Profile and classify incoming requests based on operational metadata.
- Route I/O-bound jobs to an I/O worker pool and CPU-bound jobs to a CPU worker pool.
- Return execution telemetry proving proper isolation.
**Data Elements**:
- `job_id` (str): Unique request identifier.
- `job_type` (str): "IO" (network/database) or "CPU" (numerical computation).
- `payload` (dict): Job execution parameters.

## Use Case
**Title**: Route Hospital Workloads Intelligently
**Description**: Inspect incoming task descriptors, classify their operational characteristics, and dispatch them to the appropriate executor without cross-pool interference.

### Rules
- CPU-bound tasks must not starve I/O-bound operations.
- The router must maintain separate metrics for both workload types.

### Test Cases
- Case 1: Route 5 I/O tasks and 5 CPU tasks, verifying correct classification.
- Case 2: Process hybrid batch and return aggregated outcomes with execution metrics.

### Success Criteria
- 100% of jobs are categorized and routed to their designated executor.
- Telemetry records show zero cross-pool contamination.

## Overview
In this lab, you will implement `ClinicalWorkloadRouter`, creating a routing layer that ensures CPU and I/O tasks are segregated.

## Learning Goals
- Design workload classification filters.
- Maintain separate concurrent executors for I/O and CPU workloads.
- Measure execution characteristics.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement code in `starter_code.py`.
3. Run `python tests.py` to verify routing accuracy.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Implement `classify_job(job_descriptor: dict) -> str`.
- Task 2: Implement `ClinicalWorkloadRouter.dispatch(jobs: list) -> dict`.
