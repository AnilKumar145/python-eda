# Unit 1.4: Thread Communication - Learning Outcomes

## Overview
While synchronization locks prevent corruption of shared state, the most robust concurrency architecture avoids shared mutable state altogether. By exchanging messages through thread-safe queues, programs decouple producers from consumers and eliminate locking bugs. This unit covers Python's `queue.Queue`, `queue.LifoQueue`, and `queue.PriorityQueue`, the producer-consumer design pattern, task tracking with `.task_done()` and `.join()`, and sentinel-based shutdown pipelines.

**Estimated Time**: 5-7 hours
- Knowledge: 90 min
- Exercises: 90-120 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### Message Queues & Thread-Safe Exchange
- [ ] **Contrast** shared-state concurrency (mutexes/locks) with message-passing concurrency (queues) to design deadlock-free architectures.
- [ ] **Utilize** `queue.Queue` for FIFO ordering, `queue.LifoQueue` for stack semantics, and `queue.PriorityQueue` for priority-ordered triage.
- [ ] **Configure** bounded queues (`maxsize`) to apply backpressure when producers outpace consumers.

### Producer-Consumer Architecture
- [ ] **Implement** multi-producer multi-consumer worker pipelines using non-blocking or timeout-based `get()` and `put()` calls.
- [ ] **Coordinate** task completion tracking using `queue.task_done()` and `queue.join()`.
- [ ] **Implement** graceful pipeline shutdown using sentinel tokens (`None` or sentinel objects).

### Real-World Engineering Application (Healthcare)
- [ ] **Construct** an Emergency Room (ER) patient triage ingestion queue using `PriorityQueue`, ensuring critical code-blue patients are dispatched to doctors ahead of routine triage cases.
- [ ] **Build** an asynchronous diagnostic imaging processing pipeline that receives DICOM scans from hospital scanners and distributes them across background worker threads.

---

## Assessment Criteria

### Exercises (Pass: 100% assertions pass)
- FIFO task processing pipeline using `queue.Queue` and sentinel termination.
- Priority-ordered task dispatching using `queue.PriorityQueue`.
- Task completion tracking with `task_done()` and `join()`.

### Application Lab (Pass: 100% tests pass)
- Implementation of a clinical ER patient triage pipeline prioritizing emergency cases and balancing loads across doctor consumer threads.
