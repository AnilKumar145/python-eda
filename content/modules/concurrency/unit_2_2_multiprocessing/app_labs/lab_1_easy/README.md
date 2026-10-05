---
title: "Multi-Core Genomic Chromosome Scanner"
type: app_lab
module: concurrency
unit: unit_2_2_multiprocessing
lab_number: 1
difficulty: easy
use_case: genomic_chromosome_scanner
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - concurrency
    - multiprocessing
  subtopics:
    - process-class
    - ipc-queue
    - cpu-parallelism
---

# Lab Level 1: Multi-Core Genomic Chromosome Scanner
**Module**: Concurrency
**Objective**: Build a multi-core DNA marker scanner using `multiprocessing.Process` and `multiprocessing.Queue`.
**Difficulty**: Easy
**Context**: Clinical Bioinformatics & Oncology Diagnostics

## Generic Information
**Problem Statement**: In cancer genomic diagnostics, patient biopsy samples are sequenced into billions of DNA base pairs across 24 human chromosomes. Searching every chromosome sequentially for oncogenic mutation markers takes several minutes. Because string matching on raw genomic data is purely CPU-bound, multithreading cannot achieve true speedup due to CPython's GIL. True parallel acceleration requires allocating distinct chromosomes to separate operating system processes.
**Goals**:
- Partition chromosome search tasks across multiple child processes using `multiprocessing.Process`.
- Collect mutation match counts via a thread-safe/process-safe `multiprocessing.Queue`.
- Measure parallel execution time and verify speedup over sequential execution.
**Data Elements**:
- `chromosome_id` (str): Identifier (e.g. "Chr-17", "Chr-13").
- `sequence` (str): Nucleotide string composed of 'A', 'C', 'G', 'T'.
- `target_marker` (str): Short biomarker nucleotide sequence (e.g. "TATAAA").
- `match_count` (int): Total occurrences found.

## Use Case
**Title**: Parallel DNA Marker Discovery
**Description**: Dispatch chromosome sequences to child processes, search for oncogene target markers concurrently, and aggregate match tallies in the parent process.

### Rules
- Each chromosome must be scanned in an independent `multiprocessing.Process`.
- Results must be reported through an IPC `Queue`.
- Code must adhere to Windows entry point protection (`if __name__ == '__main__':`).

### Test Cases
- Case 1: Search 4 simulated chromosomes in parallel, verifying accurate match counts for each.
- Case 2: Ensure all child processes exit cleanly with exit code 0.

### Success Criteria
- 100% of chromosome matches accurately accounted for.
- Parallel processing time is significantly faster than sequential processing.
- Clean process join teardown without zombie processes.

## Overview
You will implement `GenomicScannerEngine`, managing process lifecycles and gathering parallel search results.

## Learning Goals
- Use `multiprocessing.Process` for CPU-intensive data tasks.
- Transmit results safely across process boundaries via `multiprocessing.Queue`.
- Manage process joining.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement code in `starter_code.py`.
3. Run `python tests.py` to verify multi-process execution.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Implement top-level `scan_chromosome_task(chr_id, sequence, marker, out_q)`.
- Task 2: Implement `GenomicScannerEngine.scan_all(chromosome_dict, marker)`.
