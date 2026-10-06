"""
Lab 1 Easy: Pharmacy Drug Formulary Schema Evolution Engine
Reference Solution
"""

import sqlite3
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class RevisionNode:
    revision_id: str
    down_revision: Optional[str]
    upgrade_script: str
    downgrade_script: str


class FormularyMigrationEngine:

    def __init__(self):
        self.revisions: Dict[str, RevisionNode] = {}

    def register_revision(self, node: RevisionNode) -> None:
        self.revisions[node.revision_id] = node

    def initialize_tracking(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num TEXT PRIMARY KEY
            );
        """)
        conn.commit()

    def get_current_head(self, conn: sqlite3.Connection) -> Optional[str]:
        cursor = conn.cursor()
        cursor.execute("SELECT version_num FROM alembic_version LIMIT 1;")
        row = cursor.fetchone()
        return row[0] if row else None

    def _set_version(self, conn: sqlite3.Connection, version: Optional[str]) -> None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alembic_version;")
        if version is not None:
            cursor.execute("INSERT INTO alembic_version (version_num) VALUES (?);", (version,))
        conn.commit()

    def _get_upgrade_chain(self, current: Optional[str], target: str) -> List[RevisionNode]:
        if target not in self.revisions:
            raise ValueError(f"Target revision '{target}' not registered")

        # Build path from target backwards to root
        path: List[RevisionNode] = []
        curr = target
        while curr is not None and curr != current:
            node = self.revisions.get(curr)
            if not node:
                raise ValueError(f"Broken migration chain at revision '{curr}'")
            path.append(node)
            curr = node.down_revision

        if curr != current:
            raise ValueError(f"Cannot trace upgrade path from '{current}' to '{target}'")

        path.reverse() # Execute forward from current to target
        return path

    def upgrade_to(self, conn: sqlite3.Connection, target_revision: str) -> None:
        current = self.get_current_head(conn)
        if current == target_revision:
            return

        chain = self._get_upgrade_chain(current, target_revision)
        cursor = conn.cursor()
        for node in chain:
            cursor.executescript(node.upgrade_script)
            self._set_version(conn, node.revision_id)

    def downgrade_to(self, conn: sqlite3.Connection, target_revision: Optional[str]) -> None:
        current = self.get_current_head(conn)
        if current == target_revision:
            return

        cursor = conn.cursor()
        curr = current
        while curr != target_revision and curr is not None:
            node = self.revisions.get(curr)
            if not node:
                raise ValueError(f"Cannot downgrade: revision '{curr}' not found")
            cursor.executescript(node.downgrade_script)
            curr = node.down_revision
            self._set_version(conn, curr)

        if curr != target_revision:
            raise ValueError(f"Cannot trace downgrade path to '{target_revision}'")
