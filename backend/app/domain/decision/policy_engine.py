from app.config import settings
from typing import Tuple

class PolicyEngine:
    """
    100% Deterministic Decision Policy Engine.
    The LLM / AI Classifier is NEVER allowed to make the final operational decision.
    AI CONFIDENCE != OPERATIONAL SAFETY.
    
    Exact 8-Step Priority Order:
      STEP 1: System error? -> SYSTEM_ERROR
      STEP 2: Critical hazard detected? -> HIGH_RISK_ESCALATION
      STEP 3: Critical evidence conflict? -> HIGH_RISK_ESCALATION
      STEP 4: Operational risk above threshold? -> HIGH_RISK_ESCALATION
      STEP 5: Contents not observable or critical evidence missing? -> UNKNOWN
      STEP 6: High uncertainty? -> HIGH_RISK_ESCALATION
      STEP 7: Moderate uncertainty / non-critical missing / minor conflict? -> NEEDS_VERIFICATION
      STEP 8: Otherwise -> SAFE_TO_AUTOMATE
    """
    
    @staticmethod
    def decide(
        system_error: bool = False,
        critical_hazard_detected: bool = False,
        critical_conflict: bool = False,
        operational_risk_high: bool = False,
        not_observable_or_critical_missing: bool = False,
        high_uncertainty: bool = False,
        moderate_uncertainty_or_minor_conflict: bool = False
    ) -> Tuple[str, bool]:
        """
        Returns a tuple of (decision_state: str, automation_allowed: bool).
        Only SAFE_TO_AUTOMATE when no safety gate blocked automation may return automation_allowed = True.
        """
        # STEP 1: System error?
        if system_error:
            return ("SYSTEM_ERROR", False)

        # STEP 2: Critical hazard detected? (Syringe, Needle, Scalpel, Blade, Lancet, Unknown Sharp)
        if critical_hazard_detected:
            return ("HIGH_RISK_ESCALATION", False)

        # STEP 3: Critical evidence conflict? (Visual vs Barcode mismatch)
        if critical_conflict:
            return ("HIGH_RISK_ESCALATION", False)

        # STEP 4: High operational risk? (Abnormal mass surge / Z-score)
        if operational_risk_high:
            return ("HIGH_RISK_ESCALATION", False)

        # STEP 5: Content not observable or critical evidence missing? (Opaque bag)
        if not_observable_or_critical_missing:
            return ("UNKNOWN", False)

        # STEP 6: High model uncertainty entropy?
        if high_uncertainty:
            return ("HIGH_RISK_ESCALATION", False)

        # STEP 7: Moderate uncertainty / non-critical missing evidence / minor conflict?
        if moderate_uncertainty_or_minor_conflict:
            return ("NEEDS_VERIFICATION", False)

        # STEP 8: All safety gates pass cleanly
        return ("SAFE_TO_AUTOMATE", True)
