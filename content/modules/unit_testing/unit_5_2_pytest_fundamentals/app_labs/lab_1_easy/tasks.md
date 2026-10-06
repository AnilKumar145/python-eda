# Lab Tasks: Pediatric Dosage Calculator Test Harness

## Task 1: Clinical Medication Calculator Implementation
Implement `PediatricDosageCalculator.calculate_liquid_volume(weight_kg: float, mg_per_kg: float, concentration_mg_per_ml: float, max_dose_mg: float) -> DoseVolumeResult`:
- Check that `weight_kg > 0`, `mg_per_kg > 0`, and `concentration_mg_per_ml > 0`. If not, raise `ValueError`.
- Calculate `dose_mg = weight_kg * mg_per_kg`.
- If `dose_mg > max_dose_mg`, cap `dose_mg = max_dose_mg` and set `is_capped = True`. Otherwise `is_capped = False`.
- Calculate liquid volume: `volume_ml = round(dose_mg / concentration_mg_per_ml, 2)`.
- Return `DoseVolumeResult(dose_mg=dose_mg, volume_ml=volume_ml, is_capped=is_capped)`.

## Task 2: Authoring the Pytest Test Harness
Author comprehensive test methods covering:
- Standard weight calculation within safe ceiling.
- Heavy child exceeding the maximum adult cap (verifying `is_capped == True`).
- Exception handling for invalid zero and negative weights.

## Task 3: Grouped Test Class Structure
Organize tests into a structured `TestPediatricLiquidDosing` class without an `__init__` constructor, ensuring full discoverability by pytest runners.
