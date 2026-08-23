from typing import Dict, Any

class DigitalTwinEngine:
    """
    Hospital Department Digital Twin Simulation Engine.
    Tracks department risk levels, waste accumulation volume, and Waste Stream Integrity Score (I_dept).
    """
    @staticmethod
    def calculate_integrity_score(
        anomaly_rate: float,
        uncertainty_rate: float,
        mismatch_rate: float,
        delay_rate: float
    ) -> Dict[str, Any]:
        # Integrity Score formula: 100 - penalties
        score = 100.0 - (15.0 * anomaly_rate + 10.0 * uncertainty_rate + 20.0 * mismatch_rate + 5.0 * delay_rate)
        score = max(0.0, min(100.0, score))
        
        if score >= 90.0:
            status = "STABLE"
            color = "#10B981" # Emerald
        elif score >= 75.0:
            status = "WATCH"
            color = "#3B82F6" # Blue
        elif score >= 50.0:
            status = "ATTENTION"
            color = "#F59E0B" # Amber
        else:
            status = "CRITICAL"
            color = "#EF4444" # Red
            
        return {
            "integrity_score": round(score, 1),
            "status": status,
            "color_hex": color,
            "penalty_breakdown": {
                "anomalies": round(15.0 * anomaly_rate, 1),
                "uncertainty": round(10.0 * uncertainty_rate, 1),
                "mismatches": round(20.0 * mismatch_rate, 1),
                "delays": round(5.0 * delay_rate, 1)
            }
        }
