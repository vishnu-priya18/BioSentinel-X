import pytest
from app.domain.safety.hazard_gate import HazardGate, HazardAssessmentResult
from app.domain.decision.policy_engine import PolicyEngine

def test_hazard_gate_syringe():
    result = HazardGate.assess(metadata={"demo_hazard": "SYRINGE", "demo_hazard_confidence": 0.97})
    assert result.detected is True
    assert result.hazard_type == "SYRINGE"
    assert result.severity == "CRITICAL"
    assert result.critical_hazard is True
    assert result.automation_allowed is False

def test_hazard_gate_needle():
    result = HazardGate.assess(metadata={"item_description": "Hypodermic Needle"})
    assert result.detected is True
    assert result.hazard_type == "NEEDLE"
    assert result.severity == "CRITICAL"
    assert result.automation_allowed is False

def test_hazard_gate_scalpel():
    result = HazardGate.assess(metadata={"item_description": "Surgical Scalpel"})
    assert result.detected is True
    assert result.hazard_type == "SCALPEL"
    assert result.severity == "CRITICAL"
    assert result.automation_allowed is False

def test_hazard_gate_blade():
    result = HazardGate.assess(metadata={"item_description": "Disposable Razor Blade"})
    assert result.detected is True
    assert result.hazard_type == "BLADE"
    assert result.severity == "CRITICAL"
    assert result.automation_allowed is False

def test_hazard_gate_lancet():
    result = HazardGate.assess(metadata={"item_description": "Blood Lancet"})
    assert result.detected is True
    assert result.hazard_type == "LANCET"
    assert result.severity == "CRITICAL"
    assert result.automation_allowed is False

def test_hazard_gate_unknown_sharp():
    result = HazardGate.assess(metadata={"demo_hazard": "UNKNOWN_SHARP"})
    assert result.detected is True
    assert result.severity == "CRITICAL"
    assert result.automation_allowed is False

def test_policy_critical_hazard_blocks_automation():
    # Syringe with 97% confidence MUST result in HIGH_RISK_ESCALATION and automation_allowed == False
    decision_state, automation_allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=True,
        critical_conflict=False,
        operational_risk_high=False,
        not_observable_or_critical_missing=False,
        high_uncertainty=False,
        moderate_uncertainty_or_minor_conflict=False
    )
    assert decision_state == "HIGH_RISK_ESCALATION"
    assert automation_allowed is False

def test_policy_opaque_bag():
    decision_state, automation_allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        critical_conflict=False,
        operational_risk_high=False,
        not_observable_or_critical_missing=True,
        high_uncertainty=False,
        moderate_uncertainty_or_minor_conflict=False
    )
    assert decision_state == "UNKNOWN"
    assert automation_allowed is False

def test_policy_system_error():
    decision_state, automation_allowed = PolicyEngine.decide(
        system_error=True
    )
    assert decision_state == "SYSTEM_ERROR"
    assert automation_allowed is False

def test_policy_safe_non_hazard():
    decision_state, automation_allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=False,
        critical_conflict=False,
        operational_risk_high=False,
        not_observable_or_critical_missing=False,
        high_uncertainty=False,
        moderate_uncertainty_or_minor_conflict=False
    )
    assert decision_state == "SAFE_TO_AUTOMATE"
    assert automation_allowed is True

def test_critical_safety_invariant_property():
    """
    CRITICAL SAFETY INVARIANT TEST:
    FOR EVERY POSSIBLE EVENT:
    IF critical_hazard_detected == True
    THEN decision != SAFE_TO_AUTOMATE AND automation_allowed == False.
    """
    for err in [True, False]:
        for conflict in [True, False]:
            for risk in [True, False]:
                for unobs in [True, False]:
                    for h_unc in [True, False]:
                        for m_unc in [True, False]:
                            state, allowed = PolicyEngine.decide(
                                system_error=err,
                                critical_hazard_detected=True,
                                critical_conflict=conflict,
                                operational_risk_high=risk,
                                not_observable_or_critical_missing=unobs,
                                high_uncertainty=h_unc,
                                moderate_uncertainty_or_minor_conflict=m_unc
                            )
                            assert state != "SAFE_TO_AUTOMATE", f"Safety violation for combination: err={err}"
                            assert allowed is False, f"Automation allowed violation for combination: err={err}"
