import importlib.util
import pathlib
import pytest

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_2_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

PediatricDosageCalculator = _sol.PediatricDosageCalculator
DoseVolumeResult = _sol.DoseVolumeResult



class TestPediatricLiquidDosing:

    def test_standard_pediatric_dose_uncapped(self):
        # 12 kg toddler, 15 mg/kg paracetamol, 24 mg/mL syrup
        # 12 * 15 = 180 mg -> 180 / 24 = 7.5 mL
        result = PediatricDosageCalculator.calculate_liquid_volume(
            weight_kg=12.0,
            mg_per_kg=15.0,
            concentration_mg_per_ml=24.0,
            max_dose_mg=500.0
        )
        assert result.dose_mg == 180.0
        assert result.volume_ml == 7.5
        assert result.is_capped is False

    def test_heavy_pediatric_dose_hits_max_ceiling(self):
        # 45 kg child, 15 mg/kg -> 675 mg -> capped at 500 mg ceiling
        # 500 mg / 25 mg/mL = 20.0 mL
        result = PediatricDosageCalculator.calculate_liquid_volume(
            weight_kg=45.0,
            mg_per_kg=15.0,
            concentration_mg_per_ml=25.0,
            max_dose_mg=500.0
        )
        assert result.dose_mg == 500.0
        assert result.volume_ml == 20.0
        assert result.is_capped is True

    def test_negative_weight_raises_value_error(self):
        with pytest.raises(ValueError, match="Weight must be strictly positive"):
            PediatricDosageCalculator.calculate_liquid_volume(
                weight_kg=-4.0,
                mg_per_kg=10.0,
                concentration_mg_per_ml=20.0
            )

    def test_zero_concentration_raises_value_error(self):
        with pytest.raises(ValueError, match="Concentration must be strictly positive"):
            PediatricDosageCalculator.calculate_liquid_volume(
                weight_kg=10.0,
                mg_per_kg=10.0,
                concentration_mg_per_ml=0.0
            )
