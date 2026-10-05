# Lab 1 Tasks: Hybrid Clinical Gateway

Follow these instructions to complete the hybrid gateway in `starter_code.py`.

---

### Task 1: Define `compute_genomic_hash(sequence: str) -> str`
1. Define a top-level module function `compute_genomic_hash(sequence: str) -> str` (must be top-level for Windows multiprocessing support).
2. Calculate the SHA-256 hexdigest of the input UTF-8 encoded string.
3. Return the 64-character hexadecimal digest string.

---

### Task 2: Implement `HybridGenomicsGateway`
1. In `__init__(self, max_workers: int = 2)`:
   - Instantiate and store a `ProcessPoolExecutor(max_workers=max_workers)` as `self.pool`.
2. Implement `async def process_sample(self, sample_id: str, raw_sequence: str) -> dict`:
   - Obtain the active running loop using `asyncio.get_running_loop()`.
   - Offload the CPU computation via `await loop.run_in_executor(self.pool, compute_genomic_hash, raw_sequence)`.
   - Return:
     ```python
     {
         "sample_id": sample_id,
         "hash": computed_hash,
         "status": "PROCESSED"
     }
     ```
3. Implement `async def batch_ingest(self, samples: List[Tuple[str, str]]) -> List[dict]`:
   - Schedule each `process_sample(sample_id, seq)` concurrently using `asyncio.gather()`.
   - Return the consolidated list of records.
4. Implement `def shutdown(self)`:
   - Call `self.pool.shutdown(wait=True)` to cleanly release process resources.
