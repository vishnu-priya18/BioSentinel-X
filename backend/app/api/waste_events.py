import datetime
import logging
import base64
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.database import get_db
from app.models.domain_models import WasteEvent, AiPrediction, UncertaintyAssessment, Decision, Department, WasteCategory, AuditEvent, AuditHashChain
from app.schemas.domain_schemas import WasteEventCreate, DecisionTraceSchema
from app.domain.evidence.quality_evaluator import QualityEvaluator
from app.domain.evidence.observability_engine import ObservabilityEngine
from app.domain.evidence.evidence_fusion_engine import EvidenceFusionEngine
from app.domain.intelligence.object_detector import WasteObjectDetector, ObjectDetectionResponse
from app.domain.intelligence.classifier_adapter import DemoWasteClassifier
from app.domain.intelligence.uncertainty_engine import UncertaintyEngine
from app.domain.intelligence.anomaly_engine import AnomalyEngine
from app.domain.safety.hazard_gate import HazardGate
from app.domain.decision.policy_engine import PolicyEngine
from app.domain.decision.reasoning_panel_engine import ReasoningPanelEngine
from app.domain.decision.counterfactual_engine import CounterfactualEngine
from app.domain.decision.decision_trace import DecisionTrace

logger = logging.getLogger("biosentinel.vision")
logging.basicConfig(level=logging.INFO)

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

@router.get("/debug/latest")
def get_latest_debug_event(db: Session = Depends(get_db)):
    dec = db.query(Decision).order_by(Decision.id.desc()).first()
    if not dec or not dec.trace_json:
        raise HTTPException(status_code=404, detail="No analysis events found")
    
    trace = dec.trace_json
    return {
        "event_id": trace.get("event_id"),
        "detected_objects": trace.get("detected_objects"),
        "primary_object": trace.get("primary_object"),
        "recommended_category": trace.get("recommended_category"),
        "hazard_assessment": trace.get("hazard"),
        "uncertainty": trace.get("uncertainty"),
        "conflict": trace.get("conflicts"),
        "final_decision": trace.get("decision")
    }

@router.get("/{event_code}/trace")
def get_decision_trace(event_code: str, db: Session = Depends(get_db)):
    ev = db.query(WasteEvent).filter(WasteEvent.event_code == event_code).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Waste event not found")
        
    dec = db.query(Decision).filter(Decision.event_id == ev.id).first()
    if not dec or not dec.trace_json:
        raise HTTPException(status_code=404, detail="Decision trace not found")
        
    return dec.trace_json

@router.post("/detect")
async def detect_objects_only(
    image_file: Optional[UploadFile] = File(None),
    payload: Optional[WasteEventCreate] = None
):
    """
    Dedicated Object Detection Endpoint.
    Returns detected objects, bounding boxes, confidence, and primary object.
    """
    detection_res = WasteObjectDetector.detect(
        image_base64=payload.image_base64 if payload else None,
        metadata={"item_description": payload.user_notes if payload else ""}
    )
    return detection_res.to_dict()

@router.post("/analyze")
async def analyze_waste_event(
    payload: Optional[WasteEventCreate] = None,
    image_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Complete 12-Step BioSentinel-X Decision Pipeline:
    REAL IMAGE -> OBJECT DETECTOR -> HAZARD GATE -> CATEGORY MAPPER -> POLICY ENGINE -> DECISION TRACE
    """
    if payload is None:
        payload = WasteEventCreate(
            dept_id="dept-icu",
            declared_category_code="White",
            weight_kg=0.25,
            container_type="PLASTIC_BAG",
            opacity_state="OBSERVABLE"
        )

    event_code = payload.event_code or f"EVT-{int(datetime.datetime.utcnow().timestamp())}"
    image_bytes = None
    filename = "uploaded_photo.png"
    size_bytes = 0

    try:
        if image_file:
            filename = image_file.filename or "uploaded_photo.png"
            image_bytes = await image_file.read()
            size_bytes = len(image_bytes)
        elif payload.image_base64:
            b64_data = payload.image_base64
            if "," in b64_data:
                b64_data = b64_data.split(",")[1]
            image_bytes = base64.b64decode(b64_data)
            size_bytes = len(image_bytes)
    except Exception as e:
        logger.error(f"[VISION ERROR] Image decoding failed: {e}")
        return {
            "decision_state": "SYSTEM_ERROR",
            "automation_allowed": False,
            "reason": "Corrupted image file or invalid encoding format."
        }

    logger.info(f"[VISION DEBUG] IMAGE RECEIVED: filename={filename}, size_bytes={size_bytes}")
    logger.info("[VISION DEBUG] OBJECT DETECTOR STARTED")

    # Step 1: Quality & Observability
    quality_score = QualityEvaluator.evaluate(payload.image_base64)
    observability = ObservabilityEngine.evaluate(payload.opacity_state, payload.container_type)

    # Step 2: Object Detection
    detection_res = WasteObjectDetector.detect(payload.image_base64, {
        "item_description": payload.user_notes,
        "scenario_code": event_code
    })

    # Step 3: Classifier prediction
    classifier = DemoWasteClassifier()
    pred_res = classifier.predict(payload.image_base64, {
        "declared_category": payload.declared_category_code,
        "scenario_code": event_code,
        "item_description": payload.user_notes
    })

    primary_obj = detection_res.primary_object
    primary_class = primary_obj.class_name if primary_obj else "UNKNOWN_OBJECT"
    primary_conf = primary_obj.confidence if primary_obj else 0.50

    logger.info(f"[VISION DEBUG] DETECTOR RESULT: primary_object={primary_class}, confidence={primary_conf}")

    # Step 4: Hazard Gate Assessment
    hazard_res = HazardGate.assess(payload.image_base64, {
        "scenario_code": event_code,
        "declared_category": payload.declared_category_code,
        "item_description": payload.user_notes,
        "demo_hazard": primary_class if primary_class in ["SYRINGE", "NEEDLE", "SCALPEL", "BLADE", "LANCET"] else ""
    })

    # Step 5: Department Baseline Lookup
    dept = db.query(Department).filter(Department.id == payload.dept_id).first()
    baseline_weight = dept.baseline_daily_waste_kg if dept else 2.1

    # Step 6: Evidence Fusion
    fusion_res = EvidenceFusionEngine.fuse(
        declared_category=payload.declared_category_code,
        predicted_category=pred_res.bag_category,
        barcode_scanned=payload.barcode_scanned or f"CPCB-IND-{event_code}",
        weight_kg=payload.weight_kg,
        baseline_weight_kg=baseline_weight,
        observability=observability,
        quality_score=quality_score,
        hazard_result=hazard_res
    )

    # Step 7: Uncertainty Engine
    unc_res = UncertaintyEngine.calculate(pred_res.probabilities, quality_score, observability)

    # Step 8: Anomaly Engine
    anom_res = AnomalyEngine.evaluate_weight(payload.weight_kg, baseline_weight)

    # Step 9: Deterministic Policy Engine Decision
    decision_state, automation_allowed = PolicyEngine.decide(
        system_error=False,
        critical_hazard_detected=hazard_res.critical_hazard,
        critical_conflict=fusion_res.conflict_score >= 0.60,
        operational_risk_high=max(fusion_res.conflict_score, unc_res.uncertainty_score) >= 0.65,
        object_not_detected=(detection_res.detector_status == "NO_OBJECT_DETECTED" or primary_conf < 0.50),
        not_observable=(observability == "NOT_OBSERVABLE" or "LOW_IMAGE_QUALITY" in fusion_res.missing_evidence),
        high_uncertainty=unc_res.uncertainty_score >= 0.60,
        moderate_uncertainty=(unc_res.uncertainty_score >= 0.35 or len(fusion_res.missing_evidence) > 0 or len(fusion_res.conflict_codes) > 0)
    )

    # Step 10: Reasons & Counterfactuals
    reasons = ReasoningPanelEngine.generate_reasons(
        quality_score, pred_res.confidence, observability, fusion_res.conflict_codes, unc_res.uncertainty_score, anom_res.z_score, hazard_res
    )
    counterfactuals = CounterfactualEngine.evaluate_required_conditions(
        observability, fusion_res.conflict_codes, unc_res.uncertainty_score, quality_score, hazard_res
    )

    # Construct DecisionTrace
    trace_dict = {
        "event_id": event_code,
        "detector_status": detection_res.detector_status,
        "detected_objects": [obj.to_dict() for obj in detection_res.objects],
        "primary_object": primary_obj.to_dict() if primary_obj else None,
        "prediction": {
            "object_class": primary_class,
            "category": pred_res.bag_category,
            "confidence": primary_conf,
            "probabilities": pred_res.probabilities,
            "model_version": pred_res.model_version
        },
        "classification": {
            "object_class": primary_class,
            "waste_type": pred_res.waste_type,
            "bag_category": pred_res.bag_category
        },
        "recommended_category": {
            "code": pred_res.bag_category,
            "waste_type": pred_res.waste_type
        },
        "hazard": hazard_res.to_dict(),
        "evidence": {
            "image_quality": quality_score,
            "observability": observability,
            "barcode_support": fusion_res.barcode_support,
            "weight_support": fusion_res.weight_support,
            "historical_support": fusion_res.historical_support,
            "hazard_support": fusion_res.hazard_support,
            "missing_evidence": fusion_res.missing_evidence
        },
        "conflicts": {
            "score": fusion_res.conflict_score,
            "detected": fusion_res.conflict_score > 0,
            "conflict_codes": fusion_res.conflict_codes
        },
        "uncertainty": {
            "entropy": unc_res.entropy,
            "uncertainty_score": unc_res.uncertainty_score,
            "calibration_status": unc_res.calibration_status
        },
        "risk": {
            "score": max(fusion_res.conflict_score, unc_res.uncertainty_score, hazard_res.score if hazard_res.critical_hazard else 0.0),
            "hazard_risk": hazard_res.score,
            "anomaly_risk": anom_res.z_score / 5.0,
            "delay_risk": 0.1,
            "department_criticality": 0.8
        },
        "decision": {
            "state": decision_state,
            "automation_allowed": automation_allowed,
            "reason_codes": [r["message"] for r in reasons],
            "action_recommended": "Auto Approve" if decision_state == "SAFE_TO_AUTOMATE" else ("Critical Hazard - Human Verification & Safe Handling Required" if hazard_res.critical_hazard else "Human Verification Required")
        },
        "counterfactual": {"required": counterfactuals},
        "versions": {"model_version": pred_res.model_version, "fusion_version": "V1", "policy_version": "V1", "risk_version": "V1", "trace_version": "V1"},
        "timestamps": {"created_at": datetime.datetime.utcnow().isoformat()},
        "inference_debug": {
            "image_received": size_bytes > 0 or payload.image_base64 is not None,
            "filename": filename,
            "size_bytes": size_bytes,
            "model_version": pred_res.model_version,
            "model_status": detection_res.model_status,
            "primary_object": primary_class,
            "confidence": primary_conf,
            "mapped_category": pred_res.bag_category,
            "hazard": hazard_res.hazard_type
        }
    }

    return {"decision_state": decision_state, "automation_allowed": automation_allowed, "trace": trace_dict, "reasons": reasons}
