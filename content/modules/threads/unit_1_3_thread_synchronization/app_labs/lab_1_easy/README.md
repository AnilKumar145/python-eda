---
title: "Hospital Pharmacy Inventory Dispenser"
type: app_lab
module: threads
unit: unit_1_3_thread_synchronization
lab_number: 1
difficulty: easy
use_case: pharmacy_inventory_dispenser
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - critical-sections
    - lock
    - atomic-operations
    - data-integrity
---

# Lab Level 1: Hospital Pharmacy Inventory Dispenser
**Module**: Threads
**Objective**: Build a thread-safe medication dispensing and audit logging system using `threading.Lock`.
**Difficulty**: Easy
**Context**: Healthcare Inpatient Pharmacy

## Generic Information
**Problem Statement**: In a hospital operating room suite, multiple surgical teams and nursing stations submit simultaneous automated requests for critical narcotics and anesthetics. Without thread synchronization, simultaneous reads and decrements produce race conditions, causing inventory counts to drop below zero and resulting in unaccounted drug variances.
**Goals**:
- Prevent double-allocation and negative inventory via mutual exclusion locks.
- Record every successful and rejected dispensation in an immutable audit ledger.
- Handle high-concurrency requests safely across 20+ simultaneous threads.
**Data Elements**:
- `drug_name` (str): NDC medication name (e.g. "Propofol-20ml").
- `requested_quantity` (int): Number of units requested.
- `requester_id` (str): Identifier of the requesting physician/nurse.
- `dispense_id` (str): Unique receipt ID.

## Use Case
**Title**: Dispense Controlled Medication Safely
**Description**: Surgical teams request units of medication. The pharmacy engine validates stock availability, decrements inventory atomically, and generates a signed audit entry.

### Rules
- If stock is insufficient, the transaction must be rejected cleanly without modifying inventory.
- Inventory checks and decrements must occur within the same synchronized critical section.
- An audit trail must be recorded for every transaction attempt.

### Test Cases
- Case 1: 10 concurrent requests for 1 unit each on a stock of 10 must all succeed, leaving exactly 0 units.
- Case 2: 10 concurrent requests for 2 units each on a stock of 10 must result in exactly 5 successes, 5 rejections, and 0 final stock (no negative stock).
- Case 3: Rejections do not corrupt the inventory count or state.

### Success Criteria
- Final inventory exactly matches initial stock minus total units dispensed.
- Zero race conditions or negative balances under concurrent load.
- 100% audit log consistency.

## Overview
This lab guides you through implementing `PharmacyDispenserEngine`, ensuring that critical clinical stock operations are thread-safe and audit-compliant.

## Learning Goals
- Use `threading.Lock` and context managers to guard multi-step transactions.
- Implement thread-safe audit logging.
- Verify consistency under high concurrency.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement code in `starter_code.py`.
3. Run `python tests.py` to verify thread safety.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Initialize `PharmacyDispenserEngine` with thread locks.
- Task 2: Implement atomic `dispense(drug_name, quantity, requester_id)`.
- Task 3: Implement thread-safe `get_stock(drug_name)`.
