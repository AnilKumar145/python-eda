# Lab Level 1 Tasks: Multi-Core Genomic Chromosome Scanner

## Task 1: Top-Level Worker Task
**Difficulty**: Easy
**Points**: 10

### Objective
Implement the top-level process worker function `scan_chromosome_task`.

### Requirements
- Function signature: `scan_chromosome_task(chr_id: str, sequence: str, marker: str, out_q: multiprocessing.Queue) -> None`
- Count occurrences of `marker` in `sequence`:
  - `count = sequence.count(marker)`
- Put a tuple `(chr_id, count)` onto `out_q`.

---

## Task 2: Multi-Process Scanner Engine
**Difficulty**: Easy
**Points**: 20

### Objective
Implement `GenomicScannerEngine.scan_all(chromosome_dict: dict, marker: str) -> dict`.

### Requirements
- In `scan_all(self, chromosome_dict: dict, marker: str) -> dict`:
  - Create `out_q = multiprocessing.Queue()`.
  - For each `chr_id, sequence` in `chromosome_dict.items()`:
    - Spawn a `multiprocessing.Process` targeting `scan_chromosome_task`.
    - Pass `(chr_id, sequence, marker, out_q)` via `args`.
    - Start the process.
  - Read all `len(chromosome_dict)` results from `out_q`.
  - Join all processes.
  - Return a dictionary mapping `chr_id -> match_count`.
