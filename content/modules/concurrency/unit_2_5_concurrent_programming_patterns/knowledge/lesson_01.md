# Unit 2.5: Concurrent Programming Patterns

---

## 1. What

### Simple Definition
Imagine running a busy restaurant kitchen. If the chef had to take customer orders, chop vegetables, cook the steak, wash the dishes, and serve the tables all by themselves, customers would wait hours for their meals. 

To fix this, kitchens divide work among specialists:
- **Waiters** take orders and place ticket slips on an order wheel.
- **Line cooks** pick up tickets from the wheel, prepare meals, and place them under a warming lamp.
- **Runners** take finished plates from the warming lamp to tables.

In computer software, **Concurrent Programming Patterns** are proven blueprints that do the exact same thing for computer programs. Instead of letting multiple threads or processes randomly fight over variables and crash your system, these patterns organize work into safe, predictable, and orderly assembly lines.

### The Core Problem It Solves
When programs try to do multiple things at the same time without an organized blueprint, they quickly run into dangerous traps:
1. **Race Conditions**: Two workers try to modify the same bank balance or patient chart at the exact same millisecond, corrupting the data.
2. **Deadlocks**: Two workers freeze forever because Worker A is waiting for a tool held by Worker B, while Worker B is waiting for a tool held by Worker A.
3. **Starvation**: A busy worker hogs all resources while other workers wait forever and never get a turn to run.
4. **Memory Exhaustion**: The program accepts millions of incoming requests faster than it can process them, running out of RAM and crashing the server.

Concurrent programming patterns solve these issues by giving software engineers battle-tested structures to coordinate tasks safely.

### Key Patterns in This Unit
- **Producer–Consumer Pattern**: One group of workers produces tasks, and another group processes them through a shared waiting line (queue).
- **Worker Pool Pattern**: A fixed group of reusable workers that pick up jobs from a shared queue, preventing thread creation overhead.
- **Task Queue Pattern**: An organized buffer that holds background jobs until a worker is ready to process them.
- **Fan-Out / Fan-In Pattern**: Splitting a big task into several smaller jobs running simultaneously (Fan-Out), and combining their results into one final answer (Fan-In).
- **Immutability & Statelessness**: Designing data that can never be modified after creation, making it 100% safe to share across threads without locks.

---

## 2. Examples

Let us explore 4 complete, runnable examples that build from simple to production-grade architectures.

### Example 1: Basic Producer–Consumer with Bounded Queue and Poison Pill
The simplest and most important pattern. The producer puts numbers into a queue. When finished, it puts a special marker called a **Poison Pill** (`None`) to tell the consumer to stop.

```python
import queue
import threading
import time

# Create a queue with a maximum capacity of 3 items
task_queue = queue.Queue(maxsize=3)

def producer():
    """Generates 5 tasks and sends them to the queue."""
    for task_id in range(1, 6):
        print(f"[Producer] Creating order #{task_id}...")
        task_queue.put(task_id)  # Blocks if the queue is full (maxsize=3)
        print(f"[Producer] Order #{task_id} added to queue. (Queue size: {task_queue.qsize()})")
        time.sleep(0.05)
    
    # Send sentinel 'poison pill' to signal completion
    print("[Producer] Done generating orders. Sending poison pill.")
    task_queue.put(None)

def consumer():
    """Fetches tasks from the queue and processes them."""
    while True:
        task = task_queue.get()  # Waits until an item is available
        if task is None:
            task_queue.task_done()
            print("[Consumer] Poison pill received! Shutting down gracefully.")
            break
        
        print(f"  --> [Consumer] Cooking order #{task}...")
        time.sleep(0.1)  # Simulate time taken to cook
        print(f"  --> [Consumer] Order #{task} finished!")
        task_queue.task_done()

# Start both threads
t_prod = threading.Thread(target=producer, name="ProducerThread")
t_cons = threading.Thread(target=consumer, name="ConsumerThread")

t_prod.start()
t_cons.start()

t_prod.join()
t_cons.join()
print("All tasks processed cleanly!")
```

**Console Output**:
```text
[Producer] Creating order #1...
[Producer] Order #1 added to queue. (Queue size: 1)
  --> [Consumer] Cooking order #1...
[Producer] Creating order #2...
[Producer] Order #2 added to queue. (Queue size: 1)
[Producer] Creating order #3...
[Producer] Order #3 added to queue. (Queue size: 2)
  --> [Consumer] Order #1 finished!
  --> [Consumer] Cooking order #2...
[Producer] Creating order #4...
[Producer] Order #4 added to queue. (Queue size: 2)
[Producer] Creating order #5...
[Producer] Order #5 added to queue. (Queue size: 3)
  --> [Consumer] Order #2 finished!
  --> [Consumer] Cooking order #3...
[Producer] Done generating orders. Sending poison pill.
  --> [Consumer] Order #3 finished!
  --> [Consumer] Cooking order #4...
  --> [Consumer] Order #4 finished!
  --> [Consumer] Cooking order #5...
  --> [Consumer] Order #5 finished!
  --> [Consumer] Poison pill received! Shutting down gracefully.
All tasks processed cleanly!
```

---

### Example 2: Worker Pool Processing Multiple Jobs
Instead of only one consumer, this example uses a pool of 3 worker threads. A single queue feeds all 3 workers simultaneously.

```python
import queue
import threading
import time

job_queue = queue.Queue()
results_lock = threading.Lock()
completed_jobs = []

def worker(worker_id: int):
    """Worker loop that continuously drains the job queue."""
    while True:
        job = job_queue.get()
        if job is None:
            job_queue.task_done()
            break
        
        # Process job
        result = job * job
        time.sleep(0.05)  # Simulate computational work
        
        with results_lock:
            completed_jobs.append((job, result, worker_id))
            print(f"Worker {worker_id} processed job {job} -> result {result}")
        
        job_queue.task_done()

# 1. Spawn a fixed pool of 3 workers
workers = []
for i in range(1, 4):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    workers.append(t)

# 2. Enqueue 6 jobs
for number in [10, 20, 30, 40, 50, 60]:
    job_queue.put(number)

# 3. Wait for all jobs to be completed
job_queue.join()

# 4. Shut down workers by sending one poison pill per worker
for _ in workers:
    job_queue.put(None)

for t in workers:
    t.join()

print(f"Total completed jobs: {len(completed_jobs)}")
```

**Console Output**:
```text
Worker 1 processed job 10 -> result 100
Worker 2 processed job 20 -> result 400
Worker 3 processed job 30 -> result 900
Worker 1 processed job 40 -> result 1600
Worker 2 processed job 50 -> result 2500
Worker 3 processed job 60 -> result 3600
Total completed jobs: 6
```

---

### Example 3: Real-World Healthcare Scenario (Fan-Out / Fan-In Diagnostics)
In a hospital Emergency Department, a doctor clicks on a trauma patient's profile. We need to query three different remote databases at the same time:
1. Patient Allergies & History (from the central EHR)
2. Blood Chemistry & Troponin Levels (from the Pathology Lab)
3. Bedside Heart Rate & Oxygen (from Bedside IoT Monitors)

Instead of waiting sequentially (0.1s + 0.1s + 0.1s = 0.3s), we **Fan-Out** all three queries simultaneously and **Fan-In** the results in parallel (~0.1s total).

```python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class PatientRecord:
    patient_id: str
    allergies: tuple
    cardiac_troponin: float
    heart_rate: int
    spo2: int

def fetch_allergies(patient_id: str) -> tuple:
    time.sleep(0.08)  # Simulated remote network call
    return ("Penicillin", "Sulfa drugs")

def fetch_lab_troponin(patient_id: str) -> float:
    time.sleep(0.09)  # Simulated lab pathology query
    return 0.03  # Normal range: < 0.04 ng/mL

def fetch_bedside_vitals(patient_id: str) -> tuple:
    time.sleep(0.07)  # Simulated IoT telemetry fetch
    return (78, 98)  # HR=78 bpm, SPO2=98%

def build_patient_summary(patient_id: str) -> PatientRecord:
    start_time = time.perf_counter()
    print(f"[Fan-Out] Dispatching parallel clinical queries for {patient_id}...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Fan-Out: Launch all 3 independent calls in parallel
        future_allergies = executor.submit(fetch_allergies, patient_id)
        future_labs = executor.submit(fetch_lab_troponin, patient_id)
        future_vitals = executor.submit(fetch_bedside_vitals, patient_id)

        # Fan-In: Collect and assemble results
        allergies = future_allergies.result()
        troponin = future_labs.result()
        hr, spo2 = future_vitals.result()

    elapsed = time.perf_counter() - start_time
    print(f"[Fan-In] Composite patient record assembled in {elapsed:.3f} seconds!")

    return PatientRecord(
        patient_id=patient_id,
        allergies=allergies,
        cardiac_troponin=troponin,
        heart_rate=hr,
        spo2=spo2
    )

record = build_patient_summary("PT-9042")
print("Verified Clinical Record:", record)
```

**Console Output**:
```text
[Fan-Out] Dispatching parallel clinical queries for PT-9042...
[Fan-In] Composite patient record assembled in 0.092 seconds!
Verified Clinical Record: PatientRecord(patient_id='PT-9042', allergies=('Penicillin', 'Sulfa drugs'), cardiac_troponin=0.03, heart_rate=78, spo2=98)
```

---

### Example 4: Deadlock Prevention Using Sorted Lock Hierarchy
A classic deadlock happens when Thread 1 holds Lock A and waits for Lock B, while Thread 2 holds Lock B and waits for Lock A. This example shows how enforcing an **alphabetical lock hierarchy** completely prevents deadlocks.

```python
import threading
import time

class BankAccount:
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()

def transfer_funds(from_acc: BankAccount, to_acc: BankAccount, amount: float):
    """
    Transfers money safely between accounts.
    Rule: Always acquire locks in alphabetical order of account_id!
    """
    # Sort accounts by ID so all threads acquire locks in the exact same order
    first_acc, second_acc = sorted([from_acc, to_acc], key=lambda acc: acc.account_id)
    
    print(f"[Transfer] Acquiring lock for {first_acc.account_id}...")
    with first_acc.lock:
        print(f"[Transfer] Acquired {first_acc.account_id}. Acquiring lock for {second_acc.account_id}...")
        with second_acc.lock:
            if from_acc.balance >= amount:
                from_acc.balance -= amount
                to_acc.balance += amount
                print(f"SUCCESS: Transferred ${amount} from {from_acc.account_id} to {to_acc.account_id}")
            else:
                print(f"FAILED: Insufficient funds in {from_acc.account_id}")

acc1 = BankAccount("ACC_ALPHA", 500.0)
acc2 = BankAccount("ACC_BETA", 300.0)

# Thread 1 transfers from ALPHA to BETA
t1 = threading.Thread(target=transfer_funds, args=(acc1, acc2, 100.0))
# Thread 2 simultaneously transfers from BETA to ALPHA (opposite order)
t2 = threading.Thread(target=transfer_funds, args=(acc2, acc1, 50.0))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Final Balances -> ALPHA: ${acc1.balance}, BETA: ${acc2.balance}")
```

**Console Output**:
```text
[Transfer] Acquiring lock for ACC_ALPHA...
[Transfer] Acquired ACC_ALPHA. Acquiring lock for ACC_BETA...
[Transfer] Acquiring lock for ACC_ALPHA...
SUCCESS: Transferred $100.0 from ACC_ALPHA to ACC_BETA
[Transfer] Acquired ACC_ALPHA. Acquiring lock for ACC_BETA...
SUCCESS: Transferred $50.0 from ACC_BETA to ACC_ALPHA
Final Balances -> ALPHA: $450.0, BETA: $350.0
```

---

## 3. Explanation

### Step-by-Step Breakdown: How Producer–Consumer Works

```text
+-------------------+                                               +------------------+
|   Producer 1      | ---------\                                /-> |   Worker 1       |
+-------------------+           \    +---------------------+   /    +------------------+
                                 +-> |  Bounded Queue      | -+
+-------------------+           /    |  [Task 1, Task 2]   |   \    +------------------+
|   Producer 2      | ---------/     +---------------------+    \-> |   Worker 2       |
+-------------------+                    |         |                +------------------+
                                         |         |
                          If Queue is FULL         If Queue is EMPTY
                          Producer waits           Worker waits
```

1. **Decoupled Speed**: The Producer can run as fast or slow as it wants. It does not call the Consumer directly.
2. **Buffer and Backpressure**: The queue acts as a temporary buffer. If consumers fall behind, the queue holds the work. If the queue reaches its maximum capacity (`maxsize=3`), Python automatically pauses the producer until a consumer finishes an item. This prevents your server from running out of memory.
3. **Thread Safety**: Python's `queue.Queue` internally manages thread synchronization using locks and conditions. You never need to write manual locks around `queue.put()` or `queue.get()`.
4. **Task Completion Tracking**: When a consumer calls `queue.task_done()`, the queue decrements an internal unfinished task counter. When `queue.join()` is called by the main thread, it blocks until every single task placed on the queue has received a corresponding `task_done()`.

---

### Step-by-Step Breakdown: The Fan-Out / Fan-In Pattern

```text
               +--------------------------------------------+
               |            Incoming Client Request         |
               +--------------------------------------------+
                                     |
                                 [FAN-OUT]
                   Dispatches 3 tasks at the exact same time
                   /                 |                  \
                  v                  v                   v
          +---------------+  +---------------+  +---------------+
          | Query Service |  | Query Service |  | Query Service |
          |   A (Labs)    |  |  B (Billing)  |  |  C (Pharmacy) |
          +---------------+  +---------------+  +---------------+
                  \                  |                  /
                   \                 |                 /
                    +----------------+----------------+
                                     |
                                  [FAN-IN]
                     Waits for all 3 tasks to finish and
                     assembles one unified response dictionary
                                     |
                                     v
                       +---------------------------+
                       | Unified Composite Report  |
                       +---------------------------+
```

1. **Fan-Out**: When a single request needs data from multiple independent sources, the coordinator thread creates asynchronous tasks or submits jobs to a `ThreadPoolExecutor`. All sub-requests are dispatched in parallel.
2. **Scatter-Gather Execution**: The workers execute concurrently over the network or on multiple CPU cores.
3. **Fan-In**: The coordinator waits for all futures to resolve using `concurrent.futures.as_completed()` or `asyncio.gather()`. It captures any partial errors, combines healthy payloads, and returns a single clean object.

---

### Understanding the 3 Deadly Concurrency Traps

#### 1. Deadlock
- **What is it?** Two or more threads are permanently stuck, each holding a lock that the other needs.
- **Under the Hood**: Thread 1 holds Lock X and asks the operating system for Lock Y. Thread 2 holds Lock Y and asks for Lock X. Neither thread can proceed, and neither will release the lock they hold.
- **The Solution**: 
  - **Lock Ordering**: Always acquire locks in a consistent global order (e.g., sorted by resource ID).
  - **Timeouts**: Never use blocking `lock.acquire()` without a timeout (`lock.acquire(timeout=2.0)`).

#### 2. Starvation
- **What is it?** A thread is ready to run, but other higher-priority threads keep jumping ahead of it, so it never gets CPU time or queue items.
- **The Solution**: Use fair First-In, First-Out (FIFO) queues such as standard `queue.Queue` so every request gets served in the order it arrived.

#### 3. Race Conditions
- **What is it?** Two threads read and write to the same shared variable simultaneously. The final value depends on pure timing luck.
- **The Solution**: Avoid shared mutable state entirely. Pass messages through queues or use immutable data structures (`dataclass(frozen=True)`).

---

### Comparison of Concurrency Coordination Patterns

| Pattern | Flow Direction | Primary Benefit | When to Use | When to Avoid |
| :--- | :--- | :--- | :--- | :--- |
| **Producer–Consumer** | One-way pipeline via queue | Smooths out traffic spikes; decouples producers from consumers | File processing, log ingestion, background email sending | Simple synchronous requests where caller needs an immediate return value |
| **Worker Pool** | 1 queue feeding N workers | Bounds maximum resource usage (avoids creating 10,000 threads) | Web servers, database query pools, thumbnail generators | Long-running endless background tasks that tie up a worker forever |
| **Fan-Out / Fan-In** | 1 request splits into N jobs, then rejoins | Minimizes total wall-clock response time | Aggregating data from multiple microservices or APIs | Workloads where Task B strictly depends on the result of Task A |
| **Task Queue** | Asynchronous persistent backlog | Fault tolerance; jobs survive worker restarts | Heavy background video rendering, daily billing generation | Low-latency in-memory operations (<5 milliseconds) |

---

## 4. Why Concurrent Patterns Matter

### 1. Eliminating Bugs That Are Impossible to Reproduce
Bugs caused by manual locks and shared variables are notoriously hard to debug. They only happen under heavy production load, and running the code in a debugger changes the timing and makes the bug disappear (often called "Heisenbugs"). Using standardized patterns like Producer-Consumer completely isolates state, making concurrency bugs structurally impossible.

### 2. Built-In Protection Against Server Crashes (Backpressure)
If an eCommerce store holds a flash sale and 50,000 users click "Buy" in 10 seconds, creating 50,000 threads will immediately crash the server with an `OutOfMemoryError`. A bounded Producer-Consumer pattern with a fixed Worker Pool accepts jobs into a memory-capped queue and processes them at a steady, sustainable pace.

### 3. Dramatic Latency Reductions
In modern cloud architectures, data is split across dozens of microservices. If your web page queries 5 services sequentially, each taking 100ms, the user waits 500ms. By applying Fan-Out / Fan-In, all 5 queries happen at the same time, reducing page load latency from 500ms down to 105ms.

### 4. Clean and Maintainable Code
Junior developers often scatter `threading.Lock()` calls throughout their codebase. As the software grows, nobody knows which lock protects which variable, leading to deadlocks. Concurrent patterns replace messy synchronization locks with clean, readable message passing.

---

## 5. Advantages & Disadvantages

### Advantages

#### 1. Complete Separation of Concerns
Producers only care about creating work; consumers only care about executing work. Neither needs to know how the other is implemented.
```python
# The producer doesn't know or care whether 1 or 50 consumers are listening
queue.put(new_order)
```

#### 2. Automatic Throttling (Backpressure)
Setting `queue.Queue(maxsize=100)` means the system will never store more than 100 unprocessed items in RAM. If the queue fills up, producers automatically pause until workers catch up.

#### 3. Effortless Scale-Up
If tasks are taking too long to process, you do not need to rewrite your application logic. You simply increase the worker pool size from 4 workers to 16 workers.

---

### Disadvantages

#### 1. Increased Architectural Complexity
Compared to writing a simple for-loop, concurrent patterns require managing queues, worker thread lifecycles, and shutdown signals (poison pills).

#### 2. Memory Overhead for Queued Tasks
While bounded queues protect against crashes, enqueued items still occupy memory. Storing large payloads (e.g., 50MB video files) directly in an in-memory queue will exhaust system RAM.
*Workaround*: Store large files in object storage (e.g., S3 or local disk) and pass only lightweight file paths or IDs through the queue.

#### 3. Complex Error Handling Across Boundaries
If a worker thread crashes while processing a job from a queue, the producer does not automatically get an exception.
*Workaround*: Wrap worker logic in a `try...except` block and push error status objects to a dedicated error queue or return composite result objects.

---

## 6. Real-World Use Cases

### Domain 1: Healthcare (Patient Admission & Triage Pipeline)
- **Problem**: When a patient arrives at the Emergency Department, multiple clinical systems must be notified: Bed Management, Pharmacy, Patient Billing, and the On-Duty Nursing Station. If done synchronously, the triage kiosk freezes while waiting for each system.
- **Solution**: The admission kiosk acts as a **Producer**, placing an admission event onto a priority queue. A **Worker Pool** handles downstream notifications asynchronously.
- **Code Example**:
```python
import queue
import threading

triage_queue = queue.PriorityQueue()

def admit_patient(urgency_level: int, patient_name: str):
    # Urgency 1 = Cardiac Arrest (highest); Urgency 5 = Mild Fever
    triage_queue.put((urgency_level, patient_name))
    print(f"Admitted {patient_name} with urgency {urgency_level}")

def er_triage_worker():
    while True:
        urgency, name = triage_queue.get()
        print(f"  [Triage Nurse] Attending to {name} (Priority {urgency})")
        triage_queue.task_done()

nurse_thread = threading.Thread(target=er_triage_worker, daemon=True)
nurse_thread.start()

admit_patient(3, "John Doe (Broken Arm)")
admit_patient(1, "Jane Smith (Chest Pain)")
triage_queue.join()
```
- **Benefits**: Jane Smith (Priority 1) is immediately triaged before John Doe (Priority 3), even though John arrived first. The triage kiosk remains instant and responsive.

---

### Domain 2: eCommerce (Order Checkout & Inventory Allocation)
- **Problem**: During high-volume flash sales, thousands of shoppers purchase items simultaneously. If multiple threads decrement inventory directly in the database without coordination, overselling occurs.
- **Solution**: A **Worker Pool** pattern with a bounded task queue processes inventory deductions sequentially per product or distributes checkout jobs across a fixed set of workers.
- **Code Example**:
```python
from concurrent.futures import ThreadPoolExecutor

inventory = {"IPHONE_15": 3}

def process_purchase(order_id: str, item: str) -> str:
    global inventory
    # Protected order processing
    if inventory.get(item, 0) > 0:
        inventory[item] -= 1
        return f"Order {order_id} approved. Remaining {item}: {inventory[item]}"
    return f"Order {order_id} rejected. Out of stock!"

orders = [(f"ORD-{i}", "IPHONE_15") for i in range(1, 6)]

with ThreadPoolExecutor(max_workers=2) as pool:
    # Notice: For real production, use atomic database updates or isolated actor queues
    results = list(pool.map(lambda o: process_purchase(o[0], o[1]), orders))

for res in results:
    print(res)
```
- **Benefits**: Enforces orderly transaction throughput and prevents database connection pool exhaustion.

---

### Domain 3: Banking (Fraud Detection Multi-Engine Scoring)
- **Problem**: When a customer swipes a debit card at a point-of-sale terminal, the bank has at most 100 milliseconds to decide whether to approve or flag the transaction. The bank runs three separate fraud detection models:
  1. Geographic location velocity check
  2. Machine learning spending anomaly detector
  3. Blacklisted merchant sanctions check
- **Solution**: **Fan-Out / Fan-In**. The authorization gateway fans out the transaction payload to all 3 scoring engines simultaneously and aggregates their scores before issuing the approval code.
- **Code Example**:
```python
from concurrent.futures import ThreadPoolExecutor

def check_geo_velocity(card_id: str) -> int:
    return 0  # 0 = Low Risk, 100 = High Risk

def check_ml_anomaly(card_id: str) -> int:
    return 15

def check_merchant_sanctions(card_id: str) -> int:
    return 0

def evaluate_card_swipe(card_id: str) -> bool:
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_geo = executor.submit(check_geo_velocity, card_id)
        f_ml = executor.submit(check_ml_anomaly, card_id)
        f_sanc = executor.submit(check_merchant_sanctions, card_id)

        # Fan-in: combine risk scores
        total_risk = f_geo.result() + f_ml.result() + f_sanc.result()
    
    # Approve if total combined risk score is under 50
    return total_risk < 50

print("Card Swipe Approved:", evaluate_card_swipe("CARD-4421-9981"))
```
- **Benefits**: All three checks complete within the duration of the slowest single check (~15ms) rather than their cumulative sum (~45ms), staying well under the 100ms merchant timeout SLA.

---

## 7. Best Practices

### Practice 1: Always Cap Your Queue Sizes
**When to apply**: Whenever you use `queue.Queue()` in production.
**Why**: Default `queue.Queue()` has an unbounded capacity (`maxsize=0`). If a producer produces faster than workers can consume, millions of items will pile up in memory until the operating system kills Python with an Out-of-Memory (OOM) error.

```python
# Good Practice
import queue
# Bounded queue: holds at most 500 items, then throttles producer
safe_queue = queue.Queue(maxsize=500)
```
**Why This Works Better**: Provides automatic backpressure, protecting system stability.

---

### Practice 2: Use Sentinels (Poison Pills) for Worker Shutdown
**When to apply**: When shutting down worker threads.
**Why**: Forcibly terminating threads or using boolean flags like `is_running = False` can cause workers to exit in the middle of writing a file or processing a transaction, leaving data half-written.

```python
# Good Practice
SENTINEL = object()  # Unique sentinel marker

def worker(q):
    while True:
        task = q.get()
        if task is SENTINEL:
            q.task_done()
            break  # Exit cleanly only when all previous tasks are done
        process(task)
        q.task_done()
```
**Why This Works Better**: Ensures every single pending task in the queue is processed before the worker thread exits.

---

### Practice 3: Prefer Immutable Data Structures Across Threads
**When to apply**: When passing clinical, financial, or user records between threads.
**Why**: If multiple threads share a regular Python dictionary or list, one thread might modify a field while another thread is reading it, leading to subtle race conditions.

```python
# Good Practice
from dataclasses import dataclass

@dataclass(frozen=True)
class TransactionRecord:
    transaction_id: str
    amount: float
    timestamp: str

# Attempting tx.amount = 0.0 raises FrozenInstanceError
tx = TransactionRecord("TX-101", 450.00, "2026-10-05T14:00:00Z")
```
**Why This Works Better**: Data that cannot be changed is mathematically impossible to corrupt with a race condition.

---

### Practice 4: Always Sort Resources to Prevent Deadlocks
**When to apply**: Whenever a thread must acquire more than one lock at the same time.
**Why**: If Thread 1 acquires Lock A then Lock B, and Thread 2 acquires Lock B then Lock A, your program will inevitably deadlock.

```python
# Good Practice
def transfer(account_a, account_b, amount):
    # Always sort locks by a consistent unique identifier
    first, second = sorted([account_a, account_b], key=lambda a: a.id)
    with first.lock:
        with second.lock:
            # Transfer funds safely
            pass
```
**Why This Works Better**: Guarantees that all threads acquire locks in the exact same sequence, making circular wait deadlocks impossible.

---

### Practice 5: Always Call `queue.task_done()` Inside a `finally` Block
**When to apply**: Inside every consumer worker loop.
**Why**: If an unexpected exception happens while processing a task, `task_done()` is skipped. When the main thread calls `queue.join()`, it will hang forever because it believes a task is still running.

```python
# Good Practice
def worker(q):
    while True:
        item = q.get()
        try:
            process_item(item)
        except Exception as e:
            print(f"Error processing item: {e}")
        finally:
            q.task_done()  # ALWAYS runs, preventing queue.join() from hanging
```
**Why This Works Better**: Prevents deadlock and thread hangs during errors.

---

## 8. Top 3 Mistakes & Anti-Patterns

### Mistake 1: Forgetting to Call `queue.task_done()`
#### What's the Problem?
The worker gets an item from the queue and processes it, but forgets to call `task_queue.task_done()`.

#### Why It Happens
Developers assume that just fetching the item via `queue.get()` is enough.

#### Impact
- The main thread calls `task_queue.join()` and freezes indefinitely.
- The program appears to hang forever at shutdown.

#### Incorrect Approach
```python
import queue

q = queue.Queue()
q.put("job_1")

item = q.get()
print(f"Processed {item}")
# Missing q.task_done()!

q.join()  # HANGS FOREVER! Python never exits.
```

#### Correct Approach
```python
import queue

q = queue.Queue()
q.put("job_1")

item = q.get()
try:
    print(f"Processed {item}")
finally:
    q.task_done()  # Notifies the queue that this task is complete

q.join()  # Exits immediately and cleanly!
```

#### Lesson Learned
Every call to `queue.get()` that successfully receives a task must eventually be paired with a corresponding `queue.task_done()`.

---

### Mistake 2: Sharing Mutable Lists or Dictionaries Across Workers
#### What's the Problem?
Workers append results directly to a standard Python list `results.append(...)` without synchronization, or modify a shared dictionary.

#### Why It Happens
In single-threaded code, appending to a list is standard practice. Developers forget that under high concurrency, multiple threads can overwrite internal pointers or create corrupted records.

#### Impact
- Missing entries in the results list.
- Intermittent `RuntimeError: dictionary changed size during iteration`.
- Unpredictable data loss that only happens in production.

#### Incorrect Approach
```python
import threading

shared_results = []

def worker(val):
    # DANGEROUS: Multiple threads modifying shared mutable list directly
    shared_results.append(val * 2)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]
for t in threads: t.start()
for t in threads: t.join()
```

#### Correct Approach
```python
import queue
import threading

results_queue = queue.Queue()

def worker(val):
    # SAFE: Return results through a thread-safe queue
    results_queue.put(val * 2)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]
for t in threads: t.start()
for t in threads: t.join()

# Drain results cleanly
results = []
while not results_queue.empty():
    results.append(results_queue.get())
```

#### Lesson Learned
Do not share mutable collections directly between threads. Pass data through thread-safe queues or use immutable return values with `concurrent.futures`.

---

### Mistake 3: Acquiring Multiple Locks Without Enforcing Lock Order
#### What's the Problem?
Two different functions acquire the same set of locks in reverse order, creating a classic circular deadlock.

#### Why It Happens
Function A locks Resource 1 then Resource 2. Later, another developer writes Function B and locks Resource 2 then Resource 1.

#### Impact
- Both threads freeze permanently.
- The entire application locks up and stops responding to user traffic.
- Requires restarting the server process to recover.

#### Incorrect Approach
```python
import threading

lock_x = threading.Lock()
lock_y = threading.Lock()

# Worker 1 runs this:
def task_1():
    with lock_x:
        with lock_y:
            pass

# Worker 2 runs this simultaneously:
def task_2():
    with lock_y:      # Opposite order!
        with lock_x:  # DEADLOCK: Worker 1 has X, Worker 2 has Y!
            pass
```

#### Correct Approach
```python
import threading

lock_x = threading.Lock()
lock_y = threading.Lock()

# Both workers acquire locks in the exact same predetermined order:
def safe_task_1():
    with lock_x:
        with lock_y:
            pass

def safe_task_2():
    with lock_x:  # Same order as task 1!
        with lock_y:
            pass
```

#### Lesson Learned
Always establish a strict, global lock acquisition hierarchy. If multiple resources must be locked, acquire them in a consistent, sorted order across your entire codebase.
