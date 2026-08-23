import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BioSentinel-X"
    VERSION: str = "1.0.0-SIH-PROTOTYPE"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "biosentinel-x-sih-2026-secret-key-32bytes-min")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours for prototype
    
    # SQLite default for zero-config local run, PostgreSQL ready
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./biosentinel_x.db")
    
    # Configurable Engine Thresholds
    HIGH_CONFLICT_THRESHOLD: float = 0.60
    HIGH_RISK_THRESHOLD: float = 0.65
    HIGH_UNCERTAINTY_THRESHOLD: float = 0.60
    VERIFICATION_THRESHOLD: float = 0.35
    QUALITY_MINIMUM_THRESHOLD: float = 0.40
    
    class Config:
        case_sensitive = True

settings = Settings()
