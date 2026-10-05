"""
Multi-Service Clinical Diagnostics Aggregator - Tests
"""

import time
try:
    from solution.solution import ClinicalDiagnosticsAggregator
except (ImportError, ModuleNotFoundError):
    from starter_code import ClinicalDiagnosticsAggregator


def mock_lab(patient_id):
    time.sleep(0.15)
    return {"glucose": 95, "wbc": 6.2}

def mock_radiology(patient_id):
    time.sleep(0.20)
    return {"xray": "Chest scan clear"}

def mock_cardiology(patient_id):
    time.sleep(0.10)
    return {"ecg": "Normal Sinus Rhythm"}

def mock_failing_genomics(patient_id):
    time.sleep(0.12)
    raise ConnectionResetError("Genomic PACS cluster unreachable")


def test_concurrent_panel_aggregation():
    aggregator = ClinicalDiagnosticsAggregator(max_workers=4)
    queries = {
        "Lab": mock_lab,
        "Radiology": mock_radiology,
        "Cardiology": mock_cardiology,
    }
    
    start_time = time.perf_counter()
    results = aggregator.aggregate_patient_record("PAT-001", queries)
    elapsed = time.perf_counter() - start_time
    
    # Sequential would take 0.15 + 0.20 + 0.10 = 0.45s
    # Concurrent should take max(0.15, 0.20, 0.10) = ~0.20s (allow up to 0.35s)
    assert elapsed < 0.38, f"Execution too slow: {elapsed:.2f}s"
    assert len(results) == 3
    assert results["Lab"]["status"] == "SUCCESS"
    assert results["Lab"]["data"]["glucose"] == 95
    assert results["Radiology"]["status"] == "SUCCESS"
    assert results["Cardiology"]["status"] == "SUCCESS"
    print(f"Test 1 passed! All 3 services aggregated concurrently in {elapsed:.2f}s.")


def test_error_isolation():
    aggregator = ClinicalDiagnosticsAggregator(max_workers=4)
    queries = {
        "Cardiology": mock_cardiology,
        "Genomics": mock_failing_genomics,
    }
    
    results = aggregator.aggregate_patient_record("PAT-002", queries)
    assert len(results) == 2
    assert results["Cardiology"]["status"] == "SUCCESS"
    assert results["Genomics"]["status"] == "FAILED"
    assert "Genomic PACS cluster unreachable" in results["Genomics"]["error"]
    print("Test 2 passed! Failing genomic service isolated without halting cardiology results.")


def test_empty_queries():
    aggregator = ClinicalDiagnosticsAggregator()
    results = aggregator.aggregate_patient_record("PAT-EMPTY", {})
    assert results == {}
    print("Test 3 passed! Empty queries handled cleanly.")


if __name__ == "__main__":
    test_concurrent_panel_aggregation()
    test_error_isolation()
    test_empty_queries()
    print("All Unit 1.5 lab tests passed!")
