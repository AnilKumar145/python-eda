"""
Unit 5.3 Exercises: Fixtures and Test Data (Starter Code)
Implement each function and test fixture to satisfy the assertions.
"""

from typing import List, Dict, Any, Generator
import pathlib
import pytest


def classify_serum_potassium(k_level: float) -> str:
    """
    Exercise 1: Serum Potassium Evaluator (mmol/L)
    Reference bounds:
    - Normal range: 3.5 to 5.0 inclusive -> "NORMAL"
    - Below 3.5: "HYPOKALEMIA"
    - Above 5.0: "HYPERKALEMIA"
    - Plausibility safety check: if k_level < 1.0 or k_level > 10.0, raise ValueError.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


def write_lab_report_csv(file_path: pathlib.Path, records: List[Dict[str, Any]]) -> int:
    """
    Exercise 2: Lab Report File Exporter
    Write records to file_path as CSV with header: "test_name,value,unit".
    Return the total number of lines written (header + data rows).
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


# ====================================================================
# Verification Fixtures and Tests
# ====================================================================

# Global tracker to verify teardown
TEARDOWN_LOG = []


@pytest.fixture
def managed_reagent_lot() -> Generator[Dict[str, Any], None, None]:
    """
    Exercise 3: Setup & Teardown Fixture
    - Before yield: create reagent lot dict {'lot_id': 'LOT-2026', 'tests_remaining': 100, 'active': True}
    - Yield the lot dict
    - After yield: set lot['active'] = False and append lot_id to TEARDOWN_LOG
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    yield {}
    # ====================================================================
    # END OF YOUR CODE


@pytest.mark.parametrize("level, expected", [
    (2.8, "HYPOKALEMIA"),
    (3.4, "HYPOKALEMIA"),
    (3.5, "NORMAL"),      # Boundary
    (4.2, "NORMAL"),
    (5.0, "NORMAL"),      # Boundary
    (5.1, "HYPERKALEMIA"),
    (6.5, "HYPERKALEMIA"),
])
def test_potassium_classification_matrix(level, expected):
    assert classify_serum_potassium(level) == expected


def test_potassium_implausible_raises():
    with pytest.raises(ValueError):
        classify_serum_potassium(0.5)

    with pytest.raises(ValueError):
        classify_serum_potassium(12.0)


def test_managed_reagent_lot_lifecycle(managed_reagent_lot):
    assert managed_reagent_lot['lot_id'] == 'LOT-2026'
    assert managed_reagent_lot['active'] is True
    managed_reagent_lot['tests_remaining'] -= 10
    assert managed_reagent_lot['tests_remaining'] == 90


def test_lab_report_csv_with_tmp_path(tmp_path):
    out_file = tmp_path / "potassium_report.csv"
    data = [
        {"test_name": "Potassium", "value": 4.1, "unit": "mmol/L"},
        {"test_name": "Sodium", "value": 140, "unit": "mmol/L"}
    ]
    lines_written = write_lab_report_csv(out_file, data)
    assert lines_written == 3
    assert out_file.exists()
    content = out_file.read_text()
    assert "test_name,value,unit" in content
    assert "Potassium,4.1,mmol/L" in content
