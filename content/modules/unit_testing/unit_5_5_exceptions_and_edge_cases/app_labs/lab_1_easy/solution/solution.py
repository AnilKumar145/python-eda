from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BloodProfile:
    abo: str  # "O", "A", "B", "AB"
    rh_positive: bool  # True for +, False for -
    shelf_life_hours: int = 24


class TransfusionIncompatibilityError(Exception):
    def __init__(self, donor: BloodProfile, recipient: BloodProfile, detail: str):
        super().__init__(detail)
        self.donor = donor
        self.recipient = recipient
        self.detail = detail


@dataclass(frozen=True)
class TransfusionApproval:
    is_approved: bool
    risk_rating: str


VALID_ABO = {"O", "A", "B", "AB"}

ABO_COMPATIBILITY = {
    "O": {"O", "A", "B", "AB"},
    "A": {"A", "AB"},
    "B": {"B", "AB"},
    "AB": {"AB"}
}


class TransfusionCompatibilityGuard:

    @classmethod
    def authorize_transfusion(cls, donor: BloodProfile, recipient: BloodProfile) -> TransfusionApproval:
        if not donor or not recipient:
            raise ValueError("Donor and recipient profiles must be non-null")

        d_abo = donor.abo.strip().upper() if donor.abo else ""
        r_abo = recipient.abo.strip().upper() if recipient.abo else ""

        if d_abo not in VALID_ABO:
            raise ValueError(f"Invalid donor ABO type: '{donor.abo}'")
        if r_abo not in VALID_ABO:
            raise ValueError(f"Invalid recipient ABO type: '{recipient.abo}'")

        if donor.shelf_life_hours > 1008:
            raise ValueError(f"Donor red blood cells expired: {donor.shelf_life_hours} hours old (max 1008)")

        # 1. ABO Compatibility Check
        if r_abo not in ABO_COMPATIBILITY[d_abo]:
            raise TransfusionIncompatibilityError(
                donor=donor,
                recipient=recipient,
                detail=f"Fatal ABO mismatch: Donor {d_abo} cannot donate to Recipient {r_abo}"
            )

        # 2. Rh Compatibility Check: Rh+ cannot donate to Rh-
        if donor.rh_positive and not recipient.rh_positive:
            raise TransfusionIncompatibilityError(
                donor=donor,
                recipient=recipient,
                detail="Fatal Rh mismatch: Rh-positive donor cannot donate to Rh-negative recipient"
            )

        return TransfusionApproval(is_approved=True, risk_rating="STANDARD_CROSSMATCH")
