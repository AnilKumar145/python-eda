"""
Hospital ER Patient Triage Dispatcher - Tests
"""

try:
    from solution.solution import ERTriageDispatcher, TriageCase
except (ImportError, ModuleNotFoundError):
    from starter_code import ERTriageDispatcher, TriageCase


def test_priority_dispatching_single_doctor():
    dispatcher = ERTriageDispatcher()
    
    # Enqueue patients in reverse order of acuity
    dispatcher.admit_patient(TriageCase(4, "P-401", "Bob", "Minor cough"))
    dispatcher.admit_patient(TriageCase(2, "P-201", "Carol", "Chest discomfort"))
    dispatcher.admit_patient(TriageCase(1, "P-101", "Alice", "Cardiac arrest")) # Highest priority
    dispatcher.admit_patient(TriageCase(3, "P-301", "Dave", "Sprained wrist"))
    
    # Start single doctor to observe strict order
    dispatcher.start_doctors(1)
    dispatcher.drain_and_shutdown()
    
    # Verify processing order
    treated_patients = [record[2] for record in dispatcher.treated_records]
    assert treated_patients == ["P-101", "P-201", "P-301", "P-401"], f"Order corrupted! Got {treated_patients}"
    print("Test 1 passed! Priority dispatch order verified: P-101 (Level 1) treated first.")


def test_concurrent_multi_doctor_pool():
    dispatcher = ERTriageDispatcher()
    
    # Enqueue 12 patient cases across varying acuity levels
    for i in range(12):
        level = (i % 4) + 1
        dispatcher.admit_patient(TriageCase(level, f"PAT-{i}", f"Name-{i}", f"Condition-{i}"))
        
    dispatcher.start_doctors(3)
    dispatcher.drain_and_shutdown()
    
    assert len(dispatcher.treated_records) == 12, f"Expected 12 treated, got {len(dispatcher.treated_records)}"
    
    # Verify no doctors remain alive
    for doc in dispatcher.doctors:
        assert doc.is_alive() is False, "Doctor thread still alive after shutdown"
        
    print("Test 2 passed! Multi-doctor pool processed all 12 cases and shut down cleanly.")


if __name__ == "__main__":
    test_priority_dispatching_single_doctor()
    test_concurrent_multi_doctor_pool()
    print("All Unit 1.4 lab tests passed!")
