from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain_models import WasteEvent, Decision, AuditHashChain
from app.domain.audit.audit_chain_engine import AuditChainEngine

router = APIRouter(prefix="/simulation", tags=["SIH Grand Finale Simulation Mode"])

@router.get("/scenarios")
def list_demo_scenarios():
    return [
        {"code": "DEMO-001", "title": "Clear IV Tubing (Safe Red Waste)", "expected_state": "SAFE_TO_AUTOMATE", "description": "Clear plastic tubing, valid barcode, normal weight (0.22kg). High confidence accept."},
        {"code": "DEMO-002", "title": "Low-Quality / Blurry Image", "expected_state": "NEEDS_VERIFICATION", "description": "Dim, blurry image capture below quality threshold (0.25). Triggers verification."},
        {"code": "DEMO-003", "title": "THE KILLER CASE: Opaque Container", "expected_state": "UNKNOWN", "description": "AI predicts Red (91% confidence) BUT container is Opaque -> UNKNOWN contents!"},
        {"code": "DEMO-004", "title": "Conflicting Barcode & Weight", "expected_state": "HIGH_RISK_ESCALATION", "description": "Yellow barcode on Red plastic tubing + abnormal weight (Conflict score 0.71)."},
        {"code": "DEMO-005", "title": "Abnormal Weight Anomaly", "expected_state": "HIGH_RISK_ESCALATION", "description": "Lab waste weight 18.5kg vs 2.1kg baseline (8.8x multiplier, Z = +4.8)."},
        {"code": "DEMO-006", "title": "ICU Waste Volume Surge", "expected_state": "SAFE_TO_AUTOMATE", "description": "Surge in ICU waste volume triggers priority recalculation (P_task = 94.2)."},
        {"code": "DEMO-007", "title": "Human Verifier Review & Sign-Off", "expected_state": "SAFE_TO_AUTOMATE", "description": "Verifier inspects DEMO-002 evidence, approves event, issues Waste Passport."},
        {"code": "DEMO-008", "title": "SHA-256 Audit Chain Verification", "expected_state": "VALID_HASH_CHAIN", "description": "Executes cryptographic verification over audit chain. Result: VALID HASH CHAIN."}
    ]

@router.get("/scenarios/{code}")
def run_demo_scenario(code: str, db: Session = Depends(get_db)):
    ev = db.query(WasteEvent).filter(WasteEvent.event_code == code.upper()).first()
    if not ev:
        raise HTTPException(status_code=404, detail=f"Demo scenario {code} not found in database. Please run seed_data.")
        
    dec = db.query(Decision).filter(Decision.event_id == ev.id).first()
    
    # Audit verification check if DEMO-008
    chain_status = "VALID_HASH_CHAIN"
    if code.upper() == "DEMO-008":
        chains = db.query(AuditHashChain).all()
        # Verify chain
        valid, msg = AuditChainEngine.verify_chain(chains)
        chain_status = msg
        
    return {
        "scenario_code": code.upper(),
        "event_id": ev.id,
        "weight_kg": ev.weight_kg,
        "opacity_state": ev.opacity_state,
        "decision_state": dec.decision_state if dec else "UNKNOWN",
        "trace": dec.trace_json if dec else {},
        "reasons": dec.reasons_json if dec else [],
        "audit_chain_status": chain_status
    }
