# Tasks: Pharmacy Drug Formulary Schema Evolution Engine

## Task 1: Model Revision Registry
Define a `RevisionNode` dataclass:
- `revision_id: str`: Unique revision identifier (e.g. `"001_init"`).
- `down_revision: Optional[str]`: Identifier of parent revision (`None` if root).
- `upgrade_script: str`: SQL DDL statement to advance schema.
- `downgrade_script: str`: SQL DDL statement to roll back schema.

## Task 2: Implement FormularyMigrationEngine
In `FormularyMigrationEngine`:
- `initialize_tracking(conn)`: Create `alembic_version (version_num TEXT PRIMARY KEY)`.
- `register_revision(revision: RevisionNode)`: Add revision to internal registry.
- `get_current_head(conn)`: Query current version from `alembic_version` or `None`.
- `upgrade_to(conn, target_revision_id)`:
  Trace the path from current head to target revision. For each revision in the path, execute its `upgrade_script`, update `alembic_version`, and commit. If target does not exist or prerequisites fail, raise `ValueError`.
- `downgrade_to(conn, target_revision_id)`:
  Trace backwards from current head to target revision. For each revision, execute `downgrade_script`, update `alembic_version`, and commit.
