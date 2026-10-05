# Unit 1.3: Thread Synchronization - Learning Outcomes

## Overview
When multiple threads read and write shared mutable state simultaneously, non-deterministic race conditions occur, leading to data corruption and memory inconsistencies. Thread synchronization primitives coordinate access to critical sections, guaranteeing atomicity and state consistency. This unit covers Python's core synchronization toolkit: `threading.Lock`, reentrant `threading.RLock`, counting `threading.Semaphore`, signaling `threading.Event`, and monitor-style `threading.Condition`.

**Estimated Time**: 5-7 hours
- Knowledge: 90 min
- Exercises: 90-120 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### Race Conditions & Critical Sections
- [ ] **Identify** critical sections in multi-threaded code where unsynchronized read-modify-write sequences cause lost updates.
- [ ] **Demonstrate** how Python bytecode instruction interleaving causes race conditions even with simple expressions like `counter += 1`.
- [ ] **Apply** mutual exclusion using `threading.Lock` and context manager `with lock:` syntax to guarantee atomic operations.

### Advanced Synchronization Primitives
- [ ] **Distinguish** when to use `threading.RLock` (reentrant lock) to prevent self-deadlocks in recursive methods or nested critical sections within the same thread.
- [ ] **Implement** bounded resource throttling using `threading.Semaphore` to cap concurrent connections or access to shared hardware devices.
- [ ] **Coordinate** producer and consumer threads using `threading.Condition` with `wait()`, `notify()`, and `notify_all()`.

### Real-World Engineering Application (Healthcare)
- [ ] **Engineer** a thread-safe hospital medication inventory dispensing service that prevents double-allocation of critical pharmacy drugs under high-concurrency requests.
- [ ] **Construct** an ICU bed reservation system with capacity control governed by counting semaphores.

---

## Assessment Criteria

### Exercises (Pass: 100% assertions pass)
- Safe atomic counter implementation preventing lost updates across 20 concurrent threads.
- Reentrant locking demonstrated in nested class method invocations.
- Semaphore concurrency limiter restricting simultaneous callers to a configured bound.

### Application Lab (Pass: 100% tests pass)
- Implementation of a thread-safe hospital pharmacy dispensation engine with strict inventory consistency checks.
- Verification that concurrent dispensation attempts under high load never result in negative stock or inconsistent audit trails.
