import pytest
from app.domain.decision.policy_engine import PolicyEngine

def test_policy_safe_automation():
    # Good evidence, low uncertainty, no conflict -> SAFE_TO_AUTOMATE
    state = PolicyEngine.decide(
        conflict_score=0.0,
        risk_score=0.1,
        observability="OBSERVABLE",
        critical_missing=False,
        uncertainty_score=0.15,
        has_noncritical_missing=False,
        has_conflict=False
    )
    assert state == "SAFE_TO_AUTOMATE"

def test_policy_opaque_container_unknown():
    # Opaque container -> UNKNOWN
    state = PolicyEngine.decide(
        conflict_score=0.0,
        risk_score=0.1,
        observability="NOT_OBSERVABLE",
        critical_missing=False,
        uncertainty_score=0.15,
        has_noncritical_missing=False,
        has_conflict=False
    )
    assert state == "UNKNOWN"

def test_policy_high_conflict_escalation():
    # Known high conflict / hazard takes priority over UNKNOWN
    state = PolicyEngine.decide(
        conflict_score=0.71,
        risk_score=0.8,
        observability="NOT_OBSERVABLE",
        critical_missing=False,
        uncertainty_score=0.64,
        has_noncritical_missing=False,
        has_conflict=True
    )
    assert state == "HIGH_RISK_ESCALATION"

def test_policy_moderate_uncertainty_verification():
    # Moderate uncertainty -> NEEDS_VERIFICATION
    state = PolicyEngine.decide(
        conflict_score=0.1,
        risk_score=0.2,
        observability="OBSERVABLE",
        critical_missing=False,
        uncertainty_score=0.45,
        has_noncritical_missing=False,
        has_conflict=False
    )
    assert state == "NEEDS_VERIFICATION"

def test_policy_system_error():
    # System error -> SYSTEM_ERROR
    state = PolicyEngine.decide(
        conflict_score=0.0,
        risk_score=0.0,
        observability="OBSERVABLE",
        critical_missing=False,
        uncertainty_score=0.0,
        has_noncritical_missing=False,
        has_conflict=False,
        system_error=True
    )
    assert state == "SYSTEM_ERROR"
