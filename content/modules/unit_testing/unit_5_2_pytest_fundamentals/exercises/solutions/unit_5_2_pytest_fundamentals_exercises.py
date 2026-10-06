"""
Unit 5.2 Exercises: pytest Fundamentals (Reference Solutions)
"""

from typing import List, Optional
import pytest


def is_pytest_discoverable(filename: str, class_name: Optional[str], function_name: str) -> bool:
    """
    Exercise 1: Test Discovery Rule Engine
    """
    if not filename.endswith(".py"):
        return False
    if not (filename.startswith("test_") or filename.endswith("_test.py")):
        return False

    if class_name is not None:
        if not class_name.startswith("Test") or len(class_name) <= 4:
            return False

    if not function_name.startswith("test_"):
        return False

    return True


def filter_tests_by_keyword(test_names: List[str], keyword_expr: str) -> List[str]:
    """
    Exercise 2: Keyword Expression Filter (-k simulator)
    """
    expr = keyword_expr.strip().lower()
    if expr.startswith("not "):
        negated_term = expr[4:].strip()
        return [t for t in test_names if negated_term not in t.lower()]
    else:
        return [t for t in test_names if expr in t.lower()]


def calculate_pediatric_amoxicillin_dose(weight_kg: float, mg_per_kg: float = 45.0, max_daily_mg: float = 1500.0) -> float:
    """
    Exercise 3: Pediatric Antibiotic Dosage Calculator
    """
    if weight_kg <= 0 or mg_per_kg <= 0:
        raise ValueError("Weight and mg/kg must be positive numbers")

    daily = weight_kg * mg_per_kg
    if daily > max_daily_mg:
        daily = max_daily_mg

    single_dose = daily / 3.0
    return round(single_dose, 1)


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
