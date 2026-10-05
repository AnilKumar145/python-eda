# Lab Level 1 Tasks: Hospital Pharmacy Inventory Dispenser

## Task 1: Initialization & Locks
**Difficulty**: Easy
**Points**: 10

### Objective
Initialize `PharmacyDispenserEngine` with an inventory mapping and a `threading.Lock`.

### Requirements
- `__init__(initial_inventory: Dict[str, int])`
  - Store a copy of `initial_inventory`.
  - Create `self.lock = threading.Lock()`.
  - Create `self.audit_log: List[dict] = []`.

---

## Task 2: Atomic Dispensation
**Difficulty**: Easy
**Points**: 15

### Objective
Implement `dispense(drug_name: str, quantity: int, doctor_id: str) -> bool`.

### Requirements
- Acquire `self.lock` using `with self.lock:`.
- Check if current stock for `drug_name` is `>= quantity`.
- If yes:
  - Decrement stock by `quantity`.
  - Append an audit entry `{"status": "SUCCESS", "doctor": doctor_id, "drug": drug_name, "quantity": quantity}`.
  - Return `True`.
- If no:
  - Append an audit entry `{"status": "REJECTED", "doctor": doctor_id, "drug": drug_name, "quantity": quantity}`.
  - Return `False`.

---

## Task 3: Thread-Safe Stock Inspection
**Difficulty**: Easy
**Points**: 5

### Objective
Implement `get_stock(drug_name: str) -> int`.

### Requirements
- Acquire `self.lock` and return the current available quantity for `drug_name` (default 0 if not present).
