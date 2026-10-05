# Lab 1 Tasks: Asynchronous ICU Vital Signs Hub

Follow these instructions to complete the asynchronous vitals hub in `starter_code.py`.

---

### Task 1: Implement `poll_bed(bed_id, delay, vitals, timeout_sec)`
1. Define an asynchronous coroutine `async def poll_bed(bed_id: str, delay: float, vitals: dict, timeout_sec: float) -> dict`.
2. Inside an internal coroutine or simulated fetch, simulate asynchronous network latency using `await asyncio.sleep(delay)`.
3. Wrap the simulated fetch using `await asyncio.wait_for(..., timeout=timeout_sec)`.
4. If the fetch succeeds within `timeout_sec`, return:
   ```python
   {
       "bed_id": bed_id,
       "status": "OK",
       "vitals": vitals
   }
   ```
5. If `asyncio.TimeoutError` occurs, catch it and return:
   ```python
   {
       "bed_id": bed_id,
       "status": "TIMEOUT",
       "vitals": {}
   }
   ```

---

### Task 2: Implement `AsyncICUVitalHub.poll_all_beds(bed_configs, timeout_sec)`
1. Receive `bed_configs: List[tuple]` where each element is `(bed_id, delay, vitals)`.
2. Schedule all coroutine calls using `asyncio.gather(*tasks, return_exceptions=True)`.
3. Await completion and return the list of dictionary results.
