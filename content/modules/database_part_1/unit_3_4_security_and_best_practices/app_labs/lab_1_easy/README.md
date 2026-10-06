---
title: "Secure Clinical Prescription Audit Ledger"
type: app_lab
module: database_part_1
unit: unit_3_4_security_and_best_practices
lab_number: 1
difficulty: easy
use_case: secure_clinical_prescription_audit_ledger
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - database
    - security
  subtopics:
    - sql-injection-defense
    - savepoint-rollback
    - context-managers
    - audit-ledger
---

# Lab Level 1: Secure Clinical Prescription Audit Ledger
**Module**: Database Programming — Part 1
**Objective**: Build a HIPAA-compliant secure clinical prescription audit ledger with parameterized query defenses against SQL injection, nested transaction savepoints for dosage limit checks, and guaranteed resource cleanup.
**Difficulty**: Easy
**Context**: Hospital Controlled Substance E-Prescribing System

## Generic Information
**Problem Statement**: In hospital e-prescribing systems, controlled medications (e.g. Schedule II opioids) require tamper-evident audit trails. Malicious injection attacks through clinical note fields must be blocked, and accidental dosage over-prescription must trigger a savepoint rollback without discarding the primary patient consultation log. You will implement `PrescriptionAuditLedger` providing parameterized writes, savepoint dosage checks, and context-managed resource handling.

**Goals**:
- Implement `PrescriptionAuditLedger` with SQLite backing.
- Block SQL injection attacks through clinical note and prescriber search fields.
- Use `SAVEPOINT` to rollback unauthorized narcotic dosages while committing the consultation log.
- Provide clean context manager handling for safe connection lifecycle.

## Use Case
**Title**: Tamper-Proof Controlled Medication Audit Ledger
**Description**: Execute secure parameterized prescription inserts, enforce dosage threshold limits with savepoint rollbacks, and safely search patient audit histories.

### Rules
- All user inputs must be parameterized (`?`). No string interpolation allowed.
- If dosage exceeds max threshold (e.g. > 100mg for narcotics), rollback to savepoint and log alert.

### Test Cases
- Case 1: Attempt SQL injection in patient search. Verify zero unauthorized record leakage.
- Case 2: Process prescription exceeding threshold. Verify savepoint rollback preserves audit event but excludes excessive narcotic.
- Case 3: Process valid prescription. Verify both event and prescription commit.
