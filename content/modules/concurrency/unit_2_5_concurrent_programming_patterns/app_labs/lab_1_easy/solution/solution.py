"""
Fan-Out / Fan-In Diagnostic Telemetry Aggregator - Solution
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Callable


class DiagnosticAggregator:
    @staticmethod
    def aggregate_patient_profile(
        patient_id: str,
        services: Dict[str, Callable[[str], Any]],
        max_workers: int = 3
    ) -> Dict[str, Any]:
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_service = {
                executor.submit(func, patient_id): name
                for name, func in services.items()
            }
            for fut in as_completed(future_to_service):
                srv_name = future_to_service[fut]
                try:
                    data = fut.result()
                    results[srv_name] = {"data": data, "status": "SUCCESS"}
                except Exception as exc:
                    results[srv_name] = {"error": str(exc), "status": "FAILED"}

        return {
            "patient_id": patient_id,
            "services": results
        }
