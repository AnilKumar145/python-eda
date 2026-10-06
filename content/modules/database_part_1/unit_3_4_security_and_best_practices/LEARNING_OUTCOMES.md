# Learning Outcomes: Unit 3.4 - Database Security, Transactions, and Best Practices

By the end of this unit, you will be able to:
1. **Defend Against SQL Injection**: Diagnose vulnerable string-concatenated SQL queries and remediate them using parameter bindings.
2. **Safely Construct Dynamic Queries**: Whitelist and safely quote dynamic SQL identifiers (table and column names) where parameter placeholders are disallowed by SQL grammar.
3. **Master ACID Isolation Levels**: Describe the trade-offs between Read Committed, Repeatable Read, and Serializable, and detect phenomena such as dirty reads, non-repeatable reads, and phantom reads.
4. **Implement Savepoints for Partial Rollbacks**: Use `SAVEPOINT`, `ROLLBACK TO SAVEPOINT`, and `RELEASE SAVEPOINT` to recover from sub-operation failures without aborting outer transactions.
5. **Ensure Resource Hygiene**: Eliminate database connection and cursor leaks using Python context managers (`contextlib.closing`, `with` blocks) and exponential backoff retry policies.
