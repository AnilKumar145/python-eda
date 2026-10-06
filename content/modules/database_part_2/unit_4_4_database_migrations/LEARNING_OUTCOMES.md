# Learning Outcomes: Unit 4.4 - Database Migrations

By the end of this unit, you will be able to:

1. **Understand Schema Evolution Architecture**: Explain why imperative ad-hoc DDL queries in production fail, and how Alembic tracks migration linearity through revision chains (`revision`, `down_revision`).
2. **Deconstruct the Alembic Environment**: Configure `alembic.ini`, understand how `env.py` links SQLAlchemy `target_metadata` to the target database, and configure online vs offline migration modes.
3. **Author Upgrade and Downgrade Scripts**: Write robust `op.create_table()`, `op.add_column()`, `op.alter_column()`, and `op.create_index()` operations, paired with symmetric rollback functions (`op.drop_table()`, `op.drop_column()`).
4. **Inspect and Manipulate the `alembic_version` Table**: Trace how relational databases store the current migration pointer in the single-row `alembic_version` table.
5. **Execute Multi-Phase Zero-Downtime Migrations**: Implement expand-contract deployment patterns (Add nullable column -> Backfill data -> Add constraint -> Drop old column) without breaking active application instances.
