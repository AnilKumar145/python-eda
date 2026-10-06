# Lab 1 Easy: Surgical Schedule & Operating Theatre Dispatcher

## Overview
In this lab, you will build an operating theatre scheduling and dispatch repository using SQLAlchemy 2.0 `Session` management, atomic transactions, and parameterized `select()` filtering.

## Domain Scenario
Metropolitan Surgical Pavilion manages multiple Operating Theatres (e.g. `OT-General-1`, `OT-Cardio-2`). Surgical cases must be scheduled into specific theatres with estimated durations. If a scheduling conflict arises, the session transaction must cleanly roll back without leaving orphaned or corrupted booking states.

## Running Tests
```bash
pytest content/modules/database_part_2/unit_4_2_sqlalchemy_sessions/app_labs/lab_1_easy/tests.py -v
```
