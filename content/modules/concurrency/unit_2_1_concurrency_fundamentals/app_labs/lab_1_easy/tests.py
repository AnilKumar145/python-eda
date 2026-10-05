"""
Clinical Workload Router and Profiler - Tests
"""

try:
    from solution.solution import ClinicalWorkloadRouter, classify_job
except (ImportError, ModuleNotFoundError):
    from starter_code import ClinicalWorkloadRouter, classify_job


def test_classification():
    assert classify_job({"id": "1", "category": "database_query"}) == "IO"
    assert classify_job({"id": "2", "category": "genomic_alignment"}) == "CPU"
    assert classify_job({"id": "3", "category": "rest_poll"}) == "IO"
    assert classify_job({"id": "4", "category": "fourier_transform"}) == "CPU"
    print("Test 1 passed! Job classification accurate.")


def test_router_partitioning():
    router = ClinicalWorkloadRouter()
    jobs = [
        {"id": "JOB-1", "category": "database_lookup"},
        {"id": "JOB-2", "category": "genomic_pipeline"},
        {"id": "JOB-3", "category": "network_sync"},
        {"id": "JOB-4", "category": "crypto_hash"},
        {"id": "JOB-5", "category": "rest_api"},
    ]
    
    result = router.route_and_execute(jobs)
    assert result["io_count"] == 3
    assert result["cpu_count"] == 2
    assert result["io_job_ids"] == ["JOB-1", "JOB-3", "JOB-5"]
    assert result["cpu_job_ids"] == ["JOB-2", "JOB-4"]
    print("Test 2 passed! Router correctly segregated jobs.")


if __name__ == "__main__":
    test_classification()
    test_router_partitioning()
    print("All Unit 2.1 lab tests passed!")
