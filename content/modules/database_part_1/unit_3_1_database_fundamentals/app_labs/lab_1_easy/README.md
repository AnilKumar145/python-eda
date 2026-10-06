---
title: "Hospital Patient Registry & Encounter Schema"
type: app_lab
module: database_part_1
unit: unit_3_1_database_fundamentals
lab_number: 1
difficulty: easy
use_case: hospital_patient_registry_schema
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - database
    - sql
  subtopics:
    - schema-design
    - foreign-keys
    - indexes
    - patient-registry
---

# Lab Level 1: Hospital Patient Registry & Encounter Schema
**Module**: Database Programming — Part 1
**Objective**: Build a production-grade relational patient registry and clinical encounter database schema in SQLite/PostgreSQL with referential integrity constraints, compound indexes, and audit logging.
**Difficulty**: Easy
**Context**: Hospital Clinical Health Information Management (HIM) System

## Generic Information
**Problem Statement**: When patients arrive at hospital emergency triage or outpatient clinics, their demographics and medical encounters must be recorded without data corruption. Orphan encounter records (encounters referencing deleted or non-existent patients) lead to dangerous clinical errors. You need to implement an encapsulated `HospitalPatientRegistry` manager that initializes the relational schema, performs transactional registrations, and manages clinical encounter lookups.

**Goals**:
- Implement `HospitalPatientRegistry` with SQLite backing.
- Define relational schema (`patients` and `encounters`) with foreign key constraints.
- Create B-Tree index on `encounters(patient_id, encounter_date)`.
- Support transactional patient admission and encounter logging.

## Use Case
**Title**: Relational Patient Admission and Encounter Tracker
**Description**: Maintain consistent patient registration with foreign-key protected encounter records and index-accelerated medical history queries.

### Rules
- Schema must enforce foreign keys (`PRAGMA foreign_keys = ON;`).
- Disallow invalid foreign key references.
- Implement patient lookup with associated encounters.

### Test Cases
- Case 1: Register patient and log multiple encounters. Verify accurate relational retrieval.
- Case 2: Attempt to log encounter for non-existent patient ID. Verify rejection.
- Case 3: Verify index existence on encounters table.
