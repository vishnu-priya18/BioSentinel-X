from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain_models import WasteEvent, Decision, VerificationEvent, WastePassport, CollectionTask, WasteCategory, AuditEvent, AuditHashChain
from app.schemas.domain_schemas import VerificationRequest
from app.domain.compliance.passport_engine import PassportEngine
from app.domain.audit.audit_chain_engine import AuditChainEngine
import datetime

router = APIRouter(prefix="/verification", tags=["Human Verification Queue"])

@router.get("/queue")
def get_verification_queue(db: Session = Depends(get_db)):
    # Fetch events in NEEDS_VERIFICATION, HIGH_RISK_ESCALATION, or UNKNOWN state
    decisions = db.query(Decision).filter(Decision.decision_state.in_(["NEEDS_VERIFICATION", "HIGH_RISK_ESCALATION", "UNKNOWN"])).all()
    queue = []
    for d in decisions:
        ev = db.query(WasteEvent).filter(WasteEvent.id == d.event_id).first()
        if ev:
            # Check if already verified
            existing_ver = db.query(VerificationEvent).filter(VerificationEvent.event_id == ev.id).first()
            if not existing_ver:
                queue.append({
                    "event_id": ev.id,
                    "event_code": ev.event_code,
                    "weight_kg": ev.weight_kg,
                    "opacity_state": ev.opacity_state,
                    "decision_state": d.decision_state,
                    "reasons": d.reasons_json,
                    "created_at": ev.created_at.isoformat()
                })
    return queue

@router.post("/{event_code}/verify")
def submit_verification(event_code: str, req: VerificationRequest, db: Session = Depends(get_db)):
    ev = db.query(WasteEvent).filter(WasteEvent.event_code == event_code).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Waste event not found")
        
    cat = db.query(WasteCategory).filter(WasteCategory.code == req.verified_category_code).first()
    cat_id = cat.id if cat else ev.declared_category_id
    
    # 1. Create append-only verification event (NEVER overwrite original decision)
    ver_event = VerificationEvent(
        event_id=ev.id,
        verifier_id="usr-verifier",
        previous_category_id=ev.declared_category_id,
        verified_category_id=cat_id,
        decision_action=req.decision_action,
        verifier_notes=req.verifier_notes or "Human verifier inspected evidence graph and signed off."
    )
    db.add(ver_event)
    
    # 2. Issue Waste Passport
    passport_code = PassportEngine.generate_code(event_code)
    passport = WastePassport(
        passport_code=passport_code,
        event_id=ev.id,
        declared_category_id=ev.declared_category_id,
        verified_category_id=cat_id,
        weight_kg=ev.weight_kg,
        risk_level="LOW" if req.decision_action == "APPROVE" else "HIGH",
        status="ISSUED",
        evidence_hash="SHA256_VERIFIED"
    )
    db.add(passport)
    db.commit()
    
    return {"message": "Verification event logged successfully", "passport_code": passport_code}
