"""
Unit 4.4 Exercises: Database Migrations
Student Starter - Implement migration runner and schema evolution helpers.
"""

import sqlite3
from typing import Optional, List, Tuple


class MigrationRunner:
    """Lightweight database schema migration engine simulating Alembic version tracking."""

    @staticmethod
    def init_version_table(conn: sqlite3.Connection) -> None:
        """
        Create table 'schema_versions' if not exists with:
        version_num TEXT PRIMARY KEY,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        """
        # TODO: Implement table creation
        pass

    @staticmethod
    def get_current_version(conn: sqlite3.Connection) -> Optional[str]:
        """
        Return the current version_num from schema_versions, or None if no migrations applied.
        """
        # TODO: Query version_num
        return None

    @staticmethod
    def apply_migration(
        conn: sqlite3.Connection,
        version_id: str,
        upgrade_sql: str,
        expected_down_version: Optional[str]
    ) -> bool:
        """
        Verify that current version matches expected_down_version.
        If it matches:
          1. Execute upgrade_sql
          2. Clear existing version in schema_versions and insert version_id
          3. Commit transaction and return True
        If it doesn't match:
          Raise ValueError(f"Version mismatch: expected {expected_down_version}, got {current}")
        """
        # TODO: Implement migration application
        return False

    @staticmethod
    def rollback_migration(
        conn: sqlite3.Connection,
        current_version: str,
        downgrade_sql: str,
        target_down_version: Optional[str]
    ) -> bool:
        """
        Verify that current version matches current_version.
        If it matches:
          1. Execute downgrade_sql
          2. Delete current_version from schema_versions
          3. If target_down_version is not None, insert target_down_version
          4. Commit transaction and return True
        If it doesn't match:
          Raise ValueError("Version mismatch on downgrade")
        """
        # TODO: Implement migration rollback
        return False


if __name__ == "__main__":
    print("Run the solutions file to test your implementations.")
