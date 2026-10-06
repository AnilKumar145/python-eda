# Lab Tasks: Pharmacy Medication Inventory Repository Test Harness

## Task 1: Declare the ORM Model & Exceptions
1. Create `StockDiscrepancyError(Exception)` storing `sku`, `requested`, and `available`.
2. Define `InventoryItem(Base)` with fields:
   - `id`: Integer primary key, autoincrement.
   - `sku`: String(50), unique=True, nullable=False.
   - `name`: String(100), nullable=False.
   - `category`: String(50), nullable=False.
   - `quantity`: Integer, nullable=False, default=0.
   - `reorder_threshold`: Integer, nullable=False, default=10.
   - `unit_cost`: Float, nullable=False.

## Task 2: Implement Repository CRUD Methods
Implement `PharmacyInventoryRepository`:
- `add_item(sku, name, category, quantity, reorder_threshold, unit_cost) -> InventoryItem`: Adds and commits record. Normalizes `sku` to uppercase.
- `get_by_sku(sku: str) -> Optional[InventoryItem]`: Queries by uppercase SKU.
- `dispense_medication(sku: str, amount: int) -> InventoryItem`: Decrements stock if sufficient; raises `StockDiscrepancyError` if insufficient; raises `ValueError` if `amount <= 0`.
- `restock_medication(sku: str, amount: int) -> InventoryItem`: Increments stock by amount; raises `ValueError` if `amount <= 0`.
- `get_items_requiring_reorder() -> List[InventoryItem]`: Selects items where `quantity <= reorder_threshold`, ordered by `quantity` ascending.
- `calculate_inventory_value() -> float`: Sums `(quantity * unit_cost)` across all medications rounded to 2 decimal places.

## Task 3: Test Harness Fixture Architecture
In `tests.py`:
- Implement a pytest fixture `db_session` with `scope="function"` that creates an in-memory SQLite engine (`sqlite:///:memory:`), creates all tables, yields the session, drops tables, and disposes the engine on teardown.
- Implement a `repo` fixture that supplies the repository connected to the test session.
