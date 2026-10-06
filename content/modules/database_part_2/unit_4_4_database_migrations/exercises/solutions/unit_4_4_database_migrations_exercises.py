"""
Unit 4.4 Exercises: Database Migrations - Solutions & Test Verification
"""

import sqlite3
from typing import Optional, List, Tuple


class MigrationRunner:

    @staticmethod
    def init_version_table(conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_versions (
                version_num TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
        """)
        conn.commit()

    @staticmethod
    def get_current_version(conn: sqlite3.Connection) -> Optional[str]:
        cursor = conn.cursor()
        cursor.execute("SELECT version_num FROM schema_versions ORDER BY applied_at DESC LIMIT 1;")
        row = cursor.fetchone()
        return row[0] if row else None

    @staticmethod
    def apply_migration(
        conn: sqlite3.Connection,
        version_id: str,
        upgrade_sql: str,
        expected_down_version: Optional[str]
    ) -> bool:
        current = MigrationRunner.get_current_version(conn)
        if current != expected_down_version:
            raise ValueError(f"Version mismatch: expected {expected_down_version}, got {current}")

        cursor = conn.cursor()
        cursor.executescript(upgrade_sql)
        cursor.execute("DELETE FROM schema_versions;")
        cursor.execute("INSERT INTO schema_versions (version_num) VALUES (?);", (version_id,))
        conn.commit()
        return True

    @staticmethod
    def rollback_migration(
        conn: sqlite3.Connection,
        current_version: str,
        downgrade_sql: str,
        target_down_version: Optional[str]
    ) -> bool:
        current = MigrationRunner.get_current_version(conn)
        if current != current_version:
            raise ValueError(f"Version mismatch: expected current {current_version}, got {current}")

        cursor = conn.cursor()
        cursor.executescript(downgrade_sql)
        cursor.execute("DELETE FROM schema_versions;")
        if target_down_version is not None:
            cursor.execute("INSERT INTO schema_versions (version_num) VALUES (?);", (target_down_version,))
        conn.commit()
        return True


if __name__ == "__main__":
    print("Running Unit 4.4 Solutions Test Suite...")

    conn = sqlite3.connect(":memory:")

    # Step 1: Initialize
    MigrationRunner.init_version_table(conn)
    assert MigrationRunner.get_current_version(conn) is None, "Initial version must be None"
    print("Exercise 1 passed: Version table initialized.")

    # Step 2: Apply Migration v1 (Initial Table)
    v1_sql = """
        CREATE TABLE medications (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dosage_mg INTEGER NOT NULL
        );
    """
    MigrationRunner.apply_migration(conn, "v1_init_medications", v1_sql, None)
    assert MigrationRunner.get_current_version(conn) == "v1_init_medications", "Version must be v1"

    cursor = conn.cursor()
    cursor.execute("INSERT INTO medications VALUES (1, 'Amoxicillin', 500);")
    conn.commit()
    print("Exercise 2 passed: Migration v1 applied.")

    # Step 3: Apply Migration v2 (Add NDC Code column)
    v2_sql = "ALTER TABLE medications ADD COLUMN ndc_code TEXT;"
    MigrationRunner.apply_migration(conn, "v2_add_ndc_code", v2_sql, "v1_init_medications")
    assert MigrationRunner.get_current_version(conn) == "v2_add_ndc_code", "Version must be v2"

    cursor.execute("UPDATE medications SET ndc_code = '0093-0150-01' WHERE id = 1;")
    conn.commit()
    cursor.execute("SELECT ndc_code FROM medications WHERE id = 1;")
    assert cursor.fetchone()[0] == "0093-0150-01", "NDC code not saved"
    print("Exercise 3 passed: Migration v2 applied with column addition.")

    # Step 4: Rollback v2 to v1
    v2_downgrade_sql = """
        CREATE TABLE medications_backup (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dosage_mg INTEGER NOT NULL);
        INSERT INTO medications_backup SELECT id, name, dosage_mg FROM medications;
        DROP TABLE medications;
        ALTER TABLE medications_backup RENAME TO medications;
    """
    MigrationRunner.rollback_migration(conn, "v2_add_ndc_code", v2_downgrade_sql, "v1_init_medications")
    assert MigrationRunner.get_current_version(conn) == "v1_init_medications", "Reverted version must be v1"

    # Verify column was dropped
    cursor.execute("PRAGMA table_info(medications);")
    cols = [col[1] for col in cursor.fetchall()]
    assert "ndc_code" not in cols, "ndc_code column must not exist after rollback"
    assert "name" in cols and "dosage_mg" in cols, "Original columns must remain intact"
    print("Exercise 4 passed: Rollback to v1 executed cleanly.")

    conn.close()
    print("All Unit 4.4 Exercise Solutions PASSED!")
