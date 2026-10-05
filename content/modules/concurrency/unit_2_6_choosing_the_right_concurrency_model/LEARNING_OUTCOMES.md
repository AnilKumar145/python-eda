# Learning Outcomes: Unit 2.6 Choosing the Right Concurrency Model

By the end of this unit, learners will be able to:

1. **Evaluate Concurrency Paradigms Rigorously**: Contrast Python's three concurrency paradigms (`threading`, `multiprocessing`, `asyncio`) across memory footprint, CPU bound vs I/O bound bottlenecks, and context-switching overhead.
2. **Select Appropriate Execution Engines**: Choose definitively between ThreadPoolExecutor, ProcessPoolExecutor, and Asyncio event loops based on empirical system constraints and SLAs.
3. **Architect Hybrid Concurrency Systems**: Combine `asyncio` for high-throughput non-blocking networking with `loop.run_in_executor()` to offload heavy CPU-bound cryptography, image processing, or blocking legacy APIs.
4. **Benchmark Production Workloads**: Measure memory pressure, serialization costs (pickle overhead), and IPC latency to validate concurrency choices.
