from dataclasses import dataclass


@dataclass(frozen=True)
class DoseVolumeResult:
    dose_mg: float
    volume_ml: float
    is_capped: bool


class PediatricDosageCalculator:

    @staticmethod
    def calculate_liquid_volume(
        weight_kg: float,
        mg_per_kg: float,
        concentration_mg_per_ml: float,
        max_dose_mg: float = 500.0
    ) -> DoseVolumeResult:
        """
        Calculate liquid medicine volume in mL based on patient weight and oral suspension concentration.
        Raises ValueError if inputs are <= 0.
        """
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
