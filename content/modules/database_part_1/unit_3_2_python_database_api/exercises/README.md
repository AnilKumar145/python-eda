# Exercises: Unit 3.2 - Python Database API (DB-API 2.0)

Practice PEP 249 connection and cursor mechanics, batch processing with `fetchmany`, atomic transactions with rollback, and connection pooling in Python.

## Exercises Overview:
1. **Exercise 1: Batch Ingestion with executemany**: Implement a fast batch insert function using `executemany` with commit.
2. **Exercise 2: Chunked Result Streamer**: Implement a generator yielding records in fixed-size chunks using `fetchmany`.
3. **Exercise 3: Atomic Multi-Table Transfer**: Implement an atomic transfer with explicit rollback on error.
4. **Exercise 4: Simple Connection Pool**: Implement a lightweight connection pool utilizing `queue.Queue`.

## How to Run:
```bash
python content/modules/database_part_1/unit_3_2_python_database_api/exercises/unit_3_2_python_database_api_exercises.py
python content/modules/database_part_1/unit_3_2_python_database_api/exercises/solutions/unit_3_2_python_database_api_exercises.py
```
