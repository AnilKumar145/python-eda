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
        if weight_kg <= 0:
            raise ValueError(f"Weight must be strictly positive, got: {weight_kg}")
        if mg_per_kg <= 0:
            raise ValueError(f"Dose rate (mg/kg) must be strictly positive, got: {mg_per_kg}")
        if concentration_mg_per_ml <= 0:
            raise ValueError(f"Concentration must be strictly positive, got: {concentration_mg_per_ml}")

        calculated_mg = weight_kg * mg_per_kg
        if calculated_mg > max_dose_mg:
            final_mg = max_dose_mg
            is_capped = True
        else:
            final_mg = calculated_mg
            is_capped = False

        vol = round(final_mg / concentration_mg_per_ml, 2)
        return DoseVolumeResult(dose_mg=final_mg, volume_ml=vol, is_capped=is_capped)
