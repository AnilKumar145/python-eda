# Lab 1 Easy: Pharmacy Drug Formulary Schema Evolution Engine

## Overview
In this lab, you will build a robust database schema migration controller inspired by Alembic's revision graph architecture.

## Domain Scenario
As clinical regulations evolve, the hospital formulary database must introduce new tracking columns (e.g. Schedule-II controlled substance identifiers, cold-chain temperature monitoring requirements) across clinical environments without data loss. You will construct a migration coordinator that enforces revision linearity, checks prerequisites, and ensures atomic schema upgrades and rollbacks.

## Running Tests
```bash
pytest content/modules/database_part_2/unit_4_4_database_migrations/app_labs/lab_1_easy/tests.py -v
```
