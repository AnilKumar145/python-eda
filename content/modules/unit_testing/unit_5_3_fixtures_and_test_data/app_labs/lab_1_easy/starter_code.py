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
        """
        Runs a test, consumes 1 reagent unit, and flags outcome (LOW, NORMAL, HIGH).
        Raises RuntimeError if cartridge is depleted or unlocked is False.
        Raises KeyError if test_code is unknown.
        """
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
