"""
Hospital Pharmacy Inventory Dispenser - Solution
"""

import threading
from typing import Dict, List, Any


class PharmacyDispenserEngine:
    def __init__(self, initial_inventory: Dict[str, int]):
        self._inventory = dict(initial_inventory)
        self.lock = threading.Lock()
        self.audit_log: List[dict] = []

    def dispense(self, drug_name: str, quantity: int, doctor_id: str) -> bool:
        with self.lock:
            current_stock = self._inventory.get(drug_name, 0)
            if current_stock >= quantity:
                self._inventory[drug_name] = current_stock - quantity
                self.audit_log.append({
                    "status": "SUCCESS",
                    "doctor": doctor_id,
                    "drug": drug_name,
                    "quantity": quantity
                })
                return True
            else:
                self.audit_log.append({
                    "status": "REJECTED",
                    "doctor": doctor_id,
                    "drug": drug_name,
                    "quantity": quantity
                })
                return False

    def get_stock(self, drug_name: str) -> int:
        with self.lock:
            return self._inventory.get(drug_name, 0)
