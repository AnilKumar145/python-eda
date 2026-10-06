from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass
class ReagentCartridge:
    lot_number: str
    remaining_tests: int
    is_unlocked: bool = True


@dataclass(frozen=True)
class LabTestResult:
    test_code: str
    value: float
    flag: str
    remaining_reagent: int


class ChemistryAnalyzer:
    REFERENCE_RANGES: Dict[str, Tuple[float, float]] = {
        "GLUCOSE": (70.0, 99.0),       # mg/dL
        "POTASSIUM": (3.5, 5.0),      # mmol/L
        "SODIUM": (135.0, 145.0)      # mmol/L
    }

    def __init__(self, cartridge: ReagentCartridge):
        self.cartridge = cartridge

    def run_test(self, test_code: str, value: float) -> LabTestResult:
        upper_code = test_code.upper()
        if upper_code not in self.REFERENCE_RANGES:
            raise KeyError(f"Unknown laboratory test code: {test_code}")

        if not self.cartridge.is_unlocked:
            raise RuntimeError("Reagent cartridge is locked/disposed")

        if self.cartridge.remaining_tests <= 0:
            raise RuntimeError("Reagent cartridge depleted (0 tests remaining)")

        # Consume 1 unit of consumable reagent
        self.cartridge.remaining_tests -= 1

        low, high = self.REFERENCE_RANGES[upper_code]
        if value < low:
            flag = "LOW"
        elif value > high:
            flag = "HIGH"
        else:
            flag = "NORMAL"

        return LabTestResult(
            test_code=upper_code,
            value=value,
            flag=flag,
            remaining_reagent=self.cartridge.remaining_tests
        )
