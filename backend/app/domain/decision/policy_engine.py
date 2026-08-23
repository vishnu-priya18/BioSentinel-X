from typing import Tuple, Dict, Any

class PolicyEngine:
    """
    Deterministic Safety Policy Engine for Biomedical Waste Automation.
    Enforces the exact 12-step priority safety rule set.
    High AI prediction confidence NEVER overrides a critical safety hazard.
    An LLM or ML classifier is NEVER allowed to override this policy.
    """

    @staticmethod
    def decide(
        system_error: bool = False,
        critical_hazard_detected: bool = False,
        critical_conflict: bool = False,
        operational_risk_high: bool = False,
        object_not_detected: bool = False,
        not_observable: bool = False,
        high_uncertainty: bool = False,
        moderate_uncertainty: bool = False,
        not_observable_or_critical_missing: bool = False,
        moderate_uncertainty_or_minor_conflict: bool = False
    ) -> Tuple[str, bool]:
        """
        Returns Tuple[decision_state, automation_allowed].
        """
        # Step 1: System error check
        if system_error:
            return ("SYSTEM_ERROR", False)

        # Step 2: Critical sharp hazard check (SYRINGE, NEEDLE, SCALPEL, BLADE, LANCET)
        if critical_hazard_detected:
            return ("HIGH_RISK_ESCALATION", False)

        # Step 3: Critical evidence conflict check (e.g. Barcode vs Image Mismatch)
        if critical_conflict:
            return ("HIGH_RISK_ESCALATION", False)

        # Step 4: High operational risk / weight anomaly
        if operational_risk_high:
            return ("HIGH_RISK_ESCALATION", False)

        # Step 5: Object detection failure (Low confidence / No object detected)
        if object_not_detected:
            return ("UNKNOWN", False)

        # Step 6: Observability check (Opaque container / unobservable contents)
        if not_observable or not_observable_or_critical_missing:
            return ("UNKNOWN", False)

        # Step 7: High uncertainty (Softmax Entropy H > threshold)
        if high_uncertainty:
            return ("HIGH_RISK_ESCALATION", False)

        # Step 8: Moderate uncertainty or minor evidence gap
        if moderate_uncertainty or moderate_uncertainty_or_minor_conflict:
            return ("NEEDS_VERIFICATION", False)

        # Step 9: All safety bounds satisfied -> SAFE_TO_AUTOMATE
        return ("SAFE_TO_AUTOMATE", True)
