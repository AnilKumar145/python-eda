# Lab Tasks: Blood Bank Transfusion Compatibility Guard

## Task 1: Complete Transfusion Guard Algorithm
Implement `TransfusionCompatibilityGuard.authorize_transfusion(donor: BloodProfile, recipient: BloodProfile) -> TransfusionApproval`:
- Both donor and recipient have `abo` ("O", "A", "B", "AB") and `rh` (True for +, False for -).
- ABO matching rules:
  - O can donate RBCs to O, A, B, AB
  - A can donate to A, AB
  - B can donate to B, AB
  - AB can donate only to AB
- Rh matching rule:
  - Rh-negative donors can donate to Rh-negative and Rh-positive recipients.
  - Rh-positive donors can donate ONLY to Rh-positive recipients. If donor is Rh+ and recipient is Rh-, raise `TransfusionIncompatibilityError`.
- If donor is incompatible by ABO or Rh, raise `TransfusionIncompatibilityError` with detailed reasons.
- If donor unit is expired (`shelf_life_hours > 1008`, i.e. 42 days), raise `ValueError("Donor red blood cells expired")`.
- If compatible, return `TransfusionApproval(is_approved=True, risk_rating="STANDARD_CROSSMATCH")`.

## Task 2: Custom Exception Payload Verification
Write unit tests in `tests.py`:
- `test_incompatible_rh_factor_raises_custom_exception()`: Tests that A+ donor to A- recipient raises `TransfusionIncompatibilityError`, and asserts that `exc_info.value.donor.rh` is True and `recipient.rh` is False.
- `test_expired_unit_raises_value_error_with_regex()`: Tests that an expired blood unit raises `ValueError` matching regex `"expired"`.

## Task 3: Boundary & Edge Case Matrices
Author parameterized tests covering:
- Universal donor (O-) compatible with all 8 ABO/Rh combinations.
- Universal recipient (AB+) accepting blood from all 8 ABO/Rh combinations.
- Malformed ABO strings (e.g., "", "C", None) raising `ValueError`.
