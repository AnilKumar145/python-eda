# Exercises: Unit 3.3 - Working with PostgreSQL and Relational Stores

Practice PostgreSQL connection URI parsing, rich type serialization (JSON & Decimal), and NULL-safe data extraction.

## Exercises Overview:
1. **Exercise 1: Connection URI DSN Parser**: Parse a `postgresql://` connection URI and extract components into a validated dictionary.
2. **Exercise 2: Rich Type Serialization**: Store and retrieve records containing Python `Decimal` and `dict` JSON metadata without precision loss.
3. **Exercise 3: Null-Safe Clinical Record Extractor**: Extract patient records with fallback strings for nullable columns using `COALESCE`.
4. **Exercise 4: Resilient Database Adapter**: Implement an adapter that executes queries and maps rows to dictionaries.

## How to Run:
```bash
python content/modules/database_part_1/unit_3_3_working_with_postgresql/exercises/unit_3_3_working_with_postgresql_exercises.py
python content/modules/database_part_1/unit_3_3_working_with_postgresql/exercises/solutions/unit_3_3_working_with_postgresql_exercises.py
```
