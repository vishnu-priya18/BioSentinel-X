from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/settings", tags=["System Settings"])

@router.get("")
def get_settings():
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "VERSION": settings.VERSION,
        "HIGH_CONFLICT_THRESHOLD": settings.HIGH_CONFLICT_THRESHOLD,
        "HIGH_RISK_THRESHOLD": settings.HIGH_RISK_THRESHOLD,
        "HIGH_UNCERTAINTY_THRESHOLD": settings.HIGH_UNCERTAINTY_THRESHOLD,
        "VERIFICATION_THRESHOLD": settings.VERIFICATION_THRESHOLD,
        "QUALITY_MINIMUM_THRESHOLD": settings.QUALITY_MINIMUM_THRESHOLD,
        "CALIBRATION_STATUS": "Calibrated for Prototype Dataset (Configurable)",
        "SAFETY_DISCLAIMER": "AI classification is decision support and does not replace trained biomedical-waste personnel, hospital protocols, or applicable regulatory requirements."
    }
