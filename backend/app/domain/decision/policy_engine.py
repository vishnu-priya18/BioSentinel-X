from app.config import settings

class PolicyEngine:
    """
    100% Deterministic Decision Policy Engine.
    The LLM / AI Classifier is NEVER allowed to make the final operational decision.
    Decision priority logic:
      1. Known High Risk / Conflict takes priority over UNKNOWN
      2. NOT_OBSERVABLE / Critical Missing -> UNKNOWN
      3. High Uncertainty -> HIGH_RISK_ESCALATION
      4. Moderate Uncertainty / Non-critical missing -> NEEDS_VERIFICATION
      5. Low Uncertainty + Good Evidence -> SAFE_TO_AUTOMATE
    """
    @staticmethod
    def decide(
        conflict_score: float,
        risk_score: float,
        observability: str,
        critical_missing: bool,
        uncertainty_score: float,
        has_noncritical_missing: bool,
        has_conflict: bool,
        system_error: bool = False
    ) -> str:
        if system_error:
            return "SYSTEM_ERROR"

        # 1. Known high-risk evidence / conflict takes precedence over UNKNOWN
        if conflict_score >= settings.HIGH_CONFLICT_THRESHOLD:
            return "HIGH_RISK_ESCALATION"

        if risk_score >= settings.HIGH_RISK_THRESHOLD:
            return "HIGH_RISK_ESCALATION"

        # 2. Cannot safely observe contents
        if observability == "NOT_OBSERVABLE":
            return "UNKNOWN"

        if critical_missing:
            return "UNKNOWN"

        # 3. High model uncertainty
        if uncertainty_score >= settings.HIGH_UNCERTAINTY_THRESHOLD:
            return "HIGH_RISK_ESCALATION"

        # 4. Moderate uncertainty / non-critical missing data / minor conflict
        if (
            uncertainty_score >= settings.VERIFICATION_THRESHOLD
            or has_noncritical_missing
            or has_conflict
        ):
            return "NEEDS_VERIFICATION"

        # 5. All safety checks pass
        return "SAFE_TO_AUTOMATE"
