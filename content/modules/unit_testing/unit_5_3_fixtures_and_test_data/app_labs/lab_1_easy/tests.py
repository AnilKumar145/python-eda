import importlib.util
import pathlib
import json
import pytest

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_3_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

ChemistryAnalyzer = _sol.ChemistryAnalyzer
ReagentCartridge = _sol.ReagentCartridge
LabTestResult = _sol.LabTestResult



CARTRIDGE_DISPOSAL_BIN = []


@pytest.fixture
def fresh_cartridge():
    """Provides a fresh cartridge and ensures disposal on teardown."""
    cartridge = ReagentCartridge(lot_number="LOT-QC-99", remaining_tests=3, is_unlocked=True)
    yield cartridge

    # Teardown
    cartridge.is_unlocked = False
    CARTRIDGE_DISPOSAL_BIN.append(cartridge.lot_number)


@pytest.fixture
def calibrated_analyzer(fresh_cartridge):
    """Composed fixture: injects fresh_cartridge into analyzer."""
    return ChemistryAnalyzer(cartridge=fresh_cartridge)


@pytest.mark.parametrize("test_code, value, expected_flag", [
    ("GLUCOSE", 65.0, "LOW"),
    ("GLUCOSE", 85.0, "NORMAL"),
    ("GLUCOSE", 140.0, "HIGH"),
    ("POTASSIUM", 3.1, "LOW"),
    ("POTASSIUM", 4.2, "NORMAL"),
    ("POTASSIUM", 5.8, "HIGH"),
    ("SODIUM", 130.0, "LOW"),
    ("SODIUM", 140.0, "NORMAL"),
    ("SODIUM", 152.0, "HIGH"),
])
def test_reference_range_matrix(calibrated_analyzer, test_code, value, expected_flag):
    res = calibrated_analyzer.run_test(test_code, value)
    assert res.flag == expected_flag


def test_reagent_consumption_and_depletion(calibrated_analyzer, fresh_cartridge):
    # Runs 3 tests to consume all 3 remaining units
    calibrated_analyzer.run_test("GLUCOSE", 80.0)
    assert fresh_cartridge.remaining_tests == 2

    calibrated_analyzer.run_test("POTASSIUM", 4.0)
    assert fresh_cartridge.remaining_tests == 1

    calibrated_analyzer.run_test("SODIUM", 140.0)
    assert fresh_cartridge.remaining_tests == 0

    # 4th run should fail due to depletion
    with pytest.raises(RuntimeError, match="depleted"):
        calibrated_analyzer.run_test("GLUCOSE", 85.0)


def test_tmp_path_audit_log_export(calibrated_analyzer, tmp_path):
    result = calibrated_analyzer.run_test("GLUCOSE", 95.0)

    log_file = tmp_path / "qc_audit_log.json"
    log_data = {
        "test": result.test_code,
        "value": result.value,
        "flag": result.flag,
        "reagent_remaining": result.remaining_reagent
    }
    log_file.write_text(json.dumps(log_data), encoding="utf-8")

    assert log_file.exists()
    loaded = json.loads(log_file.read_text(encoding="utf-8"))
    assert loaded["flag"] == "NORMAL"
    assert loaded["reagent_remaining"] == 2
