import pytest
from app.domain.decision.policy_engine import PolicyEngine

def test_policy_safe_automation():
    state, allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        critical_conflict=False,
        operational_risk_high=False,
        not_observable_or_critical_missing=False,
        high_uncertainty=False,
        moderate_uncertainty_or_minor_conflict=False
    )
    assert state == "SAFE_TO_AUTOMATE"
    assert allowed is True

def test_policy_opaque_container_unknown():
    state, allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        critical_conflict=False,
        operational_risk_high=False,
        not_observable_or_critical_missing=True,
        high_uncertainty=False,
        moderate_uncertainty_or_minor_conflict=False
    )
    assert state == "UNKNOWN"
    assert allowed is False

def test_policy_high_conflict_escalation():
    state, allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        critical_conflict=True,
        operational_risk_high=True,
        not_observable_or_critical_missing=True,
        high_uncertainty=True,
        moderate_uncertainty_or_minor_conflict=False
    )
    assert state == "HIGH_RISK_ESCALATION"
    assert allowed is False

def test_policy_moderate_uncertainty_verification():
    state, allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        critical_conflict=False,
        operational_risk_high=False,
        not_observable_or_critical_missing=False,
        high_uncertainty=False,
        moderate_uncertainty_or_minor_conflict=True
    )
    assert state == "NEEDS_VERIFICATION"
    assert allowed is False

def test_policy_system_error():
    state, allowed = PolicyEngine.decide(
        system_error=True
    )
    assert state == "SYSTEM_ERROR"
    assert allowed is False
