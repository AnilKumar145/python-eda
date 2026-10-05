"""
Clinical Workload Router and Profiler - Solution
"""

from typing import Dict, List, Any


def classify_job(job: Dict[str, Any]) -> str:
    cat = str(job.get("category", "")).lower()
    cpu_keys = ["genomic", "crypto", "fourier", "rendering"]
    for k in cpu_keys:
        if k in cat:
            return "CPU"
    return "IO"


class ClinicalWorkloadRouter:
    def route_and_execute(self, jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        io_jobs = []
        cpu_jobs = []
        
        for job in jobs:
            t = classify_job(job)
            if t == "CPU":
                cpu_jobs.append(job)
            else:
                io_jobs.append(job)
                
        return {
            "io_count": len(io_jobs),
            "cpu_count": len(cpu_jobs),
            "io_job_ids": [j["id"] for j in io_jobs],
            "cpu_job_ids": [j["id"] for j in cpu_jobs],
        }
