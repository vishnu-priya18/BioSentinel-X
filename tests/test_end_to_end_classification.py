import pytest
from app.domain.intelligence.classifier_adapter import DemoWasteClassifier
from app.domain.safety.hazard_gate import HazardGate
from app.domain.decision.policy_engine import PolicyEngine

def test_end_to_end_syringe_classification():
    # 1. AI Classifier prediction
    pred = DemoWasteClassifier().predict(metadata={"item_description": "Injection Syringe"})
    assert pred.object_class == "SYRINGE"
    assert pred.waste_type == "SHARPS"
    assert pred.bag_category == "WHITE"
    assert pred.bag_category != "YELLOW"

    # 2. Hazard Gate check
    hazard = HazardGate.assess(metadata={"item_description": "Injection Syringe"})
    assert hazard.detected is True
    assert hazard.critical_hazard is True
    assert hazard.automation_allowed is False

    # 3. Policy Engine decision
    state, allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=hazard.critical_hazard
    )
    assert state == "HIGH_RISK_ESCALATION"
    assert allowed is False
