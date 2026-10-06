from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class TriageAssessment:
    total_score: int
    acuity_level: str
    recommended_action: str


class ClinicalTriageEngine:

    @staticmethod
    def score_patient(vitals: Dict[str, Any]) -> TriageAssessment:
        """
        Calculates triage assessment from vital signs dictionary.
        Keys required: 'heart_rate', 'respiratory_rate', 'spo2', 'systolic_bp'
        Raises ValueError if values are physiologically impossible.
        """
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
