# Python EAD: Real-Time Product Engineering Platform

Curriculum and test harness for Multithreading, Multiprocessing, Asynchronous Programming, and Concurrency Patterns in Python.

---

## 1. Quick Start & Prerequisites

### Prerequisites:
- **Python 3.11+** installed (`python --version`)
- **pytest** test runner (`pip install pytest`)

---

## 2. Commands to Run Exercises

Each unit includes concept-focused exercises with built-in assertion tests.

### Run an Exercise (Student Starter):
```bash
# Unit 1.1: Threading Fundamentals
python content/modules/threads/unit_1_1_threading_fundamentals/exercises/unit_1_1_threading_fundamentals_exercises.py

# Unit 1.2: Thread Management
python content/modules/threads/unit_1_2_thread_management/exercises/unit_1_2_thread_management_exercises.py

# Unit 1.3: Thread Synchronization
python content/modules/threads/unit_1_3_thread_synchronization/exercises/unit_1_3_thread_synchronization_exercises.py

# Unit 1.4: Thread Communication
python content/modules/threads/unit_1_4_thread_communication/exercises/unit_1_4_thread_communication_exercises.py

# Unit 1.5: Thread Pools
python content/modules/threads/unit_1_5_thread_pools/exercises/unit_1_5_thread_pools_exercises.py

# Unit 2.1: Concurrency Fundamentals
python content/modules/concurrency/unit_2_1_concurrency_fundamentals/exercises/unit_2_1_concurrency_fundamentals_exercises.py

# Unit 2.2: Multiprocessing
python content/modules/concurrency/unit_2_2_multiprocessing/exercises/unit_2_2_multiprocessing_exercises.py

# Unit 2.3: Process Pools
python content/modules/concurrency/unit_2_3_process_pools/exercises/unit_2_3_process_pools_exercises.py

# Unit 2.4: Asynchronous Programming
python content/modules/concurrency/unit_2_4_asynchronous_programming/exercises/unit_2_4_asynchronous_programming_exercises.py

# Unit 2.5: Concurrent Programming Patterns
python content/modules/concurrency/unit_2_5_concurrent_programming_patterns/exercises/unit_2_5_concurrent_programming_patterns_exercises.py

# Unit 2.6: Choosing the Right Concurrency Model
python content/modules/concurrency/unit_2_6_choosing_the_right_concurrency_model/exercises/unit_2_6_choosing_the_right_concurrency_model_exercises.py
```

### Run an Exercise Solution (Reference):
*(Available on the `main` branch under `exercises/solutions/`)*
```bash
python content/modules/threads/unit_1_1_threading_fundamentals/exercises/solutions/unit_1_1_threading_fundamentals_exercises.py
python content/modules/concurrency/unit_2_4_asynchronous_programming/exercises/solutions/unit_2_4_asynchronous_programming_exercises.py
```

---

## 3. Commands to Run Application Labs

Each unit includes real-world Healthcare domain application labs verified via `pytest`.

### Run Individual Lab Tests:
```bash
# Unit 1.1 Lab: Bedside Monitor Telemetry Ingestion
pytest content/modules/threads/unit_1_1_threading_fundamentals/app_labs/lab_1_easy/tests.py -v

# Unit 1.2 Lab: ICU Watchdog Heartbeat Supervisor
pytest content/modules/threads/unit_1_2_thread_management/app_labs/lab_1_easy/tests.py -v

# Unit 1.3 Lab: Hospital Central Pharmacy Dispenser
pytest content/modules/threads/unit_1_3_thread_synchronization/app_labs/lab_1_easy/tests.py -v

# Unit 1.4 Lab: ER Emergency Room Triage Dispatcher
pytest content/modules/threads/unit_1_4_thread_communication/app_labs/lab_1_easy/tests.py -v

# Unit 1.5 Lab: Clinical Diagnostics Panel Aggregator
pytest content/modules/threads/unit_1_5_thread_pools/app_labs/lab_1_easy/tests.py -v

# Unit 2.1 Lab: Clinical Workload Router and Profiler
pytest content/modules/concurrency/unit_2_1_concurrency_fundamentals/app_labs/lab_1_easy/tests.py -v

# Unit 2.2 Lab: Parallel Genomic Variant Scanner
pytest content/modules/concurrency/unit_2_2_multiprocessing/app_labs/lab_1_easy/tests.py -v

# Unit 2.3 Lab: Batch ECG Signal Analysis Pipeline
pytest content/modules/concurrency/unit_2_3_process_pools/app_labs/lab_1_easy/tests.py -v

# Unit 2.4 Lab: Real-Time ICU Asynchronous Vital Signs Hub
pytest content/modules/concurrency/unit_2_4_asynchronous_programming/app_labs/lab_1_easy/tests.py -v

# Unit 2.5 Lab: Emergency Diagnostic Pipeline Pattern Aggregator
pytest content/modules/concurrency/unit_2_5_concurrent_programming_patterns/app_labs/lab_1_easy/tests.py -v

# Unit 2.6 Lab: Multi-Modal Genomic Analysis Gateway
pytest content/modules/concurrency/unit_2_6_choosing_the_right_concurrency_model/app_labs/lab_1_easy/tests.py -v
```

---

## 4. Run All Tests Across the Entire Codebase

### Run all lab tests:
```bash
pytest content/modules/ -v
```

### Run all exercise solutions & lab tests with PowerShell:
```powershell
Get-ChildItem -Path "content/modules" -Filter "*exercises.py" -Recurse | Where-Object { $_.FullName -like "*solutions*" } | ForEach-Object { python $_.FullName }
Get-ChildItem -Path "content/modules" -Filter "tests.py" -Recurse | ForEach-Object { pytest $_.FullName -q }
```

---

## 5. Web Application

To launch the interactive web platform:
```bash
cd web-app
npm install
npm run dev
# Open http://localhost:3000
```
