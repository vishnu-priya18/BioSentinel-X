export type DecisionState = 
  | 'SAFE_TO_AUTOMATE'
  | 'NEEDS_VERIFICATION'
  | 'HIGH_RISK_ESCALATION'
  | 'UNKNOWN'
  | 'SYSTEM_ERROR';

export type ObservabilityState = 
  | 'OBSERVABLE'
  | 'PARTIALLY_OBSERVABLE'
  | 'NOT_OBSERVABLE';

export type UserRole = 
  | 'ADMIN'
  | 'SUPERVISOR'
  | 'SANITATION_WORKER'
  | 'VERIFIER'
  | 'VIEWER';

export interface HazardAssessment {
  detected: boolean;
  hazard_type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  score: number;
  critical: boolean;
  critical_hazard?: boolean;
  automation_allowed: boolean;
  evidence_source: string;
  explanation: string;
}

export interface DecisionTrace {
  event_id: string;
  prediction: {
    category: string;
    confidence: number;
    probabilities: Record<string, number>;
    model_version: string;
  };
  hazard: HazardAssessment;
  evidence: {
    image_quality: number;
    observability: ObservabilityState;
    barcode_support: number;
    weight_support: number;
    historical_support: number;
    hazard_support?: number;
    missing_evidence: string[];
  };
  conflicts: {
    score: number;
    detected: boolean;
    conflict_codes: string[];
  };
  uncertainty: {
    entropy: number;
    uncertainty_score: number;
    calibration_status: string;
  };
  risk: {
    score: number;
    hazard_risk: number;
    anomaly_risk: number;
    delay_risk: number;
    department_criticality: number;
  };
  decision: {
    state: DecisionState;
    automation_allowed?: boolean;
    reason_codes: string[];
    action_recommended: string;
  };
  counterfactual: {
    required: string[];
  };
  versions: Record<string, string>;
  timestamps: Record<string, string>;
}

export interface ReasoningItem {
  status: 'PASS' | 'WARNING' | 'FAIL';
  source: string;
  message: string;
  technical_value: string;
  explanation: string;
}

export interface DemoScenario {
  code: string;
  title: string;
  expected_state: DecisionState;
  description: string;
}
