import importlib.util
import pathlib
import pytest

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_5_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

TransfusionCompatibilityGuard = _sol.TransfusionCompatibilityGuard
BloodProfile = _sol.BloodProfile
TransfusionApproval = _sol.TransfusionApproval
TransfusionIncompatibilityError = _sol.TransfusionIncompatibilityError



def test_o_negative_universal_donor_success():
    donor = BloodProfile(abo="O", rh_positive=False)
    recipient = BloodProfile(abo="AB", rh_positive=True)

    approval = TransfusionCompatibilityGuard.authorize_transfusion(donor, recipient)
    assert approval.is_approved is True
    assert approval.risk_rating == "STANDARD_CROSSMATCH"


def test_rh_incompatibility_raises_custom_exception():
    # A+ cannot donate to A-
    donor = BloodProfile(abo="A", rh_positive=True)
    recipient = BloodProfile(abo="A", rh_positive=False)

    with pytest.raises(TransfusionIncompatibilityError) as exc_info:
        TransfusionCompatibilityGuard.authorize_transfusion(donor, recipient)

    err = exc_info.value
    assert err.donor.rh_positive is True
    assert err.recipient.rh_positive is False
    assert "Fatal Rh mismatch" in err.detail


def test_abo_mismatch_raises_custom_exception():
    # B cannot donate to A
    donor = BloodProfile(abo="B", rh_positive=False)
    recipient = BloodProfile(abo="A", rh_positive=False)

    with pytest.raises(TransfusionIncompatibilityError) as exc_info:
        TransfusionCompatibilityGuard.authorize_transfusion(donor, recipient)

    err = exc_info.value
    assert "Fatal ABO mismatch" in err.detail
    assert "Donor B cannot donate to Recipient A" in err.detail


def test_expired_unit_raises_value_error_with_regex():
    # 43 days = 1032 hours (exceeds 1008 max)
    expired_donor = BloodProfile(abo="O", rh_positive=False, shelf_life_hours=1032)
    recipient = BloodProfile(abo="O", rh_positive=False)

    with pytest.raises(ValueError, match=r"expired.*1032 hours"):
        TransfusionCompatibilityGuard.authorize_transfusion(expired_donor, recipient)


@pytest.mark.parametrize("invalid_abo", ["", "   ", "X", "C", "Rh+"])
def test_malformed_abo_inputs_raise_value_error(invalid_abo):
    donor = BloodProfile(abo=invalid_abo, rh_positive=False)
    recipient = BloodProfile(abo="O", rh_positive=False)

    with pytest.raises(ValueError, match="Invalid donor ABO"):
        TransfusionCompatibilityGuard.authorize_transfusion(donor, recipient)
