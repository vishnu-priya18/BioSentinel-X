import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models.domain_models import WasteEvent, AiPrediction, UncertaintyAssessment, Decision, Department, WasteCategory, AuditEvent, AuditHashChain
from app.schemas.domain_schemas import WasteEventCreate, DecisionTraceSchema
from app.domain.evidence.quality_evaluator import QualityEvaluator
from app.domain.evidence.observability_engine import ObservabilityEngine
from app.domain.evidence.evidence_fusion_engine import EvidenceFusionEngine
from app.domain.intelligence.classifier_adapter import DemoWasteClassifier
from app.domain.intelligence.uncertainty_engine import UncertaintyEngine
from app.domain.intelligence.anomaly_engine import AnomalyEngine
from app.domain.safety.hazard_gate import HazardGate
from app.domain.decision.policy_engine import PolicyEngine
from app.domain.decision.reasoning_panel_engine import ReasoningPanelEngine
from app.domain.decision.counterfactual_engine import CounterfactualEngine
from app.domain.decision.decision_trace import DecisionTrace
from app.domain.audit.audit_chain_engine import AuditChainEngine

router = APIRouter(prefix="/waste-events", tags=["Waste Events"])

@router.get("")
def list_events(db: Session = Depends(get_db)):
    events = db.query(WasteEvent).order_by(WasteEvent.created_at.desc()).all()
    results = []
    for e in events:
        dec = db.query(Decision).filter(Decision.event_id == e.id).first()
        dept = db.query(Department).filter(Department.id == e.dept_id).first()
        cat = db.query(WasteCategory).filter(WasteCategory.id == e.declared_category_id).first()
        results.append({
            "id": e.id,
            "event_code": e.event_code,
            "dept_name": dept.name if dept else "Unknown Dept",
            "declared_category": cat.code if cat else "Red",
            "weight_kg": e.weight_kg,
            "opacity_state": e.opacity_state,
            "decision_state": dec.decision_state if dec else "UNKNOWN",
            "created_at": e.created_at.isoformat()
        })
    return results

@router.get("/{event_code}/trace")
def get_decision_trace(event_code: str, db: Session = Depends(get_db)):
    ev = db.query(WasteEvent).filter(WasteEvent.event_code == event_code).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Waste event not found")
        
    dec = db.query(Decision).filter(Decision.event_id == ev.id).first()
    if not dec or not dec.trace_json:
        raise HTTPException(status_code=404, detail="Decision trace not found")
        
    return dec.trace_json

@router.get("/{event_code}/graph")
def get_evidence_graph(event_code: str, db: Session = Depends(get_db)):
    ev = db.query(WasteEvent).filter(WasteEvent.event_code == event_code).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Waste event not found")
        
    dec = db.query(Decision).filter(Decision.event_id == ev.id).first()
    trace = dec.trace_json if dec else {}
    
    nodes = [
        {"id": "event", "type": "event", "label": f"Waste Event: {event_code}", "status": "INFO"},
        {"id": "hazard", "type": "hazard", "label": f"Hazard: {trace.get('hazard', {}).get('hazard_type', 'NONE')} ({trace.get('hazard', {}).get('severity', 'LOW')})", "status": "FAIL" if trace.get('hazard', {}).get('critical') else "SUPPORTING"},
        {"id": "barcode", "type": "evidence", "label": f"Barcode: CPCB-{event_code}", "status": "SUPPORTING" if not trace.get("conflicts", {}).get("detected") else "CONFLICTING"},
        {"id": "dept", "type": "evidence", "label": "Department Baseline: 2.1kg", "status": "SUPPORTING"},
        {"id": "image", "type": "evidence", "label": f"Image Quality: {trace.get('evidence', {}).get('image_quality', 0.85):.2f}", "status": "SUPPORTING" if trace.get("evidence", {}).get("image_quality", 0.85) >= 0.4 else "FAIL"},
        {"id": "weight", "type": "evidence", "label": f"Weight: {ev.weight_kg}kg", "status": "SUPPORTING" if trace.get("conflicts", {}).get("conflict_codes") == [] else "CONFLICTING"},
        {"id": "classifier", "type": "ai", "label": f"AI Prediction: {trace.get('prediction', {}).get('category', 'Red')} ({trace.get('prediction', {}).get('confidence', 0.9)*100:.0f}%)", "status": "INFO"},
        {"id": "uncertainty", "type": "uncertainty", "label": f"Softmax Entropy H={trace.get('uncertainty', {}).get('entropy', 0.18):.2f}", "status": "WARNING" if trace.get("uncertainty", {}).get("entropy", 0.18) >= 0.42 else "SUPPORTING"},
        {"id": "decision", "type": "decision", "label": f"Decision: {dec.decision_state if dec else 'UNKNOWN'}", "status": dec.decision_state if dec else "UNKNOWN"}
    ]
    
    edges = [
        {"source": "event", "target": "hazard"},
        {"source": "event", "target": "barcode"},
        {"source": "event", "target": "dept"},
        {"source": "event", "target": "image"},
        {"source": "event", "target": "weight"},
        {"source": "image", "target": "classifier"},
        {"source": "classifier", "target": "uncertainty"},
        {"source": "hazard", "target": "decision"},
        {"source": "barcode", "target": "uncertainty"},
        {"source": "weight", "target": "uncertainty"},
        {"source": "uncertainty", "target": "decision"}
    ]
    
    return {"nodes": nodes, "edges": edges}

@router.post("/analyze")
def analyze_waste_event(payload: WasteEventCreate, db: Session = Depends(get_db)):
    event_code = payload.event_code or f"EVT-{int(datetime.datetime.utcnow().timestamp())}"
    
    # 1. Quality & Observability Evaluation
    quality_score = QualityEvaluator.evaluate(payload.image_base64)
    observability = ObservabilityEngine.evaluate(payload.opacity_state, payload.container_type)
    
    # 2. AI Classification Model Prediction
    classifier = DemoWasteClassifier()
    pred_res = classifier.predict(payload.image_base64, {
        "declared_category": payload.declared_category_code,
        "scenario_code": event_code,
        "item_description": payload.user_notes
    })
    
    # 3. Hazard Gate Assessment (Independent Safety Gate)
    hazard_res = HazardGate.assess(payload.image_base64, {
        "scenario_code": event_code,
        "declared_category": payload.declared_category_code,
        "item_description": payload.user_notes
    })
    
    # 4. Department Baseline Lookup
    dept = db.query(Department).filter(Department.id == payload.dept_id).first()
    baseline_weight = dept.baseline_daily_waste_kg if dept else 2.1
    
    # 5. Evidence Fusion
    fusion_res = EvidenceFusionEngine.fuse(
        declared_category=payload.declared_category_code,
        predicted_category=pred_res.predicted_category,
        barcode_scanned=payload.barcode_scanned or f"CPCB-IND-{event_code}",
        weight_kg=payload.weight_kg,
        baseline_weight_kg=baseline_weight,
        observability=observability,
        quality_score=quality_score,
        hazard_result=hazard_res
    )
    
    # 6. Uncertainty Engine
    unc_res = UncertaintyEngine.calculate(pred_res.probabilities, quality_score, observability)
    
    # 7. Anomaly Engine
    anom_res = AnomalyEngine.evaluate_weight(payload.weight_kg, baseline_weight)
    
    # 8. 8-Step Deterministic Policy Engine Decision
    decision_state, automation_allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=hazard_res.critical_hazard,
        critical_conflict=fusion_res.conflict_score >= 0.60,
        operational_risk_high=max(fusion_res.conflict_score, unc_res.uncertainty_score) >= 0.65,
        not_observable_or_critical_missing=(observability == "NOT_OBSERVABLE" or "LOW_IMAGE_QUALITY" in fusion_res.missing_evidence),
        high_uncertainty=unc_res.uncertainty_score >= 0.60,
        moderate_uncertainty_or_minor_conflict=(unc_res.uncertainty_score >= 0.35 or len(fusion_res.missing_evidence) > 0 or len(fusion_res.conflict_codes) > 0)
    )
    
    # 9. Reasons & Counterfactuals
    reasons = ReasoningPanelEngine.generate_reasons(
        quality_score, pred_res.confidence, observability, fusion_res.conflict_codes, unc_res.uncertainty_score, anom_res.z_score, hazard_res
    )
    counterfactuals = CounterfactualEngine.evaluate_required_conditions(
        observability, fusion_res.conflict_codes, unc_res.uncertainty_score, quality_score, hazard_res
    )
    
    # Construct DecisionTrace
    trace = DecisionTrace(
        event_id=event_code,
        prediction={"category": pred_res.predicted_category, "confidence": pred_res.confidence, "probabilities": pred_res.probabilities, "model_version": pred_res.model_version},
        hazard=hazard_res.to_dict(),
        evidence={"image_quality": quality_score, "observability": observability, "barcode_support": fusion_res.barcode_support, "weight_support": fusion_res.weight_support, "historical_support": fusion_res.historical_support, "hazard_support": fusion_res.hazard_support, "missing_evidence": fusion_res.missing_evidence},
        conflicts={"score": fusion_res.conflict_score, "detected": fusion_res.conflict_score > 0, "conflict_codes": fusion_res.conflict_codes},
        uncertainty={"entropy": unc_res.entropy, "uncertainty_score": unc_res.uncertainty_score, "calibration_status": unc_res.calibration_status},
        risk={"score": max(fusion_res.conflict_score, unc_res.uncertainty_score, hazard_res.score if hazard_res.critical_hazard else 0.0), "hazard_risk": hazard_res.score, "anomaly_risk": anom_res.z_score / 5.0, "delay_risk": 0.1, "department_criticality": 0.8},
        decision={"state": decision_state, "automation_allowed": automation_allowed, "reason_codes": [r["message"] for r in reasons], "action_recommended": "Auto Approve" if decision_state == "SAFE_TO_AUTOMATE" else ("Critical Hazard - Human Verification & Safe Handling Required" if hazard_res.critical_hazard else "Human Verification Required")},
        counterfactual={"required": counterfactuals},
        versions={"model_version": pred_res.model_version, "fusion_version": "V1", "policy_version": "V1", "risk_version": "V1", "trace_version": "V1"},
        timestamps={"created_at": datetime.datetime.utcnow().isoformat()}
    )
    
    return {"decision_state": decision_state, "automation_allowed": automation_allowed, "trace": trace.to_dict(), "reasons": reasons}
