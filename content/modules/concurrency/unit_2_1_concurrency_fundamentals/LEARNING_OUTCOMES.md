# Unit 2.1: Concurrency Fundamentals - Learning Outcomes

## Overview
Concurrency is the composition of independently executing processes or operations, whereas parallelism is the simultaneous execution of multiple things at the exact same physical instant on multiple CPU cores. In Python, selecting the optimal concurrency model requires analyzing whether tasks are CPU-bound or I/O-bound, profiling memory overhead, and understanding the distinct trade-offs between threads, separate processes, and single-threaded asynchronous event loops.

**Estimated Time**: 4-6 hours
- Knowledge: 60-90 min
- Exercises: 60-90 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### Core Paradigms
- [ ] **Contrast** concurrency (interleaved task handling) with parallelism (hardware-level simultaneous execution across distinct CPU cores).
- [ ] **Distinguish** synchronous execution (blocking sequential control flow) from asynchronous execution (deferred completion and event-driven progression).
- [ ] **Profile** workloads to classify operations as I/O-bound (network, disk, socket) or CPU-bound (mathematical, compression, encryption).

### Architectural Model Comparison
- [ ] **Evaluate** the trade-offs between Threads (`threading`), Processes (`multiprocessing`), and Coroutines (`asyncio`).
- [ ] **Explain** why the CPython GIL permits concurrent I/O with threads but prevents parallel CPU scaling without multiprocessing.
- [ ] **Calculate** theoretical speedup bounds using Amdahl's Law based on parallelizable code fractions.

### Real-World Engineering Application (Healthcare)
- [ ] **Architect** a hybrid hospital triage and diagnostic pipeline that routes I/O-bound doctor notifications to threads/asyncio while routing CPU-heavy genomic sequencing and ECG waveform signal processing to worker processes.
