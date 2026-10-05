---
title: "Thread Synchronization"
type: knowledge
module: threads
unit: unit_1_3_thread_synchronization
order: 3
difficulty: intermediate
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - race-conditions
    - critical-sections
    - lock
    - rlock
    - semaphore
    - condition
    - deadlocks
---

# Unit 1.3: Thread Synchronization

## 1. What

**Thread Synchronization** refers to the mechanisms and coordination protocols used to ensure that two or more concurrent threads do not simultaneously execute critical sections or access shared mutable state in a manner that results in data corruption, memory inconsistency, or race conditions.

### Shared Mutable State and Race Conditions
In a multithreaded Python process, all threads share the same global variables, object heaps, and instance attributes. A **race condition** occurs when the outcome of a program depends on the non-deterministic scheduling, timing, or interleaving of instructions between competing threads. 

A common misconception is that because CPython has a Global Interpreter Lock (GIL), Python operations are automatically thread-safe. **This is false.** The GIL only protects Python runtime internal C data structures; it does *not* protect application-level business state. A single line of Python code such as:
```python
balance += amount
```
is compiled into four distinct bytecode instructions:
1. `LOAD_FAST` (read balance)
2. `LOAD_FAST` (read amount)
3. `BINARY_OP` (add)
4. `STORE_FAST` (write back balance)

If the OS scheduler switches threads between step 1 and step 4, one thread overwrites the other thread's calculation, causing a silent, catastrophic **lost update**.

### Critical Sections & Mutex Primitives
A **critical section** is a section of code that accesses shared mutable resources and must be executed atomically by at most one thread at a time. Synchronization primitives—`Lock`, `RLock`, `Semaphore`, `Event`, and `Condition`—provide synchronization contracts that guarantee mutual exclusion, capacity throttling, and inter-thread signaling.

---

## 2. Example

### Example 1: Demonstrating a Race Condition vs. `Lock` Protection
Demonstrating how 10 concurrent threads corrupt an unprotected integer, and how a `threading.Lock` restores mathematical correctness.

```python
import threading
import time

# --- Part A: Unprotected Counter (Race Condition) ---
unprotected_counter = 0

def unsafe_worker():
    global unprotected_counter
    for _ in range(10000):
        # Read-modify-write is NOT atomic
        unprotected_counter += 1

threads = [threading.Thread(target=unsafe_worker) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Unprotected Counter: Expected 100000, Got: {unprotected_counter}")

# --- Part B: Protected Counter using Lock ---
safe_counter = 0
counter_lock = threading.Lock()

def safe_worker():
    global safe_counter
    for _ in range(10000):
        # Context manager automatically acquires and releases lock
        with counter_lock:
            safe_counter += 1

threads = [threading.Thread(target=safe_worker) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Protected Counter:   Expected 100000, Got: {safe_counter}")
```

**Expected Output:**
```text
Unprotected Counter: Expected 100000, Got: 78432   <-- Corrupted by lost updates!
Protected Counter:   Expected 100000, Got: 100000  <-- Perfectly synchronized!
```

---

### Example 2: Reentrant Lock (`RLock`) for Recursive or Nested Calls
A standard `Lock` cannot be acquired twice by the *same* thread without deadlocking itself. `RLock` tracks the acquiring thread and an internal recursion counter.

```python
import threading

class BankAccount:
    def __init__(self, initial_balance: float):
        self.balance = initial_balance
        self._lock = threading.RLock() # Reentrant lock

    def deposit(self, amount: float):
        with self._lock:
            self.balance += amount

    def deposit_with_bonus(self, amount: float, bonus: float):
        with self._lock: # First acquisition
            self.deposit(amount) # Second acquisition inside deposit()!
            self.balance += bonus

account = BankAccount(100.0)
account.deposit_with_bonus(50.0, 5.0)
print(f"Final Balance: ${account.balance:.2f}")
```

**Expected Output:**
```text
Final Balance: $155.00
```
*Note: If `self._lock` were a standard `Lock`, `deposit_with_bonus` would hang forever upon entering `deposit()`, creating a self-deadlock.*

---

### Example 3: Real-World Healthcare Scenario — Pharmacy Medication Dispenser
A hospital pharmacy manages critical vials of emergency medication (e.g. Epinephrine). Multiple surgical teams may request vials concurrently.

```python
import threading
import time
from typing import Dict

class PharmacyDispenser:
    def __init__(self, stock: Dict[str, int]):
        self._inventory = stock
        self._lock = threading.Lock()
        self.dispensed_log = []

    def request_medication(self, drug_name: str, quantity: int, doctor_id: str) -> bool:
        with self._lock:
            available = self._inventory.get(drug_name, 0)
            if available >= quantity:
                # Simulate verification delay
                time.sleep(0.01)
                self._inventory[drug_name] -= quantity
                self.dispensed_log.append((doctor_id, drug_name, quantity))
                print(f"[SUCCESS] Dispensed {quantity}x {drug_name} to {doctor_id}. Remaining: {self._inventory[drug_name]}")
                return True
            else:
                print(f"[REJECTED] {doctor_id} requested {quantity}x {drug_name}, but only {available} available.")
                return False

dispenser = PharmacyDispenser({"Epinephrine": 5})

# 3 surgical teams request medication concurrently
t1 = threading.Thread(target=dispenser.request_medication, args=("Epinephrine", 3, "Dr. Alice"))
t2 = threading.Thread(target=dispenser.request_medication, args=("Epinephrine", 3, "Dr. Bob"))
t3 = threading.Thread(target=dispenser.request_medication, args=("Epinephrine", 2, "Dr. Charlie"))

t1.start(); t2.start(); t3.start()
t1.join(); t2.join(); t3.join()
```

**Expected Output:**
```text
[SUCCESS] Dispensed 3x Epinephrine to Dr. Alice. Remaining: 2
[REJECTED] Dr. Bob requested 3x Epinephrine, but only 2 available.
[SUCCESS] Dispensed 2x Epinephrine to Dr. Charlie. Remaining: 0
```

---

### Example 4: Throttling Concurrent Resource Access via `Semaphore`
A hospital radiology department has 2 MRI machines. 5 patient scan requests arrive simultaneously. A `Semaphore(2)` limits concurrent access to exactly 2.

```python
import threading
import time

mri_semaphore = threading.Semaphore(2)

def perform_mri_scan(patient_id: str):
    print(f"[{patient_id}] Waiting in queue for an available MRI machine...")
    with mri_semaphore:
        print(f"[{patient_id}] MRI Machine acquired! Scan in progress...")
        time.sleep(0.4)
        print(f"[{patient_id}] Scan completed. Releasing MRI machine.")

patients = [f"Patient-{i}" for i in range(1, 5)]
threads = [threading.Thread(target=perform_mri_scan, args=(p,)) for p in patients]

for t in threads: t.start()
for t in threads: t.join()
```

**Expected Output:**
```text
[Patient-1] Waiting in queue for an available MRI machine...
[Patient-1] MRI Machine acquired! Scan in progress...
[Patient-2] Waiting in queue for an available MRI machine...
[Patient-2] MRI Machine acquired! Scan in progress...
[Patient-3] Waiting in queue for an available MRI machine...
[Patient-4] Waiting in queue for an available MRI machine...
[Patient-1] Scan completed. Releasing MRI machine.
[Patient-3] MRI Machine acquired! Scan in progress...
[Patient-2] Scan completed. Releasing MRI machine.
[Patient-4] MRI Machine acquired! Scan in progress...
[Patient-3] Scan completed. Releasing MRI machine.
[Patient-4] Scan completed. Releasing MRI machine.
```

---

## 3. Explanation

### Anatomy of Synchronization Primitives

```
┌─────────────────────────────────────────────────────────────────┐
│                      Synchronization Matrix                     │
├───────────────┬─────────────────────────────────────────────────┤
│ Primitive     │ Primary Mechanism & Semantics                   │
├───────────────┼─────────────────────────────────────────────────┤
│ Lock          │ Binary mutex (0 or 1). Non-reentrant.           │
│ RLock         │ Reentrant mutex. Tracks owner thread ID & depth.│
│ Semaphore     │ Atomic integer counter. acquire() decrements,   │
│               │ release() increments. Throttles capacity.       │
│ Event         │ Binary boolean flag (set/clear). Broadcasts to  │
│               │ all waiting threads.                            │
│ Condition     │ Associated with Lock. Allows threads to sleep   │
│               │ (wait) until another thread calls notify().     │
└───────────────┴─────────────────────────────────────────────────┘
```

### Understanding Deadlocks & The Dining Philosophers Problem
A **deadlock** is a state where two or more threads are permanently blocked because each holds a lock that the other needs:
```text
Thread 1 holds Lock A, waiting for Lock B
Thread 2 holds Lock B, waiting for Lock A
---> DEADLOCK! Neither thread can ever advance.
```

#### The 4 Coffman Conditions for Deadlock:
1. **Mutual Exclusion**: Resources cannot be shared simultaneously.
2. **Hold and Wait**: A thread holds one resource while requesting another.
3. **No Preemption**: Resources cannot be forcibly revoked from holding threads.
4. **Circular Wait**: A closed chain of threads exists where each waits for a resource held by the next.

#### Deadlock Prevention Strategy
The universal industry solution is **strict lock acquisition ordering**. If every thread in the system always acquires locks in alphabetical order (`Lock A` before `Lock B`), circular wait is mathematically impossible, eliminating deadlocks completely.

---

## 4. Why

### 1. Guaranteeing Financial & Clinical Data Integrity
In banking and healthcare, data corruption is non-negotiable. If two concurrent requests debit $1,000 from an account containing $1,200 without synchronization, both balance checks pass, and the account overdrafts to -$800. Synchronization enforces serializability.

### 2. Eliminating Intermittent Production Flaws
Race conditions do not happen predictably; they occur only when CPU time-slicing aligns at microsecond thresholds under high load. Unsynchronized code may run for months in testing and fail disastrously during peak production traffic.

### 3. Resource Protection & Throttling
Downstream databases, hardware sensors, and third-party payment gateways have concurrency limits. Using `Semaphore` primitives prevents a sudden burst of worker threads from overwhelming database connection pools or exceeding rate limits.

---

## 5. Advantages & Disadvantages

### Advantages
1. **Absolute Thread Safety**: Eliminates data corruption and race conditions across shared data structures.
2. **Fine-Grained Concurrency Throttling**: Semaphores enable controlled resource pooling.
3. **Cooperative Signaling**: `Condition` and `Event` prevent CPU-spinning busy-wait loops (`while not ready: pass`).

### Disadvantages
1. **Performance Contention**: Threads forced to wait on locks spend time blocked, reducing concurrency throughput.
2. **Risk of Deadlocks & Starvation**: Misordered locks cause total system freezes.
3. **Priority Inversion**: A low-priority thread holding a lock can indefinitely delay high-priority operations.

---

## 6. Real-World Use Cases

### Domain 1: Healthcare — ICU Bed Allocation System
- **Problem**: When 15 emergency triage nurses request hospital beds simultaneously, the system must not assign Bed #12 to two patients at the same time.
- **Solution**: A synchronized bed registry acquires an `RLock` on bed records, ensuring bed assignment, patient ID association, and ledger updates happen atomically.

### Domain 2: eCommerce — Flash Sale Inventory Decrement
- **Problem**: 5,000 shoppers attempt to purchase 100 discounted gaming consoles within 10 seconds.
- **Solution**: Stock check and decrement are wrapped in a fast mutex lock, rejecting purchase requests the instant inventory reaches 0 without negative stock errors.

### Domain 3: Banking — Atomic Multi-Account Fund Transfers
- **Problem**: Alice transfers $500 to Bob while Bob simultaneously transfers $200 to Alice.
- **Solution**: To prevent deadlocks, the transfer service sorts account IDs lexicographically (`min(idA, idB)` acquired first, `max(idA, idB)` acquired second), then performs atomic debits and credits.

---

## 7. Best Practices

### Practice 1: Always Use Context Managers (`with lock:`)
**When to apply**: Whenever acquiring a lock.
**Why**: Guarantees the lock is released even if an unhandled exception or early `return` occurs inside the block.

```python
# BAD PRACTICE (Leaks lock if do_work() throws an exception!)
lock.acquire()
do_work()
lock.release()

# GOOD PRACTICE (Always released, 100% exception safe)
with lock:
    do_work()
```

### Practice 2: Minimize Critical Section Duration
**When to apply**: In any synchronized block.
**Why**: Holding locks during slow operations (disk I/O, network requests, sleeping) halts all other competing threads, destroying application throughput.

```python
# BAD PRACTICE (Holds lock during slow HTTP request)
with lock:
    response = requests.get("https://api.external.com/data") # SLOW!
    db_cache[key] = response.json()

# GOOD PRACTICE (Fetch outside, lock only during fast memory write)
response = requests.get("https://api.external.com/data")
with lock:
    db_cache[key] = response.json()
```

### Practice 3: Enforce Consistent Global Lock Ordering
**When to apply**: Whenever a thread must acquire more than one lock.
**Why**: Prevents circular wait deadlocks.

```python
# GOOD PRACTICE (Sort locks by ID before acquisition)
def transfer(acc1, acc2, amount):
    first_lock, second_lock = sorted([acc1.lock, acc2.lock], key=id)
    with first_lock:
        with second_lock:
            acc1.balance -= amount
            acc2.balance += amount
```

---

## 8. Top 3 Mistakes

### Mistake 1: Assuming Simple Python Statements Are Atomic
#### What's the Problem?
Believing `counter += 1` or `my_dict[key] = my_dict[key] + 1` is atomic because of the GIL.
#### Why It Happens
Assuming a single line of high-level code translates to a single CPU instruction.
#### Impact
High concurrency results in lost updates and subtle, impossible-to-reproduce numerical discrepancies in production.
#### Incorrect Approach
```python
# Unsafe concurrent counter update
class MetricTracker:
    def record_hit(self):
        self.hits += 1 # RACE CONDITION!
```
#### Correct Approach
```python
class MetricTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self.hits = 0
    def record_hit(self):
        with self._lock:
            self.hits += 1 # Atomic update
```
#### Lesson Learned
Any read-modify-write operation on shared mutable data requires explicit synchronization.

---

### Mistake 2: Acquiring the Same `Lock` Twice in One Thread (Self-Deadlock)
#### What's the Problem?
A method acquires `self.lock`, then calls a helper method that also acquires `self.lock`.
#### Why It Happens
Refactoring code into modular helper functions without tracking lock reentrancy.
#### Impact
The thread freezes instantly waiting for *itself* to release the lock.
#### Incorrect Approach
```python
self.lock = threading.Lock()
def parent_action(self):
    with self.lock:
        self.child_action() # HANGS FOREVER!
def child_action(self):
    with self.lock: pass
```
#### Correct Approach
```python
# Use RLock which permits multiple acquisitions by the same owner thread
self.lock = threading.RLock()
def parent_action(self):
    with self.lock:
        self.child_action() # Succeeds cleanly!
```
#### Lesson Learned
Use `threading.RLock` whenever synchronized methods may call other synchronized methods on the same object.

---

### Mistake 3: Forgetting to Release Locks in Error Conditions
#### What's the Problem?
Using manual `acquire()` and `release()` without a `try...finally` block.
#### Why It Happens
Writing quick procedural code or omitting error paths.
#### Impact
An unexpected exception leaves the lock permanently acquired, causing all subsequent threads to freeze forever.
#### Incorrect Approach
```python
lock.acquire()
val = items[index] # If IndexError occurs here, lock is NEVER released!
lock.release()
```
#### Correct Approach
```python
with lock:
    val = items[index] # Automatically released even if IndexError occurs
```
#### Lesson Learned
Always wrap lock acquisitions with `with lock:` context managers.
