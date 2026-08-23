from typing import Dict, Any

class RoutingEngine:
    """
    Risk-Aware Collection Priority Routing Engine.
    Formula: P_task = 0.30*Overflow + 0.25*Hazard + 0.15*Uncertainty + 0.15*Delay + 0.10*DeptCrit + 0.05*Travel
    Returns priority_score and component_values for the 'Explain Score' UI modal.
    """
    @staticmethod
    def calculate_priority(
        overflow_risk: float = 80.0,
        hazard_risk: float = 70.0,
        uncertainty_score: float = 0.50,
        delay_minutes: float = 45.0,
        dept_criticality: float = 90.0,
        travel_cost: float = 40.0
    ) -> Dict[str, Any]:
        # Normalize all inputs to scale [0, 100]
        o_val = min(100.0, overflow_risk)
        h_val = min(100.0, hazard_risk)
        u_val = min(100.0, uncertainty_score * 100.0)
        d_val = min(100.0, (delay_minutes / 120.0) * 100.0)
        c_val = min(100.0, dept_criticality)
        t_val = min(100.0, travel_cost)
        
        # Weighted components
        w_overflow = 0.30 * o_val
        w_hazard = 0.25 * h_val
        w_uncertainty = 0.15 * u_val
        w_delay = 0.15 * d_val
        w_criticality = 0.10 * c_val
        w_travel = 0.05 * t_val
        
        priority_score = round(w_overflow + w_hazard + w_uncertainty + w_delay + w_criticality + w_travel, 1)
        
        return {
            "priority_score": priority_score,
            "components": {
                "overflow_risk": round(o_val, 1),
                "hazard_risk": round(h_val, 1),
                "uncertainty": round(u_val, 1),
                "collection_delay": round(d_val, 1),
                "department_criticality": round(c_val, 1),
                "travel_cost": round(t_val, 1)
            },
            "weighted_contributions": {
                "overflow_risk": round(w_overflow, 1),
                "hazard_risk": round(w_hazard, 1),
                "uncertainty": round(w_uncertainty, 1),
                "collection_delay": round(w_delay, 1),
                "department_criticality": round(w_criticality, 1),
                "travel_cost": round(w_travel, 1)
            },
            "formula_explanation": "Priority = 0.30*Overflow + 0.25*Hazard + 0.15*Uncertainty + 0.15*Delay + 0.10*DeptCrit + 0.05*Travel"
        }
