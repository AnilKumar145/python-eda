import importlib.util
import pathlib
import pytest

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_1_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

ClinicalTriageEngine = _sol.ClinicalTriageEngine
TriageAssessment = _sol.TriageAssessment



def test_normal_vitals_scores_level_4_non_urgent():
    # Arrange
    vitals = {
        'heart_rate': 72,
        'respiratory_rate': 16,
        'spo2': 99,
        'systolic_bp': 120
    }

    # Act
    assessment = ClinicalTriageEngine.score_patient(vitals)

    # Assert
    assert assessment.total_score == 0
    assert assessment.acuity_level == "LEVEL_4_NON_URGENT"
    assert "Standard ambulatory queue" in assessment.recommended_action


def test_isolated_hypoxia_scores_level_2_emergent():
    # Arrange
    vitals = {
        'heart_rate': 85,
        'respiratory_rate': 18,
        'spo2': 89,  # Hypoxia triggers +3 points
        'systolic_bp': 125
    }

    # Act
    assessment = ClinicalTriageEngine.score_patient(vitals)

    # Assert
    assert assessment.total_score == 3
    assert assessment.acuity_level == "LEVEL_2_EMERGENT"
    assert "Rapid physician evaluation" in assessment.recommended_action


def test_multi_system_instability_scores_level_1_resuscitation():
    # Arrange: Severe tachycardia, tachypnea, and hypotension
    vitals = {
        'heart_rate': 145,         # +3
        'respiratory_rate': 36,    # +3
        'spo2': 88,                # +3
        'systolic_bp': 75          # +2
    }

    # Act
    assessment = ClinicalTriageEngine.score_patient(vitals)

    # Assert
    assert assessment.total_score == 11
    assert assessment.acuity_level == "LEVEL_1_RESUSCITATION"
    assert "resuscitation bay" in assessment.recommended_action.lower()


def test_invalid_parameters_raise_value_error():
    # Arrange & Act & Assert for physiological bounds
    with pytest.raises(ValueError, match="Implausible SpO2"):
        ClinicalTriageEngine.score_patient({
            'heart_rate': 80,
            'respiratory_rate': 16,
            'spo2': 105,  # Exceeds 100%
            'systolic_bp': 120
        })

    with pytest.raises(ValueError, match="Missing required"):
        ClinicalTriageEngine.score_patient({
            'heart_rate': 80,
            'respiratory_rate': 16
        })
