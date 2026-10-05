# Lab Level 1 Tasks: Clinical Workload Router and Profiler

## Task 1: Job Classifier Function
**Difficulty**: Easy
**Points**: 10

### Objective
Create a function that inspects a job descriptor and returns `"IO"` or `"CPU"`.

### Requirements
- Function signature: `classify_job(job: dict) -> str`
- If `job.get("category")` contains `"database"`, `"rest"`, `"network"`, or `"disk"`: return `"IO"`.
- If `job.get("category")` contains `"genomic"`, `"crypto"`, `"fourier"`, or `"rendering"`: return `"CPU"`.
- Default to `"IO"` if unspecified.

---

## Task 2: Workload Router Implementation
**Difficulty**: Easy
**Points**: 20

### Objective
Implement `ClinicalWorkloadRouter.route_and_execute(jobs: list) -> dict`.

### Requirements
- In `route_and_execute(self, jobs: list)`:
  - Classify each job using `classify_job`.
  - Separate jobs into an `io_jobs` list and a `cpu_jobs` list.
  - Return a dictionary:
    ```python
    {
        "io_count": len(io_jobs),
        "cpu_count": len(cpu_jobs),
        "io_job_ids": [j["id"] for j in io_jobs],
        "cpu_job_ids": [j["id"] for j in cpu_jobs]
    }
    ```
