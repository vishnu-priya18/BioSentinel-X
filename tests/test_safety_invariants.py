import pytest
from app.domain.decision.policy_engine import PolicyEngine

def test_critical_hazard_safety_invariant():
    """
    SAFETY INVARIANT TEST (Section 34):
    assert not (critical_hazard_detected and decision == "SAFE_TO_AUTOMATE")
    if critical_hazard_detected: assert automation_allowed == False
    """
    for err in [True, False]:
        for conflict in [True, False]:
            for risk in [True, False]:
                for obj_missing in [True, False]:
                    for unobs in [True, False]:
                        for h_unc in [True, False]:
                            for m_unc in [True, False]:
                                state, allowed = PolicyEngine.decide(
                                    system_error=err,
                                    critical_hazard_detected=True,
                                    critical_conflict=conflict,
                                    operational_risk_high=risk,
                                    object_not_detected=obj_missing,
                                    not_observable=unobs,
                                    high_uncertainty=h_unc,
                                    moderate_uncertainty=m_unc
                                )
                                # SAFETY INVARIANT CHECK 1:
                                assert not (True and state == "SAFE_TO_AUTOMATE"), "CRITICAL SAFETY INVARIANT BROKEN: Critical hazard yielded SAFE_TO_AUTOMATE!"
                                # SAFETY INVARIANT CHECK 2:
                                assert allowed is False, "CRITICAL SAFETY INVARIANT BROKEN: Critical hazard granted automation permission!"

def test_opaque_container_safety_invariant():
    """
    Opaque container MUST yield UNKNOWN and automation_allowed == False.
    """
    state, allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        not_observable=True
    )
    assert state == "UNKNOWN"
    assert allowed is False
