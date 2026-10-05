---
title: "Thread Pools"
type: knowledge
module: threads
unit: unit_1_5_thread_pools
order: 5
difficulty: intermediate
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - thread-pool-executor
    - concurrent-futures
    - submit-vs-map
    - future-objects
    - as-completed
    - exception-handling
---

# Unit 1.5: Thread Pools

## 1. What

A **Thread Pool** is a software design pattern where a fixed or dynamic collection of pre-allocated worker threads is maintained to execute submitted tasks concurrently. Instead of creating a new OS thread every time an asynchronous task is needed—and destroying it upon completion—tasks are submitted to a work queue, picked up by an available pool thread, executed, and the thread returns to the pool to await further work.

### Why Thread Pools Over Raw `threading.Thread`?
Using low-level `threading.Thread` for every individual operation introduces three severe operational liabilities:
1. **Thread Creation Overhead**: Creating and tearing down native OS threads consumes significant CPU cycles and stack allocation.
2. **Resource Exhaustion**: If a web server spawns an unconstrained thread for every one of 5,000 incoming requests, the process will exhaust OS memory and thread handles, crashing the system.
3. **Missing Return Values & Error Handling**: A standard `threading.Thread` cannot return a value directly to its caller, and any exception raised inside a worker thread crashes silently without notifying the calling code.

### Python's `concurrent.futures.ThreadPoolExecutor`
Introduced in PEP 3148, `ThreadPoolExecutor` provides an interface for managed thread execution. It encapsulates:
- A worker pool of size `max_workers`.
- An internal work queue.
- `submit(fn, *args, **kwargs)`: Dispatches a single callable, returning an immediate `Future` handle.
- `map(fn, *iterables)`: Parallel counterpart to Python's built-in `map()`, executing `fn` across elements and yielding results in submission order.
- `Future` object: An encapsulation of an ongoing or completed asynchronous computation, providing `.result()`, `.done()`, and exception retrieval.

---

## 2. Example

### Example 1: Basic Task Submission and `Future.result()`
Submitting tasks to an executor and retrieving results synchronously.

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_patient_vitals(patient_id: str) -> dict:
    print(f"[Worker] Fetching telemetry for {patient_id}...")
    time.sleep(0.5)
    return {"patient_id": patient_id, "heart_rate": 74, "spo2": 98.2}

# Use context manager for automatic shutdown and joining
with ThreadPoolExecutor(max_workers=2) as executor:
    # submit() returns a Future object immediately
    future1 = executor.submit(fetch_patient_vitals, "P-101")
    future2 = executor.submit(fetch_patient_vitals, "P-102")

    print("[Main] Tasks submitted. Doing other work...")
    
    # future.result() blocks until the worker function returns
    vitals1 = future1.result()
    vitals2 = future2.result()
    print(f"[Main] Result 1: {vitals1}")
    print(f"[Main] Result 2: {vitals2}")
```

**Expected Output:**
```text
[Worker] Fetching telemetry for P-101...
[Worker] Fetching telemetry for P-102...
[Main] Tasks submitted. Doing other work...
[Main] Result 1: {'patient_id': 'P-101', 'heart_rate': 74, 'spo2': 98.2}
[Main] Result 2: {'patient_id': 'P-102', 'heart_rate': 74, 'spo2': 98.2}
```

---

### Example 2: Streaming Transformations with `executor.map()`
When applying the same operation across an iterable, `executor.map()` provides concise parallel processing.

```python
from concurrent.futures import ThreadPoolExecutor
import time

def calculate_dosage(weight_kg: float) -> float:
    time.sleep(0.1)
    return round(weight_kg * 0.15, 2)

patient_weights = [45.0, 72.5, 88.0, 60.2, 105.0]

with ThreadPoolExecutor(max_workers=3) as executor:
    # executor.map() yields results in the exact same order as input items
    for weight, dosage in zip(patient_weights, executor.map(calculate_dosage, patient_weights)):
        print(f"Weight: {weight:>5} kg -> Prescribed Dosage: {dosage:>5} mg")
```

**Expected Output:**
```text
Weight:  45.0 kg -> Prescribed Dosage:  6.75 mg
Weight:  72.5 kg -> Prescribed Dosage: 10.88 mg
Weight:  88.0 kg -> Prescribed Dosage:  13.2 mg
Weight:  60.2 kg -> Prescribed Dosage:  9.03 mg
Weight: 105.0 kg -> Prescribed Dosage: 15.75 mg
```

---

### Example 3: Real-World Healthcare Scenario — Asynchronous Diagnostic Panel Aggregator
A hospital patient dashboard queries 4 independent diagnostic subsystems (Lab, Radiology, Cardiology, Pharmacy). Using `as_completed()`, results are streamed to the UI as soon as each subsystem responds, rather than waiting for the slowest query.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Dict, Any

def query_lab_results(patient_id: str) -> Dict[str, Any]:
    time.sleep(0.8) # Laboratory subsystem latency
    return {"service": "Lab", "status": "WBC Normal, Glucose 95 mg/dL"}

def query_radiology(patient_id: str) -> Dict[str, Any]:
    time.sleep(1.2) # PACS imaging latency
    return {"service": "Radiology", "status": "Chest X-Ray Clear"}

def query_cardiology(patient_id: str) -> Dict[str, Any]:
    time.sleep(0.4) # Telemetry ECG latency (fastest!)
    return {"service": "Cardiology", "status": "Normal Sinus Rhythm"}

def query_pharmacy(patient_id: str) -> Dict[str, Any]:
    time.sleep(0.6) # Pharmacy dispensation latency
    return {"service": "Pharmacy", "status": "Active: Amoxicillin 500mg"}

queries = [query_lab_results, query_radiology, query_cardiology, query_pharmacy]

print("[Dashboard] Querying patient diagnostic panel...")
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=4) as executor:
    # Map future -> function name for diagnostics
    future_to_query = {
        executor.submit(fn, "PAT-9901"): fn.__name__ 
        for fn in queries
    }
    
    # as_completed yields futures as they finish!
    for future in as_completed(future_to_query):
        service_name = future_to_query[future]
        result = future.result()
        print(f" -> Received [{result['service']}]: {result['status']}")

elapsed = time.perf_counter() - start_time
print(f"[Dashboard] Complete diagnostic panel compiled in {elapsed:.2f}s!")
```

**Expected Output:**
```text
[Dashboard] Querying patient diagnostic panel...
 -> Received [Cardiology]: Normal Sinus Rhythm
 -> Received [Pharmacy]: Active: Amoxicillin 500mg
 -> Received [Lab]: WBC Normal, Glucose 95 mg/dL
 -> Received [Radiology]: Chest X-Ray Clear
[Dashboard] Complete diagnostic panel compiled in 1.21s!
```

---

### Example 4: Exception Handling Across Worker Tasks
When an unhandled exception occurs inside a worker thread, `ThreadPoolExecutor` captures the exception and re-raises it when `future.result()` is called on the main thread.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def risky_service(device_id: str):
    if device_id == "DEV-CRASH":
        raise ConnectionResetError(f"Hardware sensor {device_id} dropped carrier connection!")
    return f"Status OK for {device_id}"

devices = ["DEV-01", "DEV-CRASH", "DEV-03"]

with ThreadPoolExecutor(max_workers=3) as executor:
    future_map = {executor.submit(risky_service, dev): dev for dev in devices}
    
    for fut in as_completed(future_map):
        dev_id = future_map[fut]
        try:
            val = fut.result()
            print(f"[SUCCESS] {dev_id}: {val}")
        except Exception as exc:
            print(f"[ERROR TRAPPED] {dev_id} failed with error: {exc}")
```

**Expected Output:**
```text
[SUCCESS] DEV-01: Status OK for DEV-01
[ERROR TRAPPED] DEV-CRASH failed with error: Hardware sensor DEV-CRASH dropped carrier connection!
[SUCCESS] DEV-03: Status OK for DEV-03
```

---

## 3. Explanation

### ThreadPoolExecutor Internal Architecture
`ThreadPoolExecutor` decouples task dispatch from execution through an internal task queue:

```
    Application Code
         │
         │ executor.submit(fn, *args)
         ▼
   ┌────────────────────────────────────────────────────────┐
   │                  ThreadPoolExecutor                    │
   │                                                        │
   │    _work_queue (queue.SimpleQueue)                     │
   │   ┌───────────────────────────────────────────────┐    │
   │   │  [_WorkItem 1] -> [_WorkItem 2] -> ...        │    │
   │   └───────────────────────┬───────────────────────┘    │
   │                           │                            │
   │        ┌──────────────────┼──────────────────┐         │
   │        ▼                  ▼                  ▼         │
   │   Worker Thread 1    Worker Thread 2    Worker Thread 3│
   │   (Executes fn)      (Executes fn)      (Executes fn)  │
   │        │                  │                  │         │
   │        └──────────────────┼──────────────────┘         │
   │                           ▼                            │
   │             future.set_result(return_value)            │
   │             or future.set_exception(exc)               │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
                        Future Object
                   (Accessed via .result())
```

### Future Object State Transitions
A `Future` transitions through a strict lifecycle:
```text
               ┌───────────┐
               │  PENDING  │  (.done() == False, .running() == False)
               └─────┬─────┘
                     │ Worker thread picks up _WorkItem
                     ▼
               ┌───────────┐
               │  RUNNING  │  (.done() == False, .running() == True)
               └─────┬─────┘
                     │ Function completes or raises
                     ▼
               ┌───────────┐
               │ FINISHED  │  (.done() == True)
               └───────────┘
```

### `submit()` vs `map()` Comparison

| Feature | `executor.submit()` | `executor.map()` |
|---|---|---|
| **Return Type** | Single `Future` object | Generator yielding unpacked results |
| **Input Flexibility** | Diverse functions, differing arguments | Single function applied across iterables |
| **Result Ordering** | Can process out-of-order with `as_completed()` | Strictly yields in original submission order |
| **Exception Handling** | Trapped until individual `future.result()` | Raised immediately when generator yields failed item |
| **Fine Control** | High (timeouts, callbacks via `add_done_callback`) | Medium (convenient for uniform batch workloads) |

---

## 4. Why

### 1. Controlled Resource Utilization
In high-load services, setting `max_workers=10` ensures that no matter how many requests arrive, at most 10 operating system threads will ever be spawned, protecting CPU and memory from starvation.

### 2. Native Result Retrieval
`Future.result()` solves the classic multi-threading problem of extracting return values without needing shared accumulator dictionaries and manual locks.

### 3. Transparent Exception Propagation
In raw `threading.Thread`, exceptions are printed to `stderr` and the worker dies quietly. `ThreadPoolExecutor` stores the exception in the `Future` and re-raises it when requested, allowing clean `try...except` handling on the calling thread.

---

## 5. Advantages & Disadvantages

### Advantages
1. **Thread Reuse**: Reuses worker threads across thousands of short-lived tasks, eliminating allocation latency.
2. **Deterministic Teardown**: Context manager automatically waits for running tasks to complete.
3. **Flexible Polling**: `as_completed()` enables streaming responsive results.

### Disadvantages
1. **GIL Limitation**: Still constrained by Python's GIL for CPU-bound computation (use `ProcessPoolExecutor` instead).
2. **Hidden Task Accumulation**: If tasks are submitted faster than workers can process them, the internal unbound `_work_queue` can grow without limit unless wrapped with custom bounding logic.

---

## 6. Real-World Use Cases

### Domain 1: Healthcare — Patient Clinical Summary Compiler
- **Problem**: When a physician opens an electronic medical record (EMR), the backend must pull vitals, lab reports, imaging notes, and prescription history from 5 separate hospital databases.
- **Solution**: A `ThreadPoolExecutor(max_workers=5)` queries each database concurrently. Results are assembled using `as_completed()`, reducing page load from 3.2s to 700ms.

### Domain 2: eCommerce — Marketplace Price Aggregator
- **Problem**: A shopping platform displays competing vendor prices by querying 12 third-party merchant APIs.
- **Solution**: The aggregator submits all 12 queries to a thread pool with a 1.5s timeout. Using `Future.result(timeout=1.5)`, slow or hanging vendor APIs are ignored without delaying the search results page.

### Domain 3: Banking — Batch Wire Transfer Reconciliation
- **Problem**: Every midnight, a banking engine reconciles 2,000 inter-bank wire settlements. Sequential verification takes 45 minutes.
- **Solution**: The reconciliation batch is processed using `executor.map(reconcile_wire, wire_list)` with 20 worker threads, completing the entire ledger audit in under 3 minutes.

---

## 7. Best Practices

### Practice 1: Always Use Context Managers
**When to apply**: Instantiating `ThreadPoolExecutor`.
**Why**: Ensures `executor.shutdown(wait=True)` is called automatically, preventing orphaned threads when functions exit.

```python
# GOOD PRACTICE
with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(worker, items))
```

### Practice 2: Choose `max_workers` Based on Workload Characteristics
**When to apply**: Configuring pool size.
**Why**: For I/O-bound tasks (network, database), `max_workers = min(32, os.cpu_count() + 4)` is the Python default, but can be set higher (e.g. 20–50) depending on socket latency.

### Practice 3: Always Pass Timeouts to `Future.result()`
**When to apply**: When awaiting futures that depend on external networks.
**Why**: Prevents a hung external service from permanently blocking the calling thread.

```python
# GOOD PRACTICE
try:
    val = future.result(timeout=5.0)
except TimeoutError:
    logger.warning("Downstream service timed out!")
```

---

## 8. Top 3 Mistakes

### Mistake 1: Forgetting to Call `.result()` or Inspect Exceptions
#### What's the Problem?
Submitting tasks to `ThreadPoolExecutor` and letting the context manager exit without inspecting the returned `Future` objects.
#### Why It Happens
Assuming that if `executor.submit()` succeeded, the task completed successfully.
#### Impact
If the worker function raised an exception (e.g. `ZeroDivisionError` or `DatabaseError`), the exception is swallowed silently.
#### Incorrect Approach
```python
with ThreadPoolExecutor() as executor:
    for item in items:
        executor.submit(process, item) # Exceptions silently lost!
```
#### Correct Approach
```python
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process, item) for item in items]
    for fut in as_completed(futures):
        fut.result() # Re-raises any exception raised in worker!
```
#### Lesson Learned
Always inspect `future.result()` or iterate over completed futures to catch and handle worker exceptions.

---

### Mistake 2: Using `ThreadPoolExecutor` for CPU-Intensive Tasks
#### What's the Problem?
Using a thread pool to accelerate heavy mathematical computation.
#### Why It Happens
Confusing `ThreadPoolExecutor` with `ProcessPoolExecutor`.
#### Impact
GIL contention slows down execution compared to a single-threaded loop.
#### Correct Approach
```python
# For CPU-bound tasks, use ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as executor:
    results = list(executor.map(cpu_heavy_task, dataset))
```
#### Lesson Learned
Use `ThreadPoolExecutor` for I/O-bound tasks; use `ProcessPoolExecutor` for CPU-bound tasks.

---

### Mistake 3: Submitting Tasks to a Shut Down Executor
#### What's the Problem?
Calling `executor.submit()` after exiting the `with` block or after calling `executor.shutdown()`.
#### Why It Happens
Holding references to an executor across disparate application scopes.
#### Impact
Raises `RuntimeError: cannot schedule new futures after shutdown`.
#### Correct Approach
Keep task submission strictly scoped within the executor's active lifecycle.
#### Lesson Learned
Only submit tasks while the executor is active and open.
