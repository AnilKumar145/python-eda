"""
Bedside Monitor Telemetry Ingestion - Tests
"""

import time
try:
    from solution.solution import TelemetryIngestionEngine, read_sensor
except (ImportError, ModuleNotFoundError):
    from starter_code import TelemetryIngestionEngine, read_sensor


def test_concurrent_ingestion():
    engine = TelemetryIngestionEngine()
    configs = [
        ("BED-01-ECG", 0.3, 75),
        ("BED-01-SPO2", 0.2, 99.1),
        ("BED-01-BP", 0.4, "122/82")
    ]
    
    start_time = time.perf_counter()
    results = engine.poll_monitors(configs)
    elapsed = time.perf_counter() - start_time
    
    # Verification 1: All monitors polled
    assert len(results) == 3, f"Expected 3 records, got {len(results)}"
    assert "BED-01-ECG" in results
    assert results["BED-01-ECG"]["value"] == 75
    assert results["BED-01-SPO2"]["value"] == 99.1
    assert results["BED-01-BP"]["value"] == "122/82"
    
    # Verification 2: Concurrency speedup
    # Sequential would take 0.3 + 0.2 + 0.4 = 0.9s
    # Concurrent should take approx max(0.3, 0.2, 0.4) = 0.4s (allow up to 0.7s)
    assert elapsed < 0.75, f"Execution took {elapsed:.2f}s; threads did not run concurrently!"
    print(f"Test 1 passed! Elapsed: {elapsed:.2f}s (Concurrent speedup verified)")


def test_empty_monitors():
    engine = TelemetryIngestionEngine()
    results = engine.poll_monitors([])
    assert results == {}, f"Expected empty dict, got {results}"
    print("Test 2 passed! Empty monitors handled cleanly.")


def test_single_monitor():
    engine = TelemetryIngestionEngine()
    results = engine.poll_monitors([("BED-02-TEMP", 0.1, 98.6)])
    assert "BED-02-TEMP" in results
    assert results["BED-02-TEMP"]["value"] == 98.6
    print("Test 3 passed! Single monitor polled correctly.")


if __name__ == "__main__":
    test_concurrent_ingestion()
    test_empty_monitors()
    test_single_monitor()
    print("All lab tests passed!")
