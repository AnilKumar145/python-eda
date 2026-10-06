# Lesson 4.4: Alembic Architecture, Schema Evolution, and Version Management

---

## 1. Conceptual Foundation

In real-world software engineering, application requirements evolve constantly. A hospital electronic medication system might initially record only `medication_name` and `dosage`. Three months later, federal regulations require tracking national drug codes (`ndc_code`), manufacturer serial numbers, and temperature storage requirements.

How do you update the database schema across Development, Staging, and Production environments without losing existing patient records or requiring application downtime?

Calling `Base.metadata.create_all()` **cannot update existing tables**—it only creates tables that do not yet exist. Running manual, ad-hoc `ALTER TABLE` queries in production leads to **schema drift**, where staging and production databases diverge, causing sudden runtime crashes.

**Database Migrations** provide version control for your database schema. **Alembic** is the official database migration tool for SQLAlchemy. It models schema mutations as incremental, reversible Python script revisions, allowing teams to advance (`upgrade`) or roll back (`downgrade`) schemas deterministically.

```
[ Git Code Repository ]                      [ Target Database ]
  alembic/versions/                            +-----------------------+
    ├── 1a2b_create_drugs.py (base)            | alembic_version       |
    ├── 3c4d_add_ndc_code.py                   | version_num: '3c4d'   |
    └── 5e6f_add_cold_chain.py (head)          +-----------------------+
                                                         ^
                    alembic upgrade head                 |
                    -------------------> Updates schema & moves pointer
```

---

## 2. Architecture & Internal Mechanics

### Alembic Directory Layout
When you initialize an Alembic workspace via `alembic init alembic`, it generates:
- **`alembic.ini`**: Global configuration file defining database connection URLs, logging parameters, and template paths.
- **`alembic/env.py`**: The Python script executed whenever Alembic runs. It imports your SQLAlchemy `Base.metadata` as `target_metadata` and orchestrates database connectivity.
- **`alembic/script.py.mako`**: The template file used to generate new revision scripts.
- **`alembic/versions/`**: The folder containing all historical migration scripts.

### Revision Chains & Linked Lists
Alembic manages migrations as a **directed acyclic graph (DAG)** or linear linked list:
Each migration script defines:
- `revision: str`: A unique hash identifier (e.g. `"a1b2c3d4e5f6"`).
- `down_revision: Optional[str]`: The identifier of the preceding migration (or `None` for the initial root migration).

### The `alembic_version` Table
How does Alembic know which migrations have already been applied to your database?
Upon running its first migration, Alembic automatically creates a table named `alembic_version`:
```sql
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);
```
When you run `alembic upgrade head`, Alembic reads `version_num`, finds the path from the current version to `head`, executes each script's `upgrade()` function, and updates `version_num` accordingly.

---

## 3. Real-World Code Implementation & Patterns

### 1. Structure of an Alembic Migration Script
```python
"""add_ndc_and_storage_temp to medications

Revision ID: 3c4d5e6f7a8b
Revises: 1a2b3c4d5e6f
Create Date: 2026-10-06 10:00:00.000000
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3c4d5e6f7a8b'
down_revision: Union[str, None] = '1a2b3c4d5e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add new columns
    op.add_column('medications', sa.Column('ndc_code', sa.String(length=12), nullable=True))
    op.add_column('medications', sa.Column('requires_refrigeration', sa.Boolean(), server_default='0', nullable=False))
    
    # 2. Create index for fast lookups
    op.create_index('ix_medications_ndc', 'medications', ['ndc_code'], unique=True)


def downgrade() -> None:
    # Reverse operations in exact opposite order
    op.drop_index('ix_medications_ndc', table_name='medications')
    op.drop_column('medications', 'requires_refrigeration')
    op.drop_column('medications', 'ndc_code')
```

### 2. Programmatic Migration Execution in Python
In automated test harnesses and embedded microservices, migrations can be driven programmatically:
```python
from alembic.config import Config
from alembic import command

def run_migrations_to_head(db_url: str):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    # Upgrade to the latest revision
    command.upgrade(alembic_cfg, "head")

def rollback_single_migration(db_url: str):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    # Roll back exactly 1 step
    command.downgrade(alembic_cfg, "-1")
```

---

## 4. Failure Modes & Edge Cases

| Failure Mode | Symptoms | Root Cause & Resolution |
| :--- | :--- | :--- |
| **Adding `NOT NULL` without Default** | Migration crashes with `IntegrityError` or table lock failure. | Always add new columns as `nullable=True` or supply `server_default='...'` so existing rows satisfy constraint. |
| **Branch Conflict (Multiple Heads)** | Running `alembic upgrade head` aborts with `Multiple heads found`. | Occurs when two git branches each created a migration from the same `down_revision`. Merge with `alembic merge <rev1> <rev2>`. |
| **Asymmetric Downgrade** | `upgrade()` creates an index, but `downgrade()` forgets to drop it, causing errors on re-run. | Always write exact reverse operations in `downgrade()`. Test `upgrade -> downgrade -> upgrade` in CI. |
| **Lock Timeout under High Write Load** | `ALTER TABLE` requires an exclusive lock (`ACCESS EXCLUSIVE`), blocking web requests. | Set lock timeouts (`SET lock_timeout = '2s'`) and run heavy migrations during off-peak windows. |

---

## 5. Performance & Optimization: Expand-Contract Zero Downtime

When modifying an active column in a 24/7 hospital production system:
1. **Phase 1 (Expand)**: Add the new column as nullable (`new_column`). Deploy application version that writes to *both* old and new columns, reading from old.
2. **Phase 2 (Backfill)**: Run asynchronous background worker batching historical updates from `old_column` to `new_column`.
3. **Phase 3 (Switch)**: Deploy application version that reads exclusively from `new_column`.
4. **Phase 4 (Contract)**: Apply migration dropping `old_column`. Zero downtime achieved!

---

## 6. Industry Best Practices & Production Patterns

1. **Always Review Autogenerated Migrations**:
   `alembic revision --autogenerate` is a convenience, not magic. It cannot detect table renames (it interprets them as DROP then CREATE) or custom check constraints. Always inspect the generated `.py` file before committing.
2. **Never Edit an Already-Committed Production Migration**:
   Once a revision has been deployed to production, its file is immutable. Never edit it; author a new forward migration script.
3. **Track Migrations in CI/CD**:
   Validate migrations in your continuous integration pipeline against real database instances before merging pull requests.

---

## 7. Healthcare Domain Case Study: Pharmacy Drug Formulary Schema Evolution

Hospital pharmacies must comply with evolving FDA drug classifications. In 2026, regulatory compliance required all intravenous chemotherapy formulations to track hazardous drug storage flags (`is_hazardous_handling`) and DEA Schedule categories.

Using Alembic:
1. Revision `001_create_formulary`: Created core `drugs` and `dosages` tables.
2. Revision `002_add_fda_hazardous_flag`: Added `is_hazardous_handling` with `server_default='0'` without interrupting active ER medication dispensation.
3. Automated database testing verified that the schema upgrade executed in under 200 milliseconds without dropping active connections.

---

## 8. Hands-On Verification & Knowledge Check

1. Why does `Base.metadata.create_all()` fail to update existing database schemas when model attributes change?
2. What is the role of the `alembic_version` table in relational databases?
3. How does the Expand-Contract migration pattern allow teams to deploy schema changes with zero application downtime?
