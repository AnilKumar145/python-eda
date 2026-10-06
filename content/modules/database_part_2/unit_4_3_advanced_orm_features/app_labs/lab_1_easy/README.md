# Lab 1 Easy: Patient Allergy Cross-Reference & Eager Loading Hub

## Overview
In this lab, you will engineer a clinical Patient Allergy Management System featuring many-to-many relational mapping, compound keys on junction tables, and optimized query execution using `selectinload()`.

## Domain Scenario
Adverse drug reactions cause thousands of hospital readmissions annually. When a clinician prescribes medication, the hospital clinical decision support system cross-references the patient's record against drug allergy registries. The query must load patients and their full allergy profiles without triggering the N+1 query problem under high hospital load.

## Running Tests
```bash
pytest content/modules/database_part_2/unit_4_3_advanced_orm_features/app_labs/lab_1_easy/tests.py -v
```
