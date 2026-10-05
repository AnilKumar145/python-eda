"""
Parallel ECG Arrhythmia Signal Analyzer - Solution
"""

from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Dict, Any


def process_lead_signal(lead_data: Tuple[str, List[float]]) -> Dict[str, Any]:
    lead_id, voltages = lead_data
    if not voltages:
        return {"lead_id": lead_id, "status": "EMPTY", "peak": 0.0, "mean": 0.0}
    peak = round(max(voltages), 2)
    mean = round(sum(voltages) / len(voltages), 2)
    return {"lead_id": lead_id, "status": "SUCCESS", "peak": peak, "mean": mean}


class ECGSignalProcessor:
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers

    def analyze_leads(self, lead_batch: List[Tuple[str, List[float]]]) -> List[Dict[str, Any]]:
        if not lead_batch:
            return []
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(process_lead_signal, lead_batch))
