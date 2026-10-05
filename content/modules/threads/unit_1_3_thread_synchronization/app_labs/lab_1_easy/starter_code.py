"""
Hospital Pharmacy Inventory Dispenser - Starter Code
"""

import threading
import time
from typing import Dict, List, Any


class PharmacyDispenserEngine:
    """Thread-safe medication dispensing and inventory manager."""
    
    def __init__(self, initial_inventory: Dict[str, int]):
        # ====================================================================
        # WRITE CODE HERE (Task 1)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def dispense(self, drug_name: str, quantity: int, doctor_id: str) -> bool:
        """
        Atomically check inventory, decrement if available, and record audit entry.
        Returns True if dispensed, False if insufficient stock.
        """
        # ====================================================================
        # WRITE CODE HERE (Task 2)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================

    def get_stock(self, drug_name: str) -> int:
        """Return the current stock level for a medication."""
        # ====================================================================
        # WRITE CODE HERE (Task 3)
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
        # ====================================================================
