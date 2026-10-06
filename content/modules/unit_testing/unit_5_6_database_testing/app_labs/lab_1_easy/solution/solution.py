"""
Pharmacy Medication Inventory Repository Reference Implementation
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
        normalized_sku = sku.strip().upper()
        item = InventoryItem(
            sku=normalized_sku,
            name=name.strip(),
            category=category.strip().upper(),
            quantity=quantity,
            reorder_threshold=reorder_threshold,
            unit_cost=unit_cost
        )
        self.session.add(item)
        self.session.commit()
        return item

    def get_by_sku(self, sku: str) -> Optional[InventoryItem]:
        normalized_sku = sku.strip().upper()
        stmt = select(InventoryItem).where(InventoryItem.sku == normalized_sku)
        return self.session.scalars(stmt).first()

    def dispense_medication(self, sku: str, amount: int) -> InventoryItem:
        if amount <= 0:
            raise ValueError(f"Dispense amount must be strictly positive: got {amount}")

        item = self.get_by_sku(sku)
        if not item:
            raise ValueError(f"Medication SKU '{sku}' not found in inventory.")

        if item.quantity < amount:
            raise StockDiscrepancyError(sku=item.sku, requested=amount, available=item.quantity)

        item.quantity -= amount
        self.session.commit()
        return item

    def restock_medication(self, sku: str, amount: int) -> InventoryItem:
        if amount <= 0:
            raise ValueError(f"Restock amount must be strictly positive: got {amount}")

        item = self.get_by_sku(sku)
        if not item:
            raise ValueError(f"Medication SKU '{sku}' not found in inventory.")

        item.quantity += amount
        self.session.commit()
        return item

    def get_items_requiring_reorder(self) -> List[InventoryItem]:
        stmt = (
            select(InventoryItem)
            .where(InventoryItem.quantity <= InventoryItem.reorder_threshold)
            .order_by(InventoryItem.quantity.asc())
        )
        return list(self.session.scalars(stmt).all())

    def calculate_inventory_value(self) -> float:
        stmt = select(func.sum(InventoryItem.quantity * InventoryItem.unit_cost))
        total = self.session.scalar(stmt)
        return round(float(total or 0.0), 2)
