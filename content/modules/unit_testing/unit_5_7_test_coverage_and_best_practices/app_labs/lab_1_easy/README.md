# Application Lab 1: Clinical Audit Log Quality Gate and Coverage Harness

## Clinical & Architectural Context
Under HIPAA and medical informatics regulations, any software system accessing electronic Protected Health Information (ePHI) must maintain an immutable, tamper-evident audit trail. In this lab, you will engineer a **cryptographically hashed audit ledger** and an accompanying **100% branch-coverage automated test suite**.

---

## Architecture Overview

```
                      +-----------------------------------+
                      |      pytest Quality Test Suite    |
                      |   - 100% Branch Coverage          |
                      |   - Tamper Detection Test Cases   |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------------------------+
                      |       ClinicalAuditLedger         |
                      |   - Append-Only Event Chain       |
                      |   - SHA-256 Block Hashing         |
                      |   - Cryptographic Integrity Check |
                      +-----------------------------------+
```

---

## Lab Deliverables
1. **`starter_code.py`**: Student starter implementation with missing logic stubs.
2. **`tasks.md`**: Step-by-step implementation and coverage requirements.
3. **`solution/solution.py`**: Reference implementation of the cryptographic ledger.
4. **`tests.py`**: Production test suite providing 100% statement and branch coverage.

---

## Verification
Run tests with coverage measurement:
```bash
pytest content/modules/unit_testing/unit_5_7_test_coverage_and_best_practices/app_labs/lab_1_easy/tests.py -v
```
