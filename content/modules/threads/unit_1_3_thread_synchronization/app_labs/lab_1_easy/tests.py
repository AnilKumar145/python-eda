"""
Hospital Pharmacy Inventory Dispenser - Tests
"""

import threading
try:
    from solution.solution import PharmacyDispenserEngine
except (ImportError, ModuleNotFoundError):
    from starter_code import PharmacyDispenserEngine


def test_concurrent_dispensation_exact_stock():
    engine = PharmacyDispenserEngine({"Morphine-10mg": 20})
    successes = []
    rejections = []
    
    def worker(doc_id):
        ok = engine.dispense("Morphine-10mg", 1, doc_id)
        if ok:
            successes.append(doc_id)
        else:
            rejections.append(doc_id)
            
    threads = [threading.Thread(target=worker, args=(f"Dr-{i}",)) for i in range(20)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert len(successes) == 20, f"Expected 20 successes, got {len(successes)}"
    assert len(rejections) == 0
    assert engine.get_stock("Morphine-10mg") == 0, f"Expected 0 stock, got {engine.get_stock('Morphine-10mg')}"
    print("Test 1 passed! Exact stock concurrent dispensation verified.")


def test_concurrent_dispensation_over_subscription():
    # 10 units available, 10 doctors request 2 units each (20 units requested total)
    engine = PharmacyDispenserEngine({"Epinephrine-1mg": 10})
    successes = []
    rejections = []
    
    def worker(doc_id):
        ok = engine.dispense("Epinephrine-1mg", 2, doc_id)
        if ok:
            successes.append(doc_id)
        else:
            rejections.append(doc_id)
            
    threads = [threading.Thread(target=worker, args=(f"SurgicalTeam-{i}",)) for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert len(successes) == 5, f"Expected exactly 5 successes, got {len(successes)}"
    assert len(rejections) == 5, f"Expected exactly 5 rejections, got {len(rejections)}"
    assert engine.get_stock("Epinephrine-1mg") == 0, f"Stock went negative! Got {engine.get_stock('Epinephrine-1mg')}"
    assert len(engine.audit_log) == 10, "All 10 attempts must be recorded in audit log"
    print("Test 2 passed! Over-subscription prevented and stock never went negative.")


if __name__ == "__main__":
    test_concurrent_dispensation_exact_stock()
    test_concurrent_dispensation_over_subscription()
    print("All Unit 1.3 lab tests passed!")
