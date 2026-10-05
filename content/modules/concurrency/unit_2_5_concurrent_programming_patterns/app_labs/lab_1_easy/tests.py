"""
Verification Tests for Lab 1 Easy: Fan-Out / Fan-In Diagnostic Telemetry Aggregator
"""

import time
try:
    import solution.solution as starter_code
except (ImportError, ModuleNotFoundError):
    import starter_code
try:
    from solution.solution import DiagnosticAggregator
except (ImportError, ModuleNotFoundError):
    from starter_code import DiagnosticAggregator


def test_concurrent_fan_out_aggregation():
    def mock_ehr(pid):
        time.sleep(0.06)
        return {"allergies": ["Penicillin"], "blood_type": "O-"}

    def mock_labs(pid):
        time.sleep(0.06)
        return {"wbc": 7.2, "creatinine": 0.9}

    def mock_telemetry(pid):
        time.sleep(0.06)
        return {"heart_rate": 82, "spo2": 97}

    services = {
        "ehr": mock_ehr,
        "labs": mock_labs,
        "telemetry": mock_telemetry
    }

    t0 = time.perf_counter()
    report = DiagnosticAggregator.aggregate_patient_profile("PT-100", services, max_workers=3)
    elapsed = time.perf_counter() - t0

    assert report["patient_id"] == "PT-100"
    assert len(report["services"]) == 3
    # Sequential = 0.18s; Concurrent with 3 workers should take ~0.06-0.12s
    assert elapsed < 0.15, f"Fan-out was not concurrent: took {elapsed:.3f}s"
    assert report["services"]["ehr"]["status"] == "SUCCESS"
    assert report["services"]["ehr"]["data"]["blood_type"] == "O-"
    assert report["services"]["labs"]["data"]["wbc"] == 7.2
    print(f"Test 1 passed! Fan-Out executed in {elapsed:.3f}s with all services aggregated.")


def test_exception_shielding():
    def mock_healthy(pid):
        return {"status": "all_clear"}

    def mock_failing(pid):
        raise ConnectionResetError("PACS radiological imaging server unavailable")

    services = {
        "healthy_srv": mock_healthy,
        "failing_srv": mock_failing
    }

    report = DiagnosticAggregator.aggregate_patient_profile("PT-200", services, max_workers=2)
    assert report["patient_id"] == "PT-200"
    assert report["services"]["healthy_srv"]["status"] == "SUCCESS"
    assert report["services"]["healthy_srv"]["data"] == {"status": "all_clear"}
    
    assert report["services"]["failing_srv"]["status"] == "FAILED"
    assert "PACS radiological imaging server unavailable" in report["services"]["failing_srv"]["error"]
    print("Test 2 passed! Partial service failure was shielded without crashing the aggregator.")


if __name__ == "__main__":
    test_concurrent_fan_out_aggregation()
    test_exception_shielding()
    print("All Lab 1 Easy Tests Passed!")
