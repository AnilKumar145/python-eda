"""
Test suite for Lab 1 Easy: Pharmacy Drug Formulary Schema Evolution Engine
"""

import sqlite3
import pytest
from solution.solution import FormularyMigrationEngine, RevisionNode


@pytest.fixture
def migration_fixture():
    conn = sqlite3.connect(":memory:")
    engine = FormularyMigrationEngine()
    engine.initialize_tracking(conn)

    # Revision 1: Initial Formulary
    r1 = RevisionNode(
        revision_id="001_initial_formulary",
        down_revision=None,
        upgrade_script="""
            CREATE TABLE formulary (
                drug_id INTEGER PRIMARY KEY,
                brand_name TEXT NOT NULL,
                strength_mg INTEGER NOT NULL
            );
        """,
        downgrade_script="DROP TABLE formulary;"
    )

    # Revision 2: Add Controlled Substance Schedule
    r2 = RevisionNode(
        revision_id="002_add_dea_schedule",
        down_revision="001_initial_formulary",
        upgrade_script="ALTER TABLE formulary ADD COLUMN dea_schedule TEXT DEFAULT 'NON_CONTROLLED';",
        downgrade_script="""
            CREATE TABLE formulary_bk (drug_id INTEGER PRIMARY KEY, brand_name TEXT NOT NULL, strength_mg INTEGER NOT NULL);
            INSERT INTO formulary_bk SELECT drug_id, brand_name, strength_mg FROM formulary;
            DROP TABLE formulary;
            ALTER TABLE formulary_bk RENAME TO formulary;
        """
    )

    # Revision 3: Add Cold Chain Requirement
    r3 = RevisionNode(
        revision_id="003_add_cold_chain",
        down_revision="002_add_dea_schedule",
        upgrade_script="ALTER TABLE formulary ADD COLUMN requires_refrigeration INTEGER DEFAULT 0;",
        downgrade_script="""
            CREATE TABLE formulary_bk (drug_id INTEGER PRIMARY KEY, brand_name TEXT NOT NULL, strength_mg INTEGER NOT NULL, dea_schedule TEXT);
            INSERT INTO formulary_bk SELECT drug_id, brand_name, strength_mg, dea_schedule FROM formulary;
            DROP TABLE formulary;
            ALTER TABLE formulary_bk RENAME TO formulary;
        """
    )

    engine.register_revision(r1)
    engine.register_revision(r2)
    engine.register_revision(r3)

    yield engine, conn
    conn.close()


def test_linear_upgrade_to_head(migration_fixture):
    engine, conn = migration_fixture

    assert engine.get_current_head(conn) is None

    # Upgrade to head (revision 3)
    engine.upgrade_to(conn, "003_add_cold_chain")
    assert engine.get_current_head(conn) == "003_add_cold_chain"

    # Insert data into evolved schema
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO formulary (drug_id, brand_name, strength_mg, dea_schedule, requires_refrigeration)
        VALUES (101, 'Insulin Glargine', 100, 'NON_CONTROLLED', 1);
    """)
    conn.commit()

    cursor.execute("SELECT brand_name, requires_refrigeration FROM formulary WHERE drug_id = 101;")
    row = cursor.fetchone()
    assert row == ("Insulin Glargine", 1)


def test_downgrade_and_reupgrade(migration_fixture):
    engine, conn = migration_fixture

    # Upgrade to 3
    engine.upgrade_to(conn, "003_add_cold_chain")
    assert engine.get_current_head(conn) == "003_add_cold_chain"

    # Downgrade back to revision 1
    engine.downgrade_to(conn, "001_initial_formulary")
    assert engine.get_current_head(conn) == "001_initial_formulary"

    # Verify cold_chain and dea_schedule are gone
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(formulary);")
    cols = [c[1] for c in cursor.fetchall()]
    assert "requires_refrigeration" not in cols
    assert "dea_schedule" not in cols
    assert "brand_name" in cols

    # Re-upgrade to 2
    engine.upgrade_to(conn, "002_add_dea_schedule")
    assert engine.get_current_head(conn) == "002_add_dea_schedule"


def test_invalid_target_revision_raises_error(migration_fixture):
    engine, conn = migration_fixture
    with pytest.raises(ValueError, match="not registered"):
        engine.upgrade_to(conn, "999_nonexistent")
