"""
Unit 5.1 Exercises: Testing Fundamentals (Reference Solutions)
"""

from typing import Tuple, List, Callable, Dict
import pytest
import re


def format_test_name(unit_name: str, condition: str, expected_result: str) -> str:
    """
    Exercise 1: Format a semantic test function name.
    Pattern: test_<unit_name>_<condition>_<expected_result>
    Convert all spaces, hyphens to underscores, ensure lowercase, and remove consecutive underscores.
    """
    raw = f"test_{unit_name}_{condition}_{expected_result}".lower()
    cleaned = re.sub(r"[\s\-]+", "_", raw)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


def evaluate_triage_acuity(heart_rate: int, spo2: int, systolic: int) -> Tuple[int, str]:
    """
    Exercise 2: Clinical Triage Acuity Evaluator
    Calculate emergency acuity points:
    - Heart Rate: +2 if hr > 120 or hr < 50, otherwise 0
    - Oxygen Saturation (SpO2): +3 if spo2 < 90, otherwise 0
    - Systolic BP: +2 if systolic < 90, otherwise 0

    Classification:
    - Total points >= 4: "RESUSCITATION"
    - Total points >= 2: "EMERGENT"
    - Otherwise: "STABLE"

    Return tuple: (total_points, classification)
    """
    points = 0
    if heart_rate > 120 or heart_rate < 50:
        points += 2
    if spo2 < 90:
        points += 3
    if systolic < 90:
        points += 2

    if points >= 4:
        classification = "RESUSCITATION"
    elif points >= 2:
        classification = "EMERGENT"
    else:
        classification = "STABLE"

    return points, classification


def run_isolated_test_suite(test_cases: List[Callable[[], bool]]) -> Dict[str, int]:
    """
    Exercise 3: Test Suite Runner with Strict Isolation
    Execute each test callable in isolation.
    - If callable returns True without exception: count as 'passed'
    - If callable returns False or raises AssertionError/Exception: count as 'failed'
    Return dictionary: {'passed': int, 'failed': int, 'total': int}
    """
    passed = 0
    failed = 0
    for test in test_cases:
        try:
            result = test()
            if result is True:
                passed += 1
            else:
                failed += 1
        except Exception:
            failed += 1
        except AssertionError:
            failed += 1

    return {"passed": passed, "failed": failed, "total": len(test_cases)}


# ====================================================================
# Verification Tests
# ====================================================================

def test_semantic_naming():
    name = format_test_name("dosage calc", "zero-weight", "raises error")
    assert name == "test_dosage_calc_zero_weight_raises_error"

    name2 = format_test_name("Admit-Patient", "ward full", "returns false")
    assert name2 == "test_admit_patient_ward_full_returns_false"


def test_triage_acuity_resuscitation_aaa():
    # Arrange
    hr = 130
    spo2 = 88
    systolic = 85

    # Act
    score, category = evaluate_triage_acuity(hr, spo2, systolic)

    # Assert
    assert score == 7
    assert category == "RESUSCITATION"


def test_triage_acuity_stable_aaa():
    # Arrange
    hr = 75
    spo2 = 98
    systolic = 120

    # Act
    score, category = evaluate_triage_acuity(hr, spo2, systolic)

    # Assert
    assert score == 0
    assert category == "STABLE"


def test_isolated_test_runner():
    tests = [
        lambda: True,
        lambda: False,
        lambda: 1 / 0 == 0,  # ZeroDivisionError
        lambda: True
    ]
    results = run_isolated_test_suite(tests)
    assert results == {"passed": 2, "failed": 2, "total": 4}
