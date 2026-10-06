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


class TransfusionCompatibilityGuard:

    @classmethod
    def authorize_transfusion(cls, donor: BloodProfile, recipient: BloodProfile) -> TransfusionApproval:
        """
        Validates ABO and Rh compatibility, unit expiration, and returns approval.
        Raises ValueError on malformed inputs or expired units.
        Raises TransfusionIncompatibilityError on blood group or Rh mismatches.
        """
        # ====================================================================
        # WRITE CODE HERE
        # ====================================================================
        pass
        # ====================================================================
        # END OF YOUR CODE
