# Lab Tasks: Emergency Triage Patient Scoring Test Suite

## Task 1: Clinical Triage Scoring Algorithm
Implement `ClinicalTriageEngine.score_patient(vitals: Dict[str, Any]) -> TriageAssessment`:
- Extract `heart_rate` (bpm), `respiratory_rate` (breaths/min), `spo2` (percentage), and `systolic_bp` (mmHg).
- If any vital value is out of plausible physiological bounds (e.g., negative, heart_rate > 300, spo2 > 100), raise `ValueError`.
- Compute Modified Early Warning points:
  - `spo2 < 92`: +3 points
  - `heart_rate > 130` or `heart_rate < 40`: +3 points
  - `respiratory_rate > 30` or `respiratory_rate < 8`: +3 points
  - `systolic_bp < 90`: +2 points
- Acuity Level:
  - `>= 6 points`: `LEVEL_1_RESUSCITATION`
  - `3 to 5 points`: `LEVEL_2_EMERGENT`
  - `1 to 2 points`: `LEVEL_3_URGENT`
  - `0 points`: `LEVEL_4_NON_URGENT`

## Task 2: Implement AAA Unit Tests
Implement unit test functions in the test suite that follow strict Arrange-Act-Assert structure:
- `test_patient_with_hypoxia_scores_level_2()`
- `test_patient_with_multi_organ_instability_scores_resuscitation()`
- `test_unphysiological_vitals_raises_value_error()`

## Task 3: Test Suite Integrity & Isolation
Verify that test executions are side-effect free:
- Tests must not mutate shared mutable dictionaries.
- Tests must be completely deterministic and order-independent.
