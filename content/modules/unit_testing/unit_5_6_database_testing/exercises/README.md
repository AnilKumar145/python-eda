# Unit 5.6 Exercises: Database Testing

## Overview
These exercises test your mastery of database testing with pytest and SQLAlchemy 2.0:
- Setting up in-memory SQLite engines and table schemas
- Fixture lifecycle (`yield` teardown and table drops)
- Transaction rollback pattern for clean test isolation
- Testing repository CRUD operations and querying methods
- Handling database constraint violations (IntegrityError)

## How to Run the Exercises

### Run Starter Code (Student Verification):
```bash
pytest content/modules/unit_testing/unit_5_6_database_testing/exercises/unit_5_6_database_testing_exercises.py -v
```

### Run Reference Solution:
```bash
pytest content/modules/unit_testing/unit_5_6_database_testing/exercises/solutions/unit_5_6_database_testing_exercises.py -v
```
