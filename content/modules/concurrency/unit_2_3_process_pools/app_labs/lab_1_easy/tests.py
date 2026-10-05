"""
Parallel ECG Arrhythmia Signal Analyzer - Tests
"""

try:
    from solution.solution import ECGSignalProcessor
except (ImportError, ModuleNotFoundError):
    from starter_code import ECGSignalProcessor


def test_parallel_lead_processing():
    processor = ECGSignalProcessor(max_workers=2)
    batch = [
        ("LEAD-V1", [1.0, 2.5, 5.0, 1.5, 0.0]), # peak 5.0, mean 2.0
        ("LEAD-V2", [0.5, 1.0, 1.5]),           # peak 1.5, mean 1.0
        ("LEAD-V3", []),                        # empty
    ]
    
    results = processor.analyze_leads(batch)
    assert len(results) == 3, f"Expected 3 results, got {len(results)}"
    
    # Verify Lead V1
    v1 = results[0]
    assert v1["lead_id"] == "LEAD-V1"
    assert v1["status"] == "SUCCESS"
    assert v1["peak"] == 5.0
    assert v1["mean"] == 2.0
    
    # Verify Lead V2
    v2 = results[1]
    assert v2["peak"] == 1.5
    assert v2["mean"] == 1.0
    
    # Verify Empty Lead V3
    v3 = results[2]
    assert v3["status"] == "EMPTY"
    assert v3["peak"] == 0.0
    
    print("Test 1 passed! Parallel ECG signal processing verified.")


if __name__ == "__main__":
    test_parallel_lead_processing()
    print("All Unit 2.3 lab tests passed!")
