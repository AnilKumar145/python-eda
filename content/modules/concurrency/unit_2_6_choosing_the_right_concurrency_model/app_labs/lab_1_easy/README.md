---
title: "Hybrid Clinical Gateway: Asyncio Ingestion with Process Pool Offloading"
type: app_lab
module: concurrency
unit: unit_2_6_choosing_the_right_concurrency_model
lab_number: 1
difficulty: easy
use_case: hybrid_clinical_gateway
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - concurrency
    - architecture
  subtopics:
    - hybrid-models
    - asyncio
    - process-pool-executor
    - cpu-offloading
---

# Lab Level 1: Hybrid Clinical Gateway
**Module**: Concurrency
**Objective**: Build a production-grade hybrid architecture combining an Asyncio event loop for non-blocking telemetry ingestion with a ProcessPoolExecutor for CPU-intensive genomic signature hashing.
**Difficulty**: Easy
**Context**: Precision Oncology Sequencing Gateway

## Generic Information
**Problem Statement**: A high-throughput genomics laboratory receives continuous diagnostic streams over asynchronous network connections. Each incoming sample contains a raw nucleotide string that must undergo intensive cryptographic hashing (CPU-bound) before archival. Running heavy CPU hashing directly in an `async def` handler freezes the event loop, causing connection drops for incoming clinical feeds. The gateway must ingest network traffic asynchronously on the event loop, delegate the heavy hashing to a `ProcessPoolExecutor` via `loop.run_in_executor()`, and deliver the verified record without stalling network I/O.
**Goals**:
- Build a hybrid architecture marrying `asyncio` and `ProcessPoolExecutor`.
- Keep the event loop non-blocking while utilizing multi-core CPU capacity.
- Validate that network requests continue processing during intensive calculations.
**Data Elements**:
- `sample_id` (str): Unique clinical specimen identifier (e.g. "SMP-9021").
- `raw_sequence` (str): Genomic DNA string.
- `computed_hash` (str): Verified SHA-256 digest calculated in a worker process.

## Use Case
**Title**: Offload Heavy Genomic Processing from Async Ingestion Gateway
**Description**: An asynchronous handler receives incoming patient genomic streams, offloads hashing to an isolated process pool, and returns the archived metadata record.

### Rules
- Ingestion must be defined as an `async` coroutine.
- The CPU-intensive hashing function must run in a worker process via `loop.run_in_executor()`, NOT directly on the event loop.
- The event loop must remain free to process other concurrent requests.

### Test Cases
- Case 1: Process multiple incoming genomic packets concurrently; verify valid hashes and execution across processes.
- Case 2: Concurrency check: Ensure a high-priority quick telemetry ping completes while long CPU hashing is ongoing in the background pool.

### Success Criteria
- Event loop does not stall during CPU hashing.
- Accurate SHA-256 calculation verified.
- Clean shutdown of process pools.

## Overview
You will implement `HybridGenomicsGateway` in `starter_code.py`.

## Learning Goals
- Combine `asyncio` with `concurrent.futures.ProcessPoolExecutor`.
- Utilize `loop.run_in_executor()` for CPU offloading.
- Understand the architectural trade-offs between threads, processes, and event loops.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement methods in `starter_code.py`.
3. Run `python tests.py` to verify hybrid execution.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Define the top-level CPU hashing function `compute_genomic_hash(sequence: str) -> str`.
- Task 2: Implement `HybridGenomicsGateway.process_sample(sample_id, raw_sequence)`.
- Task 3: Implement `HybridGenomicsGateway.batch_ingest(samples)`.
