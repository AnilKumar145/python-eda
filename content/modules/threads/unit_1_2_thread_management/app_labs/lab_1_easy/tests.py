"""
ICU Patient Telemetry Watchdog Supervisor - Tests
"""

import time
try:
    from solution.solution import ICUWatchdogSupervisor, TelemetryWorker
except (ImportError, ModuleNotFoundError):
    from starter_code import ICUWatchdogSupervisor, TelemetryWorker


def test_supervisor_discovery_and_shutdown():
    supervisor = ICUWatchdogSupervisor()
    
    # 1. Start workers for 3 patients
    w1 = supervisor.register_and_start("PAT-101")
    w2 = supervisor.register_and_start("PAT-102")
    w3 = supervisor.register_and_start("PAT-103")
    
    time.sleep(0.08)
    
    # 2. Check discovery
    active_patients = supervisor.get_active_telemetry_patients()
    assert active_patients == ["PAT-101", "PAT-102", "PAT-103"], f"Expected 3 patients, got {active_patients}"
    print(f"Test 1 passed! Active patients detected: {active_patients}")
    
    # 3. Test iterations incrementing
    assert w1.iterations >= 1
    assert w2.iterations >= 1
    assert w3.iterations >= 1
    print("Test 2 passed! Telemetry workers actively cycling.")
    
    # 4. Test cooperative shutdown
    clean_exit = supervisor.shutdown_all(timeout=1.0)
    assert clean_exit is True, "Shutdown should have completed cleanly within timeout"
    
    # 5. Verify no remaining active telemetry workers
    remaining = supervisor.get_active_telemetry_patients()
    assert remaining == [], f"Expected 0 active telemetry threads, found {remaining}"
    print("Test 3 passed! All workers joined and cleanly terminated.")


if __name__ == "__main__":
    test_supervisor_discovery_and_shutdown()
    print("All Unit 1.2 lab tests passed!")
