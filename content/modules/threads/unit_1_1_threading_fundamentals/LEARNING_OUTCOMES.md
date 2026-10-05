# Unit 1.1: Threading Fundamentals - Learning Outcomes

## Overview
Multithreading enables concurrent execution of operations within a single process. In Python, threads share memory and runtime state while being scheduled by the operating system. This unit establishes the core mental model: understanding processes versus threads, distinguishing CPU-bound from I/O-bound tasks, navigating the Global Interpreter Lock (GIL), and mastering the lifecycle of threads created via `threading.Thread`.

**Estimated Time**: 4-6 hours
- Knowledge: 60-90 min
- Exercises: 60-90 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### Fundamental Concepts
- [ ] **Distinguish** between an operating system process (isolated memory space) and a thread (shared memory context within a process).
- [ ] **Analyze** whether a workload is I/O-bound (network, disk, user input) or CPU-bound (mathematical transformations, image encoding) to determine if multithreading is beneficial under Python's GIL.
- [ ] **Explain** the role of the Global Interpreter Lock (GIL) and why Python threads yield execution during I/O operations.

### Thread Lifecycle & Control
- [ ] **Instantiate** worker threads using Python's standard `threading.Thread` class with `target` and `args` parameters.
- [ ] **Execute** worker threads using `.start()` and synchronize execution back to the caller using `.join()`.
- [ ] **Distinguish** between the main thread and auxiliary worker threads, verifying active counts with `threading.active_count()`.

### Real-World Engineering Application (Healthcare)
- [ ] **Implement** concurrent telemetry loggers and asynchronous patient vital-sign monitors that run in worker threads without freezing user-facing UI or API request handlers.
- [ ] **Collect** parallel diagnostic response payloads from simulated external hospital services without blocking sequential business logic.

---

## Assessment Criteria

### Exercises (Pass: 100% assertions pass)
- Creation and invocation of `threading.Thread` instances.
- Verification that caller threads wait appropriately using `.join()`.
- Proper passing of positional and keyword arguments to targets.

### Application Lab (Pass: 100% tests pass)
- Functional implementation of a multi-source healthcare vitals ingestion stream using dedicated worker threads.
- Adherence to non-blocking patterns and clean join teardowns.
