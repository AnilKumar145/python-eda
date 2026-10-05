# Unit 2.6 Exercises: Choosing the Right Concurrency Model

Master model selection, task routing, and hybrid concurrency execution in isolation:
1. **Exercise 1: Intelligent Workload Router** - Route CPU-intensive calculations to `ProcessPoolExecutor` and I/O tasks to `ThreadPoolExecutor`.
2. **Exercise 2: Asyncio Blocking Offloader** - Wrap legacy synchronous blocking functions with `loop.run_in_executor()` to keep the event loop responsive.
3. **Exercise 3: Hybrid Pipeline Coordination** - Coordinate asynchronous non-blocking ingestion that hands off CPU-heavy transformations to worker processes.

### Running Exercises
Execute the starter exercises:
```bash
python exercises/unit_2_6_choosing_the_right_concurrency_model_exercises.py
```

Check the solution file:
```bash
python exercises/solutions/unit_2_6_choosing_the_right_concurrency_model_solutions.py
```
