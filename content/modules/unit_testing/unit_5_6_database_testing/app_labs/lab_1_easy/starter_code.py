"""
Pharmacy Medication Inventory Repository Starter Code

Implement all TODOs according to tasks.md.
"""

from typing import List, Optional
from sqlalchemy import create_engine, String, Integer, Float, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class StockDiscrepancyError(Exception):
    def __init__(self, sku: str, requested: int, available: int):
        super().__init__(f"Cannot dispense {requested} units of SKU '{sku}': only {available} units available.")
        self.sku = sku
        self.requested = requested
        self.available = available


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_threshold: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Float, nullable=False)


class PharmacyInventoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_item(
        self,
        sku: str,
        name: str,
        category: str,
        quantity: int,
        reorder_threshold: int,
        unit_cost: float
    ) -> InventoryItem:
        """
        TODO: Normalize SKU to uppercase. Create InventoryItem instance,
        add to self.session, commit, and return instance.
        """
        raise NotImplementedError("TODO: Implement add_item")

    def get_by_sku(self, sku: str) -> Optional[InventoryItem]:
        """
        TODO: Query item by uppercase SKU using select(InventoryItem).where(...).
        """
        raise NotImplementedError("TODO: Implement get_by_sku")

    def dispense_medication(self, sku: str, amount: int) -> InventoryItem:
        """
        TODO: Validate amount > 0. Fetch item by SKU. If not found, raise ValueError.
        If item.quantity < amount, raise StockDiscrepancyError.
        Decrement item.quantity, commit, and return item.
        """
        raise NotImplementedError("TODO: Implement dispense_medication")

    def restock_medication(self, sku: str, amount: int) -> InventoryItem:
        """
        TODO: Validate amount > 0. Fetch item by SKU. If not found, raise ValueError.
        Increment item.quantity, commit, and return item.
        """
        raise NotImplementedError("TODO: Implement restock_medication")

    def get_items_requiring_reorder(self) -> List[InventoryItem]:
        """
        TODO: Query items where quantity <= reorder_threshold, ordered by quantity asc.
        """
        raise NotImplementedError("TODO: Implement get_items_requiring_reorder")

    def calculate_inventory_value(self) -> float:
        """
        TODO: Calculate total inventory value sum(quantity * unit_cost) rounded to 2 decimals.
        """
        raise NotImplementedError("TODO: Implement calculate_inventory_value")
