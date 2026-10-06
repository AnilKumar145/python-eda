# Exercises: Unit 3.4 - Database Security, Transactions, and Best Practices

Practice SQL injection remediation, dynamic identifier validation, transaction savepoint rollback, and resilient retry logic.

## Exercises Overview:
1. **Exercise 1: SQL Injection Remediation**: Transform a vulnerable string-concatenated login function into a secure parameterized query.
2. **Exercise 2: Safe Dynamic Column Ordering**: Implement dynamic column ordering with strict whitelist validation.
3. **Exercise 3: Savepoint Partial Rollback**: Implement a multi-step billing transaction that rolls back optional add-ons to a savepoint on failure.
4. **Exercise 4: Exponential Backoff Query Runner**: Implement a retry decorator/wrapper handling transient SQLite lock exceptions.

## How to Run:
```bash
python content/modules/database_part_1/unit_3_4_security_and_best_practices/exercises/unit_3_4_security_and_best_practices_exercises.py
python content/modules/database_part_1/unit_3_4_security_and_best_practices/exercises/solutions/unit_3_4_security_and_best_practices_exercises.py
```
