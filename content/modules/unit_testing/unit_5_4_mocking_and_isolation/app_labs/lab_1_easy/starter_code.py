from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DispatchResult:
    delivered: bool
    channel: str
    attempts: int


class EmergencyAlertDispatcher:

    def __init__(self, primary_sms_client: Any, secondary_pager_client: Any, on_call_phone: str, on_call_pager: str):
        self.primary_sms = primary_sms_client
        self.secondary_pager = secondary_pager_client
        self.on_call_phone = on_call_phone
        self.on_call_pager = on_call_pager

    def dispatch_code_blue(self, patient_id: int, room: str) -> DispatchResult:
        """
        Dispatches Code Blue notification with automatic fallback from SMS to Pager.
        """
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
