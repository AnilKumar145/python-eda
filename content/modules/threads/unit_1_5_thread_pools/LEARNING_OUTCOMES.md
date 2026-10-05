# Unit 1.5: Thread Pools - Learning Outcomes

## Overview
Manually spawning and joining individual threads introduces high thread allocation overhead, risks resource exhaustion under load, and lacks native support for capturing return values and handling worker exceptions. Python's `concurrent.futures.ThreadPoolExecutor` provides an enterprise-grade abstraction layer that reuses an internal pool of worker threads, tracks task outcomes via `Future` objects, and isolates exception propagation.

**Estimated Time**: 5-7 hours
- Knowledge: 90 min
- Exercises: 90-120 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### ThreadPoolExecutor Architecture
- [ ] **Contrast** manual thread creation (`threading.Thread`) with managed pooling (`ThreadPoolExecutor`), explaining amortized thread creation cost and bounded concurrency.
- [ ] **Utilize** context managers (`with ThreadPoolExecutor(max_workers=N) as executor:`) to enforce deterministic shutdown and resource cleanup.
- [ ] **Choose** between `.submit()` (fine-grained control over individual `Future` objects) and `.map()` (streaming ordered transformation over iterables).

### Future Objects & Exception Propagation
- [ ] **Query** the status of asynchronous execution via `Future.done()`, `Future.running()`, and `Future.cancelled()`.
- [ ] **Retrieve** return values using `Future.result(timeout=...)` and handle worker exceptions cleanly without crashing the main process.
- [ ] **Coordinate** task batches using `concurrent.futures.as_completed()` to process results in order of completion rather than submission order.

### Real-World Engineering Application (Healthcare)
- [ ] **Engineer** a high-throughput medical lab report aggregator that queries disparate hospital microservices concurrently via a managed thread pool.
- [ ] **Implement** resilient fallback logic when individual downstream clinical API queries raise network timeouts or HTTP errors.

---

## Assessment Criteria

### Exercises (Pass: 100% assertions pass)
- Task dispatch and result retrieval using `executor.submit()` and `Future.result()`.
- Iterative processing of completed futures using `as_completed()`.
- Exception trapping and handling for failing worker tasks.

### Application Lab (Pass: 100% tests pass)
- Implementation of a resilient healthcare lab diagnostic aggregator using `ThreadPoolExecutor` and graceful timeout handling.
