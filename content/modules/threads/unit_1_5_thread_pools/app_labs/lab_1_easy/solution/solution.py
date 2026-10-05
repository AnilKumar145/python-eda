"""
Multi-Service Clinical Diagnostics Aggregator - Solution
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Dict, Any, Callable


class ClinicalDiagnosticsAggregator:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def aggregate_patient_record(
        self, 
        patient_id: str, 
        service_queries: Dict[str, Callable[[str], Any]]
    ) -> Dict[str, Dict[str, Any]]:
        if not service_queries:
            return {}
            
        results: Dict[str, Dict[str, Any]] = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_service = {
                executor.submit(func, patient_id): name
                for name, func in service_queries.items()
            }
            
            for future in as_completed(future_to_service):
                service_name = future_to_service[future]
                try:
                    data = future.result()
                    results[service_name] = {"status": "SUCCESS", "data": data}
                except Exception as exc:
                    results[service_name] = {"status": "FAILED", "error": str(exc)}
                    
        return results
