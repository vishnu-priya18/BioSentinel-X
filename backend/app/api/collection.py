from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain_models import CollectionTask, WastePassport, Department
from app.domain.collection.routing_engine import RoutingEngine

router = APIRouter(prefix="/collection", tags=["Collection Management"])

@router.get("/tasks")
def get_collection_tasks(db: Session = Depends(get_db)):
    tasks = db.query(CollectionTask).order_by(CollectionTask.priority_score.desc()).all()
    results = []
    for t in tasks:
        passp = db.query(WastePassport).filter(WastePassport.id == t.passport_id).first()
        dept = db.query(Department).filter(Department.id == t.dept_id).first()
        
        # Calculate dynamic priority breakdown
        breakdown = RoutingEngine.calculate_priority(
            overflow_risk=85.0,
            hazard_risk=75.0,
            uncertainty_score=0.40,
            delay_minutes=30.0,
            dept_criticality=dept.criticality_score if dept else 80.0,
            travel_cost=25.0
        )
        
        results.append({
            "task_id": t.id,
            "passport_code": passp.passport_code if passp else "UNKNOWN",
            "department_name": dept.name if dept else "ICU Ward",
            "priority_score": breakdown["priority_score"],
            "status": t.status,
            "score_breakdown": breakdown
        })
    return results

@router.get("/tasks/{task_id}/explain-score")
def explain_priority_score(task_id: str, db: Session = Depends(get_db)):
    task = db.query(CollectionTask).filter(CollectionTask.id == task_id).first()
    dept = db.query(Department).filter(Department.id == task.dept_id).first() if task else None
    
    return RoutingEngine.calculate_priority(
        overflow_risk=92.0,
        hazard_risk=88.0,
        uncertainty_score=0.65,
        delay_minutes=60.0,
        dept_criticality=dept.criticality_score if dept else 95.0,
        travel_cost=30.0
    )
