from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Token & Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    role_name: str
    full_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

# DecisionTrace Sub-Schemas
class PredictionPayload(BaseModel):
    category: str
    confidence: float
    probabilities: Dict[str, float]
    model_version: str

class HazardPayload(BaseModel):
    detected: bool
    hazard_type: str
    severity: str
    score: float
    critical: bool
    automation_allowed: bool
    evidence_source: str
    explanation: str

class EvidencePayload(BaseModel):
    image_quality: float
    observability: str # OBSERVABLE, PARTIALLY_OBSERVABLE, NOT_OBSERVABLE
    barcode_support: float
    weight_support: float
    historical_support: float
    hazard_support: Optional[float] = 1.0
    missing_evidence: List[str]

class ConflictsPayload(BaseModel):
    score: float
    detected: bool
    conflict_codes: List[str]

class UncertaintyPayload(BaseModel):
    entropy: float
    uncertainty_score: float
    calibration_status: str

class RiskPayload(BaseModel):
    score: float
    hazard_risk: float
    anomaly_risk: float
    delay_risk: float
    department_criticality: float

class DecisionPayload(BaseModel):
    state: str # SAFE_TO_AUTOMATE, NEEDS_VERIFICATION, HIGH_RISK_ESCALATION, UNKNOWN, SYSTEM_ERROR
    automation_allowed: bool = False
    reason_codes: List[str]
    action_recommended: str

class CounterfactualPayload(BaseModel):
    required: List[str]

class VersionsPayload(BaseModel):
    model_version: str
    fusion_version: str
    policy_version: str
    risk_version: str
    trace_version: str

class DecisionTraceSchema(BaseModel):
    event_id: str
    prediction: PredictionPayload
    hazard: HazardPayload
    evidence: EvidencePayload
    conflicts: ConflictsPayload
    uncertainty: UncertaintyPayload
    risk: RiskPayload
    decision: DecisionPayload
    counterfactual: CounterfactualPayload
    versions: VersionsPayload
    timestamps: Dict[str, str]

# Waste Event Schemas
class WasteEventCreate(BaseModel):
    event_code: Optional[str] = None
    dept_id: str
    declared_category_code: str
    weight_kg: float
    container_type: str = "PLASTIC_BAG"
    opacity_state: str = "OBSERVABLE"
    user_notes: Optional[str] = None
    barcode_scanned: Optional[str] = None
    image_base64: Optional[str] = None

class VerificationRequest(BaseModel):
    verified_category_code: str
    decision_action: str # APPROVE, RECLASSIFY, ESCALATE
    verifier_notes: Optional[str] = None

# Routing & Priority Schemas
class PriorityExplanationSchema(BaseModel):
    priority_score: float
    overflow_risk: float
    hazard_risk: float
    uncertainty: float
    collection_delay: float
    department_criticality: float
    travel_cost: float
    weighted_components: Dict[str, float]
