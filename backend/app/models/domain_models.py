import datetime
import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Role(Base):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    role_name = Column(String(50), unique=True, nullable=False, index=True) # ADMIN, SUPERVISOR, SANITATION_WORKER, VERIFIER, VIEWER
    permissions_json = Column(JSON, nullable=False)

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    config_json = Column(JSON, nullable=True)

class Department(Base):
    __tablename__ = "departments"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    hospital_id = Column(String(36), ForeignKey("hospitals.id"), nullable=False)
    name = Column(String(100), nullable=False, index=True) # ICU, Emergency, Laboratory, Ward A, Ward B, Operation Theatre
    code = Column(String(20), unique=True, nullable=False)
    baseline_daily_waste_kg = Column(Float, default=10.0)
    criticality_score = Column(Float, default=50.0) # 0 to 100

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False)
    dept_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WasteCategory(Base):
    __tablename__ = "waste_categories"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(20), unique=True, nullable=False) # Yellow, Red, White, Blue, Unknown
    display_name = Column(String(50), nullable=False)
    color_hex = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    accepted_examples = Column(JSON, nullable=True)
    safety_notes = Column(Text, nullable=True)
    active = Column(Boolean, default=True)

class WasteEvent(Base):
    __tablename__ = "waste_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_code = Column(String(50), unique=True, nullable=False, index=True) # DEMO-001, etc.
    dept_id = Column(String(36), ForeignKey("departments.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    declared_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=True)
    weight_kg = Column(Float, nullable=False)
    container_type = Column(String(50), default="PLASTIC_BAG")
    opacity_state = Column(String(30), default="OBSERVABLE", index=True) # OBSERVABLE, PARTIALLY_OBSERVABLE, NOT_OBSERVABLE
    user_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=False)
    item_type = Column(String(50), nullable=False) # IMAGE, BARCODE, WEIGHT, DEPT_HISTORY, USER_OBSERVATION, ACOUSTIC
    value = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    reliability = Column(Float, default=1.0)
    quality_score = Column(Float, default=1.0)
    status = Column(String(30), default="SUPPORTING") # SUPPORTING, CONFLICTING, MISSING, UNKNOWN

class AiPrediction(Base):
    __tablename__ = "ai_predictions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=False)
    model_name = Column(String(100), default="DEMO_SIMULATION_MODEL")
    predicted_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=False)
    class_probabilities_json = Column(JSON, nullable=False)
    confidence = Column(Float, nullable=False)
    inference_ms = Column(Float, default=34.0)
    is_simulated = Column(Boolean, default=True)

class UncertaintyAssessment(Base):
    __tablename__ = "uncertainty_assessments"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=False)
    entropy = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False)
    uncertainty_score = Column(Float, nullable=False)
    observability_state = Column(String(30), nullable=False)
    level_enum = Column(String(30), nullable=False) # LOW_UNCERTAINTY, MEDIUM_UNCERTAINTY, HIGH_UNCERTAINTY

class Decision(Base):
    __tablename__ = "decisions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=False)
    decision_state = Column(String(50), nullable=False, index=True) # SAFE_TO_AUTOMATE, NEEDS_VERIFICATION, HIGH_RISK_ESCALATION, UNKNOWN, SYSTEM_ERROR
    final_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=True)
    risk_level = Column(String(30), default="LOW")
    reasons_json = Column(JSON, nullable=False)
    missing_evidence_json = Column(JSON, nullable=True)
    conflicting_evidence_json = Column(JSON, nullable=True)
    action_recommended = Column(Text, nullable=False)
    trace_json = Column(JSON, nullable=False) # Full DecisionTrace payload

class VerificationEvent(Base):
    __tablename__ = "verification_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=False)
    verifier_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    previous_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=True)
    verified_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=False)
    decision_action = Column(String(50), nullable=False) # APPROVE, RECLASSIFY, ESCALATE
    verifier_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WastePassport(Base):
    __tablename__ = "waste_passports"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    passport_code = Column(String(50), unique=True, nullable=False, index=True)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=False)
    declared_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=True)
    verified_category_id = Column(String(36), ForeignKey("waste_categories.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    risk_level = Column(String(30), nullable=False)
    status = Column(String(30), default="ISSUED") # ISSUED, COLLECTED, HANDED_OVER, REJECTED
    evidence_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CollectionTask(Base):
    __tablename__ = "collection_tasks"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    passport_id = Column(String(36), ForeignKey("waste_passports.id"), nullable=False)
    dept_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    assigned_worker_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    priority_score = Column(Float, nullable=False) # Computed P_task score
    status = Column(String(30), default="PENDING", index=True) # PENDING, ASSIGNED, EN_ROUTE, COLLECTED, VERIFIED, HANDED_OVER, CANCELLED
    assigned_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

class CollectionEvent(Base):
    __tablename__ = "collection_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_id = Column(String(36), ForeignKey("collection_tasks.id"), nullable=False)
    worker_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    location_coords = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class HandoverEvent(Base):
    __tablename__ = "handover_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    passport_id = Column(String(36), ForeignKey("waste_passports.id"), nullable=False)
    cbwtf_vehicle_id = Column(String(50), nullable=False)
    weight_verified_kg = Column(Float, nullable=False)
    agent_name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class DepartmentProfile(Base):
    __tablename__ = "department_profiles"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    dept_id = Column(String(36), ForeignKey("departments.id"), nullable=False, unique=True)
    avg_daily_waste_kg = Column(Float, default=10.0)
    integrity_score = Column(Float, default=95.0) # 0 to 100
    anomaly_count_30d = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Anomaly(Base):
    __tablename__ = "anomalies"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    dept_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    event_id = Column(String(36), ForeignKey("waste_events.id"), nullable=True)
    anomaly_type = Column(String(50), nullable=False) # VOLUME_SURGE, WEIGHT_ABNORMAL, BARCODE_MISMATCH, UNCERTAINTY_SPIKE
    observed_value = Column(Float, nullable=False)
    baseline_value = Column(Float, nullable=False)
    z_score = Column(Float, nullable=False)
    severity = Column(String(30), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    recommended_action = Column(Text, nullable=False)
    status = Column(String(30), default="ACTIVE")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    hospital_id = Column(String(36), ForeignKey("hospitals.id"), nullable=False)
    dept_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    alert_type = Column(String(50), nullable=False)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(30), default="MEDIUM", index=True) # LOW, MEDIUM, HIGH, CRITICAL
    acknowledged_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_name = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    performed_by = Column(String(36), nullable=False)
    payload_json = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AuditHashChain(Base):
    __tablename__ = "audit_hash_chain"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    audit_event_id = Column(String(36), ForeignKey("audit_events.id"), nullable=False, unique=True)
    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    key = Column(String(100), unique=True, nullable=False)
    value_json = Column(JSON, nullable=False)
    updated_by = Column(String(36), nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
