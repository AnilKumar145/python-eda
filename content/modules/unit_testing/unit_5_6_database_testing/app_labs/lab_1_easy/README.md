# Application Lab 1: Pharmacy Medication Inventory Repository Test Harness

## Clinical & Architectural Context
In an acute-care hospital pharmacy, medication inventory records directly govern patient safety. Stockouts of critical antibiotics or vasopressors risk patient mortality, while unrecorded medication movements create hazardous reconciliation errors. 

Testing the persistence layer requires true database query execution without polluting shared production or staging servers. In this lab, you will build and test a production-grade `PharmacyInventoryRepository` using **SQLAlchemy 2.0** and **pytest**, verifying transactional updates, stock dispenses, reorder queries, and constraint enforcement against an isolated **in-memory SQLite** test harness.

---

## Architecture Overview

```
                      +-----------------------------------+
                      |         pytest Test Suite         |
                      +-----------------+-----------------+
                                        | (db_session fixture)
                                        v
                      +-----------------------------------+
                      |    PharmacyInventoryRepository    |
                      +-----------------+-----------------+
                                        | (SQLAlchemy 2.0 ORM)
                                        v
                      +-----------------------------------+
                      |   SQLite In-Memory (:memory:)     |
                      |   - InventoryItem Model           |
                      |   - Unique SKU Constraint         |
                      |   - Isolated Schema Lifecycle     |
                      +-----------------------------------+
```

---

## Lab Deliverables
1. **`starter_code.py`**: Student starter module containing repository method stubs and exception declarations.
2. **`tasks.md`**: Step-by-step instructions and acceptance criteria.
3. **`solution/solution.py`**: Complete production reference implementation.
4. **`tests.py`**: Automated test suite executing against the in-memory database harness.

---

## Verification
Run the lab test suite with pytest:
```bash
pytest content/modules/unit_testing/unit_5_6_database_testing/app_labs/lab_1_easy/tests.py -v
```
