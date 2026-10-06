"""
Unit 5.5 Exercises: Exceptions and Edge Cases (Starter Code)
Implement each function to satisfy the test assertions.
"""

from typing import Set
import pytest


class IncompatibleBloodTransfusionError(Exception):
    def __init__(self, donor_abo: str, recipient_abo: str, reason: str):
        super().__init__(reason)
        self.donor_abo = donor_abo
        self.recipient_abo = recipient_abo
        self.reason = reason


VALID_ABO_GROUPS = {"O", "A", "B", "AB"}

COMPATIBILITY_MAP = {
    "O": {"O", "A", "B", "AB"},
    "A": {"A", "AB"},
    "B": {"B", "AB"},
    "AB": {"AB"}
}


def validate_abo_compatibility(donor: str, recipient: str) -> bool:
    """
    Exercise 1: Blood Transfusion ABO Compatibility Validator
    1. Normalize donor and recipient strings to uppercase.
    2. If either is not in VALID_ABO_GROUPS, raise ValueError(f"Invalid blood group: '{value}'").
    3. If recipient is in COMPATIBILITY_MAP[donor], return True.
    4. Otherwise, raise IncompatibleBloodTransfusionError(donor, recipient, f"Incompatible transfusion: {donor} to {recipient}").
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Exercise 2: Body Mass Index (BMI) Calculator
    Formula: weight_kg / (height_m ** 2)
    Safety boundaries:
    - weight_kg must be between 1.0 and 500.0 kg inclusive
    - height_m must be between 0.3 and 2.8 meters inclusive
    Raises ValueError with descriptive message if outside physiological boundaries.
    Return BMI rounded to 1 decimal place.
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

def test_compatible_transfusions():
    assert validate_abo_compatibility("O", "A") is True
    assert validate_abo_compatibility("A", "AB") is True
    assert validate_abo_compatibility("AB", "AB") is True


def test_incompatible_transfusion_raises_custom_exception():
    with pytest.raises(IncompatibleBloodTransfusionError) as exc_info:
        validate_abo_compatibility("A", "B")

    err = exc_info.value
    assert err.donor_abo == "A"
    assert err.recipient_abo == "B"
    assert "Incompatible transfusion: A to B" in str(err)


def test_invalid_blood_group_raises_value_error_with_match():
    with pytest.raises(ValueError, match="Invalid blood group: 'XYZ'"):
        validate_abo_compatibility("XYZ", "A")


def test_bmi_valid_calculation():
    # 70 kg, 1.75 m -> 70 / (1.75^2) = 22.857... -> 22.9
    assert calculate_bmi(70.0, 1.75) == 22.9


@pytest.mark.parametrize("weight, height", [
    (0.5, 1.70),    # Weight too low (< 1.0)
    (600.0, 1.70),  # Weight too high (> 500.0)
    (70.0, 0.20),   # Height too low (< 0.3)
    (70.0, 3.20),   # Height too high (> 2.8)
    (-10.0, 1.70),  # Negative weight
])
def test_bmi_boundary_violations_raise_value_error(weight, height):
    with pytest.raises(ValueError):
        calculate_bmi(weight, height)
