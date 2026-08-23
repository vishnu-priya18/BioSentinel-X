from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain_models import WastePassport, WasteEvent, WasteCategory
from app.domain.compliance.passport_engine import PassportEngine

router = APIRouter(prefix="/passports", tags=["Waste Passports"])

@router.get("")
def list_passports(db: Session = Depends(get_db)):
    passports = db.query(WastePassport).order_by(WastePassport.created_at.desc()).all()
    results = []
    for p in passports:
        ev = db.query(WasteEvent).filter(WasteEvent.id == p.event_id).first()
        v_cat = db.query(WasteCategory).filter(WasteCategory.id == p.verified_category_id).first()
        results.append({
            "id": p.id,
            "passport_code": p.passport_code,
            "event_code": ev.event_code if ev else "UNKNOWN",
            "verified_category": v_cat.code if v_cat else "Red",
            "weight_kg": p.weight_kg,
            "risk_level": p.risk_level,
            "status": p.status,
            "evidence_hash": p.evidence_hash,
            "created_at": p.created_at.isoformat()
        })
    return results

@router.get("/{passport_code}")
def get_passport_detail(passport_code: str, db: Session = Depends(get_db)):
    p = db.query(WastePassport).filter(WastePassport.passport_code == passport_code).first()
    if not p:
        raise HTTPException(status_code=404, detail="Waste passport not found")
        
    ev = db.query(WasteEvent).filter(WasteEvent.id == p.event_id).first()
    v_cat = db.query(WasteCategory).filter(WasteCategory.id == p.verified_category_id).first()
    
    return {
        "id": p.id,
        "passport_code": p.passport_code,
        "event_code": ev.event_code if ev else "UNKNOWN",
        "verified_category": v_cat.code if v_cat else "Red",
        "weight_kg": p.weight_kg,
        "risk_level": p.risk_level,
        "status": p.status,
        "evidence_hash": p.evidence_hash,
        "created_at": p.created_at.isoformat()
    }

@router.get("/{passport_code}/qr")
def get_passport_qr_code(passport_code: str):
    """
    Generates dynamic SVG QR code representation on demand.
    Does NOT store raw SVG as DB source of truth.
    """
    svg_data = PassportEngine.generate_qr_svg(passport_code)
    return Response(content=svg_data, media_type="image/svg+xml")
