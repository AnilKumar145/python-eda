"""
Unit 5.2 Exercises: pytest Fundamentals (Starter Code)
Implement each function to satisfy the test assertions.
"""

from typing import List, Optional
import pytest


def is_pytest_discoverable(filename: str, class_name: Optional[str], function_name: str) -> bool:
    """
    Exercise 1: Test Discovery Rule Engine
    Evaluate if an artifact conforms to pytest default discovery rules:
    - filename must start with 'test_' or end with '_test.py' (and end with .py)
    - If class_name is not None: it must start with 'Test' and not equal 'Test'
    - function_name must start with 'test_'
    Return True if all applicable conditions pass, False otherwise.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


def filter_tests_by_keyword(test_names: List[str], keyword_expr: str) -> List[str]:
    """
    Exercise 2: Keyword Expression Filter (-k simulator)
    Support two modes:
    - Normal substring: "dosage" -> names containing "dosage" (case-insensitive)
    - Negation: "not infant" -> names NOT containing "infant" (case-insensitive)
    Return the filtered list preserving original order.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


def calculate_pediatric_amoxicillin_dose(weight_kg: float, mg_per_kg: float = 45.0, max_daily_mg: float = 1500.0) -> float:
    """
    Exercise 3: Pediatric Antibiotic Dosage Calculator
    Daily dose = weight_kg * mg_per_kg (capped at max_daily_mg).
    Each single dose = daily_dose / 3.0 (administered TID: 3 times a day).
    Round returned single dose to 1 decimal place.
    Raises ValueError if weight_kg <= 0 or mg_per_kg <= 0.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


# ====================================================================
# Verification Tests
# ====================================================================

def test_pytest_discovery_rules():
    assert is_pytest_discoverable("test_vitals.py", None, "test_spo2") is True
    assert is_pytest_discoverable("vitals_test.py", "TestVitals", "test_heart_rate") is True
    assert is_pytest_discoverable("helpers.py", None, "test_helper") is False
    assert is_pytest_discoverable("test_api.py", "ApiTestSuite", "test_get") is False  # Class does not start with Test
    assert is_pytest_discoverable("test_calc.py", None, "calculate_sum") is False  # Function does not start with test_


def test_keyword_filtering():
    suite = [
        "test_infant_amoxicillin",
        "test_toddler_amoxicillin",
        "test_adult_ibuprofen",
        "test_infant_ibuprofen"
    ]
    assert filter_tests_by_keyword(suite, "amoxicillin") == [
        "test_infant_amoxicillin",
        "test_toddler_amoxicillin"
    ]
    assert filter_tests_by_keyword(suite, "not infant") == [
        "test_toddler_amoxicillin",
        "test_adult_ibuprofen"
    ]


def test_pediatric_dosage_calculation():
    # 10 kg infant, 45 mg/kg -> 450 mg daily -> 150 mg per dose
    assert calculate_pediatric_amoxicillin_dose(10.0) == 150.0

    # 40 kg child, 45 mg/kg -> 1800 mg (capped at 1500 mg) -> 500 mg per dose
    assert calculate_pediatric_amoxicillin_dose(40.0) == 500.0

    with pytest.raises(ValueError):
        calculate_pediatric_amoxicillin_dose(-5.0)
