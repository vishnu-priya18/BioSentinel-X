from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.seed_data import seed_database

# Include API Routers
from app.api.auth import router as auth_router
from app.api.waste_events import router as waste_events_router
from app.api.verification import router as verification_router
from app.api.passports import router as passports_router
from app.api.collection import router as collection_router
from app.api.analytics import router as analytics_router
from app.api.digital_twin import router as digital_twin_router
from app.api.simulation import router as simulation_router
from app.api.settings import router as settings_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="BioSentinel-X: Software-Defined Biomedical Waste Decision Operating System (SIH26115)"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_setup():
    # Create all database tables
    Base.metadata.create_all(bind=engine)
    # Seed deterministic demo data (DEMO-001 to DEMO-008)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": "SIH_PROTOTYPE_SIMULATION"
    }

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(waste_events_router, prefix=settings.API_V1_STR)
app.include_router(verification_router, prefix=settings.API_V1_STR)
app.include_router(passports_router, prefix=settings.API_V1_STR)
app.include_router(collection_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(digital_twin_router, prefix=settings.API_V1_STR)
app.include_router(simulation_router, prefix=settings.API_V1_STR)
app.include_router(settings_router, prefix=settings.API_V1_STR)
