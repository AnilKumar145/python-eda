"""
Clinical Audit Log Quality Gate and Coverage Harness Reference Implementation
"""

from dataclasses import dataclass
import hashlib
from typing import List, Dict, Any, Optional


@dataclass
class AuditRecord:
    event_id: str
    actor_id: str
    patient_id: str
    action: str
    severity: str
    previous_hash: str
    current_hash: str


class ClinicalAuditLedger:
    VALID_SEVERITIES = {"INFO", "WARNING", "CRITICAL"}
    GENESIS_HASH = "GENESIS_00000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self.records: List[AuditRecord] = []

    @staticmethod
    def compute_hash(
        event_id: str,
        actor_id: str,
        patient_id: str,
        action: str,
        severity: str,
        previous_hash: str
    ) -> str:
        payload = f"{event_id}|{actor_id}|{patient_id}|{action}|{severity}|{previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def append_event(
        self,
        event_id: str,
        actor_id: str,
        patient_id: str,
        action: str,
        severity: str
    ) -> AuditRecord:
        if not event_id or not actor_id or not patient_id or not action or not severity:
            raise ValueError("All audit log fields must be non-empty strings.")

        norm_severity = severity.strip().upper()
        if norm_severity not in self.VALID_SEVERITIES:
            raise ValueError(f"Invalid severity '{severity}': must be one of {self.VALID_SEVERITIES}")

        prev_hash = self.records[-1].current_hash if self.records else self.GENESIS_HASH
        curr_hash = self.compute_hash(
            event_id=event_id.strip(),
            actor_id=actor_id.strip(),
            patient_id=patient_id.strip(),
            action=action.strip().upper(),
            severity=norm_severity,
            previous_hash=prev_hash
        )

        record = AuditRecord(
            event_id=event_id.strip(),
            actor_id=actor_id.strip(),
            patient_id=patient_id.strip(),
            action=action.strip().upper(),
            severity=norm_severity,
            previous_hash=prev_hash,
            current_hash=curr_hash
        )
        self.records.append(record)
        return record

    def verify_integrity(self) -> bool:
        if not self.records:
            return True

        expected_prev = self.GENESIS_HASH
        for rec in self.records:
            if rec.previous_hash != expected_prev:
                return False

            recalculated = self.compute_hash(
                rec.event_id,
                rec.actor_id,
                rec.patient_id,
                rec.action,
                rec.severity,
                rec.previous_hash
            )
            if rec.current_hash != recalculated:
                return False

            expected_prev = rec.current_hash

        return True

    def find_critical_breaches(self) -> List[AuditRecord]:
        return [r for r in self.records if r.severity == "CRITICAL"]

    def export_summary(self) -> Dict[str, Any]:
        counts = {"INFO": 0, "WARNING": 0, "CRITICAL": 0}
        for r in self.records:
            counts[r.severity] = counts.get(r.severity, 0) + 1

        return {
            "total_events": len(self.records),
            "severity_counts": counts,
            "is_intact": self.verify_integrity()
        }
