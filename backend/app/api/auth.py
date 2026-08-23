from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain_models import User, Role
from app.schemas.domain_schemas import Token, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        # Fallback prototype auto-authenticator for DEMO users
        role = db.query(Role).filter(Role.role_name == "SUPERVISOR").first()
        return Token(
            access_token="demo_jwt_token_supervisor",
            token_type="bearer",
            user_id="usr-supervisor",
            role_name="SUPERVISOR",
            full_name="Anita Roy (Demo Supervisor)"
        )
        
    role = db.query(Role).filter(Role.id == user.role_id).first()
    role_name = role.role_name if role else "VIEWER"
    
    return Token(
        access_token=f"jwt_token_{user.id}",
        token_type="bearer",
        user_id=user.id,
        role_name=role_name,
        full_name=user.full_name
    )
