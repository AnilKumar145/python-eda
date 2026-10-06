"""
Unit 5.5 Exercises: Exceptions and Edge Cases (Reference Solutions)
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
    """
    d = donor.strip().upper()
    r = recipient.strip().upper()

    if d not in VALID_ABO_GROUPS:
        raise ValueError(f"Invalid blood group: '{donor}'")
    if r not in VALID_ABO_GROUPS:
        raise ValueError(f"Invalid blood group: '{recipient}'")

    if r in COMPATIBILITY_MAP[d]:
        return True

    raise IncompatibleBloodTransfusionError(
        donor_abo=d,
        recipient_abo=r,
        reason=f"Incompatible transfusion: {d} to {r}"
    )


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Exercise 2: Body Mass Index (BMI) Calculator
    """
    if not (1.0 <= weight_kg <= 500.0):
        raise ValueError(f"Weight outside physiological range (1.0 - 500.0 kg): {weight_kg}")
    if not (0.3 <= height_m <= 2.8):
        raise ValueError(f"Height outside physiological range (0.3 - 2.8 m): {height_m}")

    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


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
