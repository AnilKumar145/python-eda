"""
Verification Tests for Lab 1 Easy: Asynchronous ICU Vital Signs Hub
"""

import asyncio
import time
try:
    import solution.solution as starter_code
except (ImportError, ModuleNotFoundError):
    import starter_code
try:
    from solution.solution import poll_bed, AsyncICUVitalHub
except (ImportError, ModuleNotFoundError):
    from starter_code import poll_bed, AsyncICUVitalHub


def test_concurrent_speedup_and_vitals():
    configs = [
        ("BED-101", 0.05, {"hr": 78, "spo2": 98}),
        ("BED-102", 0.06, {"hr": 88, "spo2": 95}),
        ("BED-103", 0.05, {"hr": 64, "spo2": 99}),
        ("BED-104", 0.07, {"hr": 110, "spo2": 92}),
    ]
    t0 = time.perf_counter()
    results = asyncio.run(AsyncICUVitalHub.poll_all_beds(configs, timeout_sec=0.2))
    elapsed = time.perf_counter() - t0

    assert len(results) == 4, f"Expected 4 results, got {len(results)}"
    # Sequential would take 0.05+0.06+0.05+0.07 = 0.23s. Concurrent should take ~0.07s-0.12s.
    assert elapsed < 0.18, f"Batch polling was not concurrent; took {elapsed:.3f}s"
    
    by_bed = {r["bed_id"]: r for r in results}
    assert by_bed["BED-101"]["status"] == "OK"
    assert by_bed["BED-101"]["vitals"]["hr"] == 78
    assert by_bed["BED-104"]["vitals"]["spo2"] == 92
    print(f"Test 1 passed! Concurrent polling executed in {elapsed:.3f}s with all vitals verified.")


def test_timeout_degradation():
    configs = [
        ("BED-201", 0.04, {"hr": 72, "spo2": 97}),
        ("BED-202_STALLED", 0.5, {"hr": 0, "spo2": 0}),  # Will exceed 0.1s timeout
        ("BED-203", 0.05, {"hr": 80, "spo2": 96}),
    ]
    results = asyncio.run(AsyncICUVitalHub.poll_all_beds(configs, timeout_sec=0.1))
    assert len(results) == 3
    by_bed = {r["bed_id"]: r for r in results}
    
    assert by_bed["BED-201"]["status"] == "OK"
    assert by_bed["BED-203"]["status"] == "OK"
    assert by_bed["BED-202_STALLED"]["status"] == "TIMEOUT"
    assert by_bed["BED-202_STALLED"]["vitals"] == {}
    print("Test 2 passed! Stalled bedside monitor gracefully timed out while healthy monitors succeeded.")


if __name__ == "__main__":
    test_concurrent_speedup_and_vitals()
    test_timeout_degradation()
    print("All Lab 1 Easy Tests Passed!")
