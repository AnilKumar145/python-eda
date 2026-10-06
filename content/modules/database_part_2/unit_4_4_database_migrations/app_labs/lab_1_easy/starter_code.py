"""
Lab 1 Easy: Pharmacy Drug Formulary Schema Evolution Engine
Student Starter Code
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
        # TODO: Register revision node
        pass

    def initialize_tracking(self, conn: sqlite3.Connection) -> None:
        # TODO: Create alembic_version table
        pass

    def get_current_head(self, conn: sqlite3.Connection) -> Optional[str]:
        # TODO: Return current revision from alembic_version
        return None

    def upgrade_to(self, conn: sqlite3.Connection, target_revision: str) -> None:
        # TODO: Apply upgrades sequentially to reach target_revision
        pass

    def downgrade_to(self, conn: sqlite3.Connection, target_revision: Optional[str]) -> None:
        # TODO: Apply downgrades sequentially to reach target_revision
        pass
