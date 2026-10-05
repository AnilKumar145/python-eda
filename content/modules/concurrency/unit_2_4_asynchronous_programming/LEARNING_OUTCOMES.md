# Unit 2.4: Asynchronous Programming - Learning Outcomes

## Overview
Asynchronous programming provides high-concurrency, single-threaded cooperative multitasking. Operating on a centralized event loop, Python's `asyncio` allows coroutines to voluntarily pause and yield execution while awaiting I/O operations. This model handles tens of thousands of concurrent network connections with minimal RAM and zero thread context-switching overhead. This unit covers writing async functions with `async`/`await`, scheduling tasks with `create_task()`, concurrent batching with `gather()`, handling timeouts, and structuring cooperative task cancellation.

**Estimated Time**: 5-7 hours
- Knowledge: 90 min
- Exercises: 90-120 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### Coroutines & The Event Loop
- [ ] **Define** coroutines using `async def` and manage execution suspension points using `await`.
- [ ] **Explain** the mechanics of the `asyncio` single-threaded event loop and why blocking calls freeze all tasks.
- [ ] **Run** top-level async entry points cleanly using `asyncio.run()`.

### Concurrent Task Scheduling & Batching
- [ ] **Schedule** background concurrent execution using `asyncio.create_task()`.
- [ ] **Execute** collections of coroutines concurrently using `asyncio.gather(*coroutines, return_exceptions=...)`.
- [ ] **Apply** non-blocking timeouts with `asyncio.wait_for(coroutine, timeout=...)` and handle `asyncio.TimeoutError`.
- [ ] **Cancel** executing tasks using `task.cancel()` and handle `asyncio.CancelledError`.

### Real-World Engineering Application (Healthcare)
- [ ] **Engineer** an asynchronous high-volume patient vitals ingestion microservice that handles simulated WebSocket streams from 500 bedside monitors concurrently without thread exhaustion.
