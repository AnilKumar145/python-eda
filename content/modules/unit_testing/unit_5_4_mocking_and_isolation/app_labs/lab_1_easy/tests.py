import importlib.util
import pathlib
from unittest.mock import Mock
import pytest

_sol_path = pathlib.Path(__file__).parent / "solution" / "solution.py"
_spec = importlib.util.spec_from_file_location("unit_5_4_lab_solution", _sol_path)
_sol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sol)

EmergencyAlertDispatcher = _sol.EmergencyAlertDispatcher
DispatchResult = _sol.DispatchResult



def test_primary_sms_success_never_calls_secondary_pager():
    # Arrange
    mock_sms = Mock()
    mock_sms.send_sms.return_value = {"id": "SMS-001", "status": "SENT"}

    mock_pager = Mock()

    dispatcher = EmergencyAlertDispatcher(
        primary_sms_client=mock_sms,
        secondary_pager_client=mock_pager,
        on_call_phone="+15550100",
        on_call_pager="PAGER-44"
    )

    # Act
    result = dispatcher.dispatch_code_blue(patient_id=101, room="ICU-4")

    # Assert
    assert result.delivered is True
    assert result.channel == "PRIMARY_SMS"
    assert result.attempts == 1
    mock_sms.send_sms.assert_called_once()
    mock_pager.send_page.assert_not_called()


def test_primary_sms_failure_triggers_secondary_pager_fallback():
    # Arrange
    mock_sms = Mock()
    mock_sms.send_sms.side_effect = TimeoutError("Telco gateway dropped connection")

    mock_pager = Mock()
    mock_pager.send_page.return_value = True

    dispatcher = EmergencyAlertDispatcher(
        primary_sms_client=mock_sms,
        secondary_pager_client=mock_pager,
        on_call_phone="+15550100",
        on_call_pager="PAGER-44"
    )

    # Act
    result = dispatcher.dispatch_code_blue(patient_id=202, room="OR-2")

    # Assert
    assert result.delivered is True
    assert result.channel == "SECONDARY_PAGER"
    assert result.attempts == 2
    mock_sms.send_sms.assert_called_once()
    mock_pager.send_page.assert_called_once()
    assert "Room OR-2" in mock_pager.send_page.call_args.kwargs["text"]


def test_both_channels_failing_reports_failure():
    # Arrange
    mock_sms = Mock()
    mock_sms.send_sms.side_effect = ConnectionError("SMS carrier down")

    mock_pager = Mock()
    mock_pager.send_page.side_effect = RuntimeError("Radio tower unreachable")

    dispatcher = EmergencyAlertDispatcher(
        primary_sms_client=mock_sms,
        secondary_pager_client=mock_pager,
        on_call_phone="+15550100",
        on_call_pager="PAGER-44"
    )

    # Act
    result = dispatcher.dispatch_code_blue(patient_id=303, room="PACU-1")

    # Assert
    assert result.delivered is False
    assert result.channel == "NONE"
    assert result.attempts == 2
    assert mock_sms.send_sms.call_count == 1
    assert mock_pager.send_page.call_count == 1
