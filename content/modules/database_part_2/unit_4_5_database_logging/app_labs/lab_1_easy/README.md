# Lab 1 Easy: ICU Diagnostic Query Profiler & Slow Statement Watchdog

## Overview
In this lab, you will engineer a production database observability watchdog for an Intensive Care Unit (ICU) data tier. Using SQLAlchemy event listeners, you will capture statement execution latencies, detect slow unindexed queries, and record connection pool telemetry.

## Domain Scenario
The hospital's real-time vital telemetry stream continuously writes and reads patient sensor packets. If an unindexed query blocks the database connection pool, patient monitor alerts can experience critical delays. You will build a watchdog engine that intercepts all executed SQL commands, calculates statement latencies, and logs structured warnings whenever queries exceed configurable safety thresholds.

## Running Tests
```bash
pytest content/modules/database_part_2/unit_4_5_database_logging/app_labs/lab_1_easy/tests.py -v
```
