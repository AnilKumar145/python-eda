"""
Unit 5.4 Exercises: Mocking and Isolation (Starter Code)
Implement each function to satisfy the test assertions.
"""

from typing import Dict, Any
from unittest.mock import Mock, patch
import pytest


def dispatch_emergency_pager(pager_client: Any, doctor_id: str, message: str, max_retries: int = 2) -> bool:
    """
    Exercise 1: Emergency Pager Dispatcher with Retry Logic
    Attempt to send a page using pager_client.send_page(doctor_id=doctor_id, message=message).
    If it raises TimeoutError or ConnectionError:
      - Retry up to max_retries additional times.
      - If an attempt succeeds, return True immediately.
    If all attempts fail, return False.
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


def fetch_remote_vitals(http_client: Any, patient_id: int) -> Dict[str, Any]:
    """
    Exercise 2: Remote Vitals Ingestion Client
    Make a GET request via http_client.get(url=f"/patients/{patient_id}/vitals").
    - If status_code == 200: return response.json()
    - If status_code == 404: raise ValueError(f"Patient {patient_id} not found")
    - If status_code >= 500: raise RuntimeError(f"Server error: {response.status_code}")
    """
    # ====================================================================
    # WRITE CODE HERE
    # ====================================================================
    pass
    # ====================================================================
    # END OF YOUR CODE


# ====================================================================
# Verification Tests
# ====================================================================

def test_pager_immediate_success():
    mock_client = Mock()
    mock_client.send_page.return_value = {"status": "QUEUED"}

    success = dispatch_emergency_pager(mock_client, "DOC-101", "Code Blue OR-1")
    assert success is True
    mock_client.send_page.assert_called_once_with(doctor_id="DOC-101", message="Code Blue OR-1")


def test_pager_retries_on_network_timeout():
    mock_client = Mock()
    # Fails twice with TimeoutError, then succeeds on 3rd attempt
    mock_client.send_page.side_effect = [
        TimeoutError("Net timeout 1"),
        ConnectionError("Dropped frame"),
        {"status": "DELIVERED"}
    ]

    success = dispatch_emergency_pager(mock_client, "DOC-102", "Trauma bay alert", max_retries=2)
    assert success is True
    assert mock_client.send_page.call_count == 3


def test_pager_exhausts_retries_and_returns_false():
    mock_client = Mock()
    mock_client.send_page.side_effect = TimeoutError("Total network blackout")

    success = dispatch_emergency_pager(mock_client, "DOC-103", "Urgent consult", max_retries=1)
    assert success is False
    assert mock_client.send_page.call_count == 2  # Initial try + 1 retry


def test_fetch_remote_vitals_200():
    mock_http = Mock()
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"heart_rate": 78, "spo2": 99}
    mock_http.get.return_value = mock_resp

    data = fetch_remote_vitals(mock_http, 501)
    assert data["heart_rate"] == 78
    mock_http.get.assert_called_once_with(url="/patients/501/vitals")


def test_fetch_remote_vitals_404_raises():
    mock_http = Mock()
    mock_resp = Mock()
    mock_resp.status_code = 404
    mock_http.get.return_value = mock_resp

    with pytest.raises(ValueError, match="Patient 999 not found"):
        fetch_remote_vitals(mock_http, 999)
