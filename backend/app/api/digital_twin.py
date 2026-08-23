from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain_models import Department
from app.domain.intelligence.digital_twin_engine import DigitalTwinEngine

router = APIRouter(prefix="/digital-twin", tags=["Digital Twin"])

@router.get("")
def get_digital_twin_status(db: Session = Depends(get_db)):
    depts = db.query(Department).all()
    results = []
    for d in depts:
        intel = DigitalTwinEngine.calculate_integrity_score(
            anomaly_rate=0.05 if "lab" in d.code.lower() else 0.01,
            uncertainty_rate=0.08,
            mismatch_rate=0.02,
            delay_rate=0.03
        )
        results.append({
            "dept_id": d.id,
            "name": d.name,
            "code": d.code,
            "baseline_daily_waste_kg": d.baseline_daily_waste_kg,
            "current_volume_kg": round(d.baseline_daily_waste_kg * 0.78, 1),
            "criticality_score": d.criticality_score,
            "integrity": intel,
            "pending_collection_count": 2 if "icu" in d.code.lower() else 1
        })
    return results
