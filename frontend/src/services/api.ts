import { DecisionTrace, DemoScenario } from '../types';

const API_BASE = '/api';

export const apiService = {
  async getDashboardKpis() {
    try {
      const res = await fetch(`${API_BASE}/analytics/dashboard-kpis`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using offline demo data for KPI analytics");
    }
    return {
      total_waste_events_today: 38,
      verified_events: 28,
      pending_verification: 7,
      high_risk_events: 3,
      active_collection_tasks: 8,
      waste_stream_integrity_score: 92.4,
      active_anomalies_count: 2
    };
  },

  async getEvents() {
    try {
      const res = await fetch(`${API_BASE}/waste-events`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using offline demo data for waste events");
    }
    return [
      { id: '1', event_code: 'DEMO-001', dept_name: 'ICU Ward', declared_category: 'Red', weight_kg: 0.22, opacity_state: 'OBSERVABLE', decision_state: 'SAFE_TO_AUTOMATE', created_at: new Date().toISOString() },
      { id: '2', event_code: 'DEMO-002', dept_name: 'Emergency Ward', declared_category: 'Yellow', weight_kg: 4.5, opacity_state: 'OBSERVABLE', decision_state: 'NEEDS_VERIFICATION', created_at: new Date().toISOString() },
      { id: '3', event_code: 'DEMO-003', dept_name: 'ICU Ward', declared_category: 'Red', weight_kg: 2.1, opacity_state: 'NOT_OBSERVABLE', decision_state: 'UNKNOWN', created_at: new Date().toISOString() },
      { id: '4', event_code: 'DEMO-004', dept_name: 'Pathology Lab', declared_category: 'Red', weight_kg: 3.2, opacity_state: 'OBSERVABLE', decision_state: 'HIGH_RISK_ESCALATION', created_at: new Date().toISOString() },
      { id: '5', event_code: 'DEMO-005', dept_name: 'Pathology Lab', declared_category: 'Red', weight_kg: 18.5, opacity_state: 'OBSERVABLE', decision_state: 'HIGH_RISK_ESCALATION', created_at: new Date().toISOString() },
    ];
  },

  async getDecisionTrace(eventCode: string): Promise<any> {
    try {
      const res = await fetch(`${API_BASE}/waste-events/${eventCode}/trace`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using offline trace simulation");
    }
    return null;
  },

  async getDemoScenarios(): Promise<DemoScenario[]> {
    try {
      const res = await fetch(`${API_BASE}/simulation/scenarios`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using offline demo scenarios");
    }
    return [
      { code: 'DEMO-001', title: 'Clear IV Tubing (Safe Red Waste)', expected_state: 'SAFE_TO_AUTOMATE', description: 'Clear plastic tubing, valid barcode, normal weight (0.22kg). High confidence accept.' },
      { code: 'DEMO-002', title: 'Low-Quality / Blurry Image', expected_state: 'NEEDS_VERIFICATION', description: 'Dim, blurry image capture below quality threshold (0.25). Triggers verification.' },
      { code: 'DEMO-003', title: 'THE KILLER CASE: Opaque Container', expected_state: 'UNKNOWN', description: 'AI predicts Red (91% confidence) BUT container is Opaque -> UNKNOWN contents!' },
      { code: 'DEMO-004', title: 'Conflicting Barcode & Weight', expected_state: 'HIGH_RISK_ESCALATION', description: 'Yellow barcode on Red plastic tubing + abnormal weight (Conflict score 0.71).' },
      { code: 'DEMO-005', title: 'Abnormal Weight Anomaly', expected_state: 'HIGH_RISK_ESCALATION', description: 'Lab waste weight 18.5kg vs 2.1kg baseline (8.8x multiplier, Z = +4.8).' },
      { code: 'DEMO-006', title: 'ICU Waste Volume Surge', expected_state: 'SAFE_TO_AUTOMATE', description: 'Surge in ICU waste volume triggers priority recalculation (P_task = 94.2).' },
      { code: 'DEMO-007', title: 'Human Verifier Review & Sign-Off', expected_state: 'SAFE_TO_AUTOMATE', description: 'Verifier inspects DEMO-002 evidence, approves event, issues Waste Passport.' },
      { code: 'DEMO-008', title: 'SHA-256 Audit Chain Verification', expected_state: 'SAFE_TO_AUTOMATE', description: 'Executes cryptographic verification over audit chain. Result: VALID HASH CHAIN.' }
    ];
  },

  async runSimulationScenario(code: string) {
    try {
      const res = await fetch(`${API_BASE}/simulation/scenarios/${code}`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using offline scenario runner");
    }
    return null;
  },

  async analyzeEvent(payload: any) {
    try {
      const res = await fetch(`${API_BASE}/waste-events/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using offline analysis simulation");
    }
    return null;
  }
};
