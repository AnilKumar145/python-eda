import importlib.util
import pathlib
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_6_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

Base = _sol.Base
InventoryItem = _sol.InventoryItem
PharmacyInventoryRepository = _sol.PharmacyInventoryRepository
StockDiscrepancyError = _sol.StockDiscrepancyError



@pytest.fixture(scope="function")
def db_session():
    """
    Creates an isolated in-memory SQLite database per test function.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def repo(db_session):
    return PharmacyInventoryRepository(db_session)


def test_add_and_retrieve_item(repo):
    item = repo.add_item(
        sku="cef-500",
        name="Cefazolin 500mg IV",
        category="ANTIBIOTIC",
        quantity=100,
        reorder_threshold=20,
        unit_cost=14.50
    )
    assert item.id is not None
    assert item.sku == "CEF-500"

    fetched = repo.get_by_sku("cef-500")
    assert fetched is not None
    assert fetched.name == "Cefazolin 500mg IV"
    assert fetched.category == "ANTIBIOTIC"
    assert fetched.quantity == 100


def test_duplicate_sku_raises_integrity_error(repo):
    repo.add_item("van-1000", "Vancomycin 1g", "ANTIBIOTIC", 50, 15, 32.00)
    with pytest.raises(IntegrityError):
        repo.add_item("VAN-1000", "Vancomycin Generic", "ANTIBIOTIC", 10, 5, 30.00)


def test_dispense_medication_success(repo):
    repo.add_item("fent-50", "Fentanyl 50mcg/mL", "ANALGESIC", 60, 15, 18.75)
    updated = repo.dispense_medication("FENT-50", 25)
    assert updated.quantity == 35

    fetched = repo.get_by_sku("FENT-50")
    assert fetched.quantity == 35


def test_dispense_insufficient_stock_raises_stock_discrepancy_error(repo):
    repo.add_item("prop-10", "Propofol 10mg/mL", "ANESTHETIC", 5, 10, 42.00)

    with pytest.raises(StockDiscrepancyError) as exc_info:
        repo.dispense_medication("PROP-10", 12)

    err = exc_info.value
    assert err.sku == "PROP-10"
    assert err.requested == 12
    assert err.available == 5

    # Verify inventory untouched
    assert repo.get_by_sku("PROP-10").quantity == 5


def test_dispense_invalid_amount_raises_value_error(repo):
    repo.add_item("hepar-5k", "Heparin 5000 units", "ANTICOAGULANT", 80, 20, 9.20)
    with pytest.raises(ValueError, match="strictly positive"):
        repo.dispense_medication("HEPAR-5K", 0)

    with pytest.raises(ValueError, match="strictly positive"):
        repo.dispense_medication("HEPAR-5K", -5)


def test_dispense_nonexistent_sku_raises_value_error(repo):
    with pytest.raises(ValueError, match="not found"):
        repo.dispense_medication("NON-EXISTENT-SKU", 5)


def test_restock_medication_success(repo):
    repo.add_item("norepi-4", "Norepinephrine 4mg/4mL", "VASOPRESSOR", 15, 20, 55.00)
    updated = repo.restock_medication("norepi-4", 40)
    assert updated.quantity == 55

    fetched = repo.get_by_sku("NOREPI-4")
    assert fetched.quantity == 55


def test_get_items_requiring_reorder(repo):
    repo.add_item("MED-001", "Vasopressin 20 units", "VASOPRESSOR", 3, 10, 80.00)     # reorder (3 <= 10)
    repo.add_item("MED-002", "Ondansetron 4mg", "ANTIEMETIC", 100, 25, 4.50)         # ok
    repo.add_item("MED-003", "Dopamine 400mg", "VASOPRESSOR", 8, 15, 30.00)          # reorder (8 <= 15)
    repo.add_item("MED-004", "Lorazepam 2mg", "SEDATIVE", 12, 12, 11.00)              # reorder (12 <= 12)

    reorder_list = repo.get_items_requiring_reorder()
    assert len(reorder_list) == 3
    # Ordered by quantity asc: 3, 8, 12
    assert [item.sku for item in reorder_list] == ["MED-001", "MED-003", "MED-004"]


def test_calculate_inventory_value(repo):
    repo.add_item("A1", "Med A", "CAT1", 10, 5, 10.50)  # 105.0
    repo.add_item("B2", "Med B", "CAT2", 20, 5, 5.25)   # 105.0
    repo.add_item("C3", "Med C", "CAT3", 4, 2, 50.00)   # 200.0

    total_val = repo.calculate_inventory_value()
    assert total_val == 410.00


def test_database_isolation_between_test_runs(repo):
    # Verifies each test starts with a 100% empty schema
    assert repo.get_items_requiring_reorder() == []
    assert repo.calculate_inventory_value() == 0.0
