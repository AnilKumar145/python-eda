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
        msg = f"EMERGENCY: Code Blue for Patient #{patient_id} in Room {room}"

        # Attempt 1: Primary SMS
        try:
            res = self.primary_sms.send_sms(to=self.on_call_phone, message=msg)
            if res:
                return DispatchResult(delivered=True, channel="PRIMARY_SMS", attempts=1)
        except Exception:
            pass

        # Attempt 2: Secondary Pager Fallback
        try:
            res = self.secondary_pager.send_page(pager_id=self.on_call_pager, text=msg)
            if res:
                return DispatchResult(delivered=True, channel="SECONDARY_PAGER", attempts=2)
        except Exception:
            pass

        return DispatchResult(delivered=False, channel="NONE", attempts=2)
