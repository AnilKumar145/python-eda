"""
Multi-Core Genomic Chromosome Scanner - Tests
"""

try:
    from solution.solution import GenomicScannerEngine
except (ImportError, ModuleNotFoundError):
    from starter_code import GenomicScannerEngine


def test_parallel_chromosome_scanning():
    engine = GenomicScannerEngine()
    
    # Construct 3 mock chromosome sequences with known marker frequencies
    marker = "ATCG"
    data = {
        "Chr-1": "ATCG" * 50 + "AAAA",    # 50 matches
        "Chr-2": "CCGG" + "ATCG" * 30,     # 30 matches
        "Chr-3": "TTTT" * 20,              # 0 matches
    }
    
    results = engine.scan_all(data, marker)
    assert len(results) == 3, f"Expected 3 chromosomes, got {len(results)}"
    assert results["Chr-1"] == 50
    assert results["Chr-2"] == 30
    assert results["Chr-3"] == 0
    print(f"Test 1 passed! All 3 chromosomes scanned accurately in parallel: {results}")


def test_empty_dataset():
    engine = GenomicScannerEngine()
    results = engine.scan_all({}, "ATCG")
    assert results == {}
    print("Test 2 passed! Empty chromosome dict handled cleanly.")


if __name__ == "__main__":
    test_parallel_chromosome_scanning()
    test_empty_dataset()
    print("All Unit 2.2 lab tests passed!")
