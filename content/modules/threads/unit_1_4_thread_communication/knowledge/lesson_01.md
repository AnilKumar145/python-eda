---
title: "Thread Communication"
type: knowledge
module: threads
unit: unit_1_4_thread_communication
order: 4
difficulty: intermediate
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - queue-module
    - producer-consumer
    - message-passing
    - priority-queue
    - backpressure
    - sentinel-shutdown
---

# Unit 1.4: Thread Communication

## 1. What

**Thread Communication** is the discipline of exchanging data, instructions, and control signals between concurrently executing threads without relying on unprotected shared mutable memory. Instead of multiple threads competing for locks to modify the same global structures, threads communicate by sending discrete messages across thread-safe data conduits.

### The Philosophy: Message Passing vs. Shared Memory
A foundational tenet of modern concurrent engineering (popularized by Go, Erlang, and Actor models) states:
> *"Do not communicate by sharing memory; instead, share memory by communicating."*

When threads share mutable variables (such as a shared list or dictionary), developers must carefully wrap every read and write with locks. Even a single missed lock creates catastrophic race conditions. In contrast, with **message passing**, state is encapsulated inside discrete thread workers. Data is handed off through a thread-safe message queue. Once an object is placed onto a queue, the sender relinquishes ownership, and the receiver takes exclusive control.

### Python's `queue` Module
Python's standard library provides the `queue` module, which contains three thread-safe data structures implemented with internal `threading.Lock` and `threading.Condition` primitives:
1. `queue.Queue(maxsize)`: Standard First-In, First-Out (FIFO) queue.
2. `queue.LifoQueue(maxsize)`: Last-In, First-Out (LIFO) stack.
3. `queue.PriorityQueue(maxsize)`: Priority-heap ordered queue where entries with lower numerical priority values are retrieved first.

### Bounded Buffers & Backpressure
By specifying `maxsize > 0`, queues enforce **backpressure**. When the queue fills up, producing threads attempting `queue.put()` block until consumer threads process items via `queue.get()`. This prevents fast producers from exhausting system memory when consumers process slowly.

---

## 2. Example

### Example 1: Classic Producer–Consumer Pipeline
A producer generates batch task items and places them onto a FIFO queue; consumer worker threads process them independently.

```python
import threading
import queue
import time

# Create a bounded thread-safe queue
work_queue = queue.Queue(maxsize=5)

def producer(items_to_create: int):
    for i in range(items_to_create):
        item = f"Task-{i}"
        print(f"[Producer] Enqueuing {item}...")
        work_queue.put(item) # Blocks if queue reaches maxsize=5
        time.sleep(0.1)
    
    # Send a sentinel value (None) to signal consumer shutdown
    work_queue.put(None)
    print("[Producer] Completed production. Sentinel sent.")

def consumer():
    while True:
        item = work_queue.get() # Blocks until item is available
        if item is None:
            # Sentinel received: task done and break
            work_queue.task_done()
            print("[Consumer] Sentinel received. Exiting.")
            break
        
        print(f"[Consumer] Processing {item}...")
        time.sleep(0.2)
        work_queue.task_done() # Signal item processing finished

p_thread = threading.Thread(target=producer, args=(6,))
c_thread = threading.Thread(target=consumer)

p_thread.start()
c_thread.start()

p_thread.join()
c_thread.join()
```

**Expected Output:**
```text
[Producer] Enqueuing Task-0...
[Consumer] Processing Task-0...
[Producer] Enqueuing Task-1...
[Producer] Enqueuing Task-2...
[Consumer] Processing Task-1...
[Producer] Enqueuing Task-3...
[Producer] Enqueuing Task-4...
[Consumer] Processing Task-2...
[Producer] Enqueuing Task-5...
[Producer] Completed production. Sentinel sent.
[Consumer] Processing Task-3...
[Consumer] Processing Task-4...
[Consumer] Processing Task-5...
[Consumer] Sentinel received. Exiting.
```

---

### Example 2: Tracking Task Completion with `queue.join()`
Instead of manual sentinel management, `queue.join()` blocks the main thread until every item added to the queue has had `queue.task_done()` called on it.

```python
import threading
import queue
import time

task_queue = queue.Queue()

def background_worker(worker_id: int):
    while True:
        job = task_queue.get()
        print(f"[Worker-{worker_id}] Executing {job}...")
        time.sleep(0.1)
        task_queue.task_done() # Informs queue that one task finished

# Spawn 2 daemon consumer threads
for i in range(2):
    threading.Thread(target=background_worker, args=(i,), daemon=True).start()

# Main thread loads 5 jobs
for j in range(5):
    task_queue.put(f"Job-{j}")

print("[Main] All jobs queued. Waiting for completion...")
task_queue.join() # Blocks until all 5 task_done() calls are registered!
print("[Main] All jobs processed! Exiting.")
```

**Expected Output:**
```text
[Main] All jobs queued. Waiting for completion...
[Worker-0] Executing Job-0...
[Worker-1] Executing Job-1...
[Worker-0] Executing Job-2...
[Worker-1] Executing Job-3...
[Worker-0] Executing Job-4...
[Main] All jobs processed! Exiting.
```

---

### Example 3: Real-World Healthcare Scenario — Emergency Room Priority Triage
In a hospital ER, arriving patients are assigned emergency triage levels:
- Priority 1: Resuscitation (Cardiac arrest)
- Priority 2: Emergent (Stroke / Trauma)
- Priority 3: Urgent (Fracture)
- Priority 4: Non-urgent (Cold / Sprain)

Using `queue.PriorityQueue`, critical patients jump to the front of the doctor's queue regardless of arrival order.

```python
import threading
import queue
import time
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class TriagePatient:
    priority: int                   # Lower int = higher priority
    patient_name: str = field(compare=False)
    chief_complaint: str = field(compare=False)

er_queue = queue.PriorityQueue()

def doctor_consultant(doctor_name: str):
    while True:
        patient: TriagePatient = er_queue.get()
        if patient is None:
            er_queue.task_done()
            break
        print(f"[{doctor_name}] Treating [Level {patient.priority}] {patient.patient_name}: {patient.chief_complaint}")
        time.sleep(0.15)
        er_queue.task_done()

# Start doctor consumer
doc_thread = threading.Thread(target=doctor_consultant, args=("Dr. House",), daemon=True)
doc_thread.start()

# Ingest patients arriving in random order
er_queue.put(TriagePatient(4, "John Doe", "Mild headache"))
er_queue.put(TriagePatient(3, "Sarah Smith", "Arm fracture"))
er_queue.put(TriagePatient(1, "Michael Vance", "Severe cardiac arrest")) # Level 1 jumps ahead!
er_queue.put(TriagePatient(2, "Emily Blunt", "Suspected stroke"))

er_queue.join() # Wait until all patients treated
er_queue.put(None) # Stop doctor thread
doc_thread.join()
```

**Expected Output:**
```text
[Dr. House] Treating [Level 1] Michael Vance: Severe cardiac arrest
[Dr. House] Treating [Level 2] Emily Blunt: Suspected stroke
[Dr. House] Treating [Level 3] Sarah Smith: Arm fracture
[Dr. House] Treating [Level 4] John Doe: Mild headache
```
*Notice how Michael Vance (Level 1) was handled first even though he was enqueued third!*

---

### Example 4: Non-blocking Queue Checks with Timeouts
In responsive systems, workers should not block indefinitely on `queue.get()`, but rather poll with a timeout to allow periodic health checks and cancellation responses.

```python
import threading
import queue
import time

data_queue = queue.Queue()
stop_flag = threading.Event()

def responsive_worker():
    while not stop_flag.is_set():
        try:
            # Wait up to 0.2s for an item; avoids permanent blocking
            item = data_queue.get(timeout=0.2)
            print(f"[Worker] Handled {item}")
            data_queue.task_done()
        except queue.Empty:
            # Timeout elapsed with no item; loop back and recheck stop_flag
            continue
    print("[Worker] Clean exit on stop flag.")

worker_t = threading.Thread(target=responsive_worker)
worker_t.start()

time.sleep(0.1)
data_queue.put("Batch-Alpha")
time.sleep(0.3)
stop_flag.set()
worker_t.join()
```

**Expected Output:**
```text
[Worker] Handled Batch-Alpha
[Worker] Clean exit on stop flag.
```

---

## 3. Explanation

### Internal Mechanics of `queue.Queue`
Under the hood, `queue.Queue` wraps a collections `deque` object protected by an internal `threading.Lock` and two `threading.Condition` objects:
- `not_empty`: Consumers wait on this condition when the queue is empty; `put()` notifies `not_empty`.
- `not_full`: Producers wait on this condition when the queue reaches `maxsize`; `get()` notifies `not_full`.
- `all_tasks_done`: Tracks an internal integer count of unfinished tasks. `put()` increments the count; `task_done()` decrements it; when count hits 0, `join()` unblocks.

```
       Producers (Threads 1, 2)
                │
                │ put(item)
                ▼
┌──────────────────────────────────────────────┐
│                queue.Queue                   │
│   ┌──────────────────────────────────────┐   │
│   │  [not_full] Condition (maxsize=N)    │   │
│   │                                      │   │
│   │        [ Item 3 | Item 2 | Item 1 ]  │   │
│   │                                      │   │
│   │  [not_empty] Condition               │   │
│   └──────────────────────────────────────┘   │
└──────────────────────┬───────────────────────┘
                       │
                       │ get()
                       ▼
             Consumers (Threads 3, 4)
```

### Queue Family Comparison Table

| Queue Class | Ordering Strategy | Primary Use Case | Thread Safe? |
|---|---|---|---|
| `queue.Queue(maxsize)` | FIFO (First In, First Out) | General task pipelines, web scraper worker pools | Yes (Lock + Condition) |
| `queue.LifoQueue(maxsize)` | LIFO (Last In, First Out) | Depth-first processing, undo buffers | Yes (Lock + Condition) |
| `queue.PriorityQueue(maxsize)` | Min-Heap priority order | Triage systems, SLA request dispatching | Yes (heapq + Lock) |
| `collections.deque` | FIFO or LIFO | Single-thread double-ended buffer | **No** (atomic appends only, no blocking wait) |

---

## 4. Why

### 1. Eliminating Explicit Locks from Business Code
When developers use locks, they must manage lock contention, acquire/release order, and reentrancy. Queues encapsulate all synchronization internally. Business code simply calls `.put()` and `.get()`, eliminating 95% of locking deadlocks.

### 2. Decoupling Producers from Consumers
In high-throughput systems, producers and consumers operate at fluctuating rates. A message queue acts as an elastic buffer: during traffic spikes, the queue absorbs incoming requests without slowing down ingestion APIs.

### 3. Backpressure Protection Against Out-Of-Memory (OOM)
An unbounded queue will consume all available RAM if upstream requests arrive faster than downstream workers can process them. Setting `maxsize` automatically forces fast producers to pause, matching system throughput to downstream capacity.

---

## 5. Advantages & Disadvantages

### Advantages
1. **Zero Locking Boilerplate**: No need to write manual `with lock:` blocks.
2. **Built-in Flow Control**: `maxsize` handles backpressure natively.
3. **Flexible Ordering**: FIFO, LIFO, and Priority supported transparently.

### Disadvantages
1. **Unidirectional Communication**: A queue only delivers data from producer to consumer. Returning results requires an additional response queue or `Future` object.
2. **Memory Copy Overhead**: Objects passed through queues are held in memory until consumed.

---

## 6. Real-World Use Cases

### Domain 1: Healthcare — Diagnostic Imaging Processing Pipeline
- **Problem**: CT scanners upload high-resolution DICOM images (300MB each). Sequential processing blocks scanner workstations.
- **Solution**: The scanner uploads DICOM paths to a `queue.Queue(maxsize=10)`. A pool of 4 worker threads pulls scans from the queue, performs radiological image adjustments, and saves them to PACS storage concurrently.

### Domain 2: eCommerce — Asynchronous Order Processing Architecture
- **Problem**: When a customer checks out, the web server must enqueue tasks for payment settlement, inventory reduction, receipt email delivery, and shipping manifest creation.
- **Solution**: A central order queue receives checkout payloads. Specialized consumer worker threads dequeue tasks and route them to external microservices without delaying the HTTP checkout response.

### Domain 3: Banking — Real-Time High-Value Fraud Detection
- **Problem**: Millions of credit card swipes must be evaluated. High-value transactions (>$10,000) must be evaluated with higher urgency than $2 coffee charges.
- **Solution**: Incoming swipe events are queued into a `queue.PriorityQueue`, ensuring high-dollar transactions are prioritized by fraud analysis workers in sub-100ms response windows.

---

## 7. Best Practices

### Practice 1: Always Call `queue.task_done()` for Every `queue.get()`
**When to apply**: In any consumer processing loop.
**Why**: If `task_done()` is omitted, `queue.join()` will hang forever because the unfinished task counter will never reach zero.

```python
# GOOD PRACTICE
item = q.get()
try:
    process(item)
finally:
    q.task_done() # Always called even if process() fails!
```

### Practice 2: Send One Sentinel per Consumer Thread for Shutdown
**When to apply**: Shutting down multiple consumer workers.
**Why**: A single `None` sentinel will only be consumed by the *first* worker that picks it up, leaving other workers blocked on `q.get()`.

```python
# GOOD PRACTICE (Shutting down 3 worker threads)
for _ in range(num_workers):
    q.put(None)
```

### Practice 3: Always Use `timeout` with `get()` in Long-Running Daemons
**When to apply**: In consumer loops that need to respond to application shutdown signals.
**Why**: A thread blocked on `q.get()` with no timeout cannot check stop flags or respond to `SIGINT`.

---

## 8. Top 3 Mistakes

### Mistake 1: Calling `task_done()` More Times Than `get()`
#### What's the Problem?
Invoking `queue.task_done()` when no task was retrieved or calling it multiple times for one item.
#### Why It Happens
Calling `task_done()` both inside a helper and in a finally block.
#### Impact
Raises `ValueError: task_done() called too many times`.
#### Incorrect Approach
```python
item = q.get()
handle_item(item) # Calls q.task_done() internally
q.task_done()     # Raises ValueError!
```
#### Correct Approach
```python
item = q.get()
handle_item(item) # Does NOT call task_done()
q.task_done()     # Exactly 1 task_done per get
```
#### Lesson Learned
Ensure exactly one `task_done()` call corresponds to each successful `get()`.

---

### Mistake 2: Missing Backpressure with Unbounded Queues
#### What's the Problem?
Creating `queue.Queue()` without specifying `maxsize` in high-throughput data streams.
#### Why It Happens
Default constructor `queue.Queue()` creates an unbounded queue (`maxsize=0`).
#### Impact
If producers run faster than consumers, millions of objects accumulate in memory until the process crashes with `MemoryError`.
#### Correct Approach
```python
# Always set a sensible bounded capacity for production queues
work_queue = queue.Queue(maxsize=1000)
```
#### Lesson Learned
Always configure bounded queues to enforce backpressure against upstream data bursts.

---

### Mistake 3: Storing Uncomparable Objects in `PriorityQueue`
#### What's the Problem?
Putting custom tuples `(priority, object)` where `object` does not define comparison operators (`<`).
#### Why It Happens
When two items have identical priority numbers, `PriorityQueue` tries to break the tie by comparing the objects themselves.
#### Impact
Raises `TypeError: '<' not supported between instances of 'MyClass' and 'MyClass'`.
#### Correct Approach
```python
# Use dataclass with compare=False or store (priority, count, object) where count is unique
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    data: Any = field(compare=False)
```
#### Lesson Learned
Ensure items stored in `PriorityQueue` have non-colliding comparison keys or specify `compare=False` on payload objects.
