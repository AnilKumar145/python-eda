# Lab 1 Easy: Inpatient Bed Allocation & Ward Registry

## Overview
In this lab, you will design the core SQLAlchemy 2.0 domain models for an inpatient hospital ward registry. You will model Wards and individual Bed allocations using modern type annotations, declarative relationships, and relational integrity constraints.

## Domain Scenario
Metropolitan General Hospital operates specialized clinical wards (Intensive Care Unit, Surgical Recovery, Pediatrics). Each ward has a fixed bed capacity. Beds are assigned unique physical identifier labels (e.g., `ICU-101`, `SURG-204`) and track real-time occupancy status.

## Running Tests
```bash
pytest content/modules/database_part_2/unit_4_1_orm_fundamentals/app_labs/lab_1_easy/tests.py -v
```
