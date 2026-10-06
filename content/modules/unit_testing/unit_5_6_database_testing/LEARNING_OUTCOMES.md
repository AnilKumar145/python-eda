# Learning Outcomes: Unit 5.6 - Database Testing

By the end of this unit, you will be able to:

1. **Spin Up Ephemeral In-Memory Databases**: Build ultra-fast test database fixtures using `sqlite:///:memory:` that execute within microseconds.
2. **Execute Transactional Rollback Isolation**: Wrap individual tests in nested transactions (`SAVEPOINT`) that automatically roll back on teardown, leaving the database pristine without dropping tables.
3. **Test CRUD Operations Thoroughly**: Test Create, Read, Update, and Delete operations against real relational engines rather than superficial mocks.
4. **Validate Data Access Object (DAO) / Repository Layers**: Verify that domain filters, joins, pagination queries, and aggregation statistics produce expected results.
5. **Enforce Database Schema Integrity in CI**: Author automated tests validating table creation, foreign key cascade constraints, unique constraints, and check constraints.
