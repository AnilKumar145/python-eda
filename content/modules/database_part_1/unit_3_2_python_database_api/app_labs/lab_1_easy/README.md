---
title: "Clinic Batch Vitals Ingestion & Connection Pool"
type: app_lab
module: database_part_1
unit: unit_3_2_python_database_api
lab_number: 1
difficulty: easy
use_case: clinic_batch_vitals_ingestion
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - database
    - db-api
  subtopics:
    - connection-pooling
    - executemany
    - batch-streaming
    - transactions
---

# Lab Level 1: Clinic Batch Vitals Ingestion & Connection Pool
**Module**: Database Programming — Part 1
**Objective**: Build a high-throughput clinical vitals batch ingestion pipeline backed by a thread-safe connection pool, using `executemany` for batch flushes and generator-based `fetchmany` for reports.
**Difficulty**: Easy
**Context**: Outpatient Ambulatory Telemetry Hub

## Generic Information
**Problem Statement**: Ambulatory clinics receive heart rate and pulse oximeter readings from dozens of wearable devices. Creating and destroying a database connection for each reading creates unacceptable latency. You will implement `ClinicTelemetryPipeline` backed by a reusable connection pool. The pipeline flushes telemetry batches using `cursor.executemany()` in transactional units and provides a memory-safe `stream_patient_history()` generator using `cursor.fetchmany()`.

**Goals**:
- Implement `ClinicConnectionPool` with configurable pool capacity.
- Implement `batch_record_vitals(records)` using `executemany` and transactions.
- Implement `stream_patient_history(mrn, batch_size)` generator yielding chunks with `fetchmany`.

## Use Case
**Title**: Ambulatory Telemetry Batch Ingestor
**Description**: Pool connections, batch-insert vital signs, and stream historical reports in bounded memory chunks.

### Rules
- All database access must borrow and return connections via the pool.
- Ingestion must use `cursor.executemany()` with explicit commit.
- Streaming must yield chunks using `cursor.fetchmany()`.

### Test Cases
- Case 1: Ingest 500 telemetry records via batch insert. Verify exact row count.
- Case 2: Stream patient history in chunks of 50. Verify chunk sizes and ordering.
- Case 3: Verify connection pool reuse across multiple threads.
