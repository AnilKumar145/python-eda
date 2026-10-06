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
        required = ['heart_rate', 'respiratory_rate', 'spo2', 'systolic_bp']
        for k in required:
            if k not in vitals:
                raise ValueError(f"Missing required vital parameter: {k}")

        hr = vitals['heart_rate']
        rr = vitals['respiratory_rate']
        spo2 = vitals['spo2']
        sbp = vitals['systolic_bp']

        if not (20 <= hr <= 300):
            raise ValueError(f"Implausible heart rate: {hr}")
        if not (0 <= rr <= 80):
            raise ValueError(f"Implausible respiratory rate: {rr}")
        if not (40 <= spo2 <= 100):
            raise ValueError(f"Implausible SpO2: {spo2}")
        if not (30 <= sbp <= 300):
            raise ValueError(f"Implausible systolic BP: {sbp}")

        score = 0
        if spo2 < 92:
            score += 3
        if hr > 130 or hr < 40:
            score += 3
        if rr > 30 or rr < 8:
            score += 3
        if sbp < 90:
            score += 2

        if score >= 6:
            acuity = "LEVEL_1_RESUSCITATION"
            action = "Immediate trauma/code resuscitation bay"
        elif score >= 3:
            acuity = "LEVEL_2_EMERGENT"
            action = "Rapid physician evaluation within 15 minutes"
        elif score >= 1:
            acuity = "LEVEL_3_URGENT"
            action = "Monitored observation bed"
        else:
            acuity = "LEVEL_4_NON_URGENT"
            action = "Standard ambulatory queue"

        return TriageAssessment(total_score=score, acuity_level=acuity, recommended_action=action)
